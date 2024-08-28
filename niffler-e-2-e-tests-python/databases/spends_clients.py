from sqlalchemy import create_engine, Engine, delete
from sqlmodel import Session, select, delete

from models.spend import Category


class SpendDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, pool_size=10)

    def get_user_categories(self, username):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    def delete_categories(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    def delete_all_categories(self):
        with Session(self.engine) as session:
            statement = delete(Category)
            session.exec(statement)
            session.commit()
