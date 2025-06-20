# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Install dependencies for building the docs
install:
	pip install -r requirements.txt

# Build HTML and open in default browser
html-view: html
	start "" _build/html/index.html

# Clean build directory
clean:
	rm -rf $(BUILDDIR)/*

# Build and serve documentation with live reload
autobuild:
	sphinx-autobuild -b html $(SOURCEDIR) $(BUILDDIR)/html --port 8000 --watch ..

# Build all documentation formats
all: clean html latexpdf epub

# Build PDF documentation
pdf: latexpdf

# Build EPUB documentation
epub:
	$(SPHINXBUILD) -b epub $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/epub

# Build single HTML file
singlehtml:
	$(SPHINXBUILD) -b singlehtml $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/singlehtml
