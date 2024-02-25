from flask import render_template
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.donation import Donation  # Import your Donation model
from flask_app.models.user import User  # Import your Donation model
from flask_app.models.event import Event 
from flask_app.models.action import Action


@app.route('/special-event/<int:id>')
def special_event(id):
    event = Event.get_event_by_id({'id': id})
    if not event:
        flash('Environment not found.')
        return redirect('/')

    actions = Action.get_actions_by_event_id(id)

    for action in actions:
        if action.title == 'BICYCLE CLEAN-UP DAY!':
            action.image = '../static/images/becycle.jpg'
        elif action.title == 'CLEAN GRAND PARK OF TIRANA AND THE LAKE!':
            action.image = '../static/images/cleanlake.jpg'
        else:
            action.image = '../static/images/planttrees.jpg'  # Default image URL
        
    user = None
    if 'user_id' in session:
        user = User.get_user_by_id({'id': session['user_id']})

    return render_template('envirements.html', event=event, actions=actions, user=user)


