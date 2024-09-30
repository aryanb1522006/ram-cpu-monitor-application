import subprocess
import mysql.connector
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
from tkinter import *
from tkinter import ttk  
from tkinter import messagebox

# Path to the PowerShell scripts
# Specify path according to saved data on your machone
cpu_clock_script = "C:\\scripts\\cpu_clock.ps1"
cpu_usage_script = "C:\\scripts\\cpu_utilization.ps1"
ram_usage_script = "C:\\scripts\\ram.ps1"
cpu_info_script = "C:\\scripts\\cpu_info.ps1"  

# MySQL database connection settings
connection = mysql.connector.connect(
    host='localhost',#daefault is localhost
    user='root',#default is root
    password='Your password',
    database='application'
)

my_cursor = connection.cursor()


def calculate_averages(start_time, end_time):
    sql = """
    SELECT 
        AVG(CAST(SUBSTRING_INDEX(cpu_clock, ': ', -1) AS DECIMAL(10, 5))) AS avg_cpu_clock, 
        AVG(cpu_usage) AS avg_cpu_usage, 
        AVG(ram_usage) AS avg_ram_usage 
    FROM SystemStats 
    WHERE timestamp BETWEEN %s AND %s
    """
    my_cursor.execute(sql, (start_time, end_time))
    result = my_cursor.fetchone()
    
    if result:
        avg_cpu_clock, avg_cpu_usage, avg_ram_usage = result
        return avg_cpu_clock, avg_cpu_usage, avg_ram_usage
    return None, None, None

# Function to fetch CPU information using PowerShell
def fetch_cpu_info():
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", cpu_info_script],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# Function to display CPU Information in Tkinter
def show_cpu_info():
    cpu_info = fetch_cpu_info()

    info_window = Toplevel()
    info_window.title("CPU Information")
    info_window.geometry("400x300")

    text_widget = Text(info_window, wrap=WORD)
    text_widget.insert(1.0, cpu_info)
    text_widget.pack(expand=True, fill=BOTH)

def show_averages():
    avg_window = Toplevel()
    avg_window.title("Enter Timestamp Range")
    avg_window.geometry("400x300")

    
    start_time_entry = Entry(avg_window, width=30)
    end_time_entry = Entry(avg_window, width=30)

    def on_submit():
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()
        
       
        avg_cpu_clock, avg_cpu_usage, avg_ram_usage = calculate_averages(start_time, end_time)
        
        if avg_cpu_clock is not None:
            result_label.config(text=f"Average CPU Clock: {avg_cpu_clock:.2f} GHz\n"
                                     f"Average CPU Usage: {avg_cpu_usage:.2f}%\n"
                                     f"Average RAM Usage: {avg_ram_usage:.2f}%")
        else:
            result_label.config(text="No data found for the given timestamp range.")

    Label(avg_window, text="Enter Start Timestamp (YYYY-MM-DD HH:MM:SS):").pack(pady=5)
    start_time_entry.pack(pady=5)

    Label(avg_window, text="Enter End Timestamp (YYYY-MM-DD HH:MM:SS):").pack(pady=5)
    end_time_entry.pack(pady=5)

    
    submit_button = Button(avg_window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    result_label = Label(avg_window, text="")
    result_label.pack(pady=10)

    avg_window.mainloop()
def on_select(event):
    selected_option = dropdown_var.get() 

    if selected_option == "CPU Clock Speed":
        start_graph(selected_option)
    elif selected_option == "CPU Utilization":
        start_graph(selected_option)
    elif selected_option == "RAM Usage":
        start_graph(selected_option)
    elif selected_option == "Check Average (CPU, RAM)":
        show_averages()
    elif selected_option == "CPU Information":
        show_cpu_info()  # Show CPU info if selected
          
def delete_old_data():
   #delete data older than 5 days
    delete_sql = "DELETE FROM SystemStats WHERE timestamp < NOW() - INTERVAL 5 DAY"
    my_cursor.execute(delete_sql)
    connection.commit()
    print("Old data deleted (older than 5 days).")

def insert_data():
    
    cpu_clock = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", cpu_clock_script],
        capture_output=True, text=True
    )

    cpu_usage = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", cpu_usage_script],
        capture_output=True, text=True
    )

    ram_usage = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ram_usage_script],
        capture_output=True, text=True
    )

    cpu_clock_output = cpu_clock.stdout.strip()
    cpu_usage_output = cpu_usage.stdout.strip()
    ram_usage_output = ram_usage.stdout.strip()

    # Inserting data into MySQL
    sql = "INSERT INTO SystemStats (cpu_clock, cpu_usage, ram_usage) VALUES (%s, %s, %s)"
    my_cursor.execute(sql, (cpu_clock_output, cpu_usage_output, ram_usage_output))
    connection.commit()

    print("Data inserted successfully: CPU Clock =", cpu_clock_output, 
          "CPU Usage =", cpu_usage_output, "RAM Usage =", ram_usage_output)

    
    
