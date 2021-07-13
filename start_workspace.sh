#!/bin/bash
echo "--------------------------------------------------------------------"
echo "--------------------------------------------------------------------"
echo "--------------------------------------------------------------------"
echo "------------------Leon Tinashe Mwandiringa atm----------------------"
echo "-------------------- new york transportatiton ----------------------"
echo "--------------------------------------------------------------------
"

CURRENTFOLDER=`pwd`
$SOURCEFOLDER="new-york-transport"
echo "$CURRENTFOLDER/$SOURCEFOLDER/jupyter"

docker build -t workspace --build-arg "SOURCEFOLDER=$SOURCEFOLDER" .
docker run -itd -p 8888:8888 -p 4040:4040 -v $CURRENTFOLDER/$SOURCEFOLDER/jupyter:/home/jupyter/jupyter_default_dir -v ~/.aws:/root/.aws:ro -v $CURRENTFOLDER/$SOURCEFOLDER:/home/workspace/ --name glueworkspace workspace

echo $'\e[1;34m'"------------------- Done Building and running glue worskapces ------------------------
"$'\e[0m'