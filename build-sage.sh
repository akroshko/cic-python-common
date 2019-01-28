#!/bin/bash
# THIS FILE IS ORIGINALLY FROM https://github.com/akroshko/python-stdlib-personal
# but often copied elsewhere.
# DO NOT EDIT DIRECTLY IF NOT IN python-stdlib-personal

# Copyright (C) 2016-2018, Andrew Kroshko, all rights reserved.
#
# Author: Andrew Kroshko
# Maintainer: Andrew Kroshko <akroshko.public+devel@gmail.com>
# Created: Thu Aug 09, 2018
# Version: 20181126
# URL: https://github.com/akroshko/python-stdlib-personal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

# TODO: add some warn yell ???

# the three-fingered claw, see https://stackoverflow.com/questions/1378274/in-a-bash-script-how-can-i-exit-the-entire-script-if-a-certain-condition-occurs
yell () {
    local NEWCOM=$(sed -r 's|'"$HOME"'|~|g' <<< "$0")
    echo -e "${BRed}$NEWCOM${Red}: $*${Color_Off}" >&2
}

die () {
    yell "$*"; exit 111
}

try () {
    "$@" || die "cannot $*"
}

warn () {
    # XXXX: not good because it starts up a new command, but avoids escaping slashes
    local NEWCOM=$(sed -r 's|'"$HOME"'|~|g' <<< "$0")
    echo -e "${BYellow}$NEWCOM${Yellow}: $*${Color_Off}" >&2
}

msg () {
    local NEWCOM=$(sed -r 's|'"$HOME"'|~|g' <<< "$0")
    echo -e "${BGreen}$NEWCOM${Green}: $*${Color_Off}" >&2
}

ask_yn () {
    local YN=
    while [[ "$YN" != 'y' && "$YN" != 'n' ]]; do
        while read -r -t 0;do read -r; done
        read -n 1 -p "$1 (y/n)? " YN
        echo ""
    done
    if [[ "$YN" == 'y' ]]; then
        return 0
    elif [[ "$YN" == 'n' ]]; then
        return 1
    fi
}

fetch-build-sage-nice () {
    /usr/bin/nice --adjustment 20 /usr/bin/ionice -c3 fetch-build-sage
}

export DEFAULT_SAGEVERSION="8.4"
export DEFAULT_SAGEVERSIONMD5="8f883a26f6ff2482b415151b82e22548"
# export DEFAULT_SAGEVERSION="8.3"
# export DEFAULT_SAGEVERSIONMD5="32b5eddff38f8215093b9c645763c904"
# TODO: using older version of Sage for compatibility
# export DEFAULT_SAGEVERSION="8.0"
# export DEFAULT_SAGEVERSIONMD5="93bdd128991e9144c4b137d3d6655065"

