from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.event import Event
from flask_app.models.user import User

# @app.route('/')
# def events():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     events = Event.get_all()
#     user = None
#     if 'user_id' in session:
#         data = {'id': session['user_id']}
#         user = User.get_user_by_id(data)

#     for event in events:
#         # Assuming 'image_path' is a column in your events table
#         if event['name'] == 'Peoples in Need':
#             event['image_path'] = '../static/images/clean.jpg'
#         elif event['name'] == 'Environment':
#             event['image_path'] = 'path_to_environment_image.jpg'
#         else:
#             event['image_path'] = 'default_image_path.jpg'

#     return render_template('dashboard.html', events=events, user=user)

@app.route('/')
def events():
    events = Event.get_all()
    user = None   # deklarimi me none ketu i userit ben qe edhe kur nuk ka user te loguar te shikohet contenti ne dashbord, nese e heqim jep errore
    if 'user_id' in session:
        data = {
            'id': session['user_id']
        }
        user = User.get_user_by_id(data)
    return render_template('dashboard.html', events=events, user=user)



@app.route('/events/new')
def addEvent():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    user=User.get_user_by_id(data)
    # event=Event.get_event_by_id()
    if 'user_id' in session and user['role']=='admin':
        return render_template('addEvent.html')
    return redirect('/')

@app.route('/events/new', methods=['POST'])
def addNewEvent():
    if 'user_id' not in session:
        return redirect('/')
    data_user={
        'id': session['user_id']
    }
    user=User.get_user_by_id(data_user)
    if not Event.validate_event(request.form):
        return redirect(request.referrer)
    if user['role']=='admin':
        data={
            'name': request.form['name'],
            'description':request.form['description'],
            'user_id':session['user_id']
        }
        Event.create(data)
        return redirect('/')
    return redirect('/')


@app.route('/event/<int:id>')
def view_event(id):
    data = {
        'id': id,
        'event_id': id
    }
    event = Event.get_event_by_id(data)
    user = None
    if 'user_id' in session:
        user = User.get_user_by_id({'id': session['user_id']})
    
    return render_template('detailsEvent.html', event=event, user=user)




@app.route('/event/edit/<int:id>')
def edit_event(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    event= Event.get_event_by_id(data)
    if event and event['user_id']== session['user_id']:
        return render_template('editEvent.html', event=event)
    return redirect('/')

@app.route('/event/update/<int:id>', methods=['POST'])
def update_event(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        # Include image_path here
    }
    event = Event.get_event_by_id({'id': id})
    if event and event['user_id'] == session['user_id']:
        if not Event.validate_event_update(request.form):
            return redirect(request.referrer)
        Event.update(data)
        return redirect('/event/' + str(id))
    return redirect('/')


@app.route('/event/delete/<int:id>')
def delete_event(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id
    }
    event= Event.get_event_by_id(data)
    if event['user_id']== session['user_id']:
        Event.deleteEvent(data)
    return redirect('/')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process the form data here
        # For demonstration purposes, let's just print the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"First Name: {first_name}, Last Name: {last_name}, Email: {email}, Message: {message}")
        # You can add your actual form processing logic here

        # Render the contact page with a success message
        return render_template('contact.html', success_message='Your message has been sent successfully!')

    # If it's a GET request, simply render the contact page
    return render_template('contact.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

