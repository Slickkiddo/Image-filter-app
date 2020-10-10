import numpy as np
import cv2
from datetime import datetime
import math
import os

def process_filter(image, filter):
    # Compute DFT
    DFT_image = np.fft.fft2(image)
    # Shift the DFT to center
    center_high_freq = np.fft.fftshift(DFT_image)
    # Apply log compression
    mag_fil_DFT = np.log(np.abs(center_high_freq))
    # Apply contrast stretch
    mag_fil_DFT = (255 * (mag_fil_DFT / np.max(mag_fil_DFT))).astype('uint8')

    # """filtered freq"""
    msk = filter
    # Shifted DFT * mask
    fil = center_high_freq * msk
    # Convolution theorem
    fil_out = mag_fil_DFT * msk

    # Inverse shift
    inv_shift = np.fft.ifftshift(fil)
    # Inverse DFT
    inv_dft = np.fft.ifft2(inv_shift)
    # Compute magnitudes
    fil_image = np.abs(inv_dft)

    # Send to post_process to compute contrast stretch
    final_image = post_process_image(fil_image)
    
#     save_path = '/output/'
#     name_of_file = raw_input("What is the name of the file: ")
#     completeName = os.path.join(save_path, name_of_file+".txt")         
    cv2.imwrite("filter_output_ideal_high2.jpg", final_image)
    return final_image


def post_process_image(image):
    """Post process the image to create a full contrast stretch of the image
    takes as input:
    image: the image obtained from the inverse fourier transform
    return an image with full contrast stretch
    -----------------------------------------------------
    1. Full contrast stretch (fsimage)
    2. take negative (255 - fsimage)
    """

    image = (image - np.min(image)) * (255 / (np.max(image) - np.min(image)))

    return image


def olympic(image, window_size):
    size = window_size // 2

    img = np.pad(image, (size, size), 'constant', constant_values=0)
    res = np.ones(image.shape) * 256

    for i in range(size, img.shape[0] - size):
        for j in range(size, img.shape[1] - size):
            # print(img[i, j])

            kernel = img[i - size:i + size + 1, j - size:j + size + 1]

            # print(kernel)

            kernel = np.reshape(kernel, window_size ** 2)
            kernel.sort()
            olympic_kernel = kernel[1:window_size * window_size - 1]
            mean = np.mean(olympic_kernel)

            # print(mean, "\n")
            res[i - size, j - size] = mean

    return res


def homo_filter(image, cutoff, order):
    a = 0.75
    b = 1.25
    # Take the image to log domain and then to frequency domain
    I_log = np.log1p(np.array(image, dtype="float"))
    I_fft = np.fft.fft2(I_log)

    P = image.shape[0] / 2
    Q = image[1] / 2
    U, V = np.meshgrid(range(image.shape[0]), range(image.shape[1]), sparse=False, indexing='ij')
    Duv = ((U - P) ** 2 + (V - Q) ** 2).astype(float)
    H = 1 / (1 + (Duv / cutoff ** 2) ** order)

    H = np.fft.fftshift(H)
    I_filtered = (a + b * H) * I_fft
    I_filt = np.fft.ifft2(I_filtered)
    image = np.exp(np.real(I_filt)) - 1

    image = (255 * (image / np.max(image))).astype('uint8')

    return np.uint8(image)


def get_ideal_low_pass_filter(shape, cutoff, order):
    """Computes a Ideal low pass mask
    takes as input:
    shape: the shape of the mask to be generated
    cutoff: the cutoff frequency of the ideal filter
    returns a ideal low pass mask"""
    
    print("ideal_low_pass_filter = ")
    print("cutoff: ",cutoff)
    print("order: ",order)
    
    filter = np.zeros(shape)

    D = 0

    for i in range(shape[0]):
        for j in range(shape[1]):

            D = np.sqrt((i - (shape[0] / 2)) ** 2 + (j - (shape[1] / 2)) ** 2)

            if D <= cutoff:
                filter[i, j] = 1
            else:
                filter[i, j] = 0

    # return filter
    return process_filter(image, filter)


def get_ideal_high_pass_filter(shape, cutoff, order):
    """Computes a Ideal high pass mask
    takes as input:
    shape: the shape of the mask to be generated
    cutoff: the cutoff frequency of the ideal filter
    returns a ideal high pass mask"""

    # Hint: May be one can use the low pass filter function to get a high pass mask
    print("ideal_high_pass_filter = ")
    print("cutoff: ",cutoff)
    print("order: ",order)
    filter = get_ideal_low_pass_filter(shape, cutoff, order)

    for i in range(shape[0]):
        for j in range(shape[1]):
            filter[i, j] = 1 - filter[i, j]

    # return filter
    return process_filter(image, filter)


