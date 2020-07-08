from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Development


app = Flask(__name__)
app.config.from_object(Development)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('blog/index.html')


from mod_admin import admin
from mod_users import users
from mod_blog import blog
from mod_uploads import upload

app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(blog)
app.register_blueprint(upload)


if __name__ == '__main__':
    app.run(debug=True)
