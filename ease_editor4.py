# Импортируем модули для работы с файлами, GUI и обработки изображений
import os  # Для работы с файловой системой

from PyQt5.QtWidgets import (  # Импорт необходимых виджетов из PyQt5
    QApplication,  # Класс основного приложения
    QWidget,      # Базовый класс для окон
    QFileDialog,  # Диалог выбора файлов
    QLabel,       # Для отображения изображений
    QPushButton,  # Для создания кнопок
    QListWidget,  # Для списка файлов
    QHBoxLayout,  # Горизонтальное расположение
    QVBoxLayout   # Вертикальное расположение
)
from PyQt5.QtCore import Qt  # Константы Qt
from PyQt5.QtGui import QPixmap  # Для работы с изображениями в PyQt
from PIL import Image, ImageFilter  # Библиотека для обработки изображений

# Создание основного приложения
app = QApplication([])  # Инициализация приложения
win = QWidget()  # Создание главного окна
win.resize(700, 500)  # Установка размера окна
win.setWindowTitle('Easy Editor')  # Заголовок окна

# Создание элементов интерфейса
lb_image = QLabel("Картинка")  # Метка для изображения
btn_dir = QPushButton("Папка")  # Кнопка выбора папки
lw_files = QListWidget()  # Список файлов
btn_left = QPushButton("Лево")  # Кнопка поворота влево
btn_right = QPushButton("Право")  # Кнопка поворота вправо
btn_flip = QPushButton("Зеркало")  # Кнопка отражения
btn_sharp = QPushButton("Резкость")  # Кнопка увеличения резкости
btn_bw = QPushButton("Ч/Б")  # Кнопка ч/б преобразования

# Создание layout'ов
row = QHBoxLayout()  # Основной горизонтальный layout
col1 = QVBoxLayout()  # Левая колонка
col2 = QVBoxLayout()  # Правая колонка
row_tools = QHBoxLayout()  # Панель инструментов

# Размещение элементов
col1.addWidget(btn_dir)  # Добавление кнопки выбора папки
col1.addWidget(lw_files)  # Добавление списка файлов
col2.addWidget(lb_image, 95)  # Добавление области изображения

# Добавление кнопок в панель инструментов
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)  # Добавление панели инструментов

# Настройка пропорций layout'а
row.addLayout(col1, 20)  # Левая колонка занимает 20%
row.addLayout(col2, 80)  # Правая колонка занимает 80%
win.setLayout(row)  # Установка layout'а для окна

workdir = ''  # Путь к рабочей директории

def filter(files, extensions):
    """Фильтрует список файлов, оставляя только файлы с указанными расширениями"""
    result = []    # Создаем пустой список для результатов
    for filename in files:    # Перебираем все файлы
        for ext in extensions:    # Перебираем все допустимые расширения
            if filename.endswith(ext):    # Если файл имеет нужное расширение
                result.append(filename)    # Добавляем его в результат
    return result    # Возвращаем отфильтрованный список

def chooseWorkdir():
    """Выбор рабочей директории"""
    global workdir  # Используем глобальную переменную
    workdir = QFileDialog.getExistingDirectory() # Открываем диалог выбора папки

def showFilenamesList():
    """Отображение списка файлов"""
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']  # Поддерживаемые форматы
    chooseWorkdir()  # Выбор директории
    filenames = filter(os.listdir(workdir), extensions)  # Фильтрация файлов
    lw_files.clear()  # Очистка списка
    lw_files.addItems(filenames)  # Добавление файлов в список

