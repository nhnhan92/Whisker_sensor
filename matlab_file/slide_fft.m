% X=[]; raw data (without wrinkle)

subplot(211)
Fs = 500;            % Sampling frequency
T = 1/Fs;             % Sampling period
L = 2501;             % Length of signal: length(X)
t = (0:L-1)*T;        % Time vector

Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
% figure
plot(f,P1,'r','LineWidth',2)
set(gca,'fontsize',18)
title('Slide without wrinkle')
xlabel('Frequency [Hz]')
ylabel('Voltage[V]')
grid on
% axis([0 50 0 0.5]); 

% Q=[]; raw data (with wrinkle)
subplot(212)
Fs = 500;            % Sampling frequency
T = 1/Fs;             % Sampling period
L = 3501;             % Length of signal Q
t = (0:L-1)*T;        % Time vector

Y = fft(Q);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
% figure
plot(f,P1,'b','LineWidth',2)
set(gca,'fontsize',18)
title('Slide with wrinkle')
xlabel('Frequency [Hz]')
ylabel('Voltage [V]')
grid on
% axis([0 50 0 0.5]);