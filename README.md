# Instinct - CourseCompanion

A data-driven academic communication platform that streamlines coordination between universities, professors, teaching assistants, and students.

## Overview

CourseCompanion is a comprehensive communication platform designed to improve academic interactions. Inspired by Piazza, our platform stays out of the way while offering powerful features that enhance everyday academic interactions. With automatic class enrollment, smarter post filtering, and cleaner conversation threads, CourseCompanion makes it easier for students to get the help they need—and for faculty to manage it all.

CourseCompanion enables users to have different roles on a per-class basis, meaning a user can be a student in some courses while simultaneously acting as a TA in others. All direct messages and forum posts are organized by class, ensuring relevant communications stay organized.

## Project Structure

CourseCompanion consists of three main components:

* **Streamlit App** (`./app` directory): The frontend user interface
* **Flask REST API** (`./api` directory): Backend services
* **MySQL Database**: Initialized with SQL scripts from the `./database-files` directory

## Prerequisites

Before you begin, ensure you have the following installed:
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode
- VSCode with the Python Plugin
- A distribution of Python running on your laptop (Anaconda or Miniconda recommended)
- Docker and Docker Compose

## Getting Started

### Environment Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/CourseCompanion.git
cd CourseCompanion
```

2. Set up the environment variables:
   * Create a `.env` file in the `api` folder based on the provided `.env.template` file
   * Ensure all required variables are set with appropriate values (MYSQL_ROOT_PASSWORD, DB_NAME...)

### Running the Application

#### Production Environment
To start all services in production mode:

```
docker compose up -d
```

This command will:
- Build all necessary images
- Start all containers in detached mode
- Execute SQL initialization scripts
- Set up the network between containers

#### Development/Testing Environment
For development and testing purposes:

```
# Start all containers in the background
docker compose -f docker-compose-testing.yaml up -d

# Shutdown and delete containers
docker compose -f docker-compose-testing.yaml down

# Start only a specific container (db, api, or app)
docker compose -f docker-compose-testing.yaml up db -d

# Stop containers without deleting them
docker compose -f docker-compose-testing.yaml stop
```

#### Accessing the Application
- Frontend (Streamlit App): http://localhost:8501
- Backend API: http://localhost:4000
- Database: http://localhost:3306 (accessible through your database client)

## REST API Matrix

This matrix outlines the resources identified from our user stories, including the supported HTTP methods and their associated actions.

| **Resource** | **GET** | **POST** | **PUT** | **DELETE** |
|--------------|---------|----------|---------|------------|
| `/posts` | Retrieve all posts with optional filtering parameters | n/a | n/a | n/a |
| `/posts/{id}` | Retrieve a specific post by ID | n/a | Update an existing post | Delete a specific post |
| `/posts/create` | n/a | Create a new post | n/a | n/a |
| `/comments/{id}` | Retrieve a specific comment | n/a | Update an existing comment | Delete a specific comment |
| `/comments/create` | n/a | Create a new comment on a post | n/a | n/a |
| `/comments/search` | Search for comments based on specific criteria | n/a | n/a | n/a |
| `/messages` | Retrieve all messages for the authenticated user | n/a | n/a | n/a |
| `/messages/{id}` | Retrieve a specific message | n/a | Update an existing message | Delete a message |
| `/messages/create` | n/a | Create a new message | n/a | n/a |
| `/users/{id}/roles` | Retrieve roles for a specific user | Create roles / enrollment for a specific user within a specific course | n/a | Delete roles / enrollment for a specific user within a specific course |
| `/courses` | Retrieve all courses with optional filtering parameters | Create a new course | n/a | n/a |
| `/courses/{id}` | Retrieve a specific course by ID | n/a | Update an existing course | Delete a specific course |
| `/courses/search` | Search for courses based on specific criteria | n/a | n/a | n/a |
| `/analytics/engagement` | Retrieve student engagement analytics | n/a | n/a | n/a |
| `/analytics/avg-enrollment` | Retrieves average enrollment per course section | n/a | n/a | n/a | 
| `/analytics/role-distribution`| Retrieves the distribution of user roles across the platform | n/a | n/a | n/a |
| `/analytics/active-hours` | Retrieves the most active hours based on post and comment creation | n/a | n/a | n/a | 
| `/analytics/avg-posts` | Finds average number of posts in each class | n/a | n/a | n/a |



## Troubleshooting

If you encounter any issues with the application, try these troubleshooting steps:

1. **Container fails to start**
   - Check logs with `docker compose logs [service_name]`
   - Verify your .env file contains all required variables

2. **Database connection issues**
   - Ensure the database container is running: `docker compose ps`
   - Check if database initialization completed successfully

## Team Members

- Donovan Murray
- Ziming Qi
- Maxim Ilin
- Jefferey Lafrance
- Avijit (Vee) Singh

## Version History

* 0.1
  * Initial Release
 
## Video Link

*https://www.youtube.com/watch?v=sPcV7JoRL8w
