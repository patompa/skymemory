#! /usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from chunklocator import ChunkLocator
import argparse

def draw_text_grid(img, grid_size, position_map, font_path, font_size, text_color="black"):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    img_width, img_height = img.size
    cell_width = img_width // grid_size[0]
    cell_height = img_height // grid_size[1]

    for row in range(grid_size[1]):
        for col in range(grid_size[0]):
            x = col * cell_width
            y = row * cell_height
            pos_key = f"{col+1}.{row+1}"
            if pos_key in position_map:
              text = position_map[pos_key]
            else:
               text = " "
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            text_x = x + (cell_width - text_width) // 2
            text_y = y + (cell_height - text_height) // 2
            draw.text((text_x, text_y), text, fill=text_color, font=font)

    return img




parser = argparse.ArgumentParser(
                    prog='chunk_visualization.py',
                    description='Visualize chunk positions')

strategies = ["rotation", "hop", "hop_rotation"]
parser.add_argument('-strategy','-s', choices=strategies,default="rotation")
parser.add_argument('-center_sat','-cs', type=int, default=4)
parser.add_argument('-center_orb','-co', type=int, default=3)
parser.add_argument('-servers','-ss', type=int, default=9)
parser.add_argument('-rotations','-r', type=int, default=0)
parser.add_argument('-output','-o', default="constellation.jpg")
parser.add_argument('-tot_sats','-ts', type=int, default=19)
parser.add_argument('-tot_orbs','-to', type=int, default=5)

args = parser.parse_args()


grid = ChunkLocator((args.center_sat,args.center_orb),strategy=args.strategy,servers=args.servers,tot_sats=args.tot_sats,tot_orbs=args.tot_orbs)
if args.rotations > 0:
  grid.rotate(args.rotations)

width = 100 * grid.tot_sats
height = 100 * grid.tot_orbs
background_color = (255, 255, 255)
image = Image.new('RGB', (width, height), background_color)
grid_size = (grid.tot_sats, grid.tot_orbs)
font_path = "Geneva.ttf"
font_size = 52

position_map = {}
for p in grid.positions:
  x = p["sat"]
  y = p["orb"]
  text = p["chunk"]
  position_map[f"{x}.{y}"] = f"{text}"

img_with_text = draw_text_grid(image, grid_size, position_map, font_path, font_size)
img_with_text.save(args.output)
