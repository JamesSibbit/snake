from pygame.locals import *
import pygame
import time
import random

class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)

       # initial positions, no collision.
       self.x[1] = 1*44
       self.x[2] = 2*44

    def update(self):
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0


    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i]))

class Food:
    x = 0
    y = 0
    step = 44

    def __init__(self,x,y):
        self.x = x*self.step
        self.y = y*self.step

    def draw(self,surface, image):
        surface.blit(image, (self.x, self.y))


class Collide:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if (x1==x2):
            if(y1==y2):
                return True
        return False


class Snake:

    windowWidth = 15*44
    windowHeight = 12*44
    player = 0
    surf = 0
    score = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.player = Player(3)
        self.food = Food(5,5)
        self.game = Collide()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self._running = True
        self.surf = pygame.Surface((25, 25))
        self.apple_surf = pygame.Surface((25, 25))
        self.score = 0

    def reset(self):
        self.player = Player(3)
        self.score = 0
        for i in range(0, self.player.length):
            self.player.x[i] = 0-i*44
            self.player.y[i] = 0

    def on_loop(self):
        self.player.update()

        #Check if collision with food occurs
        for i in range(0,self.player.length):
            if self.game.isCollision(self.food.x,self.food.y,self.player.x[i], self.player.y[i],44):
                self.food.x = random.randint(2,9) * 44
                self.food.y = random.randint(2,9) * 44
                self.player.length += 1
                self.score += 10


        #Check if snake collides with itself
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                self.end_game()

        for i in range(0,self.player.length):
            if self.player.x[i] > self.windowWidth:
                self.player.x[i] = 0
            elif self.player.x[i] < 0:
                self.player.x[i]  = self.windowWidth
            elif self.player.y[i] > self.windowHeight:
                self.player.y[i] = 0
            elif self.player.y[i] < 0:
                self.player.y[i] = self.windowHeight

        pass

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.surf.fill((255, 255, 255))
        self.apple_surf.fill((50,205,50))
        self.player.draw(self._display_surf, self.surf)
        self.food.draw(self._display_surf, self.apple_surf)
        smallFont = pygame.font.SysFont('comicsans', 30)
        text = smallFont.render('Score: ' + str(self.score), 1, (255,255,255))
        self._display_surf.blit(text, (10, 10))
        pygame.display.flip()


    def end_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN: # if the user hits the mouse button
                    run = False
                    self.reset()

            # This will draw text displaying the score to the screen.
            self._display_surf.blit(pygame.Surface((25, 25)), (0,0))
            largeFont = pygame.font.SysFont('comicsans', 80)
            mediumFont = pygame.font.SysFont('comicsans', 60) # creates a font object
            # lastScore = largeFont.render('Best Score: ' + str(self.updateFile()),1,(255,255,255))
            currentScore = largeFont.render('Score: '+ str(self.score),1,(255,10,10))
            play_again = mediumFont.render('Click to play again',1,(255,10,10))
            self._display_surf.blit(currentScore, (self.windowWidth/2 - currentScore.get_width()/2, self.windowHeight/2-30))
            self._display_surf.blit(play_again, (self.windowWidth/2 - play_again.get_width()/2, self.windowHeight/2+30))

            pygame.display.update()
        self.score = 0

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if ((keys[K_RIGHT] or keys[K_d])and self.player.direction != 1):
                self.player.moveRight()

            if ((keys[K_LEFT] or keys[K_a]) and self.player.direction != 0):
                self.player.moveLeft()

            if ((keys[K_UP] or keys[K_w]) and self.player.direction != 3):
                self.player.moveUp()

            if ((keys[K_DOWN] or keys[K_s]) and self.player.direction != 2):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

        pygame.quit()

app = Snake()

if __name__ == "__main__":
    app.on_execute()
