import sys,os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #hide pygame welcome message
import pygame

"""
Data class for each node
sprite1 is the non-selected sprite
sprite2 is the selected sprite
i,j are the 0-indexed positions in the grid
rect is the pygame.Rectangle which is the physical location on the screen
"""
class Node:
    def __init__(self,sprite1,sprite2,i,j,x,y,width,height):
        self.sprite1 = sprite1
        self.sprite2 = sprite2
        self.x = i
        self.y = j
        self.rect = pygame.Rect(x,y,width,height)

    def collidepoint(self,point):
        return self.rect.collidepoint(point)


WIDTH,HEIGHT = 800,600
MAX_STRENGTH = 480 # width/length of meter bar


# Reverse the calculation on the coords to get the orig i and j vals of each node
def get_ij(given_list,x,y):
    output_list = list()

    for z in given_list:
        x_val = (int(((z[0]*(2*x+1))/WIDTH)/2)) + 1
        y_val = (int(((z[1]*(2*y+1))/((HEIGHT-60) * 0.8))/2)) + 1
        
        output_list.append((x_val,y_val))
    
    return output_list


################################################################################
############ IMPLEMENT THIS ####################################################
def calculate_strength(node_list,x,y,meter):
    node_values = list()
    # ALL METERS must have a max value to calc a percentage of effectiveness to scale the meter display 
    max_instance = 0

    #print(coords_list)

    # DUMMY CALCULATIONS
    # SONG METER
    if meter == "song":
        max_instance = 2*(x*y)
        #print((len(coords_list)/max_instance)*MAX_STRENGTH)
        if (len(node_list)/max_instance) >= 1:
            return MAX_STRENGTH
        return (len(node_list)/max_instance)*MAX_STRENGTH

    # SUN METER
    if meter == "sun":
        summation = 0
        for i in range(len(node_list)):
            value = node_list[i].x
            if i%x == 0:
                value -= i
            max_instance += i
            summation += value     
        if max_instance == 0:
            return 0
            
        #print("this is:",(summation/max_instance)*MAX_STRENGTH)
        if (summation/max_instance) >= 1:
            return MAX_STRENGTH
        return ((summation/max_instance)*MAX_STRENGTH)

    # ANDRIOTIS METER
    #if meter == "andr":
    #    ...
    #    return ...

    # HEIDT-AVIV METER

    # EXPERIMENTAL (PROJECT) METER



##############################################################################

def create_nodes(nodes,x,y):
    x_step,y_step = WIDTH/(2*x + 1),((HEIGHT-60) * 0.8)/(2*y + 1)

    #load images
    icon = pygame.image.load("icon.png").convert()
    icon = pygame.transform.scale(icon,(x_step,y_step))
    icon2 = pygame.image.load("icon2.png").convert()
    icon2 = pygame.transform.scale(icon2,(x_step,y_step))
    
    for i in range(1,x*2,2):
        for j in range(1,y*2,2):
            nodes.append(Node(icon,icon2,(i-1)/2,(j-1)/2,x_step*i,y_step*j,x_step,y_step))

def draw_nodes(screen,nodes,selected_nodes):
    screen.fill((0,0,0))
    for node in nodes:
        screen.blit(node.sprite1,node.rect)
    for node in selected_nodes:
        screen.blit(node.sprite2,node.rect) #overdraw selected nodes

