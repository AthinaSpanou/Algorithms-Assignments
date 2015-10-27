import sys
import random

n = int(sys.argv[1]) #the dimensions of the maze (number of lines and columns)
start_x=int(sys.argv[2]) #the start line of the maze
start_y=int(sys.argv[3]) #the start column of the maze
random.seed(sys.argv[4])
outfile=sys.argv[5] #the output file in which the path of the maze (the labyrinth) will be written

while n<=0:
    print("ERROR! Dimension should be a positive number!")
    n=int(input("Please, give again the dimension you want your maze to have: "))

graph={} #the graph used to create the maze

for i in range(0,n):
    for j in range(0,n):
        if i==0 and j==0: #(0,0)
            graph[(i,j)]=[(i,j+1),(i+1,j)]
        elif i==n-1 and j==0: #(n-1,0)
            graph[(i,j)]=[(i,j+1),(i-1,j)]
        elif i==0 and j==n-1: #(0,n-1)
            graph[(i,j)]=[(i,j-1),(i+1,j)]
        elif i==n-1 and j==n-1: #(n-1,n-1)
            graph[(i,j)]=[(i,j-1),(i-1,j)]
        elif 0<i<n and j==0: #point in the periphery
            graph[(i,j)]=[(i-1,j),(i,j+1),(i+1,j)]
        elif 0<i<n and j==n-1: #point in the periphery
            graph[(i,j)]=[(i-1,j),(i+1,j),(i,j-1)]
        elif i==0 and 0<j<n: #point in the periphery
            graph[(i,j)]=[(i,j-1),(i+1,j),(i,j+1)]
        elif i==n-1 and 0<j<n: #point in the periphery
            graph[(i,j)]=[(i,j-1),(i,j+1),(i-1,j)]
        elif 0<i<n and 0<j<n: #every other point
            graph[(i,j)]=[(i,j-1),(i,j+1),(i+1,j),(i-1,j)]

output_file = open(outfile, "w") #open the output file in which the path of the labyrinth will be written

while start_x not in range(0,n): #check if 0 <= start_x < n
    print("Error ! Value must be in the range you gave ! Please give value again ! ")
    start_x=int(input("Please give start x: "))

while start_y not in range(0,n): #check if 0 <= start_y < n
    print("Error ! Value must be in the range you gave ! Please give value again ! ")
    start_y=int(input("Please give start y: "))

path=[] #list that shows the path of the maze
path.append((start_x,start_y)) #add to the list the first node user gives

def search(node):
    neighbouring_nodes=[] #list that contains the neighbours of a node
    neighbouring_nodes=graph[node] #take the neighbours of the node
    random_neighbours = random.sample(neighbouring_nodes,len(neighbouring_nodes))
    for k in range(0,len(random_neighbours)):
        b=random_neighbours[k] #take a neighbour from the random_neighbours list
        if b not in path: #if the neighbour is not visited
            path.append(b) #add neighbour in the list
            output_file.write(str(node) + ", " + str(b) + "\n") #write the node and its neighbour
            search(b) #call again method search

search((start_x,start_y)) #call method search for the values that user has given

output_file.close() #close the output file in which the path of the labyrinth has been written
