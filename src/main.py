from board import Board
import matplotlib.pyplot as plt

# --- Parameter ---
guess_enabled = True

# --- Initialize the game ---
board = Board()

# --- Set up Matplotlib figure ---
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
image = ax.imshow(board.render_board())
plt.axis('off')  # Hide axis lines and ticks

# --- Start the game ---
board.dig(0, 0)  # Start by opening (0,0); assumed to be safe

# --- Game Loop ---
while not board.is_solved() and not board.is_exploded():
    img = board.render_board()
    image.set_data(img)
    fig.canvas.draw()
    fig.canvas.flush_events()

    progress = board.apply_subset_digging_logic()

    if not progress and guess_enabled:
        board.try_luck()

# --- Game Over ---
img = board.render_board()
image.set_data(img)
fig.canvas.draw()
fig.canvas.flush_events()

plt.ioff()  # Turn off interactive mode
plt.show()