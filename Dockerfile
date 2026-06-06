# Copyright (c) 2026 LG Electronics Inc.
# SPDX-License-Identifier: MIT
#
# Consistent build and development environment for meta-shift.
# Base image: Ubuntu 22.04

FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=builder
ARG USER_UID=1000
ARG USER_GID=1000

# Yocto host dependencies (per the Yocto Project reference manual) plus a few
# development conveniences. python3-pytest is used to run the meta-shift tests.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential ca-certificates chrpath cpio curl debianutils diffstat \
      file gawk gcc git iputils-ping libacl1 locales lz4 \
      python3 python3-git python3-jinja2 python3-pexpect python3-pip \
      python3-pytest python3-subunit rsync socat sudo texinfo unzip vim \
      wget xz-utils zstd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Yocto requires the en_US.UTF-8 locale and bash (not dash) as /bin/sh.
RUN locale-gen en_US.UTF-8 && \
    echo "dash dash/sh boolean false" | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

# Android 'repo' tool and a default git identity for devtool/bitbake operations.
RUN curl -fsSL https://storage.googleapis.com/git-repo-downloads/repo -o /usr/bin/repo && \
    chmod a+x /usr/bin/repo && \
    git config --system user.email "anonymous@example.com" && \
    git config --system user.name  "anonymous"

# Yocto refuses to build as root, so create an unprivileged build user.
# Ubuntu 24.04 ships a default user/group at uid/gid 1000; free them first.
RUN if u="$(getent passwd ${USER_UID} | cut -d: -f1)" && [ -n "$u" ]; then userdel -r "$u" 2>/dev/null || true; fi && \
    if g="$(getent group ${USER_GID} | cut -d: -f1)" && [ -n "$g" ]; then groupdel "$g" 2>/dev/null || true; fi && \
    groupadd -g ${USER_GID} ${USERNAME} && \
    useradd -m -u ${USER_UID} -g ${USER_GID} -s /bin/bash ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US:en

WORKDIR /home/${USERNAME}

CMD ["/bin/bash"]
