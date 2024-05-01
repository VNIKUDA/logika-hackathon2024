# Бібліотека "game_staff" це просто група скриптів для гри, що винесені в окрему папку для легшої роботи з файлами
from game_staff.game_window import GameWindow # Ігрове вікно, яке по суті є самою грою
from game_staff.game_config import GameConfig # Конфіг гри (для легшої роботи з розмірами вікна по всьому проекту)
import pygame
pygame.init()

# Визначення розмірів вікна
window_size = (1280, 720)

# Cтворення конфіга та встановлення розміру екрану
config = GameConfig()
config.set_window_size(*window_size)

# Створення ігрового вікна
window = GameWindow(window_size=window_size, title="dead cells (parody)")

# Головний ігровий цикл
while window.open == True:
    # Обробник подій
    for event in pygame.event.get():
        # Якщо було закрито вікно то закінчити роботу програми
        if event.type == pygame.QUIT:
            window.close()

        # Обробник подій поточного екрана
        window.current_screen.events(event)

    # Відмальовування поточного екрана та оновлення екрана
    window.current_screen.draw()
    window.update_window()