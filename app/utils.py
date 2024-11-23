from fastapi import UploadFile
from PIL import Image
import os
import time
import asyncio
import pyvips

# Image.MAX_IMAGE_PIXELS = None

async def init_file(file_name_data: str, size):
    if size > 1000000:
        # Ждём освобождения оперативки для дальнейших действий с большими файлами
        await asyncio.sleep(5) 
    
    #Путь до исходного файла
    path_upload = os.path.join('uploads', ".".join(file_name_data[:-1]), ".".join(file_name_data))
    #Путь до сжатого
    path_compress = os.path.join('uploads', ".".join(file_name_data[:-1]), ".".join(file_name_data[-1])+".webp")
    
    path_dir_base = os.path.join('uploads', ".".join(file_name_data[:-1]))

    print(os.path.getsize(path_upload))

    for level, count in detector_of_details(size):
        img = convert_img_to_webp(path_upload, path_compress, level)
        # convert_tiff_to_webp(path_upload, path_compress)          
        # img = Image.open(path_compress)
        path_dir = os.path.join(path_dir_base, str(count))
        
        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)

        split_image(img, count, path_dir)

    # path_level = os.path.join(os.path.dirname(png_file_path), str(count), path_level) 

def detector_of_details(seze):
    levels = []
    if seze > 1000:
        levels.append([90, 6])
    if seze > 6000:
        levels.append([50, 1])
    return levels
    
def convert_img_to_webp(png_file_path: str, webp_file_path: str, quality: int):
    # Открываем PNG изображение
    with Image.open(png_file_path) as img:
        # Сохраняем изображение в формате WebP
        print("start confert")
        img.save(webp_file_path, 'WEBP', quality=quality)  # quality можно настроить от 0 до 100
        print(os.path.getsize(webp_file_path))
        return img

# def convert_tiff_to_webp(input_path, output_path):
#     image = pyvips.Image.new_from_file(input_path)
#     image.write_to_file(output_path)


def split_image(img: Image, num_squares_per_side, path_level):
    img_width, img_height = img.size
    
    # Определяем размер стороны квадрата
    square_side = min(img_width, img_height) // num_squares_per_side
    
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
            part.save(os.path.join(path_level, f"part_{index + 1}.webp"))