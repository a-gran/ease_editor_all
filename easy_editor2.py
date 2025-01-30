# Импортируем модуль os для работы с операционной системой (работа с путями, создание папок и т.д.)
import os

# Импортируем необходимые классы из PyQt5 для создания графического интерфейса
from PyQt5.QtWidgets import (
    QApplication,    # Класс для создания основного приложения с графическим интерфейсом
    QWidget,        # Базовый класс для создания окон и виджетов
    QFileDialog,    # Класс для создания диалогового окна выбора файлов и папок
    QLabel,         # Класс для отображения текста или изображений
    QPushButton,    # Класс для создания кнопок
    QListWidget,    # Класс для создания списка с элементами
    QHBoxLayout,    # Класс для горизонтального расположения виджетов
    QVBoxLayout     # Класс для вертикального расположения виджетов
)

# Импортируем константу Qt.KeepAspectRatio для сохранения пропорций при масштабировании
from PyQt5.QtCore import Qt
# Импортируем QPixmap для эффективной работы с изображениями в интерфейсе
from PyQt5.QtGui import QPixmap
# Импортируем классы из библиотеки PIL для обработки изображений
from PIL import Image, ImageFilter
# Создаем основное приложение PyQt5
app = QApplication([])
# Создаем главное окно приложения
win = QWidget()
# Устанавливаем размер окна: ширина 700 пикселей, высота 500 пикселей
win.resize(700, 500)
# Устанавливаем заголовок окна
win.setWindowTitle('Easy Editor')
# Создаем метку для отображения изображения с текстом "Картинка"
lb_image = QLabel("Картинка")
# Создаем кнопку для выбора папки с надписью "Папка"
btn_dir = QPushButton("Папка")
# Создаем виджет списка для отображения файлов
lw_files = QListWidget()

# Создаем кнопки для редактирования изображений
btn_left = QPushButton("Лево")       # Кнопка для поворота влево
btn_right = QPushButton("Право")     # Кнопка для поворота вправо
btn_flip = QPushButton("Зеркало")    # Кнопка для отражения изображения
btn_sharp = QPushButton("Резкость")  # Кнопка для увеличения резкости
btn_bw = QPushButton("Ч/Б")          # Кнопка для преобразования в черно-белое

# Создаем основной горизонтальный контейнер для размещения виджетов
row = QHBoxLayout()

# Создаем два вертикальных контейнера для разделения интерфейса на колонки
col1 = QVBoxLayout()    # Левая колонка для списка файлов
col2 = QVBoxLayout()    # Правая колонка для изображения и кнопок

# Добавляем виджеты в левую колонку
col1.addWidget(btn_dir)     # Добавляем кнопку выбора папки
col1.addWidget(lw_files)    # Добавляем список файлов

# Добавляем изображение во вторую колонку, занимает 95% пространства
col2.addWidget(lb_image, 95)

# Создаем горизонтальный контейнер для кнопок инструментов
row_tools = QHBoxLayout()

# Добавляем кнопки в панель инструментов
row_tools.addWidget(btn_left)    # Добавляем кнопку поворота влево
row_tools.addWidget(btn_right)   # Добавляем кнопку поворота вправо
row_tools.addWidget(btn_flip)    # Добавляем кнопку отражения
row_tools.addWidget(btn_sharp)   # Добавляем кнопку увеличения резкости
row_tools.addWidget(btn_bw)      # Добавляем кнопку ч/б фильтра

# Добавляем панель инструментов во вторую колонку
col2.addLayout(row_tools)

# Распределяем пространство между колонками: 20% и 80%
row.addLayout(col1, 20)    # Первая колонка занимает 20% ширины
row.addLayout(col2, 80)    # Вторая колонка занимает 80% ширины

# Устанавливаем основной контейнер в окно
win.setLayout(row)

# Показываем окно приложения
win.show()

# Переменная для хранения пути к рабочей директории
workdir = ''

