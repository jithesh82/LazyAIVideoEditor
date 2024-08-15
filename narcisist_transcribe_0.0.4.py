import openai
import whisper
import os
import pickle
import glob


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

    pickle.dump(result, open('result.pkl', 'wb'))

    obj.result = result


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
                outfile = './output/' + str(count) + '.mov'
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

# make output folder if doesn't exist
if os.path.exists('./output'):
    for file in os.listdir('./output'):
        os.remove(os.path.join('./output', file ))
else:
    os.mkdir('./output')

fileList = glob.glob('./input/*.MOV')
for file_ in fileList:
    obj = clipObj(file_)
    clipObjList.append(obj)

for obj in clipObjList:
    transcribeMe(obj)
    

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

#with open('clip_obj_list.pkl', 'wb') as f:
#    pickle.dump(clipObjList, f)

import shelve
db = shelve.open('clipobjlist')
db['objlist'] = clipObjList
db.close()