class ImageProcessor():
    """Класс для обработки изображений"""
    def __init__(self):
        self.image = None  # Оригинальное изображение
        self.dir = None    # Путь к директории
        self.filename = None  # Имя файла
        self.current_image = None  # Текущее обработанное изображение

    def loadImage(self, dir, filename):
        """Загрузка изображения"""
        self.dir = dir  # Сохраняем путь
        self.filename = filename  # Сохраняем имя файла
        image_path = os.path.join(dir, filename)  # Полный путь к файлу
        self.image = Image.open(image_path).convert('RGB')  # Открываем и конвертируем в RGB
        self.current_image = self.image.copy()  # Создаем копию для обработки

    def _save_and_show(self, operation_name):
        """Сохранение и отображение результата"""
        base_name = os.path.splitext(self.filename)[0]  # Имя файла без расширения
        folder_path = os.path.join(self.dir, base_name)  # Путь к папке сохранения
        if not os.path.exists(folder_path):  # Если папки нет
            os.makedirs(folder_path)  # Создаем её
        
        # Формируем имя нового файла
        new_filename = f"{operation_name}_{self.filename}"
        # Проверяем расширение файла
        if not new_filename.lower().endswith('.jpg'):
            new_filename = f"{os.path.splitext(new_filename)[0]}.jpg"
        save_path = os.path.join(folder_path, new_filename)  # Полный путь сохранения
        
        # Если операция - черно-белое преобразование
        if operation_name == 'bw':
            self.current_image = self.current_image.convert('L')  # Конвертируем в ч/б
        self.current_image.save(save_path, 'JPEG', quality=95)  # Сохраняем как JPEG
        self.showImage(save_path)  # Показываем результат

    def do_bw(self):
        """Черно-белое преобразование"""
        if self.current_image:  # Если есть изображение
            self.current_image = self.image.copy().convert('L')  # Создаем ч/б копию
            self._save_and_show('bw')  # Сохраняем и показываем

    def do_left(self):
        """Поворот влево"""
        if self.current_image:
            self.current_image = self.image.copy().transpose(Image.ROTATE_90)
            self._save_and_show('left')

    def do_right(self):
        """Поворот вправо"""
        if self.current_image:
            self.current_image = self.image.copy().transpose(Image.ROTATE_270)
            self._save_and_show('right')

    def do_flip(self):
        """Отражение по горизонтали"""
        if self.current_image:
            self.current_image = self.image.copy().transpose(Image.FLIP_LEFT_RIGHT)
            self._save_and_show('flip')

    def do_sharpen(self):
        """Увеличение резкости"""
        if self.current_image:
            self.current_image = self.image.copy().filter(ImageFilter.SHARPEN)
            self._save_and_show('sharp')

    def showImage(self, path):
        """Отображение изображения в интерфейсе"""
        lb_image.hide()  # Скрываем текущее изображение
        pixmap = QPixmap(path)  # Создаем объект изображения
        w, h = lb_image.width(), lb_image.height()  # Получаем размеры области
        # Масштабируем с сохранением пропорций
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmap)  # Устанавливаем изображение
        lb_image.show()  # Показываем изображение

def showChosenImage():
    """Отображение выбранного изображения"""
    if lw_files.currentRow() >= 0:  # Если выбран файл
        filename = lw_files.currentItem().text()  # Получение имени файла
        workimage.loadImage(workdir, filename)  # Загрузка изображения
        workimage.showImage(os.path.join(workdir, filename))  # Отображение

# Создание обработчика изображений
workimage = ImageProcessor()

# Привязка обработчиков событий
btn_dir.clicked.connect(showFilenamesList)  # Клик по кнопке выбора директории
lw_files.currentRowChanged.connect(showChosenImage)  # Выбор файла в списке
btn_bw.clicked.connect(workimage.do_bw)  # Преобразование в ч/б
btn_left.clicked.connect(workimage.do_left)  # Поворот влево
btn_right.clicked.connect(workimage.do_right)  # Поворот вправо
btn_sharp.clicked.connect(workimage.do_sharpen)  # Увеличение резкости
btn_flip.clicked.connect(workimage.do_flip)  # Отражение

# Запуск приложения
# Показываем окно приложения
win.show()
app.exec()  # Запуск цикла обработки событий