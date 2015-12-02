#coding=utf-8
import numpy

def changeDict(dd, ee, ff):
	dd['a'] = 1
	ee = 3
	ff[0, 0] = 100

def test():

	aa = numpy.zeros((3,3))
	aa = aa + 2
	aa = aa ** 2 
	aa[0, 1] = 5
	print aa
	print max(aa[:,1])

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
	