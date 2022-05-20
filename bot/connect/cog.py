from typing import Dict

import discord
from discord.ext import commands
from discord import app_commands, Interaction

from bot.connect.schema import MemberConnections
from bot.connect.views import ConnectionsModal
from mixins.config import ConfigMixin


class ConnectCog(ConfigMixin, commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super(ConnectCog, self).__init__()

    @app_commands.command(name='connect', description='Choose what accounts you want to connect on')
    async def connect_app_cmd(self, itx: Interaction):
        await itx.response.send_modal(ConnectionsModal(self))

    @app_commands.command(name='connections', description='View the connections that a member has specified')
    async def connections_app_cmd(self, itx: Interaction, member: discord.Member):
        key = str(member.id)
        if key not in self.config_settings.keys():
            embed = discord.Embed(title="No Connections Found", description="This member does not have any active connections")
            await itx.response.send_message(embed=embed, ephemeral=True)
            return
        inline = True
        no_value = "None"
        value: MemberConnections = MemberConnections(**self.config_settings[key])
        title = f"Connections for {member.display_name}"
        embed = discord.Embed(title=title)
        embed.add_field(name='Switch', value=value.switch or no_value, inline=inline)
        embed.add_field(name='Xbox', value=value.xbox or no_value, inline=inline)
        embed.add_field(name='PS4', value=value.ps4 or no_value, inline=inline)
        embed.add_field(name='Roblox', value=value.roblox or no_value, inline=inline)
        embed.add_field(name='Minecraft', value=value.minecraft or no_value, inline=inline)
        embed.add_field(name='Fortnite', value=value.fortnite or no_value, inline=inline)
        embed.add_field(name='Rocket League', value=value.rocket_league or no_value, inline=inline)
        embed.add_field(name='Among Us', value=value.among_us or no_value, inline=inline)
        embed.add_field(name='Twitter', value=value.twitter or no_value, inline=inline)
        embed.add_field(name='Twitch', value=value.twitch or no_value, inline=inline)
        await itx.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ConnectCog(bot))