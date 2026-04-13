from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = "11111111"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "de_project"

DB_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

with engine.connect() as conn:
    result = conn.execute(text("select current_database(), current_user;"))
    for row in result:
        print(row)