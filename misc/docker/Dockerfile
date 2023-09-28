FROM ubuntu:latest
RUN apt-get update && apt-get install -y coreutils && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    python3 \
    git \
    numactl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN useradd -ms /bin/bash dtnuser
USER dtnuser
WORKDIR /home/dtnuser
CMD ["/bin/bash"]

