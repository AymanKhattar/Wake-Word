#########################################################################################
#				 WHYD INC. DEV TEAM 
#########################################################################################

'''
Feb 29 2017 
Ayman Khattar @Whyd Inc. 
All rights reserved -------- 
Ce code permet de couper au milieu de chaques musiques un echantillon de 2 sec  
'''
# ==============================================================================

import pydub
from pydub import AudioSegment
from pydub.utils import make_chunks
 
import glob, os
from os import listdir 
from os.path import join , basename , splitext


olddir = '15k_wav_8khz/' #  dossier de depart 
newdir = '15k_wav_8khz_2sec/' # dossier d'arrivee

for cmpt in [1,2,3]: 
	for filename in listdir(olddir):
		myaudio = AudioSegment.from_file(join(olddir,filename)) 
		halfway_point = cmpt*len(myaudio) / 4
		chunk_length_ms = 1000 # 1 secondes
		title,ext = splitext(basename(filename))
		try :
			chunk_2sec = myaudio[halfway_point-chunk_length_ms:halfway_point+chunk_length_ms] # coupe 2 sec de la moitier de la musique
			chunk_2sec.export(newdir + '2sec_%s%d'%(title,cmpt), format="wav")
		except Exception:
			print('Il y a erreur dans le fichier =',filename)
			pass

