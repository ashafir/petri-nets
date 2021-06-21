#!/usr/bin/python3

import asyncio


class Task:

    def __init__(self, *input):
        self.input = input
        self.name = None
        self.task = None

    async def execute(self):
        if self.input:
            # sceduling dependencies and waiting for completion
            for x in self.input:
                if not x.task:
                    x.task = asyncio.create_task(x.execute())
            await asyncio.gather(
                *[x.task for x in self.input if not x.task.done()])

        # scheduling derived class implementation
        # and waiting for completion
        return await self.implement()

    async def implement(self):
        "Intended to be implememted in the derived class."

    @classmethod
    def run(cls, target):
        for name, task in globals().items():
            if isinstance(task, Task):
                task.name = name
        return asyncio.run(target.execute())


class Dummy(Task):
    async def implement(self):
        print(f'Task {self.name}')


class Proc(Task):
    "Runs shell commands in a subprocess"

    async def implement(self):
        print(f'Proc {self.name}')
        cmd = 'echo hello; sleep 1; echo done'
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')


# dependencies:

A = Proc()
B = Proc(A)
C = Proc(A)
D = Proc(A)
E = Proc(B)
F = Proc(E, C, D)
G = Proc(F)


if __name__ == '__main__':
    import time
    s = time.perf_counter()
    Task.run(target=G)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
