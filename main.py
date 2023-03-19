import sys,os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #hide pygame welcome message
import pygame

WIDTH,HEIGHT = 800,600

def create_rects(nodes,x,y):
    x_step,y_step = WIDTH/(2*x + 1),(HEIGHT * 0.8)/(2*y + 1)

    icon = pygame.image.load("icon.png").convert()
    icon = pygame.transform.scale(icon,(x_step,y_step))
    icon2 = pygame.image.load("icon2.png").convert()
    icon2 = pygame.transform.scale(icon2,(x_step,y_step))
    
    for i in range(1,x*2,2):
        for j in range(1,y*2,2):
            nodes.append((icon,icon2,pygame.Rect(x_step*i,y_step*j,x_step,y_step)))

def draw_nodes(screen,nodes,selected_nodes):
    screen.fill((0,0,0))
    for node in nodes:
        screen.blit(node[0],node[2])
    for node in selected_nodes:
        screen.blit(node[1],node[2]) #overdraw selected nodes
    
def draw_lines(screen,nodes,start, width=5,color=(125,125,125)):
    if start == None:
        return
    last_pos = start
    for node in nodes:
        pygame.draw.line(screen,color,last_pos,node[2].center,width = width)
        last_pos = node[2].center
        color = ((color[0]+3) % 255,(color[1]+5) % 255,(color[2]+7) % 255)
    pygame.draw.line(screen,color,last_pos,pygame.mouse.get_pos(),width=width)

def main(x,y):
    rects = list()
    selected_nodes = list()

    pygame.init()
    screen_width,screen_height = WIDTH,HEIGHT
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("grid lock test")

    create_rects(rects,x,y)

    running = True      #current state of game
    mouse_down = False  #if the mouse is currently down
    coords = None       #place where mouse_down happened
    hover = False       #were we hovering a node last frame
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_down:
                mouse_down = True
                coords = pygame.mouse.get_pos()
                #print('event',coords)
            if event.type == pygame.MOUSEBUTTONUP and mouse_down:
                mouse_down = False
                selected_nodes = list()
                #print('event2')
        
        if mouse_down:
            temp = False
            for rect in rects:
                if rect[2].collidepoint(pygame.mouse.get_pos()):
                    temp = True
                    if not hover:
                        if len(selected_nodes) > 0 and rect is selected_nodes[-1]:
                            selected_nodes.pop()
                        else:
                            selected_nodes.append(rect)
                    break   #can only collide with one rect
            hover = temp
                    
        draw_nodes(screen,rects,selected_nodes)
        if mouse_down:
            draw_lines(screen,selected_nodes,coords)
        
    
        
        pygame.display.flip()


if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) < 3:
        print("please provide two numerical arguments")
        quit()
    if sys.argv[1].isnumeric() and sys.argv[2].isnumeric():
        print(sys.argv[1],sys.argv[2])
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        main(x,y)
    else:
        print("please ensure both arguments are integers")
    quit()
