import random, os, discord, validators
from discord.ext import commands

TOKEN = "TOKEN HERE"
client = commands.Bot(command_prefix='o.')

@client.event
async def on_ready():
   game = discord.Game("o.otter")
   await client.change_presence(status=discord.Status.online, activity=game)
   print ("logged in as " + client.user.name)

@client.command(
    description = 'returns a random otter',
    brief = 'returns a random otter',
)
async def otter(ctx):
    path = r"D:/Pictures/dank otters"
    random_filename = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    image = discord.File(fp=path + "/" + str(random_filename), filename=random_filename)
    await ctx.send(content=None, file=image)

# This event watches incoming messages for a mobile link and corrects it to a non-mobile link for common websites like Youtube and Wikipedia.
@client.event
async def on_message(message):
    text = message.content
    ctx = await client.get_context(message)
    channel = message.channel
    if validators.url(text) and str.find(text, '.m.') != -1:
        await ctx.send(content = 'non mobile link: ' + text.replace('.m.', '.'))
    elif validators.url(text) and str.find(text, '/m.') != -1:
        await ctx.send(content = 'non mobile link: ' + text.replace('/m.', '/www.'))
    else:
        await client.process_commands(message)

@client.command(
    description = 'usage: pass a discord user ID to get their avatar url. o.pfp [INSERT USER ID HERE]',
    brief = 'pass a discord user ID to get an avatar URL',
)
async def pfp(ctx, id):
    try:
        newuser = await client.fetch_user(id)
        await ctx.send(content='User avatar URL: ' + str(newuser.avatar_url))
    except (discord.errors.HTTPException, discord.errors.NotFound):
        await ctx.send(content='Fetching the user failed or a user with this ID does not exist.')

client.run(TOKEN)