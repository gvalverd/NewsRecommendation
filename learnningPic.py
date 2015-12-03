#coding=utf-8
# r g b y m c k （红，绿，蓝，黄，品红，青，黑）

import numpy as np
import matplotlib.pyplot as plt

def picBarPicture():

	n_groups = 5

	means_men = [20, 35, 30, 35, 27]
	means_women = [25, 32, 34, 20, 25]

	fig, ax = plt.subplots()
	index = np.arange(n_groups) # Attention that range(n) can't be used to add a num 
	bar_width = 0.4

	opacity = 0.5
	rects1 = plt.bar(index, means_men, bar_width,alpha=opacity, color='b',label='Men')
	rects2 = plt.bar(index + bar_width, means_women, bar_width,alpha=opacity,color='r',label='Women')

	plt.xlabel('Group')
	plt.ylabel('Scores')
	plt.title('Scores by group and gender')
	plt.xticks(index, ('A', 'B', 'C', 'D', 'E'))
	plt.ylim(0,40)
	plt.legend()

	#plt.tight_layout()
	plt.show()
if __name__ == "__main__":
	picBarPicture()
