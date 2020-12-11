import time
import datetime
import json
import pandas as pd
from pandas import DataFrame
import os
import collections
import numpy as np
import csv
import collections
import nltk.classify
import nltk.metrics

"""
	to save user-user similarity matrix as a whole 
"""
index_list = ["1", "2", "3", "4", "5", "6", "7"]
filename1 = "test" + index_list[0] + ".tsv"
filename2 = "test" + index_list[1] + ".tsv"
filename3 = "test" + index_list[2] + ".tsv"
filename4 = "test" + index_list[3] + ".tsv"
filename5 = "test" + index_list[4] + ".tsv"
filename6 = "test" + index_list[5] + ".tsv"
filename7 = "test" + index_list[6] + ".tsv"

with open("user_user_matrix_nof.tsv","w",newline='') as csvfile:
	writer = csv.writer(csvfile)
	k=0;
	with open(filename1, 'r') as fp1:
		with open(filename2, 'r') as fp2:
			with open(filename3, 'r') as fp3:
				with open(filename4, 'r') as fp4:
					with open(filename5, 'r') as fp5:
						with open(filename6, 'r') as fp6:
							with open(filename7, 'r') as fp7:
								for line1 in fp1:
									line1=(line1.replace('\n', '')).split(',')
									line2 =(fp2.readline().replace('\n', '')).split(',')
									line3=((fp3.readline()).replace('\n', '')).split(',')
									line4=((fp4.readline()).replace('\n', '')).split(',')
									line5=((fp5.readline()).replace('\n', '')).split(',')
									line6=((fp6.readline()).replace('\n', '')).split(',')
									line7=((fp7.readline()).replace('\n', '')).split(',')
						
									
								  
									line=[]
									if len(line1)>1:
										print(k)
										#print(line1[-1])
										line.append(line1[0:]+ line2[1:]+ line3[1:] +line4[1:] +line5[1:] +line6[1:] +line7[1:])
										#line.append(line2[1:])	
										#line.append(line3[1:])
										#line.append(line4[1:])
										#line.append(line5[1:])
										#line.append(line6[1:])
										#line.append(line7[1:])
										k=k+1;
										#Line=DataFrame(line)
										#print(Line.T.iloc[0:])	
										writer.writerow(line)	
									#print([line])
									

