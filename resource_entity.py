from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer
from typing import Self
import datetime
from .models import TypeField, Resource


Base = declarative_base()


class ResourceEntity(Base):
    __tablename__ = "resources"

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    vanity_url: Mapped[str | None] = mapped_column(String, nullable=True)
    type: Mapped[TypeField] = mapped_column(String, nullable=False)
    expiration_time: Mapped[datetime.datetime | int | None] = mapped_column(
        String, nullable=True, default=-1
    )
    access_count: Mapped[int] = mapped_column(Integer, default=0)

    def to_model(self) -> Resource:
        return Resource(
            id=self.id,
            content=self.content,
            vanity_url=self.vanity_url,
            type=self.type,
            expiration_time=self.expiration_time,
            access_count=self.access_count,
        )

    @classmethod
    def from_model(cls, resource: Resource) -> Self:
        return cls(
            id=resource.id,
            content=resource.content,
            vanity_url=resource.vanity_url,
            type=resource.type,
            expiration_time=resource.expiration_time,
            access_count=resource.access_count,
        )
