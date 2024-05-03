# Імпорт матеріалів з скриптів
from .user_interface import Image # клас для легшої роботи з зображенням
import pygame
pygame.init()

# Скорочення для pygame.Vector2 (так краще сприймається, суто для легшої роботи)
Vector2 = pygame.Vector2


# Клас для об'єкту рівня по якому можна ходити і в який можна упиратись
class Block():
    # Конструктор класу
    # Приймає праметри position(позиція), size(розмір), path_to_image(шлях до текстурки блока)
    def __init__(self, position, size, path_to_image):
        # Позиція блока у виді вектора та розмір блока
        self.position = Vector2(*position)
        self.size = size

        # Текстурка блока
        self.image = Image(path_to_image, size, position)

        # Reсt - потрібен для колізії зi спрайтами
        self.rect = pygame.Rect(position, size)
        
        # Функція для відмальовки блока
        self.draw = self.image.draw


# Клас рівня
class Level():
    # Конструктор класу
    # Приймає параметри path_to_level(шлях до файлу який зберігає інфу про рівень), block_size(розмір одного блока), 
    # level_textures_mapping(словник типу { символ: шлях_до_текстурки } )
    def __init__(self, path_to_level, block_size, level_textures_mapping: dict):
        # Список блоків рівня
        self.level = []

        # Ширина та висота одного блока
        block_width, block_height = block_size

        # Зчитування файлу рівня та створення самого рівня з блоків
        with open(path_to_level, "r") as level:
            # y - індекс який представляє y, row - строка файлу
            for y, row in enumerate(level.readlines()):
                # X - індекс який представляє x, block - символ
                for x, block in enumerate(row.split()):
                    # Якщо символ не є заглушкою, то створити блок
                    if block in level_textures_mapping:
                        self.level.append(Block(position=(x*block_width, y*block_height), size=block_size,
                                                path_to_image=level_textures_mapping[block]))

    # Відмальовка рівня
    def draw(self, surface):
        for block in self.level:
            block.draw(surface)

# Клас для контролю рівнями
class LevelManager():
    # Конуструктор класу
    # Нічого не приймає
    def __init__(self):
        # Словник рівнів типу {назва: рівень}
        self.levels = {}

        # Поточний рівень
        self.current_level: Level

    # Додання рівня
    def add_level(self, name, level):
        self.levels[name] = level

        self.current_level = level
