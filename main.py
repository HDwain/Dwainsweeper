import pygame

#setup
pygame.init()
screenwith, screenheight = 1280,720
screen = pygame.display.set_mode((screenwith, screenheight))
clock = pygame.time.Clock()
dt = 0

#r = pygame.Rect(10, 10, 50, 50)
minefield = pygame.Rect(10, 10, 1000, 700)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    pygame.draw.rect(screen,"black",minefield,width=5)
#    countwidth = int((screenwith-r.left)/(r.width+5))
#    for i in range(countwidth):
#        x = r.left + (i*(r.width+5))
#        pygame.draw.rect(screen, "red", (x,r.top,r.width,r.height))
   
   

    pygame.display.flip() #Show Screen
    #clock.tick(60) # Max FPS 60
    dt = clock.tick(60) / 1000

pygame.quit()

