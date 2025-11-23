from event_finder import app, db


HOST = '0.0.0.0'
PORT = '8080'


app.run(host=HOST, port=PORT, debug=True)

#if (__name__) == '__main__':
#   app.run(debug==True)