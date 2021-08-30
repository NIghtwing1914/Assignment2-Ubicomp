load('Siddhi_13_9.34_16(1).mat');
tt=9.34;
x=Acceleration.X;
y=Acceleration.Y;
z=Acceleration.Z;

mag = sqrt(sum(x.^2 + y.^2 + z.^2, 2));
Nmag = mag - mean(mag);
fs=100;
[autocor,lags] = xcorr(Nmag,fs,'coeff');

plot(lags/fs,autocor);
xlabel('Lag')
ylabel('Autocorrelation');
axis([-21 21 -0.4 1.1])

[pksh,lcsh] = findpeaks(autocor);
short = mean(diff(lcsh))/fs;

[pklg,lclg] = findpeaks(autocor,'MinPeakDistance',ceil(short)*fs,'MinPeakheight',std(Nmag));
long = mean(lclg)/fs;

step_count=2*tt/long;



