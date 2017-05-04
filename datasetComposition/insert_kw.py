# Author : Ayman Khattar 20.01.2017 @Whyd Inc 
# All Rights Reserved.
# 
# 
#  Ce code permet d'inserer un mot clef de 1 second "OkWhyd" enregistre par Loick dans 500 bande de 6sec
#  Dans ce code le mot clef est insere au centre de l'echantillon de 6 secondes
# 25 FICHIERS ONT ETE ELIMINE PARCE QU'ILS NE POUVAIENT PAS ETRE LU EN MONO
# ==============================================================================
import sys
import pydub
from pydub import AudioSegment
from pydub.utils import make_chunks
import operator
import glob, os
from os import listdir 
from os.path import join , basename , splitext
# egg_path='/usr/local/lib/python3.4/dist-packages/scikits.audiolab-0.11.0-py3.4-linux-x86_64.egg'
# sys.path.append(egg_path)
# import scikits 
# from  scikits import audiolab
import scipy
from scipy.io import wavfile



olddir = '6sec_wav_V1/' #  dossier de depart 
newdir = 'kw_nokw_merg_10k/' # dossier d'arrivee
i=1
for filename in listdir(olddir):
	i=i+1
	
	print(filename)
	myaudio = AudioSegment.from_file(join(olddir,filename)) 
	if i < 5000:
		#keyword = AudioSegment.from_file('Loick_OkWhyd.wav')
		fs, a = wavfile.read(join(olddir,filename))
		fs, b = wavfile.read('Loick_OkWhyd.wav') 
		if a.shape == (48000,):
			halfway_point = round(len(a) / 2) # se placer au centre de l'echantillon
			chunk_length_ms = round(len(b)/2) # 1 secondes	
			
			SUM_a=[int(x) + int(y) for x, y in zip(b, a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms])]
			#SUM_a = map(operator.add, b, a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms])
			MERG_a = [int(x) / 2 for x in SUM_a]
			a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms] = MERG_a
			# print(myaudio[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms])
			# print(keyword) # inserer keyword
			title,ext = splitext(basename(filename))
			scipy.io.wavfile.write(newdir+'%s_kw'%title, fs, a)
			# c.export(newdir + '6sec_%s_kw'%title, format="wav") # avec keyword
	else: 
		if a.shape == (48000,):
			title,ext = splitext(basename(filename))
			myaudio.export(newdir + '%s_nokw'%title, format="wav") # sans keyword


print(i)