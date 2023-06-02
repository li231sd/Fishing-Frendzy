import pygame
import random
import sys
from player import Player
from fish import Fish
from bomb import Bomb

pygame.init()

SW = 600
SH = 400

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Fishing Frenzy")

sea_background = pygame.image.load("assets/sea.jpeg")
sea_background = pygame.transform.scale(sea_background, (SW, SH))

player = Player()
fishes = []
bombs = []

game_over = False
restart_button_rect = pygame.Rect(SW // 2 - 50, SH // 2 + 50, 100, 50)

clock = pygame.time.Clock()
FPS = 300

def restart_game():
    global player, fishes, bombs, game_over
    player = Player()
    fishes = []
    bombs = []
    game_over = False

def game_loop():
    global game_over

    while not game_over:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            player.handle_event(event)

        screen.blit(sea_background, (0, 0))

        for fish in fishes:
            if (
                fish.rect.colliderect(player.line_rect)
                and player.is_casting_line
                and not fish.is_caught
            ):
                if player.line_rect.collidepoint(fish.rect.center):
                    catch_probability = random.random() 
                    threshold = 0.5 + int(player.upgrades[0]["applied"]) * 0.5  
                    if catch_probability < threshold:
                        fish.is_caught = True
                        fish.speed = 0.0
                        player.caught_fish.append(fish)

            elif fish.is_caught and not player.is_casting_line:
                fish.is_caught = False
                fish.speed = random.uniform(0.2, 1)

            fish.update(player.line_rect)
            fish.draw(screen)
            if fish.x > SW:
                fishes.remove(fish)

        for bomb in bombs:
            bomb.update()
            bomb.draw(screen)

            if (
                player.is_casting_line
                and bomb.rect.colliderect(player.line_rect)
                and bomb.x < player.line_start_pos[0]
            ):
                game_over = True
                break

            if bomb.x < 0:
                bombs.remove(bomb)

        if len(fishes) < 10 + int(player.upgrades[2]["applied"]) * 10 and random.random() < 0.02:
            fishes.append(Fish())

        if len(bombs) < 2 and random.random() < 0.0003:
            bombs.append(Bomb())

        player.line_rect = pygame.Rect(player.line_start_pos[0], 0, player.line_width, SH)  # Update line rectangle

        player.draw_line(screen)
        player.draw_score(screen)
        player.draw_upgrades(screen)
        pygame.display.flip()

    game_over_font = pygame.font.Font(None, 50)
    score_font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    restart_game()
                    game_loop()

        screen.blit(sea_background, (0, 0))
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        score_text = score_font.render(
            "Final Score: " + str(player.score), True, (0, 0, 0)
        )
        restart_text = score_font.render("Restart", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SW // 2, SH // 2 - 50))
        score_rect = score_text.get_rect(center=(SW // 2, SH // 2))
        restart_rect = restart_text.get_rect(center=(SW // 2, SH // 2 + 75))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        pygame.draw.rect(screen, (0, 0, 0), restart_button_rect, 2)

        pygame.display.flip()

start_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 24)
text_font = pygame.font.Font(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button_rect.collidepoint(event.pos):
                restart_game()
                game_loop()

    screen.blit(sea_background, (0, 0))
    start_text = start_font.render("Fishing Frenzy", True, (236, 248, 249))
    start_rect = start_text.get_rect(center=(SW // 2, SH // 2))
    text_surface = text_font.render("v.3.1.2 STABLE (BUGS MAY OCCUR)", True, (236, 248, 249))
    start_button_text = score_font.render("Start", True, (0, 0, 0))
    start_button_rect = start_button_text.get_rect(center=(SW // 2, SH // 2 + 75))

    screen.blit(start_text, start_rect)
    screen.blit(text_surface, (10, SH - 30))
    screen.blit(start_button_text, start_button_rect)
    pygame.draw.rect(screen, (0, 0, 0), restart_button_rect, 2)

    pygame.display.flip()
