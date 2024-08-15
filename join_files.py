import os
import time

totalFiles = len(os.listdir('./output'))
print(totalFiles, os.listdir('./output'))
lines = []
for i in range(totalFiles):
    if i == totalFiles - 1:
        fName = 'file output/' + str(i + 1) + '.mov' + '\n'
    else:
        fName = 'file output/' + str(i + 1) + '.mov' + '\n'
    lines.append(fName)

f  = open('file_list.txt', 'w')
f.writelines(lines)
f.close()
    
outfile = 'rendered_' + str(time.time()) + '_.mov'
cmd = 'ffmpeg -f concat -safe 0  -i ' + 'file_list.txt'
cmd += ' -c copy ' + outfile
print(cmd)
os.system(cmd)

