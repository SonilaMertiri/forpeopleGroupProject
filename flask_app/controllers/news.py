from flask_app.models.news import News
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from flask_app import app
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'flask_app/static/newsimages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/articlenews/new', methods=['GET', 'POST'])
def add_news():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            return render_template('addNews.html')
        return redirect('/')
    elif request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/')
        user = User.get_user_by_id({'id': session['user_id']})
        if user['role'] == 'admin':
            title = request.form.get('title')
            content = request.form.get('content')
            if 'newsphoto' in request.files:
                file = request.files['newsphoto']
                if file.filename != '' and allowed_file(file.filename):
                    newsphoto = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, newsphoto))
                    data = {
                        'title': title,
                        'content': content,
                        'newsphoto': newsphoto,
                        'user_id': session['user_id']
                    }
                    try:
                        result = News.create(data)
                        if result:
                            flash('News added successfully!', 'success')
                        else:
                            flash('Failed to add news. Please try again later.', 'error')
                    except Exception as e:
                        flash(f'Error occurred: {str(e)}', 'error')
                        app.logger.error(f'Error adding news: {str(e)}')
                    return redirect('/')
                else:
                    flash('Invalid file format', 'error')
                    return redirect(request.url)
            else:
                flash('No file part', 'error')
                return redirect(request.url)
        return redirect('/')





@app.route('/news/<int:id>')
def view_news(id):
    news = News.get_news_by_id({'id': id})
    user = User.get_user_by_id({'id': session['user_id']}) if 'user_id' in session else None
    return render_template('detailsNews.html', news=news, user=user)

@app.route('/news/edit/<int:id>')
def edit_news(id):
    if 'user_id' not in session:
        return redirect('/')
    news = News.get_news_by_id({'id': id})
    if news and news['user_id'] == session['user_id']:
        return render_template('editNews.html', news=news)
    return redirect('/')

@app.route('/news/update/<int:id>', methods=['POST'])
def update_news(id):
    if 'user_id' not in session:
        return redirect('/')
    news = News.get_news_by_id({'id': id})
    if news and news['user_id'] == session['user_id']:
        title = request.form['title']
        content = request.form['content']
        newsphoto = news['newsphoto']  # Get the existing newsphoto
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                newsphoto = filename  # Update newsphoto if a new file is uploaded
            else:
                flash('Invalid file format', 'error')
                return redirect(request.url)
        # Update the news article with the new data including newsphoto
        News.update({'id': id, 'title': title, 'content': content, 'newsphoto': newsphoto})
        return redirect('/news/' + str(id))
    return redirect('/')

@app.route('/news/delete/<int:id>')
def delete_news(id):
    if 'user_id' not in session:
        return redirect('/')
    news = News.get_news_by_id({'id': id})
    if news and news['user_id'] == session['user_id']:
        News.deleteNews({'id': id})
    return redirect('/')
