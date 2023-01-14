from flask import request
from flask_socketio import Namespace, emit, join_room, leave_room

from . import db

class clientManager:
    def __init__(self, data):
        self.data = data

    def duplication(self):
        roomData = db.child('clientRooms').child(self.data['clientRoom']).get()
        if roomData.val() is not None:
            for value in roomData.each():
                if value.val()['clientName'] == self.data['clientName']:
                        db.child('clientRooms').child(self.data['clientRoom']).child(str(value.key())).update({'clientId': request.sid})
                        join_room(self.data['clientRoom'], sid=request.sid)
                        return True
                
            return False
    
    def client_leave(self):
        roomData = db.child('clientRooms').child(self.data['clientRoom']).get()
        if roomData.val() is not None:
              for value in roomData.each():
                if value.val()['clientId'] == request.sid:
                    db.child('clientRooms').child(self.data['clientRoom']).child(str(value.key())).remove()
                    
                    return True

class RoomServices(Namespace):
    def on_connect(self):
        print('[CLIENT CONENCTED]:',request.sid)

    def on_disconnect(self):
        print('[CLIENT DISCONENCTED]:',request.sid)

    def on_room_request(self, data):
        if not clientManager(data).duplication():
            db.child('clientRooms').child(data['clientRoom']).push({'clientId':request.sid, 'clientName': data['clientName'], 'clientRoom': data['clientRoom']})
            join_room(data['clientRoom'], sid=request.sid)

        roomData = db.child('clientRooms').child(data['clientRoom']).get()
        emit('room_response', dict(roomData.val()), to=data['clientRoom'], broadcast=True)
    
    def on_room_leave(self, data):
        print('leaving data here',data)
        if clientManager(data).client_leave():
            leave_room(data['clientRoom'], sid=request.sid)

        

        