from PIL import Image, ImageDraw
import io
import random
from telegram import InputMediaPhoto

def create_random_image(file_path):
    # Создаем изображение размером 100x100 пикселей
    image_size = (100, 100)
    image = Image.new('RGB', image_size, color='white')
    
    # Рисуем на изображении
    draw = ImageDraw.Draw(image)
    
    # Генерируем несколько случайных прямоугольников
    for _ in range(10):
        x0, y0 = random.randint(0, image_size[0] - 1), random.randint(0, image_size[1] - 1)
        x1, y1 = random.randint(0, image_size[0] - 1), random.randint(0, image_size[1] - 1)
        
        # Обеспечиваем, чтобы (x0, y0) был верхним левым углом, а (x1, y1) - нижним правым
        top_left = (min(x0, x1), min(y0, y1))
        bottom_right = (max(x0, x1), max(y0, y1))
        
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.rectangle([top_left, bottom_right], fill=color)
    
    # Сохраняем изображение на диск
    image.save(file_path, format='PNG')
