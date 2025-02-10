# Real-Time Password Strength Analyzer Backend

## Overview
This project implements the backend for a Real-Time Password Strength Analyzer using Python, Flask, and Celery. The application analyzes the strength of passwords by attempting to reverse-engineer their hash values using techniques such as brute force, dictionary attacks, and rainbow table lookups.

## Features
- **Password Cracking Methods**: 
  - Brute Force
  - Dictionary Attack
  - Rainbow Table Lookup
- **Password Strength Analysis**: Evaluates password strength based on cracking time and complexity.
- **Distributed Architecture**: Utilizes Celery with Redis for distributed task management.
- **RESTful APIs**: 
  - Submit a hash for analysis.
  - Check task progress.
  - Retrieve results.
- **Security Considerations**: Rate limiting is implemented. (Authentication can be added as needed.)
- **Containerization**: Docker and Docker Compose are provided for easy deployment.

## Tech Stack
- **Backend**: Python, Flask
- **Task Queue**: Celery with Redis
- **Testing**: pytest
- **Containerization**: Docker, docker-compose

## Setup

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Running Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/password-analyzer-backend.git
   cd password-analyzer-backend
