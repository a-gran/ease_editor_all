# Импортируем основной модуль для работы с изображениями
from PIL import Image
# Импортируем подмодуль с фильтрами (хотя в данном коде не используется)
from PIL import ImageFilter

class ImageEditor():
    def __init__(self, filename):
        # Сохраняем имя файла
        self.filename = filename
        # Создаем переменную для хранения оригинального изображения
        self.original = None
        # Создаем список для хранения измененных версий изображения
        self.changed = list()

    def open(self):
        try:
            # Пытаемся открыть изображение по указанному пути
            self.original = Image.open(self.filename)
        except:
            # Выводим сообщение об ошибке, если файл не найден
            print('Файл не найден!')
        # Показываем оригинальное изображение
        self.original.show()

    def do_left(self):
        # Отражаем изображение по горизонтали
        rotated = self.original.transpose(Image.FLIP_LEFT_RIGHT)
        # Добавляем измененное изображение в список
        self.changed.append(rotated)

        # Разделяем имя файла по точке для создания нового имени
        temp_filename = self.filename.split('.')
        # Создаем новое имя файла с порядковым номером изменения
        new_filename = temp_filename[0] + str(len(self.changed)) + '.jpg'
        # Сохраняем отраженное изображение
        rotated.save(new_filename)

    def do_cropped(self):
        # Задаем координаты для обрезки (левый верхний и правый нижний углы)
        box = (250, 100, 600, 400)
        # Обрезаем изображение по заданным координатам
        cropped = self.original.crop(box)
        # Добавляем обрезанное изображение в список изменений
        self.changed.append(cropped)

        # Создаем новое имя файла для обрезанного изображения
        temp_filename = self.filename.split('.')
        new_filename = temp_filename[0] + str(len(self.changed)) + '.jpg'
        # Сохраняем обрезанное изображение
        cropped.save(new_filename)
# Создаем экземпляр класса с именем файла
MyImage = ImageEditor('original.jpg')
# Открываем изображение
MyImage.open()
# Отражаем изображение по горизонтали
MyImage.do_left()
# Обрезаем изображение
MyImage.do_cropped()
# Показываем все измененные версии изображения
for im in MyImage.changed:
    im.show()