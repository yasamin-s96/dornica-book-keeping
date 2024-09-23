import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Role
from settings import settings


def seed_roles():
    engine = create_engine("mysql+pymysql://root@mysql_db:3306/book_keeping")
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session()

    roles = [
        {"name": "Admin", "slug": "admin"},
        {"name": "Manager", "slug": "manager"},
        {"name": "User", "slug": "user"},
    ]

    for role in roles:
        db_role = db.execute(sa.select(Role).where(Role.name == role["name"])).first()
        if not db_role:
            new_role = Role(**role)
            db.add(new_role)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_roles()
