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
git clone git@github.com:aryanb1522006/ram-cpu-monitor-application.git
cd cpu-ram-monitor
