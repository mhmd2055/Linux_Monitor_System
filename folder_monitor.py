import os
import time

def start_monitoring(folder_path):
    print("Monitoring folder:", folder_path)
    
    files_list = os.listdir(folder_path)
    
    try:
        while True:
            time.sleep(5)
            
            latest_files = os.listdir(folder_path)
            
            added = [item for item in latest_files if item not in files_list]
            removed = [item for item in files_list if item not in latest_files]
            
            if added:
                print("Added:", added)
            
            if removed:
                print("Removed:", removed)
                
            files_list = latest_files
            
    except KeyboardInterrupt:
        print("Done.")

if __name__ == "__main__":
    start_monitoring(".")
