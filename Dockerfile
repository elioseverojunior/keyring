ARG TAG=latest
ARG USER=

FROM debian:${TAG}

ENV USER=${USER:-keyring}

WORKDIR /tmp

RUN apt update  -y\
 && apt upgrade -y\
 && apt install -y\
 curl\
 glibc-*\
 gnome-keyring\
 htop\
 jq\
 libdbus-*\
 libdbus-*\
 libglib*\
 python3-dev\
 python3-pip\
 python3\
 vim\
 wget\
 && ln -sf /usr/bin/python3 /usr/bin/python\
 && python -m pip install --upgrade pip\
 && pip install wheel pytest secretstorage dbus-python keyring

COPY ./keyring-dbus-init.sh /usr/local/bin/keyring-dbus-init
RUN chmod +x /usr/local/bin/keyring-dbus-init

RUN useradd -m -u 1000 -U ${USER}

USER ${USER}

WORKDIR /home/${USER}

COPY --chown=${USER}:${USER} ./samples /home/${USER}/samples
RUN chmod +x "/home/${USER}/samples/test_keyring.py"

RUN openssl rand -base64 32 > /home/${USER}/.keyring

ENTRYPOINT [ "dbus-run-session", "--", "/bin/bash", "-c", "/usr/local/bin/keyring-dbus-init && /bin/bash" ]
