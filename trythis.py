import pytest
import inspect

from marshmallow_dataclass import dataclass as m_dataclass
import marshmallow_dataclass
import dataclasses


import asyncio
import time


async def inner(x):
    print(f'inner {x}')
    time.sleep(0.5)
    await asyncio.sleep(0.5)


async def count(d):
    print(f'One {d}')
    await inner(d)
    print(f'Two {d}')
    await inner(-d)
    print(f'Three {d}')


async def main():
    asyncio.create_task(count(1))

asyncio.run(main())


@marshmallow_dataclass.dataclass
class Batch():

    prev_batch: int

    def __post_init__(self):
        print("this is post init")
        raise Exception()


#batch = Batch(0)
# print(batch)
