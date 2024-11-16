import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))
# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'recruit_me'
copyright = '2024, Arnaud SOMVILLE'
author = 'Arnaud SOMVILLE'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'page_width': 'auto',
    'sidebar_width': '220px',
    'fixed_sidebar': True,
    'show_related': True,  # Ajoute des liens vers les pages connexes.
}