import subprocess
import glob
import os

# Rename results files so it wont overwrite when moved to the same file
count = 1
for dir in glob.glob('/Users/fatmacankara/Desktop/HMI/*'):
    for subdir in glob.glob(f'{dir}/*'):
        if subdir.split('/')[-1] == 'results.txt':
            os.rename(subdir, subdir+str(count))
    count +=1
    
# Move to a file to we can merge them.
# go into the folder of subfolders
#find . -name "*results*" -type f -exec cp "{}" "destination" \;
# Merge all results.
#cat * > ..txt
