import json
import os
import datetime

##################################################
# Usage:
#
# This script expects to have "json" folder on current working directory.
# "json" folder should contain statistics json files
# This script will create a "csv" directory and one csv file per one json file.
# In addition, one summary csv file will be created.  
#
# Please note this was written in short period of time

##################################################
# Rules for the uptime calculations:
#
# bypass && on-air      = unexcusable downtime
# bypass && off-air     = excusable downtime
# no-bypass && on-air   = uptime
# no-bypass && off-air  = excusable downtime
 
def create_statistics(filename_json, summary_csv):
    with open('./json/' + filename_json + '.json', 'r') as f_json:
        try:
            data = json.load(f_json)
        except ValueError:
            print("Error in JSON loading")
            return
 
        if "assets" in data:
            assets = data["assets"]
        else:
            return    
        if "stats" in data:
            stats = data["stats"]
        else:
            return

        #game data        
        match_name = data["match_name"]          
        output_feed = data["output_feed"]
        file_start_time = data["file_start_time"]

    # create more meaningful output filename which contains information of the event and feed.
    filename = match_name + "_" + output_feed + "_" + filename_json
    filenumber = filename_json[0:6]
    
    #counters for statistics.
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

    unexcusable_downtime_counter = 0
    excusable_downtime_counter = 0
    uptime_counter = 0
    bypass_and_non_supponor_cam_counter = 0
    no_bypass_and_non_supponor_cam_counter = 0
    auto_zoom_and_supponor_cam_counter = 0
    
    #game_clock
    gc_period = 0
    gc_minute = 0
    gc_second = 0
    gc_stopped = 0

    #create CSV file for a single feed (for single json file).
    single_feed_csv = open("./csv/" + filename + ".csv", "w")

    single_feed_csv.write("time;renderer_bypass;integrator_bypass;auto_zoom;auto_tracking;tracer_manual_bypass;unknown_cam;period;gameclock_minute;gameclock_second;stopped\n")

    for stat in stats:
        #Flags are used for uptime calculation rules.
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
                #print('Renderer bypass at ', round(time), 's')
                renderer_bypass += 1
                renderer_bypass_flag = 1
                system_ok_flag = 0
               
            if "upstream_bypass" in _global[0]:
                #print('upstream_bypass at ', round(time), 's')
                upstream_bypass += 1
                upstream_bypass_flag = 1
                
                if "integrator" in _global[0]["upstream_bypass"]:
                    #print('Integrator bypass at ', round(time), 's')
                    integrator_bypass += 1    
                    integrator_bypass_flag = 1
                    system_ok_flag = 0
                    
                if "tracer" in _global[0]["upstream_bypass"]:
                    #print('tracer bypass at ', round(time), 's')
                    tracer_bypass += 1    
                    tracer_bypass_flag = 1
                
                    if "auto_tracking" in _global[0]["upstream_bypass"]["tracer"]:
                        #print('Tracer auto-tracking bypass at ', round(time), 's')
                        auto_tracking += 1
                        auto_tracking_flag = 1
                        system_ok_flag = 0
                        
                    if "not_present" in _global[0]["upstream_bypass"]["tracer"]:
                        #print('not_present at ', round(time), 's')
                        not_present += 1
                        not_present_flag = 1
                        
                    if "auto_zoom" in _global[0]["upstream_bypass"]["tracer"]:
                        #print('Tracer auto-zoom bypass at ', round(time), 's')
                        auto_zoom += 1
                        auto_zoom_flag = 1
                        
                    if "manual" in _global[0]["upstream_bypass"]["tracer"]:
                        #print('Tracer manual bypass at ', round(time), 's')
                        tracer_manual_bypass += 1
                        tracer_manual_bypass_flag = 1
                        system_ok_flag = 0
                    
            if "bypass_unknown_cam" in _global[0]:
                bypass_unknown_cam += 1
                bypass_unknown_cam_flag = 1
                
        if (system_ok_flag == 1):
            system_ok_counter += 1
            
        # bypass && on-air      = unexcusable_downtime_counter
        # zoom bypass && on-air = excusable_downtime_counter
        # bypass && off-air     = excusable_downtime_counter
        # no-bypass && on-air   = uptime_counter
        # no-bypass && off-air  = excusable_downtime_counter                

        # bypass && on-air      = unexcusable_downtime_counter            
        if (system_ok_flag == 0 and bypass_unknown_cam_flag == 0):
            unexcusable_downtime_counter += 1
            
        # zoom bypass && on-air = excusable_downtime_counter            
        elif (system_ok_flag == 1 and bypass_unknown_cam_flag == 0 and auto_zoom_flag == 1):
            excusable_downtime_counter += 1
            auto_zoom_and_supponor_cam_counter += 1
            
        # bypass && off-air     = excusable_downtime_counter
        elif (system_ok_flag == 0 and bypass_unknown_cam_flag == 1):
            excusable_downtime_counter += 1
            bypass_and_non_supponor_cam_counter += 1

        # no-bypass && on-air   = uptime_counter
        elif (system_ok_flag == 1 and bypass_unknown_cam_flag == 0):
            uptime_counter += 1
        
        # no-bypass && off-air  = excusable_downtime_counter                
        elif (system_ok_flag == 1 and bypass_unknown_cam_flag == 1):
            excusable_downtime_counter += 1
            no_bypass_and_non_supponor_cam_counter += 1

        #
        single_feed_csv.write(str(round(time)) + ";" + str(round(renderer_bypass_flag)) + ";" + str(integrator_bypass) + ";" + str(auto_zoom_flag) + ";" + str(auto_tracking_flag) + ";" + str(tracer_manual_bypass_flag) + ";" + str(bypass_unknown_cam_flag) + ";" + str(gc_period) + ";" + str(gc_minute) + ";" + str(gc_second) + ";" + str(gc_stopped) + "\n" )

    print('----------------') 
    #print('Processed file: ' + filename + '.json')   
    print('Match name ', match_name) 
    print('Output feed ', output_feed)   
    print('Recording start time ', file_start_time)           
         
    if (gameclock_counter > 0):
        print('Game clock detected')
    else:
        print('Game clock not detected')

    single_feed_csv.close()
    f_json.close()
                
    print("---------------------")
    
    #create summary CSV file
    summary_csv.write(match_name + ';' + output_feed + ';' + filename + ';' + str(round(time)) + ';' + str(bypass_and_non_supponor_cam_counter + no_bypass_and_non_supponor_cam_counter) + ';' + str(auto_zoom_and_supponor_cam_counter) + ';' + str(unexcusable_downtime_counter) + ';' + str(uptime_counter) + ';' + str(excusable_downtime_counter) + '\n')
    
def loop_files():
    
    #create summary CSV file for all feeds
    summary_csv = open("./csv/summary.csv", "w")    
    summary_csv.write("_match name; output feed; file name; total game seconds; supponor cam not on pgm; auto zoom and supponor cam on air; unexcusable downtime counter;  uptime counter; excusable downtime counter\n")    
    
    # assign directory
    directory = './json'
    
    ## iterate over files in
    ## that directory
    try:
        for filename in os.listdir(directory):
            f_dir = os.path.join(directory, filename)
            
            # checking if it is a file
            if os.path.isfile(f_dir):
                print('Process file:' + f_dir)
                x = filename.split(".")            
                create_statistics(x[0], summary_csv)           
    except OSError as error:
        print(error) 
        print("\nThis script expects to have 'json' folder, which contains the statistics json files.")
        print("please create 'json' folder, copy json files into it and rerun this script")
    summary_csv.close()

def create_output_dir(dir):
    # path 
    path = './'+dir
    # Create the directory 
 
    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error) 
        print("\nIf 'csv' folder already exists, continue and overwrite csv files in it...\n")

# run() is used for calling from another python file.  
def run():
    create_output_dir('csv')
    loop_files()    
    
run()
