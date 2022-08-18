import discord
import os

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.role_message_id = 1009935788693266493
        self.emoji_to_role = {
            discord.PartialEmoji(name='🎓'): 1009923229365846037, # mentor
            discord.PartialEmoji(name='🔍'): 1009923416528269473, # search team
            discord.PartialEmoji(name='🐍'): 1009059019467542548,  # Python
            discord.PartialEmoji(name='🍊'): 1009923593293004922,  # TensorFlow
            discord.PartialEmoji(name='🕯'): 1009923760863842424,  # Pytorch
            discord.PartialEmoji(name='☕'): 1009924041831895143,  # Java
            discord.PartialEmoji(name='✖'): 1009924090007650314,  # R
            discord.PartialEmoji(name='👓'): 1009924142604234865,  # C++
            discord.PartialEmoji(name='🧣'): 1009924293158768831,  # Julia
            discord.PartialEmoji(name='🎮'): 1009924383873187932,  # other pg
        }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(os.environ['TOKEN'])