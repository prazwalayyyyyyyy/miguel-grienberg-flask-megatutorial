from app import app1, db
from app.models import User, Post

@app1.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
