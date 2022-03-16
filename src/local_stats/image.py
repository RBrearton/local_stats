"""
Stores the Image class, and its subclasses.
"""

from typing import Tuple

import numpy as np
import pywt


def _wavelet_freqs_below_length_scale(length_scale: int, wavelet_type: str):
    """
    Calculates the number of wavelet frequency scales that exist below the
    given length scale.
    """
    if wavelet_type != "sym4":
        raise NotImplementedError(
            "The only implemented wavelet choice is 'sym4'. If you would " +
            "like a different wavelet type, please raise an issue on the " +
            "local_stats github page.")
    # Wavelet length scales increase by powers of 2.
    return np.floor(np.log2(length_scale))


class Image:
    """
    The base class for all images.

    Attrs:
        image_array:
            Numpy array representing the image.
    """

    def __init__(self, image_array: np.ndarray) -> None:
        self.image_array = image_array

    def subtract_background(self, background_array: np.ndarray,
                            zero_clip=True) -> None:
        """
        Carried out a simple background subtraction on self.image_array. If
        zero_clip is true, then any pixels in image_array that are decreased
        below zero by the background subtraction will be clipped to zero. This
        is particularly useful if there's a hot pixel in your background array.

        Args:
            background_array:
                A numpy array representing the background to be subtracted.
            zero_clip:
                Boolean determining if the background subtracted image_array
                should be clipped at 0.
        """
        self.image_array -= background_array
        if zero_clip:
            self.image_array = np.clip(self.image_array, 0, np.inf)

    def wavelet_denoise(self,
                        signal_length_scale: 20,
                        cutoff_factor: float = 0.2,
                        max_cutoff_factor: float = 0.8,
                        wavelet_choice: str = "sym4") -> None:
        """
        Runs some wavelet denoising on the image. Without arguments, will run
        default denoising.

        Args:
            signal_length_scale:
                We would like to preferentially rotate our image away from
                wavelets whose length-scales are decently smaller than our
                signal length scale. This is the most important parameter for
                decimating noise wavelets. A value of 20 will kill most typical
                noise wavelets, but if your signal length scale is significantly
                larger than 20 pixels then it may be productive to increase this
                number.
            cutoff_factor:
                If any wavelet coefficient is less than cutoff_factor*(maximum
                wavelet coefficient), then set it to zero. The idea is that
                small coefficients are required to represent noise; meaningful
                data, as long as it is large compared to background, will
                require large coefficients to be constructed in the wavelet
                representation.
            max_cutoff_factor:
                The cutoff factor to be applied to signal occuring on length
                scales much smaller than signal_length_scale.
            wavelet_choice:
                Fairly arbitrary. Sym4 is the only currently supported wavelet.
                Look at http://wavelets.pybytes.com/ for more info. If you want
                a new wavelet supported, please feel free to raise an issue on
                the github page.
        """
        # Work out how many high frequency levels will have the max_cutoff
        # applied to them.
        max_noise_length = signal_length_scale/2
        max_cutoff_levels = _wavelet_freqs_below_length_scale(max_noise_length,
                                                              wavelet_choice)

        # Get the wavelet coefficients; cast them to a mutable type.
        coeffs = list(pywt.wavedec(self.image_array, wavelet_choice))
        # Work out the largest wavelet coefficient.
        max_coeff = 0
        for arr in coeffs:
            max_coeff = np.max(arr) if np.max(arr) > max_coeff else max_coeff

        # Get min_coeff from the arguments to this method.
        min_coeff = max_coeff*cutoff_factor
        high_freq_min_coeff = max_coeff*max_cutoff_factor

        for i in range(max_cutoff_levels):
            idx = -(i+1)
            coeffs[idx] = np.where(
                ((coeffs[idx] > high_freq_min_coeff).any() or
                 (coeffs[idx] < -high_freq_min_coeff).any()).any(),
                coeffs[idx], 0)

        # Apply the decimation.
        coeffs = [np.where(
            ((arr > min_coeff).any() or (arr < -min_coeff).any()).any(), arr, 0
        ) for arr in coeffs]

        # Invert the wavelet transformation.
        self.image_array = pywt.waverec(coeffs, wavelet_choice)


class DiffractionImage(Image):
    """
    A container for images obtained as a result of a diffraction experiment.
    """

    def __init__(self, image_array: np.ndarray,
                 beam_centre: Tuple[int]) -> None:
        super().__init__(image_array)
        self.beam_centre = beam_centre
