# pipenv
> [python.org](https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies)
> https://pipenv.pypa.io/en/latest/

> Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world

- `pip` + `virtualenv`
- `Pipfile`와 `Pipfile.lock`을 `requirements.txt`를 대신하여 사용
- `$ pipenv graph`를 통해 의존성 그래프를 볼 수 있다.
- `Pipfile.lock`
  - `deterministic` build
  - 락이 걸린 의존성에 대해 해쉬 파일을 생성해 보안을 높인다.
- 자동으로 virtualenv환경을 생성한다.
- 패키지 설치/삭제 자동으로 Pipfile에 추가/삭제한다.
- `.env`를 자동 인식
- `pyenv` 사용 가능하다면, 필요한 python도 자동 설치

## 
```
python3 -m pip install --user pipenv
```