import pyaudio
import numpy as np
import threading

class AudioEngine:
    def __init__(self, volume_callback):
        self.volume_callback = volume_callback
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000 # Required sample rate for Whisper
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.thread = None
        
        # Audio buffer for streaming transcription
        self.frames = []

    def start(self):
        """Starts listening to the microphone, calculating volume, and buffering audio."""
        if self.is_recording: return
        self.is_recording = True
        self.frames = [] # Clear buffer on new recording
        
        try:
            self.stream = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
            
            self.thread = threading.Thread(target=self._record_loop, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f"Failed to open audio stream: {e}")
            self.is_recording = False

    def stop(self):
        """Stops the microphone stream."""
        self.is_recording = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
        self.volume_callback(0.0)

    def get_current_audio_float32(self):
        """
        Returns the entire currently buffered audio as a float32 numpy array 
        normalized between -1.0 and 1.0, which is the format Whisper expects.
        """
        if not self.frames:
            return np.array([], dtype=np.float32)
            
        # Combine all buffered chunks
        audio_data = np.hstack(self.frames)
        # Convert int16 to float32
        return audio_data.astype(np.float32) / 32768.0

    def _record_loop(self):
        """Background thread loop to read audio chunks, buffer them, and calculate volume."""
        while self.is_recording and self.stream and self.stream.is_active():
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                if len(audio_data) > 0:
                    # Buffer the audio for transcription
                    self.frames.append(audio_data)
                    
                    # Calculate Root Mean Square (RMS) for UI volume animation
                    rms = np.sqrt(np.mean(np.square(audio_data, dtype=np.float32)))
                    max_val = 4000.0 
                    normalized_volume = min(1.0, rms / max_val)
                    
                    self.volume_callback(normalized_volume)
            except Exception as e:
                print(f"Audio read error: {e}")
                break
