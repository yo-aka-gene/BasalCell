import json
import subprocess
import sys
import os

def main():
    lockfile = "renv.lock"
    if not os.path.exists(lockfile):
        print("ERROR: renv.lock not found. Please run environment initialization first.")
        sys.exit(1)

    print("Analyzing renv.lock for Mamba restoration...")
    with open(lockfile, "r") as f:
        lock_data = json.load(f)

    packages = lock_data.get("Packages", {})
    mamba_targets = []
    renv_fallbacks = []

    for pkg_name, pkg_info in packages.items():
        source = pkg_info.get('Source', '')
        version = pkg_info.get('Version', '')


        if source == 'Bioconductor':
            conda_name = f"bioconductor-{pkg_name.lower()}"
        elif source in ['Repository', 'CRAN']:
            conda_name = f"r-{pkg_name.lower()}"
        else:
            renv_fallbacks.append(pkg_name)
            continue

        conda_spec = f"{conda_name}={version}"
    
        result = subprocess.run(
            ['mamba', 'search', conda_spec],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        if result.returncode == 0:
            mamba_targets.append(conda_spec)
        else:
            print(f"{conda_spec} not found in Conda. Assigning to renv...")
            renv_fallbacks.append(pkg_name)

    if mamba_targets:
        print(f"Installing {len(mamba_targets)} packages via Mamba...")
        try:
            subprocess.run(['mamba', 'install', '-y'] + mamba_targets, check=True)
        except subprocess.CalledProcessError:
            print("ERROR: Mamba installation failed. Check your network or environment.")
            sys.exit(1)
    else:
        print("No exact matches found in Mamba.")

    print(f"Running renv::restore() for the final sync ({len(renv_fallbacks)} packages left to renv)...")
    
    conda_lib = os.path.join(os.environ.get('CONDA_PREFIX', ''), 'lib', 'R', 'library')
    r_cmd = f".libPaths('{conda_lib}'); Sys.setenv(RENV_CONFIG_SANDBOX_ENABLED='false'); renv::restore(prompt=FALSE)"
    
    try:
        subprocess.run(['Rscript', '--vanilla', '-e', r_cmd], check=True)
    except subprocess.CalledProcessError:
        print("ERROR: renv::restore() failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
