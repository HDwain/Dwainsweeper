import pygame

#setup
pygame.init()
screenwith, screenheight = 1280,720
screen = pygame.display.set_mode((screenwith, screenheight))
clock = pygame.time.Clock()
gamefield = pygame.Rect(10, 10, 1000, 700)
singleTile = pygame.Rect(gamefield.left,gamefield.top,25,25)
countw = int(gamefield.width / singleTile.width)
counth = int(gamefield.height / singleTile.height)
grid = [["Black" for j in range(countw)] for i in range(counth)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    pygame.draw.rect(screen,"black",gamefield,width=2)
    singleTile.left = gamefield.left
    singleTile.top = gamefield.top

    for i in range(counth):
        for j in range(countw):
            pygame.draw.rect(screen,color=grid[i][j],rect=singleTile,width=1)
            singleTile.left += singleTile.width
            
        singleTile.left = gamefield.left
        singleTile.top += singleTile.height
   
   

    pygame.display.flip() #Show Screen
    clock.tick(60) # Max FPS 60
    
pygame.quit()

