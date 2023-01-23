"""
This code made by Lola Urosevic and Elizabeth Rosen is a 2d platformer game with a story element. You play through 5 levels in pygame,
and how you perform in the various levels determines the outcome of the story. To play the game, you use left and right arrow keys,
the space bar, and the left mouse click. Special features include animated enemies, and restart and
next buttons to replay levels or move onto the next text screen.
"""
#Import the modules
import pygame
from pygame.locals import *
#This module allows for music to be played
from pygame import mixer

#Initialize music. When the code runs, this music will always begin playing. The values in the brackets are presets to allow for the best sound quality.
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#Initialize pygame
pygame.init()

#Use clock to have a constant fps no matter what computer runs the code
clock = pygame.time.Clock()
fps = 60

#Determine the dimensions of the game window
screen_width = 600
screen_height = 600
#Variables
#The width and height of one tile. The board is 600 by 600, so each tile being 30x30 meaans the tile grid is 20 x 20
tile_size = 30
#The game_over variable is used to determine if the player won or lost the level
game_over = 0
#When main_menu is true, the function is called and the starting image displays on screen
main_menu = True
how_to = True
story_one = True
story_two = True
story_three = True
story_four = True
story_five = True

#Using the screen variables, set up the screen/game window.
screen = pygame.display.set_mode((screen_width, screen_height))
#When the game is run, the title on the window displays the game title
pygame.display.set_caption("Oceans: A Better Place")

