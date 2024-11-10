from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base, str_uniq, int_pk, str_null_true
from datetime import date


# создаем модель пользователей
class Student(Base):
    id: Mapped[int_pk]
    full_name: Mapped[str]
    phone_number: Mapped[str_uniq]
    description: Mapped[str]



    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.last_name!r})")

    def __repr__(self):
        return str(self)
