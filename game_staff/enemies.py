# Імпорт скриптів
from .entity import Entity # клас сутності
import pygame
pygame.init()

# Клас ворога
class Enemy(Entity):
    # Конструктор класу
    # Приймає параметри position, size, damage, animation_time, level_manager, player, FOV_width, kwarg-параметер animations
    def __init__(self, position, size, damage, health, attack_recharge_time, animation_time, level_manager, player, FOV_width, **animations):
        super().__init__(position, size, animation_time, level_manager, **animations)

        # Гравець
        self.player = player

        # Дані для механіки атаки
        self.damage = damage # урон
        self.max_health = health # максимальне здоров'я
        self.health = self.max_health # здоров'я
        self.been_hit = False # чи був ворог вдарений
        self.attack_recharge_tick = 0 # 
        self.attack_recharge_time = attack_recharge_time
        self.is_attacking = False # чи ворог зараз атакує

        # Швидкість пересування ворога
        self.speed = 1

        # Область видимості ворога(в якій ворог бачить гравця)
        self.FOV_rect = pygame.Rect(self.rect.centerx - FOV_width/2, self.rect.y-self.rect.h, FOV_width, self.rect.h*2)

        # Поточна анімація
        self.current_animation = self.animations["idle"]

    # Оновлення ворога
    def update(self, delta):
        super().update(delta)

        # Якщо ворог зараз не атакує, то збільшувати лічильник для перезарядки атаки
        if not self.is_attacking:
            self.attack_recharge_tick += 1

        # Якщо перезарядка закінчилася
        if self.attack_recharge_tick >= self.attack_recharge_time:
            
            # Якщо ворог і гравець близько то атакувати гравця
            if self.player.rect.colliderect(self.rect):
                self.attack_recharge_tick = 0
                self.is_attacking = True

        # Анімація бігу
        if self.animations["attack"].animation_tick == 0:
            if self.x_direction != 0:
                self.current_animation = self.animations["run"]
            else:
                self.current_animation = self.animations["idle"]

        # Анміація атака
        if self.is_attacking and self.animations["attack"].cycles == 0:
            self.current_animation = self.animations["attack"]

        # Якщо анімація атаки програла, то зупинити атаку
        if self.current_animation == self.animations["attack"] and self.current_animation.cycles != 0:
            self.is_attacking = False
            self.current_animation.cycles = 0
            self.current_animation.animation_tick = 0

            self.current_animation = self.animations["idle"]

        # Анімувати поточну анімацію
        self.current_animation.animate()
        self.display_sprite = self.current_animation.current_sprite
        # Розвернути спрайт якщо ворог дивиться в ліво
        if self.x_direction < 0:
            self.display_sprite = pygame.transform.flip(self.display_sprite, True, False)

        # Оновлення області видимості 
        self.FOV_rect = pygame.Rect(self.rect.centerx - self.FOV_rect.w/2, self.rect.y-self.rect.h, self.FOV_rect.w, self.rect.h*2)

    # Логіка атаки
    def attack(self):
        # Маски гравця та ворога
        mask = pygame.mask.from_surface(self.current_animation.current_sprite)
        player_mask = pygame.mask.from_surface(self.player.current_animation.current_sprite)

        # Якщо маски стикаються(тобто ворог попав по грацю), то нанести урон гравцю
        if mask.overlap_area(player_mask, (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)) != 0:
            self.player.health -= self.damage
            self.player.healing_tick = 0
            self.is_attacking = False

    # Пересування к гравцю
    def move_to_player(self, offset):
        self.x_direction = 0
        # Якщо гравець у полі видимості
        if offset(self.FOV_rect).colliderect(offset(self.player.rect)):
            # якщо гравець зліва
            if self.player.rect.centerx < self.rect.centerx:
                self.x_direction = -1
            
            # якщо гравець зправа
            elif self.rect.centerx < self.player.rect.centerx:
                self.x_direction = 1

    # Відмальовка ворога
    def draw(self, surface, offset):
        super().draw(surface, offset)

        # відмальовка здоров'я ворога
        pygame.draw.rect(surface, (200, 30, 30), offset(pygame.Rect(self.rect.x+10, self.rect.y - 30, self.rect.w-20, 20)), border_radius=5)
        pygame.draw.rect(surface, (30, 200, 30), offset(pygame.Rect(self.rect.x+10, self.rect.y - 30, self.health*((self.rect.w-20) / self.max_health), 20)), border_radius=5)
            