from flask import Flask
import os
import psycopg2
import socket
from sqlalchemy import create_engine, desc, Column, Integer, DateTime, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

Base = declarative_base()

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

class Counter(Base):
    __tablename__ = 'counts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return self.amount
    
    def to_json(self):
        return dict(amount=self.amount)


engine = create_engine(os.environ.get('DATABASE_URL'), pool_size=50)

Session=sessionmaker(bind=engine)

if not inspect(engine).has_table('counts'):
    recreate_database()
    c1 = Counter(amount=0)
    session=Session()
    session.add(c1)
    session.commit()
    session.close()

@app.route("/")
def show():
    session=Session()
    item=session.query(Counter).order_by(desc(Counter.id)).first()
    item=item.to_json().get('amount')
    html = f"<p>{item}</p>"
    session.close()
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/about")
def hello():
    html = "<h3>Hello, Arina Belousova!</h3>" 
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/stat")
def incr():
    session=Session()
    item=session.query(Counter).order_by(desc(Counter.id)).first()
    item=item.to_json().get('amount')
    c = Counter(amount=item+1)
    session.add(c)
    session.commit()
    session.close()
    html = f"<p>{item}</p>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)