# Імпорт необхідних матеріалів з бібліотек/скриптів
from .game_config import GameConfig # Конфіг гри (для легшої роботи з розмірами вікна по всьому проекту)
from .user_interface import Image, Button # Клас картинки та кнопки
from .player import Player
from .npc import NPC
from .level import LevelManager, Level
from .camera import Camera
from abc import abstractmethod # декоратор для абстрактного метода
import pygame
pygame.init()

# Конфіг гри
config = GameConfig()
config.load_config("config.json")

# Клас екрану (абстрактний/батьківський)
class Screen():
    # Конструктор класу. Приймає параметр window(вікно гри)
    def __init__(self, window):
        self.window = window # вікно гри
        self.window_surface = self.window.window_surface # pygame.Surface цього вікна 

        self.screen_changing = False

    # Встановлює себе як поточний екран вікна
    def set_screen(self):
        for button in Button.buttons:
            button.is_hovered = False
        self.screen_changing = True
        
        # Fade out
        fade = pygame.Surface(config.get_window_size(), flags=pygame.SRCALPHA)
        fade.fill((0,0,0))

        self.window.current_screen.draw()
        for alpha in range(0, 50):
            fade.set_alpha(alpha)
            self.window_surface.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)

        self.window.current_screen = self

        # fade in
        for alpha in reversed(range(0, 255, 5)):
            self.window.current_screen.update_screen()
            self.window.current_screen.draw()
            
            fade.set_alpha(alpha)

            self.window_surface.blit(fade, (0, 0))
            self.window.update_window()

        self.screen_changing = False

    # Абстрактні методи класу
    # Відмальовка всіх об'єктів екрану
    @abstractmethod
    def draw(self):
        pass

    # Обробник подій об'єктів екрану
    @abstractmethod
    def events(self, event):
        # event - об'єкт типу pygame.event.Event, потрібен для обробки подій
        pass


# Клас екрану головного меню. Є спадкоємцем класу Screen
class MenuScreen(Screen):
    # Конструктор класу. Приймає параметер window()
    def __init__(self, window):
        # Конструктор супер-класу
        super().__init__(window)

        # Створення фону
        self.background = Image(path_to_image="game_assets\\images\\main_art.png", size=config.get_window_size())

        # Кнопки для старту гри, 
        w, h = config.get_window_size()
        self.start_button = Button(path_to_image="game_assets\\images\\ГРАТИ.png", size=(175, 70), position=(50, h*0.55-80), rotation=0)
        self.setting_button = Button(path_to_image="game_assets\\images\\НАЛАШТУВАННЯ.png", size=(420, 70), position=(50, h*0.55 + 80), rotation=0)
        self.authors_button = Button(path_to_image="game_assets\\images\\АВТОРИ.png", size=(200, 70), position=(50, h*0.55 +   160), rotation=0)        
        self.exit_button = Button(path_to_image="game_assets\\images\\ВИХІД.png", size=(170, 70), position=(50, h*0.55 + 240), rotation=0)
        self.new_game_button = Button(path_to_image="game_assets\\images\\НОВА ГРА.png", size=(250, 70), position=(50, h*0.55))

        # Призначення подій на кожну з кнопок 
        self.start_button.add_action(self.window.game_screen.set_screen)
        self.setting_button.add_action(self.window.setting_screen.set_screen)
        self.authors_button.add_action(self.window.authors_screen.set_screen)
        self.exit_button.add_action(self.window.close)
        self.new_game_button.add_action(self.window.restart_game)

    # Оновлення екрана
    def update_screen(self):
        pass

    # Відмальовування екрану
    def draw(self):
        self.background.draw(self.window_surface)
        self.start_button.draw(self.window_surface)
        self.new_game_button.draw(self.window_surface)
        self.authors_button.draw(self.window_surface)
        self.setting_button.draw(self.window_surface)
        self.exit_button.draw(self.window_surface)

    # Обробник подій екрану
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.start_button.check_if_pressed(event)
            self.new_game_button.check_if_pressed(event)
            self.setting_button.check_if_pressed(event)
            self.authors_button.check_if_pressed(event)
            self.exit_button.check_if_pressed(event)

        if event.type == pygame.MOUSEMOTION:
            self.start_button.check_if_hovered(event)
            self.new_game_button.check_if_hovered(event)
            self.setting_button.check_if_hovered(event)
            self.authors_button.check_if_hovered(event)
            self.exit_button.check_if_hovered(event)


