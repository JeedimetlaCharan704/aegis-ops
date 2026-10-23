"""High-Fidelity Automated Video Recorder with Smooth Human Mouse Cursor & Scrolling.

Navigates https://aegis-ops-livid.vercel.app/, injecting an animated visual cursor
overlay and executing human-like smooth mouse trajectories, hover pauses, and
gradual scrolling to produce a presentation-ready 1080p demo video.
"""

import os
import sys
import time
import math
import subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

CURRENT_MOUSE_POS = [960, 540]

def inject_virtual_cursor(page):
    """Inject an ultra-smooth glowing neon cursor overlay with click animations."""
    js_code = """
    (() => {
        if (document.getElementById('playwright-cursor')) return;
        
        const cursor = document.createElement('div');
        cursor.id = 'playwright-cursor';
        cursor.style.width = '24px';
        cursor.style.height = '24px';
        cursor.style.borderRadius = '50%';
        cursor.style.position = 'fixed';
        cursor.style.zIndex = '2147483647';
        cursor.style.pointerEvents = 'none';
        cursor.style.backgroundColor = 'rgba(0, 229, 255, 0.75)';
        cursor.style.border = '2px solid #ffffff';
        cursor.style.boxShadow = '0 0 14px #00e5ff, 0 0 4px #ffffff';
        cursor.style.transform = 'translate(-50%, -50%)';
        cursor.style.left = '960px';
        cursor.style.top = '540px';
        cursor.style.transition = 'width 0.15s ease, height 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease';
        document.body.appendChild(cursor);

        window.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });

        window.addEventListener('mousedown', () => {
            cursor.style.backgroundColor = 'rgba(239, 68, 68, 0.95)';
            cursor.style.boxShadow = '0 0 20px #ef4444, 0 0 6px #ffffff';
            cursor.style.width = '32px';
            cursor.style.height = '32px';
        });

        window.addEventListener('mouseup', () => {
            cursor.style.backgroundColor = 'rgba(0, 229, 255, 0.75)';
            cursor.style.boxShadow = '0 0 14px #00e5ff, 0 0 4px #ffffff';
            cursor.style.width = '24px';
            cursor.style.height = '24px';
        });
    })();
    """
    page.evaluate(js_code)

def smooth_move(page, target_x, target_y, steps=25, delay=0.015):
    """Interpolate human-like Bezier cursor movement."""
    global CURRENT_MOUSE_POS
    start_x, start_y = CURRENT_MOUSE_POS

    for i in range(1, steps + 1):
        t = i / steps
        # Smooth easeInOut quad curve
        t_smooth = 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t
        cur_x = start_x + (target_x - start_x) * t_smooth
        cur_y = start_y + (target_y - start_y) * t_smooth
        page.mouse.move(cur_x, cur_y)
        time.sleep(delay)

    CURRENT_MOUSE_POS = [target_x, target_y]

def smooth_click(page, selector, hover_time=0.4):
    """Move to element center smoothly, hover, and click with animation."""
    loc = page.locator(selector).first
    box = loc.bounding_box()
    if box:
        target_x = box["x"] + box["width"] / 2
        target_y = box["y"] + box["height"] / 2
        smooth_move(page, target_x, target_y, steps=28)
        time.sleep(hover_time)
        page.mouse.down()
        time.sleep(0.12)
        page.mouse.up()
        time.sleep(0.3)
    else:
        page.click(selector)

def smooth_scroll(page, delta_y, steps=20, delay=0.02):
    """Gradual mouse wheel scrolling."""
    step_delta = delta_y / steps
    for _ in range(steps):
        page.mouse.wheel(0, step_delta)
        time.sleep(delay)

