import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from main import app, get_db

from database import Base, engine
from schemas import FilmCreate, ActorCreate, CreateGenre, CreateUser, DirectorCreate

client = TestClient(app)

url = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = sqlalchemy.create_engine(url)
test_session = Session(engine)


def get_test_db():
    try:
        yield test_session
        test_session.commit()
    except:
        raise
    finally:
        test_session.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_add_film(test_db):
    response = client.post("/films", json={"title": "Little Women", "director_id": 1, "genre_id": 1})
    assert response.status_code == 200
    assert "film was added successfully" in response.text

def test_get_all_films(test_db):
    response = client.get("/films")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_actor(test_db):
    response = client.post("/actors", json={"name": "Dylan O'Brien"})
    assert response.status_code == 200
    assert "actor was added successfully" in response.text

def test_get_all_actors(test_db):
    response = client.get("/actors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_genre(test_db):
    response = client.post("/genres", json={"name": "Test Genre"})
    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "rom-com"}  # Assuming the response returns the added genre

def test_get_all_genres(test_db):
    response = client.get("/genres")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_director(test_db):
    response = client.post("/directors", json={"name": "Autumn de Wilde"})
    assert response.status_code == 200
    assert "the director was added successfully" in response.text

def test_get_all_directors(test_db):
    response = client.get("/directors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_user(test_db):
    response = client.post("/users", json={"username": "mapofthemoon", "email": "mapofthemmon@gmail.com"})
    assert response.status_code == 200
    assert "User was added successfully" in response.text

def test_get_all_users(test_db):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_films_by_director(test_db):
    response = client.get("/directors/1/films")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
