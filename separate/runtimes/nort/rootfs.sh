cp /runtime/workload /bin/runtime-workload-elf
cat > /bin/runtime-workload <<EOF
#!/bin/sh
/usr/bin/setup-eth0.sh
/usr/bin/ioctl
/usr/bin/factorial $((1 << 28))
/bin/runtime-workload-elf /srv/workload
EOF
chmod +x /bin/runtime-workload
chmod +x /bin/runtime-workload-elf

cp /common/factorial /usr/bin/factorial
