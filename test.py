# For running tests

if __name__ == '__main__':
    # Resetting the database
    # from flask_blog import db
    # db.drop_all()
    # db.create_all()

    # Testing environment variable
    import os
    print(os.environ.get('FLASKBLOG_EMAIL_USERNAME'))
    print(os.environ.get('FLASKBLOG_SECRET_KEY'))
    print(os.environ.get('FLASKBLOG_DATABASE'))