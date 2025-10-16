"""
Audio Utilities Module
Helper functions for audio file operations
"""

import soundfile as sf
import numpy as np
from pathlib import Path
import os


class AudioUtils:
    """
    Utility class for audio file operations
    """
    
    @staticmethod
    def get_audio_duration(audio_path):
        """
        Get duration of audio file
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            float: Duration in seconds, or None if failed
        """
        try:
            info = sf.info(audio_path)
            return info.duration
        except Exception as e:
            print(f"❌ Error getting duration: {str(e)}")
            return None
    
    @staticmethod
    def get_audio_info(audio_path):
        """
        Get detailed audio file information
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            dict: Audio information
        """
        try:
            info = sf.info(audio_path)
            file_size = os.path.getsize(audio_path)
            
            return {
                'duration': info.duration,
                'sample_rate': info.samplerate,
                'channels': info.channels,
                'format': info.format,
                'subtype': info.subtype,
                'frames': info.frames,
                'file_size': file_size,
                'file_size_mb': file_size / (1024 * 1024)
            }
        except Exception as e:
            print(f"❌ Error getting audio info: {str(e)}")
            return None
    
    @staticmethod
    def convert_audio_format(input_path, output_path, output_format='wav'):
        """
        Convert audio file to different format
        
        Args:
            input_path: Path to input audio file
            output_path: Path for output file
            output_format: Target format (wav, mp3, ogg, etc.)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read audio data
            data, samplerate = sf.read(input_path)
            # Write in new format
            sf.write(output_path, data, samplerate)
            print(f"✅ Audio converted to {output_format}")
            return True
        except Exception as e:
            print(f"❌ Conversion failed: {str(e)}")
            return False
    
    @staticmethod
    def resample_audio(input_path, output_path, target_sample_rate=44100):
        """
        Resample audio to different sample rate
        
        Args:
            input_path: Path to input audio
            output_path: Path for output audio
            target_sample_rate: Target sample rate in Hz
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data, sample_rate = sf.read(input_path)
            
            if sample_rate == target_sample_rate:
                print(f"✅ Audio already at {target_sample_rate} Hz")
                return True
            
            # Resample using scipy
            from scipy import signal
            number_of_samples = round(len(data) * float(target_sample_rate) / sample_rate)
            resampled_data = signal.resample(data, number_of_samples)
            
            sf.write(output_path, resampled_data, target_sample_rate)
            print(f"✅ Audio resampled to {target_sample_rate} Hz")
            return True
            
        except Exception as e:
            print(f"❌ Resampling failed: {str(e)}")
            return False
    
    @staticmethod
    def convert_to_mono(input_path, output_path):
        """
        Convert stereo audio to mono
        
        Args:
            input_path: Path to input audio
            output_path: Path for output audio
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data, samplerate = sf.read(input_path)
            
            # Check if already mono
            if len(data.shape) == 1:
                print("✅ Audio already mono")
                sf.write(output_path, data, samplerate)
                return True
            
            # Convert to mono by averaging channels
            mono_data = np.mean(data, axis=1)
            sf.write(output_path, mono_data, samplerate)
            print("✅ Audio converted to mono")
            return True
            
        except Exception as e:
            print(f"❌ Mono conversion failed: {str(e)}")
            return False
    
    @staticmethod
    def trim_silence(input_path, output_path, silence_thresh=-50, min_silence_len=1000):
        """
        Trim silence from beginning and end of audio
        (Simplified version without pydub)
        
        Args:
            input_path: Path to input audio
            output_path: Path for output audio
            silence_thresh: Silence threshold (not used in simplified version)
            min_silence_len: Minimum silence length in ms (not used in simplified version)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data, samplerate = sf.read(input_path)
            
            # Simple threshold-based trimming
            threshold = 0.01  # Amplitude threshold
            
            # Find non-silent regions
            mask = np.abs(data) > threshold
            if len(data.shape) > 1:
                mask = np.any(mask, axis=1)
            
            nonzero_indices = np.where(mask)[0]
            
            if len(nonzero_indices) == 0:
                print("⚠️ No non-silent audio found")
                return False
            
            # Trim
            start = nonzero_indices[0]
            end = nonzero_indices[-1] + 1
            trimmed_data = data[start:end]
            
            sf.write(output_path, trimmed_data, samplerate)
            print(f"✅ Silence trimmed")
            return True
            
        except Exception as e:
            print(f"❌ Silence trimming failed: {str(e)}")
            return False
    
    @staticmethod
    def normalize_audio(input_path, output_path, target_dBFS=-20.0):
        """
        Normalize audio to target loudness
        (Simplified version)
        
        Args:
            input_path: Path to input audio
            output_path: Path for output audio
            target_dBFS: Target loudness (simplified to peak normalization)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data, samplerate = sf.read(input_path)
            
            # Peak normalization
            max_val = np.max(np.abs(data))
            if max_val > 0:
                normalized_data = data / max_val * 0.8  # Normalize to 80% to avoid clipping
            else:
                normalized_data = data
            
            sf.write(output_path, normalized_data, samplerate)
            print(f"✅ Audio normalized")
            return True
            
        except Exception as e:
            print(f"❌ Normalization failed: {str(e)}")
            return False
    
    @staticmethod
    def merge_audio_files(audio_files, output_path, crossfade=0):
        """
        Merge multiple audio files into one
        (Simplified version without crossfade)
        
        Args:
            audio_files: List of audio file paths
            output_path: Path for output audio
            crossfade: Crossfade duration (not implemented in simplified version)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not audio_files:
                print("⚠️ No audio files provided")
                return False
            
            # Read first file
            combined_data, samplerate = sf.read(audio_files[0])
            
            # Concatenate other files
            for audio_file in audio_files[1:]:
                data, sr = sf.read(audio_file)
                if sr != samplerate:
                    print(f"⚠️ Sample rate mismatch: {audio_file}")
                    continue
                combined_data = np.concatenate([combined_data, data])
            
            sf.write(output_path, combined_data, samplerate)
            print(f"✅ {len(audio_files)} audio files merged")
            return True
            
        except Exception as e:
            print(f"❌ Merging failed: {str(e)}")
            return False
    
    @staticmethod
    def extract_audio_segment(input_path, output_path, start_ms, end_ms):
        """
        Extract a segment from audio file
        
        Args:
            input_path: Path to input audio
            output_path: Path for output audio
            start_ms: Start time in milliseconds
            end_ms: End time in milliseconds
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data, samplerate = sf.read(input_path)
            
            # Convert ms to samples
            start_sample = int(start_ms * samplerate / 1000)
            end_sample = int(end_ms * samplerate / 1000)
            
            segment = data[start_sample:end_sample]
            sf.write(output_path, segment, samplerate)
            
            print(f"✅ Segment extracted: {start_ms}ms - {end_ms}ms")
            return True
            
        except Exception as e:
            print(f"❌ Extraction failed: {str(e)}")
            return False
    
    @staticmethod
    def change_speed(input_path, output_path, speed=1.0):
        """
        Change playback speed of audio using scipy
        
        Args:
            input_path: Path to input audio
            output_path: Path for output audio
            speed: Speed multiplier (e.g., 1.5 = 1.5x faster)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from scipy import signal
            
            data, samplerate = sf.read(input_path)
            
            # Resample to change speed
            num_samples = int(len(data) / speed)
            resampled_data = signal.resample(data, num_samples)
            
            sf.write(output_path, resampled_data, samplerate)
            print(f"✅ Speed changed to {speed}x")
            return True
            
        except Exception as e:
            print(f"❌ Speed change failed: {str(e)}")
            return False
    
    @staticmethod
    def get_audio_level_meter(audio_path, chunk_duration=0.1):
        """
        Get audio level meter data
        
        Args:
            audio_path: Path to audio file
            chunk_duration: Duration of each chunk in seconds
        
        Returns:
            list: List of audio levels over time (RMS values)
        """
        try:
            data, samplerate = sf.read(audio_path)
            chunk_samples = int(chunk_duration * samplerate)
            
            levels = []
            for i in range(0, len(data), chunk_samples):
                chunk = data[i:i+chunk_samples]
                rms = np.sqrt(np.mean(chunk**2))
                levels.append(float(rms))
            
            return levels
            
        except Exception as e:
            print(f"❌ Error getting audio levels: {str(e)}")
            return []
    
    @staticmethod
    def clean_temp_files(temp_dir, max_age_hours=24):
        """
        Clean old temporary audio files
        
        Args:
            temp_dir: Path to temporary directory
            max_age_hours: Maximum age in hours (default: 24)
        
        Returns:
            int: Number of files deleted
        """
        try:
            import time
            
            temp_path = Path(temp_dir)
            if not temp_path.exists():
                return 0
            
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            deleted_count = 0
            
            for file_path in temp_path.glob("*"):
                if file_path.is_file() and file_path.suffix in ['.wav', '.mp3', '.ogg']:
                    file_age = current_time - file_path.stat().st_mtime
                    
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        deleted_count += 1
            
            if deleted_count > 0:
                print(f"🗑️ Cleaned {deleted_count} old temporary files")
            
            return deleted_count
            
        except Exception as e:
            print(f"❌ Error cleaning temp files: {str(e)}")
            return 0
