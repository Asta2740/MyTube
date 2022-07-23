import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from Scrapper import youtube

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    path = db.Column(db.TEXT())
    image = db.Column(db.TEXT())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['Url']
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

        except:
            pass

        return render_template('Products.html', tasks=tasks)


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=8081)
    app.run(debug=True)
