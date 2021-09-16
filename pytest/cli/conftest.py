from pytest import fixture

# parser은 pytest의 secret 키워드이다.
# about action: https://docs.python.org/3/library/argparse.html#action
def pytest_addoption(parser):
    parser.addoption('--phase', action='store') # store 또한 키워드

