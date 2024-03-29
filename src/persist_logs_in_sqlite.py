import sqlite3
from flask import Flask, request
import json

app = Flask(__name__)

# Database path
db_path = '/home/students/ge49vav/public_html/Cocktail_Dashboard/src/log_database.db'


# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Function to set up the database table
def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create the logs table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_log TIMESTAMP,
            type_info TEXT,
            topic TEXT,
            event TEXT,
            instance_uuid TEXT,
            instance_name TEXT,
            instance_url TEXT,
            instance_info INTEGER,
            activity_uuid TEXT,
            endpoint TEXT,
            label TEXT,
            activity TEXT,
            variables_changed TEXT,  -- JSON string
            values_changed TEXT,  -- JSON string
            annotations TEXT -- JSON string
        );
        ''')

    conn.commit()
    conn.close()


@app.route('/writelogtodb', methods=['POST'])
def write_log_to_db():
    # Parse data from logs
    data = request.form.to_dict()
    notification_str = data.get('notification', '{}')
    notification = json.loads(notification_str)
    content_str = notification.get('content', {})
    annotations_dict = content_str.get('annotations', {})

    # Extract contents of '_generic' key, if it exists
    generic_contents = annotations_dict.get('_generic', {})
    annotations_json = json.dumps(generic_contents)

    # Extract relevant log fields
    timestamp_log = notification.get('timestamp')
    type_info = data.get('type')
    topic = data.get('topic')
    event = data.get('event')
    instance_uuid = notification.get('instance-uuid')
    instance_name = notification.get('instance-name')
    instance_url = notification.get('instance-url')
    instance_info = notification.get('instance')
    activity_uuid = content_str.get('activity-uuid')
    endpoint = content_str.get('endpoint')
    label = content_str.get('label')
    activity = content_str.get('activity')

    # Specific handling for 'dataelements' topic
    if data.get("topic") == 'dataelements':
        variables_changed = json.dumps(content_str.get('changed', []))
        values_changed = json.dumps(content_str.get('values', {}))
    else:
        variables_changed = None
        values_changed = None

    # Insert data into the database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO logs (
                timestamp_log, type_info, topic, event, 
                instance_uuid, instance_name, instance_url, instance_info, 
                activity_uuid, endpoint, label, activity, 
                variables_changed, values_changed, annotations
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
                    (
                        timestamp_log, type_info, topic, event,
                        instance_uuid, instance_name, instance_url, instance_info,
                        activity_uuid, endpoint, label, activity,
                        variables_changed, values_changed, annotations_json
                    )
                    )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'Error inserting into database: {e}')
        return 'Error', 500

    return 'Logged', 200


if __name__ == '__main__':
    setup_database()
    app.run(host='::', port=9090, debug=True)
