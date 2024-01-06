from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an engine and bind it to the session
engine = create_engine('sqlite:///events.db', echo=True)
Base = declarative_base()

# Define a User class that represents the 'users' table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

# Create all tables defined in the Base
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Now you can use the session to interact with the 'users' table
# For example, adding a user
new_user = User(email='example@example.com', password='password123')
session.add(new_user)
session.commit()

# Querying for a user with specific credentials
user = session.query(User).filter(User.email == 'example@example.com', User.password == 'password123').first()
print(user)
print("--------------------------------------------------------------")
print(type(user))
if user:
    print(f"User found! User ID: {user.id}, Email: {user.email}")
else:
    print("User not found or invalid credentials.")
