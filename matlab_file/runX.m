function y = runX(speed,distance, flag)
COM = 'COM8';
delete(instrfind({'Port'},{COM}));
s =serial(COM,'BaudRate',19200,'Parity','none', 'DataBits',8, 'StopBits',1,'Terminator','CR');
fopen(s);
            
%%%%%%%%%%%%%%%%%%% Parameters X - axis %%%%%%%%%%%%%%%%%%%
fprintf(s,'axisX:memsw0 5');                % set origin move to the end of the motor
fprintf(s,'axisX:memsw1 0');                % set mechanical sensor input logic (Normal Close)
fprintf(s,'axisX:memsw2 0');                % set origin sensor input logic (Normal Close)
fprintf(s,'axisX:memsw3 0');                % set near origin sensor input logic (Normal Close)
fprintf(s,'axisX:memsw4 0');                % Current down control
fprintf(s,'axisX:memsw5 0');                % Set dividing direction
fprintf(s,'axisX:memsw6 0');                % set stop processing (Emergency) 
fprintf(s,'axisX:memsw7 0');                % Set Origin Return 0 Reset
fprintf(s,'axisX:lspeed0 100');              % set start up velocity
fprintf(s,'axisX:fspeed0 1000');            % set Driving speed
fprintf(s,'axisX:rate0 10');                % set acceleration and deceleration rate (unit: msec)
fprintf(s,'axisX:unit 2');                  % set unit of mm
fprintf(s,'axisX:standard 0.002');          % resolution of the motor: 1 mm/500 pulse
fprintf(s,'axisX:drdiv 0');                 % set dividing number


if flag == 1
    SpeedX = speed;
    DistanceX = distance;
    fprintf(s,'axisX:fspeed0 %s\n',int2str(SpeedX*500));  % set speed for table 0
    fprintf(s,'axisX:selsp 0');                              % select tablle speed 0

    pause(0.2);
    fprintf(s,'axisX:GOABSolute %.3f\n',DistanceX);
    fprintf(s,'axisX:MOTION?');
    motion_stt = fgetl(s);

    while(motion_stt=='1')                      % Check whether origin is done
        fprintf(s,'axisX:MOTION?');
%         pause(0.1);
        motion_stt = fgetl(s);
        
        fprintf(s,'axisX:POS?');
        current_pos = fgetl(s);
        a = ['X-axis: Current position = ', current_pos]; 
        disp(a);
    end  
    y = 1;
    return 
else
    fprintf(s,'axisX:fspeed1 2000');        % set speed for table 0
    fprintf(s,'axisX:selsp 1');
%     pause(1);
    fprintf(s,'axisX:go 2');
    fprintf(s,'axisX:origin?');             % Ask controller for oirigin command
    origin_stt = fgetl(s);
    
    while(origin_stt=='0')                      % Check whether origin is done
        fprintf(s,'axisX:origin?');
%         pause(0.1);
        origin_stt = fgetl(s);
                
    end
    disp('X-axis: Done returning to original position')
    %%% Set home and current position to 0 after origin motion %%%
    fprintf(s,'axisX:position 0');
    fprintf(s,'axisX:Homeposition 0');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     y = 1;
%     return 
% flushinput(COM);
fclose(s);
end
            
