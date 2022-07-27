import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from Scrapper import youtube, Youtube_list
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_BINDS'] = {'PlayedMusic': 'sqlite:///PlayedMusic.db'}
db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    path = db.Column(db.TEXT())
    image = db.Column(db.TEXT())


class PlayedMusic(db.Model):
    __bind_key__ = 'PlayedMusic'
    id = db.Column(db.Integer, primary_key=True)
    Played_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['Url']
        if "&list" in task_content:
            content = Youtube_list(task_content)
            try:

                for Specific_song in content:
                    number_of_music = 0
                    tasks = Music.query.order_by(Music.id).all()
                    print("1")
                    for count in tasks:
                        number_of_music = number_of_music + 1
                    print("2")
                    print(Specific_song[1], Specific_song[1][17:30])
                    os.rename(Specific_song[1], Specific_song[1][17:30] + 'new' + str(number_of_music) + '.mp3')
                    print("3")
                    new_path = Specific_song[1][17:30] + 'new' + str(number_of_music) + '.mp3'
                    print("4")
                    new_task1 = Music(name=Specific_song[2], path=new_path, image=Specific_song[0])
                    print("5")
                    try:
                        db.session.add(new_task1)
                        print("added")
                        db.session.commit()
                        print("created")

                    except:
                        return "there was an error"
                return redirect('/')





            except:
                return "errorrrrrrrrr"

        else:
            content = youtube(task_content)

            number_of_music = 0
            tasks = Music.query.order_by(Music.id).all()
            for count in tasks:
                number_of_music = number_of_music + 1

            os.rename(content[1], content[1][17:30] + 'new' + str(number_of_music) + '.mp3')

            new_path = content[1][17:30] + 'new' + str(number_of_music) + '.mp3'
            new_task1 = Music(name=content[2], path=new_path, image=content[0])

        try:
            db.session.add(new_task1)
            print("added")
            db.session.commit()
            print("created")
            return redirect('/')
        except:
            return "there was an error"
    else:
        try:
            tasks = Music.query.order_by(Music.id).all()
            playing_id = PlayedMusic.query.order_by(PlayedMusic.id).all()

        except:
            pass
        # try:
        #     for x in tasks:
        #         print(x.id)
        # except:
        #     pass
        #
        # print(tasks)
        # print(playing_id)

        return render_template('Music_playlist.html', tasks=tasks, Last_id=playing_id)


@app.route('/test', methods=['GET', 'POST'])
def test():
    output = request.get_json()
    # print(output) # This is the output that was stored in the JSON within the browser
    # print(type(output))
    result = json.loads(output)  # this converts the json output to a python dictionary
    # print(result) # Printing the new dictionary
    # print(type(result))#this shows the json converted as a python dictionary

    New_id = result['firstname'] - 1
    print(New_id)

    new_task1 = PlayedMusic(Played_id=New_id)
    try:
        db.session.add(new_task1)
        print("added")
        db.session.commit()
        print("created")
        return redirect('/')
    except:
        return "there was an error"


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8081)
    app.run(debug=True)
