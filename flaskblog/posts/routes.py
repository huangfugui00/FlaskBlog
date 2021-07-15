from flask import Blueprint, flash, url_for, render_template, request, redirect, abort, jsonify
from flask_login import login_required, current_user

from flaskblog import db
from flaskblog.models import Post, Like
from flaskblog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new/", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/comment/<int:post_id>", methods=['GET','POST'])
def new_comment(post_id):
   # breakpoint()
    form = CommentForm()
    if form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        post_comment = Post(content=form.content.data, author=current_user,parent=post)
        db.session.add(post_comment)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))
    if request.method == 'POST':
        post = Post.query.get_or_404(post_id)
        content = request.form['content']
        post_comment = Post(content=content, author=current_user, parent=post)
        db.session.add(post_comment)
        db.session.commit()
        return jsonify(count=post.replies.count())
    return render_template('create_comment.html', title='New Comment',
                           form=form, legend='New Comment')


@posts.route("/post/<int:post_id>/")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    return render_template('post.html', title=post.title, post=post,form=form)


@posts.route("/post/<int:post_id>/update/", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete/", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/likeAction", methods=['POST'])
@login_required
def likeAction(post_id):
   # breakpoint()
    post = Post.query.get_or_404(post_id)
    if post:
        if Like.query.filter_by(liker=current_user, like_post=post).first():
            like = Like.query.filter_by(liker=current_user, like_post=post).first()
            db.session.delete(like)
            db.session.commit()
            return jsonify(count=Like.query.filter_by(like_post=post).count())
        else:
            like = Like(liker=current_user, like_post=post)
            db.session.add(like)
            db.session.commit()
            return jsonify(count=Like.query.filter_by(like_post=post).count())
    abort(403)