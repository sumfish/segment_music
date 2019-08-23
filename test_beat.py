import numpy as np
import os
import madmom.features.downbeats as dbt
from madmom.features.beats import RNNBeatProcessor 
from pydub import AudioSegment #cut

dirpath = './softjazz/03'
ori_file = '_original.mp3'
piano_file = 'piano.mp3'
os.chdir(dirpath)
os.mkdir('CutPiano')
os.mkdir('CutOri')

#### madmom
proc = dbt.DBNDownBeatTrackingProcessor(beats_per_bar=[4, 4], fps=100)
act = dbt.RNNDownBeatProcessor()(ori_file)
#print(proc(act))

#### split audio
sound = AudioSegment.from_file(ori_file)
sound2 = AudioSegment.from_file(piano_file)

#### cut by miliseconds
opening=0
end=0
has_record=False
count=0
bar4=0
for s, index in proc(act):
    if(index==1):
        if has_record :
            end=s
            bar4=bar4+1
            if(bar4%1==0):
                cut=sound[opening*1000:end*1000]
                cut2=sound2[opening*1000:end*1000]
                cut.export("./CutOri/cut"+str(count)+".wav",format='wav')
                cut2.export("./CutPiano/cut"+str(count)+".wav",format='wav')
                opening=s
                count=count+1
                bar4=0
        else:    
            opening=s
            has_record=True


