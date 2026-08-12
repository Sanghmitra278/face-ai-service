# Face AI Service

A Python-based Face AI service for face detection, face recognition, and facial feature extraction. The service provides AI-powered face processing capabilities that can be integrated with mobile applications, web applications, or backend systems through APIs.

## Features

* Face detection and processing
* Face recognition
* Face embedding generation
* Face similarity/comparison
* Pre-trained face recognition models
* REST API integration
* Local development environment support
* Model-based facial analysis

## Project Structure

```text
face-ai-service/
│
├── trained_models/
│   ├── facenet512.h5
│   └── facenet512.keras
│
├── app/
│   └── ...
│
├── services/
│   └── ...
│
├── routes/
│   └── ...
│
├── requirements.txt
├── README.md
├── .gitignore
└── ...
```

> The exact folder structure may vary depending on the current implementation.

## Technologies

* Python
* TensorFlow / Keras
* OpenCV
* FaceNet / FaceNet512
* NumPy
* REST API

## Face Recognition Models

The service uses trained/pre-trained facial recognition models for generating facial embeddings and performing face recognition operations.

Large model files are maintained separately when required because GitHub has file-size limitations.

Current model files include:

```text
trained_models/
├── facenet512.h5
└── facenet512.keras
```

If the models are stored outside the Git repository, copy them into the appropriate `trained_models` directory before running the service.

## Requirements

* Python 3.12
* pip
* Git
* Required Python packages listed in `requirements.txt`

## Installation

Clone the repository:

```bash
git clone https://github.com/Sanghmitra278/face-ai-service.git
cd face-ai-service
```

Switch to the project branch if required:

```bash
git checkout master
```

Create a virtual environment:

```bash
python -m venv venv312
```

Activate the environment on Windows:

```powershell
.\venv312\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a local `.env` file containing the configuration required by the service.

Example:

```env
HOST=127.0.0.1
PORT=5000
```

Do not commit sensitive credentials, API keys, passwords, or production configuration to GitHub.

## Running the Service

Activate the virtual environment:

```powershell
.\venv312\Scripts\Activate.ps1
```

Then start the application using the project's configured entry point.

For example:

```bash
python app.py
```

or, if the project uses another entry point:

```bash
python main.py
```

The actual command depends on the application entry point used by the project.

## API

The service is designed to expose face AI functionality through REST APIs.

Typical operations may include:

### Face Detection

Accepts an image and detects faces present in the image.

### Face Embedding

Processes a detected face and generates a numerical facial embedding.

### Face Recognition

Compares facial embeddings to determine whether faces belong to the same person.

### Face Similarity

Calculates similarity between two facial embeddings or face images.

Refer to the application's API routes for the exact endpoints, request formats, and response structures.

## Development

The project is developed and tested locally on Windows.

Recommended development environment:

```text
Windows
Python 3.12
VS Code
Virtual Environment
Git / GitHub
```

## Git and Large Files

The Python virtual environment is intentionally excluded from Git:

```text
venv312/
```

The virtual environment should be recreated locally using:

```bash
python -m venv venv312
```

Large AI model files may be maintained separately or through Git LFS depending on repository requirements.

## Security

Do not commit:

* `.env` files containing secrets
* API keys
* Database passwords
* Authentication tokens
* Private certificates
* Production credentials

Local development configuration should remain local.

## Project Status

**Status:** Active Development

The Face AI Service is being developed as an AI backend/service component for integration with applications requiring facial recognition and face-processing capabilities.

## License

Add the appropriate license information here when the project license is finalized.

