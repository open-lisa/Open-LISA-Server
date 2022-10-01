function python_from_matlab_loop()
% Define the Python interpreter
clc
pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python39\python.exe';
% [ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion
py.print("Connecting with server")
%%
sdk = py.Open_LISA_SDK.SDK(pyargs('log_level',"DEBUG", 'default_response_format',"JSON"));
%%
% Waveform
%
wave2send.freq = 1250;
wave2send.Vpp = 9;
wave2send.n = 2000;
t = linspace(0, 1/wave2send.freq, wave2send.n);
wave2send.points = sin(2*pi*t);
%% Instruments Setup
% 
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
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Power Supply
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('\nConnecting to PS ... ');
out = sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', "idn"));
fprintf('Connected! \n %s', jsondecode(char(out)))
% Setup
%
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'volt_ch 1 1.0'));
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'curr_ch 1 0.0'));
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'volt_ch 2 1.0'));
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'curr_ch 2 0.0'));
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'output_ch 1 off'));
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'output_ch 2 off'));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Function Generator
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('\nConnecting to PS ... ');
out = sdk.send_command(pyargs(pyargs('instrument_id', fg_id, 'command_invocation', "idn")));
fprintf('Connected! \n %s', jsondecode(char(out)))
% Setup
%
DataStr = string(wave2send.points);
wave_id = sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', fprintf('download_wave %s', DataStr)));
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', fprintf('set_arb %s', wave_id)));
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', fprintf('set_volt %s', string(wave2send.Vpp))));
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', 'set_offset 0'));
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', fprintf('set_freq %s', string(wave2send.freq))));
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', 'set_output off'));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Oscilloscope
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('\nConnecting to OS ... ');
out = sdk.send_command(pyargs(pyargs('instrument_id', os_id, 'command_invocation', "idn")));
fprintf('Connected! \n %s', jsondecode(char(out)))
% Setup
%
os.settings.chs.on = [1 2];
os.settings.chs.probe = [1 10]; % the instrument is always displays the x10 factor
os.settings.chs.imped = [2 1]; % 1: 10MOhm Probe % 2: 50Ohm BNC cable
os.settings.chs.bwlimit = {'OFF', 'OFF'};
os.settings.chs.coupling = {'DC', 'DC'};
os.settings.chs.scale = {'5v', '500mv'}; % Must consider which channel has the x10 probe connected
os.settings.chs.offset = [0 0];
% % Timebase
% SCALE
os.settings.timebase.scale = '100us';
% HOR. TRIGGER OFFSET
os.settings.timebase.offset = 0;
% % ACQUIRE
% Mode
os.settings.acq.mode = 'SAMPLE';
% Deep Memory Length
os.settings.acq.mdep = '10M';
% % TRIGGER
% Type
os.settings.trig.type = 'SINGLE';
% Sweep
os.settings.trig.sweep = 'AUTO';
% Mode EDGE
os.settings.trig.mode = 'EDGE';
os.settings.trig.source = 'CH1';
os.settings.trig.coupling = 'DC';
os.settings.trig.slope = 'RISE';
os.settings.trig.level = 1; % +-5 (>0.02) 
% Holdoff
os.settings.trig.holdoff = '100ns';

% Reset, Stop and Display off
%
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', 'rst'));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', 'stop'));
for ch = 1:2
    cm = sprintf('set_ch %d off', ch);
    sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', cm));
end
% Acquire setup
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_acq_mode %s', os.settings.acq.mode)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_acq_memd %s', os.settings.acq.mdep)));
% Timebase setup
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_hor_scale %s', os.settings.timebase.scale)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_hor_offset %d', os.settings.timebase.offset)));
% Trigger
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_type %s', os.settings.trig.type)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_mode %s', os.settings.trig.mode)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_sour %s', os.settings.trig.source)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_slop %s', os.settings.trig.sloep)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_lev %s', os.settings.trig.level)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_coup %s', os.settings.trig.coupling)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_hold %s', os.settings.trig.hold)));
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_trig_edge_sweep %s', os.settings.trig.sweep)));
% Channels
for n = os.settings.chs.on
    sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_ch_bw %d %s', n, os.settings.chs.bwlimit{n})));
    sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_ch_coup %d %s', n, os.settings.chs.coupling{n})));
    sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_ch_scale %d %s', n, os.settings.chs.scale{n})));
    sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', fprintf('set_ch_disp %d %s', n, os.settings.chs.offset(n))));
