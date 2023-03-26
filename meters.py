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
    vs = []
    ls = []
    ts = []
    found = False
    maxlen = 1
    
    for i in range(nodes.len() - 1):
        vs.append((nodes[i+1][0] - nodes[i][0], nodes[i+1][1] - nodes[i][1]))
        ls.append(vs[i][0]*vs[i][0] + vs[i][1]*vs[i][1])
        if i > 0:
            ts.append(vs[i][0]*vs[i+1][0] + vs[i][1]*vs[i+1][1])

    #check palindromes centered on nodes (length is even number)
    for i in range(1, ts.len()):
        if ls[i] != ls[i+1]: #base case: lengths of adjacent vecs are not equal, so not a palindrome
            continue
        length = 1
        while (i - length > 0 and i + length < ts.len() - 1):
            if (ts[i-length] != ts[i+length] or
                ls[i - length] != ls[i + length + 1]):
                break
            if (length > maxlen):
                maxlen = length
                found = True

    #check palindromes centered on segments (length is odd)
    for i in range(2, ls.len()):
        if ls[i-1] != ls[i+1] or ts[i-1] != ts[i]: #base case: lengths of adjacent vecs are not equal, so not a palindrome
            continue
        length = 1
        while (i - length > 0 and i + length < ts.len() - 1):
            if (ts[i- length - 1] != ts[i+length] or
                ls[i - length - 1] != ls[i + length + 1]):
                break
            if (length + 1 > maxlen):
                maxlen = length + 1
                found = True
             
    return ((nodes.len() - maxlen)/nodes.len()) if found else 0.0

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
    s = 0 if nodes[0] == (0,0) else 1
    l = nodes.len()
    t = get_turns(nodes)
    k = get_kmoves(nodes)
    a = get_adj(nodes)
    return s + l + t + k + a

#markov chains
def heidt(nodes, height, width):
    return 0
