#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

def install_windows():
    """
    Windows installer: assumes a Bash-like environment is available (e.g., Git Bash).
    Copies 'tsdl' to a folder under %LOCALAPPDATA% and creates a wrapper batch file (tsdl.cmd)
    so that the user can invoke the tool from the command line.
    """
    dest = os.path.join(os.environ.get("LOCALAPPDATA", os.getcwd()), "tsdl-tool")
    os.makedirs(dest, exist_ok=True)
    source = os.path.join(os.getcwd(), "tsdl")
    dest_script = os.path.join(dest, "tsdl")
    try:
        shutil.copyfile(source, dest_script)
        # On Windows, chmod is not strictly necessary but we call it anyway for Bash environments
        os.chmod(dest_script, 0o755)
        # Create a wrapper batch file to invoke Bash with the tsdl script.
        wrapper_path = os.path.join(dest, "tsdl.cmd")
        with open(wrapper_path, "w") as f:
            f.write(f'@echo off\r\nbash "{dest_script}" %*\r\n')
        print(f"tsdl installed into {dest}")
        # Attempt to add dest to user PATH via registry.
        try:
            import winreg
            reg_key = r'Environment'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_ALL_ACCESS) as envkey:
                try:
                    old_path, _ = winreg.QueryValueEx(envkey, "PATH")
                except FileNotFoundError:
                    old_path = ""
                if dest.lower() not in old_path.lower():
                    new_path = f"{old_path};{dest}" if old_path else dest
                    winreg.SetValueEx(envkey, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    print(f"Added {dest} to PATH. Restart your session for changes to take effect.")
        except Exception as e:
            print(f"Warning: Could not update PATH automatically: {e}")
    except Exception as e:
        print(f"Installation failed on Windows: {e}")

def install_unix():
    """
    Linux, macOS, Termux, etc.: Install 'tsdl' into a bin directory.
    First, try to use $PREFIX/bin if defined (useful for Termux), else default to /usr/local/bin.
    """
    # If $PREFIX is defined (as in Termux), use that. Otherwise, use /usr/local
    prefix = os.environ.get("PREFIX", "/usr/local")
    dest_dir = os.path.join(prefix, "bin")
    # Check write permission; if not writable and not in Termux, try sudo.
    if not os.access(dest_dir, os.W_OK):
        # For Termux, $PREFIX usually is writable.
        if "TERMUX_VERSION" in os.environ:
            # $PREFIX should be set; if not, fallback to ~/bin.
            dest_dir = os.path.expanduser("~/bin")
            os.makedirs(dest_dir, exist_ok=True)
        else:
            print(f"Insufficient permissions for {dest_dir}. Trying with sudo...")
            subprocess.call(["sudo", sys.executable, sys.argv[0]])
            sys.exit(0)
    os.makedirs(dest_dir, exist_ok=True)
    source = os.path.join(os.getcwd(), "tsdl")
    dest = os.path.join(dest_dir, "tsdl")
    try:
        shutil.copyfile(source, dest)
        os.chmod(dest, 0o755)
        print(f"tsdl successfully installed to {dest}")
    except Exception as e:
        print(f"Installation failed on Unix: {e}")

def main():
    if sys.platform.startswith("win"):
        install_windows()
    else:
        install_unix()

if __name__ == "__main__":
    main()
