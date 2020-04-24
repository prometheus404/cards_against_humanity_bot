# bot.py
import os
import numpy as np
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

################################GAME CLASSES#############################################

class Game:
	def __init__(self):
		self.fileName = "ita"
		self.handSize = 10
		self.maxScore = 8
		self.cardCzar=0
		self.deck = None
		self.players = []
		self.cardsPlayed = []
		self.blackCardPlayerd = None
		self.expectedCards = False
	def reset(self):
		self.handSize = 10
		self.maxScore = 8
		self.cardCzar=0
		self.deck = None
		self.players = []
		self.cardsPlayed = []
		self.blackCardPlayerd = None
		self.expectedCards = False
	def create_deck(self):
		whiteCards=[]
		blackCards=[]
		file = open(self.fileName, 'r')
		x = file.readline()
		while '@@' not in x and x:
			blackCards.append(x)
			x = file.readline()
		x=file.readline()
		while x:
			whiteCards.append(x)
			x = file.readline()
		self.deck = Deck(whiteCards, blackCards)

	def add_deck(self, secondDeckFile):
		whiteCards=[]
		blackCards=[]
		file = open(secondDeckFile, 'r')
		x = file.readline()
		while '@@' not in x and x:
			blackCards.append(x)
			x = file.readline()
		x=file.readline()
		while x:
			whiteCards.append(x)
			x = file.readline()
		self.deck.add_cards(whiteCards, blackCards)

	def draw_black(self):
		self.blackCardPlayerd = self.deck.draw_black()
		self.expectedCards = self.blackCardPlayerd.count('_')
		if self.expectedCards == 0:
			self.expectedCards = 1
		return self.blackCardPlayerd

	def create_player(self, id):
		whiteCards = [self.deck.draw_white()]
		for i in range(1, self.handSize):
			whiteCards.append(self.deck.draw_white())
		self.players.append(Player(id,whiteCards))

	def shuffle_deck(self):
		self.deck.shuffle()

	def init_players(self, playersId):
		for i in playersId:
			print(i)
			self.create_player(i)
		np.random.shuffle(self.players)

	def next_czar(self):
		self.cardCzar = (self.cardCzar + 1) % len(self.players)

	def plays(self, playerId, card):	#obsoleta
		if playerId == self.players[self.cardCzar].id:
			return False
		for i in self.cardsPlayed:
			if i[0] == playerId:
				return False
		for i in self.players:
			print(i.id)
			if i.id == playerId:
				print(i.id)
				self.cardsPlayed.append([playerId, i.cards[card]])
				i.play(i.cards[card])
				i.draw(self.deck.draw_white())
		return True

	def plays_cards(self, playerId, cards):
		if playerId == self.players[self.cardCzar].id:
			return
		for i in self.cardsPlayed:
			if i[0] == playerId:
				return
		for i in self.players:
			if i.id == playerId:
				print(i.id)
				result = []
				delta = 0
				for j in cards:
					result.append(i.cards[int(j)])	#sostituisce ogni istanza di cards con la stringa corrispondente
				self.cardsPlayed.append([playerId, ''.join(['~'+x for x in result])])

				for j in result:
					i.play(j)
					i.draw(self.deck.draw_white())
		return True


	def randomize(self):
		np.random.shuffle(self.cardsPlayed)

	def vote(self, cardIndex):
		for i in self.players:
			if i.id == self.cardsPlayed[cardIndex][0]:
				i.score += 1
		self.cardsPlayed = []   #clear cards played

	def reached_max_score(self):
		if not self.players:
			return None
		for i in self.players:
			if i.score == self.maxScore:
				return i.id
		return False

class Deck:
    def __init__(self, whiteCards, blackCards):
        self.whiteCards = whiteCards
        self.blackCards = blackCards
    def add_cards(self, newWhiteCards, newBlackCards):
        self.whiteCards = self.whiteCards + newWhiteCards
        self.blackCards = self.blackCards + newBlackCards
    def shuffle(self):
        np.random.shuffle(self.whiteCards)
        np.random.shuffle(self.blackCards)
    def draw_white(self):
        card = self.whiteCards[0]
        self.whiteCards.pop(0)
        return card
    def draw_black(self):
        card = self.blackCards[0]
        self.blackCards.pop(0)
        return card

class Player:
    def __init__(self, id, cards):
        self.id = id
        self.cards = cards
        self.score = 0
    def play(self, card):
        self.cards.remove(card)
    def draw(self, card):
        self.cards.append(card)

client = commands.Bot(command_prefix='$')

#################################GLOBAL VARIABLES########################################
class Instance:
	def __init__(self):
		self.game = Game()
		self.players = []
		self.expansions = []

instances = {}
#################################FORMATTING FUNCTIONS####################################
def format_black(string):
	return '```'+string+'```'
def format_white_public(black, cards):
	string ='```asciidoc\n' + black +'\n= cards played this turn =\n'
	x = 0
	for i in cards:
		string += str(x)+':: '+ i[1]
		x += 1
	return string+' \n```'
def format_white_private(black, cards):
	string ='```asciidoc\n' + black +'\n= your cards =\n'
	x = 0
	for i in cards:
		string += str(x)+':: '+ i
		x += 1
	return string+' \n```'
def format_scoreboard(players):
	string = '```asciidoc\n= scoreboard =\n'
	for i in players:
		string += str(i.id) + '::    ' + str(i.score) + '\n'
	return string+" \n```"
def format_player_list(players):
	string = '```asciidoc\n= players =\n'
	for i in players:
		string += '* ' + str(i) + '\n'
	return string+"```"
####################################COMMANDS#############################################

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
    	print(f'{guild.name}(id: {guild.id})')

@client.command(name='new')
async def new_game(ctx):
	if ctx.guild.id not in instances:
		instances[ctx.guild.id] = Instance()
		await ctx.send("you summoned me... wanna play? :)")
	else:
		await ctx.send("there is another instance open for this server close it with !exit")

@client.command(name='exit')
async def exit_game(ctx):
	if ctx.guild.id in instances:
		instances.pop(ctx.guild.id)
		await ctx.send('see u')
	else:
		await ctx.send('I am not playing with you')

@client.command(name='deck')
async def set_deck(ctx, deckName):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	if deckName:
		game.fileName = deckName
		await ctx.send('done')

@client.command(name="score")
async def set_score(ctx, score):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	if score > 0:
		game.score = score
		await ctx.send('done')

@client.command(name='start')
async def start(ctx):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	players = instances[ctx.guild.id].players
	game = instances[ctx.guild.id].game
	expansions = instances[ctx.guild.id].expansions
	if not players:
		await ctx.send("first find some friends (!join)")
		return
	if len(players) < 3:
		await ctx.send("first find some friends (!join)")
		return
	game.reset()
	try:
		game.create_deck()
	except Exception as e:
		await ctx.send('select a valid deck')
	if expansions:
		for i in expansions:
			game.add_deck(i)
	game.shuffle_deck()
	game.init_players(players)
	print(players)
	players.clear()
	print(game.players)
	await turn(ctx, game)

async def turn(ctx, game):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	await ctx.send('next czar: ' + game.players[game.cardCzar].id.mention)
	card = format_black(game.draw_black())
	await ctx.send(card)
	for i in game.players:
		#invia in privato le sue carte
		await i.id.create_dm()
		await i.id.dm_channel.send(format_white_private(game.blackCardPlayerd, i.cards))

@client.command(name='play')
async def play_card(ctx, *cards):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	for i in cards:
		if int(i) >= game.handSize:
			await ctx.send('play one of your cards')
			return
	if len(cards) != game.expectedCards:
		await ctx.send("this is not the right number of cards")
		return
	for i in game.players:
		if i.id == ctx.author:
			if not game.plays_cards(i.id, cards):	#collateral effect to play cards
				await ctx.send("you can't play cards until the end of this turn")

	if len(game.cardsPlayed) >= len(game.players) - 1:
		game.randomize()
		game.expectedCards = False
		print(game.cardsPlayed)
		print(len(game.cardsPlayed))
		await ctx.send(format_white_public(game.blackCardPlayerd, game.cardsPlayed))

@client.command(name='join')
async def join(ctx):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	players = instances[ctx.guild.id].players
	if ctx.author not in players:
		players.append(ctx.author)
		print(players)
		await ctx.send(format_player_list(players))

@client.command(name='refresh')
async def refresh_players(ctx):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	players = instances[ctx.guild.id].players
	for i in players:	#TODO controlla che non inserisca due volte
		game.create_player(i)
	for i in game.players:
		#invia in privato le sue carte
		await i.id.create_dm()
		await i.id.dm_channel.send(format_white_private(game.blackCardPlayerd, i.cards))

@client.command(name='vote')
async def vote(ctx, card):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	if game.expectedCards:
		await ctx.send('shut up and wait for your turn!')
		return
	if ctx.author != game.players[game.cardCzar].id:
		await ctx.send("Come on, you're not the czar")
		return
	if int(card) >= len(game.players):
		await ctx.send('I know, these cards sucks, but you have to vote one of them')
		return
	game.vote(int(card))
	game.next_czar()
	await ctx.send(format_scoreboard(game.players))
	if game.reached_max_score():
		print(game.reached_max_score())
		await ctx.send('the winner is: '+str(game.reached_max_score()))
		return
	await turn(ctx, game)

@client.command(name='skip')
async def skip(ctx):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	if game.expectedCards:
		game.randomize()
		game.expectedCards = False
		print(game.cardsPlayed)
		print(len(game.cardsPlayed))
		await ctx.send(format_white_public(game.blackCardPlayerd, game.cardsPlayed))
		if game.expectedCards == 0:
			await turn(ctx, game)
	else:
		await ctx.send("you can't skip voting phase")

@client.command(name='restart')
async def restart(ctx):
	if ctx.guild.id not in instances:
		await ctx.send('first create a game with !new')
		return
	game = instances[ctx.guild.id].game
	game.reset()


#########################################################################################
client.run(TOKEN)
