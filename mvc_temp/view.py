import pygame
from mvc_temp.settings import *


class View:
    def __init__(self):
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def draw_coins(self, coins, main_screen):
        for coin in coins:
            pygame.draw.circle(main_screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def start_draw(self, main_screen):
        main_screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', main_screen, [
            WIDTH // 2, HEIGHT // 2 - 50], GENERAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', main_screen, [
            WIDTH // 2, HEIGHT // 2 + 50], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)

    def draw_player(self, main_screen):
        pygame.draw.circle(main_screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                        int(self.pix_pos.y)), CELL_WIDTH // 2 - 2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(main_screen, PLAYER_COLOUR, (30 + 20 * x, HEIGHT - 15), 7)

    def playing_draw(self, main_screen, player, enemies, coins, main_background, high_score):
        main_screen.fill(BLACK)
        main_screen.blit(main_background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins(coins, main_screen)
        self.draw_text('CURRENT SCORE: {}'.format(player.current_score),
                       main_screen, [60, 0], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT)
        self.draw_text('HIGH SCORE: {}'.format(high_score),
                       [WIDTH // 2 + 60, 0], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT)
        player.draw(main_screen)
        for enemy in enemies:
            enemy.draw(main_screen)

    def game_over_draw(self, main_screen):
        main_screen.fill(BLACK)
        self.draw_text("GAME OVER", main_screen, [WIDTH // 2, 100], FINAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
        self.draw_text(AGAIN_TEXT, main_screen, [
            WIDTH // 2, HEIGHT // 2], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        self.draw_text(QUIT_TEXT, main_screen, [
            WIDTH // 2, HEIGHT // 1.5], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)

    def game_defeated_draw(self, main_screen):
        self.draw_text('YOU WIN', main_screen, [
            WIDTH // 2, HEIGHT // 2], FINAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
        self.draw_text(AGAIN_TEXT, main_screen, [
            WIDTH // 2, HEIGHT // 2 + 50], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        self.draw_text(QUIT_TEXT, main_screen, [
            WIDTH // 2, HEIGHT // 2 + 100], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
