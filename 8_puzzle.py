import queue

class Node:

    def __init__(self, state, parent, action, cost=None):
        self.state = state
        if parent == False:
            self.parent = False
            self.action = ''
        else:
            self.parent = parent
            self.action = action
        self.cost = cost
    
    def __str__(self):
        string = ''
        string = string + '+---+---+---+\n'
        for i in range(3):
            for j in range(3):
                tile = self.state[i * 3 + j]
                string = string + '| {} '.format(' ' if tile == 0 else tile)
            string = string + '|\n'
            string = string + '+---+---+---+\n'
        return string

    def swap(self, state, z, new):
        newState = state[:]
        newState[z] = state[new]
        newState[new] = '0'

    # expand all the possible neighbor nodes
    def expand_nodes(self, frontier, explored, searchType):
        b = self.state
        z = self.state.index('0')
        
        #check Up,Down,Left,Right neighbor nodes
        #bfs
        if searchType == 'bfs' or searchType == 'ast':
            if z-3 >= 0: self.addNewNode(Node(self.swap(b, z, z-3), self, 'Up'), frontier, explored)
            if z+3 <= 8: self.addNewNode(Node(self.swap(b, z, z+3), self, 'Down'), frontier, explored)
            if z%3-1 >= 0: self.addNewNode(Node(self.swap(b, z, z-1), self, 'Left'), frontier, explored)
            if z%3+1 < 3: self.addNewNode(Node(self.swap(b, z, z+1), self, 'Right'), frontier, explored)
        #dfs
        elif searchType == 'dfs':
            if z%3+1 < 3: self.addNewNode(Node(self.swap(b, z, z+1), self, 'Right'), frontier, explored)
            if z%3-1 >= 0: self.addNewNode(Node(self.swap(b, z, z-1), self, 'Left'), frontier, explored)
            if z+3 <= 8: self.addNewNode(Node(self.swap(b, z, z+3), self, 'Down'), frontier, explored)
            if z-3 >= 0: self.addNewNode(Node(self.swap(b, z, z-3), self, 'Up'), frontier, explored)

    def addNewNode(self, newNode, frontier, explored):
        if newNode.state not in frontier and newNode.state not in explored:
            frontier.append(newNode.state)

def Success(node):
    
    return

# bfs algorithm
def bfs(init_state, goal):
    frontier = []
    init_node = Node(init_state, False, '')
    frontier.append(init_node.state)
    explored = []
    
    while len(frontier)!=0:
        curr_state = frontier.pop(0)
        explored.append(curr_state)

        if curr_state == goal:
            return Success(curr_state)
        
        curr_state.expand_nodes(frontier, explored, 'bfs')
    
    return -1