import pytest

from main import app

# test constants
EFF_OPT_URL = "/optimize/efficient"
NAIVE_OPT_URL = "/optimize/naive"
EFF_BEN_URL = "/benchmark/efficient"
NAIVE_BEN_URL = "/benchmark/naive"
PERF_COMP_URL = "/perf-comparison/6"


# fixtures
@pytest.fixture
def lists():
    return [[2, 3, 4, 5, 6], [1, 7, 4], [2, 5, 3], [1, 1]]


@pytest.fixture
def modulo_quot():
    return 200


@pytest.fixture(scope="module")
def client():
    with app.test_client() as client:
        yield client


def test_eff_opt_url_bad_request(client):
    rv = client.get(EFF_OPT_URL, data={})
    assert rv.status_code == 400


def test_eff_opt_url_successful(client, lists, modulo_quot):
    rv = client.get(EFF_OPT_URL, json={"lists": lists, "m": modulo_quot, "f": "lambda x: x**3"})
    assert rv.status_code == 200


def test_naive_opt_url_bad_request(client):
    rv = client.get(NAIVE_OPT_URL, data={})
    assert rv.status_code == 400


def test_naive_opt_url_successful(client, lists, modulo_quot):
    rv = client.get(NAIVE_OPT_URL, json={"lists": lists, "m": modulo_quot, "f": "lambda x: x**3"})
    assert rv.status_code == 200


def test_eff_ben_url_bad_request(client):
    rv = client.get(EFF_BEN_URL, data={})
    assert rv.status_code == 400


def test_eff_ben_url_successful(client, modulo_quot):
    rv = client.get(
        EFF_BEN_URL,
        json={"num_lists": 6, "num_elements": 10, "m": modulo_quot, "f": "lambda x: x**3", "replications": 20},
    )
    assert rv.status_code == 200


def test_naive_ben_url_bad_request(client):
    rv = client.get(NAIVE_BEN_URL, data={})
    assert rv.status_code == 400


def test_naive_ben_url_successful(client, modulo_quot):
    rv = client.get(
        NAIVE_BEN_URL,
        json={"num_lists": 6, "num_elements": 10, "m": modulo_quot, "f": "lambda x: x**3", "replications": 20},
    )
    assert rv.status_code == 200


def test_perf_comp_url_bad_request(client):
    rv = client.get(PERF_COMP_URL, data={})
    assert rv.status_code == 400


def test_perf_comp_url_successful(client, modulo_quot):
    rv = client.get(PERF_COMP_URL, json={"num_elements": 10, "m": modulo_quot, "f": "lambda x: x**3"})
    assert rv.status_code == 200
