import pytest

def pytest_addoption(parser):
    parser.addoption(
            "--baseurl", action="store", default="http://localhost:8080/")

@pytest.fixture
def baseurl(request):
    return request.config.getoption("--baseurl")


