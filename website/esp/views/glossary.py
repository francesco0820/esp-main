from esp.model import get_db
from flask import render_template
import esp


@esp.app.route('/glossary/')
def glossary_view():
    users = get_users()
    print("Users data passed to template:")
    for user in users:
        print(user)
    return render_template('glossary.html', users=users)


def get_users():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT firstName, lastName, company, position, profileUrl "
        "FROM Users "
        "ORDER BY lastName"
    )
    
    users = cursor.fetchall()

    print("Raw data fetched from database:")
    for user in users:
        print(user)

    user_dicts = []
    for user in users:
        user_dicts.append({
            'first_name': user['firstName'],
            'last_name': user['lastName'],
            'company': user['company'],
            'position': user['position'],
            'profile_url': user['profileUrl'],
            'last_name_initial': user['lastName'][0].upper()
        })

    print("Processed user dictionaries:")
    for user in user_dicts:
        print(user)
    
    return user_dicts
