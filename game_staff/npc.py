# Імпорт модулів/скриптів
from .entity import Entity # клас сутності
from .user_interface import Text # клас тексту
import json
import pygame
pygame.init()

# Клас NPC (не ігровий персонаж)
class NPC(Entity):
    # Конструктор класу
    def __init__(self, position, size, animation_time, animation_sprite_size, level_manager, player, path_to_phrases, **animations):
        super().__init__(position, size, animation_time, animation_sprite_size, level_manager, **animations)

        self.player = player

        with open(path_to_phrases, "r") as file:
            phrases = file.read()
        self.phrases = json.loads(phrases)

        self.current_phrase_index = -1
        self.is_talking = False

        self.update_dialoge_elements()

    def update_dialoge_elements(self):
        self.dialog_rect = pygame.Rect(self.rect.centerx - self.rect.width, self.rect.top - self.rect.h/1.5, self.rect.width*2, self.rect.h/2)

        text_pos = self.dialog_rect.left + self.dialog_rect.width/100*4, self.dialog_rect.top + self.dialog_rect.height/100*4
        self.dialog_text = Text(text_pos, self.phrases[self.current_phrase_index], (0,0,0), 30, None, self.dialog_rect.width)

        self.interaction_rect = pygame.Rect(self.rect.centerx - self.rect.width*1.5, self.rect.top, self.rect.width*3, self.rect.height)

    def dialoge(self):
        if self.current_phrase_index == -1:
            self.is_talking = True

        self.current_phrase_index += 1

        if self.current_phrase_index == len(self.phrases):
            self.current_phrase_index = -1
            self.is_talking = False

    def draw(self, surface, offset):
        super().draw(surface, offset)

        if self.is_talking:
            pygame.draw.rect(surface, (255, 255, 255), offset(self.dialog_rect), border_radius=10)
            self.dialog_text.draw(surface, offset)