# Key Account Manager (KAM) Lead Management System

## Overview
Udaan's Key Account Manager (KAM) Lead Management System is a comprehensive, Django-based platform designed to optimize the management of leads, interactions, and account performance for large restaurant accounts. This system supports Key Account Managers in effectively tracking leads, planning calls, and monitoring account performance.

The application integrates advanced tools like Celery, Celery Beat, Redis, and MySQL to provide efficient task scheduling, data management, and asynchronous operations. Additionally, it features an automated email notification system to alert Key Account Managers upon lead allocation, ensuring timely follow-ups and proactive engagement.

---
### Link to website : [Click Here](http://3.107.25.45).
### Video Link: [Click Here](https://drive.google.com/file/d/1YC1Nce1fA0KaeQlOLNzfdfMmJn49ZAXz/view?usp=sharing).
### GitHub Repository:  [Click Here](https://github.com/jaynandwana200/KAM.git)



## Features

### 1. Lead Management
- Add, update, and delete restaurant leads with detailed information.
- Monitor lead status transitions with automatic data updates.
- **Notify Key Account Managers via email when a lead is allocated to them.**
- Remove interactions of inactive leads to maintain a clean database.
- **Notify Key Acoount managers about allocation and deallocation of Lead via email on change of Key account manager.**

### 2. Contact Management
- Add, update, and delete Points of Contact (POCs) with detailed information.
- Manage multiple Points of Contact (POCs) for each lead with:
  - Role specification (e.g., Manager, Chef).
  - Contact details (name, email, phone).
- Support for hierarchical roles to better understand account dynamics.

### 3. Interaction Tracking
- Add, update, and delete interactions with detailed information.
- Record all interactions, including:
  - Call logs with timestamps and summaries.
  - Order placements linked to specific leads.
  - Visits related to specific leads
- Maintain a detailed chronological history of interactions for analysis.
- Notify related lead on generation or updation of interaction.

### 4. Call Planning
- Set custom call frequencies for each lead.
- **Automatically generate call interactions on basis of call frequency of leads using asyc background process with help of celery.**
- Automatically highlight leads requiring follow-ups based on:
  - Call frequency.
  - Last interaction date.
- View a daily call plan to streamline communication.

### 5. Performance Monitoring
- Identify well-performing accounts based on:
  - Average orders placed.
  - Ordering patterns and frequency.
- Detect under-performing accounts to provide targeted support.

### 6. Search Functionality
- Search leads on basis of lead details.

### 6. Create Key account manager
- Create Key account manager to enable Email notification functionality and utilize the system.

---

## Technology Stack

### Frontend
- **HTML/CSS**: Provides a simple, interactive and intutive design.

### Backend
- **Django**: Provides a robust web framework for fast and secure development.

### Database
- **MySQL**: Manages structured data with efficient querying and indexing.

### Task Management
- **Celery**: Handles asynchronous tasks, such as scheduling calls and processing interactions.
- **Celery Beat**: Adds periodic task scheduling.
- **Redis**: Acts as a message broker for Celery and caches frequently accessed data.

### Additional Libraries
- **Email Library**: Sends automated email notifications for lead allocations, updates, reminders, and reports.

### Testing
- **Pytest**: Provides solid testing strategy includes comprehensive coverage, scenario and edge case testing, and integration tests.

### Deployment

- **Gunicorn**:  Python Web Server Gateway Interface (WSGI) HTTP server.
- **Nginx**: Reverse Proxy
- **Amazon EC2**: Ubuntu instance for deployment.


