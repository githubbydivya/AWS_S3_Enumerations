# author:   @githubbydivya
# date:     30/10/2022

from blessings import Terminal
import asyncio
import sys

t = Terminal()


def banner():
    divya = t.cyan_bold("@githubbydivya")

    return f"""
  _____ ____  
 / ____|___ \ 
 | (___   __) |
 ___ \ |__ < 
 ____) |___) |
 |_____/|____/           
 |___/ {divya} |___/              
    """


def print_result_colored(text, status_code=None):
    if str(status_code).startswith('4'):
        print(t.yellow_bold('[+] ') + t.yellow(text))
    elif str(status_code).startswith('2'):
        print(t.green_bold('[+] ') + t.green(text))
    else:
        print(text)


def print_started(target, limit):
    print(f'Started scanning {t.magenta_underline(target)} with rate of {t.magenta_underline(str(limit))} ...')


def fail_silently(func):
    def handle_keyboard_interrupt():
        print(t.red(" Stopping scan, waiting for threads to safely finish ..."))
        sys.exit(0)

    async def _wrapper_async(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
        except:
            return None

    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
        except:
            return None

    if asyncio.iscoroutinefunction(func):
        return _wrapper_async

    return _wrapper


def consume_generator(func):
    def _wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))

    return _wrapper
