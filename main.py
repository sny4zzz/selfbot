import asyncio
import datetime
import functools
import io
import json
import os
import random
import re
import string
import urllib.parse
import urllib.request
import time
from urllib import parse, request
from itertools import cycle
from bs4 import BeautifulSoup as bs4

import aiohttp
import colorama
import discord
import numpy
import requests
from PIL import Image
from colorama import Fore
from discord.ext import commands
from discord.utils import get
from gtts import gTTS


colorama.init()
Client = discord.Client()
Client = commands.Bot(description='Selfbot', command_prefix="-", self_bot=True)
Client.remove_command("help")

languages = {
    'hu': 'Hungarian, Hungary',
    'nl': 'Dutch, Netherlands',
    'no': 'Norwegian, Norway',
    'pl': 'Polish, Poland',
    'pt-BR': 'Portuguese, Brazilian, Brazil',
    'ro': 'Romanian, Romania',
    'fi': 'Finnish, Finland',
    'sv-SE': 'Swedish, Sweden',
    'vi': 'Vietnamese, Vietnam',
    'tr': 'Turkish, Turkey',
    'cs': 'Czech, Czechia, Czech Republic',
    'el': 'Greek, Greece',
    'bg': 'Bulgarian, Bulgaria',
    'ru': 'Russian, Russia',
    'uk': 'Ukranian, Ukraine',
    'th': 'Thai, Thailand',
    'zh-CN': 'Chinese, China',
    'ja': 'Japanese',
    'zh-TW': 'Chinese, Taiwan',
    'ko': 'Korean, Korea'
}

locales = [
    "da", "de",
    "en-GB", "en-US",
    "es-ES", "fr",
    "hr", "it",
    "lt", "hu",
    "nl", "no",
    "pl", "pt-BR",
    "ro", "fi",
    "sv-SE", "vi",
    "tr", "cs",
    "el", "bg",
    "ru", "uk",
    "th", "zh-CN",
    "ja", "zh-TW",
    "ko"
]

m_numbers = [
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:"
]

m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]

print('Block 6 Selfbot')
print('Self bot is now on')
print('''██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
██████╔╝██║     ██║   ██║██║     █████╔╝ 
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ 
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
 ██████╗ 
██╔════╝ 
███████╗ 
██╔═══██╗
╚██████╔╝
 ╚═════╝ 
         
███████╗███████╗██╗     ███████╗██████╗  ██████╗ ████████╗
██╔════╝██╔════╝██║     ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
███████╗█████╗  ██║     █████╗  ██████╔╝██║   ██║   ██║   
╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗██║   ██║   ██║   
███████║███████╗███████╗██║     ██████╔╝╚██████╔╝   ██║   
╚══════╝╚══════╝╚══════╝╚═╝     ╚═════╝  ╚═════╝    ╚═╝   
                                                          ''')
print('-help for the commands')
print('-help general for the general commands')
print('-help raid for the raid commands')
print('-help nuke for the nuke commands')
print('-info about the selfbot and owner of the selfbot')

@Client.command()
async def snipe(ctx):
    await ctx.message.delete()
    currentChannel = ctx.channel.id
    if currentChannel in Client.sniped_message_dict:
        await ctx.send(Client.sniped_message_dict[currentChannel])
    else:
        await ctx.send("No message to snipe!")

@Client.event
async def on_message_delete(message):
    if message.author.id == Client.user.id:
        return
    if Client.msgsniper:
        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            attachments = message.attachments
            if len(attachments) == 0:
                message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + str(
                    message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                await message.channel.send(message_content)
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(message.author))) + "`: " + discord.utils.escape_mentions(
                    message.content) + "\n\n**Attachments:**\n" + links
                await message.channel.send(message_content)
    if len(Client.sniped_message_dict) > 1000:
        Client.sniped_message_dict.clear()
    attachments = message.attachments
    if len(attachments) == 0:
        channel_id = message.channel.id
        message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + str(
            message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
        Client.sniped_message_dict.update({channel_id: message_content})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = message.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(message.author))) + "`: " + discord.utils.escape_mentions(
            message.content) + "\n\n**Attachments:**\n" + links
        Client.sniped_message_dict.update({channel_id: message_content})

@Client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        await ctx.send('[ERROR]: You\'re missing permission to execute this command', delete_after=3)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"[ERROR]: Missing arguments: {error}", delete_after=3)
    elif isinstance(error, numpy.AxisError):
        await ctx.send('Invalid Image', delete_after=3)
    elif isinstance(error, discord.errors.Forbidden):
        await ctx.send(f"[ERROR]: 404 Forbidden Access: {error}", delete_after=3)
    elif "Cannot send an empty message" in error_str:
        await ctx.send('[ERROR]: Message contents cannot be null', delete_after=3)
    else:
        ctx.send(f'[ERROR]: {error_str}', delete_after=3)

@Client.command(aliases=["streaming"])
async def stream(ctx, *, message):
    await ctx.message.delete()
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/sny4zzz",
    )
    await Client.change_presence(activity=stream)


