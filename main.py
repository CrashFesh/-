import os
import sys

import pygame
import requests

FPS = 120

spn_arg = 0.003
coords = [2.294363, 48.857501]
mode = "map"

pygame.init()
screen = pygame.display.set_mode((600, 450))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            if spn_arg < 49:
                spn_arg *= 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            if spn_arg > 0.002:
                spn_arg /= 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if coords[1] + 3 * spn_arg <= 90:
                coords[1] += spn_arg
            else:
                coords[1] = 90 - spn_arg // 2 - 0.0001
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if coords[1] - 3 * spn_arg >= -90:
                coords[1] -= spn_arg
            else:
                coords[1] = -90 + spn_arg // 2 + 0.0001
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if coords[0] - 2 * spn_arg >= -180:
                coords[0] -= 2 * spn_arg
            else:
                coords[0] = 180 + coords[0] - 2 * spn_arg + 180
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if coords[0] + 2 * spn_arg <= 180:
                coords[0] += 2 * spn_arg
            else:
                coords[0] = -180 + coords[0] + 2 * spn_arg - 180
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            mode = "map"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            mode = "sat"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            mode = "sat,skl"

    map_request = f"https://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&l={mode}&spn=" \
                  f"{spn_arg},{spn_arg}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        os.remove(map_file)
        pygame.quit()
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
