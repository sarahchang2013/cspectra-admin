import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Article(Base):
    __tablename__ = 'article'

    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    #use slug as the last segment of path 
    slug = Column(String(250), nullable=False)
    embeded_code = Column(String(250))
    text = Column(String(3000), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    #Add serialize function for server script, 
    #won't affect existing database.
    @property
    def serialize(self):
        """Return object data in serialization"""
        return {
                "id": self.id,
                "title": self.title,
                "slug": self.slug,
                "url_for_embeded_code": self.embeded_code,
                "text": self.text,
                "category_id": self.category_id,
                }

engine = create_engine(os.environ.get('CSPECTRA_DATABASE_URL'))


Base.metadata.create_all(engine)
