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

light_sources = [[player_x, player_y, 0.8, 5.0], [11, 11, 1.0, 3.0], [18, 2, 0.3, 15.0], [28, 2, 0.8, 10.0]]

angle_cahce = {}

'''Efficiently calculates sine and cosine to prevent multiple calls'''
def get_sin_cos(angle):
    if angle not in angle_cahce:
        angle_cahce[angle] = (math.sin(angle), math.cos(angle))
    return angle_cahce[angle]

'''Determine if an x, y position on the map is a wall'''
def is_wall(x, y):
    grid_x = int(x)
    grid_y = int(y)
    if 0 > grid_x >= MAP_WIDTH or 0 > grid_y >= MAP_HEIGHT:
        return True
    cell = GAME_MAP[grid_y][grid_x]
    return cell == '#'

'''Handle all movement: forawrd/backward, strafing, rotation. Normalizes
movement and detects wall collisions.'''
def handle_user_input(elapsed_time):
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()
    speed = 3.0 * elapsed_time
    dx, dy = 0, 0
    
    sin_a, cos_a = get_sin_cos(player_angle)
    
    if keys[pygame.K_w]:
        dx += sin_a
        dy += cos_a
    if keys[pygame.K_s]:
        dx -= sin_a
        dy -= cos_a
    if keys[pygame.K_a]:
        dx -= cos_a
        dy += sin_a
    if keys[pygame.K_d]:
        dx += cos_a
        dy -= sin_a
    
    magnitude = math.sqrt(dx * dx + dy * dy)
    if magnitude > 0:
        dx /= magnitude
        dy /= magnitude

    new_x = player_x + dx * speed
    new_y = player_y + dy * speed

    if not is_wall(new_x, new_y):
        player_x = new_x
        player_y = new_y
        light_sources[0][0] = player_x
        light_sources[0][1] = player_y
    
    if keys[pygame.K_LEFT]:
        player_angle -= elapsed_time
    if keys[pygame.K_RIGHT]:
        player_angle += elapsed_time

'''Determine how bright a wall should be based on player distance,
light falloff, and depth.'''
def calculate_light_intensity(x, y, dist_to_wall):
    total_intensity = 0.0
    for lx, ly, intensity, light_range in light_sources:
        dist_to_light = math.sqrt((x - lx) ** 2 + (y - ly) ** 2)
        light_falloff = max(0.0, 1.0 - dist_to_light / light_range)
        total_intensity += intensity * light_falloff
        
    total_intensity += 0.3 * (1.0 - dist_to_wall / DEPTH)
    return min(1.0, total_intensity)

'''Main raycasting function. Follows basic raycasting logic:
Find angle
Cast ray at angle until a wall or map border is hit
Calculate length of ceiling/floor portions of column
Draw ceiling line
Calculate the color of the wall based on lighting
Draw wall line
Draw floor line
'''
def perform_raycasting():
    global screen
    for x in range(SCREEN_WIDTH):
        ray_angle = player_angle - FOV / 2.0 + (x / SCREEN_WIDTH) * FOV
        dist_to_wall = 0
        hit_wall = False

        sin_ra, cos_ra = get_sin_cos(ray_angle)
        focal_x = sin_ra
        focal_y = cos_ra

        while not hit_wall and dist_to_wall < DEPTH:
            dist_to_wall += 0.1
            test_x = player_x + focal_x * dist_to_wall
            test_y = player_y + focal_y * dist_to_wall
            grid_x = int(test_x)
            grid_y = int(test_y)

            if grid_x < 0 or grid_x >= MAP_WIDTH or grid_y < 0 or grid_y >= MAP_HEIGHT:
                hit_wall = True
                dist_to_wall = DEPTH
            else:
                if GAME_MAP[grid_y][grid_x] == "#":
                    hit_wall = True

        ceiling = int(SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / dist_to_wall)
        floor = SCREEN_HEIGHT - ceiling

        pygame.draw.line(screen, (0, 0, 35), (x, 0), (x, ceiling))

        light_intensity = calculate_light_intensity(test_x, test_y, dist_to_wall)

        base_shade = 200
        shade = int(base_shade * light_intensity)
        shade = max(0, min(shade, 255))

        pygame.draw.line(screen, (shade, shade, shade), (x, ceiling), (x, floor))
        pygame.draw.line(screen, (0, 0, 65), (x, floor), (x, SCREEN_HEIGHT))

'''Draws a small mini-map on screen.'''
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
    
    for lx, ly, _, _ in light_sources:
        pygame.draw.circle(screen, YELLOW, (int(mini_map_x + lx * MINI_MAP_SCALE), int(mini_map_y + ly * MINI_MAP_SCALE)), MINI_MAP_SCALE // 2)

'''Draws instructions and info on screen'''
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

# Game loop
running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill(BLACK)
    
    elapsed_time = clock.tick(60) / 1000.0
    handle_user_input(elapsed_time)
    perform_raycasting()
    draw_mini_map()
    draw_info(int(clock.get_fps()))
    
    pygame.display.flip()

pygame.quit()
