from flask import Blueprint, render_template, request, redirect, url_for
from . import TEMPLATE_PATH
from . import firebase_init

views = Blueprint('views', __name__)
# clientRoom = firebase_init()

@views.route('/')
def landing():
	return render_template('AL_index.html')

@views.route('/lobby')
def lobby():
	return render_template('ALchoose.html')

@views.route('/host', methods=['GET', 'POST'])
def host():
	if request.method == 'POST':
		playerName = request.form.get('player-name')
		roomName = request.form.get('room-name')

		if roomName and playerName:
			return redirect(url_for('.room', hostRoom=roomName, hostPlayer=playerName))
		else:
			return redirect(url_for('.host'))
	else:    
		return render_template('ALnew.html')

@views.route('join')
def join():
	return render_template('ALjoin.html')


@views.route('/room/<hostRoom>/<hostPlayer>')
def room(hostRoom, hostPlayer): 
	return render_template('room.html', hostRoom=hostRoom, hostPlayer=hostPlayer)