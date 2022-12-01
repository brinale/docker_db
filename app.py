from flask import Flask, g, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
import socket

app = Flask(__name__)
#counter = 0

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Counts(db.docker_db):
  id = db.Column(db.Integer, primary_key=True)
  amount = db.Column(db.Integer, nullable=False)
  dateadded = db.Column(db.String, nullable=True)

  def __init__(self, amount):
    self.amount = amount

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='docker_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.route("/")
def show():
   ## conn = get_db_connection()
   ## cur = conn.cursor()
   ## cur.execute('SELECT * FROM books;')
   ## books = cur.fetchall()
   ## cur.close()
   ## conn.close()
    items = []
    for item in db.session.query(Counts).all():
        del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
    #global counter
    html = f"<p>{items[-1]}</p>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/about")
def hello():
    html = "<h3>Hello, Arina Belousova!</h3>" 
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/stat")
def incr():
    global counter
    db.session.add(Counts(1))
    db.session.commit()
    html = f"<p>{counter}</p>"
    counter = counter + 1
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)