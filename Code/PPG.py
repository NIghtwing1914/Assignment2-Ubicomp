import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from scipy.signal import butter,filtfilt

#Import the video
capture=cv.VideoCapture('Bhoomika_4.mp4')

fps = int(capture.get(cv.CAP_PROP_FPS)) #Get the FPS
frame_count = int(capture.get(cv. CAP_PROP_FRAME_COUNT))
duration = int(frame_count/fps)

print(fps)
print(frame_count)
print(duration)


signal=[]
i=0

while True:
    isTrue, frame= capture.read()  #Read the video frame by frame
    i+=1

    if(not isTrue or i>duration*fps):  #Limit to reading frames only before duration*fps seconds
        break
    # cv.imshow('Video',frame)

    # cv.waitKey()
    b,g,r=cv.split(frame)   #Split the frame into color channels
    mean_of_r_ch = r.mean()
    signal.append(mean_of_r_ch) #Create a signal array with mean values of pixels of red channel for every frame


signal = np.array(signal)
# print(np.shape(signal))
samples_to_skip = 1*fps
signal = signal[samples_to_skip:] #Skip the first second to avoid auto-exposure

to_plot = abs(signal-signal.mean())/ signal.std() #Normalize signal values


plt.subplot(4,1,1)
plt.plot(range(signal.shape[0]), to_plot)

plt.xlabel("Frames")
plt.ylabel("Normalized Signal")
plt.title("Normalized signal data(Mean of Red channel)")
# plt.legend()
plt.grid(linestyle='dashed',)


# Number of samples 
N = fps * (duration-1)

print(N)

yf = fft(to_plot)
xf = fftfreq(N, 1 / fps)

plt.subplot(4,1,2)
plt.plot(xf, np.abs(yf))
plt.xlabel("Frequencies")
plt.ylabel("Amplitude")
plt.title("FFT of Normalized Signal")
# plt.show()


# Creating a low pass filter

# Filter requirements

fs = 30.0       # sample rate, Hz
cutoff = 2.7      # desired cutoff frequency of the filter in Hz, slightly higher than actual 2.5
nyq = 0.5 * fs  # Nyquist Frequency
order = 2       

#Filtering
normal_cutoff = cutoff / nyq
# Get the filter coefficients 
b, a = butter(order, normal_cutoff, btype='low', analog=False)
y = filtfilt(b, a, to_plot)


plt.subplot(4,1,3)
plt.plot(range(y.shape[0]), y)
plt.xlabel("Frames")
plt.ylabel("Normalized Signal")
plt.title("After passing through low pass filter from FFT")

# plt.show()

#Finding peaks
peaks, _ = find_peaks(y, height=0.4,distance=10) #Here height and distance are hyperparamteres and need to be set at custom. For this experiment, based on observations, height=0.3 or 0.4

plt.subplot(4,1,4)
plt.plot(range(y.shape[0]), y)
plt.plot(peaks, y[peaks], "x")
plt.xlabel("Frames")
plt.ylabel("Normalized Signal")
plt.title("Peaks")

# plt.tight_layout(pad=0.5,h_pad=0.5,w_pad=0.5)
plt.subplots_adjust(left=0.110,
                    bottom=0.070, 
                    right=0.9, 
                    top=0.952, 
                    wspace=0.200, 
                    hspace=0.402)
plt.subplot_tool()

plt.show()


print(len(peaks))
print(60*len(peaks)/(duration-1)) #Estimated pulse rate


