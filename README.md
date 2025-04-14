# tsdl Tool

tsdl Tool is a cross‑platform command‑line utility designed to download and combine TS segments from an HLS playlist into a single MP4 (or other video container) file. It downloads each TS segment separately (avoiding issues with concatenated TS files and discontinuous timestamps) and then uses FFmpeg's concat demuxer to properly re‑mux the segments into a continuous video file.

## Features

- **Cross‑Platform Compatibility:**  
  Works on Windows, Linux, macOS, and Termux.
  
- **Smart TS Handling:**  
  Downloads individual TS segments instead of appending them directly, avoiding timestamp discontinuities during conversion.
  
- **Playlist Processing:**  
  Supports both master playlists (with resolution selection) and regular playlists.
  
- **Resume Capability:**  
  Maintains state during downloads so you can resume an interrupted session.
  
- **Optional Cleanup:**  
  Prompts you after conversion whether you want to delete the temporary TS files.
  
- **Output Extension Verification:**  
  Ensures your specified output file has a valid video extension (e.g. `.mp4`, `.mkv`, `.avi`, etc.).

## Repository Structure

ts-download/ 
            
        ├── LICENSE 
            
        ├── README.md           
            
        ├── tsdl                # Main script (executable Bash script) 
            
        └── install.py          # Cross‑platform installer script (Python)

## Requirements

- **FFmpeg:**  
  tsdl uses FFmpeg for concatenating the TS files into a final output. Make sure FFmpeg is installed and accessible in your PATH.

- **curl:**  
  Used to fetch playlist and segment data.

- **Bash:**  
  The tsdl script is written in Bash.  
  - On Windows, a Bash-like environment such as Git Bash or WSL is required.
  - On Termux (Android), Bash is available.

- **Python 3:**  
  The installer script (`install.py`) is written in Python 3 and is cross‑platform.

## Installation

There are two steps to install tsdl Tool:

### 1. Clone the Repository

Clone the repository using Git:

```sh
git clone https://github.com/ugo-studio/ts-download.git
cd ts-download
```

### 2. Run the Installer

The installer is cross‑platform. It detects if you're on Windows and handles installation differently from Unix‑like systems (Linux, macOS, Termux).

On Windows:

Ensure you have a Bash environment installed (e.g., Git Bash). Then run:

```sh
python install.py
```

This copies the tsdl script into a directory under %LOCALAPPDATA%\tsdl-tool and creates a wrapper batch file (tsdl.cmd) so you can invoke the tool from the command line. The installer will also attempt to update your PATH (via the registry) so that you can run tsdl from any terminal.

On Linux / macOS / Termux:

Make the installer executable if necessary and run:

```sh
./install.py
```

The script will check for the $PREFIX environment variable (useful for Termux) and fall back to /usr/local/bin if not defined. It then copies the tsdl script into the appropriate bin directory and sets its executable permission.

## Usage

Once installed, the tool can be run from any terminal or command prompt. For example:

```sh
tsdl https://example.com/path/to/playlist.m3u8 [output_file_path]
```

- **URL:** Provide the HLS playlist URL (or master playlist URL).

- **output_file_path (optional):** Specify the final video file’s output path. This path must end with a valid video extension such as .mp4, .mkv, .avi, .mov, or .flv. If not provided, the tool defaults to saving the video as ./downloads/output.mp4.


During the download process, the tool will display progress and allow you to resume downloads if interrupted. After combining the TS segments into the final video, you will be prompted whether to remove the temporary directory that held the TS files.

## Troubleshooting

- **FFmpeg Errors:**
Ensure that FFmpeg is installed and in your system PATH. Check the FFmpeg version if you encounter any conversion issues.

- *Permissions Issues (Linux/macOS/Termux):*
If the installer complains about permissions for the target directory, make sure you have the proper rights, or run the installer with sudo (if not in a Termux environment).

- *Windows PATH Update:*
If the installer could not automatically update your PATH, you may need to add the installation directory (e.g., %LOCALAPPDATA%\tsdl-tool) to your PATH manually.


## Contributing

Contributions, improvements, and bug reports are welcome!
Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
