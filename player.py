import pygame
import time

SW = 600
SH = 400

UPGRADE_BG_COLOR = (100, 149, 237)
UPGRADE_TEXT_COLOR = (255, 255, 255)

class Player:
    def __init__(self):
        self.is_casting_line = False
        self.line_end_pos = (0, 0)
        self.line_start_pos = (0, 0)  # Updated line start position
        self.line_rect = pygame.Rect(0, 0, 0, 0)
        self.caught_fish = []
        self.score = 0
        self.upgrades = [
            {"name": "Double luck!", "price": 100, "applied": False, "display_time": 0},
            {"name": "Double score!", "price": 200, "applied": False, "display_time": 0},
            {"name": "More fish!", "price": 300, "applied": False, "display_time": 0}
        ]
        self.current_upgrade = 0
        self.line_color = (0, 0, 0)  # Color of the fishing line
        self.line_width = 2  # Width of the fishing line

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_casting_line = True
            self.line_start_pos = (pygame.mouse.get_pos()[0], 0)  # Update line start position to top of the screen
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_casting_line = False
            if not self.is_casting_line:
                line_movement = self.line_end_pos[1] - 0  # Calculate vertical line movement
                for fish in self.caught_fish:
                    fish.rect.move_ip(0, line_movement)  # Adjust fish position
                self.score += len(self.caught_fish)
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
                surface, self.line_color, self.line_start_pos, self.line_end_pos, self.line_width  # Updated line drawing parameters
            )

    def draw_score(self, surface):
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        surface.blit(text, (10, 10))

    def draw_upgrades(self, surface):
        upgrade_font = pygame.font.Font(None, 24)
        upgrade_margin = 10
        upgrade_width = (SW - 2 * upgrade_margin) // 3
        upgrade_height = 30

        total_width = len(self.upgrades) * (upgrade_width + upgrade_margin) - upgrade_margin
        start_x = (SW - total_width) // 2

        for i, upgrade in enumerate(self.upgrades):
            upgrade_rect = pygame.Rect(
                start_x + i * (upgrade_width + upgrade_margin),
                SH - upgrade_height - upgrade_margin,
                upgrade_width,
                upgrade_height,
            )
            pygame.draw.rect(surface, UPGRADE_BG_COLOR, upgrade_rect, border_radius=5)

            text = upgrade_font.render(
                f"{upgrade['name']} (${upgrade['price']})", True, UPGRADE_TEXT_COLOR
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
