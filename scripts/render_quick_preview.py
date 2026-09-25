"""Render a small fixed-camera assembly preview; never modifies the saved model.
Run against a validated .blend in background Blender. Requires ffmpeg on PATH.
"""
import bpy
import shutil
import subprocess
import tempfile
from pathlib import Path

if not bpy.app.background:
    raise RuntimeError('Render in a separate background Blender process')
ffmpeg=shutil.which('ffmpeg')
if not ffmpeg:
    raise RuntimeError('ffmpeg must be installed and on PATH')
root=Path(__file__).resolve().parents[1]
s=bpy.context.scene
s.render.resolution_percentage=60
s.render.image_settings.file_format='PNG'
# Every third frame at 8 fps preserves the timing of the 24 fps master timeline.
with tempfile.TemporaryDirectory(prefix='coop-preview-') as scratch:
    for index,frame in enumerate(range(s.frame_start,s.frame_end+1,3)):
        s.frame_set(frame)
        s.render.filepath=str(Path(scratch)/f'{index:04d}.png')
        bpy.ops.render.render(write_still=True)
    subprocess.run([ffmpeg,'-y','-loglevel','error','-framerate','8','-i',str(Path(scratch)/'%04d.png'),
        '-c:v','libx264','-pix_fmt','yuv420p','-crf','23','-movflags','+faststart',str(root/'generated'/'construction-preview.mp4')],check=True)
print('COOP_PREVIEW_OK')
