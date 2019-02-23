#!venv/bin/python3
"""Generates LaTeX minted code listings from a root folder.

Usage:
    make_full_code_listings.py <root_dir> [--exclude-dirs=<dirs>]
"""
import itertools
import sys
from pathlib import Path

from docopt import docopt


exclude_dirs = [".git", "venv", "__pycache__"]
exclude_exts = [".db", ".exe", ".pdf", ".png", ".jpeg"]
output_dir = Path(__file__).parent / "sections/_code_listings/"
ext_lint_map = {".py": "python3",
                ".html": "html+jinja",
                ".sh": "bash"}


def recursively_find_dirs(root_dir):
    dirs = [root_dir]
    for d in root_dir.iterdir():
        if d.is_dir() and d.name not in exclude_dirs:
            sub_dirs = recursively_find_dirs(d)
            dirs.extend(sub_dirs)
    return dirs


def patch_string_for_latex(s):
    s = s.replace("_", "\\_")
    return s


if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)

    # Make the output_dir, creating parents as necessary
    output_dir.mkdir(parents=True, exist_ok=True)

    # Make root_dir a Path object and check it exists (exiting if not existing)
    root_dir = Path(args["<root_dir>"])
    if not root_dir.exists():
        print("Can't find project root at '{root_dir}'... exiting.")
        sys.exit(1)

    # Process extra excluded dirs
    if args["--exclude-dirs"]:
        exclude_dirs.extend(args["--exclude-dirs"].split(","))
    print(f"Excluding: {exclude_dirs}")

    # Find all dirs, including and relative to root_dir, that are not excluded
    dirs = recursively_find_dirs(root_dir)
    print(f"Found: {dirs}")

    # Create the output .tex file
    tf_p = output_dir / f"{root_dir.name}.tex"
    with tf_p.open(mode="w", encoding="utf-8") as tf:
        # Write the initial section header
        rdn = patch_string_for_latex(root_dir.name)
        tf.write(f"\\section{{Full Code Listings: \\texttt{{{rdn}}}}}\n")

        # For each directory, not excluded, find all files
        for d in dirs:
            print(f"Processing '{d}'...")
            files = (f for f in d.glob("*") if f.is_file() and f.suffix not in exclude_exts)
            # Sort better
            files = sorted(files, key=lambda p: p.name)
            for f in files:
                # Figure out the subsection title
                f_name_parts = list(itertools.dropwhile(lambda x: x != root_dir.name, f.parts))
                f_name = "/".join(f_name_parts[1::])
                f_name = patch_string_for_latex(f_name)
                # Write a subsection header for each file
                tf.write(f"\\subsection{{\\texttt{{{f_name}}}}}\n")
                # Begin a codelisting env
                tf.write("\\begin{codelisting}\n")
                # Begin a minted env
                lexer = ext_lint_map.get(f.suffix, "text")
                tf.write(f"\\begin{{minted}}[fontsize=\\small,breakanywhere]{{{lexer}}}\n")
                # Insert file contents
                tf.write(f.read_text(encoding="utf-8"))
                # tf.write("\n")
                # Close minted env
                tf.write("\\end{minted}\n")
                # Close codelisting env
                tf.write("\\end{codelisting}\n")
                # Insert pagebreak
                print(f"Minted '{f_name}' as '{lexer}'...")
