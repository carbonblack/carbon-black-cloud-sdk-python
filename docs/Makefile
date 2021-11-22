# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
SOURCEDIR     = .
APP 		  = /docs

# Put it first so that "make" without argument is like "make help".
.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Create a live server which will host the documentation with live-reloading.
.PHONY: livehtml
livehtml:
	sphinx-autobuild -b html --host 0.0.0.0 --port 7000 --watch $(APP) -c . $(SOURCEDIR) $(BUILDDIR)/html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
