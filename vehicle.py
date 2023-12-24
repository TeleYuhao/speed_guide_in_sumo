from sumolib import checkBinary  # noqa
import traci  # noqa
import os
import sys
import math

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumocfg_file = "osm.sumocfg"
if__show__gui =True
if not if__show__gui :
    sumoBinary = checkBinary('sumo')
else :
    sumoBinary = checkBinary('sumo-gui')


def cycle_time(tls_id):
    tls_logic = traci.trafficlight.getAllProgramLogics(tls_id)
    current_phase = tls_logic[0].currentPhaseIndex
    remaining_time = traci.trafficlight.getNextSwitch(tls_id) - traci.simulation.getCurrentTime()/1000
    cycle_time = 0
    for i in  range(len(tls_logic[0].phases)):
        cycle_time += tls_logic[0].phases[i].duration
    return cycle_time


def incoming_lane(tls_id):
    logic = traci.trafficlight.getAllProgramLogics(tls_id)#获取控制方案
    in_lane = traci.trafficlight.getControlledLanes(tls_id)
    program = logic[0]
    phase = {}#定义空相位
    for i in range(len(program.phases)):#遍历信号相位
        if i%2 ==0:#因为相位中间存在黄灯信号，所以绿灯信号全为双数
            phase[i] = program.phases[i].state#信号为logic格式，.state是其中的具体信号控制方案
    incoming_lanes_all = {}#定义进口车道集
    for i in phase:#遍历相位
        incoming_lanes = []#定义进口空车道
        k = 0#控制相位数
        #print(phase[i])
        for j in phase[i]:
            #print(k)
            if j =='G':#将’G‘对应的车道记录下来
                #print(k)
                incoming_lanes.append(in_lane[k])
                #print(incoming_lanes)
            k = k+1
        incoming_lanes_all[i] = incoming_lanes#将每一相位的车道保存
    return incoming_lanes_all


def next_green(vehicle_id):
    data = traci.vehicle.getNextTLS(vehicle_id)
    tls_id_1 = data[0][0]
    in_lane = incoming_lane(tls_id_1)
    cycle = cycle_time(tls_id_1)
    current_lane = traci.vehicle.getLaneID(vehicle_id)
    
    
    if current_lane[0:11] =='858770823#1' or current_lane[0:11] == '858770823#2':
        lane_code = current_lane[11:13]
        current_lane ='858770823#3' +  lane_code
    
    elif current_lane[0:11] =='858770823#5':
        lane_code = current_lane[11:13]
        current_lane ='858770823#6' +  lane_code
    
    elif current_lane[0:11] =='859509946#0':
        lane_code = current_lane[11:13]
        current_lane ='859509946#1' +  lane_code
        
    elif current_lane[0:11] =='859509946#2' or current_lane[0:11] =='859509946#3' :
        lane_code = current_lane[11:13]
        current_lane ='859509946#4' +  lane_code
    
    elif current_lane[0:11] =='859509946#6':
        lane_code = current_lane[11:13]
        current_lane ='859509946#7' +  lane_code
        
        
        
    elif current_lane[0:11] =='145696438#1' and current_lane[0:12] !='145696438#11':
        lane_code = current_lane[11:13]
        current_lane ='145696438#2' +  lane_code
        
    elif current_lane[0:11] =='145696438#5':
        lane_code = current_lane[11:13]
        current_lane ='145696438#6' +  lane_code
        
    elif current_lane[0:11] =='145696438#8' or current_lane[0:11] =='145696438#9':
        lane_code = current_lane[11:13]
        current_lane ='145696438#10' +  lane_code
        
        
    elif current_lane[0:11] =='859509947#1':
        lane_code = current_lane[11:13]
        current_lane ='859509947#2' +  lane_code
    
    
    signal_state_1 = data[0][3]
    phases = traci.trafficlight.getAllProgramLogics(tls_id_1)[0].phases
    phases_num  = len(phases)
    remaining_time = traci.trafficlight.getNextSwitch(tls_id_1) - traci.simulation.getCurrentTime()/1000
    
    if current_lane in in_lane[0]:
        green_phase = 0
        #print(green_phase)
        
        
    elif current_lane in in_lane[2]:
        green_phase = 2
        #print(green_phase)
        
    elif current_lane[0:8] == 'cluster':
        print(current_laner)
        green_phase = 0
        
        
    else :
        print("绿灯相位读取错误")
        green_phase = 0
    current_phase = traci.trafficlight.getPhase(tls_id_1)
    
    
    if signal_state_1 == 'g' or signal_state_1 == 'G':
        next_g_start = cycle - traci.trafficlight.getPhaseDuration(tls_id_1) + remaining_time
        next_g_end = cycle + remaining_time
        
        
    elif signal_state_1 == 'r' or signal_state_1 == 'y':
        
        if green_phase == 0 :
            if current_phase == 1:
                next_g_start = remaining_time+phases[2].duration+phases[3].duration
                next_g_end = next_g_start + phases[0].duration
            elif current_phase == 2:
                next_g_start = remaining_time + phases[3].duration
                next_g_end = next_g_start + phases[0].duration
            elif current_phase == 3:
                next_g_start = remaining_time
                next_g_end = next_g_start + phases[0].duration
                
                
            elif current_phase == 0:
                next_g_start = remaining_time + phases[1].duration
                next_g_end = remaining_time + phases[1].duration + phases[2].duration
                
                
        if green_phase == 2:
            if current_phase == 3:
                next_g_start = remaining_time+phases[0].duration+phases[1].duration
                next_g_end = next_g_start + phases[2].duration
            elif current_phase == 0:
                next_g_start = remaining_time+phases[1].duration
                next_g_end = next_g_start + phases[2].duration
            elif current_phase == 1:
                next_g_start = remaining_time
                next_g_end = next_g_start + phases[2].duration
                
                
                
    return next_g_start,next_g_end


