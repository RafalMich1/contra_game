import pygame, sys



# ============================================================================ #
# LAUNCHER
# ============================================================================ #
import subprocess
def check_and_run_main():
    if "main" not in sys.modules:
        print("Main module not found, launching main.py...")
        
        print(f"\033[38;5;{196}m {'---------------------------------'} \033[0m")
        subprocess.run([sys.executable, "main.py"])
    else:
        print("Main module is already running.")
if __name__ == "__main__":
    check_and_run_main()