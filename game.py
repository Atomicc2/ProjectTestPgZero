import os
from pygame import Rect

## I decided to set this feature to make the game start in the center, but it doesn't change any of the functionalities. ##
os.environ['SDL_VIDEO_CENTERED'] = '1'

## CONSTANTS ##
TILE_SIZE = 64
ROWS = 11
COLS = 20
GAME_STATE = "MENU"
SOUND_ON = True
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS
TITLE = "Platform Adventure Kodland"
GRAVITY = 0.5
Y_SPEED_START = 0
X_SPEED_START = 0
JUMP_FORCE = -15
X_SPEED = 5
HERO_IDLE_SPEED = 0.1
HERO_WALK_SPEED = 0.1
BARNACLE_ATTACK_SPEED = 0.2
BEE_WALK_SPEED = 5
BEE_WALK_ANIMATION_SPEED = 0.1 
BEE_ANIMATION_SPEED = 0.1 
GOAL_ANIMATION_SPEED = 0.1
GOAL_POSITION = (2 * TILE_SIZE, 3 * TILE_SIZE)
HERO_START_POSITION = TILE_SIZE, HEIGHT - 64

## HERO AND GOAL ##
hero = Actor("hero_idle_1")
hero.pos = HERO_START_POSITION
hero.vy = Y_SPEED_START
hero.vx = X_SPEED_START
goal = Actor('goal_animation_0')
goal.left, goal.bottom = GOAL_POSITION
goal.frame = 0

## BUTTON CLASS ##
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.hovered = False
    def draw(self):
        color = (100, 200, 100) if self.hovered else (50, 150, 50)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, (255, 255, 255))
        screen.draw.text(self.text, midtop=(self.rect.centerx, self.rect.centery - 10),
                         color=(255, 255, 255), fontsize=18)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 60, "START GAME")
exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 60, "EXIT")
sound_button = Button(WIDTH//2 - 100, HEIGHT//2 + 140, 200, 60, "SOUND: ON")

## MENU FUNCTIONS ##
def draw_menu():
    screen.fill((20, 20, 40))
    screen.draw.text("GAME MENU", topleft=(WIDTH//2 - 150, 50), 
                     color=(255, 255, 255), fontsize=60)
    start_button.draw()
    exit_button.draw()
    sound_button.draw()

def on_mouse_pos(pos):
    start_button.hovered = start_button.rect.collidepoint(pos)
    exit_button.hovered = exit_button.rect.collidepoint(pos)
    sound_button.hovered = sound_button.rect.collidepoint(pos)

def on_mouse_down(pos):
    global GAME_STATE, SOUND_ON
    if GAME_STATE == "MENU":
        if start_button.is_clicked(pos):
            GAME_STATE = "PLAYING"
        elif exit_button.is_clicked(pos):
            exit()
        elif sound_button.is_clicked(pos):
            SOUND_ON = not SOUND_ON
            if not SOUND_ON:
                music.stop()
            else:
                music.play('music_theme')

## ENEMIES ##
enemies_list = []
def create_enemy(enemy_name, enemy_tile_left, enemy_tile_bottom, enemy_vx):
    enemy = Actor(f'{enemy_name}_0')
    enemy.bottom = enemy_tile_bottom * TILE_SIZE
    enemy.left = enemy_tile_left * TILE_SIZE
    enemy.frame = 0
    enemy.vx = enemy_vx
    enemy.startleft = enemy.left
    enemies_list.append(enemy)

create_enemy('barnacle_attack', 10, 8, 0)
create_enemy('barnacle_attack', 5, 10, 0)
create_enemy('bee_walkleft', 0, 5, BEE_WALK_SPEED)
create_enemy('bee_walkleft', 5, 5, BEE_WALK_SPEED)
create_enemy('bee_walkleft', 8, 5, BEE_WALK_SPEED)

## BUILD MAP ##
def build(filename, tile_size):
    with open(filename, "r") as f:
        contents = f.read().splitlines()
    contents = [c.split(",") for c in contents]
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            val = contents[row][col]
            if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
                contents[row][col] = int(val)
    items = []
    for row in range(len(contents)):
        for col in range(len(contents[0])):
            tile_num = contents[row][col]
            if tile_num != -1:
                item = Actor(f"tiles/tile_{tile_num:02d}")
                item.topleft = (tile_size * col, tile_size * row)
                items.append(item)
    return items

platforms = build("mapa_plataformas.csv", TILE_SIZE)

## COLLISION FUNCTIONS ##
def collision_platform_x():
    platform_left = False
    platform_right = False
    for tile in platforms:
        if hero.colliderect(tile):
            if hero.vx < 0:
                hero.left = tile.right
                platform_left = True
            elif hero.vx > 0:
                hero.right = tile.left 
                platform_right = True
    return platform_left, platform_right

def collision_platform_y():
    platform_under = False
    platform_over = False
    for tile in platforms:
        if hero.colliderect(tile):
            if hero.vy > 0:
                hero.bottom = tile.top
                hero.vy = 0
                platform_under = True
            elif hero.vy < 0:
                hero.top = tile.bottom 
                hero.vy = 0
                platform_over = True
    return platform_under, platform_over

## ANIMATION LISTS ##
def animation_images_list(actor, animation, list_size):
    images_list = []
    for i in range(list_size):
        images_list.append(f'{actor}_{animation}_{i}')
    return images_list

hero_idle_images = animation_images_list('hero', 'idle', 18)
hero_walk_right_images = animation_images_list('hero', 'walk_right', 2)
hero_walk_left_images = animation_images_list('hero', 'walk_left', 2)
barnacle_attack_images = animation_images_list('barnacle', 'attack', 4)
bee_walk_right_images = animation_images_list('bee', 'walkright', 2)
bee_walk_left_images = animation_images_list('bee', 'walkleft', 2)
goal_images = animation_images_list('goal', 'animation', 2)

## HERO IDLE ANIMATION ##
hero_idle_frame = 0
def animate_hero_idle():
    global hero_idle_frame
    if hero.vx == 0 and hero.vy == 0:
        hero_idle_frame = (hero_idle_frame + 1) % len(hero_idle_images)
        hero.image = hero_idle_images[hero_idle_frame]

clock.schedule_interval(animate_hero_idle, HERO_IDLE_SPEED)

## HERO WALK ANIMATION ##
hero_walk_frame = 0
def animate_hero_walk():
    global hero_walk_frame
    if hero.vy == 0 and hero.vx > 0:
        hero_walk_frame = (hero_walk_frame + 1) % len(hero_walk_right_images)
        hero.image = hero_walk_right_images[hero_walk_frame]
    elif hero.vy == 0 and hero.vx < 0:
        hero_walk_frame = (hero_walk_frame + 1) % len(hero_walk_left_images)
        hero.image = hero_walk_left_images[hero_walk_frame]

clock.schedule_interval(animate_hero_walk, HERO_WALK_SPEED)

## BARNACLE ATTACK ANIMATION ##
def animate_barnacle_attack():
    for enemy in enemies_list:
        enemy_filename = str(enemy.image)
        if enemy_filename.startswith('barnacle'):
            original_bottom = enemy.bottom
            enemy.frame = (enemy.frame + 1) % len(barnacle_attack_images)
            enemy.image = barnacle_attack_images[enemy.frame]
            enemy.bottom = original_bottom

clock.schedule_interval(animate_barnacle_attack, BARNACLE_ATTACK_SPEED)

## GOAL ANIMATION ##
def animate_goal():
    goal.frame = (goal.frame + 1) % len(goal_images)
    goal.image = goal_images[goal.frame]

clock.schedule_interval(animate_goal, GOAL_ANIMATION_SPEED)

## BEE ANIMATION ##
def animate_bee():
    for enemy in enemies_list:
        enemy_filename = str(enemy.image)
        if enemy_filename.startswith('bee'):
            enemy.frame = (enemy.frame + 1) % len(bee_walk_left_images)
            if enemy.vx > 0:
                enemy.image = bee_walk_left_images[enemy.frame]
            else:
                enemy.image = bee_walk_right_images[enemy.frame]

clock.schedule_interval(animate_bee, BEE_ANIMATION_SPEED)

## BEE MOVEMENT ##
def bee_walk():
    for enemy in enemies_list:
        enemy_filename = str(enemy.image)
        if enemy_filename.startswith('bee'):
            enemy.x = enemy.x - enemy.vx
            if enemy.left < 0 or enemy.right > WIDTH:
                enemy.vx = - enemy.vx

music.play("music_theme")

## DRAW GAME ##
def draw_game():
    screen.clear()
    screen.fill("skyblue")
    for platform in platforms:
        platform.draw()
    hero.draw()
    goal.draw()
    for enemy in enemies_list: 
        enemy.draw()

def draw():
    if GAME_STATE == "MENU":
        draw_menu()
    else:
        draw_game()

## UPDATE ##
def update():
    if keyboard.escape:
        exit()
    for enemy in enemies_list:
        if hero.colliderect(enemy):
            if SOUND_ON:
                sounds.sfx_disappear.play()
            hero.pos = HERO_START_POSITION
            hero.vy = Y_SPEED_START
            hero.vx = X_SPEED_START
            break
    bee_walk()
    hero.vy = hero.vy + GRAVITY
    hero.y = hero.y + hero.vy
    platform_under, platform_over = collision_platform_y()
    if keyboard.w:
        if platform_under:
            if SOUND_ON:
                sounds.sfx_jump.play()
            hero.vy = JUMP_FORCE
    hero.vx = 0
    if keyboard.a:
        hero.vx = -X_SPEED

    if keyboard.d:
        hero.vx = X_SPEED
    hero.x = hero.x + hero.vx
    platform_left, platform_right = collision_platform_x()

    if hero.left < 0:
        hero.left = 0
    if hero.right > WIDTH:
        hero.right = WIDTH
    if hero.colliderect(goal):
        if SOUND_ON:
            sounds.sfx_coin.play()
        hero.pos = HERO_START_POSITION
