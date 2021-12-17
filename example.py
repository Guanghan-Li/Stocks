# Asynchronous Programming

# Concurrency
# Parallel

# Event Loop
# Threads
# Processes

# Task 1 ------------------
# Task 2 -------------

import asyncio, threading
from asyncio import sleep

state = {'hellos': 0}

async def sleepyLoop(t):
  while True:
    await sleep(t)
    state['hellos'] += 1

def waitForUser():
  while True:
    user_input = input("Enter Something: ")
    print("You entered:", user_input, state['hellos'])

async def sleepPrint(t):
  print(f"About to wait {t} seconds")
  await sleep(t)
  print(f"Waited {t} seconds")
  return t

def otherMain():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(sleepyLoop(1))

async def main():
  thread = threading.Thread(target=otherMain)
  thread.daemon = True
  thread.start()

  waitForUser()

asyncio.run(main())