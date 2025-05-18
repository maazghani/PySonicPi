# pysonicpi

Turn any `.mp3` into a **live-codable** Sonic Pi script with one command.  
The Python helper analyzes tempo, beats, and melody, then writes a Ruby file you can open straight inside Sonic Pi.

---

## What’s Sonic Pi?

[Sonic Pi](https://sonic-pi.net/) is a free, open-source live-coding environment that lets you create and perform music in real time using Ruby. It runs on macOS, Windows, Linux—and even the Raspberry Pi.

---

## Quick start

```bash
# clone & set up
git clone https://github.com/yourname/pysonicpi.git
cd pysonicpi
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt        # librosa, soundfile, numpy, tqdm
```

Convert an MP3:

```bash
python pysonicpi.py path/to/song.mp3
```

1. Open **Sonic Pi**  
2. Paste or load `song.rb`  
3. Hit **Run** and tweak the synths / samples to taste.

---

## How it works

1. **Analysis (Python)**  
   - **librosa** – beat-tracking, tempo, pitch  
   - **spleeter** (optional) – stem separation for drums/bass/vocals  
2. **Generation** – writes a Ruby script using Sonic Pi’s DSL (`live_loop`, `play`, `sample`, etc.)  
3. **Playback** – Sonic Pi handles real-time scheduling and audio output.

---

## Options

| Flag                | Description                                   |
|---------------------|-----------------------------------------------|
| `-o, --out`         | Output filename (default: same as MP3, `.rb`) |
| `--quantise <sec>`  | Snap events to grid (e.g. `0.125` = 1/16 note)|
| `--humanise <ms>`   | Random timing jitter for a looser feel        |

---

## License

MIT
