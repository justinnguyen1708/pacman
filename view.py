from enemy_model import *


class View:
    def __init__(self):
        self.font = pygame.font.SysFont(GENERAL_FONT, GENERAL_FONT_SIZE)
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.background = pygame.image.load(MAP_BACKGROUND)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.load()

    def load(self):
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open(WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        self.font = pygame.font.SysFont(font_name, size)
        text = self.font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], GENERAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        pygame.display.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [60, 0], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT)
        self.draw_text('HIGH SCORE: {}'.format(self.high_score),
                       self.screen, [WIDTH // 2 + 60, 0], GENERAL_FONT_SIZE, WHITE, GENERAL_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], FINAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
        self.draw_text(AGAIN_TEXT, self.screen, [
            WIDTH // 2, HEIGHT // 2], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        self.draw_text(QUIT_TEXT, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        pygame.display.update()

    def game_defeated_draw(self):
        self.draw_text('YOU WIN', self.screen, [
            WIDTH // 2, HEIGHT // 2], FINAL_FONT_SIZE, RED, GENERAL_FONT, centered=True)
        self.draw_text(AGAIN_TEXT, self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        self.draw_text(QUIT_TEXT, self.screen, [
            WIDTH // 2, HEIGHT // 2 + 100], FINAL_FONT_SIZE, WHITE, GENERAL_FONT, centered=True)
        pygame.display.update()
