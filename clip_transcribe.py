import openai
import whisper
import os
import pickle
import glob
import shelve
import sys

"""
What I do:
Read the clips. Extract wav files. Creates clip objects which
contains, file name, transcribe data. Opens tk windows one for
each clip showing texts.  User can choose the texts in order as
1, 2, 3 according to film script.
"""

# define this before first running the code
#projectName = "chat_room"
projectName = sys.argv[1]

# the absolute path of the folder containing this py file
rootDir = os.path.dirname((os.path.abspath(__file__)))

clipObjList = []

def transcribeMe(obj):
    """
    obj is the clipObj 
    """
    model = whisper.load_model("base")
    result = model.transcribe(obj.fileName)
    print(result)
    #text = [x +'\n' for x in result['text']]
    #with open(fname, 'w') as f:
    #    f.writelines(result['text'])

    segment_len = len(result['segments'])

    for id_ in range(segment_len):
        print(id_, result['segments'][id_]['text']) 

    # asbolute pickle path
    pickleFile = os.path.join(rootDir, 'result.pkl')
    pickle.dump(result, open(pickleFile, 'wb'))

    obj.result = result

# older version of cutMe; not used here
def cutMe(obj, count):
    #result = pickle.load(open('./result.pkl', 'rb'))
    result = obj.result

    # read cut points as a space separated string
    id_list = input('enter ids with space: ').rstrip().split()
    id_list = [int(x) for x in id_list]

    # total segments
    segment_len = len(result['segments'])

    # file being processed
    #fname = 'comedy-broken-speech-MVI_0138.MOV'

    # for ouput file name
    #count = 1

    # finding matching ids to get start and end time
    for id_ in id_list:
        for seg in result['segments']:
            if seg['id'] == id_:
                print(seg)
                start = seg['start']
                # updating start and end to avoid overlap
                start -= 0
                end = seg['end']
                end -= 0
                duration = end - start
                # absolute output path
                outputDir = os.path.join(rootDir, 'output')
                outfile = outputDir + str(count) + '.mov'
                count += 1
                # command to run
                cmd = 'ffmpeg -i ' + fname 
                cmd += ' -ss ' + str(start) + ' ' + ' -t ' + str(duration)
                cmd += ' ' + outfile
                print(cmd)
                os.system(cmd)
                break
    return count

class clipObj:
    """
    Stores all clip data updated
    as we go
    """
    def __init__(self, fileName):
        self.fileName = fileName

# absolute output path
outputDir = os.path.join(rootDir, 'output')
# make output folder if doesn't exist
if os.path.exists(outputDir):
    for file in os.listdir(outputDir):
        os.remove(os.path.join(outputDir, file ))
else:
    os.mkdir(outputDir)

# avoids re-transcribing
shelveName = projectName + '.db'
shelveFile = os.path.join(rootDir, shelveName)
print(shelveFile)
# absoluted input dir
inputDir = os.path.join(rootDir, 'input')
if not os.path.exists(shelveFile):

    fileList = glob.glob(inputDir + '/*.MOV')
    for file_ in fileList:
        obj = clipObj(file_)
        clipObjList.append(obj)

    for obj in clipObjList:
        transcribeMe(obj)

else:
    # absolute path without .db
    dbFile = os.path.join(rootDir, projectName)
    db = shelve.open(dbFile)
    clipObjList = db['objlist']
    db.close()


# first window root
# rest Toplevel
windowCount = 0
#from entry3 import makeform, fetch
from my_dynamic_tk_entry_007 import makeform, fetch
from quitter import Quitter
from tkinter import *

root = Tk()

for obj in clipObjList:

    #obj = clipObjList[0]
    segment_len = len(obj.result['segments'])
    fields = [obj.result['segments'][id_]['text'] for  id_ in range(segment_len)]
    print(fields)

    if windowCount > 0:

        top = Toplevel()
        vars = makeform(top, fields, obj)
        #Button(top, text='Fetch', command=(lambda obj=obj: fetch(vars, obj))).pack(side=LEFT)
        Quitter(top).pack(side=RIGHT)
        #top.bind('<Return>', (lambda event: fetch(vars, obj)))
    else:
        vars = makeform(root, fields, obj)
        #Button(root, text='Fetch', command=(lambda obj=obj: fetch(vars, obj))).pack(side=LEFT)
        Quitter(root).pack(side=RIGHT)
        #root.bind('<Return>', (lambda event: fetch(vars, obj)))

    windowCount += 1

root.mainloop()

#print(obj.choices)
for obj in clipObjList:
    print(obj.choices)


# creating shelve object 
# absolute path
cliobjlistdb = os.path.join(rootDir, 'clipobjlist')
db = shelve.open(cliobjlistdb)
db['objlist'] = clipObjList
db.close()

# creating shelve object to avoid repeating
# absolute path
projectdb = os.path.join(rootDir, projectName) 
db = shelve.open(projectdb)
db['objlist'] = clipObjList
db.close()
