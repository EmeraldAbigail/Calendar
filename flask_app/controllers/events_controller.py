from flask import render_template, redirect, flash, request, session
from flask_app import app
from flask_app.models.event import Event

#Routes for Events Table 

#Create an Event
@app.route('/create_event', methods=['POST'])
def create_event():
    # Check if the user has submitted the form
    if not Event.validate_event(request.form):
        return redirect('/')
    # If the user has submitted the form, create a new event
    data = {
        'title': request.form['title'],
        'start_time': request.form['start_time'],
        'end_time': request.form['end_time'],
        'location': request.form['location'],
        'details': request.form['details'],
        'recurrence': request.form['recurrence'],
        "users_id": session["user_id"]
        }
    Event.create_event(data)
    return redirect('/main')

#Display form for Event.html
@app.route('/show/event_form')
def show_event_form():
    return render_template('event.html')

#Display all Events
@app.route('/events')
def display_events():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"]
        }
    events = Event.get_all_events(data)
    return render_template('event.html', events=events)

# #Edit an Event
@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'user_id' not in session:
        return redirect('/logout')

    if request.method == 'GET':
        event = Event.get_event({'id': event_id})
        return render_template('edit.html', event=event) 

    if request.method == 'POST':
        data = {
            'id': event_id,
            'title': request.form['title'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'location': request.form['location'],
            'details': request.form['details'],
            'recurrence': request.form['recurrence'],
            'user_id': session['user_id']
        }
        if not Event.validate_event(data): 
            flash('Please fill out Event','event')
            return redirect(f'/events/{event_id}/edit') 

#Update Route
@app.route('/events/<int:event_id>/update', methods=['POST'])
def update_event(event_id):
    data = {
        'id': event_id,
        'title': request.form['title'],
        'start_time': request.form['start_time'],
        'end_time': request.form['end_time'],
        'location': request.form['location'],
        'details': request.form['details'],
        'recurrence': request.form['recurrence'],
        'user_id': session['user_id']
        }
    Event.update_event(data)
    return redirect('/main')

#Show Event Details
@app.route('/calendar/<int:event_id>/event/details')
def show_event_details(event_id):
    if not session:
        return redirect('/')

    event = Event.one_event(event_id)
    return render_template('details.html', event=event) 

#Delete Event 
@app.route('/calendar/delete/<int:event_id>/event') 
def delete(event_id):
    if not session:
        return redirect('/')
    
    Event.delete_event(event_id) 
    return redirect('/main')

#Show User Events
@app.route('/event/user_event/<int:user_id>')
def show_events_by_user(user_id):
    if not session:
        return redirect('/')
    print(user_id)
    events = Event.events_by_user(user_id)
    return render_template('details.html', event=events) 

