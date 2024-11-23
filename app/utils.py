from fastapi import UploadFile
from PIL import Image
import os
import time
import asyncio

Image.MAX_IMAGE_PIXELS = None

async def init_file(size, png_file_path, tiff_file_path):
    await asyncio.sleep(5)
    level, count = detector_of_details(size)
    print(os.path.getsize(png_file_path))
    path = convert_png_to_webp(png_file_path, tiff_file_path, level)

    parts = split_image(path, count)

    if not os.path.isdir(path_level):
        os.makedirs(path_level)

    path_level = os.path.join(os.path.dirname(png_file_path), str(count), path_level)

    
        

def detector_of_details(seze):
    if seze > 1000:
        return 90, 6

def convert_png_to_jpeg(png_file_path, jpeg_file_path, quality: int):
    # Открываем PNG изображение
    with Image.open(png_file_path) as img:
        # Проверяем, если изображение имеет альфа-канал (прозрачность)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Создаем новое изображение без альфа-канала
            img = img.convert('RGB',palette=Image.ADAPTIVE)
        
        # Сохраняем изображение в формате JPEG
        img.save(jpeg_file_path, 'JPEG', quality=quality,optimize=True)
        return jpeg_file_path
    
def convert_png_to_webp(png_file_path, webp_file_path, quality):
    # Открываем PNG изображение
    with Image.open(png_file_path) as img:
        # Сохраняем изображение в формате WebP
        img.save(webp_file_path, 'WEBP', quality=50)  # quality можно настроить от 0 до 100
        return webp_file_path 
    
def convert_png_to_tiff(png_file_path, tiff_file_path, quality):
    # Открываем PNG изображение
    with Image.open(png_file_path) as img:
        # Сохраняем изображение в формате TIFF
        img.save(tiff_file_path, 'TIFF', quality=quality)
        return tiff_file_path

def split_image(image_path, num_squares_per_side, path_level):
    # Открываем изображение
    img = Image.open(image_path)
    img_width, img_height = img.size
    
    # Определяем размер стороны квадрата
    square_side = min(img_width, img_height) // num_squares_per_side
    
    # Список для хранения частей изображения
    parts = []
    
    index = 0
    for row in range(num_squares_per_side):
        for col in range(num_squares_per_side):
            # Вычисляем координаты для обрезки
            left = col * square_side
            top = row * square_side
            right = left + square_side
            bottom = top + square_side
            
            # Проверяем, не выходит ли за пределы изображения (для последнего квадрата)
            if right > img_width or bottom > img_height:
                continue
            
            box = (left, top, right, bottom)
            
            # Обрезаем изображение и добавляем в список частей
            part = img.crop(box)
            index += 1
            part.save(os.path.join(path_level, f"part_{index + 1}.tiff"))
    
    return parts