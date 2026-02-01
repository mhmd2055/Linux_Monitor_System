import matplotlib.pyplot as plt
import os

def generate_charts():
    log_file = "reports/system_log.txt"
    if not os.path.exists(log_file):
        print(f"[!] Log file not found.")
        return

    times, cpu, ram = [], [], []
    with open(log_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            try:
                # Splitting by comma and cleaning spaces
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 3:
                    # Flexible time extraction
                    full_time = parts[0].split()[-1]
                    short_time = full_time.split(".")[0]
                    
                    times.append(short_time)
                    cpu.append(float(parts[1]))
                    ram.append(float(parts[2]))
            except:
                continue

    if len(times) < 1:
        print("[!] No valid data found in log file.")
        return

    # If only 1 point exists, duplicate it to show a dot on the chart
    if len(times) == 1:
        times.append(times[0])
        cpu.append(cpu[0])
        ram.append(ram[0])

    plt.figure(figsize=(10, 5))
    plt.plot(times[-10:], cpu[-10:], label='CPU %', color='red', marker='o', linewidth=2)
    plt.plot(times[-10:], ram[-10:], label='RAM %', color='blue', marker='s', linewidth=2)
    
    plt.title('System Performance Monitor')
    plt.xlabel('Time')
    plt.ylabel('Usage %')
    plt.legend()
    plt.grid(True, linestyle='--')
    
    plt.savefig('reports/performance_chart.png')
    print("\n[SUCCESS] Chart generated and saved in 'reports' folder.")
    
    try:
        plt.show()
    except:
        print("[!] GUI display error. You can find the image in 'reports/performance_chart.png'")
