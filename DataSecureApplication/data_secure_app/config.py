import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    USERNAME = os.environ.get('USER')
    PASSWD = os.environ.get('PASSWD')
    SQLALCHEMY_DATABASE_URI = 'mysql://' + USERNAME + ':' + PASSWD + '@localhost/dsa'
    UPLOAD_FOLDER = 'user_file_data'
    DOWNLOAD_FOLDER = 'user_file_data_downloaded'
    MAX_CONTENT_PATH = 1000000000
    ADMIN_ADDR = '0x53DE8E1b00591454e0C0315A342C148A68913248'
