import pytest
# Trick: in pytest monkey patch cannot get a session scope. 
@pytest.fixture(scope="session")
def monkeysession(request):
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    
    def fin():
        mpatch.undo()
    
    request.addfinalizer(fin)
    return mpatch