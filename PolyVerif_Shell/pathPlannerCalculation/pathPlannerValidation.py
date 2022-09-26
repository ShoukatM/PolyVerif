# -*- coding: utf-8 -*-
"""
Created on Mon May 10 16:38:24 2021

@author: 
"""
import csv  
import os
import math
import pandas as pd
from GenericParamComputation import GenericParams as gp
from utils.acquisition_structures import Deviation_Report

#function to compute localization deviation per frame/timestamp
def ComputeParams(goalPose_loc, lg_ego_loc, location, map_origion_error):
    deviation_report = location + "/deviation_report.csv" 
    
    with open(deviation_report,'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        title = Deviation_Report("timestamp_sec", "timestamp_nanosec", "position_x", "position_y",
                        "position_z", "orientation_x","orientation_y", "orientation_z", "orientation_w",
                        "deviation")
        writer.writerow(title)                         

    #goalPose_stamping = gp.TimeStamp_Mapping(goalPose_loc) # Calculate timestamp
    #lg_ego_stamping = gp.TimeStamp_Mapping(lg_ego_loc) # Calculate timestamp
    goal_pos_x = goalPose_loc.position_x[0]
    goal_pos_y = goalPose_loc.position_y[0]
    # Calculate deviation for each frame
    for idx_LG in range(lg_ego_loc["timestamp_sec"].count()-1):  
     
      # Taltech 
      # lg_pos_x   = lg_ego_loc.position_x[idx_LG] - map_origion_error[0]
      # lg_pos_y   = lg_ego_loc.position_y[idx_LG] - map_origion_error[1]
       
      # Autonomous Stuff
      lg_pos_y   = lg_ego_loc.position_x[idx_LG] - map_origion_error[0]
      lg_pos_x   = -(lg_ego_loc.position_y[idx_LG] - map_origion_error[1])

       # Calculate Euclidean distance using x nad y values
      deviation = math.sqrt((math.pow((goal_pos_x-lg_pos_x),2)) + (math.pow((goal_pos_y-lg_pos_y),2)))
      print("deviation", deviation)
       # Save data in to csv
      with open(deviation_report,'a', newline='') as csvfile:
          writer = csv.writer(csvfile)
          # Taltech
          # values = Deviation_Report(lg_ego_loc.timestamp_sec[idx_LG], lg_ego_loc.timestamp_nanosec[idx_LG],
          #                            lg_ego_loc.position_x[idx_LG],lg_ego_loc.position_y[idx_LG], lg_ego_loc.position_z[idx_LG],
          #                            lg_ego_loc.orientation_x[idx_LG],lg_ego_loc.orientation_y[idx_LG], lg_ego_loc.orientation_z[idx_LG],
          #                            lg_ego_loc.orientation_w[idx_LG], deviation)

          # Autonomous Stuff
          values = Deviation_Report(lg_ego_loc.timestamp_sec[idx_LG], lg_ego_loc.timestamp_nanosec[idx_LG],
                                     -(lg_ego_loc.position_y[idx_LG]),lg_ego_loc.position_x[idx_LG], lg_ego_loc.position_z[idx_LG],
                                     lg_ego_loc.orientation_x[idx_LG],lg_ego_loc.orientation_y[idx_LG], lg_ego_loc.orientation_z[idx_LG],
                                     lg_ego_loc.orientation_w[idx_LG], deviation)
          writer.writerow(values)   
         
#function to calculate consolidated data from framewise data 
def DeviationParams(location):
    print("Computing deviation params")
    deviation_report = location + "/deviation_report.csv"
    deviation_data = Read_data(deviation_report) # Read per frame based deviation data
    
    lengthOfData = len(deviation_data)
    #deviationFromGoalPos = deviation_data["deviation"]
    deviationFromGoalPos = deviation_data.deviation[lengthOfData - 1]
    deviationFromGoalPos = round(deviationFromGoalPos, 2)
    goalPosAchieved = False
    print("deviationFromGoalPos", deviationFromGoalPos)
    if(deviationFromGoalPos < 5):
      goalPosAchieved = True
    else:
      goalPosAchieved = False


    deviation_stats_file = location + "/planner_stats.txt" 
    file = open(deviation_stats_file,'w+');

    goalPosD = str(deviationFromGoalPos)
    goalPosAchieveD = str(goalPosAchieved)
    line = [goalPosD+"\n",goalPosAchieveD+"\n"]

    file.writelines(line)
    file.close()
    


#function to read GT data using given filename
def Read_data(filename):
    data = pd.read_csv(filename)
    #print(data.to_string()) 
    return data

#main function for calling various functions available in various classes
def main(args=None):

    currentpath = os.getcwd()
    print("location : ", currentpath)

    pos = currentpath.rfind('/')
    adePath = currentpath[0:pos]
    location = adePath + '/'
    f_path = open(location + 'PolyReports/Validation_report/config1.txt', 'r')
    path = f_path.readline()
    file_path = path.strip()
    f_path.close()

    print("adepath : ", adePath)
    print("Calculating Path Planner Validation.")
    # /home/acclivis/adehome/PolyReports/GNSS_ODOM_Localization.csv

    # Need to read from the config file for map error
    # Taltech
    #map_origion_error = [0,-300,0]

    # Autonomous stuff
    map_origion_error = [0,0,0]

    #location = '/home/acclivis/adehome/PolyReports'
    goalPose_loc_file = location  + file_path + '/Goal_Pose_PathPlanning.csv'
    lg_ego_file = location  + file_path + '/GNSS_ODOM_Localization.csv'
    
    goalPose_loc = Read_data(goalPose_loc_file)
    lg_ego_loc = Read_data(lg_ego_file)
    
    ComputeParams(goalPose_loc, lg_ego_loc, location + file_path, map_origion_error)
    DeviationParams(location + file_path)
    
    
if __name__ == '__main__':
    main()
