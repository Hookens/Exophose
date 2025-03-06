# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import SelectOption
from discord.bot import Bot
from discord.interactions import Interaction
from discord.ui import View, select, Select

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Help.helpmethods import HelpMethods

HELP_OPTIONS = [
    SelectOption(
        label="About Exophose",
        description="Links to resources and other info."
    ),
    SelectOption(
        label="Custom Roles",
        description="Managing your custom roles."
    ),
    SelectOption(
        label="Bundle Roles",
        description="Selecting roles from bundles."
    ),
    SelectOption(
        label="Custom Configuration",
        description="Configuring roles for custom creation."
    ),
    SelectOption(
        label="Bundle Configuration",
        description="Configuring bundles for limited selection."
    )
]

class HelpView(View):
    def __init__(self, bot: Bot):
        super().__init__(timeout=180)
        self.bot = bot

    async def on_timeout(self):
        self.disable_all_items()

    @select(
        placeholder="Navigate the menu",
        min_values=1,
        max_values=1,
        options=HELP_OPTIONS
    )
    async def select_callback(self, select: Select, interaction: Interaction):
        methods: HelpMethods = self.bot.get_cog("HelpMethods")
        await interaction.response.edit_message(embed=await methods.generate_help(select.values[0]))