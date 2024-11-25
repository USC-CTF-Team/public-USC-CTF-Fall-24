FROM ubuntu:22.04

RUN apt-get update && apt-get install -y gcc gcc-multilib socat
RUN useradd -ms /bin/sh chal
WORKDIR /home/chal

COPY ./canary-brute-force-chal.c ./
COPY ./flag.txt ./flag.txt

RUN gcc -o canary-brute-force-chal canary-brute-force-chal.c -no-pie -fstack-protector

RUN chown -R chal:chal /home/chal && \
     chmod 755 /home/chal && \
     chown chal:chal /home/chal/flag.txt && \
     chmod 444 /home/chal/flag.txt

EXPOSE 5000
USER chal
CMD ["socat", "-T60", "TCP-LISTEN:9999,reuseaddr,fork","EXEC:/home/chal/canary-brute-force-chal,stderr"]