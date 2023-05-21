function timing(h, m, s)
    start_time = clock;
    if s < 59.5
        while start_time(4) ~= h || start_time(5) ~= m || s - start_time(6) >= 0.00001
            current_time = clock;
            start_time = current_time;
        end
    else
        while start_time(4) ~= h || start_time(5) == m || s - start_time(6) >= 59.50001
            current_time = clock;
            start_time = current_time;
        end
    end
end