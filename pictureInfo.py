#coding=utf-8
import numpy as np 
import matplotlib.pyplot as plt
from GlobalConfig import *

def pictureDayUser():
	n_groups = 31
	index = np.arange(n_groups)
	aDayNews = [0 for i in index]
	aDayDifferrentUsers = [0 for i in index]
	aDayDifferrentNews = [0 for i in index]
	
	for i in index:
		tempUsers = []
		tempNews = []
		with open(GlobalConfig.dayFileName+str(i+1)) as fr:
			news = fr.readlines()
			aDayNews[i] = len(news)
			for item in news:
				tempUsers.append(item.split("\t")[0])
				tempNews.append(item.split("\t")[1])

			aDayDifferrentUsers[i] = len(set(tempUsers))
			aDayDifferrentNews[i] = len(set(tempNews))
		#print aDayNews[i],aDayDifferrentUsers[i],aDayDifferrentNews
	plt.figure(figsize=(30,9)) 
	bar_with = 0.28
	opacity = 0.6
	#rects1 = plt.bar(index, aDayNews, bar_with, alpha=opacity, color='b', label="News")
	rects2 = plt.bar(index + bar_with, aDayDifferrentNews, bar_with, alpha=opacity, color='r',\
		label="DiffNews")
	rects3 = plt.bar(index + 2*bar_with, aDayDifferrentUsers, bar_with, alpha=opacity, color='y', \
		label="DiffUsers")

	plt.xlabel("Day")
	plt.ylabel("Numbers")
	plt.title("One day's news and users")
	plt.xticks(index+1.5*bar_with, index+1)
	plt.legend()
	plt.show()

if __name__ == "__main__":
	pictureDayUser()
