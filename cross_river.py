#!/home/python/bin/python
#coding:utf8

class Queue(list):
	def __init__(self):
		list.__init__(self)
	def Enqueue(self,s):
		self.append(s)

	def Dequeue(self):
		return self.pop(0)

	def Print(self):
		print 'count:%d' %(len(self))
		#FIFO
		for item in self:
			item.Print()

	def Empty(self):
		if len(self) == 0:
			return True
		return False

class Stack(list):
	def __init__(self):
		list.__init__(self)

	def Push(self,s):
		self.append(s)

	def Pop(self):
		return self.pop()

	def Print(self):
		print 'count:%d' %(len(self))
		#FILO
		idx = len(self) - 1;
		while idx >= 0:
			self[idx].Print()
			idx = idx - 1
	def PrintReverse(self):
		print 'count:%d' %(len(self))
		for item in self:
			item.Print()

	def Top(self):
		return self[len(self) -1]

	def Empty(self):
		if len(self) == 0:
			return True
		return False

class State:
	def __init__(self,f,w,s,v):
		self.f = f
		self.w = w
		self.s = s
		self.v = v
		#用于广度优先搜索
		self.father_list = MyList()
		self.direction = ''
	#用与广度优先搜索
	def SetDirection(self,d):
		self.direction = d

	def SetFather(self,f):
		self.father = f

	def __eq__(self,s):
		return self.w == s.w and self.f == s.f and self.s == s.s and self.v == s.v

	def Print(self):
		print '(%d,%d,%d,%d)'%(self.f,self.w,self.s,self.v)

	def Copy(self,s):
		self.f = s.f
		self.w = s.w
		self.s = s.s
		self.v = s.v

	def IsValid(self):
	    #人在左岸,狼羊在右岸
	    if self.f == 0:
	        if self.w == self.s and self.w == 1:
	            return False
	        elif self.s == self.v and self.s == 1:
	            return False
	        else:
	            return True
	    elif self.f == 1:                                                                                         
	        if self.w == self.s and self.w == 0:                                                                        
	            return False                                                                                       
	        elif self.s == self.v and self.s == 0:                                                                      
	            return False                                                                                       
	        else:                                                                                              
	            return True
	
class MyList(list):
	def __init__(self):
		list.__init__(self)

	def Has(self,s):
		for item in self:
			if item == s:
				return True
		return False



	def Remove(self,s):
		for i in range(0,len(self)):
			if self[i] == s:
				return self.pop(i)

#第i样东西送到右岸
def L(news,s,i):
	news.Copy(s)
	if news.f == 0:
		if 0 == i:
			pass
		elif 1 == i and news.w == 0:
			news.w = 1
		elif 2 == i and news.s == 0:
			news.s = 1
		elif 3 == i and news.v == 0:
			news.v = 1;
		else:
			return False
		news.f = 1
		return True
	else:
		return False

#第i样东西送到左岸
def R(news,s,i):
	news.Copy(s)
	if news.f == 1:
		if 0 == i:
			pass
		elif 1 == i and news.w == 1:
			news.w = 0
		elif 2 == i and news.s == 1:
			news.s = 0
		elif 3 == i and news.v == 1:
			news.v = 0
		else:
			return False
		news.f = 0
		return True
	else:
		return False

def IsValid(s):
	#人在左岸
	if s.f == 0:
		if s.w == s.s and s.w == 1:
			return False
		elif s.s == s.v and s.s == 1:
			return False
		else:
			return True
	elif s.f == 1:
		if s.w == s.s and s.w == 0:
			return False
		elif s.s == s.v and s.s == 0:
			return False
		else:
			return True

#深度优先搜索
def DFS(s,e,stack,close_list,direction):
	if s == e:
		global road_num
		road_num += 1
		print '第%d条路径:'%road_num
		stack.Push(s)
		stack.PrintReverse()
		stack.Pop()
		return

	#加入close_list列表，表示已经访问过
	close_list.append(s)
	stack.Push(s)
	if direction == 'L':
		for i in range(0,4):
			news = State(0,0,0,0)
			if L(news,s,i) and news.IsValid() and close_list.Has(news) == False:
				DFS(news,e,stack,close_list,'R')
	elif direction == 'R':
		for i in range(0,4):
			news = State(0,0,0,0)
			if R(news,s,i) and news.IsValid() and close_list.Has(news) == False:
				DFS(news,e,stack,close_list,'L')
	close_list.Remove(s)
	stack.Pop()

start_state = State(0,0,0,0)
end_state = State(1,1,1,1)
direction = 'L'
road_num = 0

#close_list表存放访问过的状态
close_list = MyList()
stack = Stack()
print '----------图搜索算法---------------'
print '----------深度优先搜索-------------'
DFS(start_state, end_state,stack,close_list,direction)

#广度优先搜索
#打印路径

def PrintPath(s,e, close_list):
	if s == e:
		global road_num
		road_num += 1
		print '第%d条路径:'%road_num
		print '(%d,%d,%d,%d)'%(e.f, e.w, e.s, e.v)
		for state in close_list:
			print '(%d,%d,%d,%d)'%(state.f, state.w, state.s, state.v)
	#		print len(state.father_list)
	#加入到访问表中
	else:
		close_list.insert(0, s)
		for state in s.father_list:
			PrintPath(state, e, close_list)

	close_list.Remove(s)
	

#广度优先
def BFS(start_state,end_state):
	close_list = MyList()

	open_list = Queue()
	open_list.Enqueue(start_state)
	
	return_state = None
	while open_list.Empty() == False:
		state = open_list.Dequeue()

		if close_list.Has(state):
			state_real = close_list.Remove(state)
			state_real.father_list += state.father_list
			close_list.append(state_real)
			continue
		else:
			close_list.append(state)

		#是否是目标状态
		if state == end_state:
			return_state = state
			continue

		if state.direction == 'L':
			for i in range(0,4):
				news = State(0,0,0,0)
				if L(news,state,i) and news.IsValid() and close_list.Has(news) == False:
					news.father_list.append(state)
					news.SetDirection('R')
					open_list.Enqueue(news)
		else:
			for i in range(0,4):
				news = State(0,0,0,0)
				if R(news,state,i) and news.IsValid() and close_list.Has(news) == False:
					news.father_list.append(state)
					news.SetDirection('L')
					open_list.Enqueue(news)
	return return_state

start_state.SetDirection('L')
end_state = BFS(start_state, end_state)
close_list = MyList()
print '----------广度优先搜索-------------'
road_num = 0
PrintPath(end_state,start_state,close_list)

