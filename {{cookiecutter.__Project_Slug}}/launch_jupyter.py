import os
import platform
{%- if cookiecutter.r_ver != "none" %}
from pathlib import Path
import textwrap
{%- endif %}
import subprocess
import sys
import webbrowser


def open_browser(url):
    is_wsl = "microsoft" in platform.uname().release.lower()
    
    if is_wsl:
        try:
            subprocess.run(["wslview", url], check=True)
        except FileNotFoundError:
            safe_url = url.replace("&", "^&")
            subprocess.run(["cmd.exe", "/c", "start", safe_url])
    else:
        webbrowser.open(url)

def start_jupyter():
    print("Initiating Jupyter Lab")

    process = subprocess.Popen(
        [
            "jupyter", "lab", 
            "--no-browser", 
            "--port=8888", 
            "--ip=0.0.0.0",
            "--allow-root",
            "--IdentityProvider.token={{ cookiecutter.__project_slug }}",
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

            if "http://127.0.0.1" in line and "/lab" in line and not browser_opened:
                url = line.strip().split(" ")[-1]

                if "token=" not in url:
                    url = f"{url}?token={{ cookiecutter.__project_slug }}"

                print("\n" + "=" * 70)
                print("Jupyter Lab is available at:")
                print(f"\033[1;36m{url}\033[0m")
                print("=" * 70 + "\n")

                print("Connecting to Jupyter Lab via default browser...")
                try:
                    open_browser(url)
                except Exception as e:
                    print("Failed to open browser automatically.")
                    print(f"Reason: {e}")
                    print("\nPlease open the URL below manually:")
                    print(f"\n    \033[1;36m{url}\033[0m\n") 

                browser_opened = True

    except KeyboardInterrupt:
        print("Terminating Jupyter Lab")
        process.terminate()
        process.wait()
        print("Jupyter Lab has terminated")

if __name__ == "__main__":
{%- if cookiecutter.r_ver != "none" %}
    project_root = Path(__file__).resolve().parent
    r_profile_proxy = project_root / ".Rprofile_proxy"
    r_profile_content = textwrap.dedent(f"""\
        old_wd <- getwd()
        setwd('{project_root.as_posix()}')
        source('renv/activate.R')
        setwd(old_wd)
    """)
    r_profile_proxy.write_text(r_profile_content)
    os.environ["R_PROFILE_USER"] = str(r_profile_proxy)
{%- endif %}
    start_jupyter()
