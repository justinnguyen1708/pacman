from enemy_model import *
from player_model import *

vec = pygame.math.Vector2


class Controller:
    def __init__(self):
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        self.high_score = open(HIGH_SCORE, "r").read()

    ############################ HELPER FUNCTIONS ##################################

    def load(self):
        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open(WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open(WALLS, 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        return PLAYING_STATE

    def update_high_score(self):
        f = open(HIGH_SCORE, "w")
        f.write(str(self.player.current_score))
        f.close()

    ########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
        return True

    def playing_update(self):
        if len(self.coins) == 0:
            return GAME_DEFEATED_STATE
        else:
            self.player.update()
            for enemy in self.enemies:
                enemy.update()

            for enemy in self.enemies:
                if enemy.grid_pos == self.player.grid_pos:
                    return PLAYING_STATE if self.remove_life() else GAME_OVER_STATE
        return PLAYING_STATE

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            return False
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0
        return True

    ########################### GAME OVER FUNCTIONS ################################

    def game_over_update(self):
        self.update_high_score()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return PLAYING_STATE
        return GAME_OVER_STATE

    ########################### GAME DEFEATED FUNCTIONS ################################

    def game_defeated_update(self):
        self.update_high_score()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return self.reset()  # PLAYING_STATE
        return GAME_DEFEATED_STATE
