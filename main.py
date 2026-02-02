#!/usr/bin/env python3
import os
import sys
import time
import threading
import performance
import folder_monitor

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def run_integrated():
    clear_screen()
    print("="*40)
    print(" INTEGRATED MONITORING MODE ACTIVE")
    print("="*40)
    print("[*] Monitoring performance & files...")
    print("[*] Press Ctrl+C to stop\n")
    
    stop_event = threading.Event()

    def perf_loop():
        while not stop_event.is_set():
            metrics = performance.get_system_metrics()
            performance.log_metrics(metrics)
            time.sleep(5)

    def dir_loop():
    
        folder_monitor.start_monitoring(".")

    p_thread = threading.Thread(target=perf_loop, daemon=True)
    d_thread = threading.Thread(target=dir_loop, daemon=True)
    
    p_thread.start()
    d_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n[!] Shutting down...")

def main_menu():
    while True:
        clear_screen()
        print("1. Performance Only\n2. Directory Only\n3. Integrated Mode\n4. Exit")
        choice = input("\nSelect: ")
        if choice == '1': performance.check_system(); input("Enter to return...")
        elif choice == '2': folder_monitor.start_monitoring(".")
        elif choice == '3': run_integrated()
        elif choice == '4': break

if __name__ == "__main__":
    main_menu()