@Client.command(alises=["game"])
async def playing(ctx, *, message):
    await ctx.message.delete()
    game = discord.Game(
        name=message
    )
    await Client.change_presence(activity=game)


@Client.command(aliases=["listen"])
async def listening(ctx, *, message):
    await ctx.message.delete()
    await Client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=message,
        ))


@Client.command(aliases=["watch"])
async def watching(ctx, *, message):
    await ctx.message.delete()
    await Client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=message
        ))


@Client.command(aliases=["stopstreaming", "stopstatus", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()
    await Client.change_presence(activity=None, status=discord.Status.dnd)

@Client.command(aliases=['changehypesquad'])
async def hypesquad(ctx, house):
    await ctx.message.delete()
    request = requests.Session()
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
    }
    if house == "bravery":
        payload = {'house_id': 1}
    elif house == "brilliance":
        payload = {'house_id': 2}
    elif house == "balance":
        payload = {'house_id': 3}
    elif house == "random":
        houses = [1, 2, 3]
        payload = {'house_id': random.choice(houses)}
    try:
        request.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)

@Client.command(aliases=['tokinfo', 'tdox'])
async def tokeninfo(ctx, _token):
    await ctx.message.delete()
    headers = {
        'Authorization': _token,
        'Content-Type': 'application/json'
    }
    try:
        res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
        res = res.json()
        user_id = res['id']
        locale = res['locale']
        avatar_id = res['avatar']
        language = languages.get(locale)
        creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
            '%d-%m-%Y %H:%M:%S UTC')
    except KeyError:
        headers = {
            'Authorization': "Bot " + _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            language = languages.get(locale)
            creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
                '%d-%m-%Y %H:%M:%S UTC')
            em = discord.Embed(
                description=f"Name: `{res['username']}#{res['discriminator']} ` **BOT**\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`")
            fields = [
                {'name': 'Flags', 'value': res['flags']},
                {'name': 'Local language', 'value': res['locale'] + f"{language}"},
                {'name': 'Verified', 'value': res['verified']},
            ]
            for field in fields:
                if field['value']:
                    em.add_field(name=field['name'], value=field['value'], inline=False)
                    em.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")
            return await ctx.send(embed=em)
        except KeyError:
            await ctx.send("Invalid token")
    em = discord.Embed(
        description=f"Name: `{res['username']}#{res['discriminator']}`\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`")
    nitro_type = "None"
    if "premium_type" in res:
        if res['premium_type'] == 2:
            nitro_type = "Nitro Premium"
        elif res['premium_type'] == 1:
            nitro_type = "Nitro Classic"
    fields = [
        {'name': 'Phone', 'value': res['phone']},
        {'name': 'Flags', 'value': res['flags']},
        {'name': 'Local language', 'value': res['locale'] + f"{language}"},
        {'name': 'MFA', 'value': res['mfa_enabled']},
        {'name': 'Verified', 'value': res['verified']},
        {'name': 'Nitro', 'value': nitro_type},
    ]
    for field in fields:
        if field['value']:
            em.add_field(name=field['name'], value=field['value'], inline=False)
            em.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")
    return await ctx.send(embed=em)

@Client.command(aliases=["copyguild", "copyserver"])
async def copy(ctx):  # b'\xfc'
    await ctx.message.delete()
    await Client.create_guild(f'backup-{ctx.guild.name}')
    await asyncio.sleep(4)
    for g in Client.guilds:
        if f'backup-{ctx.guild.name}' in g.name:
            for c in g.channels:
                await c.delete()
            for cate in ctx.guild.categories:
                x = await g.create_category(f"{cate.name}")
                for chann in cate.channels:
                    if isinstance(chann, discord.VoiceChannel):
                        await x.create_voice_channel(f"{chann}")
                    if isinstance(chann, discord.TextChannel):
                        await x.create_text_channel(f"{chann}")
    try:
        await g.edit(icon=ctx.guild.icon_url)
    except:
        pass

