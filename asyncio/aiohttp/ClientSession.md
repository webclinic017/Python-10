# ClientSession
> [Aiohttp 레퍼런스](https://docs.aiohttp.org/en/stable/client_reference.html)
> [관련 Blog 글](http://blog.naver.com/PostView.nhn?blogId=ppuagirls&logNo=221561586278&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView)

클라이언트 세션은 HTTP 요청을 위한 권장 인터페이스입니다.

세션은 Connection Pool(`Connector Instance`)을 캡슐화해서 request & response합니다.
default로 `keepalives`를 지원합니다.

만약 당신의 응용 application이 large, unknown한 다른 서버들과 연결을 하는 상황을 제외하고는, ㅇ
Connection Pooling의 이점을 누리기 위해서는 **단일 세션을 사용하는 것을 추천합니다.**

**Don’t create a session per request. Most likely you need a session per application which performs all requests altogether!**

**A session contains a connection pool inside. Connection reusage and keep-alives (both are on by default) may speed up total performance!**

**The session contains a cookie storage and connection pool, thus cookies and connections are shared between HTTP requests sent by the same session.**

**즉 Application당 1개의 session interface를 가져 내부적으로 connection pool을 Encapsulation 시켜준다. 이때 요청들에 대해서는 keep-alive로 살아있는 connection들을 재활용하면서 성능 향상을 꾀하는 것이 일반적이다.** 
```python
import aiohttp
import asyncio

url = 'http://python.org'

async def fetch(client):
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session)
        return html


result = asyncio.run(main())
print(result)
```

## `class aiohttp.ClientSession`

`ClientSession()` 은 연결 자체 종료를 담당하는 context manager protocol을 지원합니다.

클라이언트 세션을 만들고 요청하는 클래스입니다. 이는 request의 session으로 생각하면 되고, `as resp`는 `ClientResponse Object`입니다.
 
여러 parameter를 ClientSession()의 args로 줄 수 있으며, `.get()`, `.post()`와 같은 method에 param들을 넣어줄 수 있습니다.


또한 resp.cookies["속성이름"]와 같이 쿠키에도 접근가능하며, resp.headers["속성이름"]을 통해서 응답 헤더의 속성에도 접근이 가능합니다.


## Parameters

```python
ClientSession(*,
              connector=None,  # 연결 풀링을 지원하는 BaseConnector 하위 클래스 인스턴스입니다.
              loop=None,  # HTTP 요청을 처리하는 데 사용되는 이벤트 루프
              cookies=None,
              headers=None,
              skip_auto_headers=None,
              auth=None,
              json_serialize=json.dumps,
              version=aiohttp.HttpVersion11,
              cookie_jar=None,
              read_timeout=None,
              conn_timeout=None,
              timeout=sentinel,
              raise_for_status=False,
              connector_owner=True,
              auto_decompress=True,
              requote_redirect_url=False,
              trust_env=False,
              trace_configs=None
              ) 
```