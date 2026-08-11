# Конспект: валидация + авторизация для pet_project_flask

> Стиль как в **SecondLife** (`webapp/user/`)  
> Теория/задачки — в чате **Чат по ООП**  
> Практика в коде — в чате **My_pet_project_Flask**

Скопируй этот файл к себе:
`C:\projects\learning\pet_project_flask\docs\FLASK_VALIDATION_AUTH_THEORY.md`

---

## Оглавление

1. [Зачем это нужно](#1-зачем-это-нужно)
2. [Валидация: два уровня](#2-валидация-два-уровня)
3. [Ручная валидация (с чего начать)](#3-ручная-валидация-с-чего-начать)
4. [Flask-WTF (как в SecondLife)](#4-flask-wtf-как-в-secondlife)
5. [Пароли: никогда не хранить как есть](#5-пароли-никогда-не-хранить-как-есть)
6. [Модель User](#6-модель-user)
7. [Flask-Login: кто сейчас залогинен](#7-flask-login-кто-сейчас-залогинен)
8. [Регистрация](#8-регистрация)
9. [Логин / логаут](#9-логин--логаут)
10. [login_required — защита маршрутов](#10-login_required--защита-маршрутов)
11. [Связка с объявлениями (Item)](#11-связка-с-объявлениями-item)
12. [Что поставить](#12-что-поставить)
13. [Что почитать перед следующей сессией](#13-что-почитать-перед-следующей-сессией)
14. [Как подготовиться](#14-как-подготовиться)
15. [План задачек (чат ООП)](#15-план-задачек-чат-ооп)
16. [План внедрения (чат pet-проекта)](#16-план-внедрения-чат-pet-проекта)
17. [Шпаргалка](#17-шпаргалка)

---

## 1. Зачем это нужно

**Сейчас** в pet-проекте:
- `/add` может открыть кто угодно
- в форму можно отправить пустое имя или `price=-10`
- непонятно, *чей* это товар

| Проблема | Решение |
|----------|---------|
| Мусор в БД | **валидация** формы |
| Кто угодно добавляет/удаляет | **авторизация** (логин) |
| Пароль в открытом виде | **хеширование** |
| «Это мой товар» | связь `Item.user_id` → `User.id` (позже) |

---

## 2. Валидация: два уровня

| Уровень | Где | Пример |
|---------|-----|--------|
| В браузере | HTML `required`, `type="number"` | удобство, легко обойти |
| На сервере | Python в Flask | **обязательно** — этому верим |

Правило: **всегда проверяй на сервере**.

Два способа на сервере:

1. **Вручную** — `if not name: ...` (проще для старта)
2. **Flask-WTF** — классы форм + валидаторы (стиль SecondLife)

Для pet-проекта рекомендуемый путь:
1. сначала ручная валидация на `/add`
2. потом формы регистрации/логина через Flask-WTF
3. потом Flask-Login

---

## 3. Ручная валидация (с чего начать)

В `add_item` после чтения формы:

```python
name = request.form.get("name", "").strip()
price_raw = request.form.get("price", "").strip()
errors = []

if not name:
    errors.append("Укажите название")

try:
    price = int(price_raw)
    if price <= 0:
        errors.append("Цена должна быть > 0")
except ValueError:
    errors.append("Цена должна быть числом")

if errors:
    return render_template("add.html", errors=errors, name=name, price=price_raw)

item = Item(name=name, price=price)
db_session.add(item)
db_session.commit()
return redirect(url_for("home"))
```

В шаблоне:

```jinja
{% for error in errors %}
  <p style="color:red">{{ error }}</p>
{% endfor %}
```

Это ты уже частично умеешь из `@property` (проверка `price > 0`) — та же идея, только на входе из формы.

---

## 4. Flask-WTF (как в SecondLife)

### Зачем
- валидаторы в одном месте
- CSRF-защита (`hidden_tag`)
- удобно показывать ошибки у полей

### Каркас формы

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        "Повтор пароля",
        validators=[DataRequired(), EqualTo("password", message="Пароли не совпадают")],
    )
    submit = SubmitField("Зарегистрироваться")
```

### В маршруте

```python
form = RegisterForm()
if form.validate_on_submit():   # POST + все проверки ок + CSRF ок
    ...
return render_template("register.html", form=form)
```

### В шаблоне

```jinja
<form method="post">
  {{ form.hidden_tag() }}   {# CSRF #}
  {{ form.login.label }} {{ form.login() }}
  {% for error in form.login.errors %}<span>{{ error }}</span>{% endfor %}
  ...
  {{ form.submit() }}
</form>
```

### Важно
В `app.py` должен быть:

```python
app.config["SECRET_KEY"] = SECRET_KEY  # из config.py
```

Без `SECRET_KEY` CSRF/сессии не заработают нормально.

### Как в SecondLife
Смотри: `webapp/user/forms.py` — `LoginForm`, `RegisterForm`, кастомные `validate_login` / `validate_email`.

---

## 5. Пароли: никогда не хранить как есть

**Нельзя:**
```python
user.password = "qwerty"   # в БД лежит открытый текст — плохо
```

**Нужно:** хеш (односторонняя функция).

```python
from werkzeug.security import generate_password_hash, check_password_hash

generate_password_hash("qwerty")  # длинная строка для БД
check_password_hash(hash_from_db, "qwerty")  # True/False
```

В модели (стиль SecondLife):

```python
def set_password(self, password):
    self.password = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password, password)
```

При регистрации: `user.set_password(form.password.data)`  
При логине: `user.check_password(form.password.data)`

---

## 6. Модель User

Учебный минимум для pet-проекта:

```python
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from db import Base

class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
```

| Поле/деталь | Зачем |
|-------------|--------|
| `UserMixin` | нужен Flask-Login (`is_authenticated`, `get_id`, …) |
| `unique=True` у login | один логин — один пользователь |
| `password` длиннее | хеш длинный, `String(120)` может не хватить → лучше 255 |
| наследование от `Base` | как `Item`, тот же SQLAlchemy 2.0 |

После добавления модели снова:

```powershell
python models.py
```

(или отдельный `create_all` — таблица `users` появится)

Как в SecondLife: `webapp/user/models.py` (там ещё email, role, связи — для pet пока не обязательно).

---

## 7. Flask-Login: кто сейчас залогинен

Flask-Login хранит в сессии **id пользователя** и даёт:

| Объект/функция | Смысл |
|----------------|--------|
| `login_user(user)` | «запомнить» пользователя после успешного входа |
| `logout_user()` | выйти |
| `current_user` | кто сейчас (или аноним) |
| `current_user.is_authenticated` | залогинен ли |
| `@login_required` | пускать только залогиненных |

### Подключение (упрощённо для pet)

```python
from flask_login import LoginManager
from config import SECRET_KEY
from db import db_session
from models import User

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # куда кидать неавторизованных

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))
```

`user_loader` — Flask-Login спрашивает: «по id из сессии верни объект User».

Как в SecondLife: `webapp/__init__.py` (`LoginManager`, `user_loader`).

---

## 8. Регистрация

Алгоритм:

```text
1. GET /register  → показать форму
2. POST /register → form.validate_on_submit()
3. проверить, что login свободен
4. User(login=...)
5. user.set_password(...)
6. db_session.add + commit
7. redirect на /login
```

Проверка «логин занят»:

```python
exists = db_session.query(User).filter_by(login=form.login.data).first()
if exists:
    # ошибка: такой логин уже есть
```

В SecondLife это сделано через `validate_login` внутри формы.

---

## 9. Логин / логаут

### Логин

```text
1. найти User по login
2. user.check_password(password)
3. если ок → login_user(user) → redirect домой
4. если нет → сообщение об ошибке
```

```python
user = db_session.query(User).filter_by(login=form.login.data).first()
if user and user.check_password(form.password.data):
    login_user(user)
    return redirect(url_for("home"))
```

### Логаут

```python
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
```

---

## 10. login_required — защита маршрутов

```python
from flask_login import login_required

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item():
    ...
```

Если гость открыл `/add` → редирект на страницу логина (`login_view`).

Позже так же защитишь edit/delete.

В шаблонах:

```jinja
{% if current_user.is_authenticated %}
  <a href="{{ url_for('logout') }}">Выйти ({{ current_user.login }})</a>
{% else %}
  <a href="{{ url_for('login') }}">Войти</a>
{% endif %}
```

Чтобы `current_user` работал в шаблонах, Flask-Login обычно сам добавляет его в контекст после `init_app`.

---

## 11. Связка с объявлениями (Item)

**Этап А (сначала):** любой залогиненный может добавлять товары.  
**Этап Б (потом):** у `Item` появляется владелец.

```python
# в Item позже
user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
```

При создании:
```python
item = Item(name=name, price=price, user_id=current_user.id)
```

Удалять/редактировать — только свой товар (`item.user_id == current_user.id`).

Это уже one-to-many: один User → много Item (ты это проходил в SQL).

---

## 12. Что поставить

```powershell
pip install flask-login flask-wtf email-validator
```

У тебя уже есть: Flask, SQLAlchemy, psycopg2.

`SECRET_KEY` в `config.py` — обязателен.

---

## 13. Что почитать перед следующей сессией

Обязательно (коротко, по делу):

1. Этот конспект целиком один раз
2. SecondLife (только посмотреть, не переписывать всё):
   - `webapp/user/models.py` — `User`, `set_password`, `check_password`
   - `webapp/user/forms.py` — `LoginForm`, `RegisterForm`
   - `webapp/user/views.py` — register / login / logout / `login_required`
   - `webapp/__init__.py` — кусок с `LoginManager`
3. Официально (по желанию, 10–15 мин):
   - Flask-Login: https://flask-login.readthedocs.io/en/latest/
   - Flask-WTF: https://flask-wtf.readthedocs.io/

Не нужно зубрить всё API — достаточно понять поток:
`форма → validate → User → hash → login_user → login_required`.

---

## 14. Как подготовиться

Чеклист до следующей сессии:

- [ ] Прочитал этот конспект
- [ ] Можешь своими словами объяснить: валидация, хеш пароля, `login_user`, `@login_required`
- [ ] В pet-проекте БД с `Item` уже работает
- [ ] В `config.py` есть `SECRET_KEY`
- [ ] Установлены `flask-login`, `flask-wtf` (можно прямо перед практикой)
- [ ] Открыл глазами `User`/`forms`/`login` в SecondLife

На сессии в чате ООП:
1. мини-теория / вопросы
2. задачки на бумаге/в редакторе (без полного проекта)
3. потом в pet-чате внедряешь по шагам

---

## 15. План задачек (чат ООП)

Будем решать примерно так:

1. Ручная валидация `name`/`price` — дописать проверки
2. Написать `RegisterForm` / `LoginForm` (класс, не весь сайт)
3. Написать `User` с `set_password` / `check_password`
4. Скелет `register` / `login` через `db_session`
5. Куда вешать `@login_required`
6. Словами: зачем `user_loader`

Подсматривать конспект сначала можно; цель — потом без подсказки объяснить цепочку.

---

## 16. План внедрения (чат pet-проекта)

Делай по одному шагу, после каждого — проверка в браузере:

| # | Шаг | Критерий «готово» |
|---|-----|-------------------|
| 1 | Ручная валидация на `/add` | пустая форма не пишет в БД, есть ошибки |
| 2 | Модель `User` + `create_all` | таблица `users` есть |
| 3 | `LoginManager` + `user_loader` + `SECRET_KEY` | приложение стартует |
| 4 | `/register` | новый пользователь в БД, пароль — хеш |
| 5 | `/login` + `/logout` | сессия появляется/пропадает |
| 6 | `@login_required` на `/add` | гостя кидает на логин |
| 7 | Ссылки Войти/Выйти в шаблоне | видно статус |
| 8 | (позже) `Item.user_id` | товар принадлежит пользователю |

---

## 17. Шпаргалка

```text
Валидация:   пусто / не число / price <= 0  → ошибки, не commit
Регистрация: User → set_password → add → commit
Логин:       найти User → check_password → login_user
Защита:      @login_required на /add (и edit/delete)
Секрет:      SECRET_KEY в config
CSRF:        form.hidden_tag() в шаблоне Flask-WTF
```

```text
Браузер                Flask                      PostgreSQL
/register POST  →  validate + set_password  →  INSERT users (hash)
/login POST     →  check_password           →  SELECT user
                →  login_user (session cookie)
/add            →  @login_required
                →  validate + Item(...)     →  INSERT items
```

---

## Статус на сейчас

| Тема | Статус |
|------|--------|
| Flask каркас / шаблоны / формы add | ✅ |
| PostgreSQL + SQLAlchemy Item | ✅ |
| Валидация | ⬜ следующая сессия |
| Регистрация / логин | ⬜ следующая сессия |
| Item принадлежит User | ⬜ после логина |

Когда вернёшься в чат ООП — пиши «готов по конспекту», начнём с задачек.