end
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Camera
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% load constant values from PDCVALUE.h library
LIBDIR = fullfile('..', 'data', 'clibs', 'PHOTRON_CAMERA', 'Include');
if not(libisloaded('PDCVALUE'))
    loadlibrary('PDCVALUE', fullfile(LIBDIR,'PDCVALUE.h'), 'alias', 'lib')
end
%%
IP_HEXA = "C0A8000A";
IP_INT = uint32(hex2dec(IP_HEXA));
%%
% Init Library
cm = sprintf('init');
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
% assert(logical(ret), sprintf('Error in %s', cm));
%%
% Detect Camera
cm = sprintf('detect_device %d',IP_INT);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
%%
assert(logical(ret), sprintf('Error in %s', 'detect_device'));
%%
DEVICE_CODE = out(2);
temp_DEVICE_NO = out(3);
DEVICE_INTERFACE = out(4);
%%
% Open Device
cm = sprintf('open_device %d %d %d',DEVICE_CODE, temp_DEVICE_NO, DEVICE_INTERFACE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'open_device'));
%%
DEVICE_CODE = out(2);
DEVICE_NO = out(3);
%% Child No
cm = sprintf('get_exist_child_device_list %d',DEVICE_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', cm));
CHILD_NO = out(2);
%% Set Record Rate
RECORD_RATE = 4000;
cm = sprintf('set_record_rate %d %d %d', DEVICE_NO, CHILD_NO, RECORD_RATE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_record_rate'));
%% Set Shutter Speed
SHUTTER_SPEED = 8000;
cm = sprintf('set_shutter_speed_fps %d %d %d', DEVICE_NO, CHILD_NO, SHUTTER_SPEED);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_shutter_speed_fps'));
%% Set Resolution
WIDTH = 1280;   HEIGHT = 512;
cm = sprintf('set_resolution %d %d %d %d', DEVICE_NO, CHILD_NO, WIDTH, HEIGHT);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_resolution'));
%% Set Trigger
PDC_TRIGGER_START = 0;
cm = sprintf('set_trigger_mode %d %d %d %d %d', DEVICE_NO, PDC_TRIGGER_START, 0, 0, 0);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_trigger_mode'));
%% Set LUT
PDC_LUT_DEFAULT4 = 4;
cm = sprintf('set_lut_mode %d %d %d', DEVICE_NO, CHILD_NO, PDC_LUT_DEFAULT4);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_lut_mode'));
%% Set Output ports
PDC_EXT_OUT_TRIGGER_POSI = 5;
cm = sprintf('set_external_out_mode %d %d %d',DEVICE_NO, 1, PDC_EXT_OUT_TRIGGER_POSI);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_external_out_mode port 1'));
%%
PDC_EXT_OUT_RECORD_POSI = 3;
cm = sprintf('set_external_out_mode %d %d %d', DEVICE_NO, 2, PDC_EXT_OUT_RECORD_POSI);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_external_out_mode port 2'));
%% Reset status to LIVE
PDC_STATUS_LIVE = 0;
cm = sprintf('set_status %d %d', DEVICE_NO, PDC_STATUS_LIVE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'reset_status_live'));
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% DATA CAPTURE %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set Camera Ready
RECORDING = false;
cm_trigger = sprintf('trigger_in %d', DEVICE_NO);
cm = sprintf('set_rec_ready %d', DEVICE_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_rec_ready'));
%% FG ON
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', 'output on'));
pause(1.5)
%% Laser ON
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'output_ch 2 on'));
pause(0.5)
%% Oscilloscope ON
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', 'run'));
%% Camera Trigger IN
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm_trigger));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'trigger_in'));
%%
RECORDING = true;
cm = sprintf('get_status %d',DEVICE_NO);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'get_status'));
status = out(2);
%% Let the camera recording
while status == PDC_STATUS_REC
    cm = sprintf('get_status %d %d', DEVICE_NO, CHILD_NO);
    json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
    out = json_2_ints(json_out);  ret = out(1);
    assert(logical(ret), sprintf('Error in %s', 'get_status'));
    status = out(2);
