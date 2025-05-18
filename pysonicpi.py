import argparse
from pathlib import Path
import librosa
import numpy as np
from tqdm import tqdm
import time

def log(msg):
    print(f"[+] {msg}")

# --- CLI setup ---
parser = argparse.ArgumentParser(description="Convert MP3 to Sonic Pi Ruby file")
parser.add_argument("mp3_path", type=str, help="Path to input MP3 file")
args = parser.parse_args()

mp3_file = Path(args.mp3_path)
if not mp3_file.exists() or mp3_file.suffix.lower() != ".mp3":
    raise FileNotFoundError(f"Invalid MP3 file: {mp3_file}")

rb_file = mp3_file.with_suffix(".rb")
log(f"Input MP3: {mp3_file}")
log(f"Output Ruby: {rb_file}")

# --- Load audio ---
log("Loading audio file...")
with tqdm(total=100, desc="Loading", unit="chunk") as pbar:
    y, sr = librosa.load(mp3_file, sr=None)
    pbar.update(100)
time.sleep(0.1)

# --- Extract tempo and beats ---
log("Estimating tempo and beats...")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
tempo_val = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
beat_times = librosa.frames_to_time(beats, sr=sr).round(3)
log(f"Detected tempo: {tempo_val:.2f} BPM")
log(f"Detected {len(beat_times)} beats")

# --- Estimate pitch contour ---
log("Estimating pitch (this may take a moment)...")
with tqdm(total=100, desc="Pitch Analysis", unit="step") as pbar:
    f0, voiced, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C6")
    )
    time.sleep(0.1)
    pbar.update(100)

notes = librosa.hz_to_note(f0[voiced]) if voiced.any() else []
log(f"Extracted {len(notes)} melodic notes")

# --- Write Sonic Pi code ---
log(f"Generating Sonic Pi script: {rb_file.name}")
with open(rb_file, "w") as f:
    f.write(f"use_bpm {tempo_val:.2f}\n\n")
    
    f.write("live_loop :beats do\n")
    for _ in beat_times:
        f.write("  sample :bd_haus\n  sleep 0.5\n")
    f.write("end\n\n")

    if len(notes) > 0:
        f.write("live_loop :melody do\n")
        for n in notes[:64]:  # limit to 64 notes
            f.write(f"  play :{n.lower()}, release: 0.2\n  sleep 0.25\n")
        f.write("end\n")
    else:
        f.write("# No pitch data extracted.\n")

log("✅ Done! Open the .rb file in Sonic Pi and press Run.")
