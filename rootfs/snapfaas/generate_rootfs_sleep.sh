SNAPFAAS=/mydata0/snapfaas
cp runtimes/python3/workload.sh runtimes/python3/workload.sh.bak
for i in {1..9}; do
    for j in {0..9}; do
        sed "s/sleep.*/sleep $i.$j/" runtimes/python3/workload.sh.bak > runtimes/python3/workload.sh
        suffix=$((i*1000+j*100))ms
        echo $suffix
        #./mk_rtimage.sh python3 /ssd/images/python3-$suffix.ext4
        #mkdir /tmp/snapfaas/snapshots/python3-$suffix
        #sudo $SNAPFAAS/target/release/fc_wrapper --mem_size 128 --vcpu_count 1 --network tap0/aa:bb:cc:dd:ff:00 \
        #    --firerunner $SNAPFAAS/target/release/firerunner \
        #    --kernel $SNAPFAAS/resources/images/vmlinux-4.20.0 --appfs $SNAPFAAS/snapfaas-images/appfs/empty/output.ext2 \
        #    --rootfs /ssd/images/python3-$suffix.ext4 --dump_dir /tmp/snapfaas/snapshots/python3-$suffix \
        #    --force_exit
        #mkdir /ssd/snapshots/diff/hello-sleep-python3-$suffix
        sudo $SNAPFAAS/target/release/fc_wrapper --mem_size 128 --vcpu_count 1 --network tap0/aa:bb:cc:dd:ff:00 \
            --firerunner $SNAPFAAS/target/release/firerunner \
            --kernel $SNAPFAAS/resources/images/vmlinux-4.20.0 --appfs /ssd/images/hello-sleep-python3.ext2 \
            --rootfs /ssd/images/python3-$suffix.ext4 --load_dir /tmp/snapfaas/snapshots/python3-$suffix \
            --dump_dir /ssd/snapshots/diff/hello-sleep-python3-$suffix --force_exit
    done
done
