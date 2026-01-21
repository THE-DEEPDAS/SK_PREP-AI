
import subprocess
import os
from typing import Optional

class AudioProcessor:
    """
    Process video files to extract audio for transcription
    Requires ffmpeg to be installed
    """
    
    @staticmethod
    def extract_audio(video_path: str, output_path: Optional[str] = None) -> str:
        """Extract audio from video file using ffmpeg"""
        
        if output_path is None:
            output_path = video_path.rsplit('.', 1)[0] + '.mp3'
        
        try:
            # Use ffmpeg to extract audio
            command = [
                'ffmpeg',
                '-i', video_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame',
                '-ar', '16000',  # 16kHz sample rate (good for speech)
                '-ac', '1',  # Mono
                '-ab', '64k',  # Bit rate
                output_path,
                '-y'  # Overwrite output file if exists
            ]
            
            subprocess.run(command, check=True, capture_output=True)
            return output_path
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr.decode()}")
        except FileNotFoundError:
            raise Exception("FFmpeg not found. Please install ffmpeg.")