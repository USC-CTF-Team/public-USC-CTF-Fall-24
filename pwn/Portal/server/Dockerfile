FROM ubuntu:22.04

RUN apt-get update && apt-get install -y gcc gcc-multilib socat

RUN useradd -ms /bin/sh chal
WORKDIR /home/chal

COPY ./buffer-overflow-chal.c ./
COPY ./flag.txt ./

RUN gcc -o buffer-overflow-chal buffer-overflow-chal.c -Wl,-z,norelro -no-pie -fno-stack-protector -z execstack -m32

RUN chown -R chal:chal /home/chal && \
     chmod 755 /home/chal && \
     chown chal:chal /home/chal/flag.txt && \
     chmod 444 /home/chal/flag.txt

EXPOSE 5000

USER chal
ENTRYPOINT ["socat", "-T60", "TCP-LISTEN:9999,reuseaddr,fork","EXEC:/home/chal/buffer-overflow-chal"]