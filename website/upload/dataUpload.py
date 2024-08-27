import logging
import csv
from datetime import datetime
import os
import sys
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

from esp import app
from esp.model import get_db, get_one_user, get_one_post


def extract_datetime(datetime_str):
    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        year_of_post = dt.strftime('%Y')
        month_of_post = dt.strftime('%B')
        day_of_post = dt.strftime('%d')
        day_of_week = dt.strftime('%A')
        military_hour = dt.strftime('%H:00-%H:59')
        # logger.debug(f"Results: {year_of_post} {month_of_post} {day_of_week} {military_hour}")
        return year_of_post, month_of_post, day_of_post, day_of_week, military_hour
    except ValueError as e:
        return None, None, None, None, None


def insert_post(connection, user_id, row, is_repost):
    # Required fields
    post_url = row.get('postUrl')
    like_count = int(row.get('likeCount', 0))
    comment_count = int(row.get('commentCount', 0))
    repost_count = int(row.get('repostCount', 0))
    is_repost = bool(is_repost)
    year_of_post, month_of_post, day_of_post, day_of_week, military_hour = extract_datetime(row.get('postTimestamp'))
    total_engagement = like_count + comment_count + repost_count

    # Optional fields
    content = row.get('postContent', '')
    themes = row.get('Themes', '').split(',')
    content_format = row.get('type', '')
    img_url = row.get('imgUrl', '')
    shared_post_url = row.get('sharedPostUrl', '')
    video_url = row.get('videoUrl', '')
    shared_job_url = row.get('sharedJobUrl', '')
    article_title = row.get('articleTitle', '')
    article_subtitle = row.get('articleSubtitle', '')
    article_reading_duration = int(row.get('articleReadingDuration', 0)) if row.get('articleReadingDuration') else None
    article_cover_url = row.get('articleCoverUrl', '')
    event_url = row.get('eventUrl', '')
    event_title = row.get('eventTitle', '')
    document_title = row.get('documentTitle', '')
    document_page_count = int(row.get('documentPageCount', 0)) if row.get('documentPageCount') else None
    thought_leadership = bool(row.get('thoughtLeadership', False))

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Posts (userID, content, contentFormat, postUrl, imgUrl, likeCount, commentCount, repostCount, sharedPostUrl, "
        "isRepost, videoUrl, sharedJobUrl, articleTitle, articleSubtitle, articleReadingDuration, articleCoverUrl, eventUrl, eventTitle, "
        "yearOfPost, monthOfPost, dayOfPost, dayOfWeek, militaryHour, documentTitle, documentPageCount, thoughtLeadership, totalEngagement) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id['userID'], content, content_format, post_url, img_url, like_count, comment_count, repost_count, shared_post_url,
         is_repost, video_url, shared_job_url, article_title, article_subtitle, article_reading_duration, article_cover_url, event_url, event_title,
         year_of_post, month_of_post, day_of_post, day_of_week, military_hour, document_title, document_page_count, thought_leadership, total_engagement)
    )
    post_id = cursor.lastrowid

    # Insert themes into db, allows for multiple themes per post
    for theme in themes:
        theme_id = get_or_create_theme(connection, theme.strip())
        cursor.execute(
            "INSERT INTO PostThemes (postID, themeID) VALUES (?, ?)",
            (post_id, theme_id)
        )
    connection.commit()


