from ast import While

import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
def main():
    
    print("Starting Asteroids with pygame version 2.6.1 ")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #instantiate player
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    while True:
        
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        #fill screen black
        screen.fill("black")

        #draw player
        player.draw(screen)

        #flip display
        pygame.display.flip()

        dt = clock.tick(60) / 1000.0
        
          


if __name__ == "__main__":
    main()
