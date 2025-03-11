# Asyncio Shells

#### About

<p>
Bind and reverse shells written in python with 
optional xor encryption and no third party libraries 
required. The shells require only importing the 
`asyncio` and (if using xor encryption) `base64` library. 
</p>

<p>
A handler is included with modes for listening and 
connecting (for both bind and reverse shells).
</p>

<p>
These shells do not require importing the subprocess, 
os, or sys libraries because they make use of 
asyncio.subprocess modules. The idea is that may 
make them a little harder to detect. So don't abuse 
the hell out of this please.
</p>

#### Usage

<p>
Included is a handler that supports both the reverse 
and bind shells, with or without xor encryption.
</p>

<pre>
python3 handler.py -h
usage: {'prog': 'handler.py'} [options] [listen | connect ] host port

positional arguments:
  {listen,connect}
    listen           Start tcp server, wait for reverse shell
    connect          Connect to a bind shell.

options:
  -h, --help         show this help message and exit
  -x XOR, --xor XOR  Enable base64 wrapped xor with this key otherwise disabled
  -v, --verbose      Enable debug messages

</pre>

<p>
For a bind shell, start the shell and then use the 
handler to connect.

First terminal:
</p>

<pre>
$ python bind.py 
</pre>

<p>Another terminal:</p>

<pre>
python3 handler.py connect 127.0.0.1 1337
</pre>

<p>
For a reverse shell, start the handler first and 
then start the shell. 
</p>

<p>
First terminal:
</p>

<pre>
python3 handler.py listen 127.0.0.1 1337
</pre>

<p>
Second terminal:
</p>

<pre>
python3 reverse.py
</pre>

#### Suggestions for production deployment


**NOTICE: This is a proof of concept application!**.
*Do NOT use in production!*
*Significant work is required! It's a POC!*

<p>In a production / 
pentest environment, you would want to obfuscate this 
code a bit and use a stager (or multiple stages) to hide  
the `exec_cmd` functionality. I would also suggest 
encrypting the application with a weak passphrase 
and then having the shell brute force itself at runtime.
I would definitely recommend adding functionality to 
make sure that the shell will not run in virtual sandboxed 
environment to avoid being flagged as malware.
</p>
