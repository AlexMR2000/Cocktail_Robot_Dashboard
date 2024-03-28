# Cocktail Dashboard

Prepared by Alexander Reisenauer (Matr.Nr.: 03712872)

- Supervisor: Dr. Jürgen Mangler
- Chair: TUM School of Computation, Information and Technology (Prof. Rinderle-Ma)

## Architectural Design

### Overview

This project provides a management dashboard for the cocktail robot developed by the chair TUM CIT. Therefore, a CPEE process is designed to orchestrate and simulate various functionalities of the cocktail robot. Further, this documentation provides an overview and detailed descriptions of a Python application that uses Flask for creating a web service and SQLite for database management. Please refer to the following graphic for further architectural details of this project:  

![alt text](https://github.com/AlexMR2000/Cocktail_Dashboard/blob/main/docs/Cocktail_Dashboard_ArchitecturalDesign_Overview.jpg)

### Components

This project incorporates the following components: 

1. Simulator: In fact, the CPEE process simulates the cocktail robot's actions in its typical working environment. That is: Setting up the robot, receiving and accepting orders, preparing and serving cocktails and shutting down. 
3. Logger: The Python script persist_logs_in_sqlite.py serves as an  interface between CPEE's logging interface and the backend. Event logs that are produced as long as the Simulator is running are parsed and persisted in a SQLite database that is located on my account on the "lehre" server.  
4. Dashboard Backend: The Python script backend_cocktail_dashboard encorporates a Flask Python Web Framework that prepares relevant logs as soon as new logs are written in the database. Hence, it constantly scans the database for updates to send new data to the Frontend.
5. Dashboard Frontend: This html script visualizes the logs in a user-friendly and comprehensive way enabling developer and non-developer to gain an overview about the cocktail robot's status and various relevant statistics. The Dashboard is view-only which aligns with the project's requirements.

### CPEE Model

The CPEE Model serves as Simulator and placeholder for more detailed (sub-)processes. In this project, the basic functionalities of a cocktail robot are implemented consisting of the following actions: 
- Setting up
- Getting an order
- Checking whether there are sufficient ingredients
- If yes: Preparing and serving the cocktail
- If no: Filling up the ingredients
- Waiting for new orders
- Shutting down
These basic functionalities are extended by optional (random) process legs such as random shut-downs (and reboots) of the robot or handling of orders that are impossible to fulfill.   

## Installation

1. Clone the repository with the following command:

`git clone https://github.com/AlexMR2000/Cocktail_Dashboard`

2. Install the required packages with the following command:

`pip install -r requirements.txt`

3. Update the configuration file with the required parameters. The configuration file is located at config/config.json and src/config.py. #TODO
4. Run the project with the following command:
`#TODO`
5. The Dashboard can be accessed at the configured port.
6. Load all CPEE models that are located in the CPEE folder #TODO Link
7. Start one or more CPEE models and watch the Dashboard's magic

## Demo with Images and Videos 

In the folder docs ([Link to Data Folder](/cpee_models/)) there are useful images and videos documenting the functionalities of this project including a process and user perspective.  

## API Documentation

### Logger

The application serves as a logging service, capturing event data sent through HTTP POST requests to a specified endpoint ´/writelogtodb´. It processes the incoming data and stores it in a structured format within an SQLite database. The service is built using Flask, a micro web framework for Python, making it lightweight and suitable for both development and production environments.

#### Application Setup

The database is configured to store logs in a table named logs, containing various fields such as timestamps, event types, instance details, activities, and annotations among others. The ´setup_database´ function is responsible for creating this table if it does not already exist.

#### Endpoint 

The endpoint `/writelogtodb` accepts POST requests containing event log data. The data is expected to be in a form-encoded format with a key named notification holding a JSON string of the event details. The application parses this data, along with other form fields, to extract relevant information such as event timestamp, type, instance details, activity information, and annotations

#### Key Functions

- `get_db_connection()` establishes a connection to the SQLite database and sets the row factory to sqlite3.Row for convenient row access.
- `setup_database()` ensures the existence of the logs table within the database, creating it with the appropriate schema if necessary.
- `write_log_to_db()` is the main function for processing incoming POST requests. It extracts data from the request, formats it appropriately, and inserts it into the logs table in the database. In case of errors during database operations, it returns an HTTP 500 response.

#### Error Handling

The application includes basic error handling, particularly for database operations within the write_log_to_db function. Errors are caught, logged to the console, and result in an HTTP 500 response to indicate a server error.

### Dashboard Backend

The application is a Flask-based web application designed for real-time monitoring and analysis of cocktail-making robots. It fetches and streams data from an SQLite database to a dashboard, displaying statistics such as cocktail counts, ingredient usage, robot status, and failures. The application is structured around two main Flask routes: the dashboard view and a streaming endpoint for real-time updates. The dashboard serves as the user interface, displaying various statistics and the current status of cocktail-making robots. The stream endpoint continuously polls the database for new log entries, processes them, and sends updates to the dashboard via Server-Sent Events (SSE).

#### Application Setup

The application defines a global `Flask` instance and specifies the path to the SQLite database that contains the log data. It also initializes two dictionaries, `last_activity_by_uuid` and `first_out_of_order_time`, to track the latest activity timestamps and the first occurrence of out-of-order status for each robot, respectively.

#### Endpoints

- Dashboard (`/`) serves the main dashboard page by rendering a template named `frontend_cocktail_dashboard.html`. The dashboard is the user interface where the real-time statistics and robot statuses are displayed.
- The Stream (`/stream`) endpoint is a generator function wrapped in a Flask `Response` object with the MIME type set to `text/event-stream`, enabling SSE. This endpoint is responsible for continuously querying the database for new log entries, processing the data, and sending updates to the client in real-time.

#### Key Functions

The `generate` function is the core of the streaming endpoint. It enters an infinite loop, periodically querying the database for new logs since the last processed entry. The function updates various statistics, such as cocktail counts, ingredient usage, robot failures, and the current status of each robot. It then formats these statistics as JSON and yields them as SSE data to the client.

#### Real-time Data Processing

The application processes various types of events logged by the robots, such as cocktail orders (`calling` event type) and robot status updates. It tracks the number of cocktails made, the usage of individual ingredients, and instances of robot failures. The function also manages the status of each robot, marking robots as out of order if they have been inactive for more than a minute and removing them from the tracking list if the out-of-order status persists for more than five minutes.

#### Error Handling

The application includes basic error handling for database operations and JSON parsing. It ensures that the application continues to run even if individual log entries contain malformed data. The streaming function uses a `try-except` block around database operations to handle any potential exceptions gracefully.

### Dashboard Frontend

The dashboard serves as a real-time monitoring interface for tracking the performance and activities of a cocktail robot system. It displays metrics such as the number of cocktails made, ingredients used, robot failures, and the current status of robots. Additionally, it includes visual representations of data through charts.

#### Structure and Style

##### HTML Structure

The HTML document is structured into several main components:

- Header: Displays the title of the dashboard and the last reset timestamp.
- Main Content: Comprises an image container and a dashboard container. The dashboard container includes sections for displaying key metrics and charts.
- Footer: Shows the last update timestamp and copyright information.

##### CSS Styling

The styling defines a clean and modern look for the dashboard, with a focus on readability and clear data presentation. Key styling elements include:

- Background colors for the header and footer.
- Flexbox layout for positioning dashboard elements.
- Custom styles for dashboard metrics (cards) to highlight key data points.
- Chart containers styled to fit within the dashboard layout harmoniously.

#### Key Functions

##### JavaScript and EventSource

The dashboard leverages JavaScript to dynamically update its content based on real-time data streamed from the server:

- EventSource: Used to establish a persistent connection with the server, listening for updates sent to the /stream endpoint.
- Data Processing: Incoming data is parsed and used to update various parts of the dashboard, such as metrics, robot statuses, and charts.
- Charts: Utilizes Chart.js to display and update bar charts representing the number of cocktails made and the ingredients used.

##### Dynamic Updates

Key dynamic elements updated through JavaScript include:

- Cocktails Made and Ingredients Used: Metrics are displayed prominently and updated in real-time as data is received.
- Robot Failures: A counter indicating the number of times robots have encountered failures.
- Robot Status: Individual sections are dynamically added or removed based on the active status of each robot, displaying current activities or indicating if a robot is out of order.
- Charts: The cocktails and ingredients charts are updated with new data points as they arrive, providing a visual representation of the usage trends over time.

#### Real-time Data Processing

The dashboard is designed to handle real-time data efficiently:

- Event Handling: Listens for new data via the EventSource connection and updates the dashboard components accordingly.
- Error Handling: Includes basic error handling for the EventSource connection, logging errors to the console.
- Cleanup and Removal: Old data, such as inactive robot statuses, are removed from the dashboard to maintain relevance and clarity.
