from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

engine = create_engine(
    url="sqlite:///./kohyli.db",
    # FOTIS: echo commands for now for debugging purposes
    echo=True,
    # We need to disable the check_same_thread flag for SQLite,
    # as otherwise we will get an error when running multiple threads.
    connect_args={"check_same_thread": False},
)


def create_tables():
    from .models import Book, User, Author, Review, Order, OrderItem

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

