from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Tasks
from flask_login import login_required
from datetime import datetime, timedelta
from flask_login import current_user
from app.celery import send_notif
from app import db

task = Blueprint('task', __name__,
               template_folder='templates',
               static_folder='static')


@task.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        tasks = current_user.tasks
        return render_template('index.html', tasks=tasks)
    else:
        pass
    return render_template('index.html')

@task.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    description = request.form['description']
    time_delta = int(request.form['time'])
    deadline = datetime.now() + timedelta(minutes=time_delta)
    reminder_Time = deadline - datetime.now() 
    add_task = Tasks(title=title, description=description, user_id=current_user.id, deadline=deadline)
    db.session.add(add_task)
    db.session.commit()
    
    tasker  = add_task.id
    user_id = current_user.id

    countdown= int(reminder_Time.total_seconds())

    send_notif.apply_async(args=(tasker, user_id,), countdown=countdown)


    return redirect(url_for('task.index'))


@task.route('/complete/<string:task_id>')
@login_required
def complete_task(task_id):
    tasks = Tasks.query.filter_by(id=task_id).first()   
    if tasks:
        tasks.completed = True
        db.session.add(tasks)
        db.session.commit()
    return redirect(url_for('task.index'))


@task.route('/delete/<string:task_id>')
@login_required
def delete_task(task_id):
    tasks = Tasks.query.filter_by(id=task_id).first()   
    if tasks:
        db.session.delete(tasks)
        db.session.commit()
    return redirect(url_for('task.index'))


