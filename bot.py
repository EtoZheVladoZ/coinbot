import discord
from discord.ext import commands
import os
import time

Client = commands.Bot(command_prefix='$')

@Client.event
async def on_ready():
    await Client.change_presence(activity = discord.Game(name = 'created by VladoZ'))
    print('Bot is online')

@Client.command(pass_context = True)
async def balance(ctx, * member: discord.User):
    channel = ctx.message.channel
    d = {}
    with open("balance.txt", 'r') as f:
        for line in f:
            key, value = line.split()
            d[key] = int(value)
    if member == ():
        if str(ctx.message.author.id) in d:
            emb = discord.Embed(colour=0x2ecc71)
            emb.set_author(name=f"{ctx.message.author.name}", icon_url=f"{ctx.message.author.avatar_url}")
            emb.add_field(name="Баланс:", value=f"{d[str(ctx.message.author.id)]}")
            await channel.send(embed=emb)
        else:
            emb = discord.Embed(title=f"{ctx.message.author.name}", colour=0x2ecc71, icon_url=f"{message.author.avatar_url}")
            emb.add_field(name="Баланс:", value="0")
            await channel.send(embed=emb)
    if member != ():
        if str(ctx.message.author.id) in d:
            emb = discord.Embed(colour=0x2ecc71)
            emb.set_author(name=f"{member[0].name}", icon_url=f"{member[0].avatar_url}")
            emb.add_field(name="Баланс:", value=f"{d[str(member[0].id)]}")
            await channel.send(embed=emb)
        else:
            emb = discord.Embed(title=f"{member[0].name}", colour=0x2ecc71, icon_url=f"{member[0].avatar_url}")
            emb.add_field(name="Баланс:", value="0")
            await channel.send(embed=emb)

@Client.command()
async def shop(ctx, value=None, * role: discord.Role):
    shop = {
        '613096198580076548': 10,
        '644959008385663034': 14
        }
    channel = ctx.message.channel
    emb = discord.Embed(title="Магазин", colour=0x2ecc71)
    emb.add_field(name="**asd**", value='**Цена**: 10 коинов\n`!shop buy 613096198580076548`', inline=False)
    emb.add_field(name="**new role**", value='**Цена**: 14 коинов\n`!shop buy 644959008385663034`', inline=False)
    if value == None:
        await ctx.channel.send(embed=emb)
    if value == 'buy':
        d = {}
        with open("balance.txt", 'r') as f:
            for line in f:
                key, value = line.split()
                d[key] = int(value)
        if str(role[0].id) in shop:
            if d[str(ctx.message.author.id)] >= shop[str(role[0].id)]:
                d[str(ctx.message.author.id)] -= shop[str(role[0].id)]
                with open("balance.txt", 'w') as f:
                    for key, value in d.items():
                        f.write("{} {}\n".format(key,value))
                rl = discord.utils.get(ctx.message.guild.roles, name=str(role[0]))
                await ctx.message.author.add_roles(rl)
                await channel.send("Вы успешно купили роль")
            else:
                await channel.send("На вашем балансе недостаточно коинов")

@Client.command()
async def transfer(ctx, price=0, * member: discord.User):
    channel = ctx.message.channel
    d = {}
    with open("balance.txt", 'r') as f:
        for line in f:
            key, value = line.split()
            d[key] = int(value)
    if member != ():
        if d[str(ctx.message.author.id)] >= int(price) and str(member[0].id) in d:
            d[str(ctx.message.author.id)] -= int(price)
            d[str(member[0].id)] += int(price)
            with open("balance.txt", 'w') as f:
                for key, value in d.items():
                    f.write("{} {}\n".format(key,value))
            await channel.send(f"Вы успешно перевели коины {member[0].name}")
        if d[str(ctx.message.author.id)] >= int(price) and str(member[0].id) not in d:
            d[str(ctx.message.author.id)] -= int(price)
            d[str(member[0].id)] = int(price)
            with open("balance.txt", 'w') as f:
                for key, value in d.items():
                    f.write("{} {}\n".format(key,value))
            await channel.send(f"Вы успешно перевели коины {member[0].name}")
        if d[str(ctx.message.author.id)] <= int(price):
            await channel.send("На вашем балансе недостаточно коинов")
    if price == 0 and member == ():
        await channel.send("!transfer <сумма> <пользователь>")
    
@Client.event
async def on_voice_state_update(member, before, after):
    d = {}
    with open("balance.txt", 'r') as f:
        for line in f:
            key, value = line.split()
            d[key] = int(value)
    if after.channel != None and after.self_mute == False and before.self_mute == False and after.channel.id != '641911705860964353':
        global time1
        time1 = time.time()
    if after.channel == None and before.channel.id != '641911705860964353':
        if str(member.id) in d:
            time2 = time.time()
            t = int((time2 - time1)/60)
            d[str(member.id)] += t
            with open("balance.txt", 'w') as f:
                for key, value in d.items():
                    f.write("{} {}\n".format(key,value))
        if str(member.id) not in d:
            t = int((time.time() - time1)/60)
            with open("balance.txt", 'a') as f:
                f.write(f"{str(member.id)} {t}\n")

token = os.environ.get('BOT_TOKEN')   
Client.run(str(token))
