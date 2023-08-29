clear all 
close all
% Example data for the bar graph
x = 1:5; % Group labels
group1_data = [10, 15, 12, 18, 20];
group1_std_dev = [2, 1, 3, 2, 1]; % Standard deviation for Group 1
group2_data = [8, 13, 11, 17, 19];
group2_std_dev = [1.5, 1.2, 2, 1.8, 1]; % Standard deviation for Group 2

% Set the bar width
bar_width = 0.3;

% Create the bar graph for Group 1
bar(x - bar_width/2, group1_data, bar_width, 'FaceColor', 'b');
hold on;

% Add error bars representing the standard deviation for Group 1
errorbar(x - bar_width/2, group1_data, group1_std_dev, 'k.', 'LineWidth', 1.5);

% Create the bar graph for Group 2
bar(x + bar_width/2, group2_data, bar_width, 'FaceColor', 'g');

% Add error bars representing the standard deviation for Group 2
errorbar(x + bar_width/2, group2_data, group2_std_dev, 'k.', 'LineWidth', 1.5);

hold off;

% Add labels and title
xlabel('Groups');
ylabel('Values');
title('Grouped Bar Graph with Standard Deviation');

% Add a legend
legend('Group 1', 'Group 1 Std. Dev.', 'Group 2', 'Group 2 Std. Dev.', 'Location', 'northwest');
