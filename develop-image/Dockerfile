FROM ubuntu:18.04

RUN apt-get update &&                                                        \
    apt-get install -y dialog &&                                             \
    apt-get install -y apt-utils &&                                          \
    apt-get upgrade -y &&                                                    \
    apt-get install -y sudo

# This adds the 'default' user to sudoers with full privileges:
RUN HOME=/home/default &&                                                    \
    mkdir -p ${HOME} &&                                                      \
    GROUP_ID=1000 &&                                                         \
    USER_ID=1000 &&                                                          \
    groupadd -r default -f -g "$GROUP_ID" &&                                 \
    useradd -u "$USER_ID" -r -g default -d "$HOME" -s /sbin/nologin          \
    -c "Default Application User" default &&                                 \
    chown -R "$USER_ID:$GROUP_ID" ${HOME} &&                                 \
    usermod -a -G sudo default &&                                            \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


RUN apt-get install -y                                                       \
       build-essential                                                       \
       vim                                                                   \
       make                                                                  \
       git                                                                   \
       less                                                                  \
       curl                                                                  \
       wget                                                                  \
       zlib1g-dev                                                            \
       libssl-dev                                                            \
       libffi-dev                                                            \
       python3-dev                                                           \
       python3-pip


# needed by Pipenv
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt install python3.7 python3-venv python3.7-venv -y
RUN apt install tox
RUN python3.7 -m pip install -U pipenv

ENV PATH="/usr/local/bin:${PATH}"
USER default

RUN sudo mkdir /build
WORKDIR /build
COPY . /build

RUN sudo make clean

RUN pipenv --python python3.7
RUN pipenv install --dev
RUN pipenv run pip3 install .

CMD ["/bin/bash"]