---
## Database Schema
![ Alt text](https://github.com/jaynandwana200/KAMwithCelery/blob/main/django_schema_diagram.png?raw=true)
## System Requirements

### 1. Hardware Requirements
### Server Hardware:
- CPU: At least 4 cores
- RAM: Minimum 4 GB (8 GB recommended for production)
- Storage: SSD with at least 20 GB free space for logs, database, and application
- Network: 100 mbps network connectivity for web hosting and inter-service communication
### Development Machine:
- CPU: Dual-core processor
- RAM: 4 GB minimum
- Storage: 10 GB available disk space
### 2. Software Requirements
- Operating System: Ubuntu 20.04 LTS or newer (recommended), Windows 10 or macOS (for local development)
- Browser: Firefox, Google chrome, Microsoft edge.




## Installation and Running Instructions

### Prerequisites
- Python 3.9+
- MySQL 5.7+
- Redis 6.0+

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/jaynandwana200/KAM.git
   ```
2. Navigate to the project directory:
   ```bash
   cd KAM/KAMassignment
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the MySQL database:
   - Create a new MYSQL database instance on aws and configure credentials in the settings.py file.
   ```
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': '',
          'USER' : '',
          'PASSWORD' : '',
          'HOST' : '',
          'PORT' : 3306,
          "OPTIONS": {
              'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
              'charset': 'utf8mb4',
              "autocommit": True,
          }
      }
    }
   ```
5. Configure redis message broker and Email settings in settings.py file
```
CELERY_BROKER_URL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
```

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```
7. Start Redis server:
   ```bash
   redis-server
   ```
8. Start Celery workers:
   ```bash
   celery -A KAMassignment.celery worker --pool=solo -l info
   celery -A KAMassignment beat -l info
   ```
9. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

---

## Test Execution guide

### Install Testing Dependencies
Install the required testing libraries:
```bash
pip install pytest pytest-django
```
### Running All Tests
Execute all tests using:
```bash
python manage.py test KAM
```

### Running Specific Tests
To run specific test cases, use the `-k` flag:
```bash
python manage.py test -k test_views
python manage.py test -k test_changeKAM
python manage.py test -k test_tasks
python manage.py test -k test_urls
python manage.py test -k test__models
python manage.py test -k test_integration
python manage.py test -k test_timezone
```

---

### Key Test Cases

### Full Workflow Integration Test
- **File**: `test_integration.py`
- **Purpose**: Validates the entire workflow:
  1. Add a KAM.
  2. Create a lead.
  3. Trigger Celery task.
  4. Verify interactions and email logic.


### Change KAM Test
- **File**: `test_changeKAM.py`
- **Purpose**: Tests the reassignment of a lead from one KAM to another, including email notifications to both old and new KAMs.


### Time Zone Handling Test
- **File**: `test_timezone.py`
- **Purpose**: Validates call scheduling with proper handling of UTC storage and time zone conversions for display.

---

### Logs and Debugging

### 4.1 Celery Logs
Monitor Celery worker logs for task execution:
```bash
celery -A KAMassignment.celery worker --pool=solo -l info
```

### 4.2 Django Server Logs
Check for errors or debug messages during testing:
```bash
python manage.py runserver
```

---

### 5. Success Criteria
1. All tests pass with no errors.
2. Celery tasks execute correctly, and interactions are logged in the database.
3. Time zone conversions and email notifications work as expected.

For additional support, refer to Django’s [official documentation](https://docs.djangoproject.com/).




## Deployment Documentation for Your Django Project

### Configure Django on EC2 (Ubuntu)
- Update `ALLOWED_HOSTS` in `settings.py` to include your public IP address.
- Install the `whitenoise` package in your project.
- Add `'whitenoise.runserver_nostatic'` to `INSTALLED_APPS`.
- Add `'whitenoise.middleware.WhiteNoiseMiddleware'` to `MIDDLEWARE`.

### Generate a Key Pair for SSH
- Generate an SSH key pair for secure server access.
- Adjust security group settings for your EC2 instance:
  - Navigate to **Inbound Rules** and configure the necessary rules to allow connections.
- Use `chmod` to secure the private key and SSH to connect to the server.

### Configure Firewall Settings
- Execute the following commands to configure the firewall:
  ```
  sudo ufw app list
  sudo ufw allow OpenSSH
  sudo ufw enable
  sudo ufw status
  ```

### Install Necessary Packages
- Update the package list:
  ```
  sudo apt update
  ```
- Install Python dependencies, Nginx, and virtualenv:
  ```
  sudo apt install python3-pip python3-dev libpq-dev nginx curl virtualenv
  ```

### Deploy Your Project
- Clone your repository:
  ```
  git clone https://github.com/jaynandwana200/KAM.git
  cd KAM/KAMassignemnt
  ```
- Set up the virtual environment and install requirements:
  ```
  virtualenv env
  source env/bin/activate
  pip install -r requirements.txt
  pip install gunicorn
  ```
- Apply migrations and prepare static files:
  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py collectstatic
  ```
- Allow traffic on port 8000:
  ```
  sudo ufw allow 8000
  python manage.py runserver 0.0.0.0:8000
  ```
- Deactivate the virtual environment:
  ```
  deactivate
  ```

#### Configure Gunicorn
- Create and edit the Gunicorn socket file:
  ```
  sudo nano /etc/systemd/system/gunicorn.socket
  ```
  Add the following:
  ```
  [Unit]
  Description=gunicorn socket

  [Socket]
  ListenStream=/run/gunicorn.sock

  [Install]
  WantedBy=sockets.target
  ```
  Save and exit (Ctrl+O, Enter, Ctrl+X).
- Create and edit the Gunicorn service file:
  ```
  sudo nano /etc/systemd/system/gunicorn.service
  ```
  Add the following:
  ```
  [Unit]
  Description=gunicorn daemon
  Requires=gunicorn.socket
  After=network.target

  [Service]
  User=ubuntu
  Group=www-data
  WorkingDirectory=/home/ubuntu/KAM/KAMassignemnt
  ExecStart=/home/ubuntu/KAM/KAMassignemnt/env/bin/gunicorn \
            --access-logfile - \
            --workers 3 \
            --bind unix:/run/gunicorn.sock \
            KAM.wsgi:application

  [Install]
  WantedBy=multi-user.target
  ```
  Save and exit (Ctrl+O, Enter, Ctrl+X).
- Start and enable Gunicorn:
  ```
  sudo systemctl start gunicorn.socket
  sudo systemctl enable gunicorn.socket
  sudo systemctl status gunicorn.socket
  ```
- Verify the socket:
  ```
  file /run/gunicorn.sock
  ```
- Test the Gunicorn service:
  ```
  curl --unix-socket /run/gunicorn.sock localhost
  ```

#### Configure Nginx
- Create and edit an Nginx configuration file:
  ```
  sudo nano /etc/nginx/sites-available/samplename
  ```
  Add the following:
  ```
  server {
      listen 80;
      server_name Your PublicIP;

      location = /favicon.ico { access_log off; log_not_found off; }
      location /static/ {
          root /home/ubuntu/YourProject;
      }

      location / {
          include proxy_params;
          proxy_pass http://unix:/run/gunicorn.sock;
      }
  }
  ```
  Save and exit (Ctrl+O, Enter, Ctrl+X).
- Enable the configuration and test Nginx:
  ```
  sudo ln -s /etc/nginx/sites-available/samplename /etc/nginx/sites-enabled
  sudo nginx -t
  sudo systemctl restart nginx
  ```
- Update firewall rules:
  ```
  sudo ufw delete allow 8000
  sudo ufw allow 'Nginx Full'
  ```

#### Fix Missing CSS on Admin Site
- Edit the main Nginx configuration file:
  ```
  sudo nano /etc/nginx/nginx.conf
  ```
  Change the `user` to `ubuntu`.
  Save and exit (Ctrl+O, Enter, Ctrl+X).

### Live Link: [Click Here](http://13.55.186.165).


## Usage Guide

### Accessing the System
- Open `http://localhost:8000` in your browser.
- Log in using admin credentials or a user account.

### Workflow
1. **Lead Management**:
   - Navigate to the "Leads" section.
   - Add or update restaurant details.
   - Allocate leads to Key Account Managers and trigger email notifications automatically.
2. **Contact Management**:
   - Add POCs under the respective lead.
   - View or edit existing contact information.
3. **Call Planning**:
   - Review the daily call schedule.
   - Mark completed calls and add notes.
4. **Performance Monitoring**:
   - Analyze performance metrics in the "Reports" section.
   - Identify trends and take corrective actions.

---

## Demonstration
A detailed walkthrough of the system is provided in the project video. It covers:
1. Code setup and environment configuration.
2. Live demonstration of major features.
3. Sample inputs and outputs for key functionalities.

- Video Link: [Click Here](#) (Replace with the actual link).

---

## Evaluation Highlights
- **Modularity**: Clean separation of features and reusable components.
- **Extensibility**: Easy to add new features, e.g., analytics dashboards.
- **Performance**: Optimized database queries and task scheduling.
- **Scalability**: Futhur Scalability can be easily achieved by using celery to handle multpile process at same time and improving on resources.	
- **Error Handling**: Comprehensive logging and graceful error messages.

---

## Bonus Features
- Automated email notifications for lead allocations and updates.
- Scalable task management with Celery and Redis.
- Comprehensive performance metrics for actionable insights.

---

