# pytest
> https://www.udemy.com/course/elegant-automation-frameworks-with-python-and-pytest


- smoke test
  - 핵심 feature를 테스트하는 suite
  - @mark.smoke를 만들면 좋을 듯

## marker

- custom marker의 경우 pytest.ini에 설명을 추가해주어야 warning이 뜨지 않는다.


```bash
$ pytest -v # verbose
$ pytest -m smoke # mark
$ pytest -m "engine or body"
$ pytest -m "not smoke"
$ pytest --markers # custom markers의 설명들을 볼 수 있다.
@pytest.mark.smoke: All critical smoke tests

@pytest.mark.body: All car body tests

@pytest.mark.engine: All car engine tests

@pytest.mark.entertainment: All tests covering the entertainments system
```

## fixture

```bash
pytest . -s # stdout print
```