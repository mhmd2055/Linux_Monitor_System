import performance
import folder_monitor

def start_app():
    print("--- Linux System Monitor ---")
    print("1. Check CPU and RAM")
    print("2. Monitor Folder Changes")
    print("3. Exit")
    
    choice = input("Select an option: ")
    
    if choice == '1':
        performance.check_system()
    elif choice == '2':
        folder_monitor.start_monitoring(".")
    else:
        print("Closing...")

if __name__ == "__main__":
    start_app()
