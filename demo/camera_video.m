
pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python39\python.exe';
%[ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion

%% Initialize Camera and Set Ready for Download Video
sdk = py.Open_LISA_SDK.SDK(pyargs('log_level',"DEBUG", 'default_response_format',"JSON"));

try 
    sdk.connect_through_TCP("127.0.0.1", "8080");
    json_instruments = sdk.get_instruments();
    instruments = jsondecode(char(json_instruments));
    fg_id = '1';
    ps_id = '2';
    os_id = '3';
    cam_id = '330355862202759620';
catch
    disp()
    disp(ME.message)
    sdk.disconnect()
end

IP_HEXA = "C0A8000A";
IP_INT = uint32(hex2dec(IP_HEXA));

% Init Library
cm = sprintf('init');
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);

% Detect Camera
cm = sprintf('detect_device %d',IP_INT);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);

DEVICE_CODE = out(2);
temp_DEVICE_NO = out(3);
DEVICE_INTERFACE = out(4);

% Open Device
cm = sprintf('open_device %d %d %d',DEVICE_CODE, temp_DEVICE_NO, DEVICE_INTERFACE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'open_device'));

DEVICE_CODE = out(2);
DEVICE_NO = out(3);

% Child No
cm = sprintf('get_exist_child_device_list %d',DEVICE_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', cm));
CHILD_NO = out(2);

% Set Record Rate
RECORD_RATE = 4000;
cm = sprintf('set_record_rate %d %d %d', DEVICE_NO, CHILD_NO, RECORD_RATE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_record_rate'));

% Set Shutter Speed
SHUTTER_SPEED = 8000;
cm = sprintf('set_shutter_speed_fps %d %d %d', DEVICE_NO, CHILD_NO, SHUTTER_SPEED);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_shutter_speed_fps'));

% Set Resolution
WIDTH = 1280;   HEIGHT = 512;
cm = sprintf('set_resolution %d %d %d %d', DEVICE_NO, CHILD_NO, WIDTH, HEIGHT);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_resolution'));

% Set Trigger
PDC_TRIGGER_START = 0;
cm = sprintf('set_trigger_mode %d %d %d %d %d', DEVICE_NO, PDC_TRIGGER_START, 0, 0, 0);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_trigger_mode'));

% Set LUT
PDC_LUT_DEFAULT4 = 4;
cm = sprintf('set_lut_mode %d %d %d', DEVICE_NO, CHILD_NO, PDC_LUT_DEFAULT4);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_lut_mode'));

% Set Output ports
PDC_EXT_OUT_TRIGGER_POSI = 5;
cm = sprintf('set_external_out_mode %d %d %d',DEVICE_NO, 1, PDC_EXT_OUT_TRIGGER_POSI);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_external_out_mode port 1'));

PDC_EXT_OUT_RECORD_POSI = 3;
cm = sprintf('set_external_out_mode %d %d %d', DEVICE_NO, 2, PDC_EXT_OUT_RECORD_POSI);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_external_out_mode port 2'));

% Reset status to LIVE
PDC_STATUS_LIVE = 0;
cm = sprintf('set_status %d %d', DEVICE_NO, PDC_STATUS_LIVE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'reset_status_live'));

% Set Camera Ready
RECORDING = false;
cm_trigger = sprintf('trigger_in %d', DEVICE_NO);
cm = sprintf('set_rec_ready %d', DEVICE_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_rec_ready'));

% Camera Trigger IN
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm_trigger));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'trigger_in'));

%% Set Playback Mode
PDC_STATUS_PLAYBACK = 1;
cm = sprintf('set_status %d %d', DEVICE_NO, PDC_STATUS_PLAYBACK);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_status playback'));

%% Get Record Rate 
cm = sprintf('get_record_rate %d %d', DEVICE_NO, CHILD_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: get_record_rate'));
RECORD_RATE = out(3)

%% Get Shutter Speed
cm = sprintf('get_shutter_speed_fps %d %d', DEVICE_NO, CHILD_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: get_shutter_speed_fps'));
SHUTTER_SPEED = out(3)

%% Download video from camera
PDC_MRAW_BITDEPTH_16 = 3;
PDC_MAX_FRAMES_NUM = 0;
SAVEDFRAMES    = 301;
cm = sprintf('download_mraw_video_from_camera %d %d %d %d %d',...
    DEVICE_NO, CHILD_NO, PDC_MRAW_BITDEPTH_16, PDC_MAX_FRAMES_NUM, SAVEDFRAMES);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm, 'command_result_output_file', "sandbox/videito.mraw"));

%% Set Live Status back
cm = sprintf('set_status %d %d', DEVICE_NO, PDC_STATUS_LIVE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'reset_status_live'));

%% Define variables to see video

mrawParam.TotalFrames = SAVEDFRAMES;
mrawParam.Width = WIDTH;
mrawParam.Height = HEIGHT;
mrawParam.FrameRate = RECORD_RATE;
mrawParam.Shutterfps = 8000;

save videito.mat mrawParam
