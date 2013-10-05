prefix=/usr
LIBEXECDIR=$(prefix)/libexec
datadir=$(prefix)/share
DBUS_SERVICES_DIR=$(datadir)/dbus-1/services
MANAGERS_DIR=$(datadir)/telepathy/managers
INSTALL=install -D -p

BUILT_FILES = $(service_in_files:.service.in=.service)
service_in_files = data/org.freedesktop.Telepathy.ConnectionManager.eri.service.in
service_DATA = $(BUILT_FILES)
manager_DATA = data/eri.manager
ERI=telepathy-eri

$(service_DATA): $(service_in_files)
	@sed -e "s|\@libexecdir\@|$(libexecdir)|" $< > $@

install: $(service_DATA)
	$(INSTALL) -m755 $(ERI)           $(DESTDIR)$(LIBEXECDIR)/telepathy-eri
	$(INSTALL) -m644 $(service_DATA)  $(DESTDIR)$(DBUS_SERVICES_DIR)/org.freedesktop.Telepathy.ConnectionManager.eri.service
	$(INSTALL) -m644 $(manager_DATA)  $(DESTDIR)$(MANAGERS_DIR)/eri.manager
