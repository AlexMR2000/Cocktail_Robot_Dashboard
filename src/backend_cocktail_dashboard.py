from flask import Flask, render_template, Response
import json
import sqlite3
import time
from datetime import datetime, timedelta
import dateutil.parser
import dateutil.tz

app = Flask(__name__)

# Database path
db_path = '/home/students/ge49vav/public_html/Cocktail_Dashboard/src/log_database.db'


# Create global variables
last_activity_by_uuid = {}
first_out_of_order_time = {}


# Render the dashboard
@app.route('/')
def dashboard():
    return render_template('frontend_cocktail_dashboard.html')


# Send data to dashboard via SSE connection
@app.route('/stream')
def stream():
    def generate():
        global last_activity_by_uuid, first_out_of_order_time
        
        # Initialize stats
        cocktail_counts = {}
        ingredients_counts = {}
        ingredients_counts_total = 0
        robot_failures = 0
        cocktails_made = 0
        robot_status_by_uuid = {}
        last_known_cocktail_by_uuid = {}
        ingredient_counts = {}

        # Track the last log ID that was processed
        last_log_id = 0

        # Getting the timestamp since when the dashboard is active
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT MIN(timestamp_log) FROM logs")
        row = cur.fetchone()
        first_log_timestamp = row[0] if row else None
        conn.close()

        # Convert the first_log_timestamp to the desired format if it exists
        if first_log_timestamp:
            first_log_datetime = dateutil.parser.isoparse(first_log_timestamp)
            formatted_first_log_timestamp = first_log_datetime.strftime('%d.%m.%Y, %H:%M:%S')
        else:
            formatted_first_log_timestamp = "N/A"

        # Checking for new data
        while True:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # Select logs that have not been processed yet
            cur.execute("SELECT * FROM logs WHERE id > ? ORDER BY id ASC", (last_log_id,))
            logs = cur.fetchall()

            for log in logs:
                instance_uuid = log['instance_uuid']
                event_type = log['event']
                timestamp = dateutil.parser.isoparse(log['timestamp_log'])
                annotations = {}

                # Update the last activity timestamp for this robot
                last_activity_by_uuid[instance_uuid] = timestamp

                # Parse 'annotations' correctly
                if event_type == 'calling':
                    if log['annotations']:
                        try:
                            # Attempt to parse the JSON content of the annotations column
                            parsed_annotations = json.loads(log['annotations'])
                            # Ensure that annotations is a dictionary even if parsed_annotations is None
                            annotations = parsed_annotations if isinstance(parsed_annotations, dict) else {}
                        except json.JSONDecodeError as e:
                            continue

                    # Check for cocktail stats and update counts
                    if 'dashboard_cocktail_stats' in annotations:
                        cocktail_name = annotations['dashboard_cocktail_stats']
                        cocktail_counts[cocktail_name] = cocktail_counts.get(cocktail_name, 0) + 1

                    # Check for robot status and update counts
                    if 'dashboard_robot_status' in annotations:
                        if annotations['dashboard_robot_status'] == "Mix and serve":
                            cocktails_made += 1
                        elif annotations['dashboard_robot_status'] == "The Robot crashed. Shutting down...":
                            robot_failures += 1

                    # Check for ingredients used and update counts
                    if 'dashboard_item_used' in annotations:
                        ingredients_name = annotations['dashboard_item_used']
                        ingredients_counts[ingredients_name] = ingredient_counts.get(ingredients_name, 0) + 1
                        ingredients_counts_total += 1

                    # Handle the idle status separately
                    if annotations.get('dashboard_robot_status') == "Idle":
                        robot_status_by_uuid[instance_uuid] = "The robot is currently waiting"
                        if instance_uuid in last_known_cocktail_by_uuid:
                            del last_known_cocktail_by_uuid[instance_uuid]

                    # If the robot is accepting an order, remember the cocktail being made
                    elif annotations.get(
                            'dashboard_robot_status') == "Accepting order" and 'dashboard_cocktail_stats' in annotations:
                        last_known_cocktail_by_uuid[instance_uuid] = annotations['dashboard_cocktail_stats']

                    # If there's a known cocktail being made, display the status with the cocktail name
                    elif instance_uuid in last_known_cocktail_by_uuid:
                        robot_status_by_uuid[
                            instance_uuid] = f"Making the cocktail '{last_known_cocktail_by_uuid[instance_uuid]}'. Current process step: {annotations.get('dashboard_robot_status', 'Processing')}"

                    # For any other robot status, just display the status text
                    else:
                        robot_status = annotations.get('dashboard_robot_status', '')
                        if robot_status:
                            robot_status_by_uuid[instance_uuid] = robot_status

                    # Update ingredient counts
                    item_used = annotations.get('dashboard_item_used')
                    if item_used:
                        ingredient_counts[item_used] = ingredient_counts.get(item_used, 0) + 1

            # Get the current time
            current_time = datetime.now(dateutil.tz.UTC)
            robots_to_remove = []

            # Declare a robot to be 'Out of Order' if it's inactive for more than one minute
            for uuid, last_timestamp in last_activity_by_uuid.items():
                if current_time - last_timestamp > timedelta(minutes=1):
                    robot_status_by_uuid[uuid] = "** Out of Order **"
                    if uuid not in first_out_of_order_time:
                        first_out_of_order_time[uuid] = last_timestamp

            # Remove a robot from the dashboard if it's inactive for more than five minutes
            for uuid, out_of_order_time in first_out_of_order_time.items():
                if current_time - out_of_order_time > timedelta(minutes=5):
                    robots_to_remove.append(uuid)

            # Update the last log ID processed
            last_log_id = log['id']

            # If there are updates, send them to the client
            if logs:
                update = {
                    'first_log_timestamp': formatted_first_log_timestamp,
                    'cocktail_counts': cocktail_counts,
                    'ingredients_counts': ingredients_counts,
                    'ingredients_counts_total': ingredients_counts_total,
                    'robot_failures': robot_failures,
                    'cocktails_made': cocktails_made,
                    'robot_status_by_uuid': robot_status_by_uuid,
                    'ingredient_counts': ingredient_counts,
                    'robots_to_remove': robots_to_remove,
                }
                yield f"data: {json.dumps(update)}\n\n"

            # Clean up after sending the update
            for uuid in robots_to_remove:
                if uuid in first_out_of_order_time:
                    del first_out_of_order_time[uuid]

            cur.close()
            conn.close()
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host="::", port=9011, debug=True)
