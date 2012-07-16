import pygame, random, sys, time
from pygame.locals import *

# set up pygame
pygame.init()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
TEXTAREAHEIGHT = 60
FPS = 40

BOXSIZE = (40, 40)

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
square_speed = [8.0, 4.0, 7.0, 7.0, 6.0]

class SquareSprite:
    "keep track of square sprites"
    def __init__(self):
        self.pos = [random.randrange(0, WINDOWWIDTH - BOXSIZE[0], int(BOXSIZE[0] / 2) ),
                    random.randrange(0, WINDOWHEIGHT - TEXTAREAHEIGHT - BOXSIZE[1], int(BOXSIZE[1] / 2) )]
        self.init_pos = [self.pos[0], self.pos[1]]
        self.square_type = random.randrange(0, len(square_colors))
        self.color = square_colors[self.square_type]
        self.time_left = square_time[self.square_type]
        self.initial_time_left = self.time_left
        self.vector = [random.random() - .5, random.random() - .5]
        self.speed = square_speed[self.square_type]
        self.hit = 0

    def update(self, elapsed_time):
        distance_factor = 1.0 - (self.time_left / self.initial_time_left)
        self.pos[0] = self.init_pos[0] + (self.vector[0] * self.speed * BOXSIZE[0] * distance_factor)
        self.pos[1] = self.init_pos[1] + (self.vector[1] * self.speed * BOXSIZE[1] * distance_factor) 
        self.time_left -= elapsed_time
        
    def draw(self, surface):
        color_intensity = self.time_left / self.initial_time_left
        draw_color = [self.color[0] * color_intensity, self.color[1] * color_intensity, self.color[2] * color_intensity]
        pygame.draw.rect(surface, draw_color, (self.pos[0], self.pos[1], BOXSIZE[0], BOXSIZE[1]))

    def undraw(self, surface, background_color):
        pygame.draw.rect(surface, background_color, (self.pos[0], self.pos[1], BOXSIZE[0], BOXSIZE[1]))

    def hit_test(self, pos):
        if ((pos[0] > self.pos[0]) and (pos[0] < self.pos[0] + BOXSIZE[0])):
            if ((pos[1] > self.pos[1]) and (pos[1] < self.pos[1] + BOXSIZE[1])):
                return 1
        return 0
        

def GetNextSquareTimer():
    return random.randrange(60, 700, 20)

# set up the window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Whack-a-Square')

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# set up sounds
hitSound = pygame.mixer.Sound('hit.wav')
shotSound = pygame.mixer.Sound('shot.wav')
pygame.mixer.music.load('background.mid')

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
pygame.mixer.music.set_volume(0.3) 
pygame.mixer.music.play(-1, 0.0)

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
            shotSound.play()
            for s in sprite_list:
                if (s.hit_test(event.pos)):
                    s.hit = 1;
                    hitSound.play()
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



