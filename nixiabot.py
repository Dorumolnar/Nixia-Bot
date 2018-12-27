import discord
import asyncio
import urllib
import datetime
import requests
import youtube_dl
import subprocess
import datetime
from datetime import timezone
import threading
import re

file = open('./botstuff/gdpssecret.txt', 'r')
gdpssecret = file.read()

def transferpermsMultithread(members,members2):
    for member in members:
        transferperms(member)
    
def transferperms(person):
    messagething = ""
    for i, val in enumerate(person.roles):
        messagething += val.id + ","
    messagething = messagething[:-1]
    print(messagething)
    print("http://owo0geometrydashnixia.tk/database/tools/bot/discordLinkTransferRoles.php?roles="+messagething+"&discordID="+str(person.id)+"&secret="+gdpssecret)
    return urllib.request.urlopen("http://owo0geomemtrydashnixia.tk/database/tools/bot/discordLinkTransferRoles.php?roles="+messagething+"&discordID="+str(person.id)+"&secret="+gdpssecret).read().decode('UTF-8')

def songUpload(song,message,client):
    msg = client.send_message(message.channel, 'Downloading song, please wait')
    options = {
        'format': 'bestaudio/best', # choice of quality
        'extractaudio' : True,      # only keep the audio
        'audioformat' : "mp3",      # convert to mp3 
        'outtmpl': '/var/www/songcdn/temp/%(id)s',        # name the file the ID of the video
        'noplaylist' : True,        # only download single song, not playlist
        } 
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([song])
        r = ydl.extract_info(song, download=False)
    client.edit_message(msg, 'Reuploading ' + r['id'] + " - " + r['title'] + " by " + r['uploader'])
    subprocess.run(['avconv','-i','/var/www/songcdn/temp/'+r['id'],'-n','-c:a','libmp3lame','-ac','2','-b:a','190k','/var/www/songcdn/'+r['id']+".mp3"])
    link = "http://songcdn.michaelbrabec.cz:9010/"+r['id']
    link = urllib.parse.quote_plus(link)
    title = urllib.parse.quote_plus(r['title'])
    uploader = urllib.parse.quote_plus(r['uploader'])
    songid = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/songAddBot.php?link="+link+".mp3&name="+title+"&author="+uploader).read().decode('UTF-8')
    print('SongID: '+songid+"\r\nReuploaded " + r['id'] + " - " + title + " by " + uploader)
    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    await client.change_presence(game=discord.Game(name='Online - ' + str(datetime.datetime.now())))
    if message.content.startswith('!'):
        print(message.content)
    if message.author.id == "259732376303697920":
        pass
    elif message.content.startswith('!isuo'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!isup'):
        await client.send_message(message.channel, 'I am online!')
    elif message.content.startswith('!level'):
        level = message.content.replace("!level ","")
        level = urllib.parse.quote_plus(level)
        levelinfo = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/levelSearchBot.php?str="+level).read().decode('UTF-8')
        await client.send_message(message.channel, levelinfo)
    elif message.content.startswith('!userlevels'):
        userlevels = message.content.replace("!userlevels ","")
        levelinfo = requests.post("http://owo0geometrydashnixiatk/database/tools/bot/userLevelSearchBot.php", data={'str': userlevels}, headers={'User-Agent': "CvoltonGDPS"})
        await client.send_message(message.channel, levelinfo.text)
    elif message.content.startswith('!links'):
        file = open('/home/pi/Desktop/botstuff/links.txt', 'r')
        await client.send_message(message.channel, file.read())
    elif message.content.startswith('!help'):
        file = open('/home/pi/Desktop/botstuff/help.txt', 'r')
        await client.send_message(message.channel, file.read())
    elif message.content.startswith('!download'):
        file = open('/home/pi/Desktop/botstuff/latest.txt', 'r')
        await client.send_message(message.channel, file.read())
    elif message.content.startswith('!songlist'):
        pg = message.content.replace("!songlist ","")
        songinfo = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/songListBot.php?page="+pg).read().decode('UTF-8')
        await client.send_message(message.channel, songinfo)
    elif message.content.startswith('!searchsong'):
        query = message.content.replace("!searchsong ","")
        query = urllib.parse.quote_plus(query)
        songinfo = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/songSearchBot.php?str="+query).read().decode('UTF-8')
        await client.send_message(message.channel, songinfo)
    elif message.content.startswith('!whorated'):
        query = message.content.replace("!whorated ","")
        rate = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/whoRatedBot.php?level="+query).read().decode('UTF-8')
        await client.send_message(message.channel, rate)
    elif message.content.startswith('!player'):
        query = message.content.replace("!player ","")
        query = urllib.parse.quote_plus(query)
        player = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/playerStatsBot.php?player="+query).read().decode('UTF-8')
        await client.send_message(message.channel, player)
    elif message.content.startswith('!top'):
        query = message.content.replace("!top ","")
        split = query.split(' ')
        try:
            type = split[0]
        except:
            type = "none"
        try:
            page = split[1]
        except:
            page = "0"
        
        leaderboards = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/leaderboardsBot.php?type="+type+"&page="+page).read().decode('UTF-8')
        await client.send_message(message.channel, leaderboards)
    elif message.content.startswith('!mods'):
        mods = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/modActionsBot.php").read().decode('UTF-8')
        await client.send_message(message.channel, mods)
    elif message.content.startswith('!daily'):
        daily = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/dailyLevelBot.php").read().decode('UTF-8')
        await client.send_message(message.channel, daily)
    elif message.content.startswith('!time'):
        time = datetime.datetime.now()
        await client.send_message(message.channel, time)
    elif message.content.startswith('!server'):
        tmp = await client.send_message(message.channel, 'Attempting to connect to servers...')
        answer = "CvoltonGDPS\r\n```"
        await client.edit_message(tmp, answer + "```")
        answer = answer + getStatus("http://owo0geometrydashnixia.tk/database/downloadGJLevel22.php","\r\n     Nixia")
    elif message.content.startswith('!songreup'):
        song = message.content.replace("!songreup ","")
        ReupThread = threading.Thread(target=songUpload,args=(song,message,client))
        ReupThread.start()
        leaderboards = urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/latestSongBot.php").read().decode('UTF-8')
        await client.send_message(message.channel, "Check SongID "+leaderboards+" in a few minutes")
    elif message.content.startswith('!linkacc'):
        account = message.content.replace("!linkacc ","")
        await client.send_message(message.channel, urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/discordLinkReq.php?account="+account+"&discordID="+str(message.author.id)+"&secret="+gdpssecret).read().decode('UTF-8'))
    elif message.content.startswith('!unlinkacc'):
        account = message.content.replace("!unlinkacc ","")
        await client.send_message(message.channel, urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/discordLinkUnlink.php?discordID="+str(message.author.id)+"&secret="+gdpssecret).read().decode('UTF-8'))
    elif message.content.startswith('!resetpassword'):
        await client.send_message(message.channel, urllib.request.urlopen("http://owo0geometrydashnixia.tk/database/tools/bot/discordLinkResetPass.php?discordID="+str(message.author.id)+"&secret="+gdpssecret).read().decode('UTF-8'))
    elif message.content.startswith('!listroles'):
        for i, val in enumerate(message.author.roles):
            await client.send_message(message.channel, str(val.id) + " : " + val.name)
    elif message.server.id == "267761099951046656":
        if message.content.startswith('!transferperms'):
            person = message.author
            if '<@' in message.content:
                personid = message.content.split('<@')[1]
                personid = personid.split('>')[0]
                non_decimal = re.compile(r'[^\d.]+')
                personid = non_decimal.sub('', personid)
                print(personid)
                person = message.server.get_member(personid)
            await client.send_message(message.channel, "Transferring roles")
            await client.send_message(message.channel, transferperms(person))
        elif message.content.startswith('!listmembers'):
            await client.send_message(message.channel, "bot gonna lag now lol prenk")
            timebeforelag = datetime.datetime.now(tz=timezone.utc).timestamp()
            TransferThread = threading.Thread(target=transferpermsMultithread,args=(message.server.members,message.server.members))
            TransferThread.start()
            timeafterlag = datetime.datetime.now(tz=timezone.utc).timestamp()
            finaltime = str(timeafterlag - timebeforelag)
            await client.send_message(message.channel, "done, " + finaltime + "s")

file = open('./botstuff/token.txt', 'r')
client.run(file.read())