@Client.command()
async def help(ctx, category=None):
   await ctx.message.delete()
   if category is None:
       embed=discord.Embed(color=0x36393f, timestamp=ctx.message.created_at)
       embed.set_title(name="Selfbot")
       embed.set_image(url="https://cdn.discordapp.com/attachments/783376581192056832/824973188676059146/ukdrill.gif")
       embed.add_field(name="𝘏𝘦𝘭𝘱 𝘈𝘤𝘤𝘰𝘶𝘯𝘵", value="𝘴𝘩𝘰𝘸𝘴 𝘵𝘩𝘦 𝘢𝘤𝘤𝘰𝘶𝘯𝘵 𝘤𝘰𝘮𝘮𝘢𝘯𝘥𝘴", inline=False)
       embed.add_field(name="𝘏𝘦𝘭𝘱 𝘎𝘦𝘯𝘦𝘳𝘢𝘭", value="𝘴𝘩𝘰𝘸𝘴 𝘵𝘩𝘦 𝘨𝘦𝘯𝘦𝘳𝘢𝘭 𝘤𝘰𝘮𝘮𝘢𝘯𝘥𝘴", inline=False)
       embed.add_field(name="𝘏𝘦𝘭𝘱 𝘙𝘢𝘪𝘥", value="𝘴𝘩𝘰𝘸𝘴 𝘵𝘩𝘦 𝘳𝘢𝘪𝘥 𝘤𝘰𝘮𝘮𝘢𝘯𝘥𝘴", inline=False)
       embed.add_field(name="𝘏𝘦𝘭𝘱 𝘕𝘶𝘬𝘦", value="𝘴𝘩𝘰𝘸𝘴 𝘵𝘩𝘦 𝘯𝘶𝘬𝘦 𝘤𝘰𝘮𝘮𝘢𝘯𝘥𝘴", inline=False)
       embed.add_field(name=" 𝘐𝘯𝘧𝘰", value="𝘪𝘯𝘧𝘰 𝘢𝘣𝘰𝘶𝘵 𝘵𝘩𝘦 𝘰𝘸𝘯𝘦𝘳 𝘰𝘧 𝘵𝘩𝘦 𝘴𝘦𝘭𝘧𝘣𝘰𝘵", inline=False)
       await ctx.send(embed=embed)


@Client.command()
async def account(ctx, category=None):
   await ctx.message.delete()
   if category is None:
       embed=discord.Embed(color=0x36393F, timestamp=ctx.message.created_at)
       embed=discord.Embed(title="Ready for some changes?")
       embed.add_field(name="Stream", value="-stream <words>", inline=False)
       embed.add_field(name="Play", value="-play <words>", inline=False)
       embed.add_field(name="Watch", value="-watch <words>", inline=False)
       embed.add_field(name="Listen", value="-listen <words>", inline=False)
       embed.add_field(name="Stopactivity", value="stops your watching, playing, streaming, or listening.")
       embed.add_field(name="Snipe", value="snipes a deleted message", inline=False)
       embed.add_field(name="Nitro", value="generates a random nitro code", inline=False)
       embed.add_field(name="Token", value="generates a random token", inline=False)
       embed.add_field(name="HypeSquad", value="changes the hypesquad (Bravery, Brilliance, and Balance)", inline=True)
       embed.add_field(name="DM", value="dms a mentioned user", inline=False)
       embed.add_field(name="DMAll", value="dms everyone in a server", inline=False)
       await ctx.send(embed=embed)
      
@Client.command()
async def general(ctx, category=None):
   await ctx.message.delete()
   if category is None:
       embed=discord.Embed(color=0x36393F, timestamp=ctx.message.created_at)
       embed.set_author(name="𝘚𝘩𝘰𝘸 𝘯𝘰 𝘔𝘦𝘳𝘤𝘺")
       embed.add_field(name="Uptime", value="shows how long the selfbot was running", inline=False)
       embed.add_field(name="Prefix ", value="changes the prefix to what you want", inline=False)
       embed.add_field(name="Whois", value="tells you the mentioned users info", inline=False)
       embed.add_field(name="Tokeninfo", value="shows info about a token", inline=False)
       embed.add_field(name="Serverinfo", value="shows info about the server", inline=False)
       embed.add_field(name="Copyserver", value="copys the server your in", inline=False)
       await ctx.send(embed=embed)

@Client.command()
async def raid(ctx, category=None):
   await ctx.message.delete()
   if category is None:
       embed=discord.Embed(color=0x36393F, timestamp=ctx.message.created_at)
       embed=discord.Embed(title="𝘉𝘭𝘰𝘤𝘬 6 𝘸𝘢𝘴 𝘩𝘦𝘳𝘦", color=0x36393f)
       embed.add_field(name="Spam", value="-spam (amount) (text)", inline=False)
       embed.add_field(name="@Everyone", value="mentions @everyone through a link", inline=False)
       embed.add_field(name="FakeWizz", value="makes a fake message about wizzing the server", inline=False)
       await ctx.send(embed=embed)


@Client.command()
async def nuke(ctx, category=None):
   await ctx.message.delete()
   if category is None:
       embed=discord.Embed(color=0x36393F, timestamp=ctx.message.created_at)
       embed=discord.Embed(title="𝘎𝘦𝘵 𝘳𝘦𝘢𝘥𝘺 𝘵𝘰 𝘧𝘶𝘤𝘬 𝘴𝘰𝘮𝘦𝘰𝘯𝘦𝘴 𝘴𝘦𝘳𝘷𝘦𝘳 𝘶𝘱 𝘨.")
       embed.add_field(name="Wizz", value="nukes the fuck out of your opps server", inline=False)
       embed.add_field(name="Masschannel", value="creates 250 channels", inline=False)
       embed.add_field(name="MassVC", value="creates 250 vc", inline=False)
       embed.add_field(name="Banall", value="bans everyone in your opps server", inline=False)
       embed.add_field(name="Kickall", value="kicks everyone in your opps server", inline=False)
       embed.set_footer(text="ggs")
       await ctx.send(embed=embed)
       

Client.run("TOKEN HERE")
