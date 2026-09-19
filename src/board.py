import numpy as np
import random
import os
from PIL import Image

# --- Parameters ---
BOARD_SIZE = 30          # Board is BOARD_SIZE x BOARD_SIZE
NUM_MINES = 200          # Total number of mines

TILE_SIZE = 32           # Pixel size for one tile

# Direction vectors for neighboring tiles (8 directions)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

# Tile states
EMPTY = 0
MINE = -1
HIDDEN = -2
FLAGGED = -3

# Load all tile images
tile_images = {}
for i in range(9):
    tile_images[i] = Image.open(os.path.join("images", f"{i}.png")).resize((TILE_SIZE, TILE_SIZE))

tile_images['hidden'] = Image.open(os.path.join("images", "hidden.png")).resize((TILE_SIZE, TILE_SIZE))
tile_images['flag'] = Image.open(os.path.join("images", "flag.png")).resize((TILE_SIZE, TILE_SIZE))
tile_images['mine'] = Image.open(os.path.join("images", "mine.png")).resize((TILE_SIZE, TILE_SIZE))


class Board:
    def __init__(self):
        # Board state: values from 0-8 or MINE
        self.state_space = np.zeros((BOARD_SIZE, BOARD_SIZE))
        # Mask of revealed/flagged/hidden tiles
        self.revealed = np.full((BOARD_SIZE, BOARD_SIZE), HIDDEN)
        self.place_mines()
        self.add_numbers()

    def place_mines(self):
        """Randomly place mines on the board."""
        mines_placed = 0
        while mines_placed < NUM_MINES:
            x, y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
            if self.state_space[x][y] == EMPTY and (x+1)*(y+1) not in [1, 2, 3, 4, 5]:
                self.state_space[x][y] = MINE
                mines_placed += 1

    def add_numbers(self):
        """Calculate and set the number of adjacent mines for each non-mine tile."""
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.state_space[x][y] == MINE:
                    continue
                count = sum(
                    1 for dx, dy in DIRECTIONS
                    if 0 <= x+dx < BOARD_SIZE and 0 <= y+dy < BOARD_SIZE and self.state_space[x+dx][y+dy] == MINE
                )
                self.state_space[x][y] = count

    def render_board(self):
        """Create an image of the current board state."""
        board_image = Image.new('RGB', (TILE_SIZE * BOARD_SIZE, TILE_SIZE * BOARD_SIZE))

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.revealed[x][y] == FLAGGED:
                    img = tile_images['flag']
                elif self.revealed[x][y] == HIDDEN:
                    img = tile_images['hidden']
                elif self.state_space[x][y] == MINE:
                    img = tile_images['mine']
                else:
                    value = int(self.revealed[x][y])
                    img = tile_images.get(value, tile_images[0])
                board_image.paste(img, (y * TILE_SIZE, x * TILE_SIZE))

        return board_image

    def dig(self, x, y):
        """Reveal a tile."""
        if self.revealed[x][y] != HIDDEN:
            return
        self.revealed[x][y] = self.state_space[x][y]
        if self.revealed[x][y] == MINE:
            print(f"Exploded on tile ({x},{y})")

    def flag(self, x, y):
        """Flag a tile as suspected mine."""
        if self.revealed[x][y] == HIDDEN:
            self.revealed[x][y] = FLAGGED

    def is_solved(self):
        """Check if all non-mine tiles have been revealed."""
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.revealed[x][y] == HIDDEN and self.state_space[x][y] != MINE:
                    return False
        return True

    def is_exploded(self):
        """Check if any mine has been revealed."""
        return np.any(self.revealed == MINE)

    def get_tiles_info(self):
        """Collect information about revealed tiles and their hidden neighbors."""
        tiles = {}
        index = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.revealed[x][y] not in [HIDDEN, FLAGGED]:
                    hidden = []
                    flagged = 0
                    for dx, dy in DIRECTIONS:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                            if self.revealed[nx][ny] == HIDDEN:
                                hidden.append((nx, ny))
                            elif self.revealed[nx][ny] == FLAGGED:
                                flagged += 1
                    real_value = self.revealed[x][y] - flagged
                    tiles[index] = {
                        'real_value': real_value,
                        'hidden_neighbors': hidden
                    }
                    index += 1
        return tiles

    def apply_subset_digging_logic(self):
        """Apply basic and advanced subset logic to reveal or flag tiles."""
        progress = False
        tiles = self.get_tiles_info()

        for _ in range(10):  # Repeat multiple times for deeper logic
            for tile in tiles.values():
                if tile['real_value'] == 0:
                    for x, y in tile['hidden_neighbors']:
                        self.dig(x, y)
                        progress = True
                elif tile['real_value'] == len(tile['hidden_neighbors']):
                    for x, y in tile['hidden_neighbors']:
                        self.flag(x, y)
                        progress = True
            new_tiles = self.combinations(tiles)
            tiles.update(new_tiles)
        return progress

    def combinations(self, tiles):
        """Apply logical combinations between tile neighborhoods."""
        new_tiles = {}
        seen = set()
        index = 0
        for info1 in tiles.values():
            for info2 in tiles.values():
                hidden1 = set(info1['hidden_neighbors'])
                hidden2 = set(info2['hidden_neighbors'])
                if hidden2.issubset(hidden1) and hidden1 != hidden2:
                    new_hidden = hidden1 - hidden2
                    new_value = info1['real_value'] - info2['real_value']
                    key = (new_value, frozenset(new_hidden))
                    if key not in seen:
                        seen.add(key)
                        new_tiles[index] = {
                            'real_value': new_value,
                            'hidden_neighbors': new_hidden
                        }
                        index += 1
        return new_tiles

    def try_luck(self):
        """If no safe moves are known, guess the tile with lowest mine probability."""
        tiles_info = self.get_tiles_info()
        mine_probabilities = {}
        counts = {}

        for info in tiles_info.values():
            real_value = info['real_value']
            hidden_neighbors = info['hidden_neighbors']
            if hidden_neighbors:
                prob = real_value / len(hidden_neighbors)
                for x, y in hidden_neighbors:
                    mine_probabilities[(x, y)] = mine_probabilities.get((x, y), 0) + prob
                    counts[(x, y)] = counts.get((x, y), 0) + 1

        if mine_probabilities:
            averaged_probs = {k: mine_probabilities[k] / counts[k] for k in mine_probabilities}
            safest_tile = min(averaged_probs.items(), key=lambda x: x[1])[0]
            print(f"Guessed safest tile at {safest_tile}")
            self.dig(*safest_tile)
        else:
            hidden_tiles = [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if self.revealed[x][y] == HIDDEN]
            if hidden_tiles:
                x, y = random.choice(hidden_tiles)
                print(f"Random guess at ({x},{y})")
                self.dig(x, y)
            else:
                print("No moves left to guess.")
