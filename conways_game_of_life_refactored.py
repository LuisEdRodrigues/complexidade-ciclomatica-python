"""
Conway's Game of Life implemented in Python.
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
"""

from __future__ import annotations

from PIL import Image

# Define glider example
GLIDER = [
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# Define blinker example
BLINKER = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]


def get_live_neighbours(cells: list[list[int]], i: int, j: int) -> int:
    rows = len(cells)
    cols = len(cells[0])
    neighbour_count = 0
    
    # Iterar sobre os 8 vizinhos
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            # Ignorar a própria célula
            if row_offset == 0 and col_offset == 0:
                continue
            
            ni, nj = i + row_offset, j + col_offset
            
            # Verificar se o vizinho está dentro dos limites
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbour_count += cells[ni][nj]
                
    return neighbour_count


def new_generation_refactored(cells: list[list[int]]) -> list[list[int]]:

    rows = len(cells)
    cols = len(cells[0])
    next_generation = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            neighbour_count = get_live_neighbours(cells, i, j)
            alive = cells[i][j] == 1
            
            if alive and (neighbour_count == 2 or neighbour_count == 3):
                next_generation[i][j] = 1
            elif not alive and neighbour_count == 3:
                next_generation[i][j] = 1
            else:
                next_generation[i][j] = 0

    return next_generation


def generate_images(cells: list[list[int]], frames: int) -> list[Image.Image]:
    """
    Generates a list of images of subsequent Game of Life states.
    """
    images = []
    for _ in range(frames):
        # Create output image
        img = Image.new("RGB", (len(cells[0]), len(cells)))
        pixels = img.load()

        # Save cells to image
        for x in range(len(cells)):
            for y in range(len(cells[0])):
                colour = 255 - cells[y][x] * 255
                pixels[x, y] = (colour, colour, colour)

        # Save image
        images.append(img)
        cells = new_generation_refactored(cells)
    return images


if __name__ == "__main__":
    images = generate_images(GLIDER, 16)
    images[0].save("out_refactored.gif", save_all=True, append_images=images[1:])
