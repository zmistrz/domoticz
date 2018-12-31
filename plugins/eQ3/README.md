# domoticz

1.Zainstalować wtyczkę do pythona, która służy do uruchamiania poleceń unix w środowisku pythona:
sudo pip3 install pexpect

2.Po pobraniu należy wejść katalog pluginu i w pliku plugin.py linia 16 zmienić lokalizację do bibliotek pythona na własną ścieżkę, którą można sprawdzić wpisując polecenie:
sudo pip3 install pexpect, które powinno zwrócić coś takiego: Requirement already satisfied: pexpect in /usr/local/lib/python3.6/dist-packages

Niestety instalacja poprzez pip nie działa. (pip install pexpect oraz pip3 install pexpect). 
Jest jakiś problem polegający na tym że Domoticz nie widzi pakietów bibliotek zainstalowanych w domyślnej lokalizacji pythona (może to poprawią kiedyś :) ).

Dostajemy błąd:

(eQ3Bth) failed to load 'plugin.py', Python Path used was '/home/pi/domoticz/plugins/eQ3/:/usr/lib/python35.zip:/usr/lib/python3.5:/usr/lib/python3.5/plat-arm-linux-gnueabihf:/usr/lib/python3.5/lib-dynload'.
Error: (testowy plugin) Module Import failed, exception: 'ImportError'
Error: (testowy plugin) Module Import failed: ' Name: pexpect'
Error: (testowy plugin) Error Line details not available.

