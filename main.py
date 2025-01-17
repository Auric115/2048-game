import pygame
import random
import sys

FPS = 60
GRID = 4

# Sizes
    # Medium
WIDTH, HEIGHT = 600, 800
MENU_SIZE = 100
GAP = 5
GRID_SIZE = 120
"""
    #Smaller
WIDTH, HEIGHT = 450, 600
MENU_SIZE = 75
GAP = 4
GRID_SIZE = 80
"""

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (117,100,82)
BG_COLOR = (250, 247, 239)
GRID_COLOR = (189, 172, 151)
CELL_COLOR_DICT = {
    2: (238, 228, 218),
    4: (235, 216, 182),
    8: (242, 177, 119),
    16: (245, 144, 91),
    32: (245, 117, 86),
    64: (245, 90, 54),
    128: (242, 207, 86),
    256: (244, 204, 71),
    512: (246, 200, 56),
    1024: (249, 197, 42),
    2048: (255, 187, 0),
    4096: (61,58,50),
    8192: (61,58,50),
    16384: (61,58,50),
    32768: (61,58,50),
    65536: (61,58,50),
    131072: (61,58,50),
}

class Cell:
    def __init__(self, val):
        self.value = val
        self.merged = False
    
    def merge(self, cell):
        if not self.merged and not cell.merged:
            if self.value == cell.value:
                self.value *= 2
                self.merged = True
                cell.reset()
                return self.value
        if self.value == 0:
            self.value = cell.value
            cell.reset()
            return 0
        
        return -1
    
    def reset(self):
        self.value = 0
        self.merged = False

    def new_round(self):
        self.merged = False

class Game:    
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048 Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)

        self.score = 0
        self.high_score = 0

        self.cells = [[(Cell(0)) for _ in range(GRID)] for _ in range(GRID)]

        self.gen_new_cell()
        self.gen_new_cell()
        self.run()

    def draw_text(self, text, x, y, size = 60, color=TEXT_COLOR, center=False):
        self.font = pygame.font.Font(None, size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_menu(self):
        side_length = GRID * (GRID_SIZE + GAP) + GAP
        x_offset = (WIDTH - (side_length)) // 2 + GAP
        y_offset = 3 * MENU_SIZE // 2

        self.draw_text("2048", WIDTH // 2, 2 * MENU_SIZE // 3, size=108, center=True)

        score_rect = pygame.Rect(x_offset - GAP, y_offset - GAP, side_length // 2 - GAP, 3 * MENU_SIZE // GAP)
        self.draw_text("score", score_rect.centerx, y_offset - 18, size=36, center=True)
        pygame.draw.rect(self.screen, GRID_COLOR, score_rect, border_radius=5)
        self.draw_text(f"{self.score}", score_rect.centerx, score_rect.centery, size=42, center=True)

        high_score_rect = pygame.Rect(x_offset + side_length // 2, y_offset - GAP, side_length // 2 - GAP, 3 * MENU_SIZE // GAP)
        self.draw_text("high score", high_score_rect.centerx, y_offset - 18, size=36, center=True)
        pygame.draw.rect(self.screen, GRID_COLOR, high_score_rect, border_radius=5)
        self.draw_text(f"{self.high_score}", high_score_rect.centerx, high_score_rect.centery, size=42, center=True)

    def draw_grid(self):
        side_length = GRID * (GRID_SIZE + GAP) + GAP
        x_offset = (WIDTH - (side_length)) // 2 + GAP
        y_offset = (HEIGHT - (side_length)) // 2 + MENU_SIZE + GAP

        grid_rect = pygame.Rect(x_offset - GAP, y_offset - GAP, side_length, side_length)
        pygame.draw.rect(self.screen, TEXT_COLOR, grid_rect, border_radius=5)

        for x in range(GRID):
            for y in range(GRID):
                cell_rect = pygame.Rect(x_offset + x * (GRID_SIZE + GAP), y_offset + y * (GRID_SIZE + GAP), GRID_SIZE, GRID_SIZE)
                if self.cells[x][y].value == 0:
                    pygame.draw.rect(self.screen, GRID_COLOR, cell_rect, border_radius=20)
                else:    
                    pygame.draw.rect(self.screen, CELL_COLOR_DICT[self.cells[x][y].value], cell_rect, border_radius=20)
                    self.draw_text(f"{self.cells[x][y].value}", cell_rect.centerx, cell_rect.centery, center=True)              

    def gen_new_cell(self):
        empty_spots = [(x, y) for x in range(GRID) for y in range(GRID) if self.cells[x][y].value == 0]

        if empty_spots:
            x, y = random.choice(empty_spots)

            self.cells[x][y].value = 2
        else:
            return -1

    def move(self, dir_x, dir_y):
        out = 0

        for row in self.cells:
            for cell in row:
                cell.new_round()

        if dir_x == 1:
            x_range = (GRID - 1, -1, -1)
        else:
            x_range = (0, GRID)

        if dir_y == 1:
            y_range = (GRID - 1, -1, -1)
        else:
            y_range = (0, GRID)

        for _ in range(GRID):
            for x in range(*x_range):
                for y in range(*y_range):
                    nx, ny = x + dir_x, y + dir_y
                    if 0 <= nx < GRID and 0 <= ny < GRID:
                        source_cell = self.cells[x][y]
                        target_cell = self.cells[nx][ny]

                        # Attempt to merge or move the source cell into the target cell
                        res = target_cell.merge(source_cell)
                        if res > 0:
                            self.score += res
                        
                        if res > -1:
                            out = 1
                        

        return out

    def game_over(self):
        for x in range(GRID):
            for y in range(GRID):
                val = self.cells[x][y].value
                if val == 0:
                    return False
                
                if x + 1 < GRID and val == self.cells[x+1][y].value:
                    return False
                if y + 1 < GRID and val == self.cells[x][y+1].value:
                    return False

        return True

    def reset(self):
        self.score = 0

        self.cells = [[(Cell(0)) for _ in range(GRID)] for _ in range(GRID)]

        self.gen_new_cell()
        self.gen_new_cell()

    def run(self):
        running = True
        paused = False

        while running:
            dirs = None
            self.screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        dirs = (0, -1)
                    elif event.key == pygame.K_DOWN:
                        dirs = (0, 1)
                    elif event.key == pygame.K_LEFT:
                        dirs = (-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        dirs = (1, 0)
                    elif event.key == pygame.K_SPACE:
                        if paused:
                            self.reset()
                            paused = False
                            continue

                    if dirs:
                        if self.move(*dirs):
                            self.gen_new_cell()
            
            if self.game_over():
                paused = True

            if self.score > self.high_score:
                self.high_score = self.score

            self.draw_menu()
            self.draw_grid()

            if paused:
                self.draw_text("Game Over! (SPACE to play again)", WIDTH // 2, (HEIGHT - (GRID * GRID_SIZE + (GRID + 1) * GAP)) // 2 + MENU_SIZE - 4 * GAP, size=36, center=True)       

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    game = Game()


if __name__=='__main__':
    main()