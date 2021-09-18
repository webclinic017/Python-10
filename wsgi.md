# wsgi

들어가기 앞서 헷갈리는 용어를 정리하겠습니다.

![](https://www.fullstackpython.com/img/visuals/full-stack-python-map.png)

- `web server`
  - A computer that hosts a website on the Internet.
  - 웹 사용자가 호스트 파일에 접근하도록 관리하는 서버
  - 일반적으로 `HTTP 서버`를 칭함 (HTTP request/response관리)
  - 정적 컨텐츠는 WAS를 거치지 않고 동적인 컨텐츠는 WAS를 거친다.
  - ex. Nginx, Apache, IIS ...
- `WAS(Web Application Server)`
  - a.k.a `Web Container`, `Servlet Container`
  - 현재 문맥 기준으로는 `wsgi server` + `web application`의 통합 개념이라 생각하면 된다.
  - ex. Gunicorn + Django
- `wsgi`
  - Web Server Gateway Interface
  - "module & container"가 필수적으로 구현해야 파이썬 표준 인터페이스
- `wsgi server(container)`
  - wsgi 인터페이스를 구현한 구현체
  - 해당 컨테이너에서 `web application`을 실행한다.
  - ex. Gunicorn, uWSGI ...
- `web application` (callable)
  - web framework를 사용해 작성한 python code
  - web framework는 내부적으로 WSGI 인터페이스의 application side를 구현하고 있다.
  - ex. FastAPI, Django, Flask ...

## WSGI
> [pep 0333](https://www.python.org/dev/peps/pep-0333/#id15)

> https://wsgi.readthedocs.io/

1. The Application/Framework Side
   - callable object
2. The Server/Gateway Side

   - The server or gateway invokes the application callable once for each request it receives from an HTTP client
   - ```python
      def run_with_cgi(application):
        ... 중략 ...

        def start_response(status, response_headers, exc_info=None):
            ... 중략 ...
            # application object를 받아서 request가 올 때마다 호출
            result = application(environ, start_response)
     ```
3. Middleware: Components that Play Both Sides
   - conform to the restrictions and requirements of both the server and application sides of WSGI
   - ```python
     class MyIter:
        ...

     class MyMiddleware:
         def __init__(self, application):
            self.application = application

        def __call__(self, environ, start_response):
            ... 중략 ...
            return MyIter(self.application(environ, start_latin), transform_ok)

     """
     1. run_with_cgi: Server/Gateway Side
     2. my_app: Application/Framework Side
     3. MyMiddleware: Middleware: Components that Play Both Sides
     """
     from my_app import my_app
     run_with_cgi(MyMiddleware(my_app))
     ```

## WSGI Servers
> [wsgi-servers reference](https://www.fullstackpython.com/wsgi-servers.html)

> [Web Server Gateway Interface (WSGI)](https://wsgi.readthedocs.io/en/latest/)를 구현한 server

과거(1990s) `apache`가 `mod_python`를 통해 python code가 서버에서 run할 수 있도록 했었지만, standard 스펙이 아닌 관계로 다수의 취약점들이 발생했다. 이를 계기로 Python community가 `WSGI`라는 "module과 containers가 구현해야하는" 표준 interface를 도입했다. (PEP 3333) 

### WSGI Purpose
> 왜 web server로 바로 찌르지 않고, WSGI를 거쳐야 하는가?

1. `flexibility`
   - 앱개발자들은 Gunicorn, uWSGI등의 제품들을 자유롭게 전환할 수 있다.
1. `scaling`
   - 다수의 requests를 동적으로 처리하는 것은 `wsgi server`의 책임이고, `web framework`(ex FastAPI, Django, Flask)들은 이로부터 자유롭다.

![](https://www.fullstackpython.com/img/visuals/web-browser-server-wsgi.png)


## Gunicorn
> https://docs.gunicorn.org/en/latest/design.html#how-many-workers

> [pre-fork worker model](https://stackoverflow.com/questions/25834333/what-exactly-is-a-pre-fork-web-server-model)

> [optimizing gunicorn](https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7)

- Web Server Gateway Interface (WSGI) server implementation
- commonly-used part of `web app deployments` that's powered some of the largest Python-powered web applications in the world, such as Instagram
- Django의 경우 wsgi.py 파일을 통해 application을 wsgi(gunicorn)에게 delegate한다. 이를 통해 WSGI 서버가 application에 대해 hook을 할 수 있다.

### Gunicorn worker model
- Gunicorn is based on a pre-fork worker model
- `pre-fork worker model`
  - `master thread`가 다른 `worker`들을 spin up 시킨다.
  - `worker`들은 requests들을 처리한다.

### How Many Workers?
- Gunicorn should only need **4-12** worker processes to handle hundreds or thousands of requests per second.
- Gunicorn relies on the operating system to provide all of the load balancing when handling requests. Generally we recommend **(2 x $num_cores)** + 1 as the number of workers to start off with. While not overly scientific, the formula is based on the assumption that for a given core, one worker will be reading or writing from the socket while the other worker is processing a request.

### How Many Threads?
- to process requests in multiple threads. 
- Using threads assumes use of the gthread worker. 
- One benefit from threads is that **requests can take longer than the worker timeout** while notifying the master process that it is not frozen and should not be killed. 