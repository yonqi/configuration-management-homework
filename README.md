# configuration-management-homework
Домашки по конфигурационному управлению
## Вариант 10
### Задание 1

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата zip. Эмулятор должен работать в режиме GUI.
Конфигурационный файл имеет формат json и содержит:

  • Путь к архиву виртуальной файловой системы.
  
  • Путь к стартовому скрипту.
  
Стартовый скрипт служит для начального выполнения заданного списка команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
  1. wc.
  2. uniq.
Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 2 теста.

#### Общее описание

Этот файл представляет собой реализацию эмулятора командной оболочки (shell) на языке Python с использованием графического интерфейса пользователя (GUI) на основе библиотеки Tkinter. Эта программа создает эмулятор командной оболочки с графическим интерфейсом, который позволяет пользователю выполнять основные команды управления файлами и навигации в файловой системе, извлеченной из ZIP-архива. Пользователь может взаимодействовать с эмулятором через интерфейс, и все команды обрабатываются в фоновом режиме, предоставляя результаты в удобочитаемом формате.

Основные функции и особенности кода следующие:

##### Класс ShellEmulator
1. `def __init__(self, config_file):`
    - Загружает конфигурацию из указанного JSON-файла. Инициализирует виртуальную файловую систему, извлекая её из заданного ZIP-архива. Сохраняет историю команд. Выполняет команд из стартового скрипта, если он указан.
2. `def load_config(self, config_file):`
    - Открывает и считывает конфигурационный файл в формате JSON. Загружает значения username, hostname, filesystem и startup_script из конфигурации, которые используются для настройки командной строки в интерфейсе.
3. `def init_filesystem(self, zip_path):`
    - Принимает путь к ZIP-архиву, который содержит виртуальную файловую систему. Извлекает содержимое ZIP-архива в временную папку /tmp/virtual_fs. Устанавливает текущее рабочее каталоги на извлеченную директорию.
4. `def execute_startup_script(self, script_path):`
    - Принимает путь к файлу скрипта. Если файл существует, считывает и выполняет команды, указанные в нем, с помощью метода run_command. Игнорирует пустые строки в скрипте.
5. `def run_command(self, command):`
    - Принимает строку команды от пользователя и добавляет её в историю. Разбивает команду на части (аргументы). Определяет, какую команду нужно выполнить, и вызывает соответствующий метод:
        - `ls`: вызывает метод ls_command().
        - `cd`: вызывает метод cd_command(), передавая аргумент пути, если он указан.
        - `exit`: возвращает строку "exit" для завершения.
        - `wc`: вызывает wc_command(filename).
        - `uniq`: вызывает uniq_command(filename).
    - Если команда не распознана, возвращает сообщение об ошибке.
6. `def ls_command(self):`
    - Возвращает список файлов и каталогов из текущего рабочего каталога, установленного на self.current_dir, и выводит их в виде строки, разделенной символом новой строки (\n).
7. `def cd_command(self, path):`
    - Принимает строку path и пытается изменить текущий рабочий каталог. Если передан путь, он объединяется с текущим путем, и проверяется, существует ли указанный каталог. Если каталог существует, обновляет self.current_dir и возвращает строку об успешном изменении. Если каталог не найден, возвращает сообщение об ошибке.
8. `def wc_command(self, filename):`
    - Принимает строку filename и проверяет его существование. Если файл существует, считает количество строк, слов и символов. Возвращает эти данные и имя файла.
9. `def uniq_command(self, filename):`
    - Принимает строку filename и проверяет его существование. Если файл существует, считывает все строки, удаляет дубликаты, сортирует их и возвращает уникальные строки.
##### Класс ShellGUI
1. `def __init__(self, root, emulator):`
    - Инициализирует графический интерфейс, создавая основное окно Tkinter. Устанавливает заголовок окна и сохраняет ссылку на экземпляр ShellEmulator, который используется для выполнения команд. Создает область вывода (ScrolledText) для отображения результатов выполнения команд. Создает поле ввода (Entry) для ввода команд пользователем и привязывает событие нажатия клавиши "Enter" к методу enter_command.
2. `def enter_command(self, event):`
    - Вызывается при нажатии клавиши "Enter" в поле ввода. Получает команду из поля ввода и очищает поле. Вызывает метод run_command у экземпляра ShellEmulator, передавая введенную команду, и получает результат выполнения команды. Если возвращаемое значение равно "exit", закрывает окно и завершает приложение. В противном случае обновляет область вывода, добавляя текстовые результаты выполнения команды и новый промпт.
3. `def update_output(self, text):`
    - Принимает строку text и добавляет её в конец области вывода. Обеспечивает автоматическую прокрутку области вывода, чтобы всегда показывать последние сообщения.
##### Вход в программу
  `if __name__ == "__main__":` 
  
  Проверяет, выполняется ли файл как основная программа. Если это так, инициализирует основной интерфейс, создавая экземпляр ShellEmulator с заданным конфигурационным файлом config.json, а затем создает и запускает интерфейс ShellGUI.

#### Настройки

Конфигурационный файл config.json поддерживает следующие параметры:

- `username`: строка, представляющая имя пользователя в командной строке.
- `hostname`: строка, представляющая имя хоста в командной строке.
- `filesystem`: путь к ZIP-архиву, содержащему виртуальную файловую систему.
- `startup_script`: путь к текстовому файлу, содержащему команды, которые будут выполняться автоматически при старте эмулятора.

#### Тест

![image](https://github.com/user-attachments/assets/cfb2848b-dd4c-490a-bebd-87b1b459d2df)
![image](https://github.com/user-attachments/assets/4cde425e-1c4c-4a32-b614-75dbb6384d89)



