import pygame
import random
import time

class Rain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rain_img
        self.rect = self.image.get_rect()
        self.speedx = 3  # Removed wind effect
        self.speedy = random.randint(25, 50)
        self.rect.x = random.randint(-100, wn_width)
        self.rect.y = random.randint(-wn_height, -5)

    def update(self):
        if self.rect.bottom > wn_height:
            self.speedx = 3  # Removed wind effect
            self.speedy = random.randint(25, 50)
            self.rect.x = random.randint(-wn_width, wn_width)
            self.rect.y = random.randint(-wn_height, -5)
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy

def draw_lightning():
    global lightning_active, lightning_duration
    if lightning_active:
        if lightning_duration > 0:
            lightning_flash = pygame.Surface((wn_width, wn_height))
            lightning_flash.fill((255, 255, 255))
            lightning_flash.set_alpha(random.randint(100, 200))
            wn.blit(lightning_flash, (0, 0))
            lightning_duration -= 1
        else:
            lightning_active = False
    elif random.randint(0, 100) < 2:  # 2% chance of lightning each frame
        lightning_active = True
        lightning_duration = random.randint(5, 10)  # Lightning lasts 5 to 10 frames


def play_random_thunder():
    global next_thunder_time
    if time.time() > next_thunder_time:
        thunder_sfx.play()
        next_thunder_time = time.time() + random.randint(6, 15)  # Schedule next thunder

def play_random_thunderAmbience():
    global next_thunderAmbience_time
    if time.time() > next_thunderAmbience_time:
        thunder_ambience.play()
        next_thunderAmbience_time = time.time() + random.randint(8, 20)  # Schedule next thunder

pygame.init()

# How fast the game screen updates
clock = pygame.time.Clock()

# Define bg color
GREY = (30, 30, 30)

# Images
rain_img = pygame.image.load('images/rain_img.png')
cloud_img = pygame.image.load('images/cloud_img.png')
cloud_img2 = pygame.image.load('images/cloud_img2.png')
cloud_img3 = pygame.image.load('images/cloud_img3.png')

# Audio
rain_sfx = pygame.mixer.Sound('audios/rain_sfx.wav')
rain_sfx.play()  # Constantly plays rain audio
thunder_sfx = pygame.mixer.Sound('audios/thunder_sfx.mp3')
next_thunder_time = time.time() + random.randint(1, 10)  # Schedule first thunder
thunder_ambience = pygame.mixer.Sound('audios/thunder_ambience.mp3')
next_thunderAmbience_time = time.time() + random.randint(5, 10)  # Schedule first thunder ambience sfx


# Window setup
wn_width = 700
wn_height = 500
wn = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('Stormy Night')

# Sprite group
rain_group = pygame.sprite.Group()

for i in range(120):
    rain = Rain()
    rain_group.add(rain)

# Cloud positions and speeds
cloud_pos = [-70, 200, 400]
cloud_speed = [random.randint(1, 2) for _ in range(3)]  # Random speed for each cloud

# Transparency variables
transparency = random.randint(20, 220)
transparency_direction = 1  # 1 for increasing, -1 for decreasing
transparency_step = 1  # How much to change the transparency each frame

# Lightning variables
lightning_active = False
lightning_duration = 0

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    rain_group.update()

    # Update cloud positions
    for i in range(3):
        cloud_pos[i] += cloud_speed[i]

        # Reset cloud positions and speeds if they move off the screen
        if cloud_pos[i] > wn_width:
            cloud_pos[i] = -cloud_img.get_width()
            cloud_speed[i] = random.randint(1, 2)  # Assign new random speed

    # Update transparency gradually
    transparency += transparency_direction * transparency_step
    if transparency >= 220:
        transparency = 220
        transparency_direction = -1  # Start decreasing
    elif transparency <= 20:
        transparency = 20
        transparency_direction = 1  # Start increasing

    # Drawing the sprites
    wn.fill(GREY)
    rain_group.draw(wn)
    draw_lightning()
    play_random_thunder()  # Check and play thunder if needed
    
    # Draw the cloud images at updated positions with the current transparency
    cloud_img.set_alpha(transparency)
    cloud_img2.set_alpha(transparency)
    cloud_img3.set_alpha(transparency)
    wn.blit(cloud_img, (cloud_pos[0], 0))
    wn.blit(cloud_img2, (cloud_pos[1], 120))
    wn.blit(cloud_img3, (cloud_pos[2], 80))
    
    pygame.display.flip()
    clock.tick(45)

# Quit
pygame.quit()
quit()