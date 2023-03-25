import math
import numpy as np

#definitely need to clean up this arcane garbage
def get_crosses(nodes):
    crosses = 0.0
    for i in range(nodes.len() - 2):
        curr = (nodes[i+1][0] - nodes[i][0], nodes[i+1][1] - nodes[i][1]) #current segment direction
        for j in range(i + 2, nodes.len() - 1):
            other = (nodes[j+1][0] - nodes[j][0], nodes[j+1][1] - nodes[j][1])
            det = other[0]*curr[1] - other[1]*curr[0]
            if (det != 0): #if it's zero there is either no solution or infinitely many solutions, neither of which would be a cross
                dx = float(nodes[j][0] - nodes[i][0])
                dy = float(nodes[j][1] - nodes[i][1])
                k = (dy * other[0] - dx * other[1])/det
                if (k > 0. and k < 1.):
                    crosses += 1
    return crosses

#This one might get complicated
def get_kmoves(nodes):
    moves = 0.0
    for i in range(nodes.len() - 1):
        x = nodes[i][0] - nodes[i+1][0]
        y = nodes[i][1] - nodes[i+1][1]
        #we want to consider the shortest possible path with the same angle
        d = gcd(x, y)
        x = x/d
        y = y/d

        dist = math.abs(vec[0]) + math.abs(vec[1]) - 2
        if dist > 2:
            moves += math.log(dist - 1, 2)
            #returns 1 when it's a normal knight move,
            #and anything bigger has diminishing returns
    return moves

def get_nadj(nodes):
    nonadj = 0
    for i in range(2, nodes.len()):
        px, py = nodes[i]
        vx = nodes[i+1][0] - px
        vy = nodes[i+1][1] - py
        for j in range(i):
            dx = nodes[j][0] - px
            dy = nodes[j][1] - py
            vx1 = nodes[j][0] - nodes[j+1][0]
            vy1 = nodes[j][1] - nodes[j+1][1]
            if (vy * dx == vx * dy and vx*vy1 - vx1*vy == 0):
                d = dx/vx
                if (d > 0. and d < 1.):
                    nonadj += 1
    return nonadj
    
def get_turns(nodes):
    turns = 0.0
    for i in range(nodes.len() - 2):
        x1 = nodes[i][0] - nodes[i+1][0]
        y1 = nodes[i][1] - nodes[i+1][1]
        
        x2 = nodes[i+1][0] - nodes[i+2][0]
        y2 = nodes[i+1][1] - nodes[i+2][1]

        if (x1*y2 - x2*y1 != 0):
            turns += 1
    return turns

#Euclidean distance
def get_eucl(nodes):
    dist = 0.0
    for i in range(nodes.len() - 1):
        vec = (nodes[i][0] - nodes[i+1][0], nodes[i][1] - nodes[i+1][1]) #stinky
        dist += math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])
    return dist

#The sum of max(|x1-x2|, |y1-y2|)
def get_maxd(nodes):
    dist = 0.0
    for i in range(nodes.len() - 1):
        vec = (nodes[i][0] - nodes[i+1][0], nodes[i][1] - nodes[i+1][1])
        dist += max(math.abs(vec[0]), math.abs(vec[1]))
    return dist

#This one might be hard
def get_nonrep(nodes):
    return 0.0

#need to find a way to calculate the maximum maxd value
def song(nodes, height, width):
    d = get_maxd(nodes)
    n = get_nonrep(nodes)
    c = get_crosses(nodes)

    return (0.81 * d / 15) + (0.4 * n) + (0.15 * math.min(c, 5) / 5)

def sun(nodes, height, width):
    l = nodes.len()
    e = get_eucl(nodes)
    c = get_crosses(nodes)
    a = get_nonadj(nodes)
    return l*math.log(e + c + a, 2)

def andriotis(nodes, height, width):
    s = nodes[0] == (0,0) ? 0 : 1
    l = nodes.len()
    t = get_turns(nodes)
    k = get_kmoves(nodes)
    a = get_adj(nodes)
    return s + l + t + k + a

#How many guesses to determine pattern starts at this position (roughly)
#cases where dimension < 3 not yet covered
def start_guesses(nodes,width,height):
    #data pulled from aviv p.306
    mat3 = {{1,3,4},{7,5,9},{2,8,6}} #[y][x]
    mat4 = {{1,4,9,3},{6,5,11.5,13},{8,10,15.5,14},{2,11.5,15.5,7}} #[y][x]

    #for matrices of odd shapes, determine if they are odd or even in size
    #then check which data column they fit most nicely into
    #not perfect, but its the data we have
    if height %2 == 0:
        marky = height//4
        y = mat4[nodes[0][0]//marky]
    else:
        marky = height//3
        y = mat3[nodes[0][0]//marky]
    if width % 2 == 0:
        markx = width//4
    else:
        markx = width//3
    return y[width//markx]/(markx * marky)

    

#assuming we know two consecutive nodes, how many guesses would it take to find the third?
def heidt_helper(nodes,height,width):
    last_node = nodes[0]
    cur_node = nodes[1]

    tot = start_guesses(nodes,width,height)

    for node in nodes[2:]:

        

        last_node = cur_node
        cur_node = node

#The hackiest markov chain you've ever seen
#returns a value between 0 and 1, with 0 being weak, and 1 being strong
#nodes must be at least length 3 to work
def heidt(nodes, height, width):
    if len(nodes < 3):
        return 0
    return min(heidt_helper(nodes,height,width)/pow(width*height-1,len(nodes)),1)







