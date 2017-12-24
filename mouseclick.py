#!/usr/bin/python
import os,sys
import math as m

# based on mouseclick.sh from https://sourceforge.net/projects/xulpdftex/
# TODO: add a license, respect original
# TODO: clean up messaging, but be informative

def main(argv):
    os.system('launch-emacsclient noframe --eval "(message \\"mouseclick.py ' + sys.argv[1] + ',' + sys.argv[2] + ',' + sys.argv[3] + ',' + sys.argv[4] + '\\")"')
    # get the arguments for xcoord and ycoord
    xcoord=int(float(argv[3])*65536)
    ycoord=int(float(argv[4])*65536)
    bname=os.path.basename(os.path.splitext(argv[1])[0])
    pwd=os.getcwd()
    pnum=int(argv[2])
    pline=0
    # open file
    fh=open(os.path.join(pwd,bname+'.pdfsync'),'r')
    # read lines
    mindist=1000000000
    celement=-1
    # read again
    # get range for a page
    for theline in fh.readlines():
        # look for the appropriate page
        if theline.startswith('s') and int(theline.split()[1]) <= pnum:
            match_line=theline
        elif theline.startswith('s') and int(theline.split()[1]) > pnum:
            break
    # now go to the beginning position
    fh.seek(0)
    started=False
    # get closest element on a page
    for theline in fh.readlines():
        if not started and theline == match_line:
            started=True
        elif started and theline.startswith('s') and len(theline.split()) > 1 and int(theline.split()[1]) > pnum:
            # we are done now
            break
        if started:
            thetype = theline.split()[0]
            if thetype == 'p':
                pxcoord=int(theline.split()[2])
                pycoord=int(theline.split()[3])
                cdist=m.sqrt((pxcoord-xcoord)**2.+(pycoord-ycoord)**2.)
                if cdist < mindist:
                    celement=int(theline.split()[1])
                    mindist=cdist
    print
    # now just grep
    fh.seek(0)
    for theline in fh.readlines():
        if theline.startswith('l') and int(theline.split()[1]) == celement:
            latexline=int(theline.split()[2])
    fh.close()
    # now launch emacs client after calculating lnum
    os.system('launch-emacsclient noframe --eval "(message \\"Info: ' + str(mindist) + ',' + str(celement) + '\\")"')
    os.system('launch-emacsclient noframe --eval "(message \\"LaTeX line: ' + str(latexline) + '\\")"')
    os.system('launch-emacsclient noframe --eval "(progn (switch-to-buffer \\"' + bname + '.tex\\") (goto-char (point-min)) (forward-line (1- ' + str(latexline) + ')) (recenter-top-bottom))"')
    os.system('launch-emacsclient noframe --eval "(message \\"Inverse search complete!!!\\")"')

if __name__ == '__main__':
    main(sys.argv)
