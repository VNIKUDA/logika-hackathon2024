# Імпорт модулів/скриптів
# Клас Sprite є батьківським класом для всіх сутностей, Vector2 це просто скорочення pygame.Vector2
from .entity import Entity, Vector2 
import pygame
pygame.init()

# Клас гравця
class Player(Entity):
    # Конструктор класу
    # def __init__(self, position, size, animation_time, **animations):
    #     super().__init__(position, size, animation_time, **animations)
		
    # Взаємодія з гравцем
    def interaction(self):
        # Встановлення напрямку по осі x до 0
        self.x_direction = 0

        # Обробник подій
        # Список натиснутих клавіш
        keys = pygame.key.get_pressed()

        # Вліво
        if keys[pygame.K_a]:
            self.x_direction += -1

        # Вправо
        if keys[pygame.K_d]:
            self.x_direction += 1

        # Стрибок
        if keys[pygame.K_SPACE] and self.y_velocity == 0:
            self.y_velocity = -8
            self.is_standing = False


    # Онволення гравця
    def update(self, delta):
        self.interaction()
        super().update(delta)
