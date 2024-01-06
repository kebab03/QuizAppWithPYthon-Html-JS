from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create an engine and bind it to the session
engine = create_engine('sqlite:///example.db', echo=True)
Session = sessionmaker(bind=engine)
db = Session()
# Simulated email and password from the login form
usn = 'example@example.com'
psw = 'password123'

# Query the database for a user with the provided email and password
result = db.query(User).filter(User.email == usn, User.password == psw).first()

if result:
    print("User found!")
    print(f"User ID: {result.id}, Email: {result.email}")
else:
    print("User not found or invalid credentials.")
