from flask import Flask, render_template, redirect, request, g, session
import sqlite3
# import enum
from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__, static_url_path='/static')


engine = create_engine('sqlite:///todo.db')
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

Base = declarative_base()


# Did not work
    # class State(enum.Enum):
    #     NEW = "new"
    #     FINISHED = "finished"


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    due = Column(String)
    # state = Column(enum.Enum(State))
    state = Column(String)

Base.metadata.create_all(engine)


@app.route('/')
def show_tasks():
    tasks = session.query(Task).all()
    return render_template('show_tasks.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    """Add new task to the DB"""
    title = request.form['title']
    description = request.form['description']
    due = request.form['due']
    state = "new"
    new_task = Task(title = title, description = description, due = due, state = state)
    session.add(new_task)
    return redirect('/')


@app.route('/delete')
def delete_task():
    """Delete a task from the DB"""
    id = int(request.args.get('id'))
    e = session.query(Task).filter_by(id = id).first()
    session.delete(e)
    return redirect('/')


@app.route('/change_state')
def change_state():
    """Change the state of a task"""
    id = int(request.args.get('id'))
    task = session.query(Task).filter_by(id = id).first()
    print(type(task))
    if task.state == "new":
        task.state = "finished"
    else:
        task.state = "new"
    return redirect('/')


@app.route('/search', methods=['POST'])
def search():
    """Search through titles"""
    search = request.form['search']
    results = session.query(Task).filter(Task.title.contains(search)).all()
    return render_template('show_tasks.html', tasks=results)


app.run(debug=True)