from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from source.db import PostgresDb

Base = declarative_base()


class ormTeacher(Base):
    __tablename__ = 'teacher'

    tc_info = Column(String(40), primary_key=True)
    tc_recomendation = Column(String(40))
    resources = relationship("ormResources", back_populates="teacher")


class ormResources(Base):
    __tablename__ = 'resources'

    rs_info = Column(String(40), primary_key=True)
    tc_info = Column(String(40), ForeignKey('teacher.tc_info'))
    rs_activity = Column(Integer)
    teacher = relationship("ormTeacher", back_populates="resources")
    news = relationship("ormNews", back_populates="resources")


class ormNews(Base):
    __tablename__ = 'news'
    ns_news_info = Column(String, primary_key=True)
    rs_info = Column(String(40), ForeignKey('resources.rs_info'))
    ns_likes = Column(Integer)
    resources = relationship("ormResources", back_populates="news")


class ormStudents_view_news(Base):
    __tablename__ = 'students_view_news'

    ns_news_info = Column(String(40))
    st_info = Column(String(40), primary_key=True)


class ormStudent(Base):
    __tablename__ = 'student'

    st_review = Column(String(40))
    st_info = Column(String(40), primary_key=True)
    st_document = Column(String(40))



db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)
