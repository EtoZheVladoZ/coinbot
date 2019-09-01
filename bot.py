import discord
from discord.ext import commands
import os

Client = commands.Bot(command_prefix='/')

@Client.event
async def on_ready():
    await Client.change_presence(activity = discord.Game(name = 'created by VladoZ'))
    print('Bot is online')

@Client.event
async def on_member_join(member):
    members_number = member.guild.get_channel(615540774620102708)
    await members_number.edit(name = f"👥Учасников: {str(member.guild.member_count)}")

@Client.event
async def on_member_remove(member):
    members_number = member.guild.get_channel(615540774620102708)
    await members_number.edit(name = f"👥Учасников: {str(member.guild.member_count)}")

@Client.event
async def on_voice_state_update(member, before, after):
    cname = f"Канал {str(member.name)}"
    main_channel = member.guild.get_channel(615541017768099840)
    f = open('id.txt', 'r+')
    if after.channel == main_channel:
        chl = await  member.guild.create_voice_channel(name = cname, user_limit = 2, category = after.channel.category)
        channel = discord.utils.get(member.guild.voice_channels, name = cname)
        await member.move_to(channel)
        overwrite = discord.PermissionOverwrite(manage_channels = True)
        await channel.set_permissions(member, overwrite = overwrite)
        f.write(str(chl.id))
    if before.channel is not None:
        id_chl = int(f.read())
        if before.channel.id == id_chl and before.channel.members == []:
            await before.channel.delete()
            f.close
    
token = os.environ.get('BOT_TOKEN')
Client.run(str(token))
