# Імпорт матеріалів з скриптів
from .user_interface import Image # клас для легшої роботи з зображенням
from .npc import NPC
from .enemies import Enemy
from .portal import Portal
import pygame
import os
import json
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
        self.image = Image(path_to_image, size, position).image

        # Reсt - потрібен для колізії зi спрайтами
        self.rect = pygame.Rect(position, size)
        
        # Функція для відмальовки блока
        # self.draw = self.image.draw

    def draw(self, surface, offset):
        surface.blit(self.image, offset(self.rect))

    @property
    def texture(self):
        return self.image.image


# Клас рівня
class Level():
    # Конструктор класу
    # Приймає параметри path_to_level(шлях до файлу який зберігає інфу про рівень), block_size(розмір одного блока), 
    # player(символ позиція гравця), level_textures_mapping(словник типу { символ: шлях_до_текстурки } )
    # def __init__(self, path_to_level, block_size, player, npcs: dict, level_textures_mapping: dict, path_to_background):
    def __init__(self, path_to_level, player, level_manager):
        # Список блоків рівня
        self.level = []
        self.npcs = []
        self.enemies = []
        self.portals = []

        self.player = player
        self.level_manager = level_manager

        # Зчитування файлу рівня
        with open(path_to_level, "r") as level_file:
            self.level_file = level_file.read()

        # Конфіг(параметри) створення рівня і схема рівня
        self.level_config = self.level_file.split("//")[0]
        self.level_config = json.loads("".join(self.level_config.split()))
        self.level_scheme = self.level_file.split("//")[1].strip()

        # Конфіг створення NPC
        self.npcs_config = self.level_config["npcs_config"]
        self.enemies_config = self.level_config["enemies_config"]
        self.blocks_config = self.level_config["blocks_config"]
        self.portals_config = self.level_config["portals_config"]

        # Ширина та висота одного блока
        self.block_width, self.block_height = self.block_size = tuple(self.level_config["blocks_config"]["block_size"])

        self.load_level()                        

        self.width = max([block.rect.right for block in self.level])
        self.height = max([block.rect.bottom for block in self.level])

        self.background = Image(self.level_config["path_to_background"], (self.width, self.height)).image

    def load_level(self):
        self.level = []
        self.npcs = []
        self.enemies = []
        self.portals = []

        # y - індекс який представляє y, row - строка файлу
        for y, row in enumerate(self.level_scheme.splitlines()):
            # X - індекс який представляє x, symbol - символ
            for x, symbol in enumerate(row.split()):
                # Якщо символ не є заглушкою, то створити блок
                if symbol in self.blocks_config:
                    self.level.append(Block(position=(x*self.block_width, y*self.block_height), size=self.block_size,
                                            path_to_image=self.blocks_config[symbol]))
                    
                elif symbol in self.enemies_config:
                    enemy = self.enemies_config[symbol]
                    self.enemies.append(
                        Enemy(
                            position=(x*self.block_width, y*self.block_height), size=tuple(self.enemies_config["enemy_size"]), damage=enemy["damage"], health=enemy["health"], attack_recharge_time=enemy["attack_recharge"], animation_time=enemy["animation_time"], FOV_width=enemy["FOV_width"],level_manager=self.level_manager, player=self.player, **enemy["animations"]
                        )
                    )

                elif symbol in self.npcs_config:
                    npc = self.npcs_config[symbol]
                    self.npcs.append(
                        NPC(
                            position=(x*self.block_width, y*self.block_height), size=tuple(self.npcs_config["npc_size"]), animation_time=npc["animation_time"],level_manager=self.level_manager, player=self.player, path_to_phrases=npc["path_to_phrases"], **npc["animations"]
                        )
                    )

                elif symbol in self.portals_config:
                    portal = self.portals_config[symbol]

                    self.portals.append(
                        Portal(
                            position=(x*self.block_width, y*self.block_height), size=tuple(self.portals_config["portal_size"]),
                            animation_time=10, level_manager=self.level_manager, player=self.player, level_destination=portal["level_destination"], texture = {"path": portal["texture"], "animation_time": 1, "sprite_size": portal["texture_size"]}
                        )
                    )

 
                elif symbol == self.level_config["player"]:
                    self.player.rect.topleft = x*self.block_width, y*self.block_height

    def is_on_surface(self, surface, object, offset=lambda rect: rect):
        return surface.get_rect().colliderect(offset(object.rect))
    
    def update(self, delta, offset):
        for enemy in self.enemies:
            # if self.is_on_update_area(update_area, enemy, offset):
            enemy.x_direction = 0
            if not enemy.is_attacking:
                enemy.move_to_player(offset)
            enemy.update(delta)


            if enemy.health <= 0:
                self.enemies.remove(enemy)

                self.player.increase_health(1)
                self.player.increase_damage(0.5)

            if enemy.is_attacking: 
                enemy.attack()

        for npc in self.npcs:
            # if self.is_on_update_area(update_area, npc, offset):
            npc.update_dialoge_elements()

    # Відмальовка рівня
    def draw(self, surface, offset):
        surface.blit(self.background, offset(self.background.get_rect()))
        for block in self.level:
            if self.is_on_surface(surface, block, offset):
                block.draw(surface, offset)

        if self.enemies == []:
            for portal in self.portals:
                if self.is_on_surface(surface, portal, offset):
                    portal.draw(surface, offset)
        
        for npc in self.npcs:
            if self.is_on_surface(surface, npc, offset):
                npc.draw(surface, offset)

        for enemy in self.enemies:
            if self.is_on_surface(surface, enemy, offset):
                enemy.draw(surface, offset)



# Клас для контролю рівнями
class LevelManager():
    # Конуструктор класу
    # Нічого не приймає
    def __init__(self):
        # Словник рівнів типу {назва: рівень}
        self.levels = {}

        # Поточний рівень
        self.current_level: Level


    def load_levels(self, level_directory, player):
        self.levels = {}
        # Обробка файлів та створення рівнів
        level_files = os.listdir(level_directory)
        for level_file in level_files:
            name = level_file.split(".")[0]
            self.add_level(name=name,
                           level=Level(f"{level_directory}\\{level_file}", player, self))

    # Встановлення поточного рівня
    def set_current_level(self, name):
        self.current_level = self.levels[name]

    # Додання рівня
    def add_level(self, name, level):
        self.levels[name] = level

        self.current_level = level
