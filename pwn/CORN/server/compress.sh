#!/bin/sh

TOP=$PWD
cd $TOP/initramfs
find . -print0 | cpio --null -ov --format=newc | gzip -9 > $TOP/initramfs.cpio.gz
