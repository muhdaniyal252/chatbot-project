# Chatbot Project

## Getting Started

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repo_url>
cd chatbot-project
```

### 2. Environment Setup

A sample environment file `.env-sample` is provided. Create your own `.env` file based on this sample:

```bash
cp .env-sample .env
```

Edit `.env` as needed for your configuration.

### 3. Build and Run with Docker

Build and start the application using Docker Compose:

```bash
docker compose up --build
```

This will build the Docker image and start the application.

### 4. Access the Application

Once the application is running, open your browser and go to:

```
http://localhost:8000
```

#### Login Credentials

- **Username:** user
- **Password:** user

After logging in, you will see agents and chats on the left sidebar. You can create a new agent and start chatting.

## How to Chat

Once you have accessed the chat interface:

- To send a written message, type your message in the input box and either press the Enter key or click the Send button.
- To send an audio message, click the microphone button located next to the Send button to start recording. Click the microphone button again to stop recording.
- After stopping the recording, your audio message will be sent to the backend for processing.
- You will receive:
  - Your original audio recording
  - A transcription of your message
  - The response in both audio and text formats

This allows for seamless interaction using either text or voice.

## Running Test Cases

To run the test cases:

1. Enter the running container:
   ```bash
   docker exec -it <container_id> bash
   ```
2. Navigate to the project directory:
   ```bash
   cd /app/myproject
   ```
3. Run the tests:
   ```bash
   pytest
   ```
   All test cases in `myproject/test` will be executed.

## Potential Upgrades

- Better error handling for improved reliability and user experience.
- Add logging for better monitoring and debugging.
- Integrate Redis to enable background query processing for seamless user interaction.
- Develop a separate frontend using React or another modern framework/library.
- Implement FastAPI as a separate microservice for improved scalability and modularity.

---

For any questions or issues, please open an issue in this repository.
