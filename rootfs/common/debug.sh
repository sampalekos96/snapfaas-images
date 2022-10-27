## Setup console
ln -s agetty /etc/init.d/agetty.ttyS1
echo ttyS1 > /etc/securetty
rc-update add agetty.ttyS1 default
rc-update add agetty.ttyS1 nonetwork

echo agetty_options=\"-a root\" >> /etc/conf.d/agetty

