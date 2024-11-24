import os
import asyncio
import pyvips

async def init_file(file_name_data: str, size):
    if size > 1000000:
        # Ждём освобождения оперативки для дальнейших действий с большими файлами
        await asyncio.sleep(2)

    # Путь до исходного файла
    path_upload = os.path.join('uploads', ".".join(
        file_name_data[:-1]), ".".join(file_name_data))
    # Путь до сжатого
    path_dir_base = os.path.join('uploads', ".".join(file_name_data[:-1]))

    print(os.path.getsize(path_upload))
    
    image = pyvips.Image.new_from_file(path_upload)

    for count_title, quality in detector_of_details(image.width, image.height):
    
        img = compress(image, quality)

        path_dir = os.path.join(path_dir_base, str(count_title*count_title))

        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)

        split_image(img, count_title, path_dir)

def detector_of_details(width, height, limit=65535):

    #Значение можно изменять в зависимости от задач
    count_title_step = 3 
    count_levels = 3
    ###############################################

    levels=[]
    curent_title = 1
    max_scale = 1
    if width >= limit and height >= limit:
        max_scale = min(limit / width, limit / height)
    scale_step = max_scale / count_levels
    
    

    for level in range(count_levels, 0, -1):
        if max_scale-scale_step*level ==0:
            qual=0.2
        else:
            qual=max_scale-scale_step*level
        levels.append([curent_title, qual])
        
        curent_title += count_title_step    
   
    return levels


def compress(img, quality: float):
    return img.resize(quality)


def split_image(img, num_squares_per_side, path_level):
    img_width, img_height = img.width, img.height
    tile_width = (img_width + num_squares_per_side - 1) // num_squares_per_side  # Округление вверх
    tile_height = (img_height + num_squares_per_side - 1) // num_squares_per_side  # Округление вверх

    for row in range(num_squares_per_side):
        for col in range(num_squares_per_side):
            # Вычисляем координаты для обрезки
            left = col * tile_width
            top = row * tile_height
            
            # Обновляем правую и нижнюю границы с учетом размеров изображения
            right = min(left + tile_width, img_width)
            bottom = min(top + tile_height, img_height)

            # Если тайл не имеет размера, пропускаем его
            if right <= left or bottom <= top:
                continue
            part = img.crop(left, top, right - left, bottom - top)

            # Сохраняем часть изображения в файл
            part.write_to_file(os.path.join(path_level, f"part_{row}_{col}.jpeg"), Q=90)
            print(os.path.join(path_level, f"part_{row}_{col}.jpeg"))
