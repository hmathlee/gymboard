#!/bin/bash

VIDEO_DIR=$1

for label in $VIDEO_DIR/*; do
	for vid in $label/*; do
		fname="${vid%.*}"
		ffmpeg -i $vid -q:v 0 ${fname}.mp4
		rm $vid
	done
done
