"""ESP model (database) API."""
import sqlite3
import flask
import esp


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = esp.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


def get_all_users():
    """Get all users from db."""
    connection = get_db()
    curr = connection.execute(
        "Select * from Users"
    )
    return curr.fetchall()


def get_one_user(profile_url):
    """Get one user from db."""
    connection = get_db()
    curr = connection.execute(
        "SELECT * FROM Users "
        "WHERE profileUrl=?",
        (profile_url, )
    )
    return curr.fetchone()


def get_one_post(post_url):
    """Get one post from db."""
    connection = get_db()
    curr = connection.execute(
        "SELECT postID FROM Posts "
        "WHERE postUrl=?",
        (post_url, )
    )
    if curr is None:
        context = {
            "message": "Not Found",
            "status_code": 404
        }
        return flask.jsonify(**context), 404
    return curr.fetchone()


def create_user(first_name, last_name, company, industry, position, profile_url):
    """Create user in db."""
    connection = get_db()
    connection.execute(
        "INSERT INTO Users(firstName, lastName, company, industry, position, profileUrl) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, company, industry, position, profile_url)
    )
    connection.commit()
    new_user = {
        "firstName": first_name,
        "lastName": last_name,
        "company": company,
        "industry": industry,
        "position": position,
        "profileUrl": profile_url
    }
    return new_user


def delete_user(profile_url):
    """Delete user from db."""
    connection = get_db()
    connection.execute(
        "DELETE FROM Users "
        "WHERE profileUrl=?",
        (profile_url,)
    )
    connection.commit()
    return ''


def create_comment(post_content, first_name, last_name, comment_content, comment_url):
    """Create comment in db."""
    post_id = get_one_post(post_content)
    user_id = get_one_user(first_name, last_name)
    connection = get_db()
    connection.execute(
        "INSERT INTO Comments(postID, userID, commentContent, commentUrl) "
        "VALUES (?, ?, ?, ?)",
        (post_id, user_id, comment_content, comment_url)
    )


@esp.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()