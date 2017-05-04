# Author : Ayman Khattar 06.03.2017 @Whyd Inc 
# All Rights Reserved.
# 
# 
# Classification d'un signal .wav de (1 a 4) sec le programmme est capable deconnaitre 
# 
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
import tensorflow as tf 
import wave
import numpy
import numpy as np 
import time
import os
from random import shuffle
from os import listdir
from os.path import isfile 
import librosa 
import re
import sys
# import skimage.io  # scikit-image
# import pyaudio
# Conditions d usage

t=time.time()

apprentissage = False # lancer l'apprentissage(True), se baser uniquement sur la prediction(False)  
DataSet = False # Train (True), Test (False) 
nb_cpu = 20  # nombre de coeurs ou threads du CPU utilise (ici : intel i5 = 4cores/8threads)
mem_gpu = 0.99 # utilisation de la moitier de la memory bandwidth (ici : AMD RADEON HD8530m : 0.5*14.4GBs)
ip_data_shape = 87#160#87 #16000 # taille du quart signal d'entree 
ip_data_width = 20#100#20 #MFCC FEATURE
path = "merged_train/" # 8 bit
path_test = "merged_test/" # 8 bit
training_iters = 300000

_nb = -1 # (1) si dataset 10k  (2) si dataset 1k (voir les label) 

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
CHUNK = 24000


if apprentissage is True:
	# Importer les fichiers : Pour l'apprentissage

	def one_hot_from_item(item, items):
		# items=set(items) # assure uniqueness
		x=[0]*len(items)# numpy.zeros(len(items))
		i=items.index(item)
		x[i]=1
		return x
	def mfcc_batch_generator(batch_size,path):
		batch_features = []
		labels = []
		files = listdir(path)
		while True:
			print("loaded batch of %d files" % len(files))
			shuffle(files)
			for file in files:
				labels.append(one_hot_from_item(speaker(file), speakers))
				#if not file.endswith(".wav"): continue
				wave, sr = librosa.load(path+file, mono=True)
				mfcc = librosa.feature.mfcc(wave, sr)
				#print(np.array(mfcc).shape)
				mfcc=np.pad(mfcc,((0,0),(0,ip_data_shape-len(mfcc[0]))), mode='constant', constant_values=0)
				chunk = np.array(mfcc)
				batch_features.append(chunk)
				if len(batch_features) >= batch_size:
					# if target == Target.word:  labels = sparse_labels(labels)
					# labels=np.array(labels)
					# print(np.array(batch_features).shape)
					# yield np.array(batch_features), labels
					# print(np.array(labels).shape) # why (64,) instead of (64, 15, 32)? OK IFF dim_1==const (20)
					yield batch_features, labels  # basic_rnn_seq2seq inputs must be a sequence
					batch_features = []  # Reset for next batch
					labels = []
	# batch_train=mfcc_batch_generator(batch_size=len(listdir(path)),path=path)
	# batch_test=mfcc_batch_generator(batch_size=len(listdir(path_test)),path=path_test)

	batch_train=mfcc_batch_generator(batch_size=64,path=path)
	batch_test=mfcc_batch_generator(batch_size=64,path=path_test)


#######
t_train=time.time() - t
#######
tf.reset_default_graph()
# Creation du reseau de neurones
tflearn.init_graph(num_cores=nb_cpu, gpu_memory_fraction=mem_gpu) # adapter le reseau a la capacite de l'ordi 
# Initialisation des couches du reseau : http://tflearn.org/layers/core/
net = tflearn.input_data(shape=[None, ip_data_width, ip_data_shape]) # creation d un placeholder, tenseur vectoriel shape=[bash size, inputdatashape]
#net = tflearn.fully_connected(net, 128) # couche cachee a 64 neurones 
net = tflearn.lstm(net, 128*4, dropout=0.5)
net = tflearn.fully_connected(net, number_classes, activation='softmax') # derniere couche, 2 neurones, sorti proba, softmax
#momentum = tflearn.optimizers.Momentum(learning_rate=0.1, decay_step=200)
#top5 = tflearn.metrics.Top_k(k=5)
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')
iteration=0 
modele = tflearn.DNN(net)
if apprentissage is True:
	if isfile('my_modele.lstm.tflearn') == True:
		modele.load('my_modele.lstm.tflearn')
	while training_iters > 0:
		training_iters=training_iters-1
		X,Y=next(batch_train)
		X_test,Y_test=next(batch_test)
		modele.fit(X, Y,n_epoch=10,show_metric=True,validation_set=(X_test,Y_test),snapshot_step=100)
		iteration=iteration+1
		if iteration > 1000:
			iteration=0
			modele.save('my_modele.lstm.tflearn')
	modele.save('my_modele.lstm.tflearn')
#########
t_learn=time.time() - t
#########
cmpt=0
Reconnu=0
R_KW=0
activ=0
modele.load('my_modele.lstm.tflearn')
for file_name in listdir(path):


	wave, sr = librosa.load(path+file_name, mono=True)
	mfcc = librosa.feature.mfcc(wave, sr)
	#print(np.array(mfcc).shape)
	mfcc=np.pad(mfcc,((0,0),(0,87-len(mfcc[0]))), mode='constant', constant_values=0)
	demo = np.array(mfcc)
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