def get_butterworth_low_pass_filter(shape, cutoff, order):
    """Computes a butterworth low pass mask
    takes as input:
    shape: the shape of the mask to be generated
    cutoff: the cutoff frequency of the butterworth filter
    order: the order of the butterworth filter
    returns a butterworth low pass mask"""
    
    
    print("butterworth_low_pass_filter = ")
    print("cutoff: ",cutoff)
    print("order: ",order)
    filter = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            D = np.sqrt((i - (shape[0] / 2)) ** 2 + (j - (shape[1] / 2)) ** 2)
            filter[i, j] = 1 / (1 + (D / cutoff) ** (2 * order))
    # print("\n\n\n\n")
    # print(filter)
    # return filter
    return process_filter(image, filter)


def get_butterworth_high_pass_filter(shape, cutoff, order):
    """Computes a butterworth high pass mask
    takes as input:
    shape: the shape of the mask to be generated
    cutoff: the cutoff frequency of the butterworth filter
    order: the order of the butterworth filter
    returns a butterworth high pass mask"""
    
    # Hint: May be one can use the low pass filter function to get a high pass mask
    print("butterworth_high_pass_filter = ")
    print("cutoff: ",cutoff)
    print("order: ",order)
    filter = get_butterworth_low_pass_filter(shape, cutoff, order)

    for i in range(shape[0]):
        for j in range(shape[1]):
            filter[i, j] = 1 - filter[i, j]

    # return filter
    return process_filter(image, filter)


def get_gaussian_low_pass_filter(shape, cutoff, order):
    """Computes a gaussian low pass mask
    takes as input:
    shape: the shape of the mask to be generated
    cutoff: the cutoff frequency of the gaussian filter (sigma)
    returns a gaussian low pass mask"""
    
    print("gaussian_low_pass_filter = ")
    print("cutoff: ",cutoff)
    print("order: ",order)
    filter = np.zeros(shape)

    for i in range(shape[0]):
        for j in range(shape[1]):
            D = np.sqrt((i - (shape[0] / 2)) ** 2 + (j - (shape[1] / 2)) ** 2)

            filter[i, j] = math.exp(-D ** 2 / (2 * (cutoff ** 2)))

    # return filter
    return process_filter(image, filter)


def get_gaussian_high_pass_filter(shape, cutoff, order):

    print("gaussian_high_pass_filter = ")
    print("cutoff: ",cutoff)
    print("order: ",order)
    # Hint: May be one can use the low pass filter function to get a high pass mask

    filter = get_gaussian_low_pass_filter(shape, cutoff, order)

    for i in range(shape[0]):
        for j in range(shape[1]):
            filter[i, j] = 1 - filter[i, j]

    # return filter
    return process_filter(image, filter)


def periodic_noise(image, n):
    divisions = image.shape[0] // n

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i // n) % 2 == 0:
                if image[i][j] + 50 < 255:
                    image[i][j] += 50
                else:
                    image[i][j] = 255
    return image

def PSNR(image, image_filtered):

    print("---------EXECUTING PSNR-------")
    MSE = 0
    # image = cv2.imread(r"output/Lenna0.jpg", 0)

    size = image.shape[0] * image.shape[1]

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            #         print("image- 1",image[i,j])
            #         print(image_new[i,j])
            MSE += (((image[i, j] - image_filtered[i, j]) ** 2) / size)
    print("MSE: ", MSE)
    R = 256
    PSNR = 10 * math.log10((R ** 2) / MSE)
    return PSNR


# image = cv2.imread("output/Lenna0.jpg", 0)
# image_fil = cv2.imread("output/filter_output_ideal_high.jpg", 0)
# psnr = PSNR(image, image_fil)
# print(psnr)


image = cv2.imread("/Users/shreyas/Downloads/Lenna0.jpg", 0)

# res = olympic(image, 3)
# cv2.imwrite("filter_output_olympic2.jpg", res)
#
# res = homomorphic_filter(image, 125, 2)
# cv2.imwrite("filter_output_homomorphic2.jpg", res)
#
# res = get_butterworth_high_pass_filter(image.shape, 125, 2)
# cv2.imwrite("filter_output_butterworth_high2.jpg", res)
#
# res = get_butterworth_low_pass_filter(image.shape, 75, 2)
# cv2.imwrite("filter_output_butterworth_low2.jpg", res)
#
# res = get_gaussian_high_pass_filter(image.shape, 125, 0)
# cv2.imwrite("filter_output_gaussian_high2.jpg", res)
#
# res = get_gaussian_low_pass_filter(image.shape, 75, 0)
# cv2.imwrite("filter_output_gaussian_low2.jpg", res)

res = get_ideal_high_pass_filter(image.shape, 50, 0)
cv2.imwrite("filter_output_ideal_high2.jpg", res)

# res = get_ideal_low_pass_filter(image.shape, 75, 0)
# cv2.imwrite("filter_output_ideal_low2.jpg", res)
#
# res = periodic_noise(image, 10)
# cv2.imwrite("noise2.jpg", res)