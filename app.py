#!/usr/bin/env python3
from models.dbmodel import db
from flask_migrate import Migrate
from routes import create_app


app = create_app()

app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
