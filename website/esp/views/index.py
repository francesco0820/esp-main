import flask
from flask import render_template, request, jsonify
import esp
import calendar
from esp.model import get_db

@esp.app.route("/")
def show_index():
    """Index page default view."""
    return render_template("index.html")


@esp.app.route('/get-executives/', methods=['GET'])
def get_executives():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    connection = get_db()
    query = f"%{query}%"
    sql_query = "SELECT DISTINCT firstName || ' ' || lastName AS fullName FROM Users WHERE fullName LIKE ? LIMIT 10"
    results = connection.execute(sql_query, (query,)).fetchall()

    executive_names = [row['fullName'] for row in results]
    return jsonify(executive_names)


@esp.app.route('/get-options/<field>/', methods=['POST'])
def get_options(field):
    connection = get_db()
    if field in ['industry', 'position', 'company']:
        query = f"SELECT DISTINCT {field} FROM Users WHERE {field} IS NOT NULL"
        options = connection.execute(query).fetchall()
        return jsonify([row[field] for row in options])
    elif field == 'theme':
        query = "SELECT DISTINCT theme FROM Themes"
        options = connection.execute(query).fetchall()
        return jsonify([row['theme'] for row in options])


@esp.app.route('/filter/', methods=['POST'])
def filter_data():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        # Handle date filter separately since it doesn't have an operator
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    query = """
        SELECT Posts.* FROM Posts
        JOIN Users ON Posts.userID = Users.userID
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes ON PostThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    print(f"Final query: {query}")
    print(f"Params: {params}")

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    print(f"Results: {results}")

    # Summary data to return
    summary_data = {
        'unique_audience_members': len(set([row['userID'] for row in results])),
        'total_unique_posts': len(results),
        'total_engagements': sum(row['totalEngagement'] for row in results),
        'average_engagements_per_post': round(sum(row['totalEngagement'] for row in results) / len(results)) if len(results) > 0 else 0,
    }

    return jsonify(summary_data)


@esp.app.route('/chart-data/posts-engagements', methods=['POST'])
def posts_vs_engagements():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    # Process filters
    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    # Construct the query for Posts
    posts_query = """
        SELECT COUNT(DISTINCT Posts.postID) as post_count, SUM(Posts.totalEngagement) as total_engagement
        FROM Posts
        JOIN Users ON Posts.userID = Users.userID
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes ON PostThemes.themeID = Themes.themeID
    """

    # Construct the query for Engagements
    engagements_query = """
        SELECT COUNT(DISTINCT Engagements.reactionID) as engagement_count
        FROM Engagements
        JOIN Users ON Engagements.userID = Users.userID
        LEFT JOIN EngagementThemes ON Engagements.reactionID = EngagementThemes.engagementID
        LEFT JOIN Themes ON EngagementThemes.themeID = Themes.themeID
    """

    if query_conditions:
        conditions_str = " WHERE " + " AND ".join(query_conditions)
        posts_query += conditions_str
        engagements_query += conditions_str

    # Execute the queries
    connection = get_db()
    post_results = connection.execute(posts_query, tuple(params.values())).fetchone()
    engagement_results = connection.execute(engagements_query, tuple(params.values())).fetchone()

    # Data to return for the chart
    chart_data = {
        'post_count': post_results['post_count'],
        'engagement_count': engagement_results['engagement_count']
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/posts-volume', methods=['POST'])
def posts_volume_over_time():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    # Apply filters (similar to the postsEngagementsChart route)
    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    # Construct the query to aggregate post volume over time
    query = """
        SELECT 
            Posts.yearOfPost || '-' || Posts.monthOfPost || '-' || Posts.dayOfPost AS post_date, 
            COUNT(Posts.postID) AS post_count
        FROM Posts
        JOIN Users ON Posts.userID = Users.userID
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes on PostThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += " GROUP BY post_date ORDER BY Posts.yearOfPost, Posts.monthOfPost, Posts.dayOfPost"

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    chart_data = {
        'dates': [row['post_date'] for row in results],
        'post_counts': [row['post_count'] for row in results]
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/engagements-volume', methods=['POST'])
def engagements_volume_over_time():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    # Apply filters (similar to the postsEngagementsChart route)
    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Engagements.yearOfPost >= ? AND Engagements.monthOfPost >= ? AND Engagements.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Engagements.yearOfPost <= ? AND Engagements.monthOfPost <= ? AND Engagements.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"EngagementThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"EngagementThemes.themeID IS NOT NULL")

    # Construct the query to aggregate post volume over time
    query = """
        SELECT 
            Engagements.yearOfPost || '-' || Engagements.monthOfPost || '-' || Engagements.dayOfPost AS post_date, 
            COUNT(Engagements.reactionID) AS engagement_count
        FROM Engagements
        JOIN Users ON Engagements.userID = Users.userID
        LEFT JOIN EngagementThemes ON Engagements.reactionID = EngagementThemes.engagementID
        LEFT JOIN Themes on EngagementThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += " GROUP BY post_date ORDER BY Engagements.yearOfPost, Engagements.monthOfPost, Engagements.dayOfPost"

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    chart_data = {
        'dates': [row['post_date'] for row in results],
        'engagement_counts': [row['engagement_count'] for row in results]
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/top-themes-posts', methods=['POST'])
def top_themes_by_post_volume():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    # SQL query to get top themes by post volume
    query = """
        SELECT 
            Themes.theme AS theme,
            COUNT(Posts.postID) AS post_count
        FROM Posts
        JOIN PostThemes ON Posts.postID = PostThemes.postID
        JOIN Themes ON PostThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += " GROUP BY Themes.theme ORDER BY post_count DESC LIMIT 10"

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    chart_data = {
        'themes': [row['theme'] for row in results],
        'post_counts': [row['post_count'] for row in results]
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/top-themes-engagements', methods=['POST'])
def top_themes_by_engagement_volume():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Engagements.yearOfPost >= ? AND Engagements.monthOfPost >= ? AND Engagements.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Engagements.yearOfPost <= ? AND Engagements.monthOfPost <= ? AND Engagements.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"EngagementThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"EngagementThemes.themeID IS NOT NULL")

    # SQL query to get top themes by engagement volume
    query = """
        SELECT 
            Themes.theme AS theme,
            COUNT(Engagements.reactionID) AS engagement_count
        FROM Engagements
        JOIN EngagementThemes ON Engagements.reactionID = EngagementThemes.engagementID
        JOIN Themes ON EngagementThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += " GROUP BY Themes.theme ORDER BY engagement_count DESC LIMIT 10"

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    chart_data = {
        'themes': [row['theme'] for row in results],
        'engagement_counts': [row['engagement_count'] for row in results]
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/content-formats-posts', methods=['POST'])
def content_formats_data():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    # SQL query to get counts of each content format
    query = """
        SELECT 
            Posts.contentFormat AS format,
            COUNT(Posts.postID) AS format_count
        FROM Posts
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes on PostThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += " GROUP BY Posts.contentFormat ORDER BY format_count DESC"

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    chart_data = {
        'formats': [row['format'] for row in results],
        'format_counts': [row['format_count'] for row in results]
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/content-formats-engagements', methods=['POST'])
def content_formats_eng_data():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Engagements.yearOfPost >= ? AND Engagements.monthOfPost >= ? AND Engagements.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Engagements.yearOfPost <= ? AND Engagements.monthOfPost <= ? AND Engagements.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"EngagementThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"EngagementThemes.themeID IS NOT NULL")

    # SQL query to get counts of each content format
    query = """
        SELECT 
            Engagements.contentFormat AS format,
            COUNT(Engagements.reactionID) AS format_count
        FROM Engagements
        LEFT JOIN EngagementThemes ON Engagements.reactionID = EngagementThemes.engagementID
        LEFT JOIN Themes on EngagementThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += " GROUP BY Engagements.contentFormat ORDER BY format_count DESC"

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    chart_data = {
        'formats': [row['format'] for row in results],
        'format_counts': [row['format_count'] for row in results]
    }

    return jsonify(chart_data)


@esp.app.route('/chart-data/top-executives', methods=['POST'])
def top_executives_data():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    # SQL query to get the top 10 executives by total posts and engagements
    query = """
        SELECT 
            Users.firstName || ' ' || Users.lastName AS executive_name,
            Users.userID,
            Users.profileUrl AS profile_url,
            COUNT(DISTINCT Posts.postID) AS post_count,
            COUNT(DISTINCT Engagements.reactionID) AS engagement_count,
            (COUNT(DISTINCT Posts.postID) + COUNT(DISTINCT Engagements.reactionID)) AS total_count
        FROM Users
        LEFT JOIN Posts ON Users.userID = Posts.userID
        LEFT JOIN Engagements ON Users.userID = Engagements.userID
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes on PostThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += """
        GROUP BY Users.userID
        ORDER BY total_count DESC
        LIMIT 10
    """

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    table_data = [
        {
            'executive_name': row['executive_name'],
            'userID': row['userID'],
            'profile_url': row['profile_url'],
            'post_count': row['post_count'],
            'engagement_count': row['engagement_count'],
            'total_count': row['total_count']
        }
        for row in results
    ]

    return jsonify(table_data)


@esp.app.route('/chart-data/top-posts', methods=['POST'])
def top_posts_data():
    filters = request.json['filters']
    query_conditions = []
    params = {}

    month_name_map = {str(i).zfill(2): month for i, month in enumerate(calendar.month_name) if month}

    for field, filter_info in filters.items():
        if field == 'date':
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            if start_date:
                year, month, day = start_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost >= ? AND Posts.monthOfPost >= ? AND Posts.dayOfPost >= ?")
                params['start_year'] = year
                params['start_month'] = month_name
                params['start_day'] = day
            if end_date:
                year, month, day = end_date.split('-')
                month_name = month_name_map.get(month)
                query_conditions.append("Posts.yearOfPost <= ? AND Posts.monthOfPost <= ? AND Posts.dayOfPost <= ?")
                params['end_year'] = year
                params['end_month'] = month_name
                params['end_day'] = day
        elif field == 'executive':
            name = filter_info.get('name')
            if name:
                query_conditions.append("Users.firstName || ' ' || Users.lastName = ?")
                params['executive_name'] = name
        else:
            operator = filter_info.get('operator')
            values = filter_info.get('value')

            if operator and values:  # Ensure both operator and value exist
                if field in ['industry', 'position', 'company']:
                    if operator == 'has_any':
                        query_conditions.append(f"Users.{field} IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Users.{field} NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Users.{field} = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"Users.{field} IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"Users.{field} IS NOT NULL")
                elif field == 'theme':
                    if operator == 'has_any':
                        query_conditions.append(f"Themes.theme IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'has_none':
                        query_conditions.append(f"Themes.theme NOT IN ({', '.join(['?' for _ in values])})")
                        params.update({f"{field}_{i}": v for i, v in enumerate(values)})
                    elif operator == 'is_exactly':
                        query_conditions.append(f"Themes.theme = ?")
                        params[field] = values[0]
                    elif operator == 'is_empty':
                        query_conditions.append(f"PostThemes.themeID IS NULL")
                    elif operator == 'is_not_empty':
                        query_conditions.append(f"PostThemes.themeID IS NOT NULL")

    # SQL query to get the top 25 posts by engagement count
    query = """
        SELECT DISTINCT
            Posts.postID,
            Users.firstName || ' ' || Users.lastName AS executive_name,
            Users.company AS company,
            Users.industry AS industry,
            Themes.theme AS theme,
            Posts.content AS post_content,
            Posts.totalEngagement AS engagement_count,
            Posts.postUrl AS post_url,
            Users.profileUrl AS profile_url
        FROM Posts
        JOIN Users ON Posts.userID = Users.userID
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes ON PostThemes.themeID = Themes.themeID
    """

    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)

    query += """
        ORDER BY engagement_count DESC
        LIMIT 25
    """

    connection = get_db()
    results = connection.execute(query, tuple(params.values())).fetchall()

    # Prepare the data to return
    table_data = [
        {
            'executive_name': row['executive_name'],
            'company': row['company'],
            'industry': row['industry'],
            'theme': row['theme'],
            'post_content': row['post_content'],
            'engagement_count': row['engagement_count'],
            'post_url': row['post_url'],
            'profile_url': row['profile_url']
        }
        for row in results
    ]

    return jsonify(table_data)


@esp.app.route('/search-post-content', methods=['POST'])
def search_post_content():
    search_term = request.json.get('searchTerm', '').strip()
    if not search_term:
        return jsonify({"summary_data": {}, "posts": []})

    connection = get_db()

    search_term_param = f'%{search_term}%'

    # Query Posts
    posts_query = """
        SELECT 
            Posts.postID,
            Users.firstName || ' ' || Users.lastName AS executive_name,
            Users.company AS company,
            Users.industry AS industry,
            Themes.theme AS theme,
            Posts.content AS post_content,
            Posts.totalEngagement AS engagement_count,
            Posts.postUrl AS post_url,
            Users.profileUrl AS profile_url
        FROM Posts
        JOIN Users ON Posts.userID = Users.userID
        LEFT JOIN PostThemes ON Posts.postID = PostThemes.postID
        LEFT JOIN Themes ON PostThemes.themeID = Themes.themeID
        WHERE Posts.content LIKE ?
        ORDER BY Posts.totalEngagement DESC
        LIMIT 25
    """

    # Query Engagements
    engagements_query = """
        SELECT 
            Engagements.reactionID AS postID,
            Users.firstName || ' ' || Users.lastName AS executive_name,
            Users.company AS company,
            Users.industry AS industry,
            Themes.theme AS theme,
            Engagements.postContent AS post_content,
            Engagements.totalEngagement AS engagement_count,
            Engagements.postUrl AS post_url,
            Users.profileUrl AS profile_url
        FROM Engagements
        JOIN Users ON Engagements.userID = Users.userID
        LEFT JOIN EngagementThemes ON Engagements.reactionID = EngagementThemes.engagementID
        LEFT JOIN Themes ON EngagementThemes.themeID = Themes.themeID
        WHERE Engagements.postContent LIKE ?
        ORDER BY Engagements.totalEngagement DESC
        LIMIT 25
    """

    posts_results = connection.execute(posts_query, (search_term_param,)).fetchall()
    engagements_results = connection.execute(engagements_query, (search_term_param,)).fetchall()

    # Combine and sort results
    combined_results = posts_results + engagements_results
    combined_results.sort(key=lambda x: x['engagement_count'], reverse=True)

    # Take the top 25 after combining
    top_results = combined_results[:25]

    # Summary calculations
    unique_audience = len(set(row['profile_url'] for row in top_results))
    total_posts = len(top_results)
    total_engagements = sum(row['engagement_count'] for row in top_results)
    average_engagements = total_engagements / total_posts if total_posts > 0 else 0

    # Convert results to JSON-friendly format
    table_data = [
        {
            'executive_name': row['executive_name'],
            'company': row['company'],
            'industry': row['industry'],
            'theme': row['theme'],
            'post_content': row['post_content'],
            'engagement_count': row['engagement_count'],
            'post_url': row['post_url'],
            'profile_url': row['profile_url']
        }
        for row in top_results
    ]

    summary_data = {
        'unique_audience': unique_audience,
        'total_posts': total_posts,
        'total_engagements': total_engagements,
        'average_engagements': round(average_engagements)
    }

    return jsonify({"summary_data": summary_data, "posts": table_data})
