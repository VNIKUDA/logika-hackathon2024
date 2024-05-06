# Імпрорт модулів
from textwrap import fill # функція для оформлення тексту (переносу слів на новий рядок)
import pygame
pygame.init()

# Клас для легшої роботи з картинками
class Image():
    # Конструктор класу.
    # Приймає параметри path_to_image(шлях до картинки), size(розмір картинки), 
    # position(позиція для відмальовування), rotation(кут повороту картинки)
    def __init__(self, path_to_image, size, position=(0, 0), rotation=0):
        # Позиція
        self.position = position

        # Завантаження картинки та її трансформування(змінення розміру та поворот)
        self.image = pygame.image.load(path_to_image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, size).convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle=rotation)

    # Відмальовування картинки
    def draw(self, surface):
        # surface - об'єкт типу pygame.Surface на якому буде відмальована картинка
        surface.blit(self.image, self.position)

# Клас для роботи з кнопками. Є спадкоємцем класу Image
class Button(Image):
    # Конструктор класу.
    # Приймає параметри всі ті самі параметри що й Image
    def __init__(self, path_to_image, size, position, rotation=0):
        # Конструктор супер класу (Image)
        super().__init__(path_to_image, size, position, rotation)

        # Маска для зчитування подій з мишкою
        # Вона дозволяє проробляти дуже точну колізію з корсором миші (якщо брати pygame.Rect,
        # він буде враховувати площу картинки, а не форму кнопки)
        self.button_area_mask = pygame.mask.from_surface(self.image)

        # Список подій(функцій), які будуть запускатися в той момент, коли буде натиснута кнопка
        self.actions = []

    # Додання події до списку подій
    def add_action(self, action):
        self.actions.append(action)

    # Запуск всіх подій
    def play_actions(self):
        for action in self.actions:
            action()

    # Обробник подій, який перевіряє чи була натиснута кнопка
    def check_if_pressed(self, event):
        # Якщо було натиснуто ліву кнопку миші
        if event.button == 1 and self.button_area_mask.get_rect(topleft=self.position, size=self.image.get_size()).collidepoint(event.pos):
            # Позиція кліку мишки відносно маски (бо маска не враховує свою позицію, тобто початок завжди з (0, 0))
            check_pos = event.pos[0] - self.position[0], event.pos[1] - self.position[1]

            # Якщо біт на цій позиції не прозорий то запустити всі події
            if self.button_area_mask.get_at(check_pos):
                self.play_actions()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Обробник подій, який перевіряє чи курсор миші націлений на кнопку
    def check_if_hovered(self, event):
        if self.button_area_mask.get_rect(topleft=self.position, size=self.image.get_size()).collidepoint(event.pos):
            check_pos = event.pos[0] - self.position[0], event.pos[1] - self.position[1]

            if self.button_area_mask.get_at(check_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Клас тексту з переносом слів на новий рядок
class Text():
    # Конструктор класу
    # Приймає параметри position(позиція), text(текст), color(колір тексту), font_size(розмір шрифта), 
    # path_to_font(шлях до шрифта), max_line_width(максимальна ширина для текструри), line_spacing(відступ між рядками)
    def __init__(self, position, text: str, color, font_size, path_to_font, max_line_width, line_spacing=0):
        self.position = position

        # Шрифт
        font = pygame.font.Font(path_to_font, font_size)

        character_width = font.render(text, True, (0,0,0)).get_width() / len(text) # (середня) ширина символу
        characters_per_line = max_line_width // character_width # кількість сиволів на один рядок 
        text = fill(text, characters_per_line) # відформатований текст

        # Кількість рядків
        lines = len(text.splitlines()) 

        # Текстура тексту
        self.image = pygame.Surface((character_width * characters_per_line, lines*font_size + lines*line_spacing)).convert_alpha()
        self.image.fill((0,0,0,0))
        for y, line in enumerate(text.splitlines()):
            self.image.blit(font.render(line, True, color), (0, y*font_size + line_spacing))

        # 
        self.rect = pygame.Rect(self.position, self.image.get_size())

    # Відмальовування тексту
    def draw(self, surface, offset):
        surface.blit(self.image, offset(self.rect))