# Draw the meters and labels
def fill_meters(screen,song,sun,andr,heidt,exp):

    text = font.render("Click anywhere to create new pattern", True, (131,139,139))
    text_rect = text.get_rect()
    text_rect.center = (400,423)
    screen.blit(text,text_rect)

    song_label = font.render("SONG METER", True, (255,255,255))
    sun_label = font.render("SUN METER", True, (255,255,255))
    andriotis_label = font.render("ANDRIOTIS METER", True, (255,255,255))
    heidtaviv_label = font.render("HEIDT-AVIV METER", True, (255,255,255))
    experimental_label = font.render("EXPERIMENTAL METER", True, (255,255,255))

    song_rect = song_label.get_rect()
    song_rect.center = (150,463)
    screen.blit(song_label,song_rect)

    sun_rect = sun_label.get_rect()
    sun_rect.center = (150,489)
    screen.blit(sun_label,sun_rect)

    andriotis_rect = andriotis_label.get_rect()
    andriotis_rect.center = (150,515)
    screen.blit(andriotis_label,andriotis_rect)

    heidtaviv_rect = heidtaviv_label.get_rect()
    heidtaviv_rect.center = (150,541)
    screen.blit(heidtaviv_label,heidtaviv_rect)

    experimental_rect = experimental_label.get_rect()
    experimental_rect.center = (150,567)
    screen.blit(experimental_label,experimental_rect)

    pygame.draw.rect(screen, (255,0,0), (290,455,song,20))
    pygame.draw.rect(screen, (255,0,0), (290,480,sun,20))
    pygame.draw.rect(screen, (255,0,0), (290,505,andr,20))
    pygame.draw.rect(screen, (255,0,0), (290,530,heidt,20))
    pygame.draw.rect(screen, (255,0,0), (290,555,exp,20))

    pygame.draw.rect(screen, (255,255,255), (290,455,MAX_STRENGTH,20),1)
    pygame.draw.rect(screen, (255,255,255), (290,480,MAX_STRENGTH,20),1)
    pygame.draw.rect(screen, (255,255,255), (290,505,MAX_STRENGTH,20),1)
    pygame.draw.rect(screen, (255,255,255), (290,530,MAX_STRENGTH,20),1)
    pygame.draw.rect(screen, (255,255,255), (290,555,MAX_STRENGTH,20),1)


def draw_lines(screen,nodes,start, width=5,color=(125,125,125)):
    if start == None:
        return
    last_pos = start
    for node in nodes:
        pygame.draw.line(screen,color,last_pos,node.rect.center,width = width)
        last_pos = node.rect.center
        color = ((color[0]+3) % 255,(color[1]+5) % 255,(color[2]+7) % 255)
    pygame.draw.line(screen,color,last_pos,pygame.mouse.get_pos(),width=width)


def main(x,y):
    nodes = list()
    selected_nodes = list()

    create_nodes(nodes,x,y)

    m_song = 0
    m_sun = 0
    m_andr = 0
    m_heidt = 0
    m_exp = 0

    pattern_created = False
    running = True      #current state of game
    mouse_down = False  #if the mouse is currently down
    coords = None       #place where mouse_down happened
    hover = False       #were we hovering a node last frame
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_down and not pattern_created:
                mouse_down = True
                pattern_created = False
                coords = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and mouse_down and not pattern_created:
                mouse_down = False
                pattern_created = True
                selected_nodes = list()
            if event.type == pygame.MOUSEBUTTONDOWN and pattern_created:
                mouse_down = False
                pattern_created = False
                #print("refresh")

        # Calculate pattern strength
        ########### IMPLEMENT THESE #############
        m_song = calculate_strength(selected_nodes,x,y,"song")
        m_sun = calculate_strength(selected_nodes,x,y,"sun")
        #m_andr = calculate_strength(value_list,x,y,"andr")
        #m_heidt = calculate_strength(value_list,x,y,"heidt")
        #m_exp = calculate_strength(value_list,x,y,"exp")
        
        
        if mouse_down:
            temp = False
            for node in nodes:
                if node.collidepoint(pygame.mouse.get_pos()):
                    temp = True
                    if not hover:
                        if len(selected_nodes) > 0 and node is selected_nodes[-1]:
                            selected_nodes.pop()
                        else:
                            selected_nodes.append(node)
                    break   #can only collide with one rect
            hover = temp

        if not pattern_created:            
            draw_nodes(screen,nodes,selected_nodes)
            fill_meters(screen,m_song,m_sun,m_andr,m_heidt,m_exp)
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

        pygame.init()
        # global variables for configuring window/page state
        screen_width,screen_height = WIDTH,HEIGHT
        screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption("grid lock test")

        font = pygame.font.SysFont("britannic", 20)
        
        main(x,y)
    else:
        print("please ensure both arguments are integers")
    quit()
