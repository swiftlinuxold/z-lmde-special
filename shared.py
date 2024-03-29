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

# Everything up to this point is common to all Python scripts called by shared-* scripts
# ======================================================================================
print "============================================================="
print "BEGIN TRANSFORMING REGULAR SWIFT LINUX INTO A SPECIAL EDITION"

abbrev = sys.argv [1]
fullname = sys.argv [2]

# Replace text in a file        
def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)
    
# Values for Regular Swift Linux
os.system ('python ' + dir_develop + '/1-build/cosmetic-regular.py')

# Wallpaper
print "Adding wallpaper"
src = dir_develop + '/edition-' + abbrev + '/login.jpg'
dest = '/usr/share/backgrounds/swift/login-' + abbrev + '.jpg'
os.system ('cp ' + src + ' ' + dest)
src = dir_develop + '/edition-' + abbrev + '/rox.jpg'
dest = '/usr/share/backgrounds/swift/rox-' + abbrev + '.jpg'
os.system ('cp ' + src + ' ' + dest)

# Sound clip
print "Adding the sound clip"
dest = '/usr/share/sounds/swift'
if not (os.path.exists(dest)):
    os.mkdir (dest)
os.system ('mkdir ' + dest)
src = dir_develop + '/edition-' + abbrev + '/*.mp3'
dest = '/usr/share/sounds/swift/sound-' + abbrev + '.mp3'
os.system ('cp ' + src + ' ' + dest)

# LightDM
print "Changing the LightDM wallpaper"
filename = '/etc/lightdm/lightdm-gtk-greeter.conf'
change_text (filename, 'login-regular.jpg', 'login-' + abbrev + '.jpg')

# Conky
print "Changing Conky"
filename = dir_user + '/.conkyrc'
change_text (filename, 'Regular Swift Linux', fullname)
filename = '/etc/skel/.conkyrc'
change_text (filename, 'Regular Swift Linux', fullname)

# ROX pinboard
print "Changing the ROX pinboard wallpaper"
filename = dir_user + '/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')
filename = '/etc/skel/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')

# IceWM startup script
print "Changing the IceWM startup script"
filename = dir_user + '/.icewm/startup'
change_text (filename, '#sound', 'mpg123 /usr/share/sounds/swift/sound-' + abbrev + '.mp3')
filename = '/etc/skel/.icewm/startup'
change_text (filename, '#sound', 'mpg123 /usr/share/sounds/swift/sound-' + abbrev + '.mp3')

# Default images for wallpaper wizards
print "Changing the default images in the wallpaper wizards"
filename = dir_user + '/.wallpaper/feh-bg.rox-ice'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')
filename = '/etc/skel/.wallpaper/feh-bg.rox-ice'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')

filename = dir_user + '/.wallpaper/feh-bg.rox-jwm'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')
filename = '/etc/skel/.wallpaper/feh-bg.rox-jwm'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')

filename = dir_user + '/.wallpaper/lightdm'
change_text (filename, 'login-regular.jpg', 'login-' + abbrev + '.jpg')
filename = '/etc/skel/.wallpaper/lightdm'
change_text (filename, 'login-regular.jpg', 'login-' + abbrev + '.jpg')

filename = dir_user + '/.wallpaper/saved'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')
filename = '/etc/skel/.wallpaper/saved'
change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')

os.system ('python ' + dir_develop + '/final/main.py')

print "FINISHED TRANSFORMING REGULAR SWIFT LINUX INTO A SPECIAL EDITION"
print "================================================================"

