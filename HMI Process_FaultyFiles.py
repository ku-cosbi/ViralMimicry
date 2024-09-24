# Some HMI-PRED output files are written in a different way, reason unknown. This code is used to convert them to the expected file version. 
import pandas as pd
import glob
folder_to_results = 'single_line_hmi_output'
for file in glob.glob(folder_to_results + '/*'):
    file_name = (file.split('/')[-1])
    with open(file, 'r') as f:
        fixed_file = open(file_name, 'w')
        lines = f.readlines()
        new_header = ''
        if ('Microbe' in lines[0]) and ('Microbial' in lines[1]) and ('I_SC' in lines[9]):
            for i in range(12):
                new_header += lines[i].strip()
                new_header +='\t'
            fixed_file.write(new_header)
            fixed_file.write('\n')

            for j in range(12, len(lines),2):

                fixed_file.write(lines[j].strip() + '\t'+ lines[j+1].strip())
                fixed_file.write('\n')
        else:
            for m in lines:
                fixed_file.write(m)
