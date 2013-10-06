SHELL := /bin/bash

PREFIX ?= /usr
LIBEXECDIR ?= $(PREFIX)/libexec
DATADIR ?= $(PREFIX)/share
MODULESDIR ?= $(DATADIR)/telepathy-eri
DBUS_SERVICES_DIR ?= $(DATADIR)/dbus-1/services
MANAGERS_DIR ?= $(DATADIR)/telepathy/managers

INSTALL = install -D -p
RM = rm -r -f

BUILT_FILES_DATA = $(service_in_files:.service.in=.service)
service_in_files = data/org.freedesktop.Telepathy.ConnectionManager.eri.service.in
service_DATA = $(BUILT_FILES_DATA)

BUILT_FILES_EXEC = $(exec_in_files:.py.in=.py)
exec_in_files = telepathy-eri.py.in
exec_DATA = $(BUILT_FILES_EXEC)

manager_DATA = data/eri.manager

tp_DATA = tp/*.py
tp_vk_DATA = tp/vk/*.py
tp_channel_DATA = tp/channel/*.py

vk_DATA = vkcom/*.py

tp_py = telepathy-python
tlp_DATA = $(tp_py)/src/*.py
tlp_server_DATA = $(tp_py)/src/server/*.py
tlp_client_DATA = $(tp_py)/src/client/*.py
tlp_gen_DATA = $(tp_py)/src/_generated/*.py

utils_DATA = utils/*.py

all: submodule $(exec_DATA) $(service_DATA)

submodule:
	@git submodule update --init
	@bash -c " \
            pushd telepathy-python/; \
            git am ../0001-fix-pending-messages.patch; \
            make distclean; \
            ./autogen.sh; \
            make; \
            popd"

$(exec_DATA): $(exec_in_files)
	@sed -e "s|\@MODULESDIR\@|$(MODULESDIR)|" $< > $@

$(service_DATA): $(service_in_files)
	@sed -e "s|\@LIBEXECDIR\@|$(LIBEXECDIR)|" $< > $@

install:
	$(INSTALL)    -m755 $(exec_DATA)       $(DESTDIR)$(LIBEXECDIR)/telepathy-eri
	$(INSTALL)    -m644 $(service_DATA)    $(DESTDIR)$(DBUS_SERVICES_DIR)/org.freedesktop.Telepathy.ConnectionManager.eri.service
	$(INSTALL)    -m644 $(manager_DATA)    $(DESTDIR)$(MANAGERS_DIR)/eri.manager
# installing req
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/tp/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/tp/vk/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/tp/channel/
	$(INSTALL)    -m644 $(tp_DATA)         $(DESTDIR)$(MODULESDIR)/tp/
	$(INSTALL)    -m644 $(tp_vk_DATA)      $(DESTDIR)$(MODULESDIR)/tp/vk/
	$(INSTALL)    -m644 $(tp_channel_DATA) $(DESTDIR)$(MODULESDIR)/tp/channel/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/vkcom/
	$(INSTALL)    -m644 $(vk_DATA)         $(DESTDIR)$(MODULESDIR)/vkcom/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/telepathy/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/telepathy/server/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/telepathy/client/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/telepathy/_generated/
	$(INSTALL)    -m644 $(tlp_DATA)        $(DESTDIR)$(MODULESDIR)/telepathy/
	$(INSTALL)    -m644 $(tlp_server_DATA) $(DESTDIR)$(MODULESDIR)/telepathy/server/
	$(INSTALL)    -m644 $(tlp_client_DATA) $(DESTDIR)$(MODULESDIR)/telepathy/client/
	$(INSTALL)    -m644 $(tlp_gen_DATA)    $(DESTDIR)$(MODULESDIR)/telepathy/_generated/
	$(INSTALL) -d -m755                    $(DESTDIR)$(MODULESDIR)/utils/
	$(INSTALL)    -m644 $(utils_DATA)      $(DESTDIR)$(MODULESDIR)/utils/

clean:
	$(RM)               $(service_DATA)
	$(RM)               $(exec_DATA)
	@git submodule deinit -f .

uninstall:
	$(RM)               $(DESTDIR)$(LIBEXECDIR)/telepathy-eri
	$(RM)               $(DESTDIR)$(DBUS_SERVICES_DIR)/org.freedesktop.Telepathy.ConnectionManager.eri.service
	$(RM)               $(DESTDIR)$(MANAGERS_DIR)/eri.manager
	$(RM)               $(DESTDIR)$(MODULESDIR)/
