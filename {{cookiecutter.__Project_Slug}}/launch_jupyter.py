import os
import subprocess
import sys
import webbrowser

def start_jupyter():
    print("Initiating Jupyter Lab")

    process = subprocess.Popen(
        [
            "jupyter", "lab", 
            "--no-browser", 
            "--port=8888", 
            "--ip=0.0.0.0",
            "--IdentityProvider.token={{ cookiecutter.__project_slug }}",
            "--ServerApp.token={{ cookiecutter.__project_slug }}"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    browser_opened = False

    try:
        for line in process.stdout:
            sys.stdout.write(line)

            if "http://127.0.0.1" in line and "/lab" in line:
                url = line.strip().split(" ")[-1]

                if "token=" not in url:
                    url = f"{url}?token={{ cookiecutter.__project_slug }}"

                print("\n" + "=" * 70)
                print("Jupyter Lab is available at:")
                print(f"\033[1;36m{url}\033[0m")
                print("=" * 70 + "\n")

                if not browser_opened:
                    print("Connecting to Jupyter Lab via default browser...")
                    try:
                        is_wsl = os.path.exists("/proc/version") and "microsoft" in open("/proc/version").read().lower()
                        
                        if is_wsl:
                            subprocess.run(["powershell.exe", "-Command", f"Start-Process '{url}'"], check=False)
                        else:
                            webbrowser.open(url)
                    except Exception:
                        print("Failed to open browser automatically. Please open the URL above manually")
                        print(f"\n    \033[1;36m{url}\033[0m\n") 

                    browser_opened = True

    except KeyboardInterrupt:
        print("Terminating Jupyter Lab")
        process.terminate()
        process.wait()
        print("Jupyter Lab has terminated")

if __name__ == "__main__":
    start_jupyter()
