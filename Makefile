SHELL := /bin/bash

prefix = /usr
LIBEXECDIR ?= $(prefix)/lib/telepathy-eri
DATADIR ?= $(prefix)/share/telepathy-eri

DBUS_SERVICES_DIR ?= $(prefix)/share/dbus-1/services
MANAGERS_DIR ?= $(prefix)/share/telepathy/managers

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
	@sed -e "s|\@DATADIR\@|$(DATADIR)|" $< > $@

$(service_DATA): $(service_in_files)
	@sed -e "s|\@LIBEXECDIR\@|$(LIBEXECDIR)|" $< > $@

install:
	$(INSTALL)    -m755 $(exec_DATA)       $(DESTDIR)$(LIBEXECDIR)/telepathy-eri
	$(INSTALL)    -m644 $(service_DATA)    $(DESTDIR)$(DBUS_SERVICES_DIR)/org.freedesktop.Telepathy.ConnectionManager.eri.service
	$(INSTALL)    -m644 $(manager_DATA)    $(DESTDIR)$(MANAGERS_DIR)/eri.manager
# installing req
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/tp/vk/
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/tp/channel/
	$(INSTALL)    -m644 $(tp_DATA)         $(DESTDIR)$(DATADIR)/tp/
	$(INSTALL)    -m644 $(tp_vk_DATA)      $(DESTDIR)$(DATADIR)/tp/vk/
	$(INSTALL)    -m644 $(tp_channel_DATA) $(DESTDIR)$(DATADIR)/tp/channel/
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/vkcom/
	$(INSTALL)    -m644 $(vk_DATA)         $(DESTDIR)$(DATADIR)/vkcom/
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/telepathy/server/
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/telepathy/client/
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/telepathy/_generated/
	$(INSTALL)    -m644 $(tlp_DATA)        $(DESTDIR)$(DATADIR)/telepathy/
	$(INSTALL)    -m644 $(tlp_server_DATA) $(DESTDIR)$(DATADIR)/telepathy/server/
	$(INSTALL)    -m644 $(tlp_client_DATA) $(DESTDIR)$(DATADIR)/telepathy/client/
	$(INSTALL)    -m644 $(tlp_gen_DATA)    $(DESTDIR)$(DATADIR)/telepathy/_generated/
	$(INSTALL) -d -m755                    $(DESTDIR)$(DATADIR)/utils/
	$(INSTALL)    -m644 $(utils_DATA)      $(DESTDIR)$(DATADIR)/utils/

clean:
	$(RM)               $(service_DATA)
	$(RM)               $(exec_DATA)
	@git submodule deinit -f .

uninstall:
	$(RM)               $(DESTDIR)$(LIBEXECDIR)/telepathy-eri
	$(RM)               $(DESTDIR)$(DBUS_SERVICES_DIR)/org.freedesktop.Telepathy.ConnectionManager.eri.service
	$(RM)               $(DESTDIR)$(DESTDIR)$(MANAGERS_DIR)/eri.manager
	$(RM)               $(DESTDIR)$(DATADIR)/telepathy-eri/
