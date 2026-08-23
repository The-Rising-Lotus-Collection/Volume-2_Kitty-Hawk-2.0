"""
=============================================================================
🪷 THE RISING LOTUS COLLECTION — VOLUME 2: KITTY HAWK 2.0
File: kitty_hawk_engine.py
Description: Vectorized Fast Fourier Transform (FFT) Audio Processing Loop
             with 3-6-9 Harmonic Alignment & 70.47 Hz Clock Synchronization
Target Platform: Edge AI Hardware Architectures (Python 3.11+)
=============================================================================
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional

# =============================================================================
# CRITICAL MANDATORY DESIGN NOTATION: VOICE-CONTROLLED PROPULSION
# =============================================================================
# The Kitty Hawk 2.0 propulsion system is controlled via human vocal resonance.
# The pilot's humming or vocalization is processed through a vectorized FFT loop,
# mapping pitch (120 Hz to 240 Hz) to throttle states.
#
# All processing loops honor the 70.47 Hz base clock (9 × 7.83 Hz Schumann)
# and the 3-6-9 harmonic constraints.
# =============================================================================

@dataclass
class PropulsionConfig:
    """Defines the 3-6-9 harmonic parameters for the propulsion control system."""
    base_clock_hz: float = 70.47          # 9 × 7.83 Hz Schumann sub-harmonic
    vocal_min_hz: float = 120.0           # Minimum vocal pitch (hover)
    vocal_max_hz: float = 240.0           # Maximum vocal pitch (boost)
    fft_window_size: int = 512            # FFT window size (512 = 2^9, honoring 3-6-9)
    sampling_rate: int = 8000             # Audio sampling rate
    clock_ticks_per_sample: float = 8000.0 / 70.47  # Samples per clock tick


def kh_process_acoustic_throttle(
    raw_audio_buffer: np.ndarray,
    sampling_rate: int = 8000,
    min_freq: float = 120.0,
    max_freq: float = 240.0
) -> Tuple[float, float, float]:
    """
    Executes a vectorized Fast Fourier Transform (FFT) loop to calculate throttle multipliers
    from human vocal resonance while ignoring external ambient cabin noise.
    
    Parameters:
        raw_audio_buffer (np.ndarray): Audio buffer from the cabin microphone array.
        sampling_rate (int): Audio sampling rate in Hz (default 8000 Hz).
        min_freq (float): Minimum vocal frequency for hover (120 Hz).
        max_freq (float): Maximum vocal frequency for boost (240 Hz).
    
    Returns:
        Tuple[float, float, float]: (vocal_frequency_hz, throttle_power, clock_alignment_factor)
            - vocal_frequency_hz: Detected pitch frequency
            - throttle_power: 0.0 (hover) to 1.0 (boost)
            - clock_alignment_factor: How well the detected frequency aligns with 3-6-9 harmonics
    """
    # 1. Compute the real-valued Fast Fourier Transform
    fft_magnitudes = np.abs(np.fft.rfft(raw_audio_buffer))
    fft_frequencies = np.fft.rfftfreq(len(raw_audio_buffer), d=1.0/sampling_rate)
    
    # 2. Isolate the target sub-harmonic human vocal tracking window (120 Hz to 240 Hz)
    vocal_window_indices = np.where((fft_frequencies >= min_freq) & (fft_frequencies <= max_freq))[0]
    
    if len(vocal_window_indices) == 0 or np.max(fft_magnitudes) < 1e-4:
        return 0.0, 0.0, 0.0  # No active vocal signal detected
    
    # 3. Identify the peak operating frequency component within the filtered window
    peak_window_index = np.argmax(fft_magnitudes[vocal_window_indices])
    kh_vocal_freq = fft_frequencies[vocal_window_indices[peak_window_index]]
    
    # 4. Map the identified pitch linearly across the propulsion states
    # min_freq (120 Hz) -> 0.0 (Base Hover)
    # max_freq (240 Hz) -> 1.0 (Maximum Boost Acceleration)
    kh_vocal_power = float((kh_vocal_freq - min_freq) / (max_freq - min_freq))
    kh_vocal_power = np.clip(kh_vocal_power, 0.0, 1.0)
    
    # 5. Calculate 3-6-9 harmonic alignment factor
    # Check if the detected frequency is a harmonic of the 70.47 Hz base clock
    clock_freq = 70.47
    harmonic_number = kh_vocal_freq / clock_freq
    nearest_harmonic = round(harmonic_number)
    alignment_error = abs(harmonic_number - nearest_harmonic)
    alignment_factor = max(0.0, 1.0 - alignment_error * 2.0)  # 0.0 to 1.0
    
    return float(kh_vocal_freq), kh_vocal_power, alignment_factor


def kh_map_throttle_to_mode(throttle_power: float) -> str:
    """
    Maps throttle power to one of four flight modes.
    
    Parameters:
        throttle_power (float): 0.0 to 1.0 throttle value.
    
    Returns:
        str: Flight mode name.
    """
    if throttle_power < 0.01:
        return "IDLE"
    elif throttle_power < 0.3:
        return "HOVER"
    elif throttle_power < 0.7:
        return "CRUISE"
    elif throttle_power < 0.95:
        return "BOOST"
    else:
        return "EMERGENCY_OVERRIDE"


def kh_get_system_config() -> PropulsionConfig:
    """
    Returns the complete 3-6-9 system configuration for the Kitty Hawk 2.0.
    
    Returns:
        PropulsionConfig: Dataclass with all system parameters.
    """
    return PropulsionConfig()


if __name__ == "__main__":
    print("AVIONICS_STATUS: Vectorized Cranial Acoustic FFT Throttle Module Initialized.")
    print("SYSTEM_CONFIG: Voice-Controlled Propulsion (120-240 Hz vocal tracking window)")
    print("CLOCK_BASE: 70.47 Hz (9 × 7.83 Hz Schumann sub-harmonic)")
    print("FFT_WINDOW: 512 samples (2^9, honoring 3-6-9 constraint)")
    
    # Simulate a live test with a synthesized vocal tone
    sample_rate = 8000
    duration_sec = 0.25
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    
    # Test tone at 180 Hz (mid-range Cruise mode)
    test_freq = 180.0
    test_audio = np.sin(2 * np.pi * test_freq * t) + 0.05 * np.random.randn(len(t))
    
    freq, power, alignment = kh_process_acoustic_throttle(test_audio, sample_rate)
    mode = kh_map_throttle_to_mode(power)
    
    print(f"TEST_RESULTS: Detected Frequency: {freq:.2f} Hz, Throttle: {power:.3f}, Mode: {mode}")
    print(f"HARMONIC_ALIGNMENT: {alignment:.3f} (1.0 = perfect 3-6-9 harmonic)")
