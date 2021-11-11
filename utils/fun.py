from discord.ext import commands
from discord import Embed
import requests
import asyncio
import random
from bs4 import BeautifulSoup


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='joke',
                      brief='Let me tell you a joke',
                      description='-> ".joke" - generates a random joke')
    async def joke(self, ctx):
        url = 'https://official-joke-api.appspot.com/random_joke'
        joke = requests.get(url).json()

        await ctx.send(joke["setup"])
        await asyncio.sleep(2)
        await ctx.send(joke['punchline'])

    @commands.command(name='fact',
                      brief='Do you know that ...?',
                      description='-> ".fact" - generates a random fact')
    async def fact(self, ctx):
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        fact = requests.get(url).json()

        embed = Embed(color=0x2ca5f1)
        embed.add_field(name="Random useless fact", value=fact['text'])

        await ctx.send(embed=embed)

    @commands.command(name='roll',
                      brief='Roll a dice',
                      description='-> ".roll" - rolls a dice \n'
                                  '-> ".roll [number]" - rolls specific number of dice')
    async def roll(self, ctx, number_of_dice=None):
        try:
            number_of_dice = int(number_of_dice)
        except ValueError and TypeError:
            number_of_dice = 1

        numbers = {1: ':one:', 2: ':two:', 3: ':three:', 4: ':four:', 5: ':five:', 6: ':six:'}
        results = ''
        for i in range(number_of_dice):
            results += str(numbers[random.randint(1, 6)]) + ', '

        embed = Embed(color=0x2ca5f1)
        embed.add_field(name='%s, you rolled: ' % ctx.message.author.name, value=results[:-2])

        await ctx.send(embed=embed)

    @commands.command(name='randint',
                      brief='Get a random number',
                      description='-> ".randint" - generates randomly 0 or 1 \n'
                                  '-> ".randint [min] [max]" - generates a random number in a given interval')
    async def randint(self, ctx, bottom=0, top=1):
        if top < bottom:
            result = ':no_entry: The second number should be higher or equal than the first one.'
            embed = Embed(color=0xff0000)
            embed.add_field(name='%s, error: ' % ctx.message.author.name, value=result)
        else:
            bottom, top = int(bottom), int(top)
            result = str(random.randint(bottom, top))
            embed = Embed(color=0x2ca5f1)
            embed.add_field(name='%s, your random number: ' % ctx.message.author.name, value=result)

        await ctx.send(embed=embed)

    @commands.command(name='randword',
                      brief='Get a random word',
                      description='-> ".randword" - generates a random word')
    async def randword(self, ctx):
        url = 'https://random-words-api.vercel.app/word'
        response = requests.get(url).json()[0]
        embed = Embed(title=response['word'], description=response['definition'], color=0x2ca5f1)

        await ctx.send(embed=embed)

    @commands.command(name='flip',
                      brief='Flip a coin',
                      description='-> ".flip" - flips a coin')
    async def flip(self, ctx):
        embed = Embed(title='%s, your result: ' % ctx.message.author.name,
                      description=random.choice(['tails', 'heads']), color=0x2ca5f1)

        await ctx.send(embed=embed)

    @commands.command(name='cat',
                      brief='Do you want to see cute cats?',
                      description='-> ".cat" - shows a random image of a cute cat',
                      aliases=['kitty'])
    async def cat(self, ctx):
        url = 'https://cataas.com/cat?json=true'
        response = requests.get(url).json()
        embed = Embed(title=':cat: Kitty!', color=0x2ca5f1)
        embed.set_image(url='https://cataas.com/' + response['url'])
        await ctx.send(embed=embed)

    @commands.command(name='dog',
                      brief='Do you want to see cute dogs?',
                      description='-> ".dog" - shows a random image of a cute dog')
    async def dog(self, ctx):
        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url).json()
        embed = Embed(title=':dog: Doggy!', color=0x2ca5f1)
        embed.set_image(url=response['message'])
        await ctx.send(embed=embed)

    @commands.command(name='word',
                      brief='Let me tell you the word of the day',
                      description='-> ".word" - returns the words of the day')
    async def word(self, ctx):
        url = 'https://www.urbandictionary.com/'
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')
        word = soup.find('div', class_='def-header').text
        meaning = soup.find('div', class_='meaning').text.encode('ascii', 'ignore')

        embed = Embed(title="Word of the day: " + word, description=meaning.decode('utf-8'), color=0x2ca5f1)

        await ctx.send(embed=embed)

    @commands.command(name='meme',
                      brief='Let\'s laugh together',
                      description='-> ".meme" - sends a funny meme',
                      aliases=['memes', 'mem'])
    async def meme(self, ctx):
        url = 'https://meme-api.herokuapp.com/gimme'
        response = requests.get(url).json()
        embed = Embed(title='Here you are!', color=0x2ca5f1)
        embed.set_image(url=response['url'])
        await ctx.send(embed=embed)

    @commands.command(name='ping',
                      description='-> ".ping" - shows bot latency')
    async def ping(self, ctx):
        embed = Embed(title='Latency: ', description='%s ms' % (round(self.client.latency, 4)*1000), color=0x2ca5f1)
        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = Embed(color=0xff0000)
            embed.add_field(name='Error', value=':no_entry: I can\'t play with you right now. Please try again later.')

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