# TODO: reverse these...
fetch-build-sage () {
    # fetch and compile current version of sage
    # usage: use --finalize to finalize the setup
    # XXXX: need to set sage variables elsewhere
    # TODO: check for valid installation
    if [[ -z "$SAGEVERSION" || -z "$SAGEVERSIONMD5" ]]; then
        msg "Using default of Sage version $DEFAULT_SAGEVERSION with an md5 checksum of $DEFAULT_SAGEVERSIONMD5"
        # update for every new version sage
        local SAGEVERSION="$DEFAULT_SAGEVERSION"
        local SAGEVERSIONMD5="$DEFAULT_SAGEVERSIONMD5"
    fi
    if [[ -n "$SAGEMIRROR" && -n "$SAGELOCATION" ]];then
       yell "Cannot specify both SAGEMIRROR and SAGELOCATION at the same time!!!"
    elif [[ -z "$SAGEMIRROR" ]]; then
        local SAGEMIRROR="http://www.cecm.sfu.ca/sage/src/"
    elif [[ -z "$SAGELOCATION" ]]; then
        # TODO: put this somewhere else and check for errors
        local SAGELOCATION="$PYMATHDBTMP/"
    fi
    if [[ -d /opt/sage-"$SAGEVERSION" && $@ != *"--finalize"* ]]; then
        if /opt/sage-"$SAGEVERSION"/sage --version; then
            warn "/opt/sage-$SAGEVERSION already present and appears functional"
        else
            yell "/opt/sage-$SAGEVERSION present but appears non-functional"
        fi
        return 1
    fi
    sudo true || return 1
    if [[ $@ != *"--finalize"* ]]; then
        sudo apt-get update
        sudo apt-get install gcc gnutls-bin gnutls-doc imagemagick libssl-dev libssl-doc libcurl4-gnutls-dev libgnutls28-dev make m4 opencl-headers perl python
        if [[ ! $@ == *"--no-x11"* ]]; then
            sudo apt-get install dvipng ocl-icd-opencl-dev tk8.6-dev texlive
        else
            sudo apt-get install ocl-icd-opencl-dev --no-install-recommends
        fi
        pushd . >/dev/null
        if [[ -e "${SAGELOCATION}/sage-${SAGEVERSION}.tar.gz" ]]; then
            cd "$SAGELOCATION"
            msg "Sage tarball already found in standard location!"
        else
            # TODO: put into ~/tmp for more universal use
            # TODO: proper error message if md5sum is not good
            if [[ ! -e "$HOME/tmp/sage-download/sage-${SAGEVERSION}.tar.gz" || ! $(md5sum "$HOME/tmp/sage-download/sage-${SAGEVERSION}.tar.gz" | cut -d' ' -f1) == "$SAGEVERSIONMD5" ]]; then
                msg "Downloading Sagemath tarball!"
                mkdir -p "$HOME/tmp/sage-download"
                cd "$HOME/tmp/sage-download"
                # should I delete this?
                # TODO: does the tarball already exist?
                #       do not delete directory in this case
                wget -O "sage-$SAGEVERSION.tar.gz" "$SAGEMIRROR/sage-$SAGEVERSION.tar.gz"
                msg "Finished downloading!"
            else
                msg "Sagemath tarball already downloaded!"
                cd "$HOME/tmp/sage-download"
            fi
        fi
        MD5SUMCURRENT=$(md5sum sage-"$SAGEVERSION".tar.gz | cut -d' ' -f1)
        echo "\"$MD5SUMCURRENT\" should be \"$SAGEVERSIONMD5\""
        if [[ "$MD5SUMCURRENT" != "$SAGEVERSIONMD5" ]]; then
            yell "md5 sum incorrect!"
            popd >/dev/null
            return 1
        fi
        msg "md5 sum correct!"
        msg "Unpacking!"
        if [[ -d "sage-$SAGEVERSION" ]]; then
            rm -rf "sage-$SAGEVERSION"
        fi
        tar xvzf "sage-${SAGEVERSION}.tar.gz"
        # check installation
        msg "Sage unpacked.  Answer 'y' to move installation directory to /opt and continue with build or 'n' to quit."
        ask_yn
        local YN=$?
        if [[ "$YN" == 0 ]]; then
            sudo mkdir -p /opt
            sudo mv "./sage-${SAGEVERSION}" /opt
            cd "/opt/sage-${SAGEVERSION}"
        else
            popd >/dev/null
            return 1
        fi
        # make sure I don't overload my underpowered portable computers
        if [[ $@ == *"-j1"* ]]; then
            MAKE='make -j1' time make
        elif [[ $@ == *"-j2"* ]]; then
            MAKE='make -j2' time make
        else
            MAKE='make -j4' time make
        fi
        # TODO: option to just finalize
        while read -r -t 0;do read -r; done
        msg "Sage installed. Answer 'y' to finalize installation or 'n' to quit."
        ask_yn
        local YN2=$?
    else
        local YN2=0
        pushd . >/dev/null
        cd "/opt/sage-${SAGEVERSION}"
    fi
    # TODO: make sure I can rerun this if necesssary
    # TODO: make an upgrade, find out if this does not work, make sure it does
    # TODO: possibly upgrade twisted
    if [[ "$YN2" == 0 ]]; then
        msg "Running Sage, manually exit when done"
        ./sage
        # build packages
        fetch-build-sage-packages
        # make docs
        if [[ ! $@ == *"--no-x11"* ]]; then
            make doc
        fi
        # TODO: overwrite binary, but ask first
        if [[ -e /usr/local/bin/sage ]]; then
            sudo rm /usr/local/bin/sage
        fi
        if [[ -e "/opt/sage-${SAGEVERSION}/sage" ]]; then
            sudo ln -s "/opt/sage-${SAGEVERSION}/sage" /usr/local/bin
        else
            yell "Cannot find /opt/sage-${SAGEVERSION}/sage so not symlinkiing to /usr/local/bin/sage"
        fi
    else
        echo "Not finalizing!  Can be done later with --finalize"
        popd >/dev/null
        return 1
    fi
    # try running sage
    msg "Running Sage, manually exit when done"
    ./sage
    msg "Installation done!"
    popd >/dev/null
}

