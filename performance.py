import psutil
import time



def display_usage():
    print("-" * 30)
    print("--- System Performance ---")
   
    cpu_usage = psutil.cpu_percent(interval=1)
    
    
    memory = psutil.virtual_memory()
    
    print(f"CPU Usage: {cpu_usage}%")
    print(f"RAM Usage: {memory.percent}%")
    print(f"Available Memory: {memory.available / (1024**3):.2f} GB")
    print("-" * 30)

if __name__ == "__main__":
    try:
        while True:
            display_usage()
            time.sleep(5) 
    except KeyboardInterrupt:
        print("\n[*] Stopping performance monitor...")
