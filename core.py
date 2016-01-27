from flask import Flask, redirect, render_template, request, send_file, Markup
import sqlite3 as lite
import time
import os, subprocess
import random, string, calendar, base64, sys
from random import shuffle
#############################################
#                   Carbon                  #
#          Back-bone that supplies          #
#              this entire app              #
#                By Photonic                #
#############################################

#Make sure Flask is using the correct template path when running on Gevent
#Most likely not needed for this but keeping it
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__,template_folder=tmpl_dir)
sessions = {}

cards = ["c10",
	"c2",
	"c3",
	"c4",
	"c5",
	"c6",
	"c7",
	"c8",
	"c9",
	"ca",
	"cb10",
	"cb2",
	"cb3",
	"cb4",
	"cb5",
	"cb6",
	"cb7",
	"cb8",
	"cb9",
	"cba",
	"cbj",
	"cbk",
	"cbq",
	"cj",
	"ck",
	"cq",
	"d10",
	"d2",
	"d3",
	"d4",
	"d5",
	"d6",
	"d7",
	"d8",
	"d9",
	"da",
	"dj",
	"dk",
	"dq",
	"h10",
	"h2",
	"h3",
	"h4",
	"h5",
	"h6",
	"h7",
	"h8",
	"h9",
	"ha",
	"hj",
	"hk",
	"hq"]

card_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']

def initalizeSession(sessionID, username):
	sessions[sessionID] = { 
				'users' :
					{
						username : []
					},
				'table_cards' : [],
				'current_turn' : username,
				'current_card' : '2',
				'status' : 'Waiting for more players..',
				'previous_player' : None,
				'previous_card' : None
				}

def chunkify(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

def initializeCards(sessionID):
	cards_ = cards
	shuffle(cards_)
	temp_cards = chunkify(cards_, 4)
	i = 0
	keys = sessions[sessionID]['users']
	for key in keys:
		sessions[sessionID]['users'][key] = temp_cards[i]
		i += 1
	print "Game has been initialized"
	print "-"
	print sessions[sessionID]['users']
	print "-"

"""
def gameString(sessionID):
	Defined as follows
	currentTurn|user1:user1_cards|user2:user2_cards|user3:user3_cards|user4:user4_cards|center_cards
	gameString = "%s|" % (sessions[sessionID]['current_turn'])
	for key, value in sessions[sessionID]['users']:
		gameString = gameString.join([gameString, '%s|%s|' % (key, str(value).replace('[', '').replace(']', ''))])
	gameString = gameString.join([gameString, str(sessions[sessionID]['table_cards']).replace('[', '').replace(']', '')])
	return gameString
"""

def addPlayer(sessionID, username):
	sessions[sessionID]['users'][username] = []

@app.route('/')
def index():
	return "ERROR: 404 Forbidden"

@app.route('/create_game', methods=['GET'])
def create_game():
	print "FUCK"
	print request.args
	if len(request.args) > 0:
		print 'tossed'
		if not sessions.has_key(request.args['id']):
			initalizeSession(request.args['id'], request.args['u'])
			print "[INFO]: GameSession with ID %s created" % request.args['id']
			return 'gameCreated'
		else:
			print "fucked"
			return 'False'

@app.route('/join_game', methods=['GET'])
def join_game():
	print "Got join game signal"
	print request.args
	if len(request.args) > 0:
		if sessions.has_key(request.args['id']):
			if len(sessions[request.args['id']]['users']) < 3:
				addPlayer(request.args['id'], request.args['u'])	
				return 'Added' #Need more players
			elif len(sessions[request.args['id']]['users']) == 3:
                                addPlayer(request.args['id'], request.args['u'])
				sessions[request.args['id']]['status'] = 'Current turn %s' % sessions[request.args['id']]['current_turn']
				initializeCards(request.args['id'])
                                return 'Added' #Need more players
			else:
				return 'False'
		else:
			return 'False'
	else:
		return 'False'

@app.route('/end_game', methods=['GET'])
def end_game():
	return render_template("login.html") #Destroy game session

@app.route('/update_hand', methods=['GET']) #GameID, username, card
def make_move():
	if len(request.args) > 0:
		print "Updating hand for %s in game %s" % (request.args['u'], request.args['id'])
		if sessions.has_key(request.args['id']):
                        if sessions[request.args['id']]['users'].has_key(request.args['u']):
				sessions[request.args['id']]['table_cards'].append(request.args['card'])
				try:
					sessions[request.args['id']]['users'][request.args['u']].remove(request.args['card'])
				except Exception as e:
					pass
				getNextCard(request.args['id'])
				getNextPlayer(request.args['id'], request.args['u'])
				sessions[request.args['id']]['status'] = '%s made a move. %s\'s turn to play %s' % (request.args['u'], sessions[request.args['id']]['current_turn'], sessions[request.args['id']]['current_card']) 				
				return "%s|%s|%s" % (sessions[request.args['id']]['current_turn'], str(sessions[request.args['id']]['users'][request.args['u']]).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), sessions[request.args['id']]['status'])

