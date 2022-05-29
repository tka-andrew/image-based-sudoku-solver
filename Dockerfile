FROM ubuntu:20.04

# Needed for Ubuntu installation
ENV DEBIAN_FRONTEND=noninteractive 
ENV TZ=Etc/UTC

# Install CMake and some necessary packages
# REFERENCE: https://docs.wxwidgets.org/trunk/overview_install.html
# under Debian and Debian-derived systems such as Ubuntu, you need to run apt get libwxgtkX.Y-dev.
# REFERENCE : https://askubuntu.com/questions/1241217/package-libwxgtk3-0-dev-has-no-installation-candidate-on-ubuntu-20-04
# libwxgtk3.0-dev was changed to libwxgtk3.0-gtk3-dev in Ubuntu 20.04.
# REFERENCE: https://askubuntu.com/questions/971560/what-is-the-purpose-of-canberra-gtk-module
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        git \
        libwxgtk3.0-gtk3-dev \
        pip  \
        python3.7 \
        python3-tk

RUN mkdir -p /src/ImageBasedSudokuSolver/

WORKDIR /src
COPY requirements.txt .
RUN pip install pip
RUN pip install --default-timeout=10 --no-cache-dir -r requirements.txt

# REFERENCE: https://www.reddit.com/r/docker/comments/szgbqc/installing_requirementstxt_takes_forever_while/
RUN mkdir -p /src/ImageBasedSudokuSolver/scripts
COPY scripts/ /src/ImageBasedSudokuSolver/scripts
RUN mkdir -p /src/ImageBasedSudokuSolver/images
COPY images/ /src/ImageBasedSudokuSolver/images
WORKDIR /src/ImageBasedSudokuSolver

# REFERENCE: https://unix.stackexchange.com/questions/230238/x-applications-warn-couldnt-connect-to-accessibility-bus-on-stderr
ENV NO_AT_BRIDGE=1

# This command runs your application, comment out this line to compile only
CMD ["python3","./scripts/imageBasedSudokuSolver.py"]
