# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 15:56:01 2022

@author: yhd
"""

from sumolib import checkBinary  # noqa
import traci  # noqa
import os
import sys
import math
from utils import cycle_time,incoming_lane,next_green,advise_speed

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
sumocfg_file = "environment/demo.sumocfg"
if__show__gui =True
if not if__show__gui :
    sumoBinary = checkBinary('sumo')
else :
    sumoBinary = checkBinary('sumo-gui')
traci.start([sumoBinary, "-c", sumocfg_file,'--fcd-output','speed_guide.fcd.xml'])
# traci.start([sumoBinary, "-c", sumocfg_file])
# traci.start([sumoBinary, "-c", sumocfg_file])

stop_veh = []

''' the above is the tools to start sumo'''


def veh_change_lane(veh_id):
    '''the function is to control vehicle change lane
    veh_id - the id of vehicle
    current_lane ,edge - the current lane or edge of the vehicle
    '''
    current_lane = traci.vehicle.getLaneID(veh_id)
    current_edge = traci.lane.getEdgeID(current_lane)
    if current_edge == 'E8':
        if current_lane != 'E8_0' and veh_id[:3] == 'f_1':
            print('vehicle_id',vehicle_id,'change_lane')
            traci.vehicle.changeLane(veh_id,0,15)
        elif current_lane != 'E8_2' and veh_id[:3] == 'f_0':
            print('vehicle_id',vehicle_id,'change_lane')
            traci.vehicle.changeLane(veh_id,2,15)
    elif current_edge == '-E_7':
        if current_lane != '-E7_0' and veh_id[:3] == 't_0':
            print('vehicle_id',vehicle_id,'change_lane')
            traci.vehicle.changeLane(veh_id,0,15)
        elif current_lane != '-E7_2' and veh_id[:3] == 't_1':
            print('vehicle_id',vehicle_id,'change_lane')
            traci.vehicle.changeLane(veh_id,2,15)
# while traci.simulation.getMinExpectedNumber() > 0:
for i in range(1000):
    traci.simulationStep()#控制仿真进行
    time = traci.simulation.getTime()#获取当前仿真时间
    for vehicle_id in traci.vehicle.getIDList():#在vehicle_list中遍历vehicle_id
        veh_change_lane(vehicle_id)#在车道进入交叉口前控制车辆进行变道操作
        if traci.vehicle.getNextTLS(vehicle_id) != ():#如果车辆前方存在交叉口
            if traci.vehicle.getNextTLS(vehicle_id)[0][2] < 200: #速度引导范围 150m
                next_g_start , next_g_end =  next_green(vehicle_id)#获取下一绿灯开始和结束时间
                distance = traci.vehicle.getNextTLS(vehicle_id)[0][2]
                if traci.vehicle.getTypeID(vehicle_id) == 'Truck':#如果车辆类型为truck，则跳过引导
                    continue
                
                speed_adv = advise_speed(vehicle_id,next_g_start,next_g_end)#获取建议速度
                
                if speed_adv < 1:
                    traci.vehicle.setSpeed(vehicle_id,-1) #如果建议速度过小，则将速度控制权返回sumo
                else:
                    traci.vehicle.setSpeed(vehicle_id,speed_adv)#将建议速度作用在车辆上
                
                
            elif traci.vehicle.getNextTLS(vehicle_id)[0][2] > 150: #离开速度引导范围
                if traci.vehicle.getTypeID(vehicle_id) == 'Truck':#如果车辆类型为truck，则跳过引导
                    continue
                traci.vehicle.setColor(vehicle_id,(255,255,0))
                traci.vehicle.setSpeed(vehicle_id,-1)
                
        elif traci.vehicle.getNextTLS(vehicle_id) == (): #如果车辆前方没有交叉口
            print(vehicle_id,'结束')
            traci.vehicle.setColor(vehicle_id,(255,255,0))
            traci.vehicle.setSpeed(vehicle_id,-1)#速度控制权返回给sumo
                
    else:
        continue
    
                
           
            
           
            
           
            