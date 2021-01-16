from discord.ext import commands
import discord
import json
import random
import asyncio
import threading

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    if not message.guild:
        return '#'

    if message.guild and  str(message.guild.id) in prefixes.keys():
        return prefixes[str(message.guild.id)]
    else: 
        prefixes[str(message.guild.id)] = '.'

        with open('prefixes.json','w') as f:
            json.dump(prefixes,f,indent=4)

        return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix= get_prefix)

rps = ["rock","paper","scissors"]
rps_2 = ["rock","paper","scissors","r","p","s"]

def get_token():
    with open('token.json','r') as f:
        tokens = json.load(f)

    return tokens['token']

async def get_msg(member :discord.Member,ctx : discord.Message):
    try:
        msg=await client.wait_for('message',timeout=20,check=lambda message: message.author == member and message.channel == member.dm_channel)

        if msg.content == rps_2[0] or msg.content == rps_2[3]:
            choice = "rock :rock:"
        elif msg.content == rps[1] or msg.content == rps_2[4]:
            choice = "paper :newspaper2:"
        else:
            choice = "scissors :scissors:"

        await member.dm_channel.send(f"You have chosen {choice}\nNow back to <#{ctx.channel.id}>")
        return msg
    except asyncio.TimeoutError:
        return asyncio.TimeoutError

