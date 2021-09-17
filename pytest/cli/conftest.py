import pytest
from config import Config
from pytest import fixture

# parser은 pytest의 secret 키워드이다.
# about action: https://docs.python.org/3/library/argparse.html#action
def pytest_addoption(parser):
    parser.addoption(
        '--phase',
        action='store', # store 또한 키워드
        help="실행할 Environment Phase") 

@fixture(scope='session')
def phase(request):
    return request.config.getoption('--phase')

@fixture(scope='session')
def app_config(phase):
    return Config(phase)


@fixture(autouse=True)
def skip_if_not_matched_phase(request, phase):
    target = request.node.get_closest_marker('phase')
    if target:
        if target.args[0] != phase:
            pytest.skip('skipped on this phase: {}'.format(phase))