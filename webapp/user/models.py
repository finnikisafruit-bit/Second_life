from flask_login import UserMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from db import Base, engine


class User(UserMixin, Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(120), index=True, default='user')
    products: Mapped[list['Product']] = relationship(back_populates='owner')
    wishlist_items: Mapped[list['Wishlist']] = relationship(back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User id: {self.id}, User login: {self.login}>'


class Wishlist(Base):
    __tablename__ = 'wishlist'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='wishlist_items')
    product: Mapped['Product'] = relationship(back_populates='wishlist_items')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