@client.event
async def on_ready():
    print(f"Started as {client.user}")

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json','w') as f:
        json.dump(prefixes,f,indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop([str(guild.id)])

    with open('prefixes.json','w') as f:
        json.dump(prefixes,f,indent=4)

@client.command(name='prefix')
async def change_prefix(ctx,prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json','w') as f:
        json.dump(prefixes,f,indent=4)

    await ctx.send(f"Prefix sucessfully changed to {prefix}")

@client.command(name='rps',aliases=['r','p','s'])
async def rock_paper_scissors(ctx, member : discord.Member = None):
    if member is None:
        q = random.randint(0, 255)
        p = random.randint(0, 255)
        r = random.randint(0, 255)
        embed = discord.Embed(title = "Choose your move in 20 seconds", description = "`rock`, `paper` or `scissors`", color=discord.Colour.from_rgb(r=q, g=p, b=r))
        sent = await ctx.send(embed=embed)

        try:
            msg = await client.wait_for("message",timeout=20,check = lambda message : message.author == ctx.author and message.channel == ctx.channel)

            if msg.content in rps_2:
                computer_move = random.choice(rps)
                if computer_move == rps[0]:
                    emoji = ":rock:"
                elif computer_move == rps[1]:
                    emoji = ":newspaper2:"
                else:
                    emoji = ":scissors:"

                lost = discord.Embed(title = "You Lost !!", description = f"Opponent threw {computer_move} {emoji}.", color = discord.Colour.from_rgb(r=q, g=p, b=r))
                win = discord.Embed(title = "You Won !!", description = f"Opponent threw {computer_move} {emoji}.", color = discord.Colour.from_rgb(r=q, g=p, b=r))
                draw = discord.Embed(title = "It's a draw.", description = f"Opponent threw {computer_move} {emoji}.", color = discord.Colour.from_rgb(r=q, g=p, b=r))

                if msg.content == rps_2[0] or msg.content == rps_2[3]:
                    if computer_move == rps[0]:
                        await ctx.send(embed=draw)
                    elif computer_move == rps[1]:
                        await ctx.send(embed=lost)
                    elif computer_move == rps[2]:
                        await ctx.send(embed=win)
                if msg.content == rps_2[1] or msg.content == rps_2[4]:
                    if computer_move == rps[0]:
                        await ctx.send(embed=win)
                    elif computer_move == rps[1]:
                        await ctx.send(embed=draw)
                    elif computer_move == rps[2]:
                        await ctx.send(embed=lost)
                if msg.content == rps_2[2] or msg.content == rps_2[5]:
                    if computer_move == rps[0]:
                        await ctx.send(embed=lost)
                    elif computer_move == rps[1]:
                        await ctx.send(embed=win)
                    elif computer_move == rps[2]:
                        await ctx.send(embed=draw)
            else:
                await ctx.send("No valid moves")

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("The bitch did not respond within time")

    elif member.id is ctx.author.id:
        await ctx.send("You cannot play with yourself.")

    else:
        await ctx.send("I have messeged you both. Check your dms")
        q = random.randint(0, 255)
        p = random.randint(0, 255)
        r = random.randint(0, 255)
        embed = discord.Embed(title = "Choose your move in 20 seconds", description = "`rock`, `paper` or `scissors`", color=discord.Colour.from_rgb(r=q, g=p, b=r))
        await ctx.author.send(embed=embed)
        await member.send(embed=embed)
        try:
            choice = None 
            choice1 = None

            loop = asyncio.get_event_loop()
            opponent, msg = loop.run_until_complete(asyncio.gather(get_msg(member,ctx),get_msg(ctx.author,ctx)))
            
            #opponent = await client.wait_for('message', check=lambda message: message.author == member and message.channel == member.dm_channel)
           
            #msg = await client.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.author.dm_channel)
            """
            while msg  or opponent:
                if msg:
                    if check:
                        if msg.content == rps_2[0] or msg.content == rps_2[3]:
                            choice = "rock :rock:"
                        elif msg.content == rps[1] or msg.content == rps_2[4]:
                            choice = "paper :newspaper2:"
                        else:
                            choice = "scissors :scissors:"

                        await ctx.author.dm_channel.send(f"You have chosen {choice}\nNow back to <#{ctx.channel.id}>")
                        check = False

                if opponent:
                    if check1:
                        if opponent.content == rps_2[0] or opponent.content == rps_2[3]:
                            choice1 = "rock :rock:"
                        elif opponent.content == rps[1] or opponent.content == rps_2[4]:
                            choice1 = "paper :newspaper2:"
                        else:
                            choice1 = "scissors :scissors:"

                        await member.dm_channel.send(f"You have chosen {choice1}\nNow back to <#{ctx.channel.id}>")
                        check1 = False
                if not check and not check1:
                     break
            """

            lost = discord.Embed(title = f"{member.mention} Won !!", description = f"{member.mention} threw {choice1} and {ctx.author.mention} threw {choice}.", color = discord.Colour.from_rgb(r=q, g=p, b=r))
            win = discord.Embed(title = f"{ctx.author.mention} Won !!", description = f"{member.mention} threw {choice1} and {ctx.author.mention} threw {choice}.", color = discord.Colour.from_rgb(r=q, g=p, b=r))
            draw = discord.Embed(title = "It's a draw.", description = f"{member.mention} threw {choice1} and {ctx.author.mention} threw {choice}.", color = discord.Colour.from_rgb(r=q, g=p, b=r))
                        
            if msg.content in rps_2 and opponent.content in rps_2:
                if msg.content == rps_2[0] or msg.content == rps_2[3]:
                    msg_emoji = ":rock:"
                elif msg.content == rps[1] or msg.content == rps_2[4]:
                    msg_emoji = ":newspaper2:"
                else:
                    msg_emoji = ":scissors:"

                if  opponent.content == rps_2[0] or opponent.content == rps_2[3]:
                    oppo_emoji = ":rock:"
                elif opponent.content == rps[1] or opponent.content == rps_2[4]:
                    oppo_emoji = ":newspaper2:"
                else:
                    oppo_emoji = ":scissors:"
                
                if msg_emoji == oppo_emoji:
                    await ctx.send(embed=draw)
                else:
                    if msg_emoji == ":rock:":
                        if oppo_emoji == ":paper":
                            await ctx.send(embed=lost)
                        elif oppo_emoji == ":scissors:":
                            await ctx.send(embed=win)
                    elif msg_emoji == ":paper:":
                        if oppo_emoji == ":rock:":
                            await ctx.send(embed=win)
                        elif oppo_emoji == ":scissors:":
                            await ctx.send(embed=lost)
                    elif msg_emoji == ":scissors:":
                        if oppo_emoji == ":paper":
                            await ctx.send(embed=lost)
                        elif oppo_emoji == ":rock:":
                            await ctx.send(embed=win)

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Someone did not respond in time")

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Argument required")
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You don't have the required permissions.")
    if isinstance(error,commands.MemberNotFound):
        await ctx.send("Member was not found.")
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("No such command found.")


client.run(get_token())
