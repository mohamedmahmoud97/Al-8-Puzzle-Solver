import sys
import heapq
import math

class Node:
    def __init__(self, state, parent, action, cost_f=None, cost_g = None):
        self.state = state
        if parent == False:
            self.parent = False
            self.action = ''
        else:
            self.parent = parent
            self.action = action
        self.cost_g = 0
    
    def print_puzzle(self):
        string = ''
        string = string + '+---+---+---+\n'
        for i in range(3):
            for j in range(3):
                tile = self.state[i * 3 + j]
                string = string + '| {} '.format(' ' if tile == '0' else tile)
            string = string + '|\n'
            string = string + '+---+---+---+\n'
        print(string)

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
    #bfs
    if searchType == 'bfs' or searchType == 'ae' or searchType == 'am':
        if z-3 >= 0: addNewNode(Node(swap(b, z, z-3), node, 'Up'), frontier, explored,searchType)
        if z+3 <= 8: addNewNode(Node(swap(b, z, z+3), node, 'Down'), frontier, explored,searchType)
        if z%3-1 >= 0: addNewNode(Node(swap(b, z, z-1), node, 'Left'), frontier, explored,searchType)
        if z%3+1 < 3: addNewNode(Node(swap(b, z, z+1), node, 'Right'), frontier, explored,searchType)
    #dfs
    elif searchType == 'dfs':
        if z%3+1 < 3: addNewNode(Node(swap(b, z, z+1), node, 'Right'), frontier, explored,searchType)
        if z%3-1 >= 0: addNewNode(Node(swap(b, z, z-1), node, 'Left'), frontier, explored,searchType)
        if z+3 <= 8: addNewNode(Node(swap(b, z, z+3), node, 'Down'), frontier, explored,searchType)
        if z-3 >= 0: addNewNode(Node(swap(b, z, z-3), node, 'Up'), frontier, explored,searchType)

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
        curr_x = newNode.state.index('0') % 3
        curr_y = newNode.state.index('0') // 3
        if searchType == 'am':
            newNode.cost = abs(curr_x) + abs(curr_y)
        elif searchType == 'ae':
            newNode.cost = math.sqrt(pow((curr_x),2) + pow((curr_y),2))
        

def getPathToGoal(node):
    path = []
    while node.parent:
        path.append(node)
        node = node.parent
    path.reverse()
    return path

def Success(node):
    goal_path = getPathToGoal(node)
    for x in goal_path:
        x.print_puzzle()
    return "successfully solved the problem"
    

# bfs algorithm
def bfs(init_state, goal):
    frontier = []
    init_node = Node(init_state, False, '')
    frontier.append(init_node)
    explored = []
    
    while len(frontier)!=0:
        curr_node = frontier.pop(0)
        explored.append(curr_node)

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

def a_star(init_state, goal, searchType):
    frontier = []
    init_node = Node(init_state, False, '')
    heapq.heappush(frontier, init_node)
    explored = []
    
    while len(frontier)!=0:
        curr_node = heapq.heappop()
        explored.append(curr_node)

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