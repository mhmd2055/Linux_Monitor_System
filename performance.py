import psutil

def get_stats():
   
    stats = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent
    }
    return stats

if __name__ == "__main__":
    data = get_stats()
    print(f"CPU Usage: {data['cpu']}% | Memory Usage: {data['memory']}%")
