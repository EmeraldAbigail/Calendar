from flask import render_template, redirect, flash, request, session
from flask_app.models import event
from flask_app.models import user
from flask_app.models import calendar
from flask_app import app

#Routes for Calendar Table
#Create a Calendar 
@app.route('/create/calendar', methods=['POST'])
def create_calendar():
    form = request.form
    data = {
        'name': form['name'],
        'user_id': session['user_id']
    }
    if not calendar.calendar_check(data):
        flash('Please label Calendar','name')
    calendar.create(data)
    return render_template('show.html', calendar=calendar)

#Edit Calendar 
@app.route('/calendar/<int:calendar_id>/edit', methods=['GET', 'POST']) 
def edit_calendar(calendar_id):
    if not session:
        return redirect('/')

    if request.method == 'GET':  
        session['calendar_id'] = calendar_id
        update_calendar = calendar.one_calendar(calendar_id)
        return render_template('edit.html', calendar=update_calendar)  
    
    data = {
        'name': request.form['name'],
        'calendar_id': calendar_id  
    }
    if not calendar.calendar_check(data):
        flash('Please name Calendar','name')
        return redirect(f'/calendar/{calendar_id}/edit') 
    calendar.update_calendar(data)
    return redirect('/main')

#Show Calendar 
@app.route('/calendar/show_calendar/<int:calendar_id>')
def show_calendar_details(calendar_id):
    if not session:
        return redirect('/')

    Calendar = Calendar.one_calendar(calendar_id)
    return render_template('show.html', calendar=calendar) 

#Delete Calendar
@app.route('/calendar/delete/<int:calendar_id>') 
def delete(calendar_id):
    if not session:
        return redirect('/')
    
    calendar.delete_calendar(calendar_id) 
    return redirect('/main')

#Show User Events
@app.route('/event/user_event/<int:user_id>')
def show_events_by_user(user_id):
    if not session:
        return redirect('/')
    print(user_id)
    event = event.events_by_user(user_id)
    return render_template('show.html', events=event) 

