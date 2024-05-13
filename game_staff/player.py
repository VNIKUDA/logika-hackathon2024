# Імпорт модулів/скриптів
# Клас Entity є батьківським класом для всіх сутностей, Vector2 це просто скорочення pygame.Vector2
from .entity import Entity, Vector2 
from .game_config import GameConfig
from .user_interface import Image
from .weapons import Weapon
import pygame
pygame.init()

config = GameConfig()

# Клас гравця
class Player(Entity):
    # Конструктор класу
    def __init__(self, position, size, animation_time, **animations):
        super().__init__(position, size, animation_time, **animations)

        # Розміри вікна
        self.windows_size = pygame.Rect((0,0), config.get_window_size())

        # Механіка здоров'я
        self.max_health = 25
        self.health = self.max_health
        self.healing_tick = 0

        # Бонус атаки
        self.damage_bonus = 0

        # Чи гравець зараз атакує
        self.is_attacking = False

        # Полманий меч
        self.broken_sword = Weapon(self, (self.rect.w, self.rect.h*1.5), 3, 80, 8, 
                                   hold={"path": "game_assets\\images\\broken_sword.png", "sprite_size": 167}, 
                                   attack={"path": "game_assets\\images\\slash.png", "sprite_size": 98})
        # Катана
        self.katana = Weapon(self, (self.rect.w, self.rect.h*1.5), 9, 170, 15, 
                             hold={"path": "game_assets\\images\\katana.png", "sprite_size": 167}, 
                             attack={"path": "game_assets\\images\\slash.png", "sprite_size": 98})

        # Іконки для зброї
        self.broken_sword_icon = Image("game_assets\\images\\broken_sword_icon.png", (50, 50), (self.windows_size.width*0.03, self.windows_size.height*0.81))
        self.katana_icon = Image("game_assets\\images\\katana_icon.png", (50, 50), (self.windows_size.width*0.03 + 70, self.windows_size.height*0.81))

        # Поточна зброя та її іконка
        self.current_weapon = self.broken_sword
        self.current_weapon_icon = self.broken_sword_icon
		
    # Переміщення гравця
    def movement(self):
        # Встановлення напрямку по осі x до 0
        self.x_direction = 0

        # Обробник подій
        # Список натиснутих клавіш
        keys = pygame.key.get_pressed()

        # Вліво
        if keys[config.controls["Left"]]:
            self.x_direction += -1
            self.direction = -1

        # Вправо
        if keys[config.controls["Right"]]:
            self.x_direction += 1
            self.direction = 1

        # Стрибок
        if keys[config.controls["Jump"]] and self.y_velocity == 0:
            self.y_velocity = -8
            self.is_standing = False

        if keys[pygame.K_RETURN] and self.current_weapon.current_animation == self.current_weapon.animations["hold"] and self.current_weapon.recharge_tick <= 0:
            self.is_attacking = True

    # Відмальовка гравця
    def draw(self, surface, offset):
        super().draw(surface, offset)
        if self.x_direction == 0 or self.current_weapon.current_animation == self.current_weapon.animations["attack"]:
            self.current_weapon.draw(surface, offset)


    # Обробник подій гравця
    def interaction(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for npc in self.level_manager.current_level.npcs:
                    if npc.interaction_rect.colliderect(self.rect):
                        npc.dialoge()

                if self.level_manager.current_level.enemies == []:
                    for portal in self.level_manager.current_level.portals:
                        if portal.interaction_rect.colliderect(self.rect):
                            portal.teleport_player()


            # Перемикання зброї
            if not self.is_attacking:
                # На меч
                if event.key == pygame.K_1:
                    self.current_weapon = self.broken_sword
                    self.current_weapon_icon = self.broken_sword_icon

                # На катану
                if event.key == pygame.K_2:
                    self.current_weapon = self.katana
                    self.current_weapon_icon = self.katana_icon

        # Атака
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.current_weapon.current_animation == self.current_weapon.animations["hold"] and self.current_weapon.recharge_tick <= 0:
                self.is_attacking = True

    # Збільшення здоро'я(після перемоги на ворогом)
    def increase_health(self, amount):
        if self.max_health < 100:
            self.max_health += amount
            self.health += amount

    # Збільшення урону
    def increase_damage(self, amount):
        self.damage_bonus += amount

        self.katana.damage += amount
        self.broken_sword.damage += amount

    # Онволення гравця
    def update(self, delta):
        super().update(delta)

        # Атака
        self.katana.recharge_tick -= 1
        self.broken_sword.recharge_tick -= 1

        self.current_weapon.update()
        if self.is_attacking:
            self.current_weapon.attack()

        else:
            for enemy in self.level_manager.current_level.enemies:
                enemy.been_hit = False

        # Відновлення здоров'я
        self.healing_tick += 1
        if self.healing_tick >= 300:
            if self.healing_tick % 20 == 0 and self.health != self.max_health:
                self.health += 1

        # Анімація
        if self.animations["attack"].animation_tick == 0:
            if self.x_direction != 0:
                self.current_animation = self.animations["run"]
            else:
                self.current_animation = self.animations["idle"]

        if self.is_attacking and self.animations["attack"].cycles == 0:
            self.current_animation = self.animations["attack"]


        if self.current_animation == self.animations["attack"] and self.current_animation.cycles != 0:
            self.is_attacking = False
            self.current_animation.cycles = 0
            self.current_animation.animation_tick = 0

            self.current_animation = self.animations["idle"]

        self.current_animation.animate()
        self.display_sprite = self.current_animation.current_sprite
        if self.direction < 0:
            self.display_sprite = pygame.transform.flip(self.display_sprite, True, False).convert_alpha()

    # Відмальовка статів гравця (здоров'я, яка зараз зброя вибрана і тд)
    def draw_stats_ui(self, surface):
        # Здоров'я
        pygame.draw.rect(surface, (200, 30, 30), pygame.Rect(self.windows_size.width*0.03, self.windows_size.height*0.9, self.max_health*10, 50), border_radius=4)
        pygame.draw.rect(surface, (30, 200, 30), pygame.Rect(self.windows_size.width*0.03, self.windows_size.height*0.9, self.health*10, 50), border_radius=4)

        # Кількість здров'я
        font = pygame.font.Font(None, 35)
        font.set_bold(True)
        health_status = font.render(f"{self.health} / {self.max_health}", True, (255, 250, 250))
        health_status_pos = self.windows_size.width*0.03 + self.max_health*5 - health_status.get_width()/2, self.windows_size.height*0.9 + 25 - health_status.get_height()/2
        surface.blit(health_status, health_status_pos)
        
        # Штука для вибраної зброї
        surface.blit(self.current_weapon_icon.get_outline(), (self.current_weapon_icon.position[0]-3, self.current_weapon_icon.position[1]-3))


        # Статус готовності для використання зброї
        # Для меча
        status_color = (107, 157, 237) if self.broken_sword.recharge_tick <= 0 else (176, 21, 0)
        weapon_status_pos = self.broken_sword_icon.position[0] + self.broken_sword_icon.image.get_width()/2, self.broken_sword_icon.position[1] + self.broken_sword_icon.image.get_height()/2
        pygame.draw.circle(surface, status_color, weapon_status_pos, self.broken_sword_icon.image.get_width()/2)
        self.broken_sword_icon.draw(surface)

        # Для катани
        status_color = (107, 157, 237) if self.katana.recharge_tick <= 0 else (176, 21, 0)
        weapon_status_pos = self.katana_icon.position[0] + self.katana_icon.image.get_width()/2, self.katana_icon.position[1] + self.katana_icon.image.get_height()/2
        pygame.draw.circle(surface, status_color, weapon_status_pos, self.katana_icon.image.get_width()/2)
        self.katana_icon.draw(surface)

