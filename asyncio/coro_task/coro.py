import asyncio


async def accumulate(coro, n, m):
    print(coro + "is started!")
    total = n

    while total < m:
        print(f'{coro} is yielding {total}')
        yield total
        total += 1
        print(f'{coro} is sleeping')
        await asyncio.sleep(.1)


async def sum_coroutine(*args):
    total = [i async for i in accumulate(*args)]  # accumulate의 반환값을 가져옴
    print("result : ", total)
    return total


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nums = [('coro1', 1, 11), ('coro2', 11, 21)]
    tasks = [asyncio.ensure_future(sum_coroutine(*args)) for args in nums]
    loop.run_until_complete(asyncio.wait(tasks))
