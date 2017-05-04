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
import wave
import numpy as np
from scipy.io import wavfile
from scipy import interpolate
from os.path import join , isfile 
from os import listdir
import os
import shutil 


i=0
path = 'MUSIQUE_renamed_mp3/' # .mp3 directory 
newpath = '15k_wav/'         # .wav distination director 
newpath_param = '15k_wav_8khz/'
drop_conv_mp3 = 'drop_mp3/'


# parameter we need 
FORMAT = 2 #Int16
CHANNELS = 1 # mono 
NEW_SAMPLERATE = 8000

a=0
for files in listdir(path) :
	a=a+1

	sufixe = files.split('.')[-1]
	prefixe = files.split('.')[0]
	if isfile(join(newpath_param,prefixe)) == True : 
		shutil.move(join(path,files),join(drop_conv_mp3,files))
	elif isfile(join(newpath_param,prefixe)) == False :

		if sufixe == 'mp3' or sufixe == 'MP3' or sufixe == 'mP3' or sufixe == 'Mp3':
			try:
				sound = AudioSegment.from_mp3(join(path,files))
				sound.export(join(newpath,prefixe), format="wav")
			except Exception:
				i=i+1
				pass

			########### on passe de la convertion mp3 -> wav a la parametrisation

			WAVE_INPUT_FILENAME = join(newpath,prefixe)
			WAVE_OUTPUT_FILENAME = join(newpath_param,prefixe)	

			try:
				Wave_read = wave.open(WAVE_INPUT_FILENAME, 'rb')
				Wave_write = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

				if Wave_read.getframerate() != 8000:

					Wave_write.setnchannels(CHANNELS)
					# Set the number of channels
					Wave_write.setsampwidth(FORMAT)
					# Set the sample width to n bytes.
				
					multiple = 2
					
					Wave_write.setframerate(multiple*Wave_read.getframerate())
					# Set the frame rate to n.

					Wave_write.writeframes(Wave_read.readframes(Wave_read.getnframes()))
					#Write audio frames and make sure nframes is correct

					Wave_read.close()
					Wave_write.close()


					old_samplerate, old_audio = wavfile.read(WAVE_OUTPUT_FILENAME)

					if old_samplerate != NEW_SAMPLERATE:
					    duration = old_audio.shape[0] / old_samplerate

					    time_old  = np.linspace(0, duration, old_audio.shape[0])
					    time_new  = np.linspace(0, duration, int(old_audio.shape[0] * NEW_SAMPLERATE / old_samplerate))

					    interpolator = interpolate.interp1d(time_old, old_audio.T)
					    new_audio = interpolator(time_new).T
					    wavfile.write(WAVE_OUTPUT_FILENAME, NEW_SAMPLERATE, np.round(new_audio).astype(old_audio.dtype))
					if isfile(WAVE_OUTPUT_FILENAME) == True : 
						os.remove(WAVE_INPUT_FILENAME)

			except Exception:
				print('Il y a erreur dans la parametrisation du fichier =',WAVE_INPUT_FILENAME)
				pass


print(i)

