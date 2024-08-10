from sqlalchemy import create_engine
from database import Base, User, Administrator, get_by_id

engine = create_engine('sqlite:///vybe.db')
Base.metadata.create_all(engine)

# user = User(username='test_username', email='e@e.e', password='test')
# user.save()
# admin = Administrator(username='test_admin', password='a', email='a@a.a')
# admin.save()


print(get_by_id(table=Administrator, obj_id=2).username)
