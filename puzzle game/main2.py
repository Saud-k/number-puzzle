import pygame
import random

# Constants
WINDOW_SIZE = 300
GRID_SIZE = 3
TILE_SIZE = WINDOW_SIZE // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sliding Puzzle")

# Create the initial grid
def create_grid():
    tiles = list(range(1, GRID_SIZE * GRID_SIZE)) + [0]  # 0 represents the empty space
    random.shuffle(tiles)
    return [tiles[i:i + GRID_SIZE] for i in range(0, len(tiles), GRID_SIZE)]

# Draw the grid
def draw_grid(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            if value != 0:
                pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 74)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

# Find the empty tile's position
def find_empty_tile(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return row, col
    return None

# Check if a move is valid
def is_valid_move(empty_row, empty_col, tile_row, tile_col):
    return (abs(empty_row - tile_row) == 1 and empty_col == tile_col) or \
           (abs(empty_col - tile_col) == 1 and empty_row == tile_row)

# Swap tiles
def swap_tiles(grid, empty_pos, tile_pos):
    empty_row, empty_col = empty_pos
    tile_row, tile_col = tile_pos
    grid[empty_row][empty_col], grid[tile_row][tile_col] = grid[tile_row][tile_col], grid[empty_row][empty_col]

# Main game loop
def main():
    grid = create_grid()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                empty_row, empty_col = find_empty_tile(grid)

                if is_valid_move(empty_row, empty_col, row, col):
                    swap_tiles(grid, (empty_row, empty_col), (row, col))

        screen.fill(BLACK)
        draw_grid(grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
