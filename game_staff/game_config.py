# Клас який зберігає налаштування гри під час робити програми
class GameConfig():
    _instance = None # зберігає єдиний створений екземпляр цього класу

    # Створює новий екземпляр класу.
    # Працює так: якщо ще не було створено екземпляра то створити та 
    # встановити розмір екрану (0, 0) і вкінці повертає сам екземпляр.
    def __new__(cls):
        # сls - стандартний параметр для функції __new__
        # що є самим класом.
        # Повертає створений екземпляр класу
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.set_window_size(0, 0)

        return cls._instance
    
    # Встановлює розмір вікна
    def set_window_size(self, width, height):
        # width - ширина вікна
        # height - висота вікна
        # Нічого не повертає
        self.window_width = width
        self.window_height = height

    # Повератає розмір вікна
    def get_window_size(self):
        return self.window_width, self.window_height