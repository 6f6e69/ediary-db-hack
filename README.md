# db-hack

Скрипт поможет легко исправить плохие оценки, удалить замечания
и добавить похвалы от учителей в электронный дневник из 
[этого репозитория](https://github.com/devmanorg/e-diary).

## Установка

В системе должен быть установлен интерпретатор языка `Python` версии
`3.5` и выше.

```
python3 --version
```

Рекомендуется использовать 
[виртуальное окружение](https://docs.python.org/3/library/venv.html).
Выполните эти команды находясь в рабочей директории.

```
python3 -m venv env
source env/bin/activate # Unix-based
.\venv\Scripts\activate # Windows
```

Скачайте [архив](https://github.com/devmanorg/e-diary/archive/refs/heads/master.zip) 
с файлами электронного дневника и разархивируйте в рабочую директорию. 


Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей. 

```
pip install -r requirements.txt
```

Скачайте [архив](https://github.com/6f6e69/ediary-db-hack/archive/refs/heads/main.zip) 
с файлами скрипта и разархивируйте в рабочую директорию.

Добудьте файл с актуальной базой данных, который имеет расширение `.sqlite3` и 
поместите его в рабочую директорию.

Если название добытой базы отличается от `schoolbase.sqlite3` то отредактируйте файл 
`projects/settings.py`, заменив название базы на свое.

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('DATABASE_NAME', 'ваше_название.sqlite3'),
    }
}
```

## Использование

При запуске скрипта всегда нужно указывать аргумент `--schoolkid` с
максимально полными Фамилией Именем Отчеством. Если данные неполные
то будет выполнена попытка найти максимально похожего ученика.

### Удаление плохих оценок

Все двойки и тройки будут заменены на пятерки.

```
python3 --schoolkid 'Vasia Ivanov' --fix-bad-marks
```

### Удаление замечаний

Все замечания ученику будут удалены.

```
python3 --schoolkid 'Vasia Ivanov' --rm-chastisements
```

### Добавление похвалы

Ученику будет добавлена случайная похвала из файла `commendations.txt` к 
последнему уроку по предмету.

```
python3 --schoolkid 'Vasia Ivanov' add_commendation --subject Музыка
```

Вы можете указать свой файл с фразами для похвалы через параметр `--file-path`
или дополнить имеющийся. Каждая фраза начинается с новой строки.

```
python3 --schoolkid 'Vasia Ivanov' add_commendation --subject Математика --file-path 'my_commendations.txt'
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).