import sys,os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #hide pygame welcome message
import pygame

WIDTH,HEIGHT = 800,600

def create_rects(nodes,x,y):

    x_step,y_step = WIDTH/x,HEIGHT/y
    
    for i in range(x):
        for j in range(y):
            icon = pygame.image.load("icon.png").convert()
            icon = pygame.transform.scale(icon,(x_step,y_step))
            nodes.append((icon,i*x_step,j*y_step))

def draw_nodes(screen,nodes):
    screen.fill((0,0,0))
    for node in nodes:
        screen.blit(node[0],(node[1],node[2]))
    

def main(x,y):
    rects = list()

    pygame.init()
    screen_width,screen_height = WIDTH,HEIGHT
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("grid lock test")

    create_rects(rects,x,y)
    
    running = True
    mouse_down = False
    coords = None
    while running:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_down:
                mouse_down = True
                coords = pygame.mouse.get_pos()
                print('event',coords)
            if event.type == pygame.MOUSEBUTTONUP and mouse_down:
                mouse_down = False
                print('event2')

        draw_nodes(screen,rects)
        if mouse_down:
            pygame.draw.line(screen,pygame.Color(125,125,125),coords,pygame.mouse.get_pos(),width=5)
        
        pygame.display.flip()


if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) < 3:
        print("please provide two numerical argument")
        quit()
    if sys.argv[1].isnumeric() and sys.argv[2].isnumeric():
        print(sys.argv[1],sys.argv[2])
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        main(x,y)
    else:
        print("please ensure both arguments are integers")
    quit()
