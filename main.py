import os, subprocess, time, random, ctypes, sys, winreg
from datetime import datetime

def check_skibidi_status():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"lookin for uac status : {e}")
        return False

def elevate_to_sigma():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"cant get uac : {e}")
        sys.exit(1)

def execute(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\nError: {e.stderr}")
        return None

def execute_with_retry(cmd, max_tries=3, wait_time=5):
    for attempt in range(max_tries):
        if execute(cmd):
            print(f"Command succeeded: {cmd}")
            return True
        print(f"tryna do : {cmd} again in {wait_time} seconds (uhm idk try {attempt + 1}/{max_tries})")
        time.sleep(wait_time)
    print(f"Command failed after {max_tries} attempts: {cmd}")
    return False

def main():
    if not check_skibidi_status():
        elevate_to_sigma()
        return

    opsec_cmds = [
        "cipher /w:C: && ipconfig /flushdns && wevtutil cl System",
        "RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 255 && fsutil usn deletejournal /d /n C:",
        "del /f /s /q %TEMP%\\*.* && powercfg /hibernate off && netsh interface ipv4 set global multicastforwarding=disabled",
        "del /q/f/s %systemroot%\\System32\\spool\\PRINTERS\\* && reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\" /v AllowTelemetry /t REG_DWORD /d 0 /f",
        "del /q/f/s %SystemRoot%\\Prefetch\\* && reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Error Reporting\" /v Disabled /t REG_DWORD /d 1 /f && MRT"
    ]

    for cmd in opsec_cmds:
        execute_with_retry(cmd)
        time.sleep(random.uniform(0.5, 1.0))

    print("ur privacy is in my hands, so u will get what u asked for my love.")
    extra_sigma()

def extra_sigma():
    extra_cmds = [
        "cleanmgr /sagerun:1",
        "chkdsk /f /r",
        "wuauclt /detectnow",
        "wuauclt /updatenow",
        "defrag C: /O"
    ]

    for cmd in extra_cmds:
        execute_with_retry(cmd)
        time.sleep(random.uniform(0.5, 1.0))

    print("Ur opsec has been enhanced my migger.")

if __name__ == "__main__":
    main()
