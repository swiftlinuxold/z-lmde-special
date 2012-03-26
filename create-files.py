#! /usr/bin/env python

def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)
    
def copy_file (file_old, file_new, text_old, text_new):
    ret = os.access(file_new, os.F_OK)
    if (ret):
        os.remove (file_new)
    shutil.copy2 (file_old, file_new)
    change_text(file_new, text_old, text_new)
    
def elim_dir (dir_to_elim): 
    if (os.path.exists(dir_to_elim)):
        shutil.rmtree (dir_to_elim)

def create_dir (dir_to_create):
    if not (os.path.exists(dir_to_create)):
        os.mkdir (dir_to_create)

def main (abbrev, fullname):
    # Check for root user login
    import os, sys
    if os.geteuid()==0:
        sys.exit('\nYou MUST be NON-ROOT to run this script.\n')

    # Get your username (not root)
    import pwd
    uname=pwd.getpwuid(1000)[0]

    import shutil # Needed for copying files

    dir_develop = '/home/' + uname + '/develop'
    dir_special = dir_develop + '/special'
    dir_temp = dir_develop + '/temp-special'

    elim_dir (dir_temp)
    create_dir (dir_temp)

    # /1-build/build-regular.sh -> /temp-diet/build.sh
    file_special = dir_build + '/build-template.py'
    file_special = dir_temp + '/build.sh'
    text_regular = 'linuxmint-201109-gnome-dvd-32bit.iso'
    text_special = 'regular.iso'
    copy_file (file_regular, file_special, text_regular, text_special)
    print file_regular, file_special, text_regular, text_special

# Remove command to execute preinstall.sh
import fileinput
for line in fileinput.input (file_diet,inplace =1):
    line = line.strip()
    if not 'preinstall' in line:
        print line 

text_regular = '$DIR_DEVELOP/remaster/main.sh'
text_diet = '$DIR_DEVELOP/temp-diet/remaster.sh'
change_text (file_diet, text_regular, text_diet)

# /remaster/main.sh -> /temp-diet/remaster.sh
file_regular = dir_develop + '/remaster/main.sh'
file_diet = dir_temp + '/remaster.sh'
text_regular = 'python $FILE2'

text_diet = 'sed -i ' + chr(39)
text_diet = text_diet + 's/regular.iso/diet.iso/g' + chr (39)
text_diet = text_diet + ' $FILE2\n\n'

text_diet = text_diet + 'sed -i ' + chr(39)
text_diet = text_diet + 's/linuxmint-201109-gnome-dvd-32bit/regular/g' + chr(39)
text_diet = text_diet + ' $FILE2\n\n'

text_diet = text_diet + 'sed -i ' + chr(39)
text_diet = text_diet + 's/1-build/diet/g' + chr (39)
text_diet = text_diet + ' $FILE2\n\n'

text_diet = text_diet + 'sed -i ' + chr(39)
text_diet = text_diet + 's/shared-regular/shared/g' + chr (39)
text_diet = text_diet + ' $FILE2\n\n'

text_diet = text_diet + text_regular
copy_file (file_regular, file_diet, text_regular, text_diet)
