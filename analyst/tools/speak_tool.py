"""
Custom speak tool implementation to work around registration issues.
"""

import subprocess
import os
import boto3
from typing import Optional
from strands import tool


@tool
def speak_custom(text: str, mode: str = "fast", voice_id: str = "Joanna", output_path: str = "speech_output.mp3", play_audio: bool = True) -> str:
    """
    Generate speech from text using either macOS say command (fast mode) or Amazon Polly (high quality mode).
    
    Args:
        text: The text to convert to speech
        mode: Speech mode - 'fast' for macOS say command or 'polly' for AWS Polly
        voice_id: The Polly voice ID to use (e.g., Joanna, Matthew) - only used in polly mode
        output_path: Path where to save the audio file (only for polly mode) 
        play_audio: Whether to play the audio through speakers after generation
        
    Returns:
        Status message about speech generation
    """
    
    if not text or not text.strip():
        return "Error: No text provided for speech generation"
        
    try:
        if mode == "fast":
            # Use macOS say command
            if play_audio:
                # Play directly through speakers
                result = subprocess.run(['say', text], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"✅ Successfully converted '{text}' to speech using macOS say command"
                else:
                    return f"❌ Error using say command: {result.stderr}"
            else:
                # Save to file without playing
                result = subprocess.run(['say', '-o', output_path, text], capture_output=True, text=True)
                if result.returncode == 0:
                    return f"✅ Successfully saved speech to '{output_path}' using macOS say command"
                else:
                    return f"❌ Error saving speech: {result.stderr}"
                    
        elif mode == "polly":
            # Use Amazon Polly
            try:
                polly = boto3.client('polly')
                
                # Generate speech
                response = polly.synthesize_speech(
                    Text=text,
                    OutputFormat='mp3',
                    VoiceId=voice_id
                )
                
                # Save audio file
                with open(output_path, 'wb') as file:
                    file.write(response['AudioStream'].read())
                
                result_msg = f"✅ Successfully generated speech using Amazon Polly (Voice: {voice_id})"
                result_msg += f"\n📁 Audio saved to: {output_path}"
                
                if play_audio:
                    # Try to play the audio file
                    try:
                        if os.system(f'afplay "{output_path}"') == 0:
                            result_msg += "\n🔊 Audio played successfully"
                        else:
                            result_msg += "\n⚠️  Audio file generated but playback failed"
                    except Exception as e:
                        result_msg += f"\n⚠️  Audio file generated but playback error: {e}"
                
                return result_msg
                
            except Exception as e:
                return f"❌ Error using Amazon Polly: {str(e)}"
                
        else:
            return f"❌ Invalid mode '{mode}'. Use 'fast' for macOS say or 'polly' for Amazon Polly"
            
    except Exception as e:
        return f"❌ Unexpected error in speech generation: {str(e)}"