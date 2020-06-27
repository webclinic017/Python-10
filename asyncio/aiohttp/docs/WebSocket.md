# Web Socket
> 

TCP Connector처럼 Connector pool이 존재하는데 AioHttp에 websocket이 필요한 이유가 명확하지 않아, 문서를 작성해보고자 합니다.

<2020.06.27 Update> 

    Websocket이라는 것은 HTML5에 도입된 새로운 기술이며, real time, Full-duplex를 지원하는 소켓기능입니다.
    TCP Socket이 있는데 왜 WebSocket이 필요했는지 궁금했었는데, 새로운 기술이라는 것을 이해하고 나니 궁금증이 어느정도 풀릴 수 있었습니다.

궁금한점?

1. TCP Connector : Web Socket = 1 : 1?
    - n:m 관계로 맺어질 수 있다. 필요에 따라, 1 : m, 또는 n : 1관계로 진행이 가능하다.  
2. 크롬 따위의 브라우저를 통해서 서버의 특정 TCP 소켓(connection)에 연결이 가능?
    - 그렇다. 여러 proxy들을 거쳐서 websocket에 들어가게 되면 해당 소켓은 TCP 소켓을 물고 있다.
3. 3-way handshake, 4-way handshake 마다 생성되는 소켓들은 TCP 소켓들인가?
    - 만약 그렇다면 web socket 1개당 tcp connector에 존재하는 tcp socket 여러개를 사용하는 것인가? (1)에서 해결 
    - 그럼 클라이언트 URL 요청 1개당 직접적으로 생성되는 서버 자원은 TCP Conn일까 아니면, Web Socket 일까? 어떤 요청인지 따라 다르다. 만약 서버에 보내는 request가 websocket이 필요한 real time 서비스가 아닌 RESTful service라면 이에 대한 요청이 처리될 것이다.
    

## Web Socket vs TCP Socket

WebSocket은 기본적으로 응용 프로그램 프로토콜 (ISO/OSI 네트워크 스택 참조)이며 메시지 지향적이며, TCP 를 전송 계층으로 사용합니다.

## 작동 원리

WebSocket Handshake

1. Upgrade 헤더를 통해 웹 서버에 요청
2. 이때 브라우저는 랜덤하게 생성한 키를 서버에 함께 보낸다.
3. 이를 받은 서버는 키를 바탕으로 토큰을 생성한 후 브라우저에 돌려준다.
4. `Protocol Overhead`방식으로 웹 서버와 브라우저가 데이터를 주고 받는다.
 
여기서 `Protocol Overhead` 방식 이란 여러 TCP 커넥션을 생성하지 않고, 실제로는 하나의 80번 포트 TCP 커넥션을 이용하면서, 별도의 헤더 등을 통해 논리적인 데이터 흐름 단위를 이용해 여러개의 커넥션을 맺는 효과를 내는 방식을 말합니다.

기존의 HTTP 연결에서는 한번의 연결을 처리하기 위해서 3번의 TCP 패킷 교환과정이(3-way) 필요했고, 종료를 위해서는 4번의 패킷 교환이 필요했다. 


## aiohttp.web의 WebSocket

```python
import aiohttp

async def websocket_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print("Web-Socket connection closed")

    return ws

app.add_routes([web.get('/ws', websocket_handler)]) 
```