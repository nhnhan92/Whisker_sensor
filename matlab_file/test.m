a = fix(clock);
time_interval = 30;
current_time = fix(clock);
if current_time(6) + time_interval >= 60
    current_time(5) = current_time(5) + 1;
    current_time(6) = 0;
    if current_time(5) >= 60
        current_time(4) = current_time(4) + 1;
        current_time(5) = 0;
    end
disp(['current time = ', num2str(current_time(4)), ',', num2str(current_time(5)), ',', num2str(current_time(6))])
else
disp(['current time = ', num2str(current_time(4)), ',', num2str(current_time(5)), ',', num2str(current_time(6))])
end