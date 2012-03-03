#! /usr/bin/env python

# Replace text in a file        
def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)

def main (abbrev, fullname):
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

    # Wallpaper
    src = dir_develop + '/edition-' + abbrev + '/login.jpg'
    dest = '/usr/share/backgrounds/swift/login-' + abbrev + '.jpg'
    os.system ('cp ' + src + ' ' + dest)
    src = dir_develop + '/edition-' + abbrev + '/rox.jpg'
    dest = '/usr/share/backgrounds/swift/rox-' + abbrev + '.jpg'
    os.system ('cp ' + src + ' ' + dest)
    # Sound clip
    dest = '/usr/share/sounds/swift'
    os.system ('mkdir ' + dest)
    src = dir_develop + '/edition-' + abbrev + '/*.mp3'
    dest = '/usr/share/sounds/swift/sound-' + abbrev + '.mp3'
    os.system ('cp ' + src + ' ' + dest)
    # LightDM
    filename = '/etc/lightdm/lightdm-gtk-greeter.conf'
    change_text (filename, 'login-regular.jpg', 'login-' + abbrev + '.jpg')
    # Conky
    filename = dir_user + '/.conkyrc'
    change_text (filename, 'Regular Swift Linux', fullname)
    filename = '/etc/skel/.conkyrc'
    change_text (filename, 'Regular Swift Linux', fullname)
    # ROX pinboard
    filename = dir_user + '/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
    change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')
    filename = '/etc/skel/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
    change_text (filename, 'rox-regular.jpg', 'rox-' + abbrev + '.jpg')
