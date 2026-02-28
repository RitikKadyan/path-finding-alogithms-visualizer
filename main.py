import pygame
import time
from algorithms.astar import AStar
from algorithms.dijkstra import Dijkstra
from algorithms.bfs import BFS
from algorithms.bidirectional import BidirectionalBFS
from core.heuristics import manhattan


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
        self.barrier = False

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
        pygame.init()  # Initialize pygame first
        self.width = 800
        self.height = 800
        self.square_size = 50
        self.rows = int(self.height / self.square_size)
        self.columns = int(self.width / self.square_size)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.gold = (255, 215, 0)
        self.gray = (220, 220, 220)
        self.spots = []
        self.target = None
        self.starting_spot = None
        self.backgroundColor = self.black
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.backgroundColor)
        self.font = pygame.font.SysFont('arial', 20)  # Font for help text
        self.keys_pressed = set()  # Track currently pressed keys
        self.draw_squares()
        self.game()

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
        # Recalculate grid dimensions based on current square size
        self.rows = int(self.height / self.square_size)
        self.columns = int(self.width / self.square_size)
        
        self.spots = []
        for row in range(1, self.rows + 1):
            for col in range(1, self.columns + 1):
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
        pygame.display.update()

    def draw_barrier(self, x, y):
        for s in self.spots:
            if s is not self.target and s is not self.starting_spot:
                if x < s.col < x + 2:
                    if y < s.row < y + 2:
                        s.draw(self.gray)
                        s.barrier = True
        pygame.display.update()

    def draw_path(self, path):
        for coord in path:
            row, col = coord
            for spot in self.spots:
                if spot.row == row and spot.col == col:
                    spot.draw(self.green)
        pygame.display.update()

    def draw_help_text(self):
        """Draw help text on the screen with background"""
        help_text = [
            "LEFT: Set Start | MID: Set Target | RIGHT: Clear Path | R: Reset",
            "A: A* | D: Dijkstra | F: BFS | I: Bidirectional | B: Draw Barrier | SCROLL: Zoom"
        ]
        # Draw semi-transparent background
        help_bg = pygame.Surface((self.width, 60))
        help_bg.set_alpha(200)
        help_bg.fill((40, 40, 40))
        self.screen.blit(help_bg, (0, self.height - 60))
        
        # Draw text in white
        y = self.height - 55
        for line in help_text:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (10, y))
            y += 25

    def clear_path(self):
        # Clear path only (green cells), keep start/target/barriers
        for spot in self.spots:
            # Only redraw if it's not start, target, or barrier
            if spot != self.starting_spot and spot != self.target and not spot.barrier:
                spot.draw(self.black)
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
                        # Right click: clear only the path, keep start/target/barriers
                        self.clear_path()
                elif event.type == pygame.KEYDOWN:
                    self.keys_pressed.add(event.key)
                    if event.key == pygame.K_r:
                        # Reset: clear only path and barriers, keep start/target
                        for spot in self.spots:
                            if spot != self.starting_spot and spot != self.target:
                                spot.barrier = False
                                spot.draw(self.black)
                        if self.starting_spot:
                            self.starting_spot.draw(self.gold)
                        if self.target:
                            self.target.draw(self.red)
                    if event.key == pygame.K_a:
                        if self.target is not None and self.starting_spot is not None:
                            self.run_algorithm(AStar(manhattan), "A*")
                    if event.key == pygame.K_d:
                        if self.target is not None and self.starting_spot is not None:
                            self.run_algorithm(Dijkstra(), "Dijkstra")
                    if event.key == pygame.K_f:
                        if self.target is not None and self.starting_spot is not None:
                            self.run_algorithm(BFS(), "BFS")
                    if event.key == pygame.K_i:
                        if self.target is not None and self.starting_spot is not None:
                            self.run_algorithm(BidirectionalBFS(), "Bidirectional BFS")
                elif event.type == pygame.KEYUP:
                    self.keys_pressed.discard(event.key)
            
            # Continuous barrier drawing when 'b' is held
            if pygame.K_b in self.keys_pressed:
                pos = pygame.mouse.get_pos()
                self.draw_barrier(pos[0] // self.square_size, pos[1] // self.square_size)
            
            # Draw help text (always on top)
            self.draw_help_text()
            pygame.display.flip()

    def run_algorithm(self, algorithm, name):
        # Convert spot coordinates (1-indexed) to grid coordinates (0-indexed)
        start = (self.starting_spot.row - 1, self.starting_spot.col - 1)
        goal = (self.target.row - 1, self.target.col - 1)
        
        # Build grid from current spots
        from core.grid import Grid
        grid = Grid(self.rows, self.columns, diagonal=False)
        for spot in self.spots:
            if spot.barrier:
                # Convert spot coordinates to grid coordinates
                grid.add_block((spot.row - 1, spot.col - 1))
        
        path, metrics = algorithm.search(grid, start, goal)
        
        # Clear previous path by redrawing all spots
        for spot in self.spots:
            if spot.barrier:
                spot.draw(self.gray)
            else:
                spot.draw(self.black)
        
        # Draw explored nodes in blue (excluding start and target)
        blue = (100, 149, 237)
        for coord in metrics.explored:
            row, col = coord
            spot_row, spot_col = row + 1, col + 1
            if (spot_row, spot_col) != (self.starting_spot.row, self.starting_spot.col) and (spot_row, spot_col) != (self.target.row, self.target.col):
                for spot in self.spots:
                    if spot.row == spot_row and spot.col == spot_col:
                        spot.draw(blue)
                        # Draw step number
                        step = metrics.explored_order.get(coord, "?")
                        self.draw_number_on_spot(spot, step)
        
        # Redraw start and target in original colors
        self.starting_spot.draw(self.gold)
        self.target.draw(self.red)
        
        if path:
            # Draw new path (excluding start and target)
            # Convert grid coordinates back to spot coordinates (add 1)
            for coord in path:
                row, col = coord
                spot_row, spot_col = row + 1, col + 1
                if (spot_row, spot_col) != (self.starting_spot.row, self.starting_spot.col) and (spot_row, spot_col) != (self.target.row, self.target.col):
                    for spot in self.spots:
                        if spot.row == spot_row and spot.col == spot_col:
                            spot.draw(self.green)
            print(f"{name}: nodes={metrics.nodes_expanded} path_len={metrics.path_length} time={metrics.runtime_ms:.2f}ms")
        else:
            print(f"{name}: No path found")

    def draw_number_on_spot(self, spot, step):
        """Draw step number on a spot"""
        x = spot.col * spot.square_size - spot.square_size // 2
        y = spot.row * spot.square_size - spot.square_size // 2
        text_surf = self.font.render(str(step), True, (255, 255, 0))
        self.screen.blit(text_surf, (x, y))



if __name__ == "__main__":
    start_game = Main()
