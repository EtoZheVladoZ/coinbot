import discord
from discord.ext import commands

Client = commands.Bot(command_prefix='/')

@Client.event
async def on_member_join(member):
    members_number = member.guild.get_channel(615540774620102708)
    await members_number.edit(name = f"Учасников: {str(member.guild.member_count)}")

@Client.event
async def on_member_remove(member):
    members_number = member.guild.get_channel(615540774620102708)
    await members_number.edit(name = f"Учасников: {str(member.guild.member_count)}")

@Client.event
async def on_voice_state_update(member, before, after):
    cname = f"Канал {str(member.name)}"
    main_channel = member.guild.get_channel(615541017768099840)
    if after.channel == main_channel:
        await  member.guild.create_voice_channel(name = cname, user_limit = 2, category = after.channel.category)
        channel = discord.utils.get(member.guild.voice_channels, name = cname)
        await member.move_to(channel)
        overwrite = discord.PermissionOverwrite(manage_channels = True)
        await channel.set_permissions(member, overwrite = overwrite)
    if before.channel is not None:
        if before.channel.name == cname:
            await before.channel.delete()
    
token = os.environ.get('BOT_TOKEN')
