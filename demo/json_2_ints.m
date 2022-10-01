function ints = json_2_ints(json_out)
    struct_out = jsondecode(char(json_out));
    encoded_value = struct_out.value;
    bytes = matlab.net.base64decode(encoded_value);
    ints = [];
    int_size = 4;
    for ii = 1:int_size:length(bytes)
        int_bytes = bytes(ii:ii+int_size-1);
        int_value = typecast(uint8(int_bytes), 'uint32');
        ints = [ints int_value];
    end
end