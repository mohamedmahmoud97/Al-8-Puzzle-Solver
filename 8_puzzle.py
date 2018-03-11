import sys
import heapq
import math
import colorama
import time

colorama.init()
def put_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))

class Node:
    def __init__(self, state, parent, action, cost_f =None, cost_g = None):
        self.state = state
        if parent == False:
            self.parent = False
            self.action = ''
        else:
            self.parent = parent
            self.action = action
        self.cost_g = 0
        self.cost_f = 0
    
    def print_puzzle(self):
        string = '\n Solving the puzzle:\n\n'
        string = string + '+---+---+---+\n'
        for i in range(3):
            for j in range(3):
                tile = self.state[i * 3 + j]
                string = string + '| {} '.format(' ' if tile == '0' else tile)
            string = string + '|\n'
            string = string + '+---+---+---+\n'
        put_cursor(0,0)
        print('{0}\r'.format(string))
        time.sleep(0.5) 
        

# swap the zero index and the decided next move index
def swap(state, z, new):
    newState = state[:]
    newState[z] = state[new]
    newState[new] = '0'
    return newState

# expand all the possible neighbor nodes
def expand_nodes(node, frontier, explored, searchType):
    b = node.state
    z = node.state.index('0')
    
    #check Up,Down,Left,Right neighbor nodes
    #for bfs, A*(manhattan and euclidean)
    if searchType == 'bfs' or searchType == 'ae' or searchType == 'am':
        if z-3 >= 0: addNewNode(Node(swap(b, z, z-3), node, 'Up'), frontier, explored,searchType)
        if z+3 <= 8: addNewNode(Node(swap(b, z, z+3), node, 'Down'), frontier, explored,searchType)
        if z%3-1 >= 0: addNewNode(Node(swap(b, z, z-1), node, 'Left'), frontier, explored,searchType)
        if z%3+1 < 3: addNewNode(Node(swap(b, z, z+1), node, 'Right'), frontier, explored,searchType)
    # dfs
    elif searchType == 'dfs':
        if z%3+1 < 3: addNewNode(Node(swap(b, z, z+1), node, 'Right'), frontier, explored,searchType)
        if z%3-1 >= 0: addNewNode(Node(swap(b, z, z-1), node, 'Left'), frontier, explored,searchType)
        if z+3 <= 8: addNewNode(Node(swap(b, z, z+3), node, 'Down'), frontier, explored,searchType)
        if z-3 >= 0: addNewNode(Node(swap(b, z, z-3), node, 'Up'), frontier, explored,searchType)

#add the new node and check if it was in the frontier or the explored lists or not
def addNewNode(newNode, frontier, explored, searchType):
    if searchType == 'bfs' or searchType == 'dfs':
        for x in frontier:
            if newNode.state == x.state:
                return
        for x in explored:
            if newNode.state == x.state:
                return
        frontier.append(newNode)
        return
    else:
        found = 0
        del_node = newNode
        for x in explored:
            if newNode.state == x.state:
                found = 2
                break
        for x,_ in frontier:
            if newNode.state == x.state:
                found = 1
                del_node = x
                break

        curr_x = newNode.state.index('0') % 3
        curr_y = newNode.state.index('0') // 3
        if searchType == 'am':
            newNode.cost_g = newNode.parent.cost_g + 1
            h = abs(curr_x) + abs(curr_y)
            newNode.cost_f = newNode.cost_g + h
        elif searchType == 'ae':
            newNode.cost_g = newNode.parent.cost_g + 1
            h = math.sqrt(pow((curr_x),2) + pow((curr_y),2))
            newNode.cost_f = newNode.cost_g + h
        
        if found == 1:
            frontier.remove((del_node,del_node.cost_f))
        frontier.append((newNode,newNode.cost_f))
        frontier.sort(key=lambda tup: tup[1])

# get the whole path of the goal
def getPathToGoal(node):
    path = []
    while node.parent:
        path.append(node)
        node = node.parent
    path.reverse()
    return path

# the success function to print every step of the path to goal
def Success(node):
    goal_path = getPathToGoal(node)
    for x in goal_path:
        x.print_puzzle()
    return "Successfully solved the problem\n"
    
# bfs algorithm
def bfs(init_state, goal):
    frontier = []
    init_node = Node(init_state, False, '')
    frontier.append(init_node)
    explored = []
    
    while len(frontier)!=0:
        curr_node = frontier.pop(0)
        explored.append(curr_node)
        # curr_node.print_puzzle()

        if curr_node.state == goal:
            return Success(curr_node)
        
        expand_nodes(curr_node, frontier, explored, 'bfs')
    
    return "There is no any way to solve this shitty problem dude."

# dfs algorithm
def dfs(init_state, goal):
    frontier = []
    init_node = Node(init_state, False, '')
    frontier.append(init_node)
    explored = []
    
    while len(frontier)!=0:
        curr_node = frontier.pop()
        explored.append(curr_node)

        if curr_node.state == goal:
            return Success(curr_node)
        
        expand_nodes(curr_node, frontier, explored, 'dfs')
    
    return "There is no any way to solve this shitty problem dude."

# A* algorithm 
def a_star(init_state, goal, searchType):
    frontier = []
    init_node = Node(init_state, False, '')
    frontier.append((init_node, 0))
    #heapq.heappush(frontier, init_node)
    explored = []
    
    while len(frontier)!=0:
        curr_node,_ = frontier.pop(0)
        explored.append(curr_node)
        # curr_node.print_puzzle()

        if curr_node.state == goal:
            return Success(curr_node)

        expand_nodes(curr_node, frontier, explored, searchType)
    
    return "There is no any way to solve this shitty problem dude."

if len(sys.argv)>1:
    myboard = sys.argv[1]
    searchType = sys.argv[2]
else:
    myboard = '1,2,5,3,4,0,6,7,8'
    searchType = 'ast'

goal = '0,1,2,3,4,5,6,7,8'
goal = goal.split(',')
init = myboard.split(',')
result = ""
if searchType == "bfs":
    result = bfs(init, goal)
elif searchType == "dfs":
    result = dfs(init, goal)
elif searchType == "am" or searchType == "ae":
    result = a_star(init, goal, searchType)
print(result)