import heapq 

######
print ("Welcome to Eight Puzzle Problem!")
init_station = list(str(raw_input("Please input your init number!")))
end_station = list(str(raw_input("Please input your end number!")))

class State:
    def __init__(self):
	self.father = None
	self.g = 0
	self.h = 0
	self.f = self.g + self.h
	self.station =[]

    def __eq__(self, s):
        #overload __eq__ method
	#return True or False
	return self.station == s.station

    def __le__(self,s):
        #overload __le__ method for compare  in heapq
        if self.f == s.f:
            return self.g <= s.g
        else:
	    return self.f<=s.f

open_table = []#heap
close_list = list()
#creat init class and end class
init = State()
init.station = init_station
end = State()
end.station = end_station
distance_matrix = [[0,1,2,1,2,3,2,3,4],
                   [1,0,1,2,1,2,3,2,3],
                   [2,1,0,3,2,1,4,3,2],
                   [1,2,3,0,1,2,1,2,3],
                   [2,1,2,1,0,1,2,1,2],
                   [3,2,1,2,1,0,3,2,1],
                   [2,3,4,1,2,3,0,1,2],
                   [3,2,3,2,1,2,1,0,1],
                   [4,3,2,3,2,1,2,1,0]]


######


def is_succeed_state(state):
#return Ture or False
    global init
    return state == end

def visualize_it():
    #visualize the graph
    pass

def print_path(state):
    global init
    state_list = list()
    while not (state.father == init):
        state_list.append(state.station)
	state = state.father
    state_list.append(state.station)
    state_list.append(init.station)
    state_list.reverse()
    for i in state_list:
        print (i)
    print("You spend %s step to find the end station" % str(len(state_list)-1))

def return_state_list(station):
    #receive a list station and return a list contains
    state_list = list() 
    space_index = station.index('0')
    if space_index in [0]:
        cand_index =[i+space_index for i in [1,3]]
    elif space_index in [2]:
	cand_index =[i+space_index for i in [-1,3]]
    elif space_index in [6]:
	cand_index =[i+space_index for i in [1,-3]]
    elif space_index in [8]:
	cand_index =[i+space_index for i in [-1,-3]]
    elif space_index in [1]:
        cand_index =[i+space_index for i in [-1,1,3]]
    elif space_index in [3]:
	cand_index =[i+space_index for i in [1,-3,3]]
    elif space_index in [5]:
        cand_index =[i+space_index for i in [-1,-3,3]]
    elif space_index in [7]:
	cand_index =[i+space_index for i in [-1,1,-3]]
    elif space_index in [4]:
        cand_index =[i+space_index for i in [-1,1,-3,3]]

   # result = [i for i in cand_index if (i>-1 and i<9)]
    result = cand_index
    for index in result:
        next_list = station[:] #Can not use next_list = station
        next_list[space_index] = station[index]
        next_list[index] = '0'
        state_list.append(next_list)
    return state_list

def cal_distance(station):
    global end_station
    x = end_station
    y = station
    z = ['0','1','2','3','4','5','6','7','8']
    x_index = [x.index(i) for i in z]
    y_index = [y.index(i) for i in z]
    
    distance = 0
    global distance_matrix
    for i in range(len(x_index)):
        distance = distance +  distance_matrix[x_index[i]][y_index[i]]
    return distance

def generate_next_state(state):
#return a list contains class State
    all_next_state = list()
    state_list = return_state_list(state.station)
    for i in state_list:
        next_state = State()
	next_state.father = state
        next_state.station = i
        next_state.g = state.g + 1
        next_state.h = cal_distance(i)
        next_state.f = next_state.g + next_state.h
        all_next_state.append(next_state)
    return all_next_state

######


heapq.heappush(open_table,init)

while len(open_table) != 0:
    temp = heapq.heappop(open_table)
    #print (temp.station)
    if is_succeed_state(temp):
	print("Congratuations! You have find the end station!")
	print_path(temp)
        break

    next_list = generate_next_state(temp)
    close_list.append(temp)
    
    for state in next_list:
        if state in open_table:
	    index = open_table.index(state)
	    if open_table[index].f > state.f or (open_table[index].f == state.f and open_table[index].g>state.g):
                open_table[index].f = state.f
		open_table[index].g = state.g
     		heapq.heapify(open_table)
	elif state in close_list:
            index = close_list.index(state)
	    if close_list[index].f < state.f :
	        close_list.remove(close_list[index])
	else:
	    heapq.heappush(open_table,state)



