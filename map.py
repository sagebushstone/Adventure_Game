# import pygame as pg
# import pytmx
# from settings import *

# def collide_hit_rect(one, two):
#     return one.hit_rect.colliderect(two.rect)

# class Map:
#     def __init__(self, filename):
#         self.data = []
#         with open(filename, 'rt') as f:
#             for line in f:
#                 self.data.append(line.strip())

#         self.tilewidth = len(self.data[0])
#         self.tileheight = len(self.data)
#         self.width = self.tilewidth * TILESIZE
#         self.height = self.tileheight * TILESIZE

# class TiledMap:
#     def __init__(self, filename):
#         tm = pytmx.load_pygame(filename, pixelalpha=True)
#         self.width = tm.width * tm.tilewidth
#         self.height = tm.height * tm.tileheight
#         self.tmxdata = tm

#     def render(self, surface):
#         ti = self.tmxdata.get_tile_image_by_gid
#         for layer in self.tmxdata.visible_layers:
#             if isinstance(layer, pytmx.TiledTileLayer):
#                 for x, y, gid, in layer:
#                     tile = ti(gid)
#                     if tile:
#                         surface.blit(tile, (x * self.tmxdata.tilewidth,
#                                             y * self.tmxdata.tileheight))

#     def make_map(self):
#         temp_surface = pg.Surface((self.width, self.height))
#         self.render(temp_surface)
#         return temp_surface

# class Camera:
#     def __init__(self, width, height):
#         self.camera = pg.Rect(0, 0, width, height)
#         self.width = width
#         self.height = height

#     def apply(self, entity):
#         return entity.rect.move(self.camera.topleft)

#     def apply_rect(self, rect):
#         return rect.move(self.camera.topleft)

#     def update(self, target):
#         x = -target.rect.centerx + int(WIDTH / 2)
#         y = -target.rect.centery + int(HEIGHT / 2)

#         # limit scrolling to map size
#         x = min(0, x)  # left
#         y = min(0, y)  # top
#         x = max(-(self.width - WIDTH), x)  # right
#         y = max(-(self.height - HEIGHT), y)  # bottom
#         self.camera = pg.Rect(x, y, self.width, self.height)

import pygame
import pytmx
from settings import *

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        # Keep a list of different kinds of files (grass, sand, water, etc.)
        self.tile_kinds = tile_kinds

        # Load the data from the file
        file = open(map_file, "r")
        data = file.read()
        file.close()

        # Set up the tiles from loaded data
        self.tiles = []
        for line in data.split('\n'):
            row = []
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)

        # How big in pixels are the tiles?
        self.tile_size = tile_size

    def draw(self, screen):
        # Go row by row
        for y, row in enumerate(self.tiles):
            # Within the current row, go through each tile
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface