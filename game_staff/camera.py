# Імпорт модулів/скриптів
from .game_config import GameConfig # клас для збереження/отримування конфігу гри
import pygame
pygame.init()

# Підключення до конфігу
config = GameConfig()

# Клас камери
class Camera():
    # Конструктор класу
    # Приймає параметер level_manager(об'єкт для менеджемнту рівнів)
    def __init__(self, level_manager):
        # Ширина та висота вікна
        self.width, self.height = config.get_window_size()

        # Менеджер рівнів та ціль для камери(по замовчуваню None)
        self.level_manager = level_manager
        # self.objects = self.level_manager.current_level.level[:] + self.level_manager.current_level.npcs[:]
        self.target = None

        # Область камери 
        self.camera = pygame.Rect(0, 0, self.width, self.height)

    # Додавання об'єкта
    # def add_object(self, object):
    #     self.objects.append(object)

    # Встановити ціль камери
    def set_target(self, target):
        self.target = target

    # Оновлення камери
    def update(self):
        # Визначення оффсету по осі x
        x = self.target.rect.centerx - self.width//2 
        x = min(-self.width + self.level_manager.current_level.width, max(0, x))

        # Визначення оффсета по осі y
        y = self.target.rect.top - self.height//2
        y = min(-self.height + self.level_manager.current_level.height, max(0, y))

        self.camera = pygame.Rect(x, y, self.width, self.height)

    # Повертає об'єкт зі застосованим оффсетом
    def apply_offset(self, rect):
        return rect.move(-self.camera.left, -self.camera.top)

    # Відмальовує гру з цілю в центрі
    def draw(self, surface):
        self.level_manager.current_level.draw(surface, self.apply_offset)
        # for object in self.objects:
        #     object.draw(surface, self.apply_offset)
        self.target.draw(surface, self.apply_offset)