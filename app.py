from flask import Flask, render_template, request, redirect, jsonify

from utils.db import db

from models.song import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Song.db'


@app.route('/')
def index():
    song = Song.query.all()
    return render_template('index.html', content=song)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/topsongs')
def topsongs():
    return render_template('topsongs.html')


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    song_id = form_data.get('song_id')
    song_name = form_data.get('song_name')
    artist = form_data.get('artist')
    streamed_hours = form_data.get('streamed_hours')

    song = Song.query.filter_by(song_id=song_id).first()
    if not song:
        song = Song(song_id=song_id, song_name=song_name, artist=artist, streamed_hours=streamed_hours)
        db.session.add(song)
        db.session.commit()
    print("sumitted successfully")
    return redirect('/')


@app.route('/delete/<int:song_id>', methods=['GET', 'DELETE'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    print("task: {}".format(song))

    if not song:
        return jsonify({'message': 'song not found'}), 404
    try:
        db.session.delete(song)
        db.session.commit()
        return jsonify({'message': 'song deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update/<int:song_id>', methods=['GET', 'POST'])
def update_song(song_id):
    song = Song.query.get(song_id)

    if not song:
        return jsonify({'message': 'Song not found'}), 404

    if request.method == 'POST':
        form_data = request.form.to_dict()
        song.song_name = form_data.get('song_name')
        song.artist = form_data.get('artist')
        song.streamed_hours = form_data.get('streamed_hours')

        db.session.commit()
        return redirect('/')

    return render_template('update.html', song=song)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
