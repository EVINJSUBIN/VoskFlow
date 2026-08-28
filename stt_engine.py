import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from faster_whisper import WhisperModel
import numpy as np
import re

class STTEngine:
    def __init__(self, model_size="base.en"):
        print(f"Loading Faster-Whisper model ({model_size})...")
        # We default to CPU with int8 for maximum hardware compatibility.
        # This can be upgraded to CUDA in the Model Manager settings later.
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print("Faster-Whisper model loaded successfully.")
        
    def filter_disfluencies(self, text):
        """
        Filters out common filler words and hesitation markers to produce a cleaner transcript.
        """
        # Common fillers (case insensitive, matching word boundaries)
        fillers = [
            r'\bumm+\b', 
            r'\buhh+\b', 
            r'\bhm+\b', 
            r'\buh\b',
            r'\bum\b',
            r'\bah+\b'
        ]
        
        filtered = text
        for filler in fillers:
            filtered = re.sub(filler, '', filtered, flags=re.IGNORECASE)
            
        # Clean up double spaces or floating punctuation left behind
        filtered = re.sub(r'\s+', ' ', filtered)
        filtered = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', filtered)
        
        return filtered.strip()

    def transcribe_audio(self, audio_data: np.ndarray):
        """
        Transcribes a normalized float32 numpy array of audio data.
        Returns the clean, punctuated, and capitalized text.
        """
        if len(audio_data) < 16000 * 0.1: # Skip if less than 100ms of audio
            return ""
            
        # beam_size=5 is a good balance between speed and accuracy
        # vad_filter=True prevents hallucinating on silence
        segments, info = self.model.transcribe(audio_data, beam_size=5, vad_filter=True)
        
        full_text = " ".join([segment.text for segment in segments])
        return self.filter_disfluencies(full_text)
