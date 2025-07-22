from flask import Flask, render_template, request, redirect, url_for
from cs50 import SQL
import os

if not os.path.exists('movies.db'):
    open('movies.db', 'w').close()


app = Flask(__name__)
db = SQL('sqlite:///movies.db')


def init_db():
    db.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genre TEXT
        )
    ''')


with app.app_context():
    init_db()

    @app.errorhandler(404)
    def handle_404(e):
        return render_template('custom404.html')

    @app.route('/')
    def index():
        movies = db.execute('SELECT * FROM movies')
        return render_template('index.html', movies=movies)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            title = request.form['title']
            year = request.form['year']
            genre = request.form['genre']
            db.execute(
                'INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)', title, year, genre)
            return redirect(url_for('index'))
        return render_template('add.html')

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        movie = db.execute('SELECT * FROM movies WHERE id = ?', id)
        if not movie:
            return redirect(url_for('index'))
        movie = movie[0]

        if request.method == 'POST':
            title = request.form['title']
            year = request.form['year']
            genre = request.form['genre']
            db.execute(
                'UPDATE movies SET title = ?, year = ?, genre = ? WHERE id = ?', title, year, genre, id)
            return redirect(url_for('index'))
        return render_template('edit.html', movie=movie)

    @app.route('/delete/<int:id>')
    def delete(id):
        db.execute('DELETE FROM movies WHERE id = ?', id)
        return redirect(url_for('index'))

    @app.route('/commit')
    def commit():
        output = os.popen('git log -1 --pretty=format:"%h|%s|%cr"').read()
        commit_hash, description, time = output.strip().split('|')
        return ({
            'hash': commit_hash,
            'description': description,
            'time': time
        })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
