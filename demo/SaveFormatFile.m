function fileName = SaveFormatFile(sdk, cam_id, fileID, DEVICE_NO, CHILD_NO)
%     LIBDIR = fullfile('.', 'data', 'clibs', 'PHOTRON_CAMERA', 'Include');
%     if not(libisloaded('PDCVALUE'))
%         loadlibrary('PDCVALUE', 'PDCVALUE.h', 'alias', 'lib', 'includepath', LIBDIR)
%     end
    fileName = [fileID '.mraw'];
    file_path = fullfile(pwd, 'movies', fileName);
%     assert(fileName ~= 0, sprintf('Error in %s', 'SaveFormatFile: No FileName'));
    %% Get Mem Info
    cm = sprintf('get_mem_frame_info %d %d',DEVICE_NO, CHILD_NO);
    json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
    out = json_2_ints(json_out);  ret = out(1);
    assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: get_mem_frame_info'));
    %%
    frameInfo = out(2);
    startNo        = out(3);
    recordedFrames = out(19);
    endNo          = out(4);
    SAVEDFRAMES    = 300;
    %% Get Record Rate 
    cm = sprintf('get_record_rate %d %d', DEVICE_NO, CHILD_NO);
    json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
    out = json_2_ints(json_out);  ret = out(1);
    assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: get_record_rate'));
    record_rate = out()
    %% Open File
    PDC_MRAW_BITDEPTH_16 = 3;
    cm = sprintf('mraw_file_save_open %d %d %d %d', DEVICE_NO, CHILD_NO, PDC_MRAW_BITDEPTH_16, 0);
    json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm, 'command_result_output_file', "sandbox/picture.mraw"));
    out = json_2_ints(json_out);  ret = out(1);
    assert(logical(ret), sprintf('Error in %s', 'SaveFormatFile: mraw_file_save_open'));
    % Load Images to file
    for i=1:SAVEDFRAMES+1
        frameNo = startNo + int32(i - 1);
        if frameNo < 0
            frameNo = endNo + abs(startNo) + frameNo + int32(1);
        end    
        cm = sprintf('mraw_file_save %d %d %d', DEVICE_NO, CHILDE_NO, frameNo);
        json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
        out = json_2_ints(json_out);  ret = out(1);
        if ret == PDC_FAILED
            cm = sprintf('mraw_file_save_close %d %d', DEVICE_NO, CHILD_NO);
            json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
            out = json_2_ints(json_out);  ret = out(1);
            error(2,'Error in %s', 'SaveFormatFile: mraw_file_save_open')
        end
    end
    cm = sprintf('mraw_file_save_close %d %d', DEVICE_NO, CHILD_NO);
    json_out = sdk.send_command(pyargs('instrument_id', cam_id, 'command_invocation', cm));
    out = json_2_ints(json_out);  ret = out(1);
end