import sys
from getpass import getpass

from db import db_session
from webapp.product.models import User

login = input('Введите логин:')

if db_session.query(User).filter_by(login=login).first():
    print('Пользователь с таким логином уже существует')
    sys.exit(0)

email = input('Введите email: ')

password1 = getpass('Введите пароль: ')
password2 = getpass('Повторите пароль: ')

if password1 != password2:
    print('Пароли не одинаковые')
    sys.exit(0)

if db_session.query(User).filter_by(email=email).first():
    print('Пользователь с таким email уже существует')
    sys.exit(0)

new_user = User(login=login, email=email, role='admin')
new_user.set_password(password1)

db_session.add(new_user)
db_session.commit()
print(f'Создан пользователь с id={new_user.id} added')
