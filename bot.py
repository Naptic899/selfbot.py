import discord
from discord.ext import commands
import datetime
import json
from ext.formatter import EmbedHelp


def run_wizard():
    print('------------------------------------------')
    print('WELCOME TO THE VERIX-SELFBOT SETUP WIZARD!')
    print('------------------------------------------')
    token = input('Enter your token:\n> ')
    print('------------------------------------------')
    prefix = input('Enter a prefix for your selfbot:\n> ')
    data = {
        "BOT": {
            "TOKEN" : token,
            "PREFIX" : prefix
            },
        "FIRST" : False
        }
    with open('data/config.json','w') as f:
        f.write(json.dumps(data, indent=4))
    print('------------------------------------------')
    print('Successfully saved your data!')
    print('------------------------------------------')
    

with open('data/config.json') as f:
    if json.load(f)['FIRST']:
        run_wizard()

with open('data/config.json') as f:  
    TOKEN = json.load(f)["BOT"]['TOKEN']

async def get_pre(bot, message):
    with open('data/config.json') as f:
        config = json.load(f)
    try:
        return config["BOT"]['PREFIX']
    except:
        return 's.'

bot = commands.Bot(command_prefix=get_pre, self_bot=True, formatter=EmbedHelp())
bot.remove_command('help')

_extensions = [

    'cogs.misc',
    'cogs.info',
    'cogs.utils'

    ]

@bot.event
async def on_ready():
    bot.uptime = datetime.datetime.now()
    print('------------------------------------------\n'
    	  'Self-Bot Ready\n'
    	  'Author: verix#7220\n'
    	  '------------------------------------------\n'
    	  'Username: {}\n'
          'User ID: {}\n'
          '------------------------------------------'
    	  .format(bot.user, bot.user.id))



@bot.command(pass_context=True)
async def ping(ctx):
    """Pong! Check your response time."""
    msgtime = ctx.message.timestamp.now()
    await (await bot.ws.ping())
    now = datetime.datetime.now()
    ping = now - msgtime
    pong = discord.Embed(title='Pong! Response Time:', 
    					 description=str(ping.microseconds / 1000.0) + ' ms',
                         color=0x00ffff)

    await bot.say(embed=pong)




@bot.command(aliases=['p'], pass_context=True)
async def purge(ctx, msgs: int, *, txt=None):
    '''Purge messages if you have the perms.'''
    await bot.delete_message(ctx.message)
    if msgs < 10000:
        async for message in bot.logs_from(ctx.message.channel, limit=msgs):
            try:
                if txt:
                    if txt.lower() in message.content.lower():
                        await bot.delete_message(message)
                else:
                    await bot.delete_message(message)
            except:
                pass
    else:
        await bot.send_message(ctx.message.channel, 'Too many messages to delete. Enter a number < 10000')


@bot.command(aliases=['c'], pass_context=True)
async def clean(ctx, msgs: int = 100):
    '''Shortcut to clean all your messages.'''
    await bot.delete_message(ctx.message)
    if msgs < 10000:
        async for message in bot.logs_from(ctx.message.channel, limit=msgs):
            try:
                if message.author == bot.user:
                    await bot.delete_message(message)
            except:
                pass
    else:
        await bot.send_message(ctx.message.channel, 'Too many messages to delete. Enter a number < 10000')

if __name__ == "__main__":
    for extension in _extensions:
        try:
            bot.load_extension(extension)
            print('Loaded extension: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
try:
    bot.run(TOKEN, bot=False)
except:
    print('\nIMPROPER TOKEN PASSED\nCHECK YOUR `config.json`\n')
    
