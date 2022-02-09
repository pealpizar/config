#!/usr/bin/env python3

#Imports
import csv
import os

# Global variables
# RAW data file
raw_file = os.getenv("HOME") + "/raw_speed.csv"
# Final data file
converted_file = os.getenv("HOME") + "/mpbs_speed.csv"
# Summary file
sum_file = os.getenv("HOME") + "/speed_test.txt"
# Average dictionary
avg_dic = dict({'Ping':0, 'Download':0, 'Upload':0})
# Hired speed Mbps
exp_down_speed = 100
exp_up_speed = 5
# Fields to write
final_header = ["Fecha","ID_Servidor", "Nombre", "Ping(ms)", "Descarga(Mbps)", "Subida(Mbps)"]

# Check if the file exist
if not os.path.exists(raw_file) :
  # Error out: The file does not exist
  print("El archivo de datos no existe")
else:
  # Open CSV write
  dst_csv = open(converted_file, 'w+')
  writer_csv = csv.DictWriter(dst_csv, final_header)
  writer_csv.writeheader()
  # Load the file on CSV
  with open(raw_file) as rawcsv:
    samples = 0
    rawread = csv.DictReader(rawcsv)
    for row in rawread:
      # Add each row to create an average and write to the email file
      avg_dic['Ping'] += float(row['latency'])
      down_Mbps = float(row['download'])/125000
      avg_dic['Download'] += down_Mbps
      up_Mbps = float(row['upload'])/125000
      avg_dic['Upload'] += up_Mbps
      # Save valies into a ordered list in order to make easier saving them
      row_value_list = [row['Date'], row['server id'], row['server name'], float(row['latency']), down_Mbps, up_Mbps ]
      # Convert into a dictionary to write
      row_dict_write = dict(zip(final_header,row_value_list))
      # Write into the file
      writer_csv.writerow(row_dict_write)
      samples += 1
  # Close the files
  dst_csv.close()

  # Average require to divide between the number of samples
  avg_dic['Ping'] = avg_dic['Ping']/samples 
  avg_dic['Download'] = avg_dic['Download']/samples 
  avg_dic['Upload'] = avg_dic['Upload']/samples 

# Write into a file the latest week average
email_cmd = ""
if ((avg_dic['Download'] < exp_down_speed*0.8) or (avg_dic['Upload'] < exp_up_speed*0.8)):
  # The hired speed is below the threshold
  email_cmd += "Speed below threshold AVG="
else:
  # The hired speed is inside the threshold
  email_cmd += "Speed correct AVG="

email_cmd += str("%.2f" % avg_dic['Download']) + "/" + str("%.2f" % avg_dic['Upload']) +"\n"


with open(sum_file, "w+") as txt:
  txt.write(email_cmd)

os.remove(raw_file)
# Preapare to send the email
email_cmd = "mail -A " + converted_file + " -s "
if ((avg_dic['Download'] < exp_down_speed*0.8) or (avg_dic['Upload'] < exp_up_speed*0.8)):
  # The hired speed is below the threshold
  email_cmd += "\'Speed below threshold AVG="
else:
  # The hired speed is inside the threshold
  email_cmd += "\'Speed correct AVG="

email_cmd += str("%.2f" % avg_dic['Download']) + "/" + str("%.2f" % avg_dic['Upload']) + "\' pealpizar@hotmail.com < /dev/null"
os.system(email_cmd)
