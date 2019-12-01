import asyncio
import curses

class Actor:
  async def tick(self):
    print( "Tick")

class Background(Actor):
  def __init__(self, name):
    self.name = name

  async def tick(self):
    print("Background Tick: ", self.name)

  async def ev(self, ev_name, ev_data):
    print( "EV: ", self.name, ev_name, ev_data)

class Dog(Actor):
  def __init__(self, name):
    self.name = name

  async def tick(self):
    print("Dog ", self.name, " tick")

async def retick(q):
  await asyncio.sleep(1.0)
  await q.put(("tick", None))

async def main(stdscr):
  q = asyncio.Queue()
  await q.put(("register", Background("Open Field" )))
  await q.put(("register", Dog("Fido" )))
  await q.put(("tick", 0))
  actors = {}
  while True:
    (ev_type, ev_data) = await q.get()
    if ev_type == "register":
      print("Registering new actor ", ev_data.name)
      actors[ev_data.name] = ev_data
      continue
    elif ev_type == "tick":
      for actor in actors.values():
        await asyncio.create_task(actor.tick())
      await asyncio.create_task(retick(q))
      continue
    for actor in actors.values():
      await asyncio.create_task(actor.ev((ev_type, ev_data)))

if __name__ == '__main__':
  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(True)

  try:
    asyncio.run(main(stdscr))
  except:
    print("App exception done")
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
