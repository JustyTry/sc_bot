import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from emission import *
from pricecheck import *
import asyncio
import random
import sqlite3


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


lots_id = {"y4y33": "лямбда блок",
           "dr61j": "бета блок",
           "y409k": "гамма блок",
           "191w2": "дигамма блок",
           "2opw0": "прем 30 дней",
           "3gv2z": "прем 90 дней",
           "7l9d3": "прем 180 дней",
           "4qldn": "тонга",
           "ok096": "Аметист",
           "1rkn1": "магнит",
           "49dj": "берлога 6у",
           "j3ml": "ксм",
           "qj2zk": "aa-12",
           "qjwv3": "барабан aa-12",
           "4qnwn": "шторм",
           "qjr43": "fortis black",
           "knw1p": "fortis orange",
           "gn975": "Портативный квантовый генератор",
           "olz36": "Моток медной проволоки",
           "gnpr5": "Темный Лим",
           "z3ogm": "Расцветший Горьколистник"}

# Набор приветствий
starter_greetings = starter_greetings = [
    "присоединился к мучениям",
    "стал мученником",
    "замученной дорогой выбился из сил и на сервер угодил",
    "мученник нарисовался"
]


def run_discord_bot():
    # Приветствие и занесение в базу
    @client.event
    async def on_member_join(member):
        con = sqlite3.connect("./database/bd.db")
        cur = con.cursor()
        greetingChannel = client.get_channel(1081559920148742195)
        role = discord.utils.get(member.guild.roles, id=1081569713970216970)
        await member.add_roles(role)
        await greetingChannel.send(f"{member.mention} {random.choice(starter_greetings)}")
        con.close()

# Начисление опыта за длину сообщений
    @client.event
    async def on_message(message):
        con = sqlite3.connect("./database/bd.db")
        cur = con.cursor()
        if message.author == client.user:
            return
        try:
            author = message.author.id
            prev_exp = cur.execute(
                """SELECT member_exp FROM members WHERE member_id=?""", (author,)).fetchone()
            exp = len(message.clean_content) + int(prev_exp[0])
            cur.execute(
                """UPDATE members SET member_exp=? WHERE member_id=?""", (exp, author,))
            con.commit()
        except:
            print(f'{message.author} нет в базе', message.author.id)

        con.close()
# Проверка на выброс

    @tasks.loop(seconds=1000)
    async def compareLoop():
        channel = client.get_channel(1146371967428071495)
        if compareTime():
            await channel.send('Выброс начался!')
            await asyncio.sleep(600)
        else:
            print("not now")

    @tasks.loop(seconds=120)
    async def pricecheckLoop():
        channel = client.get_channel(1146148119818543169)
        for id in lots_id.keys():
            if comparePrice(id):
                data = comparePrice(id)
                await channel.send(f"{sorted(data[0])}\n средняя - {data[1]}\n медиана - {data[2]} \n название - {lots_id[id]}")
            else:
                continue

    @client.event
    async def on_ready():
        print(f'{client.user} is running')
        pricecheckLoop.start()
        compareLoop.start()

    client.run(TOKEN)
