# Knowledge Base - AI based Bitcoin Price Forecast

## Ownership
Created and maintained Ayushi Garachh and Ayan Ghosh

## Course Information
The project is created as part of the course 'M. Grum: Advanced AI-based Application Systems' by the Junior Chair for Business Information Science, esp. AI-based Application Systems at University of Potsdam.

## Data origin
Data is scrapped from Yahoo Finance for period 01.01.2025 to 01.01.2026. (https://finance.yahoo.com/quote/BTC-EUR/history/?)

## Model Knowledge Data
- **currentSolution.keras**: The saved architecture and weights of the trained Artificial Neural Network.
- Serves as the central repository of "learned" patterns for the decentralized system.

## Docker setup and verification
Note - replace ghoshayan with your docker username

### 1. Build the Docker Image manually with Dockerfile
From the root of the repository, run:

```bash
docker build --tag ghoshayan/knowledgebase_bitcoin_forecast:latest -f images/knowledgeBase_bitcoin_forecast/Dockerfile .
```

### 2. Have a look on the image created

```bash
docker run -it --rm ghoshayan/knowledgebase_bitcoin_forecast:latest sh
```

### Run the following commands inside shell

```bash
ls /knowledgeBaseSource
exit
```

### 4. Create Docker volume 

```bash
docker volume ls # To verify if volume ai_system exist or not
docker volume create ai_system # ONLY IF DOES NOT EXISTS
docker volume rm ai_system # Delete volume MUST IF EXIST
```

### 3. Test local docker image

```bash
docker-compose -f images/knowledgeBase_bitcoin_forecast/docker-compose.yml up
```
### Verify using docker app and verify tmp folder in Files of container

### 4. Push docker image to ```docker https://hub.docker.com/``` of account called ```ghoshayan```

```bash
docker image push ghoshayan/knowledgebase_bitcoin_forecast:latest
```

### 5. Close docker image container

```bash
docker-compose -f images/knowledgeBase_bitcoin_forecast/docker-compose.yml down
```

## License 
This project is licensed under the AGPL-3.0 license.