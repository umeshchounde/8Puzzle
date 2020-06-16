import numpy as np
#from prompt_toolkit.shortcuts import get_input

path_cost = []
h1 = []
fn = []
h1_value = 0
count = 0
child_node = []
goal_node = []
visited_node = []
total_dic = {}
finish = False
heu = 1


class puzzle_test:
    
    def __init__(self):
        self.min_val = 0
        self.min_val_index = 0
    def get_input(self):
        
        global goal_node, heu
        l = [[int(num) for num in input("Initial state. Enter 3 numbers per line separated by a single space :").split()]]
        l.append ([int(num) for num in input("Next 3 numbers: ").split()])
        l.append ([int(num) for num in input("Last 3 numbers: ").split()])
        
        g = [[int(num) for num in input("Final state. Enter 3 numbers per line separated by a single space :").split()]]
        g.append ([int(num) for num in input("Next 3 numbers: ").split()])
        g.append ([int(num) for num in input("Last 3 numbers: ").split()])
        
        goal_node = np.array(g)
        #l=[[1,2,3],[7,4,5],[6,8,0]]
        #goal_node = np.array([[1,2,3],[8,6,4],[7,5,0]])
        print ("Available Heuristics are ")
        print ("1. Misplaced Tiles, 2. Manhattan distance ")
        heu = input("Enter your choice of heuristic (1 or 2):")

        return l
        
    def goal_Test(self, node):
        self.node = np.array(node)
        result = np.array_equal(node, goal_node)
        return (result)
    
    def goal_dict(self, goal_node):
        goal_dictI=Astar_impl(goal_node)
        goal_dict1=goal_dictI.co_ordinates(goal_node)
        return goal_dict1
        
    def child_node_gen(self, node):
        global child_node, count, total_dic, h1_value
        self.node = np.array(node)
        #temp_node = list(node)
        temp_node = np.copy(self.node)
        #print( "Node to be expanded is ")
        #print( self.node)
        zero = np.where(temp_node == 0)
        zero_loc = np.empty([2], dtype=int)
        for i in range(0,2):
            zero_loc[i] = zero[i]
            #np.insert(zero_loc, i, zero[i])
        #print( "Zero is at location " + str(zero_loc))
        
        count = 0
        
        #Move up
        if zero_loc[0] > 0:
            temp_node[zero_loc[0]][zero_loc[1]] = temp_node[(zero_loc[0] - 1)][zero_loc[1]]
            temp_node[(zero_loc[0] - 1)][zero_loc[1]] = 0
            #print( "Move up")
            child_node.append(temp_node)
            count += 1
        temp_node = np.copy(node)
        
        
        #Move down
        if zero_loc[0] < 2:
            temp_node[zero_loc[0]][zero_loc[1]] = temp_node[(zero_loc[0] + 1)][zero_loc[1]]
            temp_node[(zero_loc[0] + 1)][zero_loc[1]] = 0
            #print( "Move down")
            child_node.append(temp_node)
            count += 1
            #print( child_node
        temp_node = np.copy(node)
        
        #Move right
        if zero_loc[1] < 2:
            temp_node[zero_loc[0]][zero_loc[1]] = temp_node[zero_loc[0]][(zero_loc[1] + 1)]
            temp_node[zero_loc[0]][(zero_loc[1] + 1)] = 0
            child_node.append(temp_node)
            #print( "Move right")
            count += 1
        temp_node = np.copy(node)
        
        #Move left
        if zero_loc[1] > 0:
            temp_node[zero_loc[0]][zero_loc[1]] = temp_node[zero_loc[0]][(zero_loc[1] - 1)]
            temp_node[zero_loc[0]][(zero_loc[1] - 1)] = 0
            child_node.append(temp_node)
            #print( "Move left")
            count += 1
        temp_node = np.copy(node)
        
        count_red = 0
        #print( child_node)
        #print( "Check for duplicacy. New child node count is " + str(count))
        for i in range (0, len(visited_node)):
            for j in range (count, 0, -1):
                #print( j)
                if np.array_equal(visited_node[i], child_node[len(child_node)-j]):
                    #print( "Duplicate found")
                    #print( child_node[len(child_node)-j])
                    count_red += 1
                    del child_node[len(child_node)-j]
                    #print( "count reduced by " + str(count_red))
                                    
        if count_red > 0:
            for i in range(0, count_red):
                count -= 1
            #print( "count " + str(count))
        return child_node
        
    def compare(self, child_node):
        global h1, path_cost, fn
        fn = []
        #print (len(path_cost), len(h1))
        for i in range(0, len(path_cost)):
            #print (path_cost[i], h1[i])
            total = path_cost[i] + h1[i]
            fn.append(total)
        #print( "fn is " + str(fn))
        fn = np.array(fn)
        self.min_val = np.amin(fn)
        self.min_val_index = np.argmin(fn)
        #print( "minimum function cost is " + str(self.min_val) + " at value " + str(self.min_val_index))

        #Add node with least value to visited_node and pop it out of child_nodes
        visited_node.append(child_node[self.min_val_index])
        #print( "Visited node added")
        del child_node[self.min_val_index]
        del path_cost[self.min_val_index]
        del h1[self.min_val_index]    
        
