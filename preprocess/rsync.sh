#!/usr/local/bin/zsh

# This script is configured to be called from Woodstock and sync to Shermy attached storage
# and the Schroeder NAS.

rsync -avp --delete /VolumesFranklin/Media/ /Volumes/Shermy
rsync -av --delete /Volumes/Franklin/Media/Music/ jay@192.168.0.215:/volume1/media/Music --exclude='*.DS_Store'

