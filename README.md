# Task Management App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, intuitive web application for managing tasks, built with Flask and designed with a Material You-inspired theme.

## Demo

Check out the live demo of the application:

<a href="https://task-management-beta-swart.vercel.app/">Click here for a live demo!</a>

## Overview

This application provides a user-friendly interface for creating, updating, and tracking tasks. It features:

- **Clean UI:** Material You-inspired design for a visually appealing experience.
- **Local Storage:** Tasks are persisted locally, ensuring data is preserved across sessions.
- **Night Mode:** A toggle for switching between light and dark themes.
- **Responsive Design:** Adapts seamlessly to various screen sizes.
- **Flask Backend:** Robust API for managing tasks.

## Features

- **Add Tasks:** Easily create new tasks with titles, descriptions, and due dates.
- **Search:** Quickly find tasks by title or description.
- **Complete/Delete Actions:** Mark tasks as complete or permanently remove them.
- **Night Mode:** Switch between light and dark themes for comfortable viewing.
- **Local Storage:** Tasks are automatically saved in your browser.
- **Due-Date Validation:** Prevents creating tasks with due dates in the past.

## Technologies Used

- **Frontend:**
  - HTML5
  - CSS3 (with custom Material You-inspired theme)
  - JavaScript
  - Font Awesome
- **Backend:**
  - Python
  - Flask
  - Flask-SQLAlchemy
  - SQLite

## Setup

1. **Clone the Repository:**

   ```bash
   git clone [repository URL]
   cd [repository directory]

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv

3. **Activate the Virtual Environment:**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install Flask Flask-SQLAlchemy

5. **Initialize the Database:**

   Run the application (this step typically creates the necessary database tables):

   ```bash
   python app.py

6. **Run the Application:**

   ```bash
   python app.py
   ```

   Then open your browser and navigate to `http://127.0.0.1:5000/` to view the app.

## Unit Testing

To run the unit tests and ensure the application’s reliability, execute:

```bash
python -m unittest test_app.py
```
