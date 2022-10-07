import json
import sys
import os
import shutil

original_stdout = sys.stdout # Save a reference to the original standard output
 
def create_statistics(filename_json, summary_csv):

    with open('/temp/statistics/json/' + filename_json + '.json', 'r') as f:
        data = json.load(f)

        assets = data["assets"]
        stats = data["stats"]

        #game data        
        match_name = data["match_name"]          
        output_feed = data["output_feed"]
        file_start_time = data["file_start_time"]

    filename = match_name + "_" + output_feed + "_" + filename_json
    
    #create summary CSV file
    #summary_csv = open("./csv/summary.csv", "a")
    #summary_csv.write("filename, file_start_time, match_name - output_feed, system_uptime_%")
    #summary_csv.close()
        
    with open("./log/" + filename + ".txt", "w") as logfile:
        sys.stdout = logfile # Change the standard output to the file we created.
        #original_stdout = sys.stdout # Save a reference to the original standard output
        
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
        renderer_bypass = 0
        system_ok_counter = 0

        #game_clock
        gc_period = 0
        gc_minute = 0
        gc_second = 0
        gc_stopped = 0

        #create CSV file
        f_csv = open("./csv/" + filename + ".csv", "w")
        f_csv.write("time;renderer_bypass;upstream_bypass;integrator_bypass;tracer_bypass;tracer_not_present;auto_zoom;auto_tracking;tracer_manual_bypass;unknown_cam;period;gameclock_minute;gameclock_second;stopped\n")
    
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
            renderer_bypass_flag = 0
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
                   
                #renderer manual_bypass
                if "manual_bypass" in _global[0]:
                    print('Renderer bypass at ', round(time), 's')
                    renderer_bypass += 1
                    renderer_bypass_flag = 1
                    system_ok_flag = 0
                   
                if "upstream_bypass" in _global[0]:
                    #print('upstream_bypass at ', round(time), 's')
                    upstream_bypass += 1
                    upstream_bypass_flag = 1
                    
                    if "integrator" in _global[0]["upstream_bypass"]:
                        print('Integrator bypass at ', round(time), 's')
                        integrator_bypass += 1    
                        integrator_bypass_flag = 1
                        system_ok_flag = 0
                        
                    if "tracer" in _global[0]["upstream_bypass"]:
                        #print('tracer bypass at ', round(time), 's')
                        tracer_bypass += 1    
                        tracer_bypass_flag = 1
                    
                        if "auto_tracking" in _global[0]["upstream_bypass"]["tracer"]:
                            print('Tracer auto-tracking bypass at ', round(time), 's')
                            auto_tracking += 1
                            auto_tracking_flag = 1
                            system_ok_flag = 0
                            
                        if "not_present" in _global[0]["upstream_bypass"]["tracer"]:
                            #print('not_present at ', round(time), 's')
                            not_present += 1
                            not_present_flag = 1
                            
                        if "auto_zoom" in _global[0]["upstream_bypass"]["tracer"]:
                            print('Tracer auto-zoom bypass at ', round(time), 's')
                            auto_zoom += 1
                            auto_zoom_flag = 1
                            #system_ok_flag = 0
                            
                        if "manual" in _global[0]["upstream_bypass"]["tracer"]:
                            print('Tracer manual bypass at ', round(time), 's')
                            tracer_manual_bypass += 1
                            tracer_manual_bypass_flag = 1
                            system_ok_flag = 0
                        
                if "bypass_unknown_cam" in _global[0]:
                    #print('bypass_unknown_cam at ', round(time), 's')
                    bypass_unknown_cam += 1
                    bypass_unknown_cam_flag = 1
                    
            if (system_ok_flag == 1):
                system_ok_counter += 1
                
            f_csv.write(str(round(time)) + ";" + str(round(renderer_bypass)) + ";" + str(upstream_bypass_flag) + ";" + str(integrator_bypass_flag) + ";" + str(tracer_bypass_flag) + ";" + str(not_present_flag) + ";" + str(auto_zoom_flag) + ";" + str(auto_tracking_flag) + ";" + str(tracer_manual_bypass_flag) + ";" + str(bypass_unknown_cam_flag) + ";" + str(gc_period) + ";" + str(gc_minute) + ";" + str(gc_second) + ";" + str(gc_stopped) + "\n" )

        print('----------------') 
        print('Processed file: ' + filename + '.json')   
        print('Match name ', match_name) 
        print('Output feed ', output_feed)   
        print('Recording start time ', file_start_time)           
        
        #print('values ', values)    
        print('End time (s) ', round(time))    
        print('End time (min) ', round(time/60))    
        print('----------------') 
        print('System up time calculations:') 
        print('Total system up time (s)', system_ok_counter)
        print('Total system up time (min)', round(system_ok_counter/60))
        print('Total system up time (%)', round(system_ok_counter/values * 100 ,2))
        #print('system_ok_counter:',system_ok_counter, ', values', values)
        print('----------------') 
        print('Bypass summary which affects up time calculations:') 
        print('- Total Renderer bypass time (s)', renderer_bypass)
        print('- Total Integrator_bypass time (s) ', integrator_bypass)
        print('- Tracer auto tracking bypass time (s) ', auto_tracking)
        print('- Tracer manual bypass time (s) ', tracer_manual_bypass)
        print('----------------') 

        print('Bypass summary which does not affect up time calculations:') 
        #print('- Total upstream bypass time (s)', upstream_bypass)
        #print('Total Tracer_bypass time (s) ', tracer_bypass)
        #print('Tracer not present time (s) ', not_present)
        print('- Tracer auto zoom bypass time (s) ', auto_zoom)
        print('----------------') 
        print('Non-Supponor camera on air time (s) ', bypass_unknown_cam)
        print('----------------') 

        if (gameclock_counter > 0):
            print('Game clock detected')
        else:
            print('Game clock not detected')

        f_csv.close()
        f.close()
     
    sys.stdout = original_stdout # Reset the standard output to its original value
    
    #copy interesting files under specific folders
    print('Match name:', match_name) 
    print('Output feed:', output_feed)   
    print('Recording start time:', file_start_time)
        
    if (round(system_ok_counter/values * 100 ,2) < 80):
        print('System up time < 80%')        
        shutil.copyfile("./log/" + filename + ".txt", "./less_than_80/" + filename + ".txt")
    elif (round(system_ok_counter/values * 100 ,2) < 90):
        print('System up time < 80%')       
        shutil.copyfile("./log/" + filename + ".txt", "./less_than_90/" + filename + ".txt")   
    elif (round(system_ok_counter/values * 100 ,2) < 95):
        print('System up time < 80%')
        shutil.copyfile("./log/" + filename + ".txt", "./less_than_95/" + filename + ".txt")
        
    if (gameclock_counter > 0):
        print('Game clock detected')
        shutil.copyfile("./log/" + filename + ".txt", "./gameclock/" + filename + ".txt")
    else:
        print('Game clock not detected')
    
    print('Total system up time (%)', round(system_ok_counter/values * 100 ,2))
    print("---------------------")
    
    #create summary CSV file
    #summary_csv = open("./csv/summary.csv", "a")
    summary_csv.write(filename + ';' + file_start_time + ';' + match_name + ' - ' + output_feed + ';' + str(round(system_ok_counter/values * 100 ,2)) + '\n')
    #summary_csv.close()
    
def loop_files():
    
    #create summary CSV file
    summary_csv = open("./csv/summary.csv", "w")
    summary_csv.write("filename; file_start_time; match_name - output_feed; system_uptime_%\n")    
    
    # assign directory
    directory = './json'
    print('Use directory:', directory)
    
    ## iterate over files in
    ## that directory
    for filename in os.listdir(directory):
        f_dir = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f_dir):
            print('Process file:' + f_dir)
            x = filename.split(".")            
            create_statistics(x[0], summary_csv)           
    
    summary_csv.close()

print("--------- START ------------")
loop_files()
print("--------- END ------------")
