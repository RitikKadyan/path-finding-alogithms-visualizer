import pygame
import time


class Spot:
    def __init__(self, row, col, screen, square_size):
        self.row = row
        self.col = col
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.screen = screen
        self.square_size = square_size
        self.draw(self.black)

    def draw(self, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(self.col * self.square_size - self.square_size,
                                                         self.row * self.square_size - self.square_size,
                                                         self.square_size, self.square_size))
        pygame.draw.line(self.screen, self.white, (
            self.col * self.square_size - self.square_size, self.row * self.square_size - self.square_size),
                         (self.col * self.square_size - self.square_size, self.row * self.square_size))
        pygame.draw.line(self.screen, self.white, (
            self.col * self.square_size - self.square_size, self.row * self.square_size - self.square_size),
                         (self.col * self.square_size, self.row * self.square_size - self.square_size))


class Main:

    def __init__(self):
        self.width = 600
        self.height = 600
        self.square_size = 10  # Max is the width size
        self.rows = int(self.height / self.square_size)
        self.columns = int(self.width / self.square_size)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.gold = (255, 215, 0)
        self.spots = []
        self.target = None
        self.starting_spot = None
        self.backgroundColor = self.black
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.backgroundColor)
        self.game()
        self.draw_squares()

    def draw_squares(self):
        self.spots = []
        for row in range(1, self.rows + round(self.height // self.square_size)):
            for col in range(1, self.columns + round(self.width // self.square_size)):
                self.spots.append(Spot(row, col, self.screen, self.square_size))
        pygame.display.update()

    def draw_target(self, x, y):
        for s in self.spots:
            if s is not self.starting_spot:
                if x < s.col < x + 2:
                    if y < s.row < y + 2:
                        s.draw(self.red)
                        self.target = s
        pygame.display.update()

    def draw_starting_spot(self, x, y):
        for s in self.spots:
            if s is not self.target:
                if x < s.col < x + 2:
                    if y < s.row < y + 2:
                        s.draw(self.gold)
                        self.starting_spot = s
        pygame.display.update()

    def draw_to_target(self, col, row):
        for spot in self.spots:
            if col > 0:
                for col_loop in range(col):
                    if spot.col == self.starting_spot.col + col_loop + 1 and spot.row == self.starting_spot.row:
                        spot.draw(self.green)
            else:
                for col_loop in range(col-1, -1):
                    if spot.col == self.starting_spot.col + col_loop + 1 and spot.row == self.starting_spot.row:
                        spot.draw(self.green)
            if row > 0:
                for row_loop in range(row):
                    if spot.row == self.starting_spot.row + row_loop and spot.col == self.target.col:
                        spot.draw(self.green)
            else:
                for row_loop in range(row, -1):
                    if spot.row == self.starting_spot.row + row_loop + 1 and spot.col == self.target.col:
                        spot.draw(self.green)
        pygame.display.update()

    def game(self):
        running = True
        self.draw_squares()
        pygame.display.update()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    self.target = None
                    self.starting_spot = None
                    if event.y == -1 and self.square_size > 5:
                        self.square_size -= 1
                        self.draw_squares()
                    if event.y == 1 and self.square_size < 100:
                        self.square_size += 1
                        self.draw_squares()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.starting_spot is None:
                            self.draw_starting_spot(event.pos[0] // self.square_size, event.pos[1] // self.square_size)
                    elif event.button == 2:
                        if self.target is None:
                            self.draw_target(event.pos[0] // self.square_size, event.pos[1] // self.square_size)
                    elif event.button == 3:
                        self.draw_squares()
                        self.target = None
                        self.starting_spot = None
                        pygame.display.update()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.target is not None and self.starting_spot is not None:
                            x = calDistance(self.target, self.starting_spot)
                            self.draw_to_target(x[0], x[1])


def calDistance(spot1, spot2):
    spot1_x = spot1.col
    spot1_y = spot1.row
    spot2_x = spot2.col
    spot2_y = spot2.row

    x_distance = spot1_x - spot2_x
    y_distance = spot1_y - spot2_y

    return x_distance, y_distance


start_game = Main()
