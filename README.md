# Cocktail Dashboard

Prepared by Alexander Reisenauer (Matr.Nr.: 03712872)

- Supervisor: Dr. Jürgen Mangler
- Chair: TUM School of Computation, Information and Technology (Prof. Rinderle-Ma)

## Architectural Design

### Overview

This project provides a management dashboard for the cocktail robot developed by the chair TUM CIT. Therefore, a CPEE process is deisgned to orchestrate and simulate various functionalities of the cocktail robot. The resulting event logs are persisted in a SQLite database and sent to the dashboard via SSE connection. Please refer to the following graphic for further architectural details of this project:  

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

-- link to Syn&Share Folder --

## API Documentation

### Logger

### Dashboard Backend

### Dashboard Frontend
