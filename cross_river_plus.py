FARMER = 0;WOLF = 1;SHEEP = 2;CABBAGE =3
init_state = '0000';succeed_state = '1111'
closed = list()
END = 0

def is_succeed_state(state):
#retrun Ture or False
    return state == succeed_state

def is_valid_state(state):
#return True or False
    if (state[WOLF] == state[SHEEP]) & (state[WOLF] != state[FARMER]):
        return False
    if (state[SHEEP] == state[CABBAGE]) & (state[SHEEP] != state[FARMER]):
        return False 
    else:
        return True

def change_state(state,with_who):
#return a string
    if with_who == FARMER:
        state_changed = "%s%s%s%s" %(str(1-int(state[0])),state[1],state[2],state[3])
        return state_changed
    if with_who == WOLF:
        state_changed = "%s%s%s%s" %(str(1-int(state[0])),str(1-int(state[1])),state[2],state[3])
        return state_changed
    if with_who == SHEEP:
        state_changed = "%s%s%s%s" %(str(1-int(state[0])),state[1],str(1-int(state[2])),state[3])
        return state_changed
    if with_who == CABBAGE:
        state_changed = "%s%s%s%s" %(str(1-int(state[0])),state[1],state[2],str(1-int(state[3])))
        return state_changed

def next_step(state):
# return a list
    next_state_all = list()
    # farmer with nothing
    state_next = change_state(state,FARMER)
    if is_valid_state(state_next):
        next_state_all.append(state_next)

    state_next = change_state(state,WOLF)
    if is_valid_state(state_next):
        next_state_all.append(state_next)

    state_next = change_state(state,SHEEP)
    if is_valid_state(state_next):
        next_state_all.append(state_next)

    state_next = change_state(state,CABBAGE)
    if is_valid_state(state_next):
        next_state_all.append(state_next)

    return next_state_all

def cross_river(state):
    global END
    if END == 1:
        print ("congratulation! the farmer crossed the river!")
        return ""
    if is_succeed_state(state):
        END = 1
        print ("The station is %s" % (state))
        return ""
    if state in closed:
        print("Please choose other path!")
        return ""
    
    closed.append(state)

    print ("The station is %s" % (state))

    for next_state in next_step(state):
        cross_river(next_state)



cross_river(init_state)
