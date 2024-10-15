import pygame
import random

# Constants
INITIAL_GRID_SIZE = 3
TILE_SIZE = 75  # Size of each tile

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

def calculate_window_size(grid_size):
    return grid_size * TILE_SIZE

# Set the initial window size
grid_size = INITIAL_GRID_SIZE
screen = pygame.display.set_mode((calculate_window_size(grid_size), calculate_window_size(grid_size)))
pygame.display.set_caption("Sliding Puzzle")
clock = pygame.time.Clock()  # Create a clock object

# Create the initial grid
def create_grid(grid_size):
    tiles = list(range(1, grid_size * grid_size)) + [0]  # 0 represents the empty space
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles, grid_size):
            return [tiles[i:i + grid_size] for i in range(0, len(tiles), grid_size)]

# Count inversions
def count_inversions(tiles):
    inversions = 0
    tiles = [tile for tile in tiles if tile != 0]  # Exclude the empty tile
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions

# Check if the puzzle is solvable
def is_solvable(tiles, grid_size):
    inversions = count_inversions(tiles)
    if grid_size % 2 == 1:  # Odd grid size
        return inversions % 2 == 0
    else:  # Even grid size
        empty_row = tiles.index(0) // grid_size
        return (inversions + empty_row) % 2 == 0

# Draw the grid
def draw_grid(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            value = grid[row][col]
            if value != 0:
                pygame.draw.rect(screen, WHITE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

# Find the empty tile's position
def find_empty_tile(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
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

# Check winning condition
def is_winning_condition(grid):
    flat_grid = [tile for row in grid for tile in row]
    return flat_grid == list(range(1, len(flat_grid))) + [0]

# Main game loop
def main():
    global grid_size, screen  # Declare grid_size and screen as global
    level = 1
    grid = create_grid(grid_size)
    
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

                    if is_winning_condition(grid):
                        level += 1
                        grid_size = INITIAL_GRID_SIZE * (2 ** (level - 1))  # Double the grid size
                        grid = create_grid(grid_size)
                        # Resize the window only when the grid size changes
                        screen = pygame.display.set_mode((calculate_window_size(grid_size), calculate_window_size(grid_size)))
                        print(f"Level {level}!")

        screen.fill(BLACK)
        draw_grid(grid)
        pygame.display.update()  # Update the entire display surface to the screen
        clock.tick(30)  # Limit the frame rate to 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
