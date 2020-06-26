# Web Socket
> 

TCP Connector처럼 Connector pool이 존재하는데 AioHttp에 websocket이 필요한 이유가 명확하지 않아, 문서를 작성해보고자 합니다.


궁금한점?

1. TCP Connector : Web Socket = 1 : 1?
2. 크롬 따위의 브라우저를 통해서 서버의 특정 TCP 소켓(connection)에 연결이 가능?
3. 3-way handshake, 4-way handshake 마다 생성되는 소켓들은 TCP 소켓들인가?
    - 만약 그렇다면 web socket 1개당 tcp connector에 존재하는 tcp socket 여러개를 사용하는 것인가? 
    - 그럼 클라이언트 URL 요청 1개당 직접적으로 생성되는 서버 자원은 TCP Conn일까 아니면, Web Socket 일까?

## Web Socket vs TCP Socket

WebSocket은 기본적으로 응용 프로그램 프로토콜 (ISO/OSI 네트워크 스택 참조)이며 메시지 지향적이며, TCP 를 전송 계층으로 사용합니다.




