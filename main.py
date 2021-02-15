import os
import sys

import pygame
import requests

FPS = 120

spn_arg = 0.003

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
    map_request = f"https://static-maps.yandex.ru/1.x/?ll=2.294363,48.857501&l=map&spn={spn_arg}" \
                  f",{spn_arg}"
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
