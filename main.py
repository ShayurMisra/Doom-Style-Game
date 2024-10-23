import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from start_screen import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.start_screen = StartScreen(self)
        self.running = False

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)
        self.running = True

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()
        self.draw_minimap()
        self.draw_crosshair()

    def draw_minimap(self):
        minimap_size = 10
        minimap_surface = pg.Surface((self.map.cols * minimap_size, self.map.rows * minimap_size))
        minimap_surface.set_alpha(100)
        
        for y, row in enumerate(self.map.mini_map):
            for x, tile in enumerate(row):
                if tile:
                    color = (255, 255, 255)
                    pg.draw.rect(minimap_surface, color, (x * minimap_size, y * minimap_size, minimap_size, minimap_size))
        
        player_x, player_y = self.player.map_pos
        player_marker_size = 5
        player_marker_color = (255, 255, 0)  
        pg.draw.circle(minimap_surface, player_marker_color, 
                    (player_x * minimap_size, player_y * minimap_size), 
                    player_marker_size)
        
        self.screen.blit(minimap_surface, (10, HEIGHT - self.map.rows * minimap_size - 10))

    def draw_crosshair(self):
        crosshair_color = (255, 255, 255)
        crosshair_size = 10
        crosshair_thickness = 4

        center_x, center_y = HALF_WIDTH, HALF_HEIGHT

        pg.draw.line(self.screen, crosshair_color, 
                     (center_x - crosshair_size, center_y), 
                     (center_x + crosshair_size, center_y), 
                     crosshair_thickness)

        pg.draw.line(self.screen, crosshair_color, 
                     (center_x, center_y - crosshair_size), 
                     (center_x, center_y + crosshair_size), 
                     crosshair_thickness)


    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while not self.running:
            self.start_screen.show_start_screen()
            if self.start_screen.check_events():
                self.new_game()

        while self.running:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()