import pygame
import random

#### Setup ####
pygame.init()
screen = pygame.display.set_mode((600, 600))
gamefield = pygame.Rect(50, 50, 500, 500)
singletile = pygame.Rect(gamefield.left,gamefield.top,50,50)
count_w = int(gamefield.width / singletile.width) # count rect in width
count_h = int(gamefield.height / singletile.height) # count rect in height
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)


##### Grid Creation #####
grid = [[{"mine": False,
        "is_revealed": False,
        "is_flagged": False,
        "neighbor_count": 0}
        for j in range(count_w)] for i in range(count_h)]

##### Mine Placement ####
count_mines = 20
placed_mines = 0
while placed_mines < count_mines:
    random_i = random.randint(0, count_h -1)
    random_j = random.randint(0,count_w -1)
    if grid[random_i][random_j]["mine"] == False:
        grid[random_i][random_j]["mine"] = True
        placed_mines+=1

################## Update Neighbors #########

## for every tile ##
for i in range(count_h):
    for j in range(count_w):  

        if grid[i][j]["mine"] == True: ## skip if self mine
            continue

        ## every neighbor ##
        for ni in [-1,0,1]:
            for nj in [-1,0,1]:

                if ni == 0 and nj == 0: ## skip self
                    continue

                check_i = i + ni # neighbor index i
                check_j = j + nj # neighbor index j

                if 0 <= check_i < count_h and 0 <= check_j < count_w: # if neighbor is inside the gamefield
                    if grid[check_i][check_j]["mine"] == True:        # if neighbor is mine
                        grid[i][j]["neighbor_count"]+=1               # increase neighbor count
    
######################## Game Loop ###############################    
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
                        grid[mouse_i][mouse_j]["is_revealed"] = True
                        
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
            if grid[i][j]["is_revealed"] == True:
                pygame.draw.rect(screen,"white",rect=tile_rect)
                pygame.draw.rect(screen,"black",rect=tile_rect,width=1)

                if grid[i][j]["neighbor_count"] > 0:  ### if has neighbors
                    mines = grid[i][j]["neighbor_count"]    
                    text_surface = font.render(str(mines),True,"black")         ### change number into picture 
                    text_rect = text_surface.get_rect(center=tile_rect.center)  ### get center pos of rect
                    screen.blit(text_surface,text_rect)                         ### display picture at rect center
            else:
                pygame.draw.rect(screen,"grey",rect=tile_rect)
                pygame.draw.rect(screen,"black",rect=tile_rect,width=1)

            #draw mine# (delete later)
            if grid[i][j]["mine"] == True:
                pygame.draw.circle(screen,"red",tile_rect.center,radius=15)
   
   #############################################################################################

    pygame.display.flip() #Show Screen
    clock.tick(60) # Max FPS 60
    
pygame.quit()