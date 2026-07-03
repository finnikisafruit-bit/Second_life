from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, engine


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(120))
    size: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(300))
    url: Mapped[str] = mapped_column(String(300))
    city: Mapped[str] = mapped_column(String(120))
    condition: Mapped[str] = mapped_column(String(120))

    def __repr__(self):
        return f'<Product id: {self.id}, {self.title}>'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
