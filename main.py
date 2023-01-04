import discord
from discord import app_commands
# coding: utf-8
import configparser
import datetime
intents = discord.Intents.all()
intents.message_content = True  # メッセージコンテントのintentはオンにする
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

MY_GUILD = discord.Object(id=config_ini.getint('GUILD', 'guild_id'))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self) 
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=intents)

def print_time_line():
    print(datetime.datetime.now())
    print('------------------------------------')

@client.event
async def on_ready(): #botログイン完了時に実行
    print('on_ready')
    print_time_line()

def print_info(member,msg):
    print(member)
    print(msg)
    print_time_line()

def add_embed_simple(title, descrip, color, member):
    embed = discord.Embed(title = title, description = descrip, color = color)
    embed.set_author(name= "["+str(member)+"]さん", )
    return embed

@client.event
async def on_raw_reaction_add(payload): #ロール付与機能
    guild_id = config_ini.getint('GUILD', 'guild_id')
    if payload.message_id == config_ini.getint('MESSAGE_ID', 'splFes_msg_id_2'): 
        checked_emoji = payload.emoji.id 
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        #channel_id = config_ini.getint('CHANNEL', 'splFes_ch_id')
        #channel = client.get_channel(channel_id)
        member = guild.get_member(payload.user_id)
        change_reaction = 1
        if checked_emoji == config_ini.getint('EMOJI_ID', 'fuka'):
            await payload.member.add_roles(guild.get_role(config_ini.getint('ROLE_ID', 'fuka')))
            msg = config_ini.get('TEXT', 'fuka') + 'のロールを付与しました！'
        elif checked_emoji == config_ini.getint('EMOJI_ID', 'utsuho'):
            await payload.member.add_roles(guild.get_role(config_ini.getint('ROLE_ID', 'utsuho')))
            msg = config_ini.get('TEXT', 'utsuho') + 'のロールを付与しました！'
        elif checked_emoji == config_ini.getint('EMOJI_ID', 'mantaro'): 
            await payload.member.add_roles(guild.get_role(config_ini.getint('ROLE_ID', 'mantaro')))
            msg = config_ini.get('TEXT', 'mantaro') + 'のロールを付与しました！'
    elif payload.message_id == config_ini.getint('MESSAGE_ID', 'pokemonSV_msg_id'): 
        checked_emoji = payload.emoji.id 
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)
        change_reaction = 1
        if checked_emoji == config_ini.getint('EMOJI_ID', 'scarlet'): 
            await payload.member.add_roles(guild.get_role(config_ini.getint('ROLE_ID', 'scarlet')))
            msg = config_ini.get('TEXT', 'scarlet') + 'のロールを付与しました！'
        elif checked_emoji == config_ini.getint('EMOJI_ID', 'violet') : 
            await payload.member.add_roles(guild.get_role(config_ini.getint('ROLE_ID', 'violet')))
            msg = config_ini.get('TEXT', 'violet') + 'のロールを付与しました！'
    elif payload.message_id == config_ini.getint('MESSAGE_ID', 'test_msg_id'): 
        print(payload.emoji.id)
        print_time_line()
        change_reaction = 0
    else :
        change_reaction = 0
    if change_reaction == 1:
        embed = add_embed('ロール更新', msg, int(config_ini.get('COLOR', 'role_lightBlue'),16))
        await payload.member.send(embed=embed)
        print_info(member,msg)

@client.event
async def on_raw_reaction_remove(payload):
    guild_id = config_ini.getint('GUILD', 'guild_id')
    if payload.message_id == config_ini.getint('MESSAGE_ID', 'splFes_msg_id_2'):
        checked_emoji = payload.emoji.id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)
        change_reaction = 1
        if checked_emoji == config_ini.getint('EMOJI_ID', 'fuka'):
            await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'fuka')))
            msg = config_ini.get('TEXT', 'fuka') + 'のロールを外しました！'
        if checked_emoji == config_ini.getint('EMOJI_ID', 'utsuho'): 
            await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'utsuho')))
            msg = config_ini.get('TEXT', 'utsuho') + 'のロールを外しました！'
        if checked_emoji == config_ini.getint('EMOJI_ID', 'mantaro'): 
            await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'mantaro')))
            msg = config_ini.get('TEXT', 'mantaro') + 'のロールを外しました！'
    elif payload.message_id == config_ini.getint('MESSAGE_ID', 'pokemonSV_msg_id'): 
        checked_emoji = payload.emoji.id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        member = guild.get_member(payload.user_id)
        change_reaction = 1
        if checked_emoji == config_ini.getint('EMOJI_ID', 'scarlet'):
            await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'scarlet')))
            msg = config_ini.get('TEXT', 'scarlet') + 'のロールを外しました！'
        if checked_emoji == config_ini.getint('EMOJI_ID', 'violet'):
            await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'violet')))
            msg = config_ini.get('TEXT', 'violet') + 'のロールを外しました！'
    else :
        change_reaction = 0
    if change_reaction == 1:
        embed = add_embed('ロール更新', msg, int(config_ini.get('COLOR', 'role_lightBlue'),16))
        await member.send(embed=embed)
        print_info(member,msg)

@client.event
async def on_message(message): #メッセージを検知した時に実行
    #print(message)
    if message.author == client.user: #message.author(メッセージ送信者名)がclient.user(bot)だった時、処理を回避(しないと無限ループする)
        return
    if message.content.startswith('$hello'): #message.content(メッセージ内容)が「$hello」から始まるとき
        await message.channel.send('Hello!') 

@client.tree.command(
    name="reset_role",
    description=config_ini.get('COMMAND_00', 'reset_role'))
async def remove_roles(interaction: discord.Interaction):
    guild_id = config_ini.getint('GUILD', 'guild_id')
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
    member = interaction.user
    await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'fuka')))
    await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'utsuho')))
    await member.remove_roles(guild.get_role(config_ini.getint('ROLE_ID', 'mantaro')))
    await interaction.response.send_message(config_ini.get('COMMAND_00', 'text'), ephemeral=True)
    embed = add_embed_simple(config_ini.get('COMMAND_00', 'title'), config_ini.get('COMMAND_00', 'description'), 
        int(config_ini.get('COLOR', 'roleReset_lightGray'),16), member)
    await member.send(embed=embed)
    print_info(member,config_ini.get('COMMAND_00', 'description'))

client.run(config_ini.get('TOKEN', 'token_test'))