import pygame as pg
from variables import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(Yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, Height/2)
        
        
        self.pos = vec(Width/2, Height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 0.1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 0.1
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, Gravity)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -Acceleration
        if keys[pg.K_RIGHT]:
            self.acc.x = Acceleration

        self.acc.x += self.vel.x*Friction
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc

        if self.pos.x > Width:
            self.pos.x = Width
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y