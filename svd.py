#coding=utf-8
import numpy as np
from GlobalConfig import *
from numpy import linalg as la
import run

userSet = {}
newsSet = {}


def getUserNewsClickMatrix(filename, toFilename):
	global userSet, newsSet

	userNewsMat = np.mat(np.zeros((15000,9000)))

	with open(filename) as fr:
		allData = fr.readlines()
		for item in allData:
			item = item.strip().split("\t")
			if not item[0] in userSet:
				userSet[item[0]] = len(userSet)
			if not item[1] in newsSet:
				newsSet[item[1]] = len(newsSet)
			userNewsMat[userSet[item[0]], newsSet[item[1]]] += 1
	(userNo, newsNo) = (int(len(userSet)*.98), len(newsSet))
	print userNo,newsNo

	userNewsMat = userNewsMat[:userNo, :newsNo]
	U, Sigma, VT = la.svd(userNewsMat)

	result = "user\tnews\tclick\n"
	nonZero = np.nonzero(userNewsMat)
	for i in range(np.shape(nonZero[0])[1]):
		row = nonZero[0][0, i]
		col = nonZero[1][0, i]
		result += str(row+1)+"\t"+str(col+1)+"\t"+str(int(userNewsMat[row, col]))+"\n"

	with open(toFilename, "w") as fw:
		fw.write(result)

	run.storeStatisticInfo((userNewsMat, U, Sigma, VT, userSet, newsSet), GlobalConfig.userNewsMatrix)

def testSigma():
	(userNewsMat, U, Sigma, VT, userSet, newsSet) = run.getStatisticInf(GlobalConfig.userNewsMatrix)
	print len(Sigma)
	sumValue = np.sum(Sigma)
	for i in range(len(Sigma)):
		if np.sum(Sigma[:(i+1)]) >= (sumValue*0.9):
			print str(i+1)
			break

if __name__ == "__main__":
	#getUserNewsClickMatrix(GlobalConfig.trainningData, GlobalConfig.trainningUserNews)
	#getUserNewsClickMatrix(GlobalConfig.testData, GlobalConfig.testUserNews)
	testSigma()





