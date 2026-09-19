import pygame
import random

#### Setup ####
pygame.init()
screenwith, screenheight = 600,600
screen = pygame.display.set_mode((screenwith, screenheight))
clock = pygame.time.Clock()
gamefield = pygame.Rect(50, 50, 500, 500)
singletile = pygame.Rect(gamefield.left,gamefield.top,50,50)
count_w = int(gamefield.width / singletile.width) # anzahle quadrate in der breite
count_h = int(gamefield.height / singletile.height) # anzahl quadrate in der höhe
#### Grid Creation ####
grid = [[{"mine": False,
        "aufgedeckt": False,
        "markiert": False,
        "nachbarn": 0}
        for j in range(count_w)] for i in range(count_h)]

##### Mine Placement ####
count_mines = 10
placed_mines = 0
while placed_mines < count_mines:
    random_i = random.randint(0, count_h -1)
    random_j = random.randint(0,count_w -1)
    if grid[random_i][random_j]["mine"] == False:
        grid[random_i][random_j]["mine"] = True
        placed_mines+=1
    

### Game Loop ####    
running = True
while running:

    #### Event handler ##############################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Linksklick
                mouse_x,mouse_y = event.pos
                mouse_j = (mouse_x - gamefield.left) // singletile.width
                mouse_i = (mouse_y - gamefield.top) // singletile.height
                if mouse_i >= 0 and mouse_i < count_h:
                    if mouse_j >= 0 and mouse_j < count_w:
                        grid[mouse_i][mouse_j]["aufgedeckt"] = True

    ################### Draw #########################
    screen.fill("white")
    pygame.draw.rect(screen,color="grey",rect=gamefield,width=2)
    for i in range(count_h):
        for j in range(count_w):            

            #### Calculate Single Square ######################
            tile_x = gamefield.left + j * singletile.width
            tile_y = gamefield.top + i * singletile.height
            tile_rect = pygame.Rect(tile_x, tile_y, singletile.width, singletile.height)

            #### Draw ##########################################
            if grid[i][j]["aufgedeckt"] == True:
                pygame.draw.rect(screen,"white",rect=tile_rect)
                pygame.draw.rect(screen,"black",rect=tile_rect,width=1)
            else:
                pygame.draw.rect(screen,"grey",rect=tile_rect)
                pygame.draw.rect(screen,"black",rect=tile_rect,width=1)
            if grid[i][j]["mine"] == True:
                pygame.draw.circle(screen,"red",tile_rect.center,radius=15)
   
   #############################################################################################

    pygame.display.flip() #Show Screen
    clock.tick(60) # Max FPS 60
    
pygame.quit()