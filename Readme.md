# CPU and RAM Monitor Application

This is a Python-based desktop application that monitors real-time CPU clock speed, CPU usage, and RAM usage. The data is stored in a MySQL database and can be visualized through dynamic graphs. Additionally, the application allows the user to query historical data and calculate average CPU clock, CPU usage, and RAM usage for a specified time range.

## Features

- **Real-Time Monitoring**: Fetch real-time CPU clock speed, CPU utilization, and RAM usage using PowerShell scripts and plot them dynamically using Matplotlib.
- **MySQL Database Integration**: Store monitoring data in a MySQL database and periodically delete data older than 5 days.
- **CPU Information**: Fetch and display CPU-specific information using PowerShell.
- **Averaging Data**: Calculate and display the average CPU clock speed, CPU utilization, and RAM usage for a desired timestamp range.
- **GUI**: Built with Tkinter for easy interaction, providing options to choose what to monitor or query averages.

## Requirements

- Python 3.x
- MySQL Server
- PowerShell (for running the scripts)
- Libraries/Modules:
  - `subprocess`
  - `mysql-connector-python`
  - `matplotlib`
  - `tkinter`

## Setup

### 1. Clone the repository
```bash
git clone git@github.com:aryanb1522006/ram-cpu-monitor-application.git \
&& cd cpu-ram-monitor
```

### 2. Install Python dependencies
```bash
pip install mysql-connector-python matplotlib
```

### 3. MySQL Database Setup
```sql
CREATE DATABASE application;
USE application;

CREATE TABLE SystemStats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpu_clock VARCHAR(255),
    cpu_usage VARCHAR(255),
    ram_usage VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. MySQL connection credentials
Ensure that your MySQL connection is properly set up in the Python script:

```python
connection = mysql.connector.connect(
    host='localhost',
    user='your_mysql_user',
    password='your_mysql_password',
    database='application'
)
```

### 5. PowerShell Scripts
Ensure you have the following PowerShell scripts in the correct path:

- `cpu_clock.ps1`: Returns current CPU clock speed.
- `cpu_utilization.ps1`: Returns current CPU utilization.
- `ram.ps1`: Returns current RAM usage.
- `cpu_info.ps1`: Returns CPU information.

## Usage

1. **Welcome Page**: A welcome window will appear. Click "Proceed" to enter the main window.
2. **Dropdown Menu**: The dropdown menu allows you to select one of the following options:
   - **CPU Clock Speed**: Display real-time CPU clock speed.
   - **CPU Utilization**: Display real-time CPU utilization percentage.
   - **RAM Usage**: Display real-time RAM usage percentage.
   - **Check Average (CPU, RAM)**: Enter a time range and get the average CPU clock speed, CPU usage, and RAM usage during that period.
   - **CPU Info**: Fetch and display detailed CPU-specific information (e.g., model, cores, threads).
## Database Maintenance

The application automatically deletes data older than 5 days from the `SystemStats` table.
## Sample Images
![App Screenshot](https://i.imgur.com/jtQI8uw.png)

![App Screenshot](https://i.imgur.com/y1NWJmU.png)

![App Screenshot](https://i.imgur.com/Vldjq9n.png)