#!/bin/bash
RAW_FILE="$HOME/raw_speed.csv"
SERVER_ID=14859

#Check if the header file exist
if [ ! -f $RAW_FILE ]; then
  #Run the header dump
  touch $RAW_FILE
  echo -n '"Date",' > $RAW_FILE
  speedtest -f csv --output-header |  head -n1  >> $RAW_FILE
fi

# Append the result of the speedtest to the file
speedtest -s $SERVER_ID -f csv | ts '"%Y-%m-%d %H:%M:%S",' >> $RAW_FILE
#speedtest-cli --csv >> $RAW_FILE


