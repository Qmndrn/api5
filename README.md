# Скрипты для работы с Google Drive API

## Описание

Набор Python-скриптов для управления файлами на Google Drive: создание папок, загрузка и скачивание файлов, получение публичных ссылок. Все скрипты используют официальный Google Drive API v3 и работают через командную строку.

## Структура проекта

```
project/
│
├── auth.py            # Авторизация и создание сервиса Google Drive
├── create_folder.py   # Создание папок на Google Drive
├── upload_files.py    # Загрузка файлов на Google Drive
├── download.py        # Скачивание файлов с Google Drive
├── get_links.py       # Получение публичных ссылок на файлы
├── main.py            # Главный скрипт (объединяет весь функционал)
└── client_secret_...json  # Файл с ключами от Google API (ваш)
```

---

## Установка

### 1. Скачайте проект

```bash
cd ваш-репозиторий
git clone https://github.com/Qmndrn/api5.git
```

### 2. Установите зависимости

```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```
или

```bash
pip install -r requirements.txt
```

---

## Настройка Google API (обязательно перед первым запуском)

Перед использованием скриптов нужно получить файл с ключами от Google.

### Шаг 1 — Создайте проект в Google Cloud Console

1. Откройте [console.cloud.google.com](https://console.cloud.google.com).
2. Войдите в свой Google-аккаунт.
3. Нажмите на выпадающий список проектов вверху страницы → **"Новый проект"**.
4. Введите любое название (например, `MyDriveProject`) и нажмите **"Создать"**.

### Шаг 2 — Включите Google Drive API

1. В левом меню выберите **"API и сервисы"** → **"Библиотека"**.
2. В строке поиска введите `Google Drive API`.
3. Кликните на результат и нажмите **"Включить"**.

### Шаг 3 — Создайте учётные данные (credentials)

1. В левом меню перейдите в **"API и сервисы"** → **"Учётные данные"**.
2. Нажмите **"Создать учётные данные"** → **"Идентификатор клиента OAuth"**.
3. Если система попросит настроить экран согласия — нажмите **"Настроить экран согласия"**:
   - Выберите тип **"Внешний"** → **"Создать"**.
   - Введите любое имя приложения, ваш email и нажмите **"Сохранить и продолжить"** (остальные поля можно пропустить).
4. Вернитесь к созданию учётных данных. Тип приложения выберите **"Приложение для ПК"**.
5. Нажмите **"Создать"**.
6. Скачайте JSON-файл (кнопка со стрелкой вниз) — это и есть ваш `client_secret_....json`.

### Шаг 4 — Укажите путь к файлу в `auth.py`

Откройте файл `auth.py` и замените путь в переменной `CLIENT_SECRET_FILE` на путь к вашему скачанному JSON-файлу:

```python
CLIENT_SECRET_FILE = "путь/к/вашему/client_secret_....json"
```

Пример для Windows:
```python
CLIENT_SECRET_FILE = "C:/Users/Ваше_имя/Downloads/client_secret_....json"
```

Пример для Linux/Mac:
```python
CLIENT_SECRET_FILE = "/home/ваше_имя/Downloads/client_secret_....json"
```

### Шаг 5 — Первый запуск и авторизация

При первом запуске любого скрипта автоматически откроется браузер с окном авторизации Google. Нужно:

1. Выбрать свой аккаунт Google.
2. Нажать **"Продолжить"** (Google может показать предупреждение — это нормально для непроверенных приложений, нажмите "Дополнительно" → "Перейти к ...").
3. Разрешить доступ к Google Drive.

После этого в папке проекта появится файл `token_drive` — он сохраняет авторизацию, чтобы не входить каждый раз заново.

---

## Как узнать ID папки на Google Drive

аргумент `--parent` — это ID папки на Google Drive. Чтобы его узнать:

1. Откройте [drive.google.com](https://drive.google.com) в браузере.
2. Перейдите в нужную папку.
3. Посмотрите на адресную строку — в конце URL будет ID папки:

```
https://drive.google.com/drive/folders/1nR8uuxZgoPQQf3STWPUegLn-meb34gxo
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        Это и есть ID папки
```

---

## Использование

### `main.py` — Главный скрипт (полный функционал)

Создаёт папку `Projects/Python` на Drive, загружает файлы, выдаёт публичные ссылки и позволяет скачивать файлы.

```bash
# Запуск с настройками по умолчанию (создаст папку Projects в корне Drive)
python main.py

# Указать свою папку как родительскую (по ID)
python main.py --parent 1nR8uuxZgoPQQf3STWPUegLn-meb34gxo

# Указать другое имя для создаваемой папки
python main.py --folder_name МоиПроекты
```

---

### `create_folder.py` — Создание папок

Создаёт папку с указанным именем в корне Drive, а внутри неё — вложенную папку `Python`.

```bash
# Создать папку Projects в корне Drive (и Python внутри)
python create_folder.py

# Создать папку с другим именем
python create_folder.py --folder_name МоиФайлы

# Создать папку Python внутри существующей папки по ID
python create_folder.py --parent 1nR8uuxZgoPQQf3STWPUegLn-meb34gxo
```

---

### `upload_files.py` — Загрузка файлов

Загружает файлы в указанную папку на Google Drive. Если файл с таким именем уже существует — перезаписывает его.

> Перед использованием откройте `upload_files.py` и укажите актуальные пути к файлам в переменных `file_paths` и `file_names`.

```bash
# Загрузить файлы в папку по ID
python upload_files.py --parent 1nR8uuxZgoPQQf3STWPUegLn-meb34gxo
```

---

### `download.py` — Скачивание файлов

Показывает список файлов в папке и позволяет скачать нужный по имени.

> Создайте папку `downloads` в директории проекта перед запуском, или скрипт создаст её сам.

```bash
# Скачать файл из папки по ID
python download.py --parent 1nR8uuxZgoPQQf3STWPUegLn-meb34gxo
```

После запуска скрипт покажет список файлов и спросит, какой скачать:

```
файл: photo.webp
файл: ggdrive.py
Введите имя файла для скачивания: photo.webp
Download 100%.
Хотите продолжить? нет
```

---

### `get_links.py` — Получение публичных ссылок

Делает все файлы в папке публично доступными (для чтения) и выводит ссылки на них.

```bash
# Получить ссылки на файлы в папке по ID
python get_links.py --parent 1nR8uuxZgoPQQf3STWPUegLn-meb34gxo
```

Вывод будет выглядеть так:

```
Ссылка на файл photo.webp: https://drive.google.com/file/d/XXXX/view?usp=drivesdk
Ссылка на файл ggdrive.py: https://drive.google.com/file/d/YYYY/view?usp=drivesdk
```

---

## Возможные ошибки и их решение

**`ModuleNotFoundError: No module named 'googleapiclient'`**
→ Установите зависимости: `pip install google-api-python-client google-auth-oauthlib`

**`FileNotFoundError: client_secret_....json`**
→ Проверьте путь к JSON-файлу в `auth.py` в переменной `CLIENT_SECRET_FILE`.

**`Token has been expired or revoked`**
→ Удалите файл `token_drive` из папки проекта и запустите скрипт снова — авторизация пройдёт заново.

**`HttpError 403: The caller does not have permission`**
→ Убедитесь, что вы авторизовались в том же аккаунте, в котором находится папка на Drive.

**Браузер не открывается при авторизации**
→ Скопируйте ссылку из терминала вручную и откройте её в браузере.

---

## Цель проекта

Код написан в образовательных целях. Проект показывает, как:

- Работать с Google Drive API через официальный Python-клиент (`google-api-python-client`)
- Реализовывать OAuth 2.0 авторизацию (`google-auth-oauthlib`)
- Загружать и скачивать файлы через API (`MediaFileUpload`, `MediaIoBaseDownload`)
- Управлять правами доступа и получать публичные ссылки
- Работать с аргументами командной строки (`argparse`)
