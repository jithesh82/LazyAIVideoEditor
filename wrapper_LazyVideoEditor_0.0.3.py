import os
from tqdm import tqdm
import glob

"""
clean, transcribe, combine clips for final touch up
"""

projectName = 'breeze'

# the main directory under work folder
projectDir = '/home/jk/jk/work/' + projectName

run = True

if run:

    # cleaning  and 
    # copying rode-mic audio to prepare-video/rode-mic
    print('cleaning rode-mic folder ...')
    rodeMicFile = os.path.join(projectDir, projectName + '.wav')
    prepVideoRodeMicDir = '/home/jk/jk/python/LazyVideoEditor0.0.4/prepare_videos/rode-mic' 
    for file_ in os.listdir(prepVideoRodeMicDir):
        fullPath = os.path.join(prepVideoRodeMicDir, file_)
        if os.path.isfile(fullPath):
            os.remove(fullPath)
    print('copying the rode-mic file .....')
    cmd = 'cp ' + rodeMicFile + ' ' + prepVideoRodeMicDir
    os.system(cmd)

    # path to prepare video - start point directory
    raw_video = '/home/jk/jk/python/LazyVideoEditor0.0.4/prepare_videos/raw-video' 
    print('removing files in raw_video')
    for file in tqdm(os.listdir(raw_video)):
        fullPath = os.path.join(raw_video, file)
        if os.path.isfile(fullPath):
            os.remove(fullPath)

    # copy files from projectDir to raw-video for processing
    pattern = projectDir + '/' + '*.MOV'
    print(pattern)
    print('copying files from ', projectDir, ' to ', raw_video)
    for file in tqdm(glob.glob(pattern)):
        cmd = 'cp ' + file + ' ' + raw_video
        os.system(cmd)

    # start preprocessing the video - audio replace with rode-audio
    processPY = '~/jk/python/LazyVideoEditor0.0.4/prepare_videos/prepare_videos_0.0.4.py'
    print('starting processing video/audio files')
    cmd = 'python ' + processPY
    os.system(cmd)

    # clean the input directory in LazyVideoEditor Folder and copy processed files
    print("cleaning input dir in LazyVideoEditor.....")
    lazyInputDir = '/home/jk/jk/python/LazyVideoEditor0.0.4/input' 
    os.makedirs(lazyInputDir, exist_ok=True)
    for file_ in os.listdir(lazyInputDir):
        fullPath = os.path.join(lazyInputDir, file_)
        if os.path.isfile(fullPath):
            os.remove(fullPath)
    # copy files from prepare_videos/input to LazyVideoEditor/input
    print('copying the processed files.....')
    prepVideoInputDir = '/home/jk/jk/python/LazyVideoEditor0.0.4/prepare_videos/input' 
    pattern = prepVideoInputDir + '/*.MOV'
    for file_ in glob.glob(pattern):
        cmd = 'cp ' + file_ + ' ' + lazyInputDir 
        os.system(cmd)

    # transcribe and choose and create clipobjects
    transcribeClipPY = "~/jk/python/LazyVideoEditor0.0.4/narcisist_transcribe_0.0.5.py"
    print('starting to transcribe ......')
    cmd = 'python ' + transcribeClipPY + ' ' + projectName 
    os.system(cmd)

    # running the clipobj analyzer
    print("running clip object analyzer......")
    clipObjectAnalyzePY = "~/jk/python/LazyVideoEditor0.0.4/objclip_analysis_0.0.2.py"
    cmd = "python " + clipObjectAnalyzePY
    os.system(cmd)

# running join files 
print("joing files to final video ......")
joinFilesPY = "~/jk/python/LazyVideoEditor0.0.4/join_files_0.0.1.py"
cmd = "python " + joinFilesPY
os.system(cmd)
