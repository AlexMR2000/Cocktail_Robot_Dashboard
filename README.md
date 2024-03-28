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

In the folder docs (#TODO Link) there are useful images and videos documenting the functionalities of this project including a process and user perspective.  

## API Documentation

### Logger

The application serves as a logging service, capturing event data sent through HTTP POST requests to a specified endpoint ´/writelogtodb´. It processes the incoming data and stores it in a structured format within an SQLite database. The service is built using Flask, a micro web framework for Python, making it lightweight and suitable for both development and production environments.

#### Setting up

The database is configured to store logs in a table named logs, containing various fields such as timestamps, event types, instance details, activities, and annotations among others. The ´setup_database´ function is responsible for creating this table if it does not already exist.

#### API Endpoint `/writelogtodb`

This endpoint accepts POST requests containing event log data. The data is expected to be in a form-encoded format with a key named notification holding a JSON string of the event details. The application parses this data, along with other form fields, to extract relevant information such as event timestamp, type, instance details, activity information, and annotations

#### Function Descriptions

`get_db_connection()`
Establishes a connection to the SQLite database and sets the row factory to sqlite3.Row for convenient row access.

`setup_database()`
Ensures the existence of the logs table within the database, creating it with the appropriate schema if necessary.

`write_log_to_db()`
Main function for processing incoming POST requests. It extracts data from the request, formats it appropriately, and inserts it into the logs table in the database. In case of errors during database operations, it returns an HTTP 500 response.

#### Error Handling

The application includes basic error handling, particularly for database operations within the write_log_to_db function. Errors are caught, logged to the console, and result in an HTTP 500 response to indicate a server error.

### Dashboard Backend

### Dashboard Frontend
