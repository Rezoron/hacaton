import os
import asyncio
import pyvips


async def init_file(file_name_data: str, size):
    if size > 1000000:
        # Ждём освобождения оперативки для дальнейших действий с большими файлами
        await asyncio.sleep(5)

    # Путь до исходного файла
    path_upload = os.path.join('uploads', ".".join(
        file_name_data[:-1]), ".".join(file_name_data))
    # Путь до сжатого
    path_dir_base = os.path.join('uploads', ".".join(file_name_data[:-1]))

    print(os.path.getsize(path_upload))

    for quality, count_title in detector_of_details(size):
        img = compress(path_upload, quality)

        path_dir = os.path.join(path_dir_base, str(count_title*count_title))

        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)

        split_image(img, count_title, path_dir)


def detector_of_details(seze):
    levels = []
    if seze > 1000:
        levels.append([50, 1])

    if seze > 6000:
        levels.append([90, 6])

    return levels


def compress(png_file_path: str, quality: int):
    image = pyvips.Image.new_from_file(png_file_path)
    resized_image = image.resize(quality/100)
    return resized_image


def split_image(img, num_squares_per_side, path_level):
    img_width, img_height = img.width, img.height

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
            part = img.crop(left, top, right, bottom)
            index += 1
            part.write_to_file(os.path.join(
                path_level, f"part_{index}.jpeg"), strip=True)
            print(os.path.join(
                path_level, f"part_{index}.webp"))
