""" Bot to fetch current price of Solana and update status of bot to show current price """


import asyncio
import aiohttp
import discord

from dotenv import dotenv_values


client = discord.Client()

variables = dotenv_values(".env")


async def change(prev, curr):


    """ Finds percent change of two numbers """


    percent_change = round(((curr - prev) / prev) * 100, 2)


    return "(" + str(percent_change) + "%)"


async def get_price():


    """ Fetches current solana price from coingecko """


    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd&include_market_cap=false&include_24hr_vol=false&include_24hr_change=false&include_last_updated_at=false"


    async with aiohttp.ClientSession() as session:

        async with session.get(str(url)) as response:

            json = await response.json()


    return json["solana"]["usd"]


@client.event
async def on_ready():


    """ Main function for bot """


    previous = await get_price()


    while True:


        price = await get_price()

        percent_change = await change(previous, price)

        previous = price

        formatted_price = "$" + str(price) + " " + percent_change

        await client.change_presence(activity=discord.Game(formatted_price))

        await asyncio.sleep(300)


client.run(variables["PRICE_BOT"])
