import discord
from discord.ext import commands
from colorama import init, Fore as cc
import os
import asyncio
import logging

# Initialize colorama and logging
init()
logging.basicConfig(level=logging.INFO)

# Color setup
dr = cc.LIGHTRED_EX
g = cc.LIGHTGREEN_EX
b = cc.LIGHTBLUE_EX
m = cc.LIGHTMAGENTA_EX
c = cc.LIGHTCYAN_EX
y = cc.LIGHTYELLOW_EX
w = cc.RESET

# Banner
baner = f'''
{dr} _   _       _       {m} ____        _   
{dr}| \ | |_   _| | _____{m}| __ )  ___ | |_ 
{dr}|  \| | | | | |/ / _ {m}\  _ \ / _ \| __|
{dr}| |\  | |_| |   <  __{m}/ |_) | (_) | |_ 
{dr}|_| \_|\__,_|_|\_\___{m}|____/ \___/ \__|
{y}Made by: {g}FASIL_503'''

# Nuking functions (same as provided)
# [Include all the async functions (delete_all_channel, delete_all_roles, etc.) here]

# Main loop
def main():
    while True:
        os.system('clear')
        choice = input(f'''   
{baner}                
{c}--------------------------------------------
{b}[Menu]
    {y}└─[1] {m}- {g}Run Setup Nuke Bot
    {y}└─[2] {m}- {g}Exit
{y}====>{g}''')
        if choice == '1':
            token = input(f'{y}Input bot token:{g} ')
            name = input(f'{y}Input name for created channels/roles:{g} ')
            os.system('clear')
            choice_type = input(f'''
{baner}                
{c}--------------------------------------------
{b}[Select]
    {y}└─[1] {m}- {g}Nuke all servers
    {y}└─[2] {m}- {g}Nuke specific server  
    {y}└─[3] {m}- {g}Exit
{y}====>{g}''')
            client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
            if choice_type == '1':
                @client.event
                async def on_ready():
                    print(f'\n[+] Logged as {client.user.name}\n[+] Bot in {len(client.guilds)} servers!')
                    for guild in client.guilds:
                        await nuke_guild(guild, name)
                    await client.close()
            elif choice_type == '2':
                guild_id = input(f'{y}Input server ID:{g} ')
                @client.event
                async def on_ready():
                    target_guild = discord.utils.get(client.guilds, id=int(guild_id))
                    if target_guild:
                        await nuke_guild(target_guild, name)
                    else:
                        print(f'{dr}Server not found!')
                    await client.close()
            elif choice_type == '3':
                print(f'{dr}Exit...')
                exit()
            try:
                client.run(token)
                input('Nuke finished. Press Enter to return to menu...')
            except Exception as e:
                print(f'{dr}Error: {e}')
                input('Press Enter to continue...')
        elif choice == '2':
            print(f'{dr}Exit...')
            exit()

if __name__ == "__main__":
    main()
