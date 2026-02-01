

import psutil
import time
import os
from datetime import datetime


def get_system_metrics():
    """

    """
    metrics = {}
    
    # ===== CPU Metrics =====
    cpu_percent = psutil.cpu_percent(interval=1)
    load_avg = os.getloadavg()  # (1min, 5min, 15min)
    
    # ===== Memory Metrics =====
    memory = psutil.virtual_memory()
    mem_total = memory.total / (1024**3)  # تحويل لـ GB
    mem_used = memory.used / (1024**3)
    mem_available = memory.available / (1024**3)
    mem_percent = memory.percent
    
    # ===== Disk Metrics (root partition) =====
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024**3)
    disk_used = disk.used / (1024**3)
    disk_free = disk.free / (1024**3)
    disk_percent = disk.percent
    
    # ===== System Uptime =====
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_hours = uptime_seconds / 3600
    
    # ===== Process Information =====

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    #  Running vs Sleeping
    running_count = 0
    sleeping_count = 0
    for p in processes:
        if p.info['status'] == 'running':
            running_count += 1
        elif p.info['status'] == 'sleeping':
            sleeping_count += 1
    
    total_processes = len(processes)
    
    # Top 3 by CPU 
    top_cpu = sorted(processes, key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:3]
    
    # Top 3 by Memory
    top_mem = sorted(processes, key=lambda x: x.info['memory_percent'] or 0, reverse=True)[:3]
    
    #   dictionary
    metrics = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_percent': cpu_percent,
        'load_avg_1min': load_avg[0],
        'load_avg_5min': load_avg[1],
        'load_avg_15min': load_avg[2],
        'mem_total_gb': mem_total,
        'mem_used_gb': mem_used,
        'mem_available_gb': mem_available,
        'mem_percent': mem_percent,
        'disk_total_gb': disk_total,
        'disk_used_gb': disk_used,
        'disk_free_gb': disk_free,
        'disk_percent': disk_percent,
        'uptime_hours': uptime_hours,
        'total_processes': total_processes,
        'running_processes': running_count,
        'sleeping_processes': sleeping_count,
        'top_cpu': top_cpu,
        'top_mem': top_mem
    }
    
    return metrics


def display_usage():
    """

    """
    print("-" * 60)
    print("--- System Performance ---")
    
    metrics = get_system_metrics()
    

    print(f"Timestamp: {metrics['timestamp']}")
    print(f"\nCPU Usage: {metrics['cpu_percent']}%")
    print(f"Load Average: {metrics['load_avg_1min']:.2f}, {metrics['load_avg_5min']:.2f}, {metrics['load_avg_15min']:.2f}")
    
    print(f"\nMemory:")
    print(f"  Total: {metrics['mem_total_gb']:.2f} GB")
    print(f"  Used: {metrics['mem_used_gb']:.2f} GB")
    print(f"  Available: {metrics['mem_available_gb']:.2f} GB")
    print(f"  Usage: {metrics['mem_percent']}%")
    
    print(f"\nDisk (/):")
    print(f"  Total: {metrics['disk_total_gb']:.2f} GB")
    print(f"  Used: {metrics['disk_used_gb']:.2f} GB")
    print(f"  Free: {metrics['disk_free_gb']:.2f} GB")
    print(f"  Usage: {metrics['disk_percent']}%")
    
    print(f"\nUptime: {metrics['uptime_hours']:.2f} hours")
    
    print(f"\nProcesses:")
    print(f"  Total: {metrics['total_processes']}")
    print(f"  Running: {metrics['running_processes']}")
    print(f"  Sleeping: {metrics['sleeping_processes']}")
    

    print(f"\nTop 3 by CPU:")
    for p in metrics['top_cpu']:
        name = p.info['name']
        cpu = p.info['cpu_percent']
        print(f"  {name}: {cpu}%")
    
    # Top 3 by Memory
    print(f"\nTop 3 by Memory:")
    for p in metrics['top_mem']:
        name = p.info['name']
        mem = p.info['memory_percent']
        print(f"  {name}: {mem:.1f}%")
    
    print("-" * 60)
    return metrics


def log_metrics(metrics):
    """

    """

    if not os.path.exists('reports'):
        os.makedirs('reports')
    


    with open('reports/system_log.txt', 'a') as f:

        line = f"{metrics['timestamp']}, {metrics['cpu_percent']}, {metrics['mem_percent']}\n"
        f.write(line)
    

    with open('reports/detailed_log.txt', 'a') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Time: {metrics['timestamp']}\n")
        f.write(f"CPU: {metrics['cpu_percent']}% (Load: {metrics['load_avg_1min']:.2f}, {metrics['load_avg_5min']:.2f}, {metrics['load_avg_15min']:.2f})\n")
        f.write(f"Memory: {metrics['mem_used_gb']:.2f}/{metrics['mem_total_gb']:.2f} GB ({metrics['mem_percent']}%)\n")
        f.write(f"Disk: {metrics['disk_used_gb']:.2f}/{metrics['disk_total_gb']:.2f} GB ({metrics['disk_percent']}%)\n")
        f.write(f"Uptime: {metrics['uptime_hours']:.2f} hours\n")
        f.write(f"Processes: {metrics['running_processes']} running, {metrics['sleeping_processes']} sleeping\n")


def check_system():
    """

    """
    metrics = display_usage()
    log_metrics(metrics)
    return metrics


# ===== الـ Main =====
if __name__ == "__main__":

    try:
        while True:
            check_system()
            time.sleep(10)  
    except KeyboardInterrupt:

        print("\n[*] Stopping performance monitor...")
