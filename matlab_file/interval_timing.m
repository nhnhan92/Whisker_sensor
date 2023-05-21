function [h, m, s] = interval_timing(time_interval)
    current_time = clock;
    if current_time(6) + time_interval >= 60
        current_time(5) = current_time(5) + 1;
        current_time(6) = current_time(6) + time_interval - 60;
        if current_time(5) >= 60
            current_time(4) = current_time(4) + 1;
            current_time(5) = 0;
        end
        h = current_time(4);
        m = current_time(5);
        s = current_time(6);
        return
    else
        h = current_time(4);
        m = current_time(5);
        s = current_time(6)+ time_interval;
        return
    end
end