end
RECORDING = false;
% Laser Off
sdk.send_command(pyargs('instrument_id', ps_id, 'command_invocation', 'output_ch 2 off'));
% FG Off
sdk.send_command(pyargs('instrument_id', fg_id, 'command_invocation', 'output off'));
% Oscilloscope stop
sdk.send_command(pyargs('instrument_id', os_id, 'command_invocation', 'stop'));
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% DATA SAVING %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Images
% Set Playback Mode
PDC_STATUS_PLAYBACK = 1;
cm = sprintf('set_status %d %d', DEVICE_NO, PDC_STATUS_PLAYBACK);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'set_status playback'));
%%
fileID = 'openlisa_video';
fileName = SaveFormatFile(sdk, cam_id, fileID, DEVICE_NO, CHILD_NO);

%% Set Live Status back
cm = sprintf('set_status %d %d', DEVICE_NO, PDC_STATUS_LIVE);
json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
out = json_2_ints(json_out);  ret = out(1);
assert(logical(ret), sprintf('Error in %s', 'reset_status_live'));

%
% Waveform




end
%% 
%%%%%%%%%%%%%%%%
% Functions
% %%%%%%%%%%%%%%%%
% function ints = json_2_ints(json_out)
%     struct_out = jsondecode(char(json_out));
%     encoded_value = struct_out.value;
%     bytes = matlab.net.base64decode(encoded_value);
%     ints = [];
%     int_size = 4;
%     for ii = 1:int_size:length(bytes)
%         int_bytes = bytes(ii:ii+int_size-1);
%         int_value = swapbytes(typecast(uint8(int_bytes), 'uint32'));
%         ints = [ints int_value];
%     end
% end
%
% function fileName = SaveFormatFile(sdk, cam_id, fileID, DEVICE_NO, CHILD_NO)
%     LIBDIR = fullfile('.', 'data', 'clibs', 'PHOTRON_CAMERA', 'Include');
%     if not(libisloaded('PDCVALUE'))
%         loadlibrary('PDCVALUE', 'PDCVALUE.h', 'alias', 'lib', 'includepath', LIBDIR)
%     end
%     fileName = [fileID '.mraw'];
%     file_path = fullfile(pwd, 'movies', fileName);
%     assert(fileName ~= 0, sprintf('Error in %s', 'SaveFormatFile: No FileName'));
%     % Get Mem Info
%     cm = sprintf('get_mem_frame_info %d %d',DEVICE_NO, CHILD_NO);
%     json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
%     out = json_2_ints(json_out);  ret = out(1);
%     assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: get_mem_frame_info'));
%     frameInfo = out(2);
%     startNo        = frameInfo.m_nStart;
%     recordedFrames = frameInfo.m_nRecordedFrames;
%     endNo          = frameInfo.m_nEnd;
%     SAVEDFRAMES    = 300;
%     % Get Record Rate 
%     cm = sprintf('get_record_rate %d %d', DEVICE_NO, CHILD_NO);
%     json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
%     out = json_2_ints(json_out);  ret = out(1);
%     assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: get_record_rate'));
%     record_rate = out(2)
%     % Open File
%     cm = sprintf('mraw_file_save_open %d %d %s %d %d', DEVICE_NO, CHILD_NO, file_path, PDC_MRAW_BITDEPTH_16, 0);
%     json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
%     out = json_2_ints(json_out);  ret = out(1);
%     assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: mraw_file_save_open'));
%     % Load Images to file
%     for i=1:SAVEDFRAMES+1
%         frameNo = startNo + int32(i - 1);
%         if frameNo < 0
%             frameNo = endNo + abs(startNo) + frameNo + int32(1);
%         end    
%         cm = sprintf('mraw_file_save %d %d %d', DEVICE_NO, CHILDE_NO, frameNo);
%         json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
%         out = json_2_ints(json_out);  ret = out(1);
%         if ret == PDC_FAILED
%             cm = sprintf('mraw_file_save_close %d %d', DEVICE_NO, CHILD_NO);
%             json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
%             out = json_2_ints(json_out);  ret = out(1);
%             error(2,'Error in %s', 'SaveFormatFile: mraw_file_save_open')
%         end
%     end
%     cm = sprintf('mraw_file_save_close %d %d', DEVICE_NO, CHILD_NO);
%     json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
%     out = json_2_ints(json_out);  ret = out(1);
% end