import subprocess

with open('requirements.txt') as f:
    packages = f.readlines()

for package in packages:
    package = package.strip()
    if package:  # Skip empty lines
        subprocess.run(['pipx', 'install', package])
