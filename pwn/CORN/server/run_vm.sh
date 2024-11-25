#!/bin/sh

qemu-system-x86_64 \
  -kernel ./bzImage \
  -initrd ./initramfs.cpio.gz \
  -nographic \
  -append "console=ttyS0 loadpin.enforce=0" \
  -monitor /dev/null \
  -m 1G \
  -cpu qemu64,+smep,+smap \
  -no-reboot \
