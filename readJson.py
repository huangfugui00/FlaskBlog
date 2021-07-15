import json
from flaskblog import db
from flaskblog.models import Post


with open('posts.json', 'r') as f:
    posts_json = json.load(f)
    for post in posts_json:
        post = Post(title=post['title'], content=post['content'], user_id=post['user_id'])
        db.session.add(post)
    db.session.commit()
