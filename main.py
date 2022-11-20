import discord
# coding: utf-8
import configparser
import datetime
intents = discord.Intents.all()
intents.message_content = True  # メッセージコンテントのintentはオンにする
client = discord.Client(intents=intents)
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

@client.event
async def on_ready(): #botログイン完了時に実行
    print('on_ready')
    print(datetime.datetime.now())
    print('----------------------------------------------')

def print_info(member,msg):
    print(member)
    print(msg)
    print(datetime.datetime.now())
    print('----------------------------------------------')

@client.event
async def on_raw_reaction_add(payload): #ロール付与機能
    if payload.message_id == config_ini.getint('MESSAGE', 'splFes_msg_id_2'): 
        checked_emoji = payload.emoji.id 
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        channel_id = config_ini.getint('CHANNEL', 'splFes_ch_id')
        channel = client.get_channel(channel_id)
        member = guild.get_member(payload.user_id)
        if checked_emoji == config_ini.getint('FUKA', 'emoji_id'):
            await payload.member.add_roles(guild.get_role(config_ini.getint('FUKA', 'role_id')))
            msg = 'フウカのロールを付与しました！'
        elif checked_emoji == config_ini.getint('UTSUHO', 'emoji_id'):
            await payload.member.add_roles(guild.get_role(config_ini.getint('UTSUHO', 'role_id')))
            msg = 'ウツホのロールを付与しました！'
        elif checked_emoji == config_ini.getint('MANTARO', 'emoji_id'): 
            await payload.member.add_roles(guild.get_role(config_ini.getint('MANTARO', 'role_id')))
            msg = 'マンタローのロールを付与しました！'
    elif payload.message_id == config_ini.getint('MESSAGE', 'pokemonSV_msg_id'): 
        checked_emoji = payload.emoji.id 
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)
        if checked_emoji == config_ini.getint('KORAIDON', 'emoji_id'): 
            await payload.member.add_roles(guild.get_role(config_ini.getint('KORAIDON', 'role_id')))
            msg = 'スカーレットのロールを付与しました！'
        elif checked_emoji == config_ini.getint('MIRAIDON', 'emoji_id') : 
            await payload.member.add_roles(guild.get_role(config_ini.getint('MIRAIDON', 'role_id')))
            msg = 'バイオレットのロールを付与しました！'
    elif payload.message_id == config_ini.getint('MESSAGE', 'test_msg_id'): 
        checked_emoji = payload.emoji.id 
        print(checked_emoji)
    await payload.member.send(msg)
    print_info(member,msg)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == config_ini.getint('MESSAGE', 'splFes_msg_id_2'):
        checked_emoji = payload.emoji.id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)
        if checked_emoji == config_ini.getint('FUKA', 'emoji_id'):
            await member.remove_roles(guild.get_role(config_ini.getint('FUKA', 'role_id')))
            msg = 'フウカのロールを外しました！'
        if checked_emoji == config_ini.getint('UTSUHO', 'emoji_id'): 
            await member.remove_roles(guild.get_role(config_ini.getint('UTSUHO', 'role_id')))
            msg = 'ウツホのロールを外しました！'
        if checked_emoji == config_ini.getint('MANTARO', 'emoji_id'): 
            await member.remove_roles(guild.get_role(config_ini.getint('MANTARO', 'role_id')))
            msg = 'マンタローのロールを外しました！'
    elif payload.message_id == config_ini.getint('MESSAGE', 'pokemonSV_msg_id'): 
        checked_emoji = payload.emoji.id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)
        if checked_emoji == config_ini.getint('KORAIDON', 'emoji_id'):
            await member.remove_roles(guild.get_role(config_ini.getint('KORAIDON', 'role_id')))
            msg = 'スカーレットのロールを外しました！'
        if checked_emoji == config_ini.getint('MIRAIDON', 'emoji_id'):
            await member.remove_roles(guild.get_role(config_ini.getint('MIRAIDON', 'role_id')))
            msg = 'バイオレットのロールを外しました！'
    await member.send(msg)
    print_info(member,msg)

@client.event
async def on_message(message): #メッセージを検知した時に実行
    #print(message)
    if message.author == client.user: #message.author(メッセージ送信者名)がclient.user(bot)だった時、処理を回避(しないと無限ループする)
        return
    if message.content.startswith('$hello'): #message.content(メッセージ内容)が「$hello」から始まるとき
        await message.channel.send('Hello!') 

client.run(config_ini.get('TOKEN', 'token'))