def insert_engagement(connection, user_id, row):
    # Required fields
    post_url = row.get('postUrl')
    like_count = int(row.get('likeCount', 0))
    comment_count = int(row.get('commentCount', 0))
    repost_count = int(row.get('repostCount', 0))
    action = row.get('action')
    reaction_type, is_comment = classify_types(action)
    year_of_post, month_of_post, day_of_post, day_of_week, military_hour = extract_datetime(row.get('postTimestamp'))
    total_engagement = like_count + comment_count + repost_count

    # Optional fields
    post_id = get_one_post(row.get('postUrl')) if get_one_post(row.get('postUrl')) else None
    post_content = row.get('postContent', '')
    themes = row.get('Themes', '').split(',')
    content_format = row.get('type', '')
    img_url = row.get('imgUrl', '')
    comment_content = row.get('commentContent', '')
    comment_url = row.get('commentUrl', '')
    shared_post_url = row.get('sharedPostUrl', '')
    video_url = row.get('videoUrl', '')
    shared_job_url = row.get('sharedJobUrl', '')
    article_title = row.get('articleTitle', '')
    article_subtitle = row.get('articleSubtitle', '')
    article_reading_duration = int(row.get('articleReadingDuration', 0)) if row.get('articleReadingDuration') else None
    article_cover_url = row.get('articleCoverUrl', '')
    event_url = row.get('eventUrl', '')
    event_title = row.get('eventTitle', '')
    document_title = row.get('documentTitle', '')
    document_page_count = int(row.get('documentPageCount', 0)) if row.get('documentPageCount') else None
    thought_leadership = bool(row.get('thoughtLeadership', False))

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Engagements (userID, postID, postContent, contentFormat, postUrl, imgUrl, likeCount, commentCount, repostCount, "
        "commentContent, commentUrl, sharedPostUrl, isComment, reactionType, videoUrl, sharedJobUrl, articleTitle, articleSubtitle, "
        "articleReadingDuration, articleCoverUrl, eventUrl, eventTitle, yearOfPost, monthOfPost, dayOfPost, dayOfWeek, militaryHour, documentTitle, "
        "documentPageCount, thoughtLeadership, totalEngagement) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id['userID'], post_id, post_content, content_format, post_url, img_url, like_count, comment_count, repost_count,
         comment_content, comment_url, shared_post_url, is_comment, reaction_type, video_url, shared_job_url, article_title, article_subtitle,
         article_reading_duration, article_cover_url, event_url, event_title, year_of_post, month_of_post, day_of_post, day_of_week, military_hour, document_title,
         document_page_count, thought_leadership, total_engagement)
    )
    engagement_id = cursor.lastrowid

    for theme in themes:
        theme_id = get_or_create_theme(connection, theme.strip())
        cursor.execute(
            "INSERT INTO EngagementThemes (engagementID, themeID) VALUES (?, ?)",
            (engagement_id, theme_id)
        )

    connection.commit()


def classify_types(reaction_type):
    is_comment = False
    if 'celebrates this' in reaction_type:
        reaction_type = 'Celebrates'
    elif 'likes this' in reaction_type:
        reaction_type = 'Likes'
    elif 'contributed to this collaborative article' in reaction_type:
        reaction_type = 'Contributed to article'
    elif 'commented on this' in reaction_type:
        reaction_type = 'Comments'
        is_comment = True
    elif 'replied to' in reaction_type:
        reaction_type = 'Replied to a comment'
    elif any(keyword in reaction_type for keyword in ['loves this', 'finds this funny', 'finds this insightful', 'supports this', 'comment on this funny']):
        reaction_type = 'Reaction'
    else:
        reaction_type = 'Liked a comment'

    return reaction_type, is_comment


def get_or_create_theme(connection, theme):
    cursor = connection.cursor()
    cursor.execute("SELECT themeID FROM Themes WHERE theme = ?", (theme,))
    result = cursor.fetchone()
    if result:
        return result['themeID']
    else:
        cursor.execute("INSERT INTO Themes (theme) VALUES (?)", (theme,))
        connection.commit()
        return cursor.lastrowid


def upload_from_csv(file_path):
    with app.app_context():
        connection = get_db()
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            if header[0].startswith('\ufeff'):
                header[0] = header[0].replace('\ufeff', '')
            reader.fieldnames = header

            for row in reader:
                user = get_one_user(row.get('profileUrl'))
                if not user:
                    continue

                action = row.get('action')
                if action == 'Post':
                    insert_post(connection, user, row, 0)
                elif 'reposted this' in action:
                    insert_post(connection, user, row, 1)
                else:
                    insert_engagement(connection, user, row)
        print("Data uploaded successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dataUpload.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        upload_from_csv(file_path)
