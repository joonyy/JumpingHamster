import pygame as pg
import random
from variables import *
from sprite import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(Font_name)

    def load_data(self):
        # Load high score
        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, HS), 'r') as f:
                self.highscore = int(f.read())
        except FileNotFoundError:
            self.highscore = 0

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platfrom
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 0.1
                self.player.vel.y = 0
                
        # If player reached top 1/4 of screen
        if self.player.rect.top <= Height/4 :
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= Height:
                    plat.kill()
                    self.score += 10
     #Die
        if self.player.rect.bottom > Height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Spawn new platforms
        while len(self.platforms) < 6:
            width = random.randrange(70, 110)
            p = Platform(random.randrange(0, Width - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game Loop - Events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22,White, Width/2, 15)
        # *after* drawing everything, flip the display\
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass
  
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                    
    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, White, Width/2, Height/4)
        self.draw_text("Arrows to move, Space to jump",
                       22, White, Width/2, Height/2)
        self.draw_text("Press a key to play",
                       22, White, Width/2, Height*3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, White, Width/2, Height/4)
        self.draw_text("Score : " + str(self.score),
                       22, White, Width/2, Height/2)
        self.draw_text("Press a key to play again",
                       22, White, Width/2, Height*3/4)
        pg.display.flip()
        self.wait_for_key()


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()