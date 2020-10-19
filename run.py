import discord
from discord.ext import commands
import random
import re
import numpy as np
import pymorphy2 # Словарь
import weather as wth # Погода
import concurrent.futures # Потоки
from whoami import WAI # Игра кто я
import util # Доп функции
import money # Курс валют
import asyncio # Асинхронный вызов
import gun # Русская рулетка
import wiki as wikipedia
import youtube_dl
from music_module import MusicCog

TOKEN = "NzE3MTE1NjY2MDUzNzI2MjMw.XtVoDA.GQgmNXj_-MSsHfp4gkOF8XXAEwQ"

bot = commands.Bot(command_prefix="!")
morph = pymorphy2.MorphAnalyzer()

WhoAmI = WAI()

class ThrowEvent():
    def __init__(self, string, inp):
        self.string = string
        self.inp = inp

class Emoji:
    heartno   = "<:heartno:717115272766685216>"
    hearthalf = "<:hearthalf:717115255632822373>"
    heartfull = "<:hearthalf:717115233889550457>"
    catnolike = "<:catnolike:717123162424344654>"
    pressf    = "<:pressf:717111874730066041>"
    pepega    = "<:pepega:717107929274122291>"



random_events = [
    ThrowEvent("<@!{0.id}> кинул {1} в <@!{2.id}>", 3),
    ThrowEvent("<@!{0.id}> кинул {1} в <@!{2.id}>, но промахнулся.", 3),
    ThrowEvent("<@!{0.id}> кинул {1} в <@!{2.id}>, но {3} отскочил, и полетел обратно в <@!{0.id}>", 4),
    ThrowEvent("<@!{0.id}>, хватит кидаться! " + Emoji.catnolike, 1)
]

RussianGun = gun.Gun()

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))





@bot.command(pass_context=True)
async def check(ctx, *args):
    tf = bool(random.randint(0, 1))
    name = ctx.author.name
    ret_string = "{0}: {1} - {2}".format(name, " ".join(args), "удачно" if tf else "неудачно")
    await ctx.send(ret_string)

@bot.command(pass_context=False)
async def coin(ctx):
    await ctx.send("Орёл" if random.randint(0, 1) else "Решка")

@bot.command(pass_context=True)
async def throw(ctx, *args):
    random_throw = False
    if len(args) == 1:
        if re.match("^<@[!&]?\d+>$", args[0]):
            what = "снежок"
            member = args[0]
        else:
            what = args[0]
            member = np.random.choice(ctx.guild.members)
            random_throw = True
    elif len(args) == 2:
        what, member = args
    else:
        return
    try:
        word = morph.parse(what)[0]
        if word.score > 0.7:
            what_nomn = word.inflect({'nomn'}).word
            what_accs = word.inflect({"accs"}).word
        else:
            what_nomn = what
            what_accs = what
    except:
        what_nomn = what
        what_accs = what
    if not random_throw:
        if  re.match("^<@[!&]?\d+>$", member):
            member = int(member[re.search("^<@[!&]?", member).end():-1])
            member = ctx.guild.get_member(member)
        else:
            member = ctx.guild.get_member_named(member)
        if member != None:
            event = np.random.choice(random_events, p = [0.40, 0.40, 0.1, 0.1])
            fdata = [ctx.author, what_accs, member, what_nomn]
            ret_string = event.string.format(*fdata[:event.inp+1])
            await ctx.send(ret_string)
    else:
        if member.id == ctx.author.id:
            ret_string = "<@!{0.id}> кинул {1}, и попал сам в себя.".format(ctx.author, what_accs)
        else:
            ret_string = "<@!{0.id}> кинул {1}, и {2} в <@!{3.id}>".format(ctx.author, what_accs, "попал" if random.randint(0, 1) else "чуть не попал" ,member)
        await ctx.send(ret_string)

@bot.command(pass_context=True)
async def weather(ctx, *city):
    if len(city) > 0:
        city = " ".join(city)
    else:
        city = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(wth.get_weather, city)
        ret = future.result()
        await ctx.send(ret)
    
