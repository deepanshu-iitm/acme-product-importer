from db import engine
from models import Base, Product, Webhook

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
