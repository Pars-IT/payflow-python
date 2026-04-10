from app.db import SessionLocal
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


def seed_user():
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email="habibi.mh@gmail.com").first()
        if not user:
            user = User(
                name="Mohammad",
                email="habibi.mh@gmail.com",
                password=generate_password_hash("secret"),
            )
            session.add(user)
            session.commit()
        else:
            user.name = "Mohammad"
            user.password = generate_password_hash("secret")
            session.commit()
        print(f"User seeded: {user.email}")
    except IntegrityError as e:
        session.rollback()
        print(f"Error seeding user: {e}")
    finally:
        session.close()
