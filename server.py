from autobahn.asyncio.component import Component, run, Session
from asyncio import sleep
import os
import argparse
import six

url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
realmv = os.environ.get('CBREALM', u'realm1')
print(url, realmv)
component = Component(transports=url, realm=realmv)


def cool(number):
  print("Called")
  if number == 5:
    return "You are cool"
  else:
    return "You are not cool"

@component.on_join
async def joined(session: Session, details):
    print("session ready")
    try:
      #session.register('com.app.cool', cool)
      session.register(cool, 'com.app.cool')
    except:
      print("Could not register function")

if __name__ == "__main__":   
  run([component])