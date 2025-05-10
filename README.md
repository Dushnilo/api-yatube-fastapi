# Yatube Social Network

## Description
The **api_yatube** project is a REST API service that allows making requests to the **Yatube** social network. With this project, users can create personal diaries, follow other users, subscribe to them, and leave comments.

### Technologies Used
- Python
- FastAPI

### Installation and Running the Project

1. Clone the repository and navigate to it in the command line:

   ```bash
   git clone https://github.com/Dushnilo/api_yatube.git
   cd api_yatube
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Update the project's package manager:

   ```bash
   python -m pip install --upgrade pip
   ```

4. Install dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

5. Navigate to the directory containing the `main.py` file:

   ```bash
   cd yatube_api
   ```

6. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

7. Fill in `.env` with actual values:

   ```env
   SECRET_KEY=your_secret_key_here
   DB_PASSWORD=your_database_password
   ```

8. Run the project:

   ```bash
   uvicorn main:app
   ```

### Features and Example Requests
Unauthorized users can only view content. To add, modify, or delete data, registration is required. All possible request and response examples, as well as access rights, are described in the ReDoc documentation.

#### Viewing Documentation
To view the documentation on your local machine after starting the service:

```bash
uvicorn main:app
```

Navigate to the following address:

```
http://127.0.0.1:8000/redoc/
```

#### Access to Admin Panel
The admin panel is available at:

```
http://127.0.0.1:8000/admin/
```

- **Login**: `root@email.com`
- **Password**: `testpass123`



---



# Социальная сеть Yatube

## Описание
Проект **api_yatube** — это REST API сервис, позволяющий делать запросы к социальной сети **Yatube**. Благодаря этому проекту можно создавать личные дневники, следить за другими пользователями, подписываться на них и оставлять комментарии.

### Использованные технологии
- Python
- FastAPI

### Установка и запуск проекта

1. Клонируйте репозиторий и перейдите в него в командной строке:

   ```bash
   git clone https://github.com/Dushnilo/api_yatube.git
   cd api_yatube
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Обновите пакетный менеджер проекта:

   ```bash
   python -m pip install --upgrade pip
   ```

4. Установите зависимости из файла `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

5. Перейдите в директорию с файлом `main.py`:

   ```bash
   cd yatube_api
   ```

6. Скопируйте `.env.example` в `.env`:

   ```bash
   cp .env.example .env
   ```

7. Заполните `.env` реальными значениями:

   ```env
   SECRET_KEY=your_secret_key_here
   DB_PASSWORD=your_database_password
   ```

8. Запустите проект:

   ```bash
   uvicorn main:app
   ```

### Возможности и примеры запросов
Неавторизованным пользователям доступен только просмотр контента. Для добавления, изменения и удаления данных необходимо зарегистрироваться. Все возможные примеры запросов и ответов, а также права доступа описаны в документации в формате ReDoc.

#### Просмотр документации
Для просмотра документации на локальном компьютере после запуска сервиса:

```bash
uvicorn main:app
```

Перейдите по адресу:

```
http://127.0.0.1:8000/redoc/
```

#### Доступ к админке
Админка доступна по адресу:

```
http://127.0.0.1:8000/admin/
```

- **Логин**: `root@email.com`
- **Пароль**: `testpass123`
<!--  -->
