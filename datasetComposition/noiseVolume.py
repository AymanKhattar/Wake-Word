# Author : Ayman Khattar 20.01.2017 @Whyd Inc 
# All Rights Reserved.
# 
# 
#  Ce code permet d'inserer un mot clef de 1 second "OkWhyd" prononce par 17 personnes et modifie 15 fois
# l'emplacement du mt clef varie dans la bande son
#
# mise a jour 22 fevrier, gener 10K fichier son base sur 10K bruit musical different
# multiplication par 2 du volume du wakeword   
# ==============================================================================
import sys
import pydub
import shutil
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
import numpy as np


remplacer = True

olddir = '15k_wav_8khz_2sec'	
newdir = '15k_wav_8khz_2sec_volume10'

if os.path.exists(newdir):
	if remplacer == True:
		for root, dirs, files in os.walk(newdir, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		os.rmdir(newdir)
		os.mkdir(newdir)
else :
	os.mkdir(newdir)


for wakeword in listdir(olddir):
		fs, b = wavfile.read(join(olddir,wakeword)) # lire les differents mots clefs
		baud = AudioSegment.from_wav(join(olddir,wakeword))
		if len(b.shape)==1:
			chunk_length_ms = int(round(len(b)/2)) # longueur du wake word	
			#newb = np.array([uint8(2*x) for x in b])
			newb = baud - 30
			#print(baud[1:10])
			#print("Dessus = b \n Dessous = newb")
			#print(newb[1:10])
			#print("\n\n\n")
			
			#newa = a +80
		
			title,ext = splitext(basename(wakeword))
			newb.export(join(newdir,'%s.wav'%(title)),"wav")
			#scipy.io.wavfile.write(newdir+'%s_kw'%(title), fs, newb)

