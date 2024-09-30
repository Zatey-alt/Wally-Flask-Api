import os

class Config:
    SECRET_KEY = '6F6598821C1485A99C499C8EE2859'
    UPLOAD_FOLDER = '/static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    SQLALCHEMY_DATABASE_URI = 'postgresql://wally_database_user:W8ZiNLr3Gb5SkYV1GxBSxbuIFiOaeNrv@dpg-crt7hoo8fa8c73ct1d0g-a.oregon-postgres.render.com/wally_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
