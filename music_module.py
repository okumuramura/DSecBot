import re
import youtube_dl
import asyncio
from discord.ext import commands
from collections import deque
import discord

class MusicMod():
    def __init__(self):
        self.__url_pattern__ = re.compile(r"^https?://.+\..+$")
        self.youtube_dl_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'default_search': 'auto',
            # 'noplaylist': True,
            'nocheckcertificate': True
        }
        self.ffmpeg_options = {
            'options': '-vn'
        }

        self.ytdl = youtube_dl.YoutubeDL(self.youtube_dl_options)

    def is_url(self, query):
        return bool(self.__url_pattern__.match(query))

    async def yt_get_urls(self, query, loop = None):
        loop = loop or asyncio.get_event_loop() 
        urls = []
        line = "{0}{1}".format("ytsearch:" if not self.is_url(query) else "", query)
        data = await loop.run_in_executor(None, lambda : self.ytdl.extract_info(line, download = False))
        if "entries" in data:
            for file in data["entries"]:
                urls.append(file.get("webpage_url"))
        else:
            urls.append(data.get("webpage_url"))
        return urls

    @classmethod
    async def from_url(self, url, *, loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda : self.ytdl.extract_info(url, download = not stream))
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return self.YTSource(discord.FFmpegPCMAudio(filename, **self.ffmpeg_options), data=data)

    class YTSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=1):
            super().__init__(source, volume)

            self.data = data
            self.title = data.get('title')
            self.url = data.get('url')



class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue : deque
        self.queue = deque([])
        self.player = None
        self.current_play = ""

    def get_next(self):
        try:
            return self.queue.pop()
        except IndexError:
            return None
    
    @commands.command()
    async def join2(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()    
    async def next2(self, ctx):
        is_ok = False
        async with ctx.typing():
            data = self.get_next()
            if data is not None:
                is_ok = True
                self.player = await MusicMod.from_url(data, loop = self.bot.loop)
                ctx.voice_client.play(self.player, after = await self.next)
        if is_ok:
            await ctx.send('Сейчас играет: {}'.format(player.title))
        else:
            self.player = None
            await ctx.send("В очереди пусто :(")

    @commands.command()
    async def yt2(self, ctx, *, url):
        self.queue.append(MusicMod.yt_get_urls(url))
        if self.player is None:
            await self.next2(ctx)
            

    

if __name__ == "__main__":
    music = MusicMod()
    print(music.is_url("https://youtu.be/3GwjfUFyY6M"))
    # res = await music.yt_get_urls("https://www.youtube.com/watch?v=IgVtYWj-6Tw&list=PLEghovcPVHbvuhTdVVJnwVEVSpl0Zfn4v")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(music.yt_get_urls("https://r8---sn-jvhnu5g-bvwl.googlevideo.com/videoplayback?expire=1603136951&ei=VpmNX8iMOYqm7QShqJnoBg&ip=92.39.221.187&id=o-AJIygna6iHU4GEmXRX0Yk71ImhHHyZ48Cv3TvxTQBAK6&itag=251&source=youtube&requiressl=yes&mh=Hk&mm=31%2C29&mn=sn-jvhnu5g-bvwl%2Csn-jvhnu5g-n8vy&ms=au%2Crdu&mv=m&mvi=8&pl=24&initcwndbps=1777500&vprv=1&mime=audio%2Fwebm&gir=yes&clen=680500&dur=34.561&lmt=1541890260315064&mt=1603115209&fvip=8&keepalive=yes&fexp=23915654&c=WEB&txp=2301222&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgD6LFmourtRkOeVvjsXyIqYAfucRFozK2SSHAoRoOtz8CIQCUNW-1IDwS8KYcsNKzfU5NQQuNFo-6NY9o_tM6-R9D4A%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAISDRZEgMtO9j-G-B4RenpHulO2uEdkxJScQ6zSjDykfAiEAu6tG_sJY0FMIxWoV4CoOL41EH3m1VxluHOSp7uFYFaA%3D&ratebypass=yes"))