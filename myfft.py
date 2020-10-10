import numpy as np
import time
import myfft_functions
import cv2
from numpy.random import rand
import math
import matplotlib.pyplot as plt


def forward_transform(matrix):
    """Computes the forward Fourier transform of the input matrix
    takes as input:
    matrix: a 2d matrix
    returns a complex matrix representing fourier transform"""

    ft = np.zeros(matrix.shape, dtype='complex_')
    N = matrix.shape[0]

    for u in range(matrix.shape[0]):
        for v in range(matrix.shape[1]):
            # print("\t\tU = ", u, " V = ", v)
            s = 0

            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    # print("i = ", i, " j = ", j)
                    cos = np.round(math.cos(((2 * math.pi) / N) * (u * i + v * j)), decimals=5)
                    sin = np.round(math.sin(((2 * math.pi) / N) * (u * i + v * j)), decimals=5)
                    s += matrix[i, j] * complex(cos, -sin)
                    # print(((2 * math.pi) / 2) * (u * i + v * j), cos, sin, s)

            ft[u, v] = s
            # print("[", u, ",", v, "]", ft[u, v])
        # print("\n")
    return ft


matrix_times = {"DFT": [], "FFT": [], "NumpyFFT": []}

for i in range(5, 55, 5):
    x = np.int_(rand(i, i) * 256)

    time_start = time.process_time()
    DFT = forward_transform(x)
    time_end_dft = time.process_time() - time_start
    matrix_times['DFT'].append(time_end_dft)

    time_start = time.process_time()
    X, m, n = myfft_functions.fft2(x)
    time_end_fft = time.process_time() - time_start
    matrix_times['FFT'].append(time_end_fft)

    time_start = time.process_time()
    np.fft.fft2(x)
    time_end = time.process_time() - time_start
    matrix_times['NumpyFFT'].append(time_end)
    print("\n -------------------- -------------------- -------------------- -------------------- --------------------")
    print("\nValue of N = ", i)
    print("\nDFT - ", time_end_dft)
    print("\nFFT - ", time_end_fft)
    print("\nNUMPY FFT - ", time_end)
    print("\nFFT is faster than DFT by ", time_end_dft / time_end_fft, " times.")
    print("\nNumpy FFT is faster than our implementation by ", time_end_fft / time_end, " times.\n")

print(matrix_times)

count = 1
for k, v in matrix_times.items():
    print(" N = ", count * 5)
    print("DFT - ", matrix_times['DFT'][count])
    print("FFT - ", matrix_times['FFT'][count])
    print("NumpyFFT", matrix_times['NumpyFFT'][count])
    count += 1

plt.plot([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], matrix_times['DFT'])
plt.plot([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], matrix_times['FFT'])
plt.plot([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], matrix_times['NumpyFFT'])

plt.show()
