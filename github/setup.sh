#!/bin/bash

set -eu

if [[ -d $APPNAME ]]
then
	echo "App folder exists"
else
	mkdir ~/$APPNAME
if [[ -d ~/$APPNAME/config ]]
then
	echo "config folder exists"
else
	mkdir ~/$APPNAME/config
fi

if [[ -d ~/$APPNAME/kubeconfig ]]
then
	echo "Kubeconfig folder exists"
else
	mkdir ~/$APPNAME/kubeconfig
fi


#gpg --quiet --batch --yes --decrypt --passphrase="$EXKEY" --output ~/trigger/secrets ~/trigger/secrets.gpg &&

#tar -xf ~/trigger/secrets -C ~/trigger/ &&

#mv ~/trigger/config ~/$APPNAME/kubeconfig/ &&
mv ~/trigger/Config.yaml ~/$APPNAME/config/ &&