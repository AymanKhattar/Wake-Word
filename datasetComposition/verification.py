import wave
import os
from os.path import join 
from os import listdir

path = "merged_15k_2sec_16k8"
i=0
chan1=0
chan2=0
format32=0
format16=0
format8=0
rate44=0
rate800=0 
rate1600=0 
for files in listdir(path): 
	#files = f.split('.')[0]
	#try :
	Wave_read = wave.open(join(path,files), 'rb')
	if Wave_read.getframerate() == 44100:
		rate44=rate44+1
	elif Wave_read.getframerate() == 8000:
		rate800=rate800+1
	elif Wave_read.getframerate() == 16000:
		rate1600=rate1600+1		
	else: 
		print(Wave_read.getframerate(),files) 
	if 	Wave_read.getnchannels() == 1:
		chan1 = chan1+1
	if 	Wave_read.getnchannels() == 2: 
		chan2 = chan2+1 
	if 	Wave_read.getsampwidth() == 2: # if input 16 bits 
		format16 = format16+1
	elif 	Wave_read.getsampwidth() == 4: # if input 32 bits 
		format32 = format32+1
	elif 	Wave_read.getsampwidth() == 1: # if input 8 bits 
		format8 = format8+1
	else:
		print(join(path,files))
		#print(Wave_read.getsampwidth()) 
	#except Exception:
	#	print(files)
		pass
	Wave_read.close()
print("\n\n\n\n")
print(" 1 channel %d "%(chan1))
print(" 2 channel %d"%(chan2))
print(" rate 44100 %d"%(rate44))
print(" rate 8000 %d"%(rate800))
print(" rate 16000 %d"%(rate1600))
print(" format 16 %d"%(format16))
print(" format 8 %d"%(format8))
