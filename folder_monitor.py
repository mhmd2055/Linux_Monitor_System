#!/usr/bin/env python3
"""
Directory Monitoring Module
Student: [Your Name]
Module: Linux File System Analysis + Directory Monitoring
"""

import os
import time
import pwd
import grp
from datetime import datetime


def get_file_metadata(file_path):
    """
    Extract metadata from file using os.stat, pwd, grp
    """
    try:
        stat_info = os.stat(file_path)
        
        # Determine file type
        if os.path.isdir(file_path):
            file_type = 'directory'
        elif os.path.islink(file_path):
            file_type = 'symbolic link'
        else:
            file_type = 'regular file'
        
        metadata = {
            'name': os.path.basename(file_path),
            'type': file_type,
            'size': stat_info.st_size,  # bytes
            'owner': pwd.getpwuid(stat_info.st_uid).pw_name,
            'group': grp.getgrgid(stat_info.st_gid).gr_name,
            'permissions': oct(stat_info.st_mode)[-3:],
            'access_time': datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'modify_time': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'create_time': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modify_timestamp': stat_info.st_mtime  # for comparison
        }
        
        return metadata
        
    except Exception as e:
        return {'name': os.path.basename(file_path), 'error': str(e)}


def log_event(event_type, data):
    """
    Log directory events to file
    """
    os.makedirs('reports', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open('reports/directory_log.txt', 'a') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Event: {event_type}\n")
        f.write(f"Time: {timestamp}\n")
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key != 'modify_timestamp':
                    f.write(f"{key.capitalize()}: {value}\n")
        else:
            f.write(f"Details: {data}\n")


def start_monitoring(folder_path="."):
    """
    Monitor folder for changes (Creation, Deletion, Modification)
    """
    print(f"[*] Monitoring folder: {os.path.abspath(folder_path)}")
    print("[*] Press Ctrl+C to stop\n")
    
    os.makedirs('reports', exist_ok=True)
    
    # Database of tracked files
    files_db = {}
    
    # Read existing files
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        files_db[item] = get_file_metadata(full_path)
    
    print(f"[+] Tracking {len(files_db)} items initially")
    
    # Monitoring loop
    try:
        while True:
            time.sleep(5)
            
            current_files = set(os.listdir(folder_path))
            tracked_files = set(files_db.keys())
            
            # File Creation
            added = current_files - tracked_files
            for item in added:
                full_path = os.path.join(folder_path, item)
                metadata = get_file_metadata(full_path)
                files_db[item] = metadata
                
                print(f"[+] CREATED: {item}")
                print(f"    Type: {metadata['type']}, Size: {metadata['size']} bytes")
                print(f"    Owner: {metadata['owner']}, Group: {metadata['group']}")
                log_event('FILE CREATION', metadata)
            
            # File Deletion
            removed = tracked_files - current_files
            for item in removed:
                print(f"[-] DELETED: {item}")
                log_event('FILE DELETION', {
                    'filename': item,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                del files_db[item]
            
            # File Modification
            for item in current_files & tracked_files:
                full_path = os.path.join(folder_path, item)
                current_meta = get_file_metadata(full_path)
                
                if item in files_db:
                    old_meta = files_db[item]
                    
                    size_changed = current_meta.get('size') != old_meta.get('size')
                    time_changed = current_meta.get('modify_timestamp') != old_meta.get('modify_timestamp')
                    
                    if size_changed or time_changed:
                        print(f"[*] MODIFIED: {item}")
                        
                        if size_changed:
                            print(f"    Size: {old_meta['size']} -> {current_meta['size']} bytes")
                        
                        modification_data = {
                            'filename': item,
                            'old_size': old_meta.get('size'),
                            'new_size': current_meta.get('size'),
                            'old_permissions': old_meta.get('permissions'),
                            'new_permissions': current_meta.get('permissions'),
                            'old_modify_time': old_meta.get('modify_time'),
                            'new_modify_time': current_meta.get('modify_time'),
                            'owner': current_meta.get('owner'),
                            'group': current_meta.get('group')
                        }
                        
                        log_event('FILE MODIFICATION', modification_data)
                        files_db[item] = current_meta
            
    except KeyboardInterrupt:
        print("\n[*] Stopping folder monitor...")
        print(f"[+] Events saved to reports/directory_log.txt")
        print(f"[+] Total tracked items: {len(files_db)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        start_monitoring(sys.argv[1])
    else:
        start_monitoring(".")
