"""
Simple Flask application for displaying blog posts.

The application reads post data from a JSON file and passes
the data to an HTML template for display. The application also
adds new posts, delete a post and update an existing one.
"""

from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# blog posts data file variable name
POSTS_FILE = "posts.json"

@app.route('/')
def home():
    """
    Display all blog posts on the home page.

    Reads the posts from the JSON file and passes them to
    the index.html template.

    Returns:
        str: The rendered HTML page containing the blog posts.
    """

    # Read the JSON file.
    blog_posts = read_posts_from_file(POSTS_FILE)

    return render_template('index.html', posts=blog_posts)


@ app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Display the add-post form and process the creation of a new blog post.

    For a GET request, renders the form for creating a new blog post.

    For a POST request, retrieves the author, title, and content from the
    submitted form, generates a new post ID. Then it adds the post to the existing
    blog posts, saves the updated data to the JSON file, and redirects the
    user to the home page.

    Returns:
        Response: The rendered add-post page for GET requests, or a redirect
        to the home page after successfully creating a post.
    """

    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts = read_posts_from_file(POSTS_FILE)

        # Generate the ID for the new post.
        new_id = max((post["id"] for post in blog_posts), default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }

        blog_posts.append(new_post)

        # save the updated posts list back to the JSON file
        save_posts_to_file(blog_posts, POSTS_FILE)

        return redirect(url_for('home')), 200

    # Else, it's a GET request
    # So display the add.html page for the user to add the new post
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    """
    Deletes a blog post specified by the post_id from the posts blog storage.

    It handles the POST request by reading all posts from the JSON file
    and storing them in a list, it deletes the specified post (from the retrieved
    list ) by matching its id with the post_id. Then it stores the list back in
    the JSON file.

    Parameters:
         post_id (str): The id of the post to delete

    Returns:
        Response: a redirect to the home page after successfully deleting a post.
    """
    blog_posts = read_posts_from_file(POSTS_FILE)

    # Removing dictionary where the ID is equal to the post_id
    blog_posts = list(filter(lambda d: str(d.get('id')) != str(post_id), blog_posts))


    # save the updated posts list back to the JSON file
    save_posts_to_file(blog_posts, POSTS_FILE)

    return redirect(url_for('home')), 200


def fetch_post_by_id(post_id, blog_posts):
    """
    Find a blog post by its ID.

    Searches through the list of blog posts for a post whose ID
    matches the specified post ID.

    Args:
        post_id (int): The ID of the post to find.
        blog_posts (list): A list of dictionaries containing blog posts.

    Returns:
        tuple: The index and dictionary of the matching post.
        None: If no post with the specified ID is found.
    """

    for index, post in enumerate(blog_posts):
        if str(post.get('id')) == str(post_id):
            return index, post

    return None

def save_posts_to_file(blog_posts, file_name):
    """"
    Storing all posts in the specified JSON file

    Args:
          blog_posts (list): A list of the blog posts to save
          file_name (str): The name of the JSON file

    """
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, indent=4)

def read_posts_from_file(file_name):
    """"
    Retrieving all posts from the JSON file

    Args:
        file_name (str): The name of the JSON file

    Returns:
         list: A list of the blog posts

    """
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """
    Display or update an existing blog post.

    For a GET request, the blog post with the specified ID is loaded
    from the JSON file and displayed in the update form.

    For a POST request, the post is updated with the submitted form
    data, saved back to the JSON file, and the user is redirected
    to the home page.

    Args:
        post_id (int): The ID of the blog post to update.

    Returns:
        Response: The rendered update form for a GET request,
        a redirect to the home page after a successful update,
        or a 404 response if the post cannot be found.
    """

    blog_posts = read_posts_from_file(POSTS_FILE)

    result = fetch_post_by_id(post_id, blog_posts)

    if result is None:
        # Post not found
        return "Post not found", 404

    list_index, post = result



    # update the post's data according to the changes made in the update form
    if request.method == 'POST':
        # update the post fields using the new input
        blog_posts[list_index]["author"] = request.form.get("author")
        blog_posts[list_index]["title"] = request.form.get("title")
        blog_posts[list_index]["content"] = request.form.get("content")

        # save the updated posts list back to the JSON file
        save_posts_to_file(blog_posts, POSTS_FILE)

        return redirect(url_for('home')), 200


    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """
    Likes a blog post specified by the post_id from the posts blog storage.

    It handles the POST request by reading all posts from the JSON file
    and storing them in a list, it increments the number of likes for the specified
    post (from the retrieved list ) by matching its id with the post_id. Then it
    stores the list back in the JSON file.

    Parameters:
         post_id (str): The id of the post to delete

    Returns:
        Response: a redirect to the home page after successfully handling the like.
    """
    blog_posts = read_posts_from_file(POSTS_FILE)

    result = fetch_post_by_id(post_id, blog_posts)

    if result is None:
        # Post not found
        return "Post not found", 404

    list_index, post = result

    blog_posts[list_index]["likes"] += 1

    # save the updated posts list back to the JSON file
    save_posts_to_file(blog_posts, POSTS_FILE)

    return redirect(url_for('home')), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)