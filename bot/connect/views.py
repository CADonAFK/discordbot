import logging
from typing import TYPE_CHECKING
import dataclasses

import discord
from discord import ui, Interaction

from bot.connect.schema import MemberConnections

if TYPE_CHECKING:
    from bot.connect.cog import ConnectCog

log = logging.getLogger(__name__)


class ModalStepView(ui.View):

    def __init__(self, cog: 'ConnectCog', value: MemberConnections, **kwargs):
        super(ModalStepView, self).__init__(**kwargs)
        self.cog = cog
        self.value = value

    @ui.button(label='Next Page', style=discord.ButtonStyle.blurple)
    async def next_page(self, itx: Interaction, button: ui.Button):
        await itx.response.send_modal(ConnectionsModalTwo(self.cog, self.value))


class ConnectionsModal(ui.Modal, title="Choose what accounts you want to connect on"):

    def __init__(self, cog: 'ConnectCog', **kwargs):
        super().__init__(**kwargs)
        self.cog = cog

    switch = ui.TextInput(label="Switch account", placeholder="Switch account")
    xbox = ui.TextInput(label="Xbox account", placeholder="Xbox account")
    ps4 = ui.TextInput(label="PS4 account", placeholder="PS4 account")
    roblox = ui.TextInput(label="Roblox account", placeholder="Roblox account")
    minecraft = ui.TextInput(label="Minecraft account", placeholder="Minecraft account")

    async def on_submit(self, itx: Interaction) -> None:
        value = MemberConnections(
            switch=self.switch.value,
            xbox=self.xbox.value,
            ps4=self.ps4.value,
            roblox=self.roblox.value,
            minecraft=self.minecraft.value,
        )
        view = ModalStepView(self.cog, value)
        msg = "You are almost done. There is one more page of connections to fill out. Click Next to continue"
        await itx.response.send_message(msg, view=view, ephemeral=True)


class ConnectionsModalTwo(ui.Modal, title="Choose what accounts you want to connect on"):

    def __init__(self, cog: 'ConnectCog', value: MemberConnections, **kwargs):
        super().__init__(**kwargs)
        self.cog = cog
        self.value = value

    fortnite = ui.TextInput(label="Fortnite account", placeholder="Fortnite account")
    rocket_league = ui.TextInput(label="Rocket League account", placeholder="Rocket League account")
    among_us = ui.TextInput(label="Among Us account", placeholder="Among Us account")
    twitter = ui.TextInput(label="Twitter account", placeholder="Twitter account")
    twitch = ui.TextInput(label="Twitch account", placeholder="Twitch account")

    async def on_submit(self, itx: Interaction):
        key = str(itx.user.id)

        self.value.fortnite = self.fortnite.value
        self.value.rocket_league = self.rocket_league.value
        self.value.among_us = self.among_us.value
        self.value.twitter = self.twitter.value
        self.value.twitch = self.twitch.value

        self.cog.config_settings[key] = dataclasses.asdict(self.value)
        self.cog.save_settings()
        await itx.response.send_message("Your connections have been saved", ephemeral=True)