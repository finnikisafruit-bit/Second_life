from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, engine


class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(120), unique=True)
    email: Mapped[str] = mapped_column(unique=True)

    def __repr__(self):
        return f'<User: {self.nickname}, {User.email}>'


class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    size: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(String(300))
    url: Mapped[str] = mapped_column(String(300))
    city: Mapped[str] = mapped_column(String(120))
    condition: Mapped[str] = mapped_column(String(120))

    def __repr__(self):
        return f'<Product: {self.id}, {self.title}>'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
