#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""rt-claw Expression Window — display expression GIFs on Raspberry Pi desktop.

Requires: python3-tk python3-pil python3-pil.imagetk
Install:  sudo apt install python3-tk python3-pil python3-pil.imagetk
"""

import sys
import os
import socket
import threading
import argparse

_MISSING_DEPS = []

try:
    import tkinter as tk
except ImportError:
    _MISSING_DEPS.append("python3-tk")
    tk = None

try:
    from PIL import Image, ImageSequence
except ImportError:
    _MISSING_DEPS.append("python3-pil")
    Image = None
    ImageSequence = None

try:
    from PIL import ImageTk
except ImportError:
    _MISSING_DEPS.append("python3-pil.imagetk")
    ImageTk = None

try:
    from PIL.Image import Resampling
    LANCZOS = Resampling.LANCZOS
except (ImportError, AttributeError):
    try:
        LANCZOS = Image.LANCZOS
    except AttributeError:
        LANCZOS = None


class ExpressionWindow:
    def __init__(self, assets_dir, ipc_path, fullscreen=False):
        self.assets_dir = assets_dir
        self.ipc_path = ipc_path
        self.fullscreen = fullscreen
        self.current_expression = "idle"
        self.gif_frames = []
        self.frame_index = 0

        self.root = tk.Tk()
        self.root.title("rt-claw Expression")

        if fullscreen:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.geometry("320x240")

        self.label = tk.Label(self.root, bg='black')
        self.label.pack(expand=True, fill='both')

        self.load_expression("idle")

        self.animate()

        self.ipc_thread = threading.Thread(target=self.ipc_listener,
                                           daemon=True)
        self.ipc_thread.start()

    def load_expression(self, name):
        """Load GIF file for the named expression."""
        path = os.path.join(self.assets_dir, f"{name}.gif")
        if not os.path.exists(path):
            print(f"GIF not found: {path}")
            return False

        try:
            self.gif_image = Image.open(path)
            self.gif_frames = []

            for frame in ImageSequence.Iterator(self.gif_image):
                frame = frame.convert('RGBA')
                if self.fullscreen:
                    screen_w = self.root.winfo_screenwidth()
                    screen_h = self.root.winfo_screenheight()
                    frame = frame.resize((screen_w, screen_h), LANCZOS)
                else:
                    frame = frame.resize((320, 240), LANCZOS)

                self.gif_frames.append(ImageTk.PhotoImage(frame))

            self.frame_index = 0
            self.current_expression = name
            return True

        except Exception as e:
            print(f"Failed to load GIF: {e}")
            return False

    def animate(self):
        """Animate GIF frames."""
        if self.gif_frames:
            frame = self.gif_frames[self.frame_index]
            self.label.configure(image=frame)
            self.frame_index = (self.frame_index + 1) % len(self.gif_frames)

            delay = self.gif_image.info.get('duration', 100)
            self.root.after(delay, self.animate)

    def ipc_listener(self):
        """Listen on Unix domain socket for expression commands."""
        if os.path.exists(self.ipc_path):
            os.unlink(self.ipc_path)

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.ipc_path)
        sock.listen(5)
        os.chmod(self.ipc_path, 0o666)

        print(f"IPC listening on {self.ipc_path}")

        while True:
            try:
                conn, _ = sock.accept()
                with conn:
                    data = conn.recv(64).decode('utf-8').strip()
                    if data.startswith('set '):
                        expr = data[4:].strip()
                        print(f"Received command: set {expr}")
                        self.root.after(0,
                                        lambda e=expr: self.load_expression(e))
            except Exception as e:
                print(f"IPC error: {e}")

    def run(self):
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(
        description='rt-claw Expression Window')
    parser.add_argument('--assets', default='assets/expressions',
                        help='Path to expression GIF assets')
    parser.add_argument('--ipc', default='/run/rtclaw-expression.sock',
                        help='Unix domain socket path')
    parser.add_argument('--fullscreen', action='store_true',
                        help='Run in fullscreen mode')

    args = parser.parse_args()

    if not os.path.exists(args.assets):
        print(f"Assets directory not found: {args.assets}")
        sys.exit(1)

    window = ExpressionWindow(args.assets, args.ipc, args.fullscreen)
    window.run()


if __name__ == '__main__':
    main()
