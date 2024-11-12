import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    # Por defecto las columna tienen nullable=True (esto es cuando el campo no es obligatorio)
    # Si una columna debe ser obligatoria se digita nullable=False (esto es cuando el campo  es obligatorio)
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False) 
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

    def to_dict(self):
        return {}

class User(Base):
    __tablename__= 'user'
    id = Column(Integer, primary_key=True)
    username = Column (String(30), nullable=False, unique=True)
    firstname = Column (String(30))
    lastname = Column (String(30))
    email = Column (String(40), nullable = False, unique= True)
    comment = relationship('comment', back_populates='author_relationship')
    post= relationship('post', back_populates='author_post_relationship')
    followers =  relationship('Follower', back_populates= 'followed_user', foreign_keys = 'Follower.user_to_id')
    following = relationship('Follower', back_populates='follower_user', foreign_keys='Follower.user_from_id')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column (String(200), nullable=False)
    author = Column (Integer, ForeignKey ('user.id'))
    author_relationship = relationship(User, back_populates= 'comments')
    post = Column (Integer, ForeignKey ('post.id'))
    post_relationship = relationship('Post', back_populates= 'comments')

class Post(Base):
    __tablename__= 'post'
    id = Column (Integer, primary_key=True)
    author = Column (Integer, ForeignKey ('user.id'))
    author_post_relationship = relationship(User, back_populates= 'post')
    comment = relationship('comment', back_populates='post_relationship')

class Follower(Base):
    __tablename__= "follower"
    id = Column (Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable =False)
    user_to_id = Column (Integer, ForeignKey ('user.id'), nullable = False)
    follower_user = relationship (User, foreign_keys =[user_from_id], back_populates = 'following')
    followed_user = relationship (User, foreign_keys =[user_to_id], back_populates = 'followers')

class Media (Base):
    __tablename__='media'
    id = Column (Integer, primary_key =True)
    type = Column (Enum ('image', 'video', 'audio', name='media_types'), nullable=False)
    url = Column (String (255), nullable=False, unique = True)
    post_id = Column (Integer, ForeignKey('post.id'), nullable=False)
    post_relationship= relationship('Post', back_populates ='media')

    

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
