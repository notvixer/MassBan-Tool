import aiohttp, asyncio
from tasksio import TaskPool
###############################

members = []

for line in open("retards.txt"):
   members.append(line.replace("\n", ""))

################################

TOKEN = str(input("ENTER A BOT TOKEN: "))
GUILD = int(input("GUILD ID TO MASSBAN:  "))

async def ban(session, mem):
  async with session.put("https://discord.com/api/v10/guilds/%d/bans/%d" % (GUILD, int(mem))) as resp:
    if resp.status in (200, 201, 204):
      print("[\u001b[32;1mBANNED\u001b[0m] \u001b[31;1mSUCCESSFULLY ELIMINATED %s\u001b[0m" % (mem))
    elif resp.status == 429:
      again = await resp.json()
      print("[\u001b[31;1mRATELIMITED\u001b[0m] \u001b[34;1mRATELIMITED, RETRYING IN %d\u001b[0m" % (again['retry_after']))
      await asyncio.sleep(int(again['retry_after']))
      await ban(session, mem)


async def main():
  async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=70), headers={"Authorization": f"Bot {TOKEN}"}) as s:
    print('created session successfully, starting in 5 seconds...')
    await asyncio.sleep(5)
    async with TaskPool(4_000) as p:
      for n in members:
        await p.put(ban(s, n))


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except:
    print('Well, a problem occurred.')
