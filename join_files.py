import os
import time
import sys
import shutil

projectName = sys.argv[1]

# the absolute path of the folder containing this py file
rootDir = os.path.dirname((os.path.abspath(__file__)))

# absolute path
outputDir = os.path.join(rootDir, 'output')
totalFiles = len(os.listdir(outputDir))
print(totalFiles, os.listdir(outputDir))
lines = []
for i in range(totalFiles):
    if i == totalFiles - 1:
        fName = 'file ' + os.path.join(outputDir,  str(i + 1) + '.mov') + '\n'
    else:
        fName = 'file ' + os.path.join(outputDir, str(i + 1) + '.mov') + '\n'
    lines.append(fName)

f  = open('file_list.txt', 'w')
f.writelines(lines)
f.close()

# absolute outfile
outfile = 'rendered_' + str(time.time()) + '_.mov'
outfile = os.path.join(rootDir, outfile)
cmd = 'ffmpeg -f concat -safe 0  -i ' + 'file_list.txt'
cmd += ' -c copy ' + outfile
print(cmd)
os.system(cmd)

# copy the final file to project folder
shutil.copy(outfile, '/home/jk/jk/work/' + projectName + '/' + os.path.basename(outfile))
