# Імпорт модулів/скриптів
# Клас Entity є батьківським класом для всіх сутностей, Vector2 це просто скорочення pygame.Vector2
from .entity import Entity, Vector2 
import pygame
pygame.init()

# Клас гравця
class Player(Entity):
    # Конструктор класу
    # def __init__(self, position, size, animation_time, **animations):
    #     super().__init__(position, size, animation_time, **animations)
		
    # Переміщення гравця
    def movement(self):
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

    # Обробник подій гравця
    def interaction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for npc in self.level_manager.current_level.npcs:
                    if npc.interaction_rect.colliderect(self.rect):
                        npc.dialoge()

    # Онволення гравця
    def update(self, delta, surface, offset):
        self.movement()
        super().update(delta, surface, offset)
