import sys

from controller import *
from view import *

pygame.init()


class EventManager:
    def __init__(self):
        self.running = True
        self.state = START_STATE
        self.clock = pygame.time.Clock()

    def run(self):
        view = View()
        controller = Controller()
        while self.running:
            if self.state == START_STATE:
                self.start_events()
                self.start_update()
                view.start_draw()
            elif self.state == PLAYING_STATE:
                self.running = controller.playing_events()
                self.state = controller.playing_update()
                view.playing_draw(controller.get_coins())
            elif self.state == GAME_OVER_STATE:
                self.running = controller.game_over_events()
                self.state = controller.game_over_update()
                view.game_over_draw()
            elif self.state == GAME_DEFEATED_STATE:
                self.running = controller.game_defeated_events()
                self.state = controller.game_defeated_update()
                view.game_defeated_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def start_update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = PLAYING_STATE

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.running = True

    def game_defeated_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.running = True
