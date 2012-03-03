#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

import shutil

# LightDM wallpaper
src = dir_develop + '/ui-login/etc_lightdm/lightdm-gtk-greeter.conf'
dest = '/etc/lightdm/lightdm-gtk-greeter.conf'
shutil.copyfile(src, dest)

# Conky
src = dir_develop + '/ui-de/dotconkyrc/conkyrc-regular'
dest = dir_user + '/.conkyrc'
shutil.copyfile(src, dest)
dest = '/etc/skel/.conkyrc'
shutil.copyfile(src, dest)

# ROX pinboard
src = dir_develop+'/ui-de/ROX-Filer/pb_swift'
dest = dir_user + '/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
shutil.copyfile(src, dest)
dest = '/etc/skel/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
shutil.copyfile(src, dest)
import fileinput
for line in fileinput.input(dest,inplace =1):
    line = line.strip()
    if not 'debian-installer-launcher' in line:
        print line 

# IceWM startup
src = dir_develop + '/ui-de/etc_X11_icewm/startup'
dest = dir_user + '/.icewm/startup'
shutil.copyfile(src, dest)
os.system ('chmod a+rwx ' + dest)
dest = '/etc/X11/icewm/startup'
shutil.copyfile(src, dest)
os.system ('chmod a+rwx ' + dest)
dest = '/etc/skel/.icewm/startup'
shutil.copyfile(src, dest)
os.system ('chmod a+rwx ' + dest)
