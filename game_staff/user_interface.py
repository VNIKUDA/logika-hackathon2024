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

        # Маска для зчитування натиску миші на кнопку
        # Вона дозволяє проробляти дуже точну колізію з кліком мишки (якщо брати pygame.Rect,
        # він буде враховувати площу картинки, а не форму кнопки)
        self.click_area_mask = pygame.mask.from_surface(self.image)

        # Список подій(функцій), які будуть запускатися в той момент, коли буде натиснута кнопка
        self.actions = []

    # Додання події до списку подій
    def add_action(self, action):
        self.actions.append(action)

    # Запуск всіх подій
    def play_actions(self):
        for action in self.actions:
            action()

    # Обробник подій, який перевіряє чи не була натиснута кнопка
    def check_if_pressed(self, event):
        # Якщо було натиснуто ліву кнопку миші
        if event.button == 1:
            # Позиція кліку мишки відносно маски (бо маска не враховує свою позицію, тобто початок завжди з (0, 0))
            check_pos = event.pos[0] - self.position[0], event.pos[1] - self.position[1]

            # Якщо біт на цій позиції не прозорий то запустити всі події
            if self.click_area_mask.get_at(check_pos):
                self.play_actions()