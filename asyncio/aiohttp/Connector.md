# Connector
> [Aiohttp API](https://docs.aiohttp.org/en/stable/client_reference.html)

Connector란 `aiohttp client API`의 운송 수단입니다.

2가지 standard-Type이 존재합니다.

1. `TCPConnector`
    - 일반적인 TCP 소켓
    - HTTP / HTTPS 스키마를 support 
2. `UnixConnector` 
    - Unix Socket을 사용
    - 일반적으로 testing 목적으로 사용됨
    
모든 커넥터 클래스는 `BaseConnector`에서 파생 되어야합니다.
기본적으로 모든 커넥터들은 keep-alive connection을 지원 합니다. (행위는 `force_close` 생성자 parameter에 의해 제어됨)

## BaseConnector

```python
BaseConnector(*,
              keepalive_timeout=15,
              force_close=False,
              limit=100,
              limit_per_host=0,
              enable_cleanup_closed=False,
              loop=None
              )
```

Parameters
- keepalive_timeout (float) 
    - timeout for connection reusing after releasing (optional). 
    - Values 0. For disabling keep-alive feature use force_close=True flag.

- limit (int) 
    - total number simultaneous connections. If limit is None the connector has no limit (default: 100).

- limit_per_host (int) 
    - limit simultaneous connections to the same endpoint. 
    - Endpoints are the same if they are have equal (host, port, is_ssl) triple. 
    - If limit is 0 the connector has no limit (default: 0).

- force_close (bool) 
    - close underlying sockets after connection releasing (optional).

- enable_cleanup_closed (bool) 
    - some SSL servers do not properly complete SSL shutdown process, in that case asyncio leaks ssl connections. 
    - If this parameter is set to True, aiohttp additionally aborts underlining transport after 2 seconds. It is off by default.

- loop
    - event loop used for handling connections.
    - If param is None, asyncio.get_event_loop() is used for getting default event loop. (2.0 부터 사용되지 않음)

## TCPConnector

가장 일반적인 transport layer이다. 
어떤 커넥터 타입을 사용할지 모르겠다면 해당 클래스를 사용하는것을 추천한다.

```python
TCPConnector(*, 
             ssl=None, 
             verify_ssl=True, 
             fingerprint=None, 
             use_dns_cache=True, 
             ttl_dns_cache=10, 
             family=0,
             ssl_context=None, 
             local_addr=None, 
             resolver=None, 
             keepalive_timeout=sentinel, 
             force_close=False, 
             limit=100,
             limit_per_host=0, 
             enable_cleanup_closed=False, 
             loop=None)
```

## Connection
> `class aiohttp.Connection`

Connector object로 부터의 single connection을 Encapsule하고 있는 object이다.

**End-User는 Connection을 생성해서는 안되고 반드시 BaseConnector.connect() 코루틴을 통해 얻어야 한다.**

