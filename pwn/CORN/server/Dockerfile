FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat qemu-system-x86

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY initramfs.cpio.gz bzImage run_vm.sh /home/ctf/

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 555 /home/ctf/run_vm.sh && \
    chmod 444 /home/ctf/bzImage && \
    chmod 444 /home/ctf/initramfs.cpio.gz

EXPOSE 5000
USER ctf
CMD ["socat", "-T60", "TCP-LISTEN:9999,reuseaddr,fork","EXEC:/home/ctf/run_vm.sh,stderr"]
