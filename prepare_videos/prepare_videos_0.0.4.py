import librosa
import os
import audalign
from pdb import set_trace as trace
import noisereduce
import soundfile
from pydub import AudioSegment
from pydub.effects import normalize 
from tqdm import tqdm

"""
extract audio
find the duration using librosa
optional: remove noise using noisereduce
find shift using audalign
cut the audio from rode - based up on start=shift duration=duration
replace the video-audio with cut rode audio
"""

# choose to replace with normalized or raw rode-audio
chooseNormalized = True

# the absolute path of the folder containing this py file
rootDir = os.path.dirname((os.path.abspath(__file__)))

# create these directories if doesn't exist
outDirs = ['extracted-audio', 'input', 'noise-reduce', 'processed-audio', 'normalized']
# make it absolute
outDirs = [os.path.join(rootDir, dir_) for dir_ in outDirs]

for dir_ in outDirs:
    os.makedirs(dir_, exist_ok=True) # make it if doesn't exist
# make sure these directories are clean
for dir_ in outDirs:
    for file_ in os.listdir(dir_):
        fullPath = os.path.join(dir_, file_)
        if os.path.isfile(fullPath):
            os.remove(fullPath)

# absolute paths for folders in use
rawVideoDir = os.path.join(rootDir, 'raw-video')
extractedAudioDir =  os.path.join(rootDir, 'extracted-audio')
noiseReduceDir = os.path.join(rootDir, 'noise-reduce')
rodeMicDir = os.path.join(rootDir, 'rode-mic')
processedAudioDir = os.path.join(rootDir,  'processed-audio')
normalizedDir = os.path.join(rootDir, 'normalized')
inputDir = os.path.join(rootDir, 'input')


for videoFile in tqdm(os.listdir(rawVideoDir)):
    # extract audio from video clip - shell
    #videoFile = 'camels-tent-MVI_0090.MOV'
    file = os.path.join(rawVideoDir, videoFile)
    # file name without extension and directory
    #fileRootName = os.path.splitext(os.path.basename(file))[0]
    fileRootName = os.path.splitext(videoFile)[0]
    # with extension
    fileName = fileRootName + '.wav'
    cmd = 'ffmpeg -i ' + file + ' ' + os.path.join(extractedAudioDir, fileName)
    print(cmd)
    os.system(cmd)

    # clip duration
    y, sr = librosa.load(os.path.join(extractedAudioDir, fileName))
    duration = librosa.get_duration(y=y, sr=sr)
    # cleaning audio from the camera
    clean = noisereduce.reduce_noise(y=y, sr=sr, prop_decrease=0.5)
    clean_filename = os.path.join(noiseReduceDir, fileName)
    soundfile.write(clean_filename, clean, sr)


    # finding offset of clips w.r.t full recording
    fingprint_rec = audalign.FingerprintRecognizer()
    correlation_rec = audalign.CorrelationRecognizer()
    rode_mic_filename = os.listdir(rodeMicDir)[0]
    rode_mic_file = os.path.join(rodeMicDir, rode_mic_filename)
    # aligning audios: finding shift
    results = audalign.align_files(os.path.join(extractedAudioDir, fileName),
                                   rode_mic_file,
                                   recognizer=fingprint_rec
                                   )
    #print(results)
    shiftAmount = results[fileName]
    print(shiftAmount)

    # crop the audio
    # processed-audio: to save clean cropped rode-mic audio
    processedAudio = os.path.join(processedAudioDir, fileName)
    cmd = 'ffmpeg -i' + ' ' + rode_mic_file + ' -ss ' + str(shiftAmount) 
    cmd += ' ' + ' -t ' + str(duration) + ' ' + processedAudio 
    print(cmd)
    os.system(cmd)

    # normalize to -3.0db
    print('normalizing .................')
    audio = AudioSegment.from_file(processedAudio)
    normalized_audio = normalize(audio, headroom=0.3) # -3.0db
    normalAudioFile = os.path.join(normalizedDir, fileName)
    normalized_audio.export(normalAudioFile)

    # replacing the video-audio with clean-audio file from camera
    # ffmpeg -i ./input/comedy-broken-speech-MVI_0138.MOV -i cut_full.wav -c:v copy \
    # -map 0:v:0 -map 1:a:0 -shortest replaced_comedy-broken-speech-MVI_0138.MOV
    #cmd = 'ffmpeg -i ' + file + ' -i ' + clean_filename + ' -c:v copy -map 0:v:0 '
    #cmd += '-map 1:a:0 -shortest '  + os.path.join('./input', videoFile) 
    #os.system(cmd)

    if chooseNormalized:

        # replacing the video-audio with rode-mic-audio file from camera
        # ffmpeg -i ./input/comedy-broken-speech-MVI_0138.MOV -i cut_full.wav -c:v copy \
        # -map 0:v:0 -map 1:a:0 -shortest replaced_comedy-broken-speech-MVI_0138.MOV
        cmd = 'ffmpeg -i ' + file + ' -i ' + normalAudioFile + ' -c:v copy -map 0:v:0 '
        cmd += '-map 1:a:0 -shortest '  + os.path.join(inputDir, videoFile) 
        print(cmd)
        os.system(cmd)

    else:

        # replacing the video-audio with rode-mic-audio file from camera
        # ffmpeg -i ./input/comedy-broken-speech-MVI_0138.MOV -i cut_full.wav -c:v copy \
        # -map 0:v:0 -map 1:a:0 -shortest replaced_comedy-broken-speech-MVI_0138.MOV
        cmd = 'ffmpeg -i ' + file + ' -i ' + processedAudio + ' -c:v copy -map 0:v:0 '
        cmd += '-map 1:a:0 -shortest '  + os.path.join(inputDir, videoFile) 
        print(cmd)
        os.system(cmd)


