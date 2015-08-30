#!/bin/sh -x

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

cd "/home/prashanth/PartFour/src/arbotix_ros/arbotix_python"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/prashanth/PartFour/install/lib/python2.7/dist-packages:/home/prashanth/PartFour/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/prashanth/PartFour/build" \
    "/usr/bin/python" \
    "/home/prashanth/PartFour/src/arbotix_ros/arbotix_python/setup.py" \
    build --build-base "/home/prashanth/PartFour/build/arbotix_ros/arbotix_python" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/prashanth/PartFour/install" --install-scripts="/home/prashanth/PartFour/install/bin"
