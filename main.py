import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = updateable
    Shot.containers = (shots, updateable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    font = pygame.font.Font("DejaVuSans.ttf", 32)

    lives = 3
    score = 0
    dt = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        for obj in updateable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                lives -= 1
                if lives <= 0:
                    print("Game over!")
                    print(f"Score: {score}")
                    sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    score += 50
                    shot.kill()
                    asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        lives_text = font.render(f"{lives * "♥"}", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
