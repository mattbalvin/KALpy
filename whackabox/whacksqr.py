import pygame, random, sys, time
from pygame.locals import *

# set up pygame
pygame.init()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
TEXTAREAHEIGHT = 100
FPS = 40

BOXSIZE = (30, 30)

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

square_colors = [WHITE, RED, GREEN, BLUE, YELLOW]
square_time = [3000, 1000, 2000, 2500, 1500]
square_points = [5, 25, 15, 10, 20]

class SquareSprite:
    "keep track of square sprites"
    def __init__(self):
        self.x = random.randrange(0, WINDOWWIDTH - BOXSIZE[0], int(BOXSIZE[0] / 2) )
        self.y = random.randrange(0, WINDOWHEIGHT - TEXTAREAHEIGHT - BOXSIZE[1], int(BOXSIZE[1] / 2) )
        self.square_type = random.randrange(0, len(square_colors))
        self.color = square_colors[self.square_type]
        self.time_left = square_time[self.square_type]
        self.hit = 0

    def update(self, elapsed_time):
        self.time_left -= elapsed_time
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, BOXSIZE[0], BOXSIZE[1]))

    def undraw(self, surface, background_color):
        pygame.draw.rect(surface, background_color, (self.x, self.y, BOXSIZE[0], BOXSIZE[1]))

    def hit_test(self, pos):
        if ((pos[0] > self.x) and (pos[0] < self.x + BOXSIZE[0])):
            if ((pos[1] > self.y) and (pos[1] < self.y + BOXSIZE[1])):
                return 1
        return 0
        

def GetNextSquareTimer():
    return random.randrange(100, 1000, 20)

# set up the window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Whack-a-Square')

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# draw the window onto the screen
mainClock = pygame.time.Clock()
pygame.display.update()

random.seed(time.time())
sprite_list = []
timeleft = 120000
nextsquare = GetNextSquareTimer()
elapsed_time = 0
square_list = []
score = 0

# run the game loopSquareSprite
while True:
    timeleft -= elapsed_time
    if (timeleft <= 0):
        pygame.quit()
        sys.exit()
   
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # Did we hit anything?
            for s in sprite_list:
                if (s.hit_test(event.pos)):
                    s.hit = 1;
                    score += square_points[s.square_type]
            
    nextsquare -= elapsed_time
    if (nextsquare <= 0):
        newsquare = SquareSprite()
        sprite_list.append(newsquare)
        nextsquare = GetNextSquareTimer()

    for s in sprite_list:
        s.undraw(windowSurface, BACKGROUNDCOLOR)
        s.update(elapsed_time)
        if ((s.hit) or (s.time_left <= 0)):
            sprite_list.remove(s)
            del s
        else:
            s.draw(windowSurface)
    
    # Show Timer
    timerText = basicFont.render(str(int(timeleft / 1000)), True, WHITE, BACKGROUNDCOLOR)
    timerTextRect = timerText.get_rect()
    timerTextRect.centerx = windowSurface.get_rect().right - 100
    timerTextRect.centery = windowSurface.get_rect().bottom - timerTextRect.height

    # draw the Timer onto the surface
    windowSurface.blit(timerText, timerTextRect)

    # Show Score
    scoreText = basicFont.render(str(int(score)), True, WHITE, BACKGROUNDCOLOR)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.centerx = windowSurface.get_rect().left + scoreTextRect.height + 10
    scoreTextRect.centery = windowSurface.get_rect().bottom - scoreTextRect.height

    # draw the Timer onto the surface
    windowSurface.blit(scoreText, scoreTextRect)

    pygame.display.update()

    elapsed_time = mainClock.tick()



