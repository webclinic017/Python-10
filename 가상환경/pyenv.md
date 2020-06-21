# pyenv
> [Real Python](https://realpython.com/intro-to-pyenv/)

## 설치 과정

의존성 구축( 빌드 종속성 )

    $ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
    
pyenv-installer 사용

    $ curl https://pyenv.run | bash
    
- pyenv: 실제 pyenv응용
- pyenv-virtualenv: 플러그인 pyenv및 가상 환경
- pyenv-update: 업데이트 플러그인 pyenv
- pyenv-doctor: 플러그인 pyenv및 빌드 종속성이 설치되어 있는지 확인하는 플러그인
- pyenv-which-ext: 시스템 명령을 자동으로 찾는 플러그인

시스템 설정 적용하기
    
    $ code ~/.bashrc
    $ 아래의 코드 type
    $ source ~/.bashrc 

`~/.bashrc`

```shell
... 중략 ...

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```


## pyenv을 통한 파이썬 버전별 설치 방법

사용가능한 python version 확인 (3.6~8 version 기준)

    pyenv install --list | grep " 3\.[678]"

설치

    pyenv install 3.8-dev
    
설치된 위치 확인

    ls ~/.pyenv/versions/

설치 삭제 방법 1

    rm -rf ~/.pyenv/versions/3.8-dev
 
설치 삭제 방법 2

    pyenv uninstall 3.8-dev
 
 
## pyenv를 통한 버전 변경

로컬에 사용가능한 python 버전 리스트

    pyenv versions

시스템 버전 python 사용

    pyenv global system
    
파이썬 버전 변경

    pyenv global 3.8-dev

폴더별 파이썬 버전 설정

local

    minkj1992@minkj1992-900X5L:~/code/Python$ python -V
    Python 3.6.9

    minkj1992@minkj1992-900X5L:~/code/Python/asyncio$ pyenv local 3.8-dev
    minkj1992@minkj1992-900X5L:~/code/Python/asyncio$ ls -al
    합계 16
    drwxrwxr-x  2 minkj1992 minkj1992 4096  6월 21 17:26 .
    drwxr-xr-x 16 minkj1992 minkj1992 4096  6월 21 16:49 ..
    -rw-r--r--  1 minkj1992 minkj1992    8  6월 21 17:26 .python-version
    -rw-rw-r--  1 minkj1992 minkj1992  162  6월 21 16:48 README.md
    
    minkj1992@minkj1992-900X5L:~/code/Python/asyncio$ python -V
    Python 3.8.3+


- 이 local명령은 종종 응용 프로그램 별 Python 버전을 설정하는 데 사용됩니다. 
- 이를 사용하여 버전을 3.8-dev다음과 같이 설정할 수 있습니다.
- 이 명령은 `.python-version`을 현재 디렉토리에 파일을 만듭니다.  
- pyenv사용자 환경에서 활성이 파일은 당신을 위해이 버전을 자동으로 활성화됩니다.


## 가상환경

- pyenv 는 여러 버전의 Python 자체를 관리합니다.
- virtualenv / venv 는 특정 Python 버전의 가상 환경을 관리합니다.
- pyenv-virtualenv 는 다양한 버전의 Python에서 가상 환경을 관리합니다.


가상환경 생성

    minkj1992@minkj1992-900X5L:~/code/Python/asyncio$ pyenv virtualenv 3.8-dev async-venv
    Looking in links: /tmp/tmpy_h3fll9
    Requirement already satisfied: setuptools in /home/minkj1992/.pyenv/versions/3.8-dev/envs/async-venv/lib/python3.8/site-packages (47.1.0)
    Requirement already satisfied: pip in /home/minkj1992/.pyenv/versions/3.8-dev/envs/async-venv/lib/python3.8/site-packages (20.1.1)

- pyenv의 python version 루트 디렉토리 `/home/minkj1992/.pyenv/versions`에 알맞은 버전안에 가상환경이 생성된다.
- 나의 경우에는 `<pyenv의 version디렉토리>/3.8-dev/envs/async-venv/`에 지정한 가상환경이 생성됨


가상환경 활성화

    pyenv activate async-venv

- 이 경우에는 터미널에서 global하게 가상환경이 잡힌다. 
- 즉, 해당 디렉토리를 벗어나도 가상환경을 유지한다.

가상환경 비활성화

    pyenv deactivate

해당 디렉토리 가상환경 지정

    pyenv local async-venv
    
- 이 경우 `.python-version`자체 내용이 변경된다.
    - 나의 경우에는 `3.8-dev` -> `async-venv`
    - 파이썬 버전만 기입되어있던 파일 내용이, 가상환경 이름으로 변경되었다. 
- 해당 디렉토리에 들어올 경우에 가상환경이 자동으로 활성화 된다.
- 이 경우 `deactivate`가 작동하지 않는다.


가상환경 자동 activate 확인

    (async-venv) minkj1992@minkj1992-900X5L:~/code/Python/asyncio$ cd ..
    minkj1992@minkj1992-900X5L:~/code/Python$ cd asyncio/
    (async-venv) minkj1992@minkj1992-900X5L:~/code/Python/asyncio$ 