class Astar_impl():
    global path_cost, count
    def __init__(self, node):
        self.node = node
        #self.get_path_cost(node)
    
    def get_path_cost(self, node1, node2):
        global h1_value
        child_node = node1
        self.node = node2
        h1_value = total_dic[str(self.node)][1] + 1
        for i in range(count, 0, -1):
            #print( "i is " +str(-i))
            total_dic[str(child_node[-i])] = [str(self.node), h1_value]
            path_cost.append(h1_value)
        #print( total_dic[str(child_node[count-1])][1]
        #print( "total dic count is " + str(len(total_dic)))
        #print( total_dic)
        
                    
    def misplacedH(self, node, goal):
        global misplaced, h1
        h1 = []
        print( "Misplaced tiles heuristic chosen")
        self.goal_node = goal
        self.node = node
        #misplaced = [0 for x in range(0, len(node))]
        #print( misplaced
        #print( self.goal_node
        #print( self.node
        for i in range(0, len(self.node)):
            misplaced = 0
            for j in range (0, 3):
                for k in range(0, 3):
                    #print( self.node[i][j][k]
                    if self.node[i][j][k] != self.goal_node[j][k]:
                        misplaced += 1                        
            h1.append(misplaced)
        #print( "Misplaced tile heuristic of child nodes is " + str(misplaced)

    def co_ordinates(self, goal_node):
        coordinates_dict={}
        for x,row in enumerate(goal_node):
            for y,val in enumerate(row):
                #val1=hash(tuple(np.array(val)))
                coordinates_dict[val]=(x,y)
        return coordinates_dict
    
    def manhattan_distance(self,child_node):
        #print((child_node))
        co_ord1=self.co_ordinates(child_node)
        dist=0
        for i in range (9):
            
            j=(co_ord1.get(i))
            k=(goal_dict1.get(i))
            dist+=abs(j[0]-k[0])+abs(j[1]-k[1])
            #print(dist)
        return dist
        
    def find_path(self, node):
        path = []
        res = str(node)
        path.insert(0,res)
        #print( str(visited_node[0]))
        while res != str(visited_node[0]):
            res = total_dic[res][0]    
            path.insert(0,res)
        #print( "Path is ")
        for r,j in enumerate(path):
            print(j)
        
class main_func():
    global path_cost, h1, h1_value, goal_node, visited_node, finish, fn, child_node, total_node,goal_dict1, heu
    
    print("Welcome to 8 puzzle problem implementation")
    print( "")
    p = puzzle_test()
    l = np.array(p.get_input())
    goal_dict1=p.goal_dict(goal_node)
    print ("Your initial state is ")
    print( l)
    print( "")
    print( "Goal state is ")
    print( goal_node)
    visited_node.append(l)
    total_dic[str(l)] = [str(l), h1_value]
    #total_node.append(l)
    result = p.goal_Test(visited_node[len(visited_node) - 1])
    if result == True:
        finish = True
    '''shape = np.shape(parent_node)
    print( "Array shape is ", shape'''
    i = 0
    
    while finish != True:
        #Generate child_nodes
        p.child_node_gen(visited_node[i])
        #print( "Child nodes are ")
        #print( child_node)    
        #heu1=1
        #Get Heuristic and path_cost
        a = Astar_impl(child_node)
        if int(heu)==1: 
            print()
            a.misplacedH(child_node, goal_node)
        else:
            h1=[]
            for child_node1 in child_node:
                misplaced=a.manhattan_distance(child_node1)
                h1.append(misplaced)
        a.get_path_cost(child_node, visited_node[i])
        
        #print( "Path costs are " + str(path_cost))
        #print( "H1 heuristic is " + str(h1))
        
        #Compare to get minimum value node1
        p.compare(child_node)
        #print( "New child nodes are ")
        #print( child_node)
        #print( "Visited nodes are ")
        #print( visited_node)
        
        #Check if goal reached
        result = p.goal_Test(visited_node[len(visited_node) - 1])
        #print( "Goal state achieved? " + str(result))
        if result == True:
            print( "Goal reached")
            print("Total nodes generared is " + str(len(total_dic)))
            print( "Total nodes expanded is " + str(len(visited_node)))
            #print("Path is ")
            a.find_path(visited_node[len(visited_node) - 1])
            finish = True
            #print( "Total levels is " + str(i))
        '''if result == True:
            min_fn = min(fn)
            print( "min value of "
        '''
        i += 1
        if i == 10000:
            a.find_path(visited_node[len(visited_node) - 1])
            finish = True

main_func()        


