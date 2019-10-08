import secrets, os
from PIL import Image

from flask import current_app, url_for
from flask_mail import Message

from .. import mail

def send_pw_reset_email(user):
    token = user.get_pw_reset_token()
    msg = Message(
        subject='Password Reset Request',
        sender='noreply@flaskblog.com',
        recipients=[user.email]
    )
    msg.body = \
        f'''Please visit the following link to reset your password:
{url_for('users.pw_reset', token=token, _external=True)}

Note: This link will expire in 30 minutes'''
    mail.send(msg)


def save_profile_pic(image_data):
    random_hex = secrets.token_hex(8)
    _, img_ext = os.path.splitext(image_data.filename)
    img_file = random_hex + img_ext

    image = Image.open(image_data)
    image.thumbnail((256, 256))  # Resize

    image.save(os.path.join(current_app.root_path, 'static', img_file))
    return img_file