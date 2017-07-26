import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key = 'YCXCWEeGUD55KV8zxQl29Vqys'
consumer_secret = 'sAuWJUuFOJeORK0JrgknP4FKqml9dMOjA4TVjiJ3C9qFIZcB6t'
access_token = '1374751998-Olqap3rLJEMb7a8v9KUmNNVtqTeYrc4K1c00dSt'
access_secret = 'jDXMAUlr2yhkP73ZesZzcupQMOJWStciZG6zNcoZwPYJ6'

#This snippet of code sends the gathered data to the client socket. 
#The data is sent in Json format and encoded in UTF - 8. 
#It also states the status of the data transfer, 
#whether it was successful or not.

class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'].encode('utf-8') )
          self.client_socket.send( msg['text'].encode('utf-8') )
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True


#This block of code is the one responsible for the connection to twitter 
#API. It requires you to give authentication, this serves the purpose 
#of connecting the module to the twitter apps and, in turn allow 
#streaming.

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=["bnha","boku no hero academia","my hero academia","bokunoheroacademia","myheroacademia","boku-no-hero-academia","my-hero-academia"])



#This block of code is responsible for setting a socket in the 
#given IP address to a be passive socket that would only listen to 
#request. This is done by binding the host IP address and the specified 
#socket to the variable s. This means when the program is ran it won’t 
#automatically stream but rather would wait for a request using the 
#function start(). This block of code also would not work  if the program 
#where this is located was not the entry point of this activation. 
#Listen also has a queue of 5. 

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "10.115.10.72"      # Get local machine name
  port = 5555                 # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )
