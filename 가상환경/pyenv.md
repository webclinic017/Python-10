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
