"""
    Websocket interface to a NFC reader.
    Copyright (C) 2014 Lennart Buit, Jelte Zeilstra

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
"""

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

from nfc_list import init_reader

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'niet doorvertellen!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('nfc_echo_test')
def on_message(message):
    emit('nfc_echo_test_response', {'data': message['data']})

def send_nfc_tag(uid, atqa, sak):
    socketio.emit('nfc_read', {'uid': uid, 'atqa': atqa, 'sak': sak})

if __name__ == '__main__':
    init_reader(send_nfc_tag)
    socketio.run(app)
