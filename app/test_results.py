import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_average__success() -> None:
    os.environ["SUPERBENCHMARK_DEBUG"] = "True"

    response = client.get("/results/average/")

    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 10.2,
        "average_time_to_first_token": 216.0,
        "average_time_per_output_token": 27.6,
        "average_total_generation_time": 485.2
    }

    del os.environ["SUPERBENCHMARK_DEBUG"]


def test_get_average__not_available() -> None:
    response = client.get("/results/average/")

    assert response.status_code == 503


def test_get_average_range__success() -> None:
    os.environ["SUPERBENCHMARK_DEBUG"] = "True"

    url = "/results/average/2024-06-01T12:00:00/2024-06-01T13:00:00"

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {
        "average_token_count": 5.5,
        "average_time_to_first_token": 175.0,
        "average_time_per_output_token": 27.5,
        "average_total_generation_time": 325.0
    }

    del os.environ["SUPERBENCHMARK_DEBUG"]


def test_get_average_range__no_content() -> None:
    os.environ["SUPERBENCHMARK_DEBUG"] = "True"

    url = "/results/average/2024-06-01T10:00:00/2024-06-01T11:00:00"

    response = client.get(url)

    assert response.status_code == 204

    del os.environ["SUPERBENCHMARK_DEBUG"]


def test_get_average_range__not_available() -> None:
    url = "/results/average/2024-06-01T12:00:00/2024-06-01T13:00:00"
    response = client.get(url)

    assert response.status_code == 503
