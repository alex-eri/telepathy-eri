SUBDIRS = client server

# telepathy.* modules containing files written by hand.
telepathydir = $(pythondir)/telepathy
telepathy_PYTHON = \
	constants.py \
	errors.py \
	__init__.py \
	interfaces.py \
	utils.py

# telepathy._generated.* auto-generated modules
spec_dir = $(top_srcdir)/spec
spec_files := $(patsubst $(spec_dir)%.xml,_generated%.py,$(wildcard $(spec_dir)/*.xml))

# We leave _generated/errors.py out of here because there exists a
# spec/errors.xml file, so that means there'll be a
# _generated/errors.py in $(spec_files). See fd.o#32526
BUILT_SOURCES = \
	_generated/interfaces.py \
	_generated/constants.py \
	_generated/__init__.py \
	$(spec_files)

generateddir = $(telepathydir)/_generated
nodist_generated_PYTHON = $(BUILT_SOURCES)

# telepathy._version generated module
versiondir = $(telepathydir)
nodist_version_PYTHON = _version.py

CLEANFILES = \
	_version.py \
	$(BUILT_SOURCES)

EXTRA_DIST = _version.py.in

distclean-local:
	rm -rf *.pyc *.pyo _generated

XSLTPROC_OPTS = --nonet --novalid --xinclude
tools_dir = $(top_srcdir)/tools

_generated/interfaces.py: $(tools_dir)/python-interfaces-generator.xsl $(wildcard $(spec_dir)/*.xml)
	$(AM_V_GEN)$(XSLTPROC) $(XSLTPROC_OPTS) -o $@ \
	    $(tools_dir)/python-interfaces-generator.xsl \
	    $(spec_dir)/all.xml

_generated/constants.py: $(tools_dir)/python-constants-generator.xsl $(wildcard $(spec_dir)/*.xml)
	$(AM_V_GEN)$(XSLTPROC) $(XSLTPROC_OPTS) -o $@ \
	    $(tools_dir)/python-constants-generator.xsl \
	    $(spec_dir)/all.xml

_generated/errors.py: $(tools_dir)/python-errors-generator.xsl $(wildcard $(spec_dir)/*.xml)
	$(AM_V_GEN)$(XSLTPROC) $(XSLTPROC_OPTS) -o $@ \
	    $(tools_dir)/python-errors-generator.xsl \
	    $(spec_dir)/all.xml

_generated/__init__.py:
	$(AM_V_GEN)$(mkdir_p) $(dir $@)
	@echo "# Placeholder for package" > $@

_generated/%.py: $(tools_dir)/spec-to-python.xsl $(spec_dir)/%.xml
	$(AM_V_GEN)$(XSLTPROC) $(XSLTPROC_OPTS) -o $@ \
	    $(tools_dir)/spec-to-python.xsl \
	    $(spec_dir)/$*.xml
