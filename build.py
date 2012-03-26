#! /usr/bin/env python

# PREREQUISITES:
# 1.  All necessary repositories must have already been downloaded
# 2.  The regular.iso file must already be in /mnt/host

def elim_dir (dir_to_elim): 
	if (os.path.exists(dir_to_elim)):
		shutil.rmtree (dir_to_elim)

def create_dir (dir_to_create):
    if not (os.path.exists(dir_to_create)):
        os.mkdir (dir_to_create)

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
    
    dir_develop = '/home/' + uname + '/develop'
    dir_user = '/home/' + uname
    
    os.system ('mount -t vboxsf guest /mnt/host')
    base_iso = '/mnt/host/regular.iso'
    while not (os.path.isfile (base_iso)):
        print ('Could not find your ' + base_iso + 'file.')
        print ('Please go to your host OS and copy the appropriate file into')
        print ('the /home/(username)/guest directory.')
        print ('Press Enter when you are finished')
        var_dummy = raw_input ('TEST')
        os.system ('mount -t vboxsf guest /mnt/host')

    # Prepare to save the screen output
    import shutil
    dir_output = dir_develop + '/temp-output'
    elim_dir (dir_output)
    create_dir (dir_output)
    file_output = dir_output + '/build-special.txt'
    
    # Prepare the Regular Swift Linux remastering script
    os.system ('sh ' + dir_develop + '/remaster/main.sh')
    
    # Change the remastering script
    file_remaster = '/usr/lib/linuxmint/mintConstructor/mintConstructor.py'
    text_old = 'regular.iso'
    text_new = abbrev + '.iso'
    change_text (file_remaster, text_old, text_new)
    text_old = 'linuxmint-201109-gnome-dvd-32bit'
    text_new = 'regular'
    change_text (file_remaster, text_old, text_new)
    
    # Replace the line in the remastering script that 
    # calls the shared-regular.py script from chroot
    # os.system(self.chrootPrefix + 'python /usr/local/bin/develop/1-build/shared-regular.py')
    
    # chroot syntax:
    # os.system(self.chrootPrefix + 'python SCRIPT')
    
    # Commands to enter as chroot are:
    # sys.path.append (dir_develop + '/special')
    # import shared
    # shared.main (abbrev, fullname)
    
    # Syntax for entering all 3 commands as chroot:
    # 
    #
    #
    import fileinput
    for line in fileinput.input(dest,inplace =1):
        line = line.strip()
        if not 'shared-regular.py' in line:
            print line
        else:
            newpart = 'sys.path.append(dir_develop+'
            newpart = newpart + chr(39) + '/special' + chr(39) + ')\n'
            
            newpart = newpart + 'import shared\n'
            
            newpart = newpart + 'os.system(self.chrootPrefix+'
            newpart = newpart + chr(39)
            newpart = newpart
            
    
    # Execute the remastering script
