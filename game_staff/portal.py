from .entity import Entity
import pygame
pygame.init()


class Portal(Entity):
    def __init__(self, position, size, animation_time, level_manager, player, level_destination, **animations):
        super().__init__(position, size, animation_time, level_manager, **animations)

        self.level_destination = level_destination
        self.player = player

        self.interaction_rect = pygame.Rect(self.rect.x-self.rect.w, self.rect.y, self.rect.w*3, self.rect.h)

    def teleport_player(self):
        self.level_manager.current_level = self.level_manager.levels[self.level_destination]
        self.level_manager.current_level.load_level()

    def interaction(self, event):
        for event in pygame.event.get():
            if event.type == pygame.K_e and self.interaction_rect.colliderect(self.player.rect):
                self.teleport_player()