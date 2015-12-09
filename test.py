#coding=utf-8
import numpy, time, math
import matplotlib.pyplot as plt
import pickle

a = 3
b = 4
def changeDict(dd, ee, ff):
	dd['a'] = 1
	ee = 3
	ff[0, 0] = 100

def getTimeSep(timeString):
	a = int(time.mktime(time.strptime(timeString, '%Y-%m-%d %H:%M:%S'))) 
	print a
	return a

def getTimeString(intTime):
	format = "%Y年%m月%d日 %H:%M:%S"
	value = time.localtime(intTime)
	dt = time.strftime(format, value)
	return dt

def testB():
	global a
	print a

def test():
	a = [1.2, 3.4, 5.6]
	for i in a:
		print str(i)
	'''
	#help(range)
	a = [1,3,4]
	for i in a:
		print a.index(i)
	'''


	'''
	a = [["a", 3.4],["b", 4.8], ["c", 1.2]]
	a = sorted(a, key = lambda x:x[1], reverse=True)
	print a
	'''


	'''
	a = [1, 2, 3, 4]
	print a[:2]

	a = {"a":{1:2},"b":{3:4,4:5}}
	print "a" in a
	print len(a)
	'''


	'''
	a = [[1,2],[3,4]]
	print [1] in a
	'''

	'''
	a = {"a":[1,2]}
	print a
	a["a"] = [3,4]
	print a
	del a["a"]
	print a
	'''

	'''
	print 3 ** 0.5
	print 4 ** 2

	a = numpy.zeros((2,3))
	a[0,:] += 1
	print a
	#print numpy.shape(numpy.argwhere(a[0,:]>0))
	print numpy.shape(numpy.nonzero(a[0,:]))
	a = len(a[numpy.nonzero(a[1,:])])
	print a
	'''

	'''
	a = [1, 2, 3]
	b = {1:2,3:4}
	
	fw = open("aa", 'w')
	pickle.dump((a, b), fw)
	fw.close
	'''

	'''
	global a,b
	print a,b
	a = 2
	testB()
	fr = open("aa", "r")
	(a, b) = pickle.load(fr)
	print a, b
	'''

	'''
	a = numpy.zeros((2,3))
	a = a + 3
	a[1:] -= 1
	print type(a[1:])
	print a
	#print (a[0,:]**2).sum(axis=1)
	print a[0:]**2
	print numpy.sum(a[0:]**2, axis=1)**0.5
	print numpy.dot(a, a.T)
	'''


	'''
	print math.sqrt(5.0)
	a = numpy.zeros((1,3))
	print type(a)
	a = numpy.mat(a)
	print type(a)
	b = numpy.zeros((3,1))
	b = b + 2
	a = a + 1
	print numpy.dot(a,b)
	print a.T.dot(a)
	#print a.T * a
	'''

	'''
	a = numpy.mat([[1.0,2,3],[2,3,4]])
	b = numpy.mat([[1,2.1],[2,3],[4,5]])
	print a * b

	a = raw_input()
	print a
	'''

	'''
	help(plt.bar)
	'''
	
	'''
	a = [[0 for j in range(4)] for i in range(3)]
	print a
	a[1].append(3)
	print a

	print getTimeString(1393644411)

	
	a = getTimeSep("2014-3-1 0:0:0")
	b = getTimeSep("2014-3-2 0:0:0")
	print b - a
	print 24*60*60
	
	print 1/3
	'''


	'''
	aa = numpy.zeros((3,3))
	aa = aa + 2
	aa = aa ** 2 
	aa[0, 1] = 5
	print aa
	print max(aa[:,1])
	'''

	'''
	dic = {'a': 3}
	print dic
	a = 4
	ff = numpy.zeros((3,3))
	print ff
	changeDict(dic, a, ff)
	print dic, a, ff
	'''

	'''
	a = numpy.zeros((2,3))
	print 1/3
	a[0, 0] = 1.0/3
	print a.dtype,a
	'''

	'''
	dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
	for item in dic:
		print dic[item]
	del dic["a"]
	print dic
	dic = sorted(dic.iteritems(), key=lambda d:d[1], reverse = True)
	print dic[0]
	'''


	'''
	a = set(["1", "2", "3"])
	print a
	b = set(["4", "2"])
	print b
	print a|b
	a = a | b
	print len(a)
	

	a = set({"1", "2", "3"})
	b = set({"2", "4"})
	print a|b
	'''

	'''
	a = "2324"
	print a.isdigit()
	'''

	'''
	stopWord = []
	with open(GlobalConfig.stopWord) as fr:
		stopWord = set(fr.readlines())
		print len(stopWord)
	with open("StopWord1", "w") as fw:
		for i in stopWord:
			fw.write(i)
		#fw.write(str(stopWord))
	'''
	
	'''
	print GlobalConfig.allData
	print time.time()
	print time.gmtime(1394463264)
	print int(time.mktime(time.strptime('2014-3-4 3:2:3', '%Y-%m-%d %H:%M:%S')))
	'''

	'''
	tt = [["3",3,3],["1",1,1],["2",2,2]]
	tt = sorted(tt, key=lambda x:int(x[0]))
	'''

	'''
	a = [ [1, 2, 3], [1, 5, 6], [7, 8, 9]]
	c = [1, 3, 4]
	b = []
	b.append(1)
	print "All different docs:%d" % len(b)
	'''
if __name__ == "__main__":
	test()
	