fetch-build-sage-packages () {
    # be in sage directory, the ./sage is safety for this
    # http://doc.sagemath.org/html/en/reference/misc/sage/misc/package.html
    ./sage -i openssl
    ./sage -pip install --upgrade pip
    ./sage -pip install --upgrade service_identity
    ./sage -pip install --upgrade dill
    ./sage -pip install --upgrade lxml
    ./sage -pip install --upgrade multiprocess
    # out of date pillow has been an issue for me before
    ./sage -pip install --upgrade pillow
    ./sage -pip install --upgrade psycopg2-binary
    ./sage -pip install --upgrade pycurl
    ./sage -pip install --upgrade pyopenssl
    # ./sage -pip install --upgrade rlipython
    ./sage -pip install --upgrade readline
    # install sage mode
    # TODO: remove, does not seem to exist, try melpa
    # ./sage -i sage_mode
    # TODO: I can replace most of my keys now
    # echo "Setting up rlipython!"
    # ./sage -ipython -c "import rlipython;rlipython.install()"
}

main () {
    # TODO: this might be an issue with just -h in this way at some point
    if [[ $@ != *"--install"* || $@ == *"--help"* || $@ == *"-h"* ]]; then
        echo "Usage: "
        echo ""
        echo "--install"
        echo "  Do the installation for real."
        echo ""
        echo "--no-x11"
        echo "  Do not install with X11 dependencies"
        echo "  The main effect is that documentation will not be built"
        echo ""
        echo "--finalize"
        echo "  Just finalize, trying to install optional packages"
        echo ""
        echo "-j1"
        echo "  Use one process for building Sage"
        echo "  Useful for laptops and other computers with limited computational power, memory, or thermal managment"
        echo ""
        echo "-j2"
        echo "  Use two processes for building Sage"
        echo "  Useful for dual-core desktops and quad-core computers with limited computational power, memory, or thermal managment"
        echo ""
        echo "-j4 (default)"
        echo "  Use four processes for building Sage"
        echo "  Useful for quad-core computers where -j8 is slow or leads to lockups"
        echo ""
        echo "-j8"
        echo "  Use eight processes for building Sage"
        echo "  Useful for four core/eight thread computers where it can provide an advantage"
        echo ""
        echo "Environment variables:"
        echo ""
        echo "SAGEVERSION:    The Sage version to install, (default $DEFAULT_SAGEVERSION)"
        echo "                Must specific SAGEVERSIONMD5 with SAGEVERSION"
        echo "SAGEVERSIONMD5: The md5 checksum of the Sage version to install, (default $DEFAULT_SAGEVERSIONMD5)"
        echo "                Must specific SAGEVERSION with SAGEVERSIONMD5"
        echo "SAGEMIRROR:     The url of the Sage mirror to use, e.g., http://www.cecm.sfu.ca/sage/src/"
        echo "                Mutually exclusive to SAGELOCATION"
        echo "SAGELOCATION:   The directory in the filesystem where the Sage tarball is located"
        echo "                Mutually exclusive to SAGEMIRROR"
    else
        fetch-build-sage "$@"
    fi
}

main "$@"