def filter(files, extensions):
    """Фильтрует список файлов, оставляя только файлы с указанными расширениями"""
    result = []    # Создаем пустой список для результатов
    for filename in files:    # Перебираем все файлы
        for ext in extensions:    # Перебираем все допустимые расширения
            if filename.endswith(ext):    # Если файл имеет нужное расширение
                result.append(filename)    # Добавляем его в результат
    return result    # Возвращаем отфильтрованный список

def chooseWorkdir():
    """Открывает диалог выбора рабочей директории"""
    global workdir    # Используем глобальную переменную
    workdir = QFileDialog.getExistingDirectory()    # Открываем диалог выбора папки

def showFilenamesList():
    """Показывает в списке все поддерживаемые графические файлы из выбранной папки"""
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']    # Список поддерживаемых форматов
    chooseWorkdir()    # Выбираем рабочую папку
    
    # Получаем отфильтрованный список файлов
    filenames = filter(os.listdir(workdir), extensions)

    lw_files.clear()    # Очищаем список
    for filename in filenames:    # Перебираем все подходящие файлы
        lw_files.addItem(filename)    # Добавляем имя файла в список

# Привязываем функцию showFilenamesList к клику по кнопке выбора директории
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    """Класс для работы с изображениями"""
    def __init__(self):
        self.image = None    # Текущее изображение
        self.dir = None     # Путь к папке с изображением
        self.filename = None    # Имя файла изображения
        self.save_dir = "Modified/"    # Папка для сохранения обработанных изображений

    def loadImage(self, dir, filename):
        """Загружает изображение из файла"""
        self.dir = dir    # Сохраняем путь к папке
        self.filename = filename    # Сохраняем имя файла
        image_path = os.path.join(dir, filename)    # Составляем полный путь к файлу
        self.image = Image.open(image_path)    # Открываем изображение

    def do_bw(self):
        """Преобразует изображение в черно-белое"""
        self.image = self.image.convert("L")    # Преобразуем в оттенки серого
        self.saveImage()    # Сохраняем результат
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)    # Показываем результат

    def do_left(self):
        """Поворачивает изображение влево на 90 градусов"""
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        """Поворачивает изображение вправо на 90 градусов"""
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        """Отражает изображение по горизонтали"""
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        """Увеличивает резкость изображения"""
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        """Сохраняет обработанное изображение в отдельную папку"""        
        path = os.path.join(self.dir, self.save_dir) # Создаем полный путь к папке для сохранения
        # Если папка не существует, создаем её
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)        
        image_path = os.path.join(path, self.filename) # Составляем полный путь для сохранения файла        
        self.image.save(image_path) # Сохраняем изображение

    def showImage(self, path):
        """Показывает изображение в окне программы"""
        lb_image.hide()    # Скрываем текущее изображение        
        pixmapimage = QPixmap(path) # Создаем объект QPixmap из файла        
        w, h = lb_image.width(), lb_image.height()# Получаем размеры области отображения        
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) # Масштабируем изображение с сохранением пропорций        
        lb_image.setPixmap(pixmapimage) # Устанавливаем изображение в метку        
        lb_image.show() # Показываем метку с изображением

def showChosenImage():
    """Показывает выбранное в списке изображение"""
    if lw_files.currentRow() >= 0:    # Если есть выбранный элемент
        filename = lw_files.currentItem().text()    # Получаем имя файла
        workimage.loadImage(workdir, filename)    # Загружаем изображение
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)    # Показываем изображение

# Создаем объект для обработки изображений
workimage = ImageProcessor()
# Подключаем обработчики событий к событиям интерфейса
lw_files.currentRowChanged.connect(showChosenImage)    # При выборе файла в списке
btn_bw.clicked.connect(workimage.do_bw)              # При нажатии на кнопку ч/б
btn_left.clicked.connect(workimage.do_left)          # При нажатии на кнопку поворота влево
btn_right.clicked.connect(workimage.do_right)        # При нажатии на кнопку поворота вправо
btn_sharp.clicked.connect(workimage.do_sharpen)      # При нажатии на кнопку увеличения резкости
btn_flip.clicked.connect(workimage.do_flip)          # При нажатии на кнопку отражения
# Запускаем основной цикл приложения
app.exec()