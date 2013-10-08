#
# Regular cron jobs for the telepathy-eri package
#
0 4	* * *	root	[ -x /usr/bin/telepathy-eri_maintenance ] && /usr/bin/telepathy-eri_maintenance