@bot.command(pass_context=True)
async def whoami(ctx, *answer):
    if len(answer) > 0:
        right = WhoAmI.get_user_answer(ctx.author.id)
        if right:
            answer = " ".join(answer)
            correct = util.check_words_correct(answer, right)
            if correct == 2:
                await ctx.send("<@!{0.id}>, верно, ваш персонаж: {1}\nПоздравляю!".format(ctx.author, right))
                WhoAmI.remove_person(ctx.author.id)
            elif correct == -1:
                await ctx.send("<@!{0.id}>, неверно".format(ctx.author))
            elif correct == 0:
                await ctx.send("<@!{0.id}>, видимо в вашем ответе опечатка".format(ctx.author))
            else:
                await ctx.send("<@!{0.id}>, введите полный ответ, пожалуйста".format(ctx.author))
        else:
            await ctx.send('<@!{0.id}>, видимо вы ещё не начали игру.\nДля того чтобы начать напишите "!whoami" без аргументов.'.format(ctx.author))
    
    else:
        character = WhoAmI.get_object()
        for member in ctx.guild.members:
            if member.id != ctx.author.id and not member.bot:
                await member.send('<@!{0.id}> начал игру "Кто я?"\nЕго персонаж: {1}, помогите <@!{0.id}> его отгадать.'.format(ctx.author, character))
        WhoAmI.add_person(ctx.author.id, character)
        await ctx.send("<@!{0.id}>, ваша игра началась!\nДругие пользователи знают, кто вы, задавайте им вопросы.\nДля ответа напишите \"!whoami $Ваш вариант ответа$ (кириллица)\nПриятной игры!".format(ctx.author))


@bot.command(pass_context=True)
async def usd(ctx, value = None):
    if value == None:
        ret_string = money.get_usd()
        await ctx.send(ret_string)
    elif value.isdigit():
        ret_string = money.get_usd(value)
        await ctx.send(ret_string)
    else:
        await ctx.send("<@!{0.id}>, только цифры, ну!".format(ctx.author))

@bot.command(pass_context=True)
async def eur(ctx, value = None):
    if value == None:
        ret_string = money.get_eur()
        await ctx.send(ret_string)
    elif value.isdigit():
        ret_string = money.get_eur(value)
        await ctx.send(ret_string)
    else:
        await ctx.send("<@!{0.id}>, только цифры, ну!".format(ctx.author))

@bot.command(pass_context=True)
async def checkhp(ctx, user = None):
    user_id = ctx.author.id
    if user != None:
        if re.match("^<@[!&]?\d+>$", user):
            user = int(user[re.search("^<@[!&]?", user).end():-1])
            user = ctx.guild.get_member(user)
            user_id = user.id
    hp = 1
    
    message = await ctx.send(util.gen_hp(Emoji, user_id, 0))
    while (random.randint(0, 4) != 0 and hp <= 10):
        await message.edit(content = util.gen_hp(Emoji, user_id, hp))
        await asyncio.sleep(2)
        hp+=1
    await message.edit(content = util.gen_hp(Emoji, user_id, hp-1) + "!")

@bot.command(pass_context=True)
async def gun(ctx, reload = None):
    if reload == "reload":
        RussianGun.reload()
        await ctx.send("Револьвер перезаряжен!")
        return
    if RussianGun.shot():
        msg = await ctx.send("Бах!\n" + RussianGun.kill().format(ctx.author))
        emoji = bot.get_emoji(717111874730066041)
        RussianGun.reload()
        await msg.add_reaction(emoji)
    else:
        await ctx.send("Щелк!\n" + RussianGun.miss().format(ctx.author))
        
@bot.command(pass_context = True)
async def wiki(ctx, *query):
    if len(query) > 0:
        query = " ".join(query)
    else:
        query = "Википедия"
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(wikipedia.summary, query)
        result = future.result()
    if result != None:
        await ctx.send("{1.title}\n{0}\n{1.url}".format(*result))
    else:
        await ctx.send('<@!{0.id}>, по запросу "{1}" ничего не найдено. {2}'.format(ctx.author, query, Emoji.pepega))



# WTF!!!

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else self.stop(ctx))

        await ctx.send('Сейчас играет: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else self.stop(ctx))

        await ctx.send('Сейчас играет: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Сейчас играет: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Не подключен к голосовому каналу")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Громкость изменена: {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Для использования этой команды присоеденитесь к голосовому каналу.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot.add_cog(Music(bot))
bot.add_cog(MusicCog(bot))
bot.run(TOKEN)