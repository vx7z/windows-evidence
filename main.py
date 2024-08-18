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

def main():
    if not check_skibidi_status():
        elevate_to_sigma()
        return

    opsec_cmds = [
        "cipher /w:C:",
        "ipconfig /flushdns",
        "wevtutil cl System",
        "RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 255",
        "fsutil usn deletejournal /d /n C:",
        "del /f /s /q %TEMP%\\*.*",
        "powercfg /hibernate off",
        "netsh interface ipv4",
        "del /q/f/s %systemroot%\\System32\\spool\\PRINTERS\\*",
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
        "del /q/f/s %SystemRoot%\\Prefetch\\*",
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f',
        "MRT"
    ]

    max_tries = 5
    wait_time = 10

    for cmd in opsec_cmds:
        for attempt in range(max_tries):
            if execute(cmd):
                break
            else:
                print(f"tryna do : {cmd} again in {wait_time} seconds (uhm idk try {attempt + 1}/{max_tries})")
                time.sleep(wait_time)
        
        time.sleep(random.uniform(1.5, 2.5))

    print("ur privacy is in my hands, so u will get what u asked for my love.")
    extra_sigma()

def extra_sigma():
    execute("cleanmgr /sagerun:1")
    execute("chkdsk /f /r")
    execute("wuauclt /detectnow")
    execute("wuauclt /updatenow")
    execute("defrag C: /O")

    print("Ur opsec has been enhanced my migger.")

if __name__ == "__main__":
    main()