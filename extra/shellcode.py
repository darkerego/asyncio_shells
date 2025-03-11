


class Shell:
    _asyncio = None

    def __init__(self):
        self._asyncio = __import__('asyncio')
        self.loop = None
        self.get_event_loop()
        self.tasks = set()
        self.queue = self.asyncio.Queue()
        self.counter = 0

    @property
    def asyncio(self):
        return Shell._asyncio


    def get_event_loop(self):
        try:
            _loop = self.asyncio.get_running_loop()
        except RuntimeError:
            _loop = self.asyncio.get_event_loop_policy().new_event_loop()
        self.loop = _loop
    async def exec_cmd(self, cmd , as_task: bool = False):
        self.counter += 1
        proc = await self.asyncio.create_subprocess_shell(
            cmd,
            stdout=self.asyncio.subprocess.PIPE,
            stderr=self.asyncio.subprocess.STDOUT
        )

        stdout, stderr = await proc.communicate()
        return stdout

    def done_callback(self, task):
        self.tasks.discard(task)

        try:
            res = task.result()
        except Exception:
            res = task.exception()
        self.queue.put((self.counter, res))

    async def exec_cmd_nonblocking(self, cmd):
        result = await self.loop.run_in_executor(
            None, self.exec_cmd, cmd)
        print('default thread pool', result)