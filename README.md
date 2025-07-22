# Incident Prediction System

This system detects anomalies and classifies logs using real-time Kafka streaming, ML models, FastAPI backend, and React frontend.

## Components

- MLflow tracking
- Model training
- REST API
- Dashboard
- Alerting (Email)
- Docker deployment

## How to Run

1. Train the models either mannually or simply run the command to start the docker container, it will automatically train the models. you will have to restart the container once the model_trainer container exits so that the backend runs with the trained models. If you train them mannually then connect the database accordingly, adjust the host aswell.

2. Start the backend service using the fastapi command.

3. Launch Frontend using npm run build , npm start.

4. Monitor via alerts that are sent automatically on detecting anomally.
   Make sure you have adjusted the sender and reciever email details before launching the backend and frontend to avoid conflicts.

5. All these steps can be done automatically using the docker command.

Command is : docker-compose build --no-cache
docker-compose up -d

Note: use this command in command prompt in the project directory.
Tip: Docker Desktop should be running.
