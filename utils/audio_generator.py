"""
Audio Generator for Sensory Spectrum
Generates 10 MP3 files with color names using gTTS (Google Text-to-Speech)
"""

from gtts import gTTS
import os

def generate_audio_files():
    """Generate all 10 color audio files"""
    colors = [
        ("Red", 1),
        ("Green", 2),
        ("Blue", 3),
        ("Yellow", 4),
        ("Cyan", 5),
        ("Magenta", 6),
        ("Orange", 7),
        ("Purple", 8),
        ("White", 9),
        ("Black", 10)
    ]

    audio_dir = "audio_files"
    os.makedirs(audio_dir, exist_ok=True)

    for color_name, track_num in colors:
        try:
            print(f"Generating {track_num:04d}.mp3 - '{color_name}'...")
            tts = gTTS(text=color_name, lang='en', slow=False)
            filename = f"{track_num:04d}.mp3"
            filepath = os.path.join(audio_dir, filename)
            tts.save(filepath)
            print(f"✅ {filename} created!")
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")

    print("\n🎉 All 10 audio files ready!")
    print(f"📁 Copy '{audio_dir}/*.mp3' to SD card root (FAT32)")
    print("💡 Tip: Test files on computer first!")

if __name__ == "__main__":
    generate_audio_files()
