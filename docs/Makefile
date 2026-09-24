# Makefile for building the Sphinx documentation

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help clean html pdf

help:
	@echo "Sphinx documentation build commands:"
	@echo "  make html     - Build HTML documentation"
	@echo "  make pdf      - Build PDF documentation (via LaTeX)"
	@echo "  make clean    - Clean all build files"

html:
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html
	@echo "HTML docs built in $(BUILDDIR)/html"

pdf:
	$(SPHINXBUILD) -b latex $(SOURCEDIR) $(BUILDDIR)/latex
	make -C $(BUILDDIR)/latex all-pdf
	@echo "PDF docs built in $(BUILDDIR)/latex"

clean:
