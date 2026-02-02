#!/usr/bin/env python3
# Modified by Haleem: Added directory monitoring logic and documentation.
import os
import time
import pwd
import grp
from datetime import datetime

def get_file_metadata(file_path):
    try:
        stat_info = os.stat(file_path)
        if os.path.isdir(file_path):
            file_type = 'directory'
        elif os.path.islink(file_path):
            file_type = 'symbolic link'
        else:
            file_type = 'regular file'
        
        return {
            'name': os.path.basename(file_path),
            'type': file_type,
            'size': stat_info.st_size,
            'owner': pwd.getpwuid(stat_info.st_uid).pw_name,
            'group': grp.getgrgid(stat_info.st_gid).gr_name,
            'permissions': oct(stat_info.st_mode)[-3:],
            'modify_time': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'modify_timestamp': stat_info.st_mtime
        }
    except:
        return None

def log_event(event_type, data):
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('reports/directory_log.txt', 'a') as f:
        f.write(f"\n[{timestamp}] {event_type}: {data}\n")

def start_monitoring(folder_path="."):
    print(f"[*] Monitoring: {os.path.abspath(folder_path)}")
    files_db = {item: get_file_metadata(os.path.join(folder_path, item)) 
                for item in os.listdir(folder_path)}
    try:
        while True:
            time.sleep(2)
            current_items = os.listdir(folder_path)
            
            # Check added
            for item in set(current_items) - set(files_db.keys()):
                meta = get_file_metadata(os.path.join(folder_path, item))
                files_db[item] = meta
                print(f"[+] ADDED: {item}")
                log_event('ADDED', meta)

            # Check removed
            for item in set(files_db.keys()) - set(current_items):
                print(f"[-] REMOVED: {item}")
                log_event('REMOVED', item)
                del files_db[item]
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    start_monitoring(".")
