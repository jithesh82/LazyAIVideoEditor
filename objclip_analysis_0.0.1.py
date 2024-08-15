import shelve
import os
#from narcisist_transcribe_004 import cutMe

# make output folder if doesn't exist
if os.path.exists('./output'):
    for file in os.listdir('./output'):
        os.remove(os.path.join('./output', file))
#os.mkdir('./output')

def cutMe(obj, count=1):
    #result = pickle.load(open('./result.pkl', 'rb'))
    result = obj.result
    choices = obj.choices

    # extract all non-zero elements from choices to create id_list
    #id_list = [int(id_) for id_ in choices if id_ != '0']

    # extracting ids from user choices -> id = index(user_choice)
    id_list = []
    choiceNos = [] # corresponding user choice numbers
    for i in range(len(choices)):
        if choices[i] != '0':
            id_list.append(i)
            choiceNos.append(choices[i])

    # read cut points as a space separated string
    #id_list = input('enter ids with space: ').rstrip().split()
    #id_list = [int(x) for x in id_list]

    # total segments
    segment_len = len(result['segments'])

    # file being processed
    #fname = 'comedy-broken-speech-MVI_0138.MOV'

    # for ouput file name
    #count = 1

    # finding matching ids to get start and end time
    for i in range(len(id_list)):
        for seg in result['segments']:
            id_ = id_list[i]
            if seg['id'] == id_:
                print(seg)
                start = seg['start']
                # updating start and end to avoid overlap
                start -= 0
                end = seg['end']
                end -= 0
                duration = end - start
                # count is user entered value from obj.choices
                count = choiceNos[i] 
                outfile = './output/' + str(count) + '.mov'
                #file name
                fname = obj.fileName
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

db = shelve.open('clipobjlist')
print(list(db.keys()))
print(db['objlist'][0].result)

for obj in db['objlist']:
    cutMe(obj)

db.close()
