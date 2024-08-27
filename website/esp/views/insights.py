from flask import render_template
import esp


@esp.app.route('/insights/', methods=['GET', 'POST'])
def insight_view():
    # if request.method == 'POST':
        # Handle form submission to add new insight
        # insight_name = request.form['insight_name']
        # insight_details = request.form['insight_details']
        # month_year = request.form['month_year']

        # conn = get_db()
        # c = conn.cursor()
        # c.execute('''
            # INSERT INTO Insights (insightName, insightDetails, monthYear)
            # VALUES (?, ?, ?)
        # ''', (insight_name, insight_details, month_year))
        # conn.commit()

        # return redirect(url_for('insight_view'))

    # Get the most recent month_year
    # conn = get_db()
    # c = conn.cursor()
    # c.execute('SELECT DISTINCT monthYear FROM Insights ORDER BY monthYear DESC LIMIT 1')
    # most_recent_month_year = c.fetchone()

    # if most_recent_month_year:
        # most_recent_month_year = most_recent_month_year[0]
        
        # Query insights for the most recent month_year
        # c.execute('SELECT insightName, insightDetails FROM Insights WHERE monthYear = ?', (most_recent_month_year,))
        # insights = [{'name': row[0], 'details': row[1]} for row in c.fetchall()]
    # else:
        # insights = []
        # most_recent_month_year = "No records"

    # Fetch all available months for the dropdown
    # c.execute('SELECT DISTINCT monthYear FROM Insights ORDER BY monthYear DESC')
    # available_months = [row[0] for row in c.fetchall()]

    # return render_template('insights.html', insights=insights, available_months=available_months, selected_month_year=most_recent_month_year)

    return render_template("insights.html")



# @esp.app.route('/insights/add', methods=['POST'])
# def add_insight():
    # insight_name = request.form['insight_name']
    # insight_details = request.form['insight_details']
    # month_year = request.form['month_year']

    # conn = get_db()
    # c = conn.cursor()
    # c.execute('''
        # INSERT INTO Insights (insightName, insightDetails, monthYear)
        # VALUES (?, ?, ?)
    # ''', (insight_name, insight_details, month_year))
    # conn.commit()

    # return redirect(url_for('insight_view'))
