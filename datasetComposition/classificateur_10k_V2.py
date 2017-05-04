# Author : Ayman Khattar 22.01.2017 @Whyd Inc 
# All Rights Reserved.
# 
# 
# Classification d'un signal .wav de (1 a 4) sec le programmme est capable deconnaitre 
# avec precision le mot prononce par une voix figurante dans la data set. 
# problem : la reconnaissance generalise mal pour une voix inconnu de la data set 
# 
# Essai effectue sur un Asus - intel core i5 - 
# 
# environ 1 min pour l'apprentissage
# environ 1 sec pour la prediction 
# 
# ==============================================================================

import tflearn 
import wave
import numpy
import time
import os
from random import shuffle
from os import listdir 

import re
import sys
# import skimage.io  # scikit-image
# import pyaudio
# Conditions d usage

t=time.time()

apprentissage = True # lancer l'apprentissage(True), se baser uniquement sur la prediction(False)  
DataSet = True # Train (True), Test (False) 
nb_cpu = 8  # nombre de coeurs ou threads du CPU utilise (ici : intel i5 = 4cores/8threads)
mem_gpu = 0.5 # utilisation de la moitier de la memory bandwidth (ici : AMD RADEON HD8530m : 0.5*14.4GBs)
ip_data_shape = 32000 # taille du signal d'entree 

if DataSet is True:
	path = "merged_15k_2sec_16k8/" # 8 bit
else:
	path = "merged_15k_2sec_16k8_test/" # 8 bit
_nb = -1 # 1 si dataset 10k  2 si dataset 1k (voir les label) 

def split_at(mot, change, endroit): # return (avant_change,apres_change)
    words = mot.split(change)
    return change.join(words[:endroit]), change.join(words[endroit:]) 
def speaker(filename):  # vom Dateinamen
	# if not "_" in file:
	#   return "Unknown"
	return filename.split("_")[_nb]

def get_speakers(path=path):

	files = os.listdir(path)
	def nobad(name):
		return "_" in name and not "." in name.split("_")[_nb]
	speakers=list(set(map(speaker,filter(nobad,files))))
	print(len(speakers)," Commande: ",speakers)
	return speakers

speakers = get_speakers()
number_classes=len(speakers)


# Importer les fichiers : Pour la prediction
CHUNK = 16000
def load_wav_file(name):
	f = wave.open(name, "rb")
	chunk = []
	data0 = f.readframes(CHUNK)
	while data0:  # f.getnframes()
		data = numpy.fromstring(data0, dtype='uint8')
		data = (data + 128) / 255.  # 0-1 for Better convergence
		chunk.extend(data)
		data0 = f.readframes(CHUNK)
	chunk = chunk[0:CHUNK * 2]  # should be enough for now -> cut
	chunk.extend(numpy.zeros(CHUNK * 2 - len(chunk)))  # fill with padding 0's
	return chunk

if apprentissage is True:
	# Importer les fichiers : Pour l'apprentissage

	def one_hot_from_item(item, items):
		# items=set(items) # assure uniqueness
		x=[0]*len(items)# numpy.zeros(len(items))
		i=items.index(item)
		x[i]=1
		return x
	def wave_batch_generator(batch_size=10000): #speaker
		batch_waves = []
		labels = []
		files = os.listdir(path)
		while True:			
			shuffle(files)
			print("loaded batch of %d files" % len(files))
			for wav in files:
				# if not wav.endswith(".wav"):continue
				labels.append(one_hot_from_item(speaker(wav), speakers))
				chunk = load_wav_file(path+wav)
				batch_waves.append(chunk)
				if len(batch_waves) >= batch_size:
					yield batch_waves, labels
					labels = []
					batch_waves = []
					print("Label : "%(labels))
	batch=wave_batch_generator()
	X,Y=next(batch)
#######
t_train=time.time() - t
#######
# Creation du reseau de neurones
tflearn.init_graph(num_cores=nb_cpu, gpu_memory_fraction=mem_gpu) # adapter le reseau a la capacite de l'ordi 
# Initialisation des couches du reseau : http://tflearn.org/layers/core/
net = tflearn.input_data(shape=[None, ip_data_shape]) # creation d un placeholder, tenseur vectoriel shape=[bash size, inputdatashape]
#net = tflearn.fully_connected(net, 128) # couche cachee a 64 neurones 
net = tflearn.fully_connected(net, 64) # couche cachee a 64 neurones 
net = tflearn.fully_connected(net, 32) # couche cachee a 64 neurones 
#net = tflearn.fully_connected(net, 16) # couche cachee a 64 neurones 
#net = tflearn.fully_connected(net, 8) # couche cachee a 64 neurones 
#net = tflearn.fully_connected(net, 4) # couche cachee a 64 neurones 

net = tflearn.dropout(net, 0.5) # un dropout aleatoire 
net = tflearn.fully_connected(net, number_classes, activation='softmax') # derniere couche, 2 neurones, sorti proba, softmax
#momentum = tflearn.optimizers.Momentum(learning_rate=0.1, decay_step=200)
#top5 = tflearn.metrics.Top_k(k=5)
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')

modele = tflearn.DNN(net)
if apprentissage is True:
	modele.fit(X, Y,n_epoch=3,show_metric=True,snapshot_step=100)
	modele.save('my_modele.tflearn')
#########
t_learn=time.time() - t
#########
cmpt=0
Reconnu=0
R_KW=0
activ=0
modele.load('my_modele.tflearn')
for file_name in listdir(path):
	demo=load_wav_file(path + file_name)
	result=modele.predict([demo])
	result=numpy.argmax(result) 
	item=speakers[result]
	result = item
	if result == 'kw':
		 print("%s contient Ok Whyd"%(file_name))	 
	else :
		 print("%s ne contient pas Ok Whyd"%(file_name))
	if speaker(file_name) == 'kw':
		activ=1
                cmpt=cmpt+1
	if speaker(file_name) == result:
		Reconnu=Reconnu+1
        if speaker(file_name) == result and activ ==1:
                R_KW=R_KW+1	
	activ=0
#	print(speaker(file_name))
###############
t_test=time.time() - t
t_total=time.time() - t
################
print("Score de bonne reconnaissance totale (%d/%d)"%(Reconnu,len(listdir(path))))
print("Score des Kw reconnu lorsqu'ils sont prononce (%d/%d)"%(R_KW,cmpt))
print("temps d'apprentissage : %f sec"%(t_learn))
print("temps de test des 500 fichiers base test : %f sec "%(t_test))
print("temps total : %f sec "%(t_total))

