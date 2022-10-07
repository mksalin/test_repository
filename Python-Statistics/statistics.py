import json

#with open('/temp/statistics/000000-Home_program-20220928-182933-record.json', 'r') as f:

filename = "test.json"
#with open('/temp/statistics/statistics6.json', 'r') as f:
with open('/temp/statistics/' + filename, 'r') as f:
    data = json.load(f)

assets = data["assets"]
stats = data["stats"]

#counters
values = 0
gameclock_counter = 0

bypass_unknown_cam = 0
auto_tracking = 0
upstream_bypass = 0
tracer_bypass = 0
not_present = 0
auto_zoom = 0
tracer_manual_bypass = 0
integrator_bypass = 0
system_ok_counter = 0

#game_clock
gc_period = 0
gc_minute = 0
gc_second = 0
gc_stopped = 0

#create CSV file
f = open("C:/temp/statistics/" + filename + ".csv", "w")
f.write("time;upstream_bypass;integrator_bypass;tracer_bypass;tracer_not_present;auto_zoom;auto_tracking;tracer_manual_bypass;unknown_cam;period;gameclock_minute;gameclock_second;stopped\n")

for stat in stats:
    #flags
    bypass_unknown_cam_flag = 0
    auto_tracking_flag = 0
    upstream_bypass_flag = 0
    tracer_bypass_flag = 0
    not_present_flag = 0
    auto_zoom_flag = 0
    tracer_manual_bypass_flag = 0
    integrator_bypass_flag = 0
    system_ok_flag = 1
    values += 1  
    time = stat["time"]

    if "assets" in stat:
        asset = stat["assets"]

    if "game_clock" in stat:
        game_clock = stat["game_clock"]
        gameclock_counter += 1
        gc_minute = game_clock["minute"]
        gc_period = game_clock["period"]
        gc_second = game_clock["second"]
        gc_stopped = game_clock["stopped"]
        
    if "global" in stat:
        _global = stat["global"]
           
        if "upstream_bypass" in _global[0]:
            #print('upstream_bypass at ', time)
            upstream_bypass += 1
            upstream_bypass_flag = 1
            
            if "integrator" in _global[0]["upstream_bypass"]:
                print('integrator bypass at ', time)
                integrator_bypass += 1    
                integrator_bypass_flag = 1
                system_ok_flag = 0
                
            if "tracer" in _global[0]["upstream_bypass"]:
                #print('tracer bypass at ', time)
                tracer_bypass += 1    
                tracer_bypass_flag = 1
            
            if "auto_tracking" in _global[0]["upstream_bypass"]["tracer"]:
                print('auto_tracking bypass at ', time)
                auto_tracking += 1
                auto_tracking_flag = 1
                system_ok_flag = 0
                
            if "not_present" in _global[0]["upstream_bypass"]["tracer"]:
                #print('not_present at ', time)
                not_present += 1
                not_present_flag = 1
                
            if "auto_zoom" in _global[0]["upstream_bypass"]["tracer"]:
                print('auto_zoom bypass at ', time)
                auto_zoom += 1
                auto_zoom_flag = 1
                #system_ok_flag = 0
                
            if "manual" in _global[0]["upstream_bypass"]["tracer"]:
                print('manual bypass at ', time)
                tracer_manual_bypass += 1
                tracer_manual_bypass_flag = 1
                system_ok_flag = 0
                
        if "bypass_unknown_cam" in _global[0]:
            #print('bypass_unknown_cam at ', time)
            bypass_unknown_cam += 1
            bypass_unknown_cam_flag = 1
            
    if (system_ok_flag == 1):
        #print('system ok...')
        system_ok_counter += 1
        
    f.write(str(round(time)) + ";" + str(upstream_bypass_flag) + ";" + str(integrator_bypass_flag) + ";" + str(tracer_bypass_flag) + ";" + str(not_present_flag) + ";" + str(auto_zoom_flag) + ";" + str(auto_tracking_flag) + ";" + str(tracer_manual_bypass_flag) + ";" + str(bypass_unknown_cam_flag) + ";" + str(gc_period) + ";" + str(gc_minute) + ";" + str(gc_second) + ";" + str(gc_stopped) + "\n" )

print('----------------') 
print('values ', values)    

print('Summary: ' + filename)    
print('End time (s) ', round(time))    
print('End time (min) ', round(time/60))    
print('----------------') 
print('Total sytem up time (s)', system_ok_counter)
print('Total system up time (min)', round(system_ok_counter/60))
print('Total system up time (%)', round(system_ok_counter/values * 100 ,2))

print('----------------') 
print('Bypass summary') 
print('Total upstream_bypass time (s)', upstream_bypass)
print('- Total Integrator_bypass time (s) ', integrator_bypass)
#print('Total Tracer_bypass time (s) ', tracer_bypass)
#print('Tracer not present time (s) ', not_present)
print('- Tracer auto zoom bypass time (s) ', auto_zoom)
print('- Tracer auto tracking bypass time (s) ', auto_tracking)
print('- Tracer manual bypass time (s) ', tracer_manual_bypass)
print('----------------') 
print('Non-Supponor camera on air time (s) ', bypass_unknown_cam)
print('----------------') 

if (gameclock_counter > 0):
    print('Game clock detected')
else:
    print('Game clock not detected')

f.close()
