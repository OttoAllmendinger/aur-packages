pacman -R murmur-static
makepkg --asroot -fi
murmur -supw fnord
/etc/rc.d/murmur start
/etc/rc.d/murmur stop
pacman -R murmur-static
