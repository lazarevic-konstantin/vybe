from sqlalchemy import create_engine
from model import Base, User


engine = create_engine('sqlite:///vybe.db')
Base.metadata.create_all(engine)

user = User(username='test_username', email='e@e.e', password='test')
user.save()
