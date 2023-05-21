function [y, timeElapsed] = runZ(speed,distance, flag)
COM = 'COM8';
delete(instrfind({'Port'},{COM}));
s =serial(COM,'BaudRate',19200,'Parity','none', 'DataBits',8, 'StopBits',1,'Terminator','CR');
fopen(s);
%%%%%%%%%%%%%%%%%%% Parameters Z - axis %%%%%%%%%%%%%%%%%%%
fprintf(s,'axisY:memsw0 5');                % set origin move to the end of the motor
fprintf(s,'axisY:memsw1 0');                % set mechanical sensor input logic (Normal Close)
fprintf(s,'axisY:memsw2 0');                % set origin sensor input logic (Normal Close)
fprintf(s,'axisY:memsw3 0');                % set near origin sensor input logic (Normal Close)
fprintf(s,'axisY:memsw4 0');                % Current down control
fprintf(s,'axisY:memsw5 0');                % Set dividing direction
fprintf(s,'axisY:memsw6 0');                % set stop processing (Emergency) 
fprintf(s,'axisY:memsw7 0');                % Set Origin Return 0 Reset
fprintf(s,'axisY:lspeed0 100');              % set start up velocity
fprintf(s,'axisY:fspeed0 1000');            % set Driving speed
fprintf(s,'axisY:rate0 10');                % set acceleration and deceleration rate (unit: msec)
fprintf(s,'axisY:unit 2');                  % set unit of mm
% fprintf(s,'axisY:standard 0.01');          % resolution of the motor: 4 mm/500 pulse
fprintf(s,'axisY:standard 0.004');          % resolution of the motor: 2 mm/500 pulse
fprintf(s,'axisY:drdiv 0');                 % set dividing number

if flag == 1
    tic
%     disp(fix(clock));
    SpeedX = speed;
    DistanceX = distance;
    fprintf(s,'axisY:fspeed0 %s\n',int2str(SpeedX*500));  % set speed for table 0
    fprintf(s,'axisY:selsp 0');                              % select tablle speed 0

    fprintf(s,'axisY:GOABSolute %.3f\n',DistanceX);
    fprintf(s,'axisY:MOTION?');
    motion_stt = fgetl(s);
    while(motion_stt=='1')                      % Check whether origin is done
        fprintf(s,'axisY:MOTION?');
        pause(0.1);
        motion_stt = fgetl(s);
        
        fprintf(s,'axisY:POS?');
%         current_pos = fgetl(s);
%         a = ['Z-axis: Target position = ', num2str(DistanceX), '; Z-axis: Current position = ', current_pos]; 
%         disp(a);
    end 
    timeElapsed = toc;
    disp(['EXECUTION TIME: ', num2str(timeElapsed)]);
%     disp(fix(clock));
    disp ('Z-axis: Arrived')
    y = 1;
    return 
else

    fprintf(s,'axisY:fspeed0 5000');        % set speed for table 0
    fprintf(s,'axisY:selsp 0');
    fprintf(s,'axisY:go 2');
    fprintf(s,'axisY:origin?');             % Ask controller for oirigin command
    origin_stt = fgetl(s);
    
    while(origin_stt=='0')                      % Check whether origin is done
        fprintf(s,'axisY:origin?');
%         pause(0.1);
        origin_stt = fgetl(s);
                
    end
    
%     disp('Z-axis: Done returning to original position')
    %%% Set home and current position to 0 after origin motion %%%
    fprintf(s,'axisY:position 0');
    fprintf(s,'axisY:Homeposition 0');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     y = 1;
%     return 
% flushinput(COM);
fclose(s);
end
            
