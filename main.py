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
        self.neighbors = []

    # Draws the spot and fills with color from color param. The default color is black.
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

        pygame.display.update()


class Main:

    def __init__(self):
        self.width = 200
        self.height = 200
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

    def assign_neighbors(self):
        for spot in self.spots:
            for spot2 in self.spots:
                if spot2.col == spot.col or spot2.col == spot.col + 1 or spot2.col == spot.col - 1:
                    if spot2.row == spot.row + 1 or spot2.row == spot.row - 1:
                        spot.neighbors.append(spot2)
                if spot2.row == spot.row:
                    if spot2.col == spot.col + 1 or spot2.col == spot.col - 1:
                        spot.neighbors.append(spot2)

    def draw_squares(self):
        self.spots = []
        for row in range(1, self.rows + round(self.height // self.square_size)):
            for col in range(1, self.columns + round(self.width // self.square_size)):
                self.spots.append(Spot(row, col, self.screen, self.square_size))
        self.assign_neighbors()
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
                        # self.draw_neighbors(s)
        pygame.display.update()

    def draw_to_target(self, col, row):
        for spot in self.spots:
            if col > 0:
                for col_loop in range(col):
                    if spot.col == self.starting_spot.col + col_loop + 1 and spot.row == self.starting_spot.row:
                        spot.draw(self.green)
            else:
                for col_loop in range(col - 1, -1):
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

    @staticmethod
    def draw_neighbors(spot):
        for neighbor in spot.neighbors:
            neighbor.draw(neighbor.red)
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
                            self.draw_squares()
                            self.target.draw(self.red)
                            self.starting_spot.draw(self.gold)
                            x = calDistance(self.target, self.starting_spot)
                            self.draw_to_target(x[0], x[1])
                    if event.key == pygame.K_a:
                        a_star(self.starting_spot, self.target)


# Find the best spot closest to target spot
def consider_spot(spot_to_consider, target):
    best_spot = None
    best_spot_f_cost = None

    # Goes through all the spot(spot_to_consider)'s neighbors
    for neighbor in spot_to_consider.neighbors:
        if neighbor == target:  # If the neighbor spot is the target spot return target to end while loop and print target reached
            print("Target reached!")
            return target

        curr_h_cost = abs(neighbor.row - target.row) + abs(neighbor.col - target.col)
        curr_g_cost = None
        if neighbor.col == spot_to_consider.col:
            if neighbor.row == spot_to_consider.row + 1 or neighbor.row == spot_to_consider.row - 1:
                curr_g_cost = 1
        elif neighbor.row == spot_to_consider.row:
            if neighbor.col == spot_to_consider.col + 1 or neighbor.col == spot_to_consider.col - 1:
                curr_g_cost = 1
        else:
            curr_g_cost = 1
        curr_f_cost = curr_h_cost + curr_g_cost
        if best_spot_f_cost is None:
            best_spot_f_cost = curr_f_cost
            best_spot = neighbor
        elif curr_f_cost < best_spot_f_cost:
            best_spot_f_cost = curr_f_cost
            best_spot = neighbor

    best_spot.draw(best_spot.white)
    return best_spot


# Runs the A* path finding algorithm
def a_star(start, end):
    spot = consider_spot(start, end)
    while spot != end:
        time.sleep(0.25)
        spot = consider_spot(spot, end)


def calDistance(spot1, spot2):
    spot1_x = spot1.col
    spot1_y = spot1.row
    spot2_x = spot2.col
    spot2_y = spot2.row

    x_distance = spot1_x - spot2_x
    y_distance = spot1_y - spot2_y

    return x_distance, y_distance


if __name__ == "__main__":
    start_game = Main()
