from flask_blog import create_app
from flask_blog.models import init_db

app = create_app()
init_db(app)

if __name__ == '__main__':
    app.run()

# From Python Flask Tutorial by Cory Schafer
# https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
