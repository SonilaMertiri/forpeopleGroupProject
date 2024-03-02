from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_app.models.news import News

# Add the following import for file upload handling
from werkzeug.utils import secure_filename
import os

# Define the upload folder for storing images
UPLOAD_FOLDER = 'flask_app/static/eventsimages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def events():
    events = Event.get_all()
    latest_news = News.get_all()
    user = None   
    
    if 'user_id' in session:
        user_id = session['user_id']
        data = {
            'id': user_id
        }
        user = User.get_user_by_id(data)
    return render_template('index.html', events=events, user=user, latest_news=latest_news)

@app.route('/events/new')
def addEvent():
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']
    data = {
        'id': user_id
    }
    user = User.get_user_by_id(data)
    
    if user and user['role'] == 'admin':
        return render_template('addEvent.html')
    return redirect('/')


@app.route('/events/new', methods=['GET', 'POST'])
def add_events():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            return render_template('addEvent.html')
        return redirect('/')
    elif request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            name = request.form.get('name')
            description = request.form.get('description')
            if 'image_path' in request.files:
                file = request.files['image_path']
                if file.filename != '' and allowed_file(file.filename):
                    image_path = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, image_path))
                    data = {
                        'name': name,
                        'description': description,
                        'image_path': image_path,
                        'user_id': session['user_id']
                    }
                    try:
                        result = Event.create(data)
                        if result:
                            flash('Event added successfully!', 'success')
                        else:
                            flash('Failed to add event. Please try again later.', 'error')
                    except Exception as e:
                        flash(f'Error occurred: {str(e)}', 'error')
                        app.logger.error(f'Error adding event: {str(e)}')
                    return redirect('/')
                else:
                    flash('Invalid file format', 'error')
                    return redirect(request.url)
            else:
                flash('No file part', 'error')
                return redirect(request.url)
        return redirect('/')


# 


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
    
    return render_template('event.html', event=event, user=user)




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




@app.route('/about-us')
def about_us():
    return render_template('about_us.html')





#ACTIONS


# routet per actions


@app.route('/actions/new/<int:id>', methods=['GET', 'POST'])
def add_action(id):
    data = {
        'id': id
    }
    if request.method == 'GET':
        user = User.get_user_by_id(session['user_id'])
        if 'user_id' not in session:
            return redirect('/')

        eventi = Event.get_event_by_id(data)
        if not eventi:
            flash('Invalid event ID', 'error')
            return redirect('/')
        
        return render_template('add_action.html', event=eventi, user=user)
    
    elif request.method == 'POST':
        user = User.get_user_by_id(session['user_id'])
        if 'user_id' not in session:
            return redirect('/')
        
        
        title = request.form['title']
        content = request.form['content']
        
        eventi = Event.get_event_by_id(data)
        if not eventi:
            flash('Invalid event ID', 'error')
            return redirect(request.referrer)
        
        filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Invalid file format', 'error')
                return redirect('/actions/new/{}'.format(id))
        
        data1 = {
            'title': title,
            'content': content,
            'image': filename,
            'event_id': id,
            'user_id': session['user_id']
        }
        
        Event.create_action(data1)
        
        flash('Action added successfully!', 'success')
        return redirect('/')


@app.route('/action/edit/<int:id>')
def edit_action(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id': id
        }
    action = Event.get_action_by_id(data)

    if action and action['user_id'] == session['user_id']:
        event_data = {
            'id': action['event_id']
            }
        event = Event.get_event_by_id(event_data)

        return render_template('editAction.html', action=action, event=event)
    
    return redirect(request.referrer)


@app.route('/action/edit/<int:id>', methods=['POST'])
def update_action(id):
    if 'user_id' not in session:
        return redirect('/')

    title = request.form.get('title')
    content = request.form.get('content')
    image = request.files['image'] if 'image' in request.files else None

    filename = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        flash('Invalid file format', 'error')
        return redirect('/actions/new/{}'.format(id))

    data = {
        'id': id,
        'title': title,
        'content': content,
        'image': filename  
    }

    updated = Event.update_action(data)

    if updated:
        return redirect('/event')  
    else:
        flash('Failed to update action', 'error')
        return redirect(request.referrer)
    


@app.route('/delete/action/<int:id>')
def delete_action(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    action=Event.get_action_by_id(data)
    if action['user_id']== session['user_id']:
        Event.delete_action(data)
    return redirect(request.referrer)

