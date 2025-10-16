"""
Audio Recorder Module
Handles microphone recording functionality
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
from datetime import datetime
import queue
import threading


class AudioRecorder:
    """
    Audio recording class for capturing microphone input
    """
    
    def __init__(self, config):
        """
        Initialize AudioRecorder
        
        Args:
            config: Configuration object with audio settings
        """
        self.config = config
        self.sample_rate = config.SAMPLE_RATE
        self.channels = config.CHANNELS
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recorded_frames = []
        
        # Ensure temp directory exists
        self.temp_dir = Path(config.TEMP_DIR)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def _audio_callback(self, indata, frames, time, status):
        """
        Callback function for audio recording
        
        Args:
            indata: Input audio data
            frames: Number of frames
            time: Time info
            status: Status flags
        """
        if status:
            print(f"Recording status: {status}")
        
        if self.is_recording:
            self.audio_queue.put(indata.copy())
    
    def record_audio(self, duration=30, device=None):
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds (default: 30)
            device: Audio device index (default: None for system default)
        
        Returns:
            str: Path to saved audio file, or None if recording failed
        """
        try:
            print(f"🎤 Recording audio for {duration} seconds...")
            self.is_recording = True
            self.recorded_frames = []
            
            # Start recording
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback,
                device=device
            ):
                # Record for specified duration
                import time
                start_time = time.time()
                while time.time() - start_time < duration:
                    try:
                        frame = self.audio_queue.get(timeout=0.1)
                        self.recorded_frames.append(frame)
                    except queue.Empty:
                        continue
            
            self.is_recording = False
            
            # Combine all frames
            if not self.recorded_frames:
                print("❌ No audio data recorded!")
                return None
            
            audio_data = np.concatenate(self.recorded_frames, axis=0)
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            filepath = self.temp_dir / filename
            
            sf.write(filepath, audio_data, self.sample_rate)
            
            print(f"✅ Audio saved to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Recording error: {str(e)}")
            self.is_recording = False
            return None
    
    def record_with_callback(self, duration, progress_callback=None):
        """
        Record audio with progress callback
        
        Args:
            duration: Recording duration in seconds
            progress_callback: Function to call with progress updates
        
        Returns:
            str: Path to saved audio file
        """
        try:
            self.is_recording = True
            self.recorded_frames = []
            
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback
            ):
                import time
                start_time = time.time()
                
                while time.time() - start_time < duration:
                    try:
                        frame = self.audio_queue.get(timeout=0.1)
                        self.recorded_frames.append(frame)
                        
                        # Call progress callback
                        if progress_callback:
                            elapsed = time.time() - start_time
                            progress = min(elapsed / duration, 1.0)
                            progress_callback(progress)
                    except queue.Empty:
                        continue
            
            self.is_recording = False
            
            if not self.recorded_frames:
                return None
            
            audio_data = np.concatenate(self.recorded_frames, axis=0)
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            filepath = self.temp_dir / filename
            
            sf.write(filepath, audio_data, self.sample_rate)
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Recording error: {str(e)}")
            self.is_recording = False
            return None
    
    def stop_recording(self):
        """Stop ongoing recording"""
        self.is_recording = False
    
    def get_available_devices(self):
        """
        Get list of available audio input devices
        
        Returns:
            list: List of device dictionaries
        """
        try:
            devices = sd.query_devices()
            input_devices = []
            
            for idx, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append({
                        'index': idx,
                        'name': device['name'],
                        'channels': device['max_input_channels'],
                        'sample_rate': device['default_samplerate']
                    })
            
            return input_devices
        except Exception as e:
            print(f"❌ Error getting devices: {str(e)}")
            return []
    
    def test_microphone(self, duration=2):
        """
        Test microphone by recording a short sample
        
        Args:
            duration: Test duration in seconds (default: 2)
        
        Returns:
            bool: True if microphone works, False otherwise
        """
        try:
            print("🧪 Testing microphone...")
            test_audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32'
            )
            sd.wait()
            
            # Check if audio has any signal
            max_amplitude = np.max(np.abs(test_audio))
            
            if max_amplitude > 0.001:  # Threshold for detecting audio
                print(f"✅ Microphone working! Max amplitude: {max_amplitude:.4f}")
                return True
            else:
                print("⚠️ Microphone not detecting audio!")
                return False
                
        except Exception as e:
            print(f"❌ Microphone test failed: {str(e)}")
            return False
    
    def get_audio_level(self, duration=0.1):
        """
        Get current audio input level
        
        Args:
            duration: Measurement duration in seconds
        
        Returns:
            float: Audio level (0.0 to 1.0)
        """
        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32'
            )
            sd.wait()
            
            level = np.max(np.abs(audio))
            return min(level, 1.0)
            
        except Exception as e:
            print(f"❌ Error getting audio level: {str(e)}")
            return 0.0
