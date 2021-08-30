load('Somesh_12_8.50_15(5).mat');
x=Acceleration.X;
y=Acceleration.Y;
z=Acceleration.Z;
d=datenum(Acceleration.Timestamp);
out=d-d(1);
t=out*86400;
mag = sqrt(sum(x.^2 + y.^2 + z.^2, 2));

plot(t,mag);
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');

Nmag = mag - mean(mag);

plot(t,Nmag);
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');

minPeakHeight = std(Nmag); % constant * std(Nmag) where constant is a hyperparameter we change in the ablation study

[pks,locs] = findpeaks(Nmag,'MINPEAKHEIGHT',minPeakHeight); % [pks,locs] = findpeaks(Nmag,'MINPEAKHEIGHT',minPeakHeight, 'MinPeakProminence',1.5);

% MinPeakProminence and MinPeakheight are hyperparameters

steps=numel(pks);

hold on;
plot(t(locs), pks, 'r', 'Marker', 'v', 'LineStyle', 'none');
title('Counting Steps');
xlabel('Time (s)');
ylabel('Acceleration Magnitude, No Gravity (m/s^2)');
hold off

