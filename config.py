import os

class Config:
    SECRET_KEY = '6F6598821C1485A99C499C8EE2859'
    UPLOAD_FOLDER = '/static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    SQLALCHEMY_DATABASE_URI = 'postgresql://wally_database_6ll1_user:gWVOkr9oL5Cv4k5W19m9SVIRth3hl2oc@dpg-crt8l75umphs73fkf250-a.oregon-postgres.render.com/wally_database_6ll1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
