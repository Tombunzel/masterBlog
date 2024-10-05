import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_posts():
    with open("data.json", "r") as handle:
        posts = json.load(handle)
    return posts


def write_posts(posts):
    with open("data.json", "w") as handle:
        json.dump(posts, handle, indent=4)


def get_post_by_id(posts, post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    return post


@app.route('/')
def index():
    """renders the index.html template with the current data"""
    posts = get_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['POST', 'GET'])
def add():
    """add a post to data
    if GET method: render the add.html form-page to add a post
    if POST method: update the data and redirect to home"""
    if request.method == 'POST':
        posts = get_posts()
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        new_post = {'id': len(posts) + 1,
                    'author': author,
                    'title': title,
                    'content': content,
                    'likes': 0
                    }

        posts.append(new_post)
        write_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """delete post from data"""
    posts = get_posts()
    for i, post in enumerate(posts):
        if post['id'] == post_id:
            del posts[i]

    write_posts(posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['POST', 'GET'])
def update(post_id):
    """update a post
    if GET method: render the update.html form-page
    if POST method: get updated info and write to data file"""
    posts = get_posts()
    post = get_post_by_id(posts, post_id)

    if request.method == 'POST':
        if post is None:
            return "Post not found", 404

        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        write_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """increment likes to a post"""
    posts = get_posts()
    post = get_post_by_id(posts, post_id)

    if post is None:
        return "Post not found", 404

    post['likes'] += 1
    write_posts(posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
