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
nb_part=12
def decoup(part, size): # decouper la bande son de 6sec en "part" parties
	a = [x+1 for x in range(0,part-1)] #np.concatenate(np.array([a,x]))
	b=a
	print(len(a))
	print(round(size/len(a)))
	for x in range(0,int(size/len(a))):
		b=np.concatenate([b,a])
	#print(b,len(b))
	return b

def speaker_switch(part, size): # decouper la bande son de 6sec en "part" parties
	a = [x+1 for x in range(0,part-1)] #np.concatenate(np.array([a,x]))
	b=a
	print(len(a))
	print(round(size/len(a)))
	for x in range(0,int(size/len(a))):
		b=np.concatenate([b,a])
	#print(b,len(b))
	return b

#newdir = 'kw_nokw_merg_freq/kw_nokw_merg_10k_m30/' # dossier d'arrivee
#wakeword = 'kw_nokw_merg_freq/2hommemedium_Loick_OkWhyd_m30.wav'
term_freq = """\
. 
_5.
_10.
_15.
_20.
_25.
_30.
_35.
_40.
_m5.
_m10.
_m15.
_m20.
_m25.
_m30.
""".split()

speakers = """\
1femmegrave_Marie
1hommegrave_Thibault
2femmeaigu_Camille
2femmeaigu_Delphine
2hommemedium_Loick
3femmeaigu_Audrey
4femmegrave_Aurore
4hommegrave_Fahiz
5femmegrave_Youk
5hommegrave_Thomas
6femmemedium_Pauline
6hommegrave_Xavier
7hommegrave_Florent
8hommegrave_John
9hommegrave_Brian
10hommegrave_Rageur
11hommemedium_Valentin
""".split()

olddir = '6sec_wav_V1/09891'	
motclef = '_OkWhyd'
newdir = 'kw_volume10/'
VECTwakeword=['DataSet_keyword/'+speaker+motclef+x+'wav'  for speaker in speakers for x in term_freq]

if not os.path.exists(newdir):
	os.mkdir(newdir)
k=0
i=1
it = 1
cmpt = 1
it2 = 1
for wakeword in VECTwakeword:
		fs, b = wavfile.read(wakeword) # lire les differents mots clefs
		fsa, a = wavfile.read(olddir)
		baud = AudioSegment.from_wav(wakeword)
		if len(b.shape)==1:
			chunk_length_ms = int(round(len(b)/2)) # longueur du wake word	
			#newb = np.array([uint8(2*x) for x in b])
			newb = baud - 1
			print(baud[1:10])
			print("Dessus = b \n Dessous = newb")
			print(newb[1:10])
			print("\n\n\n")
			
			newa = a +80
			print(a[1:10])
			print("Dessus = a \n Dessous = newa")
			print(newa[1:10])
			print("\n\n\n")
			

			title,ext = splitext(basename(wakeword))
			strfreq = term_freq[k].split(".")[0] # wakeword (_m10 .. etc)
			newb.export(newdir+'%s.wav'%(title),"wav")
			#scipy.io.wavfile.write(newdir+'%s_kw'%(title), fs, newb)
