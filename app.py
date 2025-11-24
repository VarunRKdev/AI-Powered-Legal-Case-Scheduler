from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

# Initialize Flask app
app = Flask(__name__)

# File paths
input_file = "New_Microsoft_Excel_Worksheet.csv"
output_file = "scheduled_cases.csv"

# Function to generate random deadlines
def generate_random_deadlines(num_cases, start_date=datetime.now(), days_range=180):
    return [(start_date + timedelta(days=np.random.randint(0, days_range))).strftime("%Y-%m-%d") for _ in range(num_cases)]

# Function to assign deadlines and priorities
def assign_deadlines_and_priorities(data):
    # Normalize priorities
    scaler = MinMaxScaler(feature_range=(1, 100))
    data['Normalized_Priority'] = scaler.fit_transform(data[['Priority']].fillna(0))

    # Assign deadlines
    data['Deadline'] = generate_random_deadlines(len(data))

    # Calculate urgency score
    data['Urgency_Score'] = data['Normalized_Priority'] / ((datetime.now() - pd.to_datetime(data['Deadline'])).dt.days + 1)

    # Sort by urgency
    data = data.sort_values(by='Urgency_Score', ascending=False)
    return data

# Route to display all cases
@app.route('/')
def index():
    try:
        data = pd.read_csv(output_file)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Case_ID', 'Case_Title', 'Case_Text', 'Priority', 'Deadline', 'Urgency_Score'])

    return render_template('index.html', cases=data.to_dict(orient='records'))

# Route to add a new case
@app.route('/add', methods=['GET', 'POST'])
def add_case():
    if request.method == 'POST':
        case_id = request.form['case_id']
        case_title = request.form['case_title']
        case_text = request.form['case_text']
        priority = request.form['priority']

        try:
            data = pd.read_csv(input_file)
        except FileNotFoundError:
            data = pd.DataFrame(columns=['Case_ID', 'Case_Title', 'Case_Text', 'Priority'])

        new_case = {
            'Case_ID': case_id,
            'Case_Title': case_title,
            'Case_Text': case_text,
            'Priority': priority
        }

        data = data.append(new_case, ignore_index=True)
        data.to_csv(input_file, index=False)

        # Reassign deadlines and priorities
        scheduled_data = assign_deadlines_and_priorities(data)
        scheduled_data.to_csv(output_file, index=False)

        return redirect(url_for('index'))

    return render_template('add.html')

# Route to delete a case
@app.route('/delete/<case_id>', methods=['POST'])
def delete_case(case_id):
    try:
        data = pd.read_csv(input_file)
        data = data[data['Case_ID'] != case_id]
        data.to_csv(input_file, index=False)

        # Reassign deadlines and priorities
        scheduled_data = assign_deadlines_and_priorities(data)
        scheduled_data.to_csv(output_file, index=False)
    except FileNotFoundError:
        pass

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
