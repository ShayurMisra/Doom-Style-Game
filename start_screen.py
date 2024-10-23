import pygame as pg

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.SysFont(None, 48)

    def show_start_screen(self):
        self.game.screen.fill((0, 0, 0))

        # Game title
        title_text = self.font.render('Welcome to the Apocalypse', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2 - 100))
        self.game.screen.blit(title_text, title_rect)

        # Game description
        description_text = self.font.render('Use the WASD keys to move and mouse to look.', True, (255, 255, 255))
        description_rect = description_text.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2 - 50))
        self.game.screen.blit(description_text, description_rect)

        # Instructions
        instructions_text = self.font.render('Press Enter to Start', True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(self.game.screen.get_width() // 2, self.game.screen.get_height() // 2 + 100))
        self.game.screen.blit(instructions_text, instructions_rect)

        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                return True
        return False
