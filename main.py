import pygame
import random

#TODO Chain reveal
#TODO implement first click safe
#TODO Implement difficulties
#TODO enum


#### Setup ####
pygame.init()
width,height = 800,540
margin,gap = 20,10
screen = pygame.display.set_mode((width, height))
gamefield = pygame.Rect(margin, margin, 500, 500)
singletile = pygame.Rect(gamefield.left,gamefield.top,50,50)
tile_count_x = int(gamefield.width / singletile.width) # count rect in width
tile_count_y = int(gamefield.height / singletile.height) # count rect in height
clock = pygame.time.Clock()
score = 0

##### Text Box ####
textframe_x = gamefield.right+gap
textframe_w = width - textframe_x - margin
textframe = pygame.Rect(textframe_x,margin,textframe_w,gamefield.height)

font_small = pygame.font.SysFont(None,20)
font = pygame.font.SysFont(None, 30)
font_large = pygame.font.SysFont(None,60)

def reset_game():
    game_over = False
    game_won = False

    ##### Grid Creation #####
    grid = [[{"mine": False,
            "is_revealed": False,
            "is_flagged": False,
            "neighbor_count": 0}
            for j in range(tile_count_x)] for i in range(tile_count_y)]

    ##### Mine Placement ####
    count_mines = int(tile_count_x * tile_count_y * 0.1)
    placed_mines = 0
    while placed_mines < count_mines:
        random_i = random.randint(0, tile_count_y -1)
        random_j = random.randint(0,tile_count_x -1)
        if grid[random_i][random_j]["mine"] == False:
            grid[random_i][random_j]["mine"] = True
            placed_mines+=1

    ################## Update Neighbors #####################

    ## for every tile ##
    for i in range(tile_count_y):
        for j in range(tile_count_x):  

            if grid[i][j]["mine"] == True: ## skip if self mine
                continue

            ## every neighbor ##
            for ni in [-1,0,1]:
                for nj in [-1,0,1]:

                    if ni == 0 and nj == 0: ## skip self
                        continue

                    check_i = i + ni # neighbor index i
                    check_j = j + nj # neighbor index j

                    if check_j >= 0 and check_j < tile_count_x:               # ifs check is in gamefield area
                        if check_i >= 0 and check_i < tile_count_y:           #

                            if grid[check_i][check_j]["mine"] == True:        # if neighbor is mine
                                grid[i][j]["neighbor_count"]+=1               # increase neighbor count

    return grid, game_over, game_won, count_mines
    
def check_win(grid):
    for i in range(tile_count_y): 
        for j in range(tile_count_x):
            if grid[i][j]["mine"] == False and grid[i][j]["is_revealed"] == False:
                return False  
    return True

def draw_text(surface, text, font, color, center_pos):
    text_surf = font.render(str(text), True, color)         #create text as picture
    text_rect = text_surf.get_rect(center=center_pos)       #position picture
    surface.blit(text_surf, text_rect)                      #Display on screen

def count_flags(grid):
    count = 0
    for i in range(tile_count_y):
        for j in range(tile_count_x):
            if grid[i][j]["is_flagged"] == True:
                count += 1
    return count

def get_grid_pos(mouse_pos):
    mouse_x,mouse_y = mouse_pos
    mouse_j = (mouse_x - gamefield.left) // singletile.width
    mouse_i = (mouse_y - gamefield.top) // singletile.height
    if mouse_i >= 0 and mouse_i < tile_count_y:      # check if mouse is in gamefield
        if mouse_j >= 0 and mouse_j < tile_count_x:
            return mouse_i,mouse_j
    return None,None

######################## Game Loop ###############################    
running = True
grid,game_over,game_won,mines_count = reset_game()
while running:

    #### Event handler ###################################################################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                grid,game_over,game_won,mines_count = reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # LMB                  
                if game_over == False and game_won == False:

                    mouse_i,mouse_j = get_grid_pos(event.pos)                                     
                    if mouse_i is not None and mouse_j is not None:
                        if grid[mouse_i][mouse_j]["is_flagged"] == False:                                                                                           
                            grid[mouse_i][mouse_j]["is_revealed"] = True    ## Reveal
                                    ###check game status ##
                            if grid[mouse_i][mouse_j]["mine"] == True:      ## if mine revealed
                                game_over = True
                            else:
                                game_won = check_win(grid)
                                if game_won == True:
                                    score += 1

            if event.button == 3: # RMB   
                if game_over == False and game_won == False:             
                    mouse_i,mouse_j = get_grid_pos(event.pos)
                    if mouse_i is not None and mouse_j is not None:
                        if grid[mouse_i][mouse_j]["is_revealed"] == False: 
                            if grid[mouse_i][mouse_j]["is_flagged"] == False:
                                grid[mouse_i][mouse_j]["is_flagged"] = True
                            else:
                                grid[mouse_i][mouse_j]["is_flagged"] = False

    ################### Draw ###########################################################################
    screen.fill("white")
    pygame.draw.rect(screen,color="grey",rect=gamefield,width=2)
    for i in range(tile_count_y):
        for j in range(tile_count_x):            

            ####### Calculate Single Square #######################
            tile_x = gamefield.left + j * singletile.width
            tile_y = gamefield.top + i * singletile.height
            tile_rect = pygame.Rect(tile_x, tile_y, singletile.width, singletile.height)

            ####### Draw ##########################################
            if grid[i][j]["is_revealed"] == True:
                pygame.draw.rect(screen,"white",rect=tile_rect)
                pygame.draw.rect(screen,"black",rect=tile_rect,width=1)
                if grid[i][j]["mine"] == True:
                    pygame.draw.circle(screen,"red",tile_rect.center,radius=(tile_rect.width/3))

                if grid[i][j]["neighbor_count"] > 0:    ### if has neighbors
                    mines = grid[i][j]["neighbor_count"]    
                    text_surface = font.render(str(mines),True,"black")         ### change number into picture 
                    text_rect = text_surface.get_rect(center=tile_rect.center)  ### get center pos of rect
                    screen.blit(text_surface,text_rect)                         ### display picture at rect center
            else:
                pygame.draw.rect(screen,"grey",rect=tile_rect)
                pygame.draw.rect(screen,"black",rect=tile_rect,width=1)
                
                if grid[i][j]["is_flagged"] == True: ##################################### if flagged draw flag ##################################
                    flag_rect = pygame.Rect(0,0,tile_rect.width/2,tile_rect.height/2)
                    flag_rect.center = tile_rect.center
                    pygame.draw.rect(screen,"blue",rect=flag_rect)

    ##### TextBox #####
    pygame.draw.rect(screen,"black",textframe,width=1)
    score_pos = (textframe.centerx,textframe.top + 40)
    flagged_pos = (textframe.centerx,textframe.bottom - 120)
    mine_count_pos = (textframe.centerx,textframe.bottom - 80)
    reset_pos = (textframe.centerx,textframe.bottom - 40)
    draw_text(screen,f"Score: {score}",font,"black",score_pos)
    draw_text(screen,f"Mines: {mines_count}",font,"black",mine_count_pos) 
    draw_text(screen,f"Flagges: {count_flags(grid)}",font,"black",flagged_pos)
    draw_text(screen,"Press R to Restart",font_small,"black",reset_pos)

    ################################ Game Over #########################################
    if game_over:

        ###### Game Over #######
        text_surface = font_large.render("GAME OVER !",True,"crimson") #change to picture
        text_rect = text_surface.get_rect(center=gamefield.center) #
        text_rect.centery = gamefield.top + gamefield.height / 3
        screen.blit(text_surface,text_rect)

    ######## Game Won #########
    if game_won:
        text_surface = font_large.render("GG WP EZ GET RECKT !",True,"forestgreen")
        text_rect = text_surface.get_rect(center=gamefield.center)
        text_rect.centery = gamefield.top + gamefield.height / 3
        screen.blit(text_surface,text_rect)        

   #############################################################################################

    pygame.display.flip() #Show Screen
    clock.tick(60) # Max FPS 60
    
pygame.quit()