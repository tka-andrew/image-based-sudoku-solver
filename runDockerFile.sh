# REFERENCE: https://jerin-electronics.medium.com/docker-now-ep1-python-opencv-in-docker-1dda564672c3

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native

# You need to bind your volume to the docker container, so that the image can be saved to your host machine
# REFERENCE: https://stackoverflow.com/questions/31046522/docker-save-file
sudo docker run --rm -it -e DISPLAY=$DISPLAY -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH \
                --volume=$PWD:/src/ImageBasedSudokuSolver/ \
                -e XAUTHORITY=$XAUTH -t tka-andrew/image-based-sudoku-solver:latest
