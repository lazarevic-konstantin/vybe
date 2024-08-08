from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///vybe.db')
Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)


def with_session(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        session = db_session()
        try:
            result = method(self, session=session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return wrapper
