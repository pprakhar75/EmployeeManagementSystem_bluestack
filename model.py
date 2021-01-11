from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

user_name = 'root'
password = str('root')

engine = create_engine('mysql+pymysql://' + user_name + ':' + password + '@localhost')
engine.execute("CREATE DATABASE IF NOT EXISTS employeedatabase")  # create db
engine.execute("USE employeedatabase")

engine.connect()
Session = sessionmaker()
Session.configure(bind=engine)


class Employee(Base):
    __tablename__ = 'Employee'
    emp_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(50), primary_key=True)
    password = Column(String(50))  # to encrypt
    employee_gender = Column(String(10))
    employee_role = Column(String(20), default='default')
    login_status = Column(String(5))  # todo can seggregate the tables later


class Conference(Base):
    __tablename__ = 'Conference'
    confid = Column(Integer, primary_key=True, autoincrement=True)
    conference_name = Column(String(20))


# class Login(Base):
#     __tablename__ = 'login'
#     empid = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     password = Column(String(20))  # todo can be encrypted
#     login_status = Column(String(5))  # todo can be bool, can have default value as well


# class EmployeeRole(Base):
#     __tablename__ = 'EmployeeRole'
#     user_id = Column(Integer, )  # a user can have multiple roles
#     role = Column(String)


Base.metadata.create_all(engine)
session = Session()
