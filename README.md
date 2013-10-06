telepathy-eri
=============

VK Connection Manager for Telepathy.

Requirements
------------

* python-mechanize
* make
* automake
* libxslt

How to install
--------------

```
$ make
# make install
```

How to use
----------

1. Open empathy/gnome-online-accounts
2. Add vk account

How to remove
-------------

```
# make uninstall
```

Some bubuntu-specific notes
---------------------------

For 12.10+ bubuntus copy files from accounts/* to /usr/share/accounts

Token authorize
---------------

At adding account use wrong password.

Open link: https://oauth.vk.com/authorize?client_id=2692017&scope=friends,messages,offline&redirect_uri=https://oauth.vk.com/blank.html&v=5.0&response_type=token

In response you will have redirect and in address-string you will have alike:
```
#access_token=[THIS]&expires_in=0&user_id=136195746
```

1. Open additional settings
2. Into Token-parameter enter "THIS"
