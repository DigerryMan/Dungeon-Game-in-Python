import pygame 

WIDTH = 500
HEIGHT = 500
 
background_colour = (234, 212, 252) 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
  
pygame.display.set_caption('test') 
   
screen.fill(background_colour) 
  
pygame.display.flip() 
  
running = True
   
while running: 
    for event in pygame.event.get():      
        if event.type == pygame.QUIT: 
            running = False