# Клас ігрового еркану
class GameScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

        # Об'єкт для менеджменту рівнів + додання рівня
        self.level_manager = LevelManager()

        self.player = Player(position=(0, -1), size=(100, 200), animation_time=8, level_manager=self.level_manager, 
                        idle={"path": "game_assets\\images\\hero.png", "sprite_size": 251},
                        run={"path": "game_assets\\images\\hero_run.png", "sprite_size": 221},
                        attack={"path": "game_assets\\images\\hero.png", "sprite_size": 251})
        
        self.player.max_health = config.game_data["player_max_health"]
        self.player.health = config.game_data["player_max_health"]
        self.player.increase_damage(config.game_data["player_damage_bonus"])

        self.level_manager.load_levels(level_directory="levels", player=self.player)
        self.level_manager.current_level = self.level_manager.levels[config.game_data["level_name"]]
        self.level_manager.current_level.load_level()

        # Камера
        self.camera = Camera(self.level_manager)
        self.camera.set_target(self.player)

        self.pause_button = Button(path_to_image="game_assets\\images\\Pause.png", size=(75, 75), position=(30, 30))
        self.pause_button.add_action(self.window.pause_screen.set_screen)


    # Оновлення екрана
    def update_screen(self):
        self.level_manager.current_level.update(self.window.delta, self.camera.apply_offset)
        self.camera.update()
        if not self.screen_changing:
            self.player.movement()

        self.player.update(self.window.delta)

        if self.player.health <= 0:
            self.player.health = 0
            self.window.restart_game()
            
        
    # Відмальовування екрана
    def draw(self):
        self.camera.draw(self.window_surface)
        self.player.draw_stats_ui(self.window_surface)

        self.pause_button.draw(self.window_surface)

    # Обробник подій екрана
    def events(self, event):
        # Обробник подій гравця
        self.player.interaction(event)

        # Відкриття меню паузи на ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.window.pause_screen.set_screen()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pause_button.check_if_pressed(event)

        if event.type == pygame.MOUSEMOTION:
            self.pause_button.check_if_hovered(event)

class DeadScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

        self.background = Image("game_assets\\images\\main_art.png", config.get_window_size())

        w, h = config.get_window_size()
        self.you_lose_text = Image("game_assets\\images\\ВИ ПРОГРАЛИ.png", (800, 180), (50, h*0.5-90))
        self.menu_button = Button("game_assets\\images\\МЕНЮ.png", (180, 70), (50, h*0.75 + 80))
        self.restart_button = Button("game_assets\\images\\ЗАНОВО.png", (270, 70), (50, h*0.75))

    def update_screen(self):
        self.menu_button.actions = []
        self.menu_button.add_action(self.window.menu_screen.set_screen)

        self.restart_button.actions = []
        self.restart_button.add_action(self.window.game_screen.set_screen)

    def draw(self):
        self.background.draw(self.window_surface)
        self.you_lose_text.draw(self.window_surface)
        self.restart_button.draw(self.window_surface)
        self.menu_button.draw(self.window_surface)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.restart_button.check_if_pressed(event)
            self.menu_button.check_if_pressed(event)

        if event.type == pygame.MOUSEMOTION:
            self.menu_button.check_if_hovered(event)
            self.restart_button.check_if_hovered(event)


class SettingScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

        self.background = Image(path_to_image="game_assets\\images\\main_art.png", size=config.get_window_size())
        self.back_button = Button(path_to_image="game_assets\\images\\back.png", size=(248, 75), position=(30, 30))

        self.about_controls = Image(path_to_image="game_assets\\images\\about_controls.png", size=(1048, 305), position=(50, 140))

        controls_type = "" if config.controls_type == "A, D, SPACE" else "_arrows"
        self.change_controls_button = Button(f"game_assets\\images\\controls{controls_type}.png", (700, 75), (50, 520))
        self.change_controls_button.add_action(self.change_controls)

        self.about_button = Button(path_to_image="game_assets\\images\\ПРО ГРУ.png", size=(250, 70), position=(50, 600))

    def update_screen(self):
        self.back_button.actions = []
        self.back_button.add_action(self.window.menu_screen.set_screen)

        self.about_button.actions = []
        self.about_button.add_action(self.window.about_screen.set_screen)

    def change_controls(self):
        if config.controls_type == "A, D, SPACE":
            config.controls_type = "Arrows"
            config.controls = {
                "Left": pygame.K_LEFT,
                "Right": pygame.K_RIGHT,
                "Jump": pygame.K_UP
            }

            img = "controls_arrows.png"

        else:
            config.controls_type = "A, D, SPACE"
            config.controls = {
                "Left": pygame.K_a,
                "Right": pygame.K_d,
                "Jump": pygame.K_SPACE
            }

            img = "controls.png"

        size = self.change_controls_button.image.get_size()
        position = self.change_controls_button.position

        self.change_controls_button = Button(f"game_assets\\images\\{img}", size, position)
        self.change_controls_button.add_action(self.change_controls)


    def draw(self):
        self.background.draw(self.window_surface)
        self.back_button.draw(self.window_surface)
        self.about_controls.draw(self.window_surface)
        self.change_controls_button.draw(self.window_surface)
        self.about_button.draw(self.window_surface)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.back_button.check_if_pressed(event)
            self.change_controls_button.check_if_pressed(event)
            self.about_button.check_if_pressed(event)

        if event.type == pygame.MOUSEMOTION:
            self.back_button.check_if_hovered(event)
            self.change_controls_button.check_if_hovered(event)
            self.about_button.check_if_hovered(event)


class AuthorsScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

        self.background = Image(path_to_image="game_assets\\images\\main_art.png", size=config.get_window_size())
        self.back_button = Button(path_to_image="game_assets\\images\\back.png", size=(248, 75), position=(30, 30))

        w, h = self.window_surface.get_size()
        self.authors = Image(path_to_image="game_assets\\images\\authors.png", size=(732, 488), position=(w*0.5 - 732/2, h*0.5 - 488/2))

    def update_screen(self):
        self.back_button.actions = []
        self.back_button.add_action(self.window.menu_screen.set_screen)

    def draw(self):
        self.background.draw(self.window_surface)
        self.back_button.draw(self.window_surface)
        self.authors.draw(self.window_surface)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.back_button.check_if_pressed(event)
        if event.type == pygame.MOUSEMOTION:
            self.back_button.check_if_hovered(event)

class AboutScreen(Screen):
    def __init__(self, window):
        super().__init__(window)
        
        self.background = Image(path_to_image="game_assets\\images\\main_art.png", size=config.get_window_size())
        self.back_button = Button(path_to_image="game_assets\\images\\back.png", size=(248, 75), position=(30, 30))
        self.back_button.add_action(self.window.setting_screen.set_screen)

        w, h = self.window_surface.get_size()
        self.about_text = Image(path_to_image="game_assets\\images\\about_game.png", size=(732, 427), position=(w/2 - 732/2, h/2 - 427/2))


    def update_screen(self):
        pass

    def draw(self):
        self.background.draw(self.window_surface)
        self.back_button.draw(self.window_surface)
        self.about_text.draw(self.window_surface)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.back_button.check_if_pressed(event)

        if event.type == pygame.MOUSEMOTION:
            self.back_button.check_if_hovered(event)


# Меню паузи
class PauseScreen(Screen):
    def __init__(self, window):
        super().__init__(window)

        # Фон паузи
        self.background = Image("game_assets\\images\\main_art.png", config.get_window_size())
        self.continue_button = Button(path_to_image="game_assets\\images\\Continue.png", size=(75, 75), position=(30, 30))

        w, h = self.window_surface.get_size()
        self.pause_text = Image("game_assets\\images\\ПАУЗА.png", (400, 130), (50, h*0.5-65))
        self.reset_level_button = Button("game_assets\\images\\ЗАНОВО.png", (270, 70), (50, h*0.75))
        self.menu_button = Button("game_assets\\images\\МЕНЮ.png", (180, 70), (50, h*0.75 + 80))

    # Оновлення  екрана
    def update_screen(self):
        self.reset_level_button.actions = []
        self.reset_level_button.add_action(self.window.game_screen.level_manager.current_level.load_level)
        self.reset_level_button.add_action(self.window.game_screen.set_screen)

        self.menu_button.actions = []
        self.menu_button.add_action(self.window.menu_screen.set_screen)

        self.continue_button.actions = []
        self.continue_button.add_action(self.window.game_screen.set_screen)


    # Відмальовування екрана
    def draw(self):
        self.background.draw(self.window_surface)
        self.pause_text.draw(self.window_surface)
        self.reset_level_button.draw(self.window_surface)
        self.menu_button.draw(self.window_surface)
        self.continue_button.draw(self.window_surface)

    # Обробник подій екрана
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.window.game_screen.set_screen()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_level_button.check_if_pressed(event)
            self.menu_button.check_if_pressed(event)
            self.continue_button.check_if_pressed(event)

        if event.type == pygame.MOUSEMOTION:
            self.reset_level_button.check_if_hovered(event)
            self.menu_button.check_if_hovered(event)
            self.continue_button.check_if_hovered(event)
        