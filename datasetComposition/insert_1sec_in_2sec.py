# Author : Ayman Khattar 20.01.2017 @Whyd Inc 
# All Rights Reserved.
# 
# 
#  Ce code permet d'inserer un mot clef de 1 second "OkWhyd" prononce par 17 personnes et modifie 15 fois
# l'emplacement du mt clef varie dans la bande son  
# ==============================================================================
import sys
import pydub
import shutil
from pydub import AudioSegment
from pydub.utils import make_chunks
import operator
import glob, os
from os import listdir 
from os.path import join , basename , splitext, isfile
# egg_path='/usr/local/lib/python3.4/dist-packages/scikits.audiolab-0.11.0-py3.4-linux-x86_64.egg'
# sys.path.append(egg_path)
# import scikits 
# from  scikits import audiolab
import scipy
from scipy.io import wavfile
import numpy as np
nb_part=3
def decoup(part, size): # decouper la bande son de 6sec en "part" parties
	a = [x+1 for x in range(0,part-1)] #np.concatenate(np.array([a,x]))
	b=a
	#print(len(a))
	#print(round(size/len(a)))
	for x in range(0,int(size/len(a))):
		b=np.concatenate([b,a])
	#print(b,len(b))
	return b

def speaker_switch(part, size): # decouper la bande son de 6sec en "part" parties
	a = [x+1 for x in range(0,part-1)] #np.concatenate(np.array([a,x]))
	b=a
	#print(len(a))
	#print(round(size/len(a)))
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
	
musicdir = '15k_wav_8khz_2sec_volumem30/' #  dossier de depart 
motclef = '_OkWhyd'
newdir = 'merged_m30/'
buffershape = 16000
VECTwakeword=['Okwhyd_param/'+speaker+motclef+x+'wav'  for speaker in speakers for x in term_freq]

if not os.path.exists(newdir):
	os.mkdir(newdir)
#VECTnewdir=['kw_nokw_merg_freq/'+speaker+'/' for x in term_freq]
#print('\n \n \n ******************** newdir')
#print(VECTnewdir)	
# print('\n \n \n ******************** wakeword')
# for i in range(len(VECTwakeword)):
# 	print(VECTwakeword[i])
# 	VECTnewdir=['kw_nokw_merg_freq/kw_nokw_merg_10k'+x+'/' for x in term_freq] # division dans des dossier suivant la frequence (au cas ou ca pose pb lors de l'insertion)
# 	if os.path.exists(newdir):
# 		shutil.rmtree(newdir)
# 	for wakeword in VECTwakeword:
# 		newdir = VECTnewdir[k] 
# 		print(newdir)
# 		print(term_freq[k].split(".")[0])
# 		os.makedirs(newdir)
# 		os.mkdir(newdir) 
k=0
i=1
it = 1
cmpt = 1
it2 = 1
for musicfile in listdir(musicdir):
	if it == 0 or it == 254: 
		cmpt = -cmpt
	if cmpt > 0 : 
		it=it+1
	if cmpt < 0:
		it=it-1
	i=i+1
	# print(VECTwakeword[it])
	# print(i)
	if k == 15:
		k=0

	title,ext = splitext(basename(musicfile))
	try:
		myaudio = AudioSegment.from_file(join(musicdir,musicfile)) 
		if i < 16975 and isfile(newdir+'%s_kw'%(title)) == False: # half of the musicdir dataset and ensure the output doesnt exist already 
			#keyword = AudioSegment.from_file('Loick_OkWhyd.wav')
			fs, a = wavfile.read(join(musicdir,musicfile))
			fs, b = wavfile.read(VECTwakeword[it]) # lire les differents mots clefs
			if a.shape == (buffershape,) and len(b.shape)==1:
				#print(a.shape)
				cut = int(decoup(int(nb_part), int(len(listdir(musicdir))))[i])
				halfway_point = int(round(cut*len(a) / nb_part)) # deplacer le ww dans l'echantillon
				#halfway_point = int(round(len(a) / nb_part)) # deplacer le ww dans l'echantillon
				chunk_length_ms = int(round(len(b)/2)) # longuer du wake word	
				#print(chunk_length_ms)
				#print(halfway_point)
				#print(zip(b, a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms]))

				SUM_a=[2*int(x) + int(y) for x, y in zip(b, a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms])]
				MERG_a = [int(x) / 2 for x in SUM_a]
				# merger le wake word avec la bande son 
				#print(len(a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms]),len(MERG_a))
				if len(a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms]) == len(MERG_a):
					it2 = it2 + 1
					a[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms] = MERG_a
					# print(myaudio[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms])
					# print(keyword) # inserer keyword
					strfreq = term_freq[k].split(".")[0] # wakeword (_m10 .. etc)
					#print('%d'%k)
					scipy.io.wavfile.write(newdir+'%s_kw'%(title), fs, a)
					# c.export(newdir + '6sec_%s_kw'%title, format="wav") # avec keyword
		elif isfile(newdir + '%s_nokw'%(title)) == False : 
			if i > 16975 and a.shape == (buffershape,):
				title,ext = splitext(basename(musicfile))
				myaudio.export(newdir + '%s_nokw'%(title), format="wav") # sans keyword
				print('nokow%d'%k)
					# # # print(i)
	except Exception:
		pass
		
	k=k+1

