close all
clear 
clc

%% Experiment parameters
% Import Init pos 
init_pos_for = importfile('init_pos_for.xlsx');
init_pos_rev = importfile('init_pos_rev.xlsx');
init_pos_stra = importfile('init_pos_stra.xlsx');
pressure = 2;   % pressure * 10 kPa
mode = 'straigh';

if mode == 'forward' % the whisker bends toward the side of strain gauge
    init_posZ = init_pos_for(pressure,3);    % vi tri bat dau sweep truc Z - offset
    init_posX = init_pos_for(pressure,2);
    offset = init_pos_for(pressure,4);
elseif mode == 'reverse' % the whisker bends toward the opposite side of strain gauge
    init_posZ = init_pos_rev(pressure,3);    % vi tri bat dau sweep truc Z - offset
    init_posX = init_pos_rev(pressure,2);
    offset = init_pos_rev(pressure,4);
elseif mode == "straigh"
    init_posZ = init_pos_stra(pressure,3);    % vi tri bat dau sweep truc Z - offset
    init_posX = init_pos_stra(pressure,2);
    offset = init_pos_stra(pressure,4);
else
    init_posZ = 27.5;    % vi tri bat dau sweep truc Z - offset
    init_posX = 24.3;
    offset = 20;
end

% Fixed parameters
D_small_end = 9.83369;
fast_speed = 10;        % toc do cua linear 300mm
normal_speed = 4;       % toc do cua linear 15mm, 50mm

% Changable parameters
hour = 21;              % hour
min = 29;               % minute10
sc = 30;                % second, ***Note: luôn luôn ít h?n th?i gian trên DCS-100A 3 giây
No_repeat = 10;          % number of sweeping cycle (1 forward and 1 backward sweeping)
time_interval = 20;     % thoi gian doi sau moi lan sweep = trong DSC100A

%% Set up linear stage
% Z axis
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
%% Initialization
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
    
% return Z axis to origin   
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
    
disp('Z-axis: Done returning to original position')
%%% Set home and current position to 0 after origin motion %%%
fprintf(s,'axisY:position 0');
fprintf(s,'axisY:Homeposition 0');

%% Start
% Moving X to start position
SpeedX = normal_speed;
DistanceX = init_posX;
fprintf(s,'axisX:fspeed0 %s\n',int2str(SpeedX*500));  % set speed for table 0
fprintf(s,'axisX:selsp 0');                              % select tablle speed 0
pause(0.2);
fprintf(s,'axisX:GOABSolute %.3f\n',DistanceX);
fprintf(s,'axisX:MOTION?');
motion_stt = fgetl(s);

while(motion_stt=='1')                      % Check whether origin is done
    fprintf(s,'axisX:MOTION?');
    pause(0.1);
    motion_stt = fgetl(s);
end

% Moving Z to start position
SpeedZ = fast_speed;
DistanceX = init_posZ;
fprintf(s,'axisY:fspeed0 %s\n',int2str(SpeedZ*500));  % set speed for table 0
fprintf(s,'axisY:selsp 0');                              % select tablle speed 0

fprintf(s,'axisY:GOABSolute %.3f\n',DistanceX);
fprintf(s,'axisY:MOTION?');
motion_stt = fgetl(s);
    while(motion_stt=='1')                      % Check whether origin is done
        fprintf(s,'axisY:MOTION?');
        pause(0.1);
        motion_stt = fgetl(s);
    end 

%% Excution
% Check timing
timing(hour,min,sc);
count_cycle = 0;

tic
for i = 1:No_repeat
    % Forward
%     [~, exe_time] = runZ(fast_speed, init_posZ + 160 + offset*2+10,1);     % tong qua duong quet = length mau thu + offset*2 + diameter of whisker tip
    tic
    SpeedX = fast_speed;
    DistanceX = init_posZ + 183 + offset*2+D_small_end;
    fprintf(s,'axisY:fspeed0 %s\n',int2str(SpeedX*500));  % set speed for table 0
    fprintf(s,'axisY:selsp 0');                              % select tablle speed 0

    fprintf(s,'axisY:GOABSolute %.3f\n',DistanceX);
    fprintf(s,'axisY:MOTION?');
    motion_stt = fgetl(s);
    while(motion_stt=='1')                      % Check whether origin is done
        fprintf(s,'axisY:MOTION?');
%         pause(0.1);
        motion_stt = fgetl(s);
        fprintf(s,'axisY:POS?');
        current_pos = fgetl(s);
    end 
    timeElapsed = toc;
    disp(['EXECUTION TIME: ', num2str(timeElapsed)]);
%     disp ('Z-axis: Arrived')
    [interval_h, interval_m, interval_s] = interval_timing(time_interval-timeElapsed);
    disp(['Next time:', num2str(interval_h),':', num2str(interval_m),':', num2str(interval_s)]);
    timing(interval_h,interval_m,interval_s);

    % Backward
%     [~, exe_time] = runZ(fast_speed, init_posZ,1);
    
    tic
    SpeedX = fast_speed;
    DistanceX = init_posZ;
    fprintf(s,'axisY:fspeed0 %s\n',int2str(SpeedX*500));  % set speed for table 0
    fprintf(s,'axisY:selsp 0');                              % select tablle speed 0

    fprintf(s,'axisY:GOABSolute %.3f\n',DistanceX);
    fprintf(s,'axisY:MOTION?');
    motion_stt = fgetl(s);
    while(motion_stt=='1')                      % Check whether origin is done
        fprintf(s,'axisY:MOTION?');
%         pause(0.1);
        motion_stt = fgetl(s);
        fprintf(s,'axisY:POS?');
        current_pos = fgetl(s);
%         a = ['Z-axis: Target position = ', num2str(DistanceX), '; Z-axis: Current position = ', current_pos]; 
%         disp(a);
    end 
    timeElapsed = toc;
    disp(['EXECUTION TIME: ', num2str(timeElapsed)]);
%     disp ('Z-axis: Arrived')
       
    count_cycle = count_cycle + 1;
    disp(['Number of sweeping cycle done: ', num2str(count_cycle), '; Remaining: ', num2str(No_repeat - count_cycle)]);
    if count_cycle == No_repeat
        break
    else
        [interval_h, interval_m, interval_s] = interval_timing(time_interval-timeElapsed);
        disp(['Next time:', num2str(interval_h),':', num2str(interval_m),':', num2str(interval_s)]);
        timing(interval_h,interval_m,interval_s);
    end
    
end

%% Returning to origin
[interval_h, interval_m, interval_s] = interval_timing(5);
timing(interval_h,interval_m,interval_s);
runX(normal_speed,1,0);
runZ(fast_speed,1,0);

timeElapsed = toc;
disp(['EXECUTION TIME: ', num2str(timeElapsed)]);
