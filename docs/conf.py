"""Sphinx configuration file"""
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Carbon Black Cloud Python SDK'
copyright = '2020-2023 VMware Carbon Black'
author = 'Developer Relations'

# The full version, including alpha/beta/rc tags
release = '1.4.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.napoleon', 'sphinx.ext.autodoc', 'sphinx.ext.autosectionlabel', 'sphinx_copybutton']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'tango'

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# Generate unique labels
autosectionlabel_prefix_document = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    'style_external_links': True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/cbc-sdk-thumbnail.png"

# Output file base name for HTML help builder.
htmlhelp_basename = 'CarbonBlackAPI-PythonBindingsdoc'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'CarbonBlackCloud-PythonBindings.tex', u'Carbon Black Cloud Python API Documentation',
     u'Carbon Black Developer Network', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'carbonblackcloud-pythonbindings', u'Carbon Black Cloud Python API Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'CarbonBlackCloud-PythonBindings', u'Carbon Black Cloud Python API Documentation',
     author, 'CarbonBlackCloud-PythonBindings', 'Python bindings for the Carbon Black Cloud API',
     'Miscellaneous'),
]

latex_elements = {
    # Additional stuff for the LaTeX preamble.
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',

    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
    'preamble': "".join((
        '\\DeclareUnicodeCharacter{25A0}{=}',  # Solid box
    )),
}

autoclass_content = 'both'

# options for sphinx generation.
# use a regular expression to strip standard prompt and continuation when copying an example
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
copybutton_prompt_text = r">>> |\.\.\. "


def setup(app):
    """Setup Sphinx."""
    app.add_css_file('css/custom.css')
