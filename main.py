import pygame
import math
from constants import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_x = 6.0
player_y = 8.0
player_angle = math.pi / 2

font = pygame.font.Font(None, 24)

def is_wall(x, y):
    grid_x = int(x)
    grid_y = int(y)
    if 0 > grid_x >= MAP_WIDTH or 0 > grid_y >= MAP_HEIGHT:
        return True
    cell = GAME_MAP[grid_y][grid_x]
    return cell == '#'

def handle_user_input(elapsed_time):
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()
    speed = 3.0 * elapsed_time
    dx, dy = 0, 0
    
    if keys[pygame.K_w]:
        dx += math.sin(player_angle)
        dy += math.cos(player_angle)
    if keys[pygame.K_s]:
        dx -= math.sin(player_angle)
        dy -= math.cos(player_angle)
    if keys[pygame.K_a]:
        dx -= math.cos(player_angle)
        dy += math.sin(player_angle)
    if keys[pygame.K_d]:
        dx += math.cos(player_angle)
        dy -= math.sin(player_angle)
    
    magnitude = math.sqrt(dx * dx + dy * dy)
    if magnitude > 0:
        dx /= magnitude
        dy /= magnitude

    new_x = player_x + dx * speed
    new_y = player_y + dy * speed

    if not is_wall(new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    if keys[pygame.K_LEFT]:
        player_angle -= elapsed_time
    if keys[pygame.K_RIGHT]:
        player_angle += elapsed_time

def perform_raycasting():
    for x in range(SCREEN_WIDTH):
        ray_angle = player_angle - FOV / 2.0 + (x / SCREEN_WIDTH) * FOV
        dist_to_wall = 0
        hit_wall = False

        focal_x = math.sin(ray_angle)
        focal_y = math.cos(ray_angle)

        while not hit_wall and dist_to_wall < DEPTH:
            dist_to_wall += 0.1
            test_x = int(player_x + focal_x * dist_to_wall)
            test_y = int(player_y + focal_y * dist_to_wall)

            if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                hit_wall = True
                dist_to_wall = DEPTH
            else:
                if GAME_MAP[test_y][test_x] == "#":
                    hit_wall = True

        ceiling = int(SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / dist_to_wall)
        floor = SCREEN_HEIGHT - ceiling
        x_screen = x * (SCREEN_WIDTH / SCREEN_WIDTH)

        pygame.draw.line(screen, (0, 0, 65), (x_screen, 0), (x_screen, ceiling))
        shade = int(255 - (dist_to_wall / DEPTH) * 255)
        blue_shade = max(0, min(shade + 15, 255))
        pygame.draw.line(screen, (shade, shade, blue_shade), (x_screen, ceiling), (x_screen, floor))
        pygame.draw.line(screen, (0, 0, 35), (x_screen, floor), (x_screen, SCREEN_HEIGHT))
        
def draw_mini_map():
    mini_map_x = SCREEN_WIDTH - MINI_MAP_SCALE * MAP_WIDTH - 2
    mini_map_y = 0

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if GAME_MAP[y][x] == "#":
                pygame.draw.rect(screen, WHITE, (mini_map_x + x * MINI_MAP_SCALE, mini_map_y + y * MINI_MAP_SCALE, MINI_MAP_SCALE, MINI_MAP_SCALE))
            else:
                pygame.draw.rect(screen, (50, 50, 50), (mini_map_x + x * MINI_MAP_SCALE, mini_map_y + y * MINI_MAP_SCALE, MINI_MAP_SCALE, MINI_MAP_SCALE))

    fov_line_length = 5
    fov_start_x = mini_map_x + player_x * MINI_MAP_SCALE
    fov_start_y = mini_map_y + player_y * MINI_MAP_SCALE
    fov_end_x = fov_start_x + fov_line_length * math.sin(player_angle)
    fov_end_y = fov_start_y + fov_line_length * math.cos(player_angle)

    pygame.draw.line(screen, (255, 255, 0), (fov_start_x, fov_start_y), (fov_end_x, fov_end_y))
    pygame.draw.circle(screen, (255, 0, 0), (int(mini_map_x + player_x * MINI_MAP_SCALE), int(mini_map_y + player_y * MINI_MAP_SCALE)), MINI_MAP_SCALE)

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
