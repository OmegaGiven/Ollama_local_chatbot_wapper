import subprocess

# Function to ensure required packages are installed
def install_requirements(required_packages = ["streamlit", "pymupdf", "gitingest"]):
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))  # Check if installed
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call(["pip", "install", package])
            # subprocess.check_call(["apt", "install", f"python3-{package}"])

install_requirements()