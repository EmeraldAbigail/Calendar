from flask import render_template, redirect, flash, request, session
from flask_app.models import event
from flask_app import app

#Routes for Calendar Table
#Create an Event
@app.route('/insert/event', methods=['POST'])
def create_event():
    form = request.form
    data = {
        'title': form['title'],
        'start_time': form['start_time'],
        'end_time': form['end_time'],
        'location': form['location'],
        'details': form['details'],
        'recurrence': form['recurrence'],
        'reminder': form['reminder'], 
        'calendar_id': form['calendar_id'],
        'user_id': session['user_id']
    }
    if not event.event_check(data):
        flash('Please fill out Event','event')
    event.create(data)
    return redirect('/main')

#Edit  an Event
@app.route('/calendar/<int:event_id>/events/edit', methods=['GET', 'POST']) 
def edit_event(event_id):
    if not session:
        return redirect('/')

    if request.method == 'GET':  
        session['event_id'] = event_id
        update_event = event.update_event(event_id)
        return render_template('event/edit.html', event=update_event)  
    
    data = {
        'title': request.form['title'],
        'start_time': request.form['start_time'],
        'end_time': request.form['end_time'],
        'location': request.form['location'],
        'details': request.form['details'],
        'recurrence': request.form['recurrence'],
        'reminder': request.form['reminder'], 
        'calendar_id': request.form['calendar_id'],
        'user_id': session['user_id']
    }
    if not event.event_check(data):
        flash('Please fill out Event','event')
        return redirect(f'/calendar/<int:calendar_id>/events/edit') 
    event.update_event(data)
    return redirect('/main')

#Show Calendar 
@app.route('/calendar/show_calendar/<int:event_id>/events/details')
def show_event_details(event_id):
    if not session:
        return redirect('/')

    event = event.one_event(event_id)
    return render_template('details.html', event=event) 

#Delete Event 
@app.route('/calendar/delete/<int:event_id>/event') 
def delete(event_id):
    if not session:
        return redirect('/')
    
    event.delete_event(event_id) 
    return redirect('/main')

#Show User Events
@app.route('/event/user_event/<int:user_id>')
def show_events_by_user(user_id):
    if not session:
        return redirect('/')
    print(user_id)
    Event = Event.events_by_user(user_id)
    return render_template('details.html', events=event) 

