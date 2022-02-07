#!/bin/bash
RAW_FILE="$HOME/raw_speed.csv"
SERVER_ID=14859

#Check if the header file exist
if [ ! -f $RAW_FILE ]; then
  #Run the header dump
  touch $RAW_FILE
  speedtest-cli --csv-header > $RAW_FILE
fi

# Append the result of the speedtest to the file
speedtest-cli --server $SERVER_ID --csv >> $RAW_FILE
#speedtest-cli --csv >> $RAW_FILE


