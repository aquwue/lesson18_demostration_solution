from unittest.mock import MagicMock

import pytest

from demostration_solution.dao.model.movie import Movie
from demostration_solution.dao.movie import MovieDAO
from demostration_solution.service.movie import MovieService
from demostration_solution.setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie_1 = Movie(id=1, title="title1", description="description1", trailer="trailer1", year=1990, rating=3)
    movie_2 = Movie(id=2, title="title2", description="description2", trailer="trailer2", year=1997, rating=1)
    movie_3 = Movie(id=3, title="title3", description="description3", trailer="trailer3", year=1991, rating=2)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.get_all = MagicMock()
    movie_dao.get_all = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None
        assert len(movie) == 2, f'Кол-во фильмов должно быть равно 1, а у вас {len(movie)}'  # неправильный тетст

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "description": "Test",
            "rating": 7.8,
            "title": "Test",
            "trailer": "Test",
            "year": 2022,
            "genre_id": 17,
            "director_id": 1
        }

        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        ret = self.movie_service.delete(1)
        assert ret is None

    def test_update(self):
        movie_d = {
            "id": 4,
            "description": "Test",
            "rating": 7.8,
            "title": "Test",
            "trailer": "Test",
            "year": 2022,
            "genre_id": 17,
            "director_id": 1
        }
        ret = self.movie_service.update(movie_d)
        assert ret is None


