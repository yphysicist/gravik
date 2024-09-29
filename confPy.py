import tkinter as tk
from tkinter import filedialog
import configparser
import os
import ctypes

def Title():
    """Устанавливает заголовок консоли и выводит информацию."""
    ctypes.windll.kernel32.SetConsoleTitleW("ПММ УЧЕТА ИЗМЕНЕНИЙ ПАРАМЕТРОВ ГПЗ ВО ВРЕМЕНИ")
    print("\n")
    print('===================================================================')
    print('*    ПРОГРАММНО-МАТЕМАТИЧЕСКАЯ МОДЕЛЬ УТОЧНЕНИЯ ФУНДАМЕНТАЛЬНЫХ   *')
    print('*      АСТРОНОМО-ГЕОДЕЗИЧЕСКИХ ПАРАМЕТРОВ С УЧЕТОМ ИЗМЕНЕНИЙ      *')
    print('*            ПАРАМЕТРОВ ГПЗ ВО ВРЕМЕНИ (ПММ "ГРАВИКА")            *')
    print('===================================================================')

def SelectTask():
    """Позволяет выбрать задачу из консоли."""
    print('-------------------------------------------------------------------')
    print('Выбери задачу:                                                     ')
    print('-------------------------------------------------------------------')
    print('Прогноз изменений параметров планетарного ГПЗ во времени        - 1')
    print('-------------------------------------------------------------------')
    iPrompt = "Выбор(0 - завершение работы)?                                   ->"
    
    while True:
        iTask = input(iPrompt)
        try:
            iTask = int(iTask)
        except ValueError:
            iTask = int(-1)
        if iTask < 0 or iTask > 1:
            print("Ошибка выбора задачи!")
            continue
        else:
            break
    return iTask

def get_config_file():
    """Функция для выбора конфигурационного файла через окно Windows."""
    print("Инициализация окна выбора файла...")

    try:
        root = tk.Tk()
        root.withdraw()  # Скрываем главное окно tkinter
        
        # Создаем скрытое окно
        root.after(200, lambda: root.deiconify())  # Показать окно через 200 мс
        root.lift()  # Поднимаем окно на передний план
        root.attributes('-topmost', True)  # Окно всегда поверх остальных
        root.focus_force()  # Перемещаем фокус на окно
        
        # Диалог выбора файла
        config_file = filedialog.askopenfilename(
            title="Выберите конфигурационный файл",
            filetypes=[("Config files", "*.txt"), ("All files", "*.*")]
        )

        if config_file:
            print(f"Файл выбран: {config_file}")
        else:
            print("Файл не выбран.")

        root.update()  # Обновляем окно
        root.destroy()  # Закрываем окно

        return config_file

    except Exception as e:
        print(f"Ошибка при выборе файла: {e}")
        return None

def parse_config(config_file):
    """Функция для чтения конфигурационного файла и извлечения нужных данных."""
    config = configparser.ConfigParser()
    
    # Пробуем открыть файл с кодировкой cp1251
    with open(config_file, encoding='cp1251') as f:
        config.read_file(f)

    # Извлечение значений из раздела [Задание]
    target_file = config.get('Задание', 'Целевой файл')
    reference_file = config.get('Задание', 'Опорный файл')
    additional_files = [config.get('Задание', f'Дополнительный файл {i}') for i in range(1, 6)]

    # Извлечение значений из раздела [Настройки]
    write_to_file = config.get('Настройки', 'Запись в файл (y/n)')
    output_file = config.get('Настройки', 'Имя файла')

    return target_file, reference_file, additional_files, write_to_file, output_file

def build_command(target_file, reference_file, additional_files, output_file):
    """Функция для формирования команды."""
    # Фильтрация дополнительных файлов, если они не 'no'
    additional_files_filtered = [file for file in additional_files if file.lower() != 'no']
    
    # Формирование команды
    command = f"python predict.py --csv {output_file} {target_file} {reference_file} {' '.join(additional_files_filtered)}"
    
    return command

def main():
    """Основная программа."""
    while True:
        Title()  # Устанавливаем заголовок и выводим меню
        
        # Пользователь выбирает задачу
        iTask = SelectTask()
        if iTask == 0:
            os.system("pause")
            exit()
        
        # Если выбрана задача 1 - выполняем сценарий с конфигурационным файлом
        if iTask == 1:
            # Открываем окно выбора конфигурационного файла
            config_file = get_config_file()
            
            if not config_file:
                print("Конфигурационный файл не выбран.")
                continue  # Переход к новому выбору задачи

            # Парсим конфигурационный файл
            target_file, reference_file, additional_files, write_to_file, output_file = parse_config(config_file)
            
            # Формируем команду
            command = build_command(target_file, reference_file, additional_files, output_file)

            # Вывод команды
            print(f"Сформированная команда: {command}")

            # Выполнение команды, если включена опция записи
            if write_to_file.lower() == 'y':
                os.system(command)
            else:
                print("Запись в файл отключена.")

        # Продолжаем выполнение программы
        continue

if __name__ == "__main__":
    main()
