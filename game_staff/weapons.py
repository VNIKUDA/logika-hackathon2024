from .game_config import GameConfig
from .entity import Animation
import pygame
pygame.init()

# Конфіг гри
config = GameConfig()

# Клас зброї
class Weapon():
    def __init__(self, player, size, damage, recharge_time, animation_time, **animations):
        # Гравець, урон зброї та розмір
        self.player = player
        self.damage = damage
        self.size = size

        # Анімації
        self.animations = {}
        for name, animation in animations.items():
            animation = Animation(animation["path"], animation["sprite_size"], animation_time)
            animation.resize(self.size)
            self.animations[name] = animation

        # Поточна анімація
        self.current_animation = list(self.animations.values())[0]

        # Перезарядка
        self.recharge_time = recharge_time
        self.recharge_tick = recharge_time

        # Маска для визначення чи попала зброя по ворогу
        self.weapon_mask = pygame.mask.from_surface(self.current_animation.current_sprite)
        self.rect = pygame.Rect((self.player.rect.centerx, self.player.rect.centery - self.weapon_mask.get_rect().h/2), self.size)

    # Відмальовка зброї
    def draw(self, surface, offset):
        display_surf = self.current_animation.current_sprite
        if self.player.direction < 0:
            display_surf = pygame.transform.flip(display_surf, True, False)

        # Якщо анімація тримання в руках, то відмалювати в руках
        if self.current_animation == self.animations["hold"]:
            display_rect = self.rect.move(-55, 50) if self.player.direction > 0 else self.rect.move(55, 50)
        # Якщо ні, то відмалювати по переду гравця
        else:
            display_rect = self.rect

        # Відмальовка
        surface.blit(display_surf, offset(display_rect))

    # Логіка атаки
    def attack(self):
        # Список ворогів
        enemies = self.player.level_manager.current_level.enemies

        for enemy in enemies:
            # Якщо ворог ще не був ударений (за цю атаку), то перевірити чи гравець попав по ньому
            if not enemy.been_hit:
                enemy_mask = pygame.mask.from_surface(enemy.current_animation.current_sprite)
                # Якщо попав, нанести урон ворогу
                if self.weapon_mask.overlap_area(enemy_mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)) != 0:
                    enemy.health -= self.damage
                    enemy.been_hit = True

    # Оновлення
    def update(self):
        # Анімація
        self.current_animation.animate()
        
        # Якщо атака то запустити анімацію атаки
        if self.player.is_attacking and self.animations["attack"].cycles == 0 and self.recharge_tick <= 0:
            self.current_animation = self.animations["attack"]

        # Якщо анімація атаки закінчилася
        if self.current_animation == self.animations["attack"] and self.current_animation.cycles != 0:
            self.player.is_attacking = False
            self.current_animation.cycles = 0
            self.recharge_tick = self.recharge_time

            self.current_animation = self.animations["hold"]

        # Оновлення маски та колізійного бокса відносно куди дивиться гравець
        if self.player.direction > 0: 
            self.weapon_mask = pygame.mask.from_surface(self.current_animation.current_sprite)
            self.rect = pygame.Rect((self.player.rect.centerx, self.player.rect.centery - self.weapon_mask.get_rect().h/2), self.size)
        else:
            self.weapon_mask = pygame.mask.from_surface(pygame.transform.flip(self.current_animation.current_sprite, True, False))
            self.rect = pygame.Rect((self.player.rect.centerx-self.size[0], self.player.rect.centery - self.weapon_mask.get_rect().h/2), self.size)




        