@app.route('/check_bs', methods=['GET'])
def check_bs():
	if len(request.args) > 0:
		if sessions.has_key(request.args['id']):
                        if sessions[request.args['id']]['users'].has_key(request.args['u']):
				if sessions[request.args['id']]['table_cards'][-1].replace('h', '').replace('c', '').replace('d', '').replace('b', '') != sessions[request.args['id']]['previous_card']:
					for card in sessions[request.args['id']]['table_cards']:
						sessions[request.args['id']]['users'][sessions[request.args['id']]['previous_player']].append(card)
						sessions[request.args['id']]['table_cards'].remove(card)
					sessions[request.args['id']]['status'] = '%s called bullshit on %s and was right' % (request.args['u'], sessions[request.args['id']]['previous_player']) 										  
					return "%s|%s|%s" % (sessions[request.args['id']]['current_turn'], str(sessions[request.args['id']]['users'][request.args['u']]).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), sessions[request.args['id']]['status'])
				else:
					for card in sessions[request.args['id']]['table_cards']:
						sessions[request.args['id']]['users'][request.args['u']].append(card)
						sessions[request.args['id']]['table_cards'].remove(card)
					sessions[request.args['id']]['status'] = '%s called bullshit on %s and was wrong' % (request.args['u'], sessions[request.args['id']]['previous_player']) 										  
					return "%s|%s|%s" % (sessions[request.args['id']]['current_turn'], str(sessions[request.args['id']]['users'][request.args['u']]).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), sessions[request.args['id']]['status'])


def getNextCard(sessionID):
	current_card = sessions[sessionID]['current_card']
	i = card_order.index(current_card)
	if current_card == card_order[-1]:
		sessions[sessionID]['previous_card'] = sessions[sessionID]['current_card']
		sessions[sessionID]['current_card'] = card_order[0]
	else:
		sessions[sessionID]['previous_card'] = sessions[sessionID]['current_card']
		sessions[sessionID]['current_card'] = card_order[i+1]


def getNextPlayer(sessionID, current):
	keys = sessions[sessionID]['users'].keys()
	for i, key in enumerate(keys):
		if key == current:
			if key == sessions[sessionID]['users'].keys()[-1]:
				sessions[request.args['id']]['previous_player'] = sessions[request.args['id']]['current_turn']
				sessions[request.args['id']]['current_turn'] = keys[0]
				return keys[0]
				break
			else:
				sessions[request.args['id']]['previous_player'] = sessions[request.args['id']]['current_turn']
				try:
					sessions[request.args['id']]['current_turn'] = keys[i+1]
					return keys[i+1]
				except Exception as e:
					sessions[request.args['id']]['previous_player'] = sessions[request.args['id']]['current_turn']
					sessions[request.args['id']]['current_turn'] = keys[0]
					return keys[0]
				break

@app.route('/check_user', methods=['GET'])
def check_user():
	if len(request.args) > 0:
		print "Checking user %s for game %s" % (request.args['u'], request.args['id'])
		if sessions.has_key(request.args['id']):
			if sessions[request.args['id']]['users'].has_key(request.args['u']):
				print "User found"
				return 'True'
			else:
				print "User not found"
				return 'False'
		else:
			return "NOTFOUND"

@app.route('/get_details', methods=['GET'])
def get_details():
	"""
	Detail format:
	currentTurn|cards
	"""
	if len(request.args) > 0:
		print request.args
		if sessions.has_key(request.args['id']):
			print "Sent details"
			print "%s|%s|%s" % (sessions[request.args['id']]['current_turn'], str(sessions[request.args['id']]['users'][request.args['u']]).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), sessions[request.args['id']]['status'])
			return "%s|%s|%s" % (sessions[request.args['id']]['current_turn'], str(sessions[request.args['id']]['users'][request.args['u']]).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), sessions[request.args['id']]['status'])
		else:
			return "BIG FUCK TO YOU HACKER!!!!!"

app.config["SECRET_KEY"] = "jw09mrhcw0e8agv0a8fmsgd08vfag0sfmd0"
