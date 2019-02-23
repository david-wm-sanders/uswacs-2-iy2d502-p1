#!venv/bin/python3
"""Generates LaTeX figure floats for screenshots."""
import itertools
import sys
from pathlib import Path


screenshot_path = Path(__file__).parent / "screenshots"
output_dir = Path(__file__).parent / "sections/_screenshots/"


if __name__ == '__main__':
    # Make the output_dir, creating parents as necessary
    output_dir.mkdir(parents=True, exist_ok=True)

    shots = screenshot_path.glob("*.png")

    tf_p = output_dir / "appendix.tex"
    with tf_p.open(mode="w", encoding="utf-8") as tf:
        # Write the section header
        tf.write("\\section{Evidential Screenshots}\n")
        for shot in shots:
            # Begin a figure
            tf.write("\\begin{figure}[h!]\n")
            # Configure figure
            tf.write("\\centering\n\\captionsetup{skip=\\skipfigurecaptionlen}\n")
            # Include graphic
            shot_p = str(shot)
            shot_p = shot_p.replace("\\", "/")
            tf.write(f"\\includegraphics[width=1\\textwidth]{{{shot_p}}}\n")
            # Add blank caption
            tf.write("\\caption{\\todo{blank: insert caption}}\n")
            # Add label
            label_id = f"fig:{shot.stem}"
            tf.write(f"\\label{{{label_id}}}\n")
            # End figure
            tf.write("\\end{figure}\n")
            # Insert pagebreak
            tf.write("\\pagebreak\n")
