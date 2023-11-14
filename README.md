# DiscordTools

A collection of useful tools for managing a Discord server

## Install
```
$ pip install discordtools
```

## Usage

### Downloading avatars
```
➜ discordtools download-avatars --help
Usage: discordtools download-avatars [OPTIONS]

Options:
  -t, --token TEXT              Discord Token. DISCORD_TOKEN envvar.
                                [required]
  -g, --guild-id TEXT           Guild ID. DISCORD_GUILD_ID envvar.  [required]
  -r, --role TEXT               Filter users by role
  -p, --path DIRECTORY          Path of the folder to save the avatars.
                                DISCORD_AVATAR_PATH envvar.  [required]
  -i, --include-default-avatar  Include users with default avatar.
                                DISCORD_INCLUDE_DEFAULT_AVATAR envvar.
  --help                        Show this message and exit.
```