#Load photos before while loop so that they don't constantly need to be loaded in the game's while loop.
bg_img = pygame.image.load(r'''C:\Users\Lola\Desktop\background.jpg''')
startup_img = pygame.image.load(r'''C:\Users\Lola\Desktop\startup.png''')
restart_img = pygame.image.load(r'''C:\Users\Lola\Desktop\reset.png''')
next_img = pygame.image.load(r'''C:\Users\Lola\Desktop\next.png''')
story_img_one = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\storyone.png''')
story_img_two = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\storytwo.png''')
story_img_three = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\storythree.png''')
story_img_four = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\storyfour.png''')
story_img_five = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\storyfive.png''')
how_to_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\howto.png''')
a_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\a.png''')
b_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\b.png''')
ab_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\ab.png''')
aa_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\aa.png''')
bb_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\bb.png''')
ba_img = pygame.image.load(r'''C:\Users\Lola\Desktop\Game Level Images\ba.png''')



#Load sounds
pygame.mixer.music.load(r'''C:\Users\Lola\Desktop\centaur.mp3''')
#The 5000 value means it will fade into the game, instead of starting loud right away.
pygame.mixer.music.play(-1, 0.0, 5000)


class Button():
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (120, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #Get mouse position
        pos = pygame.mouse.get_pos()

        #Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #Draw button
        screen.blit(self.image, self.rect)
        return action

#Create a class for the player
class Player():
    def __init__(self, x, y):
        self.reset(x,y)


    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 1

        #Find where the player is moving by detecting key presses
        #When game over is 0, that means the player has not lost or won yet
        if game_over == 0:
            #Get key presses
            key = pygame.key.get_pressed()
            #If the space key is pressed, and the player hasn't already jumped nor are they in the air, then the character jumps.
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -14
                #Self.jumped is changed to true so that the player cannot double jump
                self.jumped = True
            #If the space button is not pressed, the player has not jumped
            if key[pygame.K_SPACE] == False:
                #Change the jumped value to false, allowing the player to jump again
                self.jumped = False
            #If the player presses the left key, the player moves to the left
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                #Set as negative so that if the player stops moving, the player faces left
                self.direction = -1
            #If the player presses the right key, the player moves to the right
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                #Set as positive so that if the player stops moving, the player faces right
                self.direction = 1
            #If the player stops pressing both arrows, they stop moving
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                #If they are facing right, use the right images
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                #If they are facing left, use the left images
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #Handle animation
            if self.counter > walk_cooldown:
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #Add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            #Check for collisions before the character moves, so that there is no delay in the collision occuring. If there is a collision, the player stops.
            self.in_air = True
            for tile in world_data.tile_list:
                #Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #Check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #Check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #Check for enemy collisions
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1

            #Check for water collisions
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1

            #Check for spike collisions
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1

            #Check for upside down spike collisions
            if pygame.sprite.spritecollide(self, upspike_group, False):
                game_over = -1
            
            #Check for exit collisions
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #Update coordinates
            self.rect.x += dx
            self.rect.y += dy

        #Draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        #Put together the images of when the player is facing right and left
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        #Load the image and scale it
        img_right = pygame.image.load(r'''C:\Users\Lola\Desktop\Ericsonr.png''')
        img_right = pygame.transform.scale(img_right, (24, 48))
        #Flip the image to have when the player turns left
        img_left = pygame.transform.flip(img_right, True, False)
        self.images_right.append(img_right)
        self.images_left.append(img_left)
        #Load images for when the player hits an enemy or dangerous block
        dead_image = pygame.image.load(r'''C:\Users\Lola\Desktop\ghost.png''')
        self.dead_image = pygame.transform.scale(dead_image, (24, 24))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World():
    def __init__(self, data):
        #Create a list to add the values of the tile list.
        self.tile_list = []

        #load images to be used in the level
        rock_img = pygame.image.load(r'''C:\Users\Lola\Desktop\rock.png''')

        row_count = 0
        #Go through every row of the level data
        for row in data:
            #Go through every column of the level data
            col_count = 0
            for tile in row:
                #If the tile value is 1, place a rock in that position
                if tile == 1:
                    #Transform the image to fit within the tile size
                    img = pygame.transform.scale(rock_img, (tile_size, tile_size))
                    #Make a rectangle to use for collisions and positioning
                    img_rect = img.get_rect()
                    #Set coordinates for the rock placement
                    img_rect.x = col_count*tile_size
                    img_rect.y = row_count*tile_size
                    #Make tiles using the image and it's rectangle to a list
                    tile = (img, img_rect)
                    #Add those tile values to the tile list
                    self.tile_list.append(tile)
                #If the tile value is 2, place a spike in that position
                if tile == 2:
                    spike = Spike(col_count * tile_size, row_count * tile_size)
                    spike_group.add(spike)
                #If the tile value is 3, place a blob in that position
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 10)
                    blob_group.add(blob)
                #If the tile value is 4, place the exit door in that position
                if tile == 4:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                #If the tile value is 7, place a water block in that position
                if tile == 5:
                    upspike = UpsideSpike(col_count * tile_size, row_count * tile_size)
                    upspike_group.add(upspike)
                if tile == 7:
                    water = Water(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    water_group.add(water)
                #Increase the column count to check 
                col_count += 1
            row_count += 1
    
    #Displays the images on the screen
    def draw(self):
        #For every tile, the images are loaded on screen
        for tile in self.tile_list:
            #Tile[0] is the image itself, tile[1] is the coordinates
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'''C:\Users\Lola\Desktop\blob.png''')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        water_img = pygame.image.load(r'''C:\Users\Lola\Desktop\water.png''')
        self.image = pygame.transform.scale(water_img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        door_img = pygame.image.load(r'''C:\Users\Lola\Desktop\door.png''')
        self.image = pygame.transform.scale(door_img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spk_img = pygame.image.load(r'''C:\Users\Lola\Desktop\spk.png''')
        self.image = pygame.transform.scale(spk_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

class UpsideSpike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spk_img = pygame.image.load(r'''C:\Users\Lola\Desktop\spk.png''')
        self.image = pygame.transform.scale(spk_img, (tile_size, tile_size))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


#Load level data points.
#The grid represents the 20 by 20 tiles. Every number represents a different object (See if tile statments for each number)
#This data is then used to display the levels.
world_one_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 4, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
[1, 1, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

world_two_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1, 1, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

world_three_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 2, 2, 1],
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
[1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1],
]

world_four_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
]

world_five_data =[
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 1],
[1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#Create instance of the player class
player = Player(60, screen_height - 78)

#Create instances of all sprite groups
blob_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
upspike_group = pygame.sprite.Group()

#Create instance of world class
world_data = World(world_one_data)

#Create button 
restart_button = Button(screen_width // 2 - 80, screen_height // 2 - 20, restart_img)
next_button = Button(460, 500, next_img)

#run is given a boolean value to run the game's while loop. 
# If the user closes the window, run is set to false, then the game ends.
run = True
#This is where the game runs.
while run:
    
    #The clock is called to keep frames per second constant
    clock.tick(fps)
    
    #Load the first image to start the game
    screen.blit(startup_img, (0,0))

    
    if main_menu == True:
        #Add each startup image first
        if next_button.draw():
            main_menu = False
            second_next_button = Button(300, 500, next_img)
    
    elif how_to == True:
        screen.blit(how_to_img, (0, 0))
        if second_next_button.draw():
            how_to = False
    
    elif story_one == True:
        screen.blit(story_img_one, (0, 0))
        if next_button.draw():
            story_one = False

    elif story_two == True:
        screen.blit(story_img_two, (0, 0))
        if second_next_button.draw():
            story_two = False

    elif story_three == True:
        screen.blit(story_img_three, (0, 0))
        if next_button.draw():
            story_three = False
    
    elif story_four == True:
        screen.blit(story_img_four, (0, 0))
        if second_next_button.draw():
            story_four = False

    elif story_five == True:
        screen.blit(story_img_five, (0, 0))
        if next_button.draw():
            story_five = False

    else:
        screen.blit(bg_img, (0,0))
        world_data.draw()
        if game_over == 0:
            blob_group.update()
        blob_group.draw(screen)
        water_group.draw(screen)
        spike_group.draw(screen)
        exit_group.draw(screen)
        upspike_group.draw(screen)
        game_over = player.update(game_over)

        #If player has died
        if game_over == -1:
            screen.blit(b_img, (0, 0))
            if next_button.draw():
                game_over = 0
                player.reset(60, screen_height - 78)
                blob_group = pygame.sprite.Group()
                water_group = pygame.sprite.Group()
                exit_group = pygame.sprite.Group()
                spike_group = pygame.sprite.Group()
                upspike_group = pygame.sprite.Group()
                world_data = World(world_two_data)
                world_data.draw()
                blob_group.draw(screen)
                water_group.draw(screen)
                spike_group.draw(screen)
                exit_group.draw(screen)
                upspike_group.draw(screen)
                game_over = player.update(game_over)
                

        #If player has completed level
        if game_over == 1:
            pass
                
    #Pygame looks for the event of the user clicking the exit button by going through all events
    for event in pygame.event.get():
        #If they did press the exit button , run is set to false and the game stops.
        if event.type == pygame.QUIT:
            run = False

    #Throughout the code, all the draw functions are updated using the update function. Pygame takes all previous draw functions and actually loads them in.
    pygame.display.update()

#Quit pygame to close out the code.
pygame.quit()