def fetch_latest_data():
    """Fetches the latest CPU clock, usage, and RAM usage data from the database."""
    my_cursor.execute("SELECT cpu_clock, cpu_usage, ram_usage, timestamp FROM SystemStats ORDER BY timestamp DESC LIMIT 1")
    row = my_cursor.fetchone()
   
    if row:
        # Extract numeric values and convert CPU clock from MHz to GHz
        cpu_clock_value = float(''.join(filter(str.isdigit, row[0]))) / 1000  # Convert MHz to GHz
        cpu_usage_value = float(row[1].strip().split()[0]) 
        ram_usage_str = row[2].strip()  
        if ram_usage_str and any(char.isdigit() for char in ram_usage_str):
            ram_usage_value = float(ram_usage_str)  
        timestamp = row[3]  
        return cpu_clock_value, cpu_usage_value, ram_usage_value, timestamp

    return None, None, None, None


def fetch_cpu_info():
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", cpu_info_script],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def show_cpu_info():
    cpu_info = fetch_cpu_info()

    info_window = Toplevel()
    info_window.title("CPU Information")
    info_window.geometry("400x300")

    text_widget = Text(info_window, wrap=WORD)
    text_widget.insert(1.0, cpu_info)
    text_widget.pack(expand=True, fill=BOTH)


def start_graph(selected_option):
    if selected_option == "CPU Information":
        show_cpu_info()  
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.style.use('ggplot')

    cpu_clocks = []
    cpu_usages = []
    ram_usages = []
    timestamps = []

    
    def update(frame):
       
        insert_data()

        
        cpu_clock, cpu_usage, ram_usage, timestamp = fetch_latest_data()

        if cpu_clock is not None:
            
            cpu_clocks.append(cpu_clock)
            cpu_usages.append(cpu_usage)
            ram_usages.append(ram_usage)
            timestamps.append(timestamp)

            
            ax.clear()

            if selected_option == "CPU Clock Speed":
                
                ax.plot(timestamps, cpu_clocks, label="CPU Clock (GHz)", color='b', marker='o')
                ax.set_title("Real-Time CPU Clock Speed")
                ax.set_ylabel("CPU Clock (GHz)")

            elif selected_option == "CPU Utilization":
                
                ax.plot(timestamps, cpu_usages, label="CPU Usage (%)", color='r', marker='x')
                ax.set_title("Real-Time CPU Utilization")
                ax.set_ylabel("CPU Usage (%)")

            elif selected_option == "RAM Usage":
                ax.plot(timestamps, ram_usages, label="RAM Usage (%)", color='g', marker='o')
                ax.set_title("Real-Time RAM Usage")
                ax.set_ylabel("RAM Usage (%)")
                ax.set_ylim(0, 100)  

           
            ax.set_xlabel("Timestamp")
            ax.legend(loc='upper left')
            plt.xticks(rotation=45, ha='right')  
            plt.tight_layout()

        else:
            print("No valid data to plot.")

   
    delete_old_data()

    # Set up the animation function, updating every 1000 milliseconds (1 second)
    ani = FuncAnimation(fig, update, interval=1000)

    
    plt.show()


def welcome_page():
    welcome_window = Tk()
    welcome_window.title("Welcome")
    welcome_window.geometry("600x300")

    welcome_label = Label(welcome_window, text="Welcome to the CPU and RAM Monitor Application", font=('Helvetica', 14, 'bold'))
    welcome_label.pack(pady=20)

    proceed_button = Button(welcome_window, text="Proceed", font=('Helvetica', 12), command=lambda: [welcome_window.destroy(), open_main_window()])
    proceed_button.pack(pady=20)

    welcome_window.mainloop()


def open_main_window():
    root = Tk()
    root.title("CPU and RAM Monitor")
    root.geometry("400x300")
    
    
    label = Label(root, text="Select an option to monitor:")
    label.pack(pady=10)

   
    global dropdown_var
    dropdown_var = StringVar()
    dropdown = ttk.Combobox(root, textvariable=dropdown_var)
    dropdown['values'] = ("CPU Clock Speed", "CPU Utilization", "RAM Usage", "Check Average (CPU, RAM)","CPU Information")
    dropdown['state'] = 'readonly'  
    dropdown.pack(pady=20)

    
    dropdown.bind("<<ComboboxSelected>>", on_select)

    root.mainloop()

welcome_page()

connection.close()