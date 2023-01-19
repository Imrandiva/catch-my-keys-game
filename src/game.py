import json
import random
import time

import pygame
import threading
from network import Network



walls = []

wallLength = 16

class Player():
    height = width = 10

    def __init__(self, startx, starty, color):
        self.x = startx
        self.y = starty
        self.body = pygame.Rect(self.x, self.y, 20, 20)
        self.speed = 2
        self.color = color
        self.keys = 0 
        self.boostLevel = 1
        self.winner = False

    # Rita upp spelaren på planen
    def draw(self, g):
        self.body = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(g, self.color, self.body)

    # Rör spelaren i vald rikting. Blockera rörelse vid spelarkollision
    def move(self, dirn, object):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        0 = right
        1 = left
        2 = down
        3 = up
        """
        if pygame.Rect.colliderect(self.body, object):
            if dirn == 0:
                self.x -= 2 * self.speed
            elif dirn == 1:
                self.x += 2 * self.speed
            elif dirn == 2:
                self.y += 2 * self.speed
            else:
                self.y -= 2 * self.speed
        else:
            if dirn == 0:
                self.x += self.speed
            elif dirn == 1:
                self.x -= self.speed
            elif dirn == 2:
                self.y -= self.speed
            else:
                self.y += self.speed



class Game:
    def __init__(self, w, h):
        self.network = Network()
        self.width = w
        self.height = h
        self.player = Player(random.randint(0,920), random.randint(0,100), (0,0,255))
        self.player2 = Player(900,100, (255,0,0))
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.allKeys = []
        self.keyToRemove = []


    """
      Main funktionen för spelet
      """
    def run(self):
        # printKeys(self.player.keys)
        clock = pygame.time.Clock()

        # Ritar spelplanen
        field = """
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                                      W",
"W                                                      W",
"W      WWWWW                   W                       W",
"W          W                   WWWWWWWWWWWWWW          W",
"W          W                                W          W",
"W          WWWWWWWWWW                       W          W",
"W          W                                WWWWWW     W",
"W                                W                     W",
"W                                W                     W",
"W            WWWWWWWWWWWWWWW     WWWWWWWWWW            W",
"W            W                         W               W",
"W                                      W               W",
"W                                      W               W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
""".splitlines()[1:]
        x = y = 0
        for row in field:
            for col in row:
                if col == "W":
                    Wall((x, y))
                x += wallLength
            y += wallLength
            x = 0

        # Skapar och tar bort nycklar från spelplanen    
        self.createKey()
        self.removeKey()

        run = True
        collision_move = None

        while run:

            clock.tick(60)

            if self.winner():
                time.sleep(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    run = False

            # Kollar efter knapptryck för rörelse
            pressedKey = pygame.key.get_pressed()
            # Flytta spelaren i vald rikting
            if pressedKey[pygame.K_d]:
                if self.player.x <= self.width - self.player.speed:
                    self.player.move(0,self.player2.body)
                collision_move = 1
            if pressedKey[pygame.K_a]:
                if self.player.x >= self.player.speed:
                    self.player.move(1,self.player2.body)
                collision_move = 0
            if pressedKey[pygame.K_w]:
                if self.player.y >= self.player.speed:
                    self.player.move(2,self.player2.body)
                collision_move = 3
            if pressedKey[pygame.K_s]:
                if self.player.y <= self.height - self.player.speed:
                    self.player.move(3,self.player2.body)
                collision_move = 2


            # Kollar efter väggkollisioner och ser till att spelaren inte kan gå igenom väggen
            # Om sista nivå, resetta poäng till 0 vid kollision
            for wall in walls:
                if self.player.body.colliderect(wall.rect):
                    self.player.move(collision_move, self.player2.body)
                    if self.player.keys > 800:
                        self.player.keys = 0

                        
            # Om spelaren tar upp en nyckel
            for key in self.allKeys:
                if self.player.body.colliderect(key.rect):
                    self.keyToRemove.append(key)
                    self.player.keys += 50


            # Bonusnivåer där man kan ta ikapp poäng om man ligger under
            if 200 <= self.player.keys < 400 or 600 <= self.player.keys < 800:
                self.player.color = (255,255,0)
                if pygame.Rect.colliderect(self.player.body, self.player2.body) and self.player.keys > self.player2.keys:
                    self.player.keys -= int(self.player2.keys * 0.8)
            # Sista nivån
            elif self.player.keys >= 800:
                self.player.color = (255, 183, 197)
            else:
                self.player.color = (0,0,255)


            # Förhindra att spelaren går utanför spelplanen. Om så är fallet, flytta tillbaka spelare till spelplanen
            if self.player.x > self.width or self.player.x < 0 or self.player.y > self.height or self.player.y < 0:
                self.player.x = random.randint(0,920)
                self.player.y = random.randint(0, 100)

            # Bron mellan servern och spelardata för spelarna
            self.player2.x, self.player2.y, self.player2.keys, self.allKeys = self.get_data(self.send_data())
            self.draw_objects()


            self.canvas.update()

        pygame.quit()

    def draw_objects(self):

        self.canvas.draw_background()

        # Rita väggarna
        for wall in walls:
            pygame.draw.rect(self.canvas.get_canvas(), (255, 183, 197), wall.rect)

        self.canvas.draw_text("Points: " + str(self.player.keys), 12, 100, 100)
        if 200 <= self.player.keys < 400 or 600 <= self.player.keys < 800:
            self.canvas.draw_text("AVOID COLLIDING WITH ANOTHER PLAYER IF YOU THINK YOU HAVE MORE KEYS THAN THEM", 12,
                                  200, 200)
        if self.player.keys >= 800:
            self.canvas.draw_text("AVOID THE WALLS AT ANY COST", 12, 200, 200)

        for key in self.allKeys:
            pygame.draw.rect(self.canvas.get_canvas(), (255, 183, 197), key.rect)

        self.player.draw(self.canvas.get_canvas())
        self.player2.draw(self.canvas.get_canvas())


    """
   Skicka uppdaterad data till servern
    :return: Data i JSON format som ska skickas
    """
    def send_data(self):
        keyPos = []
        keysToRemove = []
        for key in self.allKeys:
            if key not in keyPos:
                keyPos.append((key.x_pos,key.y_pos))
        for key in self.keyToRemove:
            if key not in keysToRemove:
                keysToRemove.append((key.x_pos,key.y_pos))
        data = {
           "player-id": self.network.id,
           "player-x-pos": self.player.x,
           "player-y-pos": self.player.y,
           "player-keys": self.player.keys,
           "keys": keyPos,
           "keysToRemove": keysToRemove
        }
        return self.network.send_data(json.dumps(data))


    """
       # Hämta motståndarens data från servern
        :return: Hämtad data från servern
        """
    @staticmethod
    def get_data(data):
        try:
            # d = data.split(":")[1]
            pos = json.loads(data)

            keys = []
            pos["keys"] = [t for t in (set(tuple(i) for i in pos["keys"]))]
            for key in pos["keys"]:
                if key not in keys:
                    keys.append(Key(key[0],key[1]))
            return int(pos["player-x-pos"]),int(pos["player-y-pos"]),int(pos["player-keys"]),keys
            #return int(d[0]), int(d[1])
        except:
            return 0,0,[]

    # Skapa ny nyckel var tredje sekund
    def createKey(self):
        threading.Timer(3.0,self.createKey).start()
        x_val = random.randint(0,920)
        y_val = random.randint(0,100)
        self.allKeys.append(Key(x_val, y_val))

    # Ta bort en nyckel från spelplanen var 15e sekund
    def removeKey(self):
        threading.Timer(9.0, self.removeKey).start()
        if len(self.allKeys) > 0:
            self.allKeys.pop(-1)


    """
      Kolla om någon spelare har vunnit
      :return: true om någon har vunnit, annars false
      """
    def winner(self):

        if self.player.keys >= 1000 and pygame.Rect.colliderect(self.player.body, self.player2.body):
            self.player.winner = True
            self.canvas.draw_text("You won! Congrats!", 12, 500, 100)
            self.canvas.update()
            return True
        if self.player2.keys >= 1000 and pygame.Rect.colliderect(self.player.body, self.player2.body):
            self.canvas.draw_text("You lost! Better luck next time", 12, 500, 100)
            self.player.winner = False
            self.canvas.update()

            return True
        return False

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    # Uppdatera spelplanen
    @staticmethod
    def update():
        pygame.display.update()

    # Rita text på spelplaner
    def draw_text(self, text, size, x_pos, y_pos):
        pygame.font.init()
        font = pygame.font.SysFont("arial", size)
        render = font.render(text, False, (0,0,0))

        self.screen.blit(render, (x_pos,y_pos))

    # Hämta spelplan
    def get_canvas(self):
        return self.screen

    # Rita spelplanens bakgrund
    def draw_background(self):
        self.screen.fill((255,255,255))



# Klass för väggarna
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


# Klass för nyckelobjekten
class Key():
    def __init__(self, x_pos,y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(x_pos, y_pos, 8, 8)











