import difflib
import os
import sys
import traceback

import disnake
import disnake.ext.commands as commands
from fastapi import FastAPI

import config_discordbot as cfg
from config_bot import logger

app = FastAPI()


# For next update
@app.get("/")
async def read_root():
    return {"Hello": str(gst_bot.user)}


activity = disnake.Activity(
    type=disnake.ActivityType.watching,
    name="Gamestonk Terminal: https://github.com/GamestonkTerminal/GamestonkTerminal",
)


def fancy_traceback(exc: Exception) -> str:
    """May not fit the message content limit"""
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    return f"```py\n{text[-4086:]}\n```"


class GSTHelpCommand(commands.MinimalHelpCommand):
    """Custom Help Command."""

    def get_command_signature(self, command):
        command_syntax = f"{self.clean_prefix}{command.qualified_name}"
        command_usage = command.usage if command.usage is not None else ""
        signature_text = f"""
        Example usage:
            `{command_syntax} {command_usage}`"""
        return signature_text

    def add_bot_commands_formatting(self, commands, heading):
        """Add a minified bot heading with commands to the output."""
        if commands:
            menu_header = heading.replace("Commands", " category")
            self.paginator.add_line(
                f"__**{menu_header}**__ " + f"contains {len(commands)} commands."
            )
            self.paginator.add_line(f"\t\t`!help {heading}` for info and options.")


class GSTBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="..",
            intents=disnake.Intents.all(),
            help_command=GSTHelpCommand(sort_commands=False, commands_heading="list:"),
            sync_commands_debug=True,
            sync_permissions=True,
            activity=activity,
        )

    def load_all_extensions(self, folder: str) -> None:
        py_path = f"{folder}"
        folder = f"{folder}"
        for name in os.listdir(folder):
            if name.endswith(".py") and os.path.isfile(f"{folder}/{name}"):
                self.load_extension(f"{py_path}.{name[:-3]}")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        # Get all command names
        all_cmds = gst_bot.all_commands.keys()
        if isinstance(error, commands.CommandNotFound):
            cmd = str(error).split('"')[1]
            similar_cmd = difflib.get_close_matches(cmd, all_cmds, n=1, cutoff=0.7)

            if similar_cmd:
                error_help = f"Did you mean '**!{similar_cmd[0]}**'?"
            else:
                # TODO: This can be improved by triggering help menu
                error_help = f"**Possible commands are:** {', '.join(all_cmds)}"

            await ctx.send(f"_{error}_\n{error_help}\n", delete_after=30.0)

    async def on_slash_command_error(
        self,
        inter: disnake.AppCmdInter,
        error: commands.CommandError,
    ) -> None:
        embed = disnake.Embed(
            title=f"Slash command `{inter.data.name}` failed due to `{error}`",
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        if inter.response._responded:
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed, delete_after=30.0)

    async def on_user_command_error(
        self,
        inter: disnake.AppCmdInter,
        error: commands.CommandError,
    ) -> None:
        embed = disnake.Embed(
            title=f"User command `{inter.data.name}` failed due to `{error}`",
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        if inter.response._responded:
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed, delete_after=30.0)

    async def on_message_command_error(
        self,
        inter: disnake.AppCmdInter,
        error: commands.CommandError,
    ) -> None:
        embed = disnake.Embed(
            title=f"Message command `{inter.data.name}` failed due to `{error}`",
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        if inter.response._responded:
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed, delete_after=30.0)

    async def on_ready(self):
        # fmt: off
        logger.info(
            f"\n"
            f"The bot is ready.\n"
            f"User: {self.user}\n"
            f"ID: {self.user.id}\n"
        )
        # fmt: on


if cfg.IMGUR_CLIENT_ID == "REPLACE_ME" or cfg.DISCORD_BOT_TOKEN == "REPLACE_ME":
    logger.info(
        "Update IMGUR_CLIENT_ID or DISCORD_BOT_TOKEN or both in %s \n",
        os.path.join("discordbot", "config_discordbot"),
    )
    sys.exit()
print(f"disnake: {disnake.__version__}\n")


gst_bot = GSTBot()
gst_bot.load_all_extensions("cogs")


# Runs the bot
gst_bot.run(cfg.DISCORD_BOT_TOKEN)