def advise_speed(vehicle_id, next_g_start, next_g_end):
    min_speed = 2.0
    max_speed = traci.vehicle.getAllowedSpeed(vehicle_id)
    acc = traci.vehicle.getAccel(vehicle_id)
    dec = -traci.vehicle.getDecel(vehicle_id)
    distance = traci.vehicle.getNextTLS(vehicle_id)[0][2]
    speed_now = traci.vehicle.getSpeed(vehicle_id)
    phase_now = traci.vehicle.getNextTLS(vehicle_id)[0][3]
    if phase_now == 'G' or phase_now == 'g':
        remaining_time = traci.trafficlight.getNextSwitch(
            traci.vehicle.getNextTLS(vehicle_id)[0][0]) - traci.simulation.getCurrentTime() / 1000
        if remaining_time > distance / (speed_now + 0.01):  # 绿灯匀速通过
            speed_advise = speed_now
            traci.vehicle.setColor(vehicle_id, (0, 255, 0))  # 设置颜色为绿色
            print('speed_now:', speed_now)
            print(speed_advise, '绿灯匀速通过')


        elif remaining_time > ((distance - (max_speed ** 2 - speed_now ** 2) / (2 * acc)) / max_speed + (
                max_speed - speed_now) / acc) and remaining_time < distance / (speed_now + 0.0000000001):
            discriminant = acc ** 2 * remaining_time ** 2 + 2 * acc * speed_now * remaining_time - 2 * acc * distance  # 计算方程判别式
            accTime = (acc * remaining_time - math.sqrt(discriminant)) / acc
            speed_advise = speed_now + accTime * acc  # 绿灯加速通过
            traci.vehicle.setColor(vehicle_id, (255, 0, 255))  # 设置颜色为粉色
            print('speed_now:', speed_now)
            print(speed_advise, '绿灯加速通过')

        elif remaining_time <= ((distance - (max_speed ** 2 - speed_now ** 2) / (2 * acc)) / max_speed + (
                max_speed - speed_now) / acc) and next_g_start < (
                (distance - (min_speed ** 2 - speed_now ** 2) / (2 * dec)) / min_speed + (min_speed - speed_now) / dec):
            discriminant_1 = dec ** 2 * next_g_start ** 2 + 2 * dec * speed_now * next_g_start - 2 * dec * distance
            decTime_1 = (dec * next_g_start + math.sqrt(discriminant_1)) / dec
            speed_advise_1 = speed_now + decTime_1 * dec  # 绿灯减速通行

            discriminant_2 = dec ** 2 * next_g_end ** 2 + 2 * dec * speed_now * next_g_end - 2 * dec * distance
            decTime_2 = (dec * next_g_end + math.sqrt(discriminant_2)) / dec
            speed_advise_2 = speed_now + decTime_2 * dec  # 绿灯减速通行

            speed_advise = (speed_advise_1 + speed_advise_2) / 2

            traci.vehicle.setColor(vehicle_id, (0, 255, 255))  # 设置颜色为蓝色

            print(traci.simulation.getCurrentTime() / 1000)
            print('speed_now:', speed_now)
            print(speed_advise_1, speed_advise_2, '绿灯减速通行')


        elif remaining_time <= ((distance - (max_speed ** 2 - speed_now ** 2) / (2 * acc)) / max_speed + (
                max_speed - speed_now) / acc) and next_g_start >= (
                (distance - (min_speed ** 2 - speed_now ** 2) / (2 * dec)) / min_speed + (min_speed - speed_now) / dec):
            discriminant = dec ** 2 * next_g_start ** 2 + 2 * dec * speed_now * next_g_start - 2 * dec * distance
            decTime = (dec * next_g_start + math.sqrt(discriminant)) / dec
            speed_advise = speed_now + decTime * dec  # 绿灯减速停车
            if speed_advise < min_speed:
                speed_advise = min_speed

            traci.vehicle.setColor(vehicle_id, (255, 0, 0))  # 设置为红色
            print('speed_now:', speed_now)
            print(speed_advise, '绿灯减速停车')

    if phase_now == 'r' or phase_now == 'y':
        if next_g_start < distance / (speed_now + 0.01) and next_g_end > distance / (speed_now + 0.01):
            if distance / (speed_now + 0.01) - next_g_start < 2:
                speed_advise = distance / (next_g_start + 3)
                print('略微减速')
            else:
                speed_advise = speed_now  # 红灯匀速通行
            traci.vehicle.setColor(vehicle_id, (255, 255, 255))  # 设置颜色为白色
            print('speed_now:', speed_now)
            print(speed_advise, '红灯匀速通过')


        elif next_g_start < distance / (speed_now + 0.0000001) and next_g_start > (
                (distance - (max_speed ** 2 - speed_now ** 2) / (2 * acc)) / max_speed + (max_speed - speed_now) / acc):
            discriminant = dec ** 2 * next_g_start ** 2 + 2 * dec * speed_now * next_g_start - 2 * dec * distance  # 计算方程判别式
            decTime = (dec * next_g_start + math.sqrt(discriminant)) / dec
            speed_advise = speed_now + decTime * dec  # 红灯减速通行
            traci.vehicle.setColor(vehicle_id, (0, 0, 255))  # 设置颜色为蓝色
            print('speed_now:', speed_now)
            print(speed_advise, '红灯减速通过')


        elif next_g_end > ((distance - (max_speed ** 2 - speed_now ** 2) / (2 * acc)) / max_speed + (
                max_speed - speed_now) / acc) and next_g_end < distance / (speed_now + 0.00000001):
            discriminant = acc ** 2 * next_g_end ** 2 + 2 * acc * speed_now * next_g_end - 2 * acc * distance  # 计算方程判别式
            accTime = (acc * next_g_end - math.sqrt(discriminant)) / acc
            speed_advise = speed_now + accTime * acc  # 红灯加速通过
            traci.vehicle.setColor(vehicle_id, (255, 0, 255))  # 设置颜色为粉色
            print('speed_now:', speed_now)
            print(speed_advise, '红灯加速通过')
            print(traci.simulation.getCurrentTime() / 1000)


        else:
            print('红灯减速停车')
            speed_advise = min_speed
            traci.vehicle.setColor(vehicle_id, (255, 0, 0))  # 设置为红色

    return speed_advise

traci.start([sumoBinary, "-c", sumocfg_file])


while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for vehicle_id in traci.vehicle.getIDList():
        traci.vehicle.setMaxSpeed(vehicle_id,16.67)
        allowed_speed = traci.vehicle.getAllowedSpeed(vehicle_id)

            
            
        if traci.vehicle.getNextTLS(vehicle_id) != ():
            if traci.vehicle.getNextTLS(vehicle_id)[0][2] < 210: 
                next_g_start , next_g_end =  next_green(vehicle_id)
                distance = traci.vehicle.getNextTLS(vehicle_id)[0][2]
                speed_adv = advise_speed(vehicle_id,next_g_start,next_g_end)
                traci.vehicle.setSpeed(vehicle_id,speed_adv)
                

                
            elif traci.vehicle.getNextTLS(vehicle_id)[0][2] > 220:
                traci.vehicle.setColor(vehicle_id,(255,255,0))
                traci.vehicle.setSpeed(vehicle_id,allowed_speed)
                
        elif traci.vehicle.getNextTLS(vehicle_id) == ():
            print(vehicle_id,'结束')
            traci.vehicle.setColor(vehicle_id,(255,255,0))
            traci.vehicle.setSpeed(vehicle_id,allowed_speed)
                

traci.close()