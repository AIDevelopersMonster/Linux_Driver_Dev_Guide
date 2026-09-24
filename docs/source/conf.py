# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Project information -----------------------------------------------------
project = 'Linux Driver Development Guide for Raspberry Pi 3'
copyright = '2025, Alex Malachevsky'
author = 'Alex Malachevsky'
release = '2025.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

# -- Internationalization ----------------------------------------------------
language = 'ru'

# -- Options for LaTeX output (PDF) ------------------------------------------

latex_engine = 'xelatex'

latex_elements = {
    'preamble': r'''
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\newfontfamily\cyrillicfont{DejaVu Serif}
\newfontfamily\cyrillicfonttt{DejaVu Sans Mono}
    ''',
    'latex_engine': 'xelatex',
}

latex_documents = [
    ('index', 'LinuxDriverGuide.tex', 'Linux Driver Development Guide for Raspberry Pi 3',
     'Alex Malachevsky', 'manual'),
]



