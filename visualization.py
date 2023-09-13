from PIL import Image, ImageDraw
import os
import re

# Configure the outputted image
img_size = (3072, 1024)
padding = (1074, 50)

# Colors specified in RGB
black_color = (0, 0, 0)
red_color = (255, 0, 0)
aqua_color = (51, 239, 242)


def get_grid_pos(x, y, padding, cells):
    assert x >= 0 and x < cells[0]
    assert y >= 0 and y < cells[1]

    grid_size = (img_size[0] - 2 * padding[0], img_size[1] - 2 * padding[1])
    cell_width = grid_size[0] / cells[0]
    cell_height = grid_size[1] / cells[1]

    left = padding[0] + cell_width * x
    top = padding[1] + cell_height * y
    right = padding[0] + cell_width * (x + 1)
    bottom = padding[1] + cell_height * (y + 1)

    return (left, top, right, bottom)

def draw_grid(draw, padding, cells, thickness):
    for x in range(cells[0]):
        for y in range(cells[1]):
            cell = get_grid_pos(x, y, padding, cells)
            left = cell[0] - (thickness / 2)
            top = cell[1] - (thickness / 2)
            right = cell[2] + (thickness / 2)
            bottom = cell[3] + (thickness / 2)

            draw.rectangle([left, top, right, bottom], outline=black_color, width=thickness)

def color_cell(draw, padding, cells, x, y, color):
    cell = get_grid_pos(x, y, padding, cells)
    draw.rectangle(cell, fill=color)

def draw_circle(draw, padding, cells, x, y, margin, color):
    cell = get_grid_pos(x, y, padding, cells)

    # 5% of cell size
    circle_padding = margin * (cell[2] - cell[0])

    left = cell[0] + circle_padding
    top = cell[1] + circle_padding
    right = cell[2] - circle_padding
    bottom = cell[3] - circle_padding

    draw.ellipse([left, top, right, bottom], fill=color)


def draw_path(draw, padding, cells, path_coords, color, thickness=10):
    for i in range(1, len(path_coords)):
        # Get the center of the start cell
        start_cell = get_grid_pos(path_coords[i-1][0], path_coords[i-1][1], padding, cells)
        start_center = ((start_cell[0] + start_cell[2]) / 2, (start_cell[1] + start_cell[3]) / 2)

        # Get the center of the end cell
        end_cell = get_grid_pos(path_coords[i][0], path_coords[i][1], padding, cells)
        end_center = ((end_cell[0] + end_cell[2]) / 2, (end_cell[1] + end_cell[3]) / 2)

        # Draw the line
        draw.line([start_center, end_center], fill=color, width=thickness)

def generate_image(cells, initial_pos, goal_pos, obstacles, response = "", output_filename="img-out/output_image.png"):
    img = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(img)

    draw_circle(draw, padding, cells, initial_pos[0], initial_pos[1], 0.05, red_color)
    color_cell(draw, padding, cells, goal_pos[0], goal_pos[1], aqua_color)

    for obstacle in obstacles:
        color_cell(draw, padding, cells, obstacle[0], obstacle[1], black_color)

        draw_path(draw, padding, cells, response, aqua_color)

    draw_grid(draw, padding, cells, 5)

    for coord in response:
        draw_circle(draw, padding, cells, coord[0], coord[1], 0.40, aqua_color)

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    img.save(output_filename)
