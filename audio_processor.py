import torch
import whisper
import tempfile
import numpy as np
import os
import subprocess
from typing import Optional
from analysis_prompt import AUDIO_ANALYSIS_PROMPT
from cv_processor import analyze_audio_with_granite

class AudioProcessor:
    def __init__(self, model_size: str = "base"):
        """Initialize with lazy loading"""
        self.model_size = model_size
        self._model = None  # Lazy load later
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_audio(self, audio_file) -> Optional[np.ndarray]:
        """Safely load audio from Streamlit UploadedFile"""
        try:
            # Create temp file with proper extension
            suffix = os.path.splitext(audio_file.name)[1]
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(audio_file.getbuffer())
                tmp_path = tmp.name
            
            # Load audio using Whisper's built-in loader
            audio = whisper.load_audio(tmp_path)
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            return audio
            
        except Exception as e:
            print(f"Audio loading failed: {str(e)}")
            return None


    @property
    def model(self):
        """Lazy load model when first needed"""
        if self._model is None:
            # Disable torch's class inspection during load
            torch._C._disable_class_wrapper = True
            try:
                self._model = whisper.load_model(self.model_size, device=self.device)
            finally:
                torch._C._disable_class_wrapper = False
        return self._model

    def convert_to_wav(self, input_path: str, output_path: str):
        """Convert any audio format to WAV using ffmpeg"""
        try:
            subprocess.run([
                "ffmpeg", "-i", input_path, "-ac", "1", "-ar", "16000",
                "-y", output_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Audio conversion failed: {e.stderr.decode()}")

    def _save_temp_audio(self, audio_file) -> Optional[str]:
        """Save uploaded audio to a properly named temp file"""
        try:
            # Get file extension
            ext = os.path.splitext(audio_file.name)[1].lower()
            if not ext:
                ext = ".mp3"  # default extension
            
            # Create temp file with proper extension
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                tmp.write(audio_file.getbuffer())
                return tmp.name
        except Exception as e:
            print(f"Temp file creation failed: {str(e)}")
            return None

    def transcribe(self, audio_file) -> Optional[str]:
        """Complete transcription pipeline with proper file handling"""
        temp_path = None
        try:
            # 1. Save to properly named temp file
            temp_path = self._save_temp_audio(audio_file)
            if not temp_path:
                return None
                
            # 2. Load audio using Whisper's loader
            audio = whisper.load_audio(temp_path)
            audio = whisper.pad_or_trim(audio)
            
            # 3. Process audio
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
            _, probs = self.model.detect_language(mel)
            lang = max(probs, key=probs.get)
            options = whisper.DecodingOptions(fp16=False)
            result = whisper.decode(self.model, mel, options)
            
            return result.text
            
        except Exception as e:
            print(f"Transcription failed: {str(e)}")
            return None
            
        finally:
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
                
               
    def process_audio(self, audio_file, job_category: str) -> Optional[dict]:
        """Full processing pipeline"""
        try:
            transcript = self.transcribe(audio_file)
            if not transcript.strip():
                raise ValueError("Empty transcription result")
                
            return analyze_audio_with_granite(transcript, AUDIO_ANALYSIS_PROMPT, job_category)
            
        except Exception as e:
            print(f"Audio processing error: {str(e)}")
            return None