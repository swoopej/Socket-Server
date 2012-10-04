#import socket 
import os
import SocketServer, logging

class Request_Handler(SocketServer.BaseRequestHandler):
	#will be called by the socket server when it receives a request

	def handle(self):
		#overriding default handle class
		while True:
			data = self.request.recv(1024)
			print 'receiving request from ', self.client_address
			if not data:
				break
			print 'sending back data...'
			self.request.send(data)
			self.parse_message(data)
		return

	def parse_message(self, data):
		#splits up the incoming request
		datalist = data.splitlines()
		words = []
		for line in datalist:
			word = line.split() #split by line
			for x in word:
				if x != '/':
					words.append(x) #split by whitespace separated word in each line
		if words[0] == 'GET':
			print 'GET request'
			MSG = 'You sent a GET request'
			self.request.send(MSG)
		else:
			MSG = "You don't have POST access to this database."
			self.request.send(MSG)

class Forking_Server(SocketServer.ForkingMixIn, SocketServer.TCPServer):
	#use forking mixin to create a fork for each request
	pass

if __name__ == '__main__':
	address = ('localhost', 0) #kernel will give a port
	server = Forking_Server(address, Request_Handler)
	ip, port = server.server_address
	print 'server running on port:', port
	server.serve_forever()


