'''This is test code for "How async lock is act" test code'''

import asyncio
from random import uniform

critical_section = {'count': 0}


async def before_lock(name):
    for i in range(4):
        print(f'Before Lock: {name} is make {i}')
        await asyncio.sleep(uniform(0.1, 0.5))


async def after_lock(name):
    for i in range(4):
        print(f'After Lock: {name} is clean up {i}')
        await asyncio.sleep(uniform(0.1, 0.5))


async def worker(name, lock):
    print(f'{name} is working now')

    await before_lock(name)

    # lock 을 가지지 못하였다면 해당 context 이후의 코드 조차도 실행 못한다.
    async with lock:
        print('>' * 20 + f' {name} entered critical area')
        for _ in range(3):
            r = critical_section['count']
            await asyncio.sleep(.1)
            critical_section['count'] += 1
            print('>' * 20 + f" {name} : {r} -> {critical_section['count']}")
            await asyncio.sleep(.1)
    print(f'{name} leave critial area ' + '<' * 20)

    await after_lock(name)
    print(f'{name} is finished')


async def main():
    lock = asyncio.Lock()
    fs = [worker(f'worker{i}', lock) for i in range(4)]
    await asyncio.wait(fs)


if __name__ == '__main__':
    asyncio.run(main())
