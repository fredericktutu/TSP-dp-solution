import numpy as np
def get_subset_pair(snum):
	'''
	获取snum对应的集合去掉一个城市的所有集合及对应的城市
	用二进制数来表示城市集V
	假设V中总共4个城市
	>>>get_subset_nums(3)
	[1,2]
	explain: 3 的二进制表示 0011, 减去一座城市的状态有两个2(0010) 1(0001)
	
	>>>get_subset_nums(6)
	[2,4]
	explain: 6(0110) -> 2(0010)  4(0100)
	'''
	city = 0
	poly = 1
	tmp = snum
	res = []
	while tmp > 0:
		if tmp % (poly * 2) == poly:
			res.append((city + 1, snum - poly))
			tmp -= poly
		poly *= 2
		city += 1
			
	return res

def get_zero_citys(snum, n):
	'''
	>>>get_zero_citys(3,4)
	[2,3]
	#0011 -> 2 3
	
	>>>get_zero_citys(4,6)
	[0,1,3,4,5]
	#000100 -> 
	'''
	city = 0
	poly = 1
	res = []
	while city < n:
		if snum % (poly * 2) == 0:
			res += [city + 1]
		else:
			snum -= poly
		poly *= 2
		city += 1
	return res






class tsp:
	def __init__(self, cityNum, dist):
	                   #城市数量，距离集，源城市
	    #为了方便，每次输入的时候源节点的编号为0
		self.N = cityNum
		self.dist = dist 
		self.d = np.zeros((self.N, (2 ** (self.N-1))))  #n行,2^(n-1)列   因为行中包括s, 列中不包括s
													 #并且第0行只有d[0][2^(n-1)]要用到,因为0不在中间过程中出现
		self.mark = []
		for i in range(self.N):
			self.mark.append([])
			for j in range((2 ** (self.N-1))):
				self.mark[i].append([None])
		
		
		
	def solution(self):
		for i in range(1, self.N):
			self.d[i][0] = self.dist[i][0]
			
		for snum in range(1,2 ** (self.N - 1)):
			for city in get_zero_citys(snum, self.N - 1):
				pathList = [(ncity,nsnum,self.dist[city][ncity] + self.d[ncity][nsnum]) for (ncity, nsnum) in get_subset_pair(snum)]
				pathList.sort(key = lambda tup: tup[2])
				self.d[city][snum] = pathList[0][2]
				self.mark[city][snum] = (pathList[0][0], pathList[0][1])
			
			
		pathList = [(city,snum,self.dist[0][city] + self.d[city][snum])for (city, snum) in get_subset_pair(2 ** (self.N - 1) - 1)]
		pathList.sort(key = lambda tup: tup[2])
		self.d[0][-1] = pathList[0][2]
		self.mark[0][-1] = (pathList[0][0],pathList[0][1])
		#print("距离矩阵\n",self.d)
		#print("回溯矩阵\n",self.mark)
		print("tsp 的最优路径长度为", self.d[0][-1])
		
		#下面输出路径
		path = []
		last = self.mark[0][-1]
		for i in range(self.N - 1):   #回溯，将经过的节点按顺序放入path，注意放入的顺序即和旅行商的行动的顺序一样
			current = (last[0])
			last = self.mark[last[0]][last[1]]
			path.append(current)
		path.append(0)
		last = 0
		print("路径为")
		for current in path:
			print("{0}->{1}: {2}".format(last, current, self.dist[last][current]))
			last = current
			
	
cityNum = int(input())
dist = []
'''
输入格式
3
0 1 2 城市0到其他距离
2 0 3 城市1到其他距离
3 4 0城市2到其他距离
'''
for i in range(cityNum):
	lst = list(map(int, input().split(" ")))
	if len(lst) == cityNum:
		dist.append(lst)
	else:
		print("数目不对")
	
tsp1 = tsp(cityNum, dist)
tsp1.solution()

