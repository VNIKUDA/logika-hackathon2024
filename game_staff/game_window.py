# Імпорт зі скрипту screens.py екрани Меню та для тестів
from .screens import MenuScreen, GameScreen, PauseScreen, SettingScreen, AuthorsScreen, AboutScreen, DeadScreen
from .game_config import GameConfig
import pygame
pygame.init()

# Конфіг гри
config = GameConfig()

# Вікно гри
class GameWindow():
    # Конструктор класу
    def __init__(self, window_size, title="game", framerate=60, flags=0):
        # Створення вікна та встановлення назви заголовка програми 
        self.window_surface = pygame.display.set_mode(window_size, flags)
        pygame.display.set_caption(title)

        # Таймер, який буде оновлювати гру та FPS
        self.clock = pygame.time.Clock()
        self.FPS = framerate
        self.delta = 0

        # Плашка завантаження щоб прикрити довге завантаження рівнів
        loading = pygame.font.Font(None, 100).render("Завантажується...", True, (235, 235, 235))
        self.window_surface.blit(loading, (window_size[0]/2 - loading.get_width()/2, window_size[1]/2 - loading.get_height()/2))
        self.update_window()

        # Створення екранів
        self.pause_screen = PauseScreen(self)
        self.dead_screen = DeadScreen(self)
        self.game_screen = GameScreen(self)
        self.setting_screen = SettingScreen(self)
        self.about_screen = AboutScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.menu_screen = MenuScreen(self)
        
        # Поточний екран
        self.current_screen = self.menu_screen

        # Змінна, яка відображає стан вікна
        self.open = True

    # Перезапуск гри з початку
    def restart_game(self):
        player_health = self.game_screen.player.health
        config.load_progress("new_game.json")

        self.dead_screen = DeadScreen(self)
        self.pause_screen = PauseScreen(self)
        self.game_screen = GameScreen(self)
        if player_health <= 0:
            self.dead_screen.set_screen()
        else:
            self.game_screen.set_screen()
        self.setting_screen = SettingScreen(self)
        self.about_screen = AboutScreen(self)
        self.authors_screen = AuthorsScreen(self)
        self.menu_screen = MenuScreen(self)

    # Закриття вікна
    def close(self):
        self.open = False

    # Оновлення вікна
    def update_window(self):
        pygame.display.update()
        self.delta = self.clock.tick(self.FPS)/10