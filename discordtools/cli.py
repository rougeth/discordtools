import asyncio
from pathlib import Path

import click
import discord
from rich.console import Console


async def download(member, path, semaphore):
    """Download an user avatar"""
    async with semaphore:
        avatar_path = path / f"{member.id}.webp"
        with open(avatar_path, "wb") as avatar:
            await member.avatar_url.save(avatar)


async def download_avatars(members, path):
    """Download avatar from a list of users"""
    semaphore = asyncio.Semaphore(50)
    tasks = [download(member, path, semaphore) for member in members]
    await asyncio.gather(*tasks)


async def get_members(guild, include_default_avatar):
    """Get all members from a Discord server"""
    members = await guild.fetch_members().flatten()
    if not include_default_avatar:
        # Filter out users who didn't define an avatar
        members = [
            member
            for member in members
            if member.default_avatar_url != member.avatar_url
        ]
    return members


async def main(token, guild_id, path, include_default_avatar):
    console = Console()
    with console.status("Authenticating at Discord..."):
        client = discord.Client(intents=discord.Intents.all())
        await client.login(token)

    try:
        with console.status("Authenticating to Discord..."):
            guild = await client.fetch_guild(guild_id)
            console.log(f"Discord Server: {guild.name}")

        with console.status("Retreving all members..."):
            members = await get_members(guild, include_default_avatar)
            console.log(f"Total members: {len(members)}")

        with console.status("Downloading avatars..."):
            await download_avatars(members, path)
            console.log(f"Avatars downloaded at {path.resolve()}")
    finally:
        await client.close()


@click.group()
def cli():
    ...


@cli.command()
@click.option(
    "-t", "--token", envvar="DISCORD_TOKEN", required=True, help="Discord Token"
)
@click.option(
    "-g", "--guild-id", envvar="DISCORD_GUILD_ID", required=True, help="Guild ID"
)
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    envvar="DISCORD_AVATAR_PATH",
    required=True,
    help="Path of the folder to save the avatars",
)
@click.option(
    "-i",
    "--include-default-avatar",
    is_flag=True,
    envvar="DISCORD_INCLUDE_DEFAULT_AVATAR",
    help="Include users with default avatar",
)
def download_avatars(include_default_avatar, path, guild_id, token):
    asyncio.run(main(token, guild_id, path, include_default_avatar))


if __name__ == "__main__":
    cli()
