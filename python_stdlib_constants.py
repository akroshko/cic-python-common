#!/usr/bin/env python
#####################################################################################
## some constants that might be necessary

## copied from my bash-stdlib library and modified for Python
# https://wiki.archlinux.org/index.php/Color_Bash_Prompt
# Reset
Color_Off='\33[0m'       # Text Reset
# Regular Colors
Black='\33[0;30m'        # Black
Red='\33[0;31m'          # Red
Green='\33[0;32m'        # Green
Yellow='\33[0;33m'       # Yellow
Blue='\33[0;34m'         # Blue
Purple='\33[0;35m'       # Purple
Cyan='\33[0;36m'         # Cyan
White='\33[0;37m'        # White
# Bold
BBlack='\33[1;30m'       # Black
BRed='\33[1;31m'         # Red
BGreen='\33[1;32m'       # Green
BYellow='\33[1;33m'      # Yellow
BBlue='\33[1;34m'        # Blue
BPurple='\33[1;35m'      # Purple
BCyan='\33[1;36m'        # Cyan
BWhite='\33[1;37m'       # White
# Underline
UBlack='\33[4;30m'       # Black
URed='\33[4;31m'         # Red
UGreen='\33[4;32m'       # Green
UYellow='\33[4;33m'      # Yellow
UBlue='\33[4;34m'        # Blue
UPurple='\33[4;35m'      # Purple
UCyan='\33[4;36m'        # Cyan
UWhite='\33[4;37m'       # White
# Background
On_Black='\33[40m'       # Black
On_Red='\33[41m'         # Red
On_Green='\33[42m'       # Green
On_Yellow='\33[43m'      # Yellow
On_Blue='\33[44m'        # Blue
On_Purple='\33[45m'      # Purple
On_Cyan='\33[46m'        # Cyan
On_White='\33[47m'       # White
# High Intensity
IBlack='\33[0;90m'       # Black
IRed='\33[0;91m'         # Red
IGreen='\33[0;92m'       # Green
IYellow='\33[0;93m'      # Yellow
IBlue='\33[0;94m'        # Blue
IPurple='\33[0;95m'      # Purple
ICyan='\33[0;96m'        # Cyan
IWhite='\33[0;97m'       # White
# Bold High Intensity
BIBlack='\33[1;90m'      # Black
BIRed='\33[1;91m'        # Red
BIGreen='\33[1;92m'      # Green
BIYellow='\33[1;93m'     # Yellow
BIBlue='\33[1;94m'       # Blue
BIPurple='\33[1;95m'     # Purple
BICyan='\33[1;96m'       # Cyan
BIWhite='\33[1;97m'      # White
# High Intensity backgrounds
On_IBlack='\33[0;100m'   # Black
On_IRed='\33[0;101m'     # Red
On_IGreen='\33[0;102m'   # Green
On_IYellow='\33[0;103m'  # Yellow
On_IBlue='\33[0;104m'    # Blue
On_IPurple='\33[10;95m'  # Purple
On_ICyan='\33[0;106m'    # Cyan
On_IWhite='\33[0;107m'   # White
