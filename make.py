import subprocess
from pathlib import Path

# TODO: Add this?
# .\venv\Scripts\python.exe .\make_full_code_listings.py ..\uswacs-2-iy2d502-salapp\ --not-files=.env,sec_requirements.txt --not-dirs=migrations

print(f"Making report...")
commands = [["xelatex.exe", "-shell-escape", "report.tex"],
            ["bibtex.exe", "report.aux"],
            ["xelatex.exe", "-shell-escape", "report.tex"],
            ["xelatex.exe", "-shell-escape", "report.tex"]]
for command in commands:
    subprocess.run(command)
