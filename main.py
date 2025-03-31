import pygame
import math
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_x = 6.0
player_y = 8.0
playerAngle = math.pi / 2

font = pygame.font.Font(None, 24)

def is_wall(x, y):
    grid_x = int(x)
    grid_y = int(y)
    if 0 > grid_x >= MAP_WIDTH or 0 > grid_y >= MAP_HEIGHT:
        return True
    cell = GAME_MAP[grid_y][grid_x]
    return cell == '#'

def handle_user_input(elapsed_time):
    global player_x, player_y, playerAngle
    keys = pygame.key.get_pressed()
    speed = 3.0 * elapsed_time
    dx, dy = 0, 0
    
    if keys[pygame.K_w]:
        dx += math.sin(playerAngle)
        dy += math.cos(playerAngle)
    if keys[pygame.K_s]:
        dx -= math.sin(playerAngle)
        dy -= math.cos(playerAngle)
    if keys[pygame.K_a]:
        dx -= math.cos(playerAngle)
        dy += math.sin(playerAngle)
    if keys[pygame.K_d]:
        dx += math.cos(playerAngle)
        dy -= math.sin(playerAngle)
    
    magnitude = math.sqrt(dx * dx + dy * dy)
    if magnitude > 0:
        dx /= magnitude
        dy /= magnitude

    newX = player_x + dx * speed
    newY = player_y + dy * speed

    if not is_wall(newX, newY):
        player_x = newX
        player_y = newY
    
    if keys[pygame.K_LEFT]:
        playerAngle -= elapsed_time
    if keys[pygame.K_RIGHT]:
        playerAngle += elapsed_time

def perform_raycasting():
    for x in range(SCREEN_WIDTH):
        rayAngle = playerAngle - FOV / 2.0 + (x / SCREEN_WIDTH) * FOV
        distToWall = 0
        hitWall = False

        focalX = math.sin(rayAngle)
        focalY = math.cos(rayAngle)

        while not hitWall and distToWall < DEPTH:
            distToWall += 0.1
            testX = int(player_x + focalX * distToWall)
            testY = int(player_y + focalY * distToWall)

            if testX < 0 or testX >= MAP_WIDTH or testY < 0 or testY >= MAP_HEIGHT:
                hitWall = True
                distToWall = DEPTH
            else:
                if GAME_MAP[testY][testX] == "#":
                    hitWall = True

        ceiling = int(SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / distToWall)
        floor = SCREEN_HEIGHT - ceiling
        xScreen = x * (SCREEN_WIDTH / SCREEN_WIDTH)

        pygame.draw.line(screen, (0, 0, 65), (xScreen, 0), (xScreen, ceiling))
        shade = int(255 - (distToWall / DEPTH) * 255)
        blue_shade = max(0, min(shade + 15, 255))
        pygame.draw.line(screen, (shade, shade, blue_shade), (xScreen, ceiling), (xScreen, floor))
        pygame.draw.line(screen, (0, 0, 35), (xScreen, floor), (xScreen, SCREEN_HEIGHT))
        
def draw_mini_map():
    miniMapX = SCREEN_WIDTH - MINI_MAP_SCALE * MAP_WIDTH - 2
    miniMapY = 0

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if GAME_MAP[y][x] == "#":
                pygame.draw.rect(screen, WHITE, (miniMapX + x * MINI_MAP_SCALE, miniMapY + y * MINI_MAP_SCALE, MINI_MAP_SCALE, MINI_MAP_SCALE))
            else:
                pygame.draw.rect(screen, (50, 50, 50), (miniMapX + x * MINI_MAP_SCALE, miniMapY + y * MINI_MAP_SCALE, MINI_MAP_SCALE, MINI_MAP_SCALE))

    fovLineLength = 5
    fovStartX = miniMapX + player_x * MINI_MAP_SCALE
    fovStartY = miniMapY + player_y * MINI_MAP_SCALE
    fovEndX = fovStartX + fovLineLength * math.sin(playerAngle)
    fovEndY = fovStartY + fovLineLength * math.cos(playerAngle)

    pygame.draw.line(screen, (255, 255, 0), (fovStartX, fovStartY), (fovEndX, fovEndY))
    pygame.draw.circle(screen, (255, 0, 0), (int(miniMapX + player_x * MINI_MAP_SCALE), int(miniMapY + player_y * MINI_MAP_SCALE)), MINI_MAP_SCALE)

def draw_info(fps):
    text_fps = font.render(f"FPS: {fps}", True, WHITE)
    text_w = font.render("W = Forward", True, WHITE)
    text_a = font.render("A = Left", True, WHITE)
    text_s = font.render("S = Backwards", True, WHITE)
    text_d = font.render("D = Right", True, WHITE)
    text_left = font.render("LEFT = Rotate Left", True, WHITE)
    text_right = font.render("RIGHT = Rotate Right", True, WHITE)

    screen.blit(text_fps, (10, 10))
    screen.blit(text_w, (10, 30))
    screen.blit(text_a, (10, 50))
    screen.blit(text_s, (10, 70))
    screen.blit(text_d, (10, 90))
    screen.blit(text_left, (10, 110))
    screen.blit(text_right, (10, 130))

running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill((0, 0, 10))
    
    elapsed_time = clock.tick(60) / 1000.0
    handle_user_input(elapsed_time)
    perform_raycasting()
    draw_mini_map()
    draw_info(int(clock.get_fps()))
    
    pygame.display.flip()

pygame.quit()
