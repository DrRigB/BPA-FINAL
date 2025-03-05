# HealthHive

**HealthHive** is a health tracking application designed to help users track their health and wellness data efficiently. This project allows users to create accounts, manage their profiles, and monitor various health metrics over time.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

HealthHive is a full-stack application built using modern web technologies. It allows users to log their health data, track progress, and make informed decisions to improve their well-being. The project is aimed at individuals looking to stay on top of their health goals.

## Features

- **User Authentication:** Users can sign up, log in, and manage their profile.
- **Health Data Tracking:** Users can input and track different health metrics (e.g., weight, steps, calories).
- **Progress Visualization:** Visualize health data trends through graphs and charts.
- **Database Integration:** Data is stored securely in MySQL, allowing for easy retrieval and updates.
- **Responsive Design:** The app is fully responsive and optimized for mobile and desktop usage.

## Tech Stack

- **Frontend:**
  - HTML5, CSS3, JavaScript
  - Framework: Django
  - Libraries: Bootstrap
  
- **Backend:**
  - Python with Django
  - MySQL Database for storing user and health data
  - Authentication with Django's built-in auth system
  
- **Deployment:**
  - Heroku
  
## Installation

### Prerequisites

Before setting up the project locally, ensure you have the following installed:

- [Python](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- [Git](https://git-scm.com/)

### Setup

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/nxtcarson/healthhive
   cd healthhive
   ```

2. Install required Python packages:
   ```bash
   pip install django mysqlclient openai
   ```

3. Set up the database:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   cd djangotest
   python manage.py runserver
   ```

5. Visit `http://localhost:8000` in your web browser to access the application.
