# Імпорт модулів
import pygame 
pygame.init()

# Скорочення для pygame.Vector2 (суто для легшої роботи)
Vector2 = pygame.Vector2


# Клас анімації. Завантажує зі спрайт-листа спрайти і крутить їх по колу
class Animation():
	# Конструктор класу
	# Приймає параметри path_to_spritesheet(шлях до спрайт-листа анімації), sprite_size(розмір одного спрайта, 
	# потрібно для правильної загрузки спрайтів), sprite_time(кілкість кадрів для відмальовки спрайта)
	def __init__(self, path_to_spritesheet, sprite_size, sprite_time):
		# Завантаження спрайт-листа
		spritesheet = pygame.image.load(path_to_spritesheet).convert_alpha()

		# Обробка спрайтів
		self.sprites = []
		for index in range(0, spritesheet.get_width() // sprite_size):
			# Поверхня нового спрайта
			sprite = pygame.Surface((sprite_size, spritesheet.get_height()))
			sprite.fill((0,0,0,0))

			# Відмаловка частини спрайт-листа, де знаходиться спрайт 
			sprite.blit(spritesheet, (0, 0), area = (sprite_size * index, 0, sprite_size, spritesheet.get_height()))

			# Додання до спрайтів
			self.sprites.append(sprite.convert_alpha())

		self.animation_tick = 0 # лічильник, який визначає коли який спрайт відмальовувати
		self.sprite_time = sprite_time # кількість кадрів для відмальовки спрайта
		self.current_sprite = self.sprites[0] # поточний спрайт

	# Зміна розміру спрайтів
	def resize(self, size):
		sprites = []

		for sprite in self.sprites:
			sprites.append(pygame.transform.scale(sprite, size).convert_alpha())

		self.sprites = sprites
		self.current_sprite = self.sprites[0]
		
	# Відтворення анімації
	def animate(self):
		self.animation_tick += 1

		# Зброс лічильника анімації
		if self.animation_tick >= len(self.sprites)*self.sprite_time:
			self.animation_tick = 1

		# Встановлення поточного спрайта
		self.current_sprite = self.sprites[self.animation_tick // self.sprite_time]


# Клас сутності
class Entity():
	# Конструктор класа
	# Приймає параметри position(позиція сутності), size(розмір сутності), animation_time(кілкість кадрів для 
	# відмальовки спрайта), level_manager(менеджер рівнів), kwarg-параметер animations(словник типу назва:шлях_до_спрайт-листа)
	def __init__(self, position, size, animation_time, animation_sprite_size, level_manager, **animations):
		# Позиція та розмір сутності
		self.position = Vector2(position)
		self.size = size

		# менеджер рівнів
		self.level_manager = level_manager

		# Напрямок по осі x, швидкість по осі y(гравітація) та просто швидкість
		self.x_direction = 0
		self.y_velocity = 0
		self.speed = 5

		# rect для роботи з колізією та переміщенням
		self.rect = pygame.Rect(self.position, self.size)
 
		# Завантаження анімацій
		self.animations = {}
		for name, path_to_spritesheet in animations.items():
			animation = Animation(path_to_spritesheet, animation_sprite_size, animation_time)
			animation.resize(self.size)
			self.animations[name] = animation

		# Поточна анімація
		self.current_animation: Animation = list(self.animations.values())[0]


	# Оновлення сутності (гравітація, колізія, переміщення)
	def update(self, delta, surface, offset):
		# зміщення від поточної позиції
		dx = round(self.x_direction * self.speed * delta)
		dy = round(self.y_velocity * delta)

		# Ліміт пришвидшення швидкості вільного падіння
		if self.y_velocity < 20:
			self.y_velocity += 0.2 * delta

		# Колізія з рівнем
		for block in self.level_manager.current_level.level:
			if self.level_manager.current_level.is_on_surface(surface, block, offset):
				# Перевірка колізії по осі x
				if block.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.w, self.rect.h):
					# dx = 0
					if self.x_direction < 0:
						dx = block.rect.right - self.rect.left

					elif self.x_direction > 0:
						dx = block.rect.left - self.rect.right

				# Перевірка колізії по осі y
				if block.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.w, self.rect.h):
					if self.y_velocity < 0:
						self.y_velocity = 0.00000000000000001
						dy = block.rect.bottom - self.rect.top

					elif self.y_velocity >= 0:
						self.y_velocity = 0
						dy = block.rect.top - self.rect.bottom

		# Переміщення гравця по зміщенню
		self.rect.x += dx
		self.rect.y += dy

		self.current_animation.animate()
	
	# Перевірає чи треба відмальовувати сутність на екрані
	def is_on_surface(self, surface, offset):
		return surface.get_rect().colliderect(offset(self.rect))

	# Відмальовуванння сутності
	def draw(self, surface, offset):
		if self.is_on_surface(surface, offset):
			surface.blit(self.current_animation.current_sprite, offset(self.rect))
		# pygame.draw.rect(surface, (255, 0, 255), self.rect)
        
	@property
	def texture(self):
		return self.current_animation.current_sprite