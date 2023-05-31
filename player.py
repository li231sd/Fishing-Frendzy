import pygame
import random
import time

SW = 600
SH = 400


class Player:
    def __init__(self):
        self.is_casting_line = False
        self.line_start_pos = (0, 0)
        self.line_end_pos = (0, 0)
        self.line_rect = pygame.Rect(0, 0, 0, 0)
        self.caught_fish = []
        self.score = 0
        self.upgrades = [
            {"name": "Double luck!", "price": 10, "applied": False, "display_time": 0},
            {"name": "Double score!", "price": 20, "applied": False, "display_time": 0},
            {"name": "More fish!", "price": 30, "applied": False, "display_time": 0}
        ]
        self.current_upgrade = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_casting_line = True
            self.line_start_pos = (pygame.mouse.get_pos()[0], 0)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_casting_line = False
            self.line_rect = pygame.Rect(
                self.line_start_pos[0],
                0,
                self.line_end_pos[0] - self.line_start_pos[0],
                SH,
            )
            if not self.is_casting_line:
                for fish in self.caught_fish:
                    fish.x += self.line_end_pos[0] - self.line_start_pos[0]
                    fish.rect.x = fish.x - 10
                    self.score += 1
                self.caught_fish.clear()
                self.check_upgrade_unlock()
                if self.current_upgrade == len(self.upgrades):
                    game_over = True  # Set the game_over variable to True when all upgrades have been applied
        elif event.type == pygame.MOUSEMOTION:
            if self.is_casting_line:
                self.line_end_pos = pygame.mouse.get_pos()

    def draw_line(self, surface):
        if self.is_casting_line:
            pygame.draw.line(
                surface, (0, 0, 0), self.line_start_pos, self.line_end_pos, 2
            )

    def draw_score(self, surface):
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        surface.blit(text, (10, 10))

    def draw_upgrades(self, surface):
        upgrade_font = pygame.font.Font(None, 24)
        upgrade_bg_color = (100, 149, 237)
        upgrade_text_color = (255, 255, 255)
        upgrade_margin = 10
        upgrade_width = (SW - 2 * upgrade_margin) // 3
        upgrade_height = 30

        for i, upgrade in enumerate(self.upgrades):
            upgrade_rect = pygame.Rect(
                upgrade_margin + i * (upgrade_width + upgrade_margin),
                SH - upgrade_height - upgrade_margin,
                upgrade_width,
                upgrade_height,
            )
            pygame.draw.rect(surface, upgrade_bg_color, upgrade_rect, border_radius=5)

            text = upgrade_font.render(
                f"{upgrade['name']} (${upgrade['price']})", True, upgrade_text_color
            )
            text_rect = text.get_rect(center=upgrade_rect.center)
            surface.blit(text, text_rect)

            if upgrade["applied"]:
                pygame.draw.rect(
                    surface, (255, 0, 0), upgrade_rect, width=2, border_radius=5
                )
                if upgrade["display_time"] > 0 and time.time() < upgrade["display_time"]:
                    text = upgrade_font.render(
                        f"{upgrade['name']} applied!", True, (0, 0, 0)
                    )
                    text_rect = text.get_rect(center=(SW // 2, SH // 2))
                    surface.blit(text, text_rect)
                else:
                    upgrade["applied"] = False
            else:
                pygame.draw.rect(
                    surface, (0, 0, 0), upgrade_rect, width=2, border_radius=5
                )

    def check_upgrade_unlock(self):
        if self.current_upgrade < len(self.upgrades):
            if self.score >= self.upgrades[self.current_upgrade]["price"]:
                self.apply_upgrade(self.upgrades[self.current_upgrade])
                self.current_upgrade += 1

    def apply_upgrade(self, upgrade):
        upgrade["applied"] = True
        upgrade["display_time"] = time.time() + 1  # Display upgrade text for 1 second
        self.score -= upgrade["price"]