def record():
    output_dir = os.path.abspath("recorded_video")
    os.makedirs(output_dir, exist_ok=True)

    print("[*] Launching Chromium (1920x1080) for High-Fidelity Recording...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=output_dir,
            record_video_size={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        url = "https://aegis-ops-livid.vercel.app/"
        print(f"[*] Loading live dashboard: {url}...")
        page.goto(url, wait_until="networkidle")
        inject_virtual_cursor(page)
        time.sleep(2)

        # -------------------------------------------------------------
        # SEGMENT 1 (0:00 - 0:25): Header & Overview
        # -------------------------------------------------------------
        print("[>] 0:00 - 0:25: Header & Overview...")
        smooth_move(page, 450, 60, steps=30)  # Move to logo
        time.sleep(4)
        smooth_move(page, 780, 60, steps=25)  # Hover over tags (#strands-decider-2b)
        time.sleep(5)
        smooth_move(page, 1150, 60, steps=25) # Status pill
        time.sleep(6)

        # -------------------------------------------------------------
        # SEGMENT 2 (0:25 - 0:50): Dual-Brain Architecture Showcase
        # -------------------------------------------------------------
        print("[>] 0:25 - 0:50: Showcasing Dual-Brain Cards...")
        smooth_scroll(page, 380, steps=25)
        time.sleep(2)
        inject_virtual_cursor(page)

        # Hover System 1 card (Decider 2B)
        smooth_move(page, 480, 620, steps=30)
        time.sleep(8)

        # Hover System 2 card (Amazon Bedrock)
        smooth_move(page, 1420, 620, steps=35)
        time.sleep(8)

        # Smooth scroll back up to Launchpad
        smooth_scroll(page, -380, steps=25)
        time.sleep(3)

        # -------------------------------------------------------------
        # SEGMENT 3 (0:50 - 1:25): Demo 1 - DDoS Traffic Surge & Auto-Remediation
        # -------------------------------------------------------------
        print("[>] 0:50 - 1:25: Demo 1 - DDoS Traffic Surge...")
        smooth_click(page, "button:has-text('DDoS Traffic Surge')")
        time.sleep(3)

        # Move to Run Dual-Brain Agent button and click
        smooth_click(page, "#runBtn")
        print("    Waiting for Decider 2B response...")
        time.sleep(4)

        # Move cursor to show metrics bar & Decider 2B verdict
        smooth_move(page, 280, 480, steps=25)  # Hover 77ms latency metric
        time.sleep(3)
        smooth_move(page, 1100, 480, steps=25) # Hover PROTECTED status
        time.sleep(3)

        # Scroll to Bedrock forensic post-mortem
        smooth_scroll(page, 320, steps=20)
        smooth_move(page, 1400, 750, steps=30) # Point to Bedrock report
        time.sleep(8)

        # Scroll back up to launchpad
        smooth_scroll(page, -320, steps=20)
        time.sleep(2)

        # -------------------------------------------------------------
        # SEGMENT 4 (1:25 - 1:55): Demo 2 - Adversarial Prompt Injection Defense
        # -------------------------------------------------------------
        print("[>] 1:25 - 1:55: Demo 2 - Adversarial Prompt Injection Defense...")
        smooth_click(page, "button:has-text('Adversarial Prompt Injection')")
        time.sleep(3)

        # Move and click Run Dual-Brain Agent
        smooth_click(page, "#runBtn")
        print("    Waiting for Decider 2B attack interception...")
        time.sleep(4)

        # Move cursor to highlight the ATTACK BLOCKED and DENY verdict
        smooth_move(page, 1100, 480, steps=25) # ATTACK BLOCKED badge
        time.sleep(4)
        smooth_scroll(page, 280, steps=15)
        smooth_move(page, 620, 680, steps=25)  # DENY (98% confidence)
        time.sleep(6)

        # Scroll back up
        smooth_scroll(page, -280, steps=15)
        time.sleep(2)

        # -------------------------------------------------------------
        # SEGMENT 5 (1:55 - 2:20): Demo 3 - High-Frequency Chaos Alert Storm
        # -------------------------------------------------------------
        print("[>] 1:55 - 2:20: Demo 3 - High-Frequency Chaos Alert Storm...")
        smooth_click(page, "#chaosBtn")
        time.sleep(3)

        # Smooth scroll to Chaos stats grid
        smooth_scroll(page, 450, steps=25)
        time.sleep(2)

        # Glide cursor across the Chaos stat cards
        smooth_move(page, 360, 680, steps=25)  # 50 Incidents
        time.sleep(3)
        smooth_move(page, 650, 680, steps=25)  # Decider duration (3.0s)
        time.sleep(3)
        smooth_move(page, 950, 680, steps=25)  # Throughput (16.4/s)
        time.sleep(3)
        smooth_move(page, 1250, 680, steps=25) # Attacks blocked (12)
        time.sleep(3)
        smooth_move(page, 1550, 680, steps=25) # Dollars saved ($1.50)
        time.sleep(4)

        # -------------------------------------------------------------
        # SEGMENT 6 (2:20 - 2:40): Demo 4 - Latency & Cost Benchmark Report
        # -------------------------------------------------------------
        print("[>] 2:20 - 2:40: Demo 4 - Benchmark Suite Table...")
        smooth_scroll(page, -450, steps=20)
        time.sleep(2)
        smooth_click(page, "#benchBtn")
        time.sleep(3)

        # Scroll to benchmark table
        smooth_scroll(page, 600, steps=25)
        time.sleep(2)

        # Glide cursor down the benchmark rows showing the 32x speedup
        smooth_move(page, 950, 700, steps=25)
        time.sleep(3)
        smooth_move(page, 950, 820, steps=25)
        time.sleep(4)

        # -------------------------------------------------------------
        # CLOSING (2:40 - 2:48): Smooth scroll back to top header
        # -------------------------------------------------------------
        print("[>] Closing: Scrolling back to top header...")
        smooth_scroll(page, -800, steps=30)
        smooth_move(page, 960, 200, steps=25)
        time.sleep(6)

        # Flush video
        page.close()
        video_path = page.video.path()
        context.close()
        browser.close()

    print(f"\n[+] Raw video recorded: {video_path}")
    
    # Convert to standard high-compatibility MP4 using imageio-ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    mp4_path = os.path.join(output_dir, "AegisOps_Demo_Walkthrough.mp4")
    print(f"[*] Encoding final 1080p MP4: {mp4_path}...")

    cmd = [ffmpeg, "-y", "-i", video_path, "-c:v", "libx264", "-preset", "medium", "-crf", "20", mp4_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        file_size_mb = os.path.getsize(mp4_path) / (1024 * 1024)
        print(f"[SUCCESS] High-Fidelity MP4 Video Created: {mp4_path} ({file_size_mb:.2f} MB)")
    else:
        print("[!] FFmpeg conversion failed. Raw WebM video available at:", video_path)

if __name__ == "__main__":
    record()
