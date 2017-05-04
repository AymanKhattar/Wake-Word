#########################################################################################
#									  WHYD INC. DEV TEAM 
#########################################################################################

'''
Feb 28 2017 
Ayman Khattar @Whyd Inc. 
All rights reserved -------- 
This script convert automaticly mp3 -> wav files. It allows to chose few parameters such as :
'''
from pydub import AudioSegment
import os 
from os import listdir
from os.path import join, isfile
import shutil 






i=0
path = 'MUSIQUE_renamed_mp3/' # .mp3 directory 
newpath = '15k_wav/'         # .wav distination director 
drop_conv_mp3 = 'drop_mp3/'
for files in listdir(path) :
	sufixe = files.split('.')[-1]
	prefixe = files.split('.')[0]
	if isfile(join(newpath,prefixe)) == True : 
		shutil.move(join(path,files),join(drop_conv_mp3,files))
	elif isfile(join(newpath,prefixe)) == False :

		if sufixe == 'mp3' or sufixe == 'MP3' or sufixe == 'mP3' or sufixe == 'Mp3':
			try:
				sound = AudioSegment.from_mp3(join(path,files))
				sound.export(join(newpath,prefixe), format="wav")
			except Exception:
				i=i+1
				pass
print(i)
