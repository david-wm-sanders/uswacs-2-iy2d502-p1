import subprocess
from pathlib import Path

print(f"Making report...")
commands = [["pdflatex.exe", "-shell-escape", "report.tex"],
            ["bibtex.exe", "report.aux"],
            ["pdflatex.exe", "-shell-escape", "report.tex"],
            ["pdflatex.exe", "-shell-escape", "report.tex"]]
for command in commands:
    subprocess.run(command)
