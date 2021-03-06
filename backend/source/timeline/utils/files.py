import subprocess
from pathlib import Path


def generate_pdf_preview(input_path: Path, output_path: Path, max_dimensions: (int, int), overwrite=False):
    if output_path.exists() and not overwrite:
        raise FileExistsError

    try:
        command = [
            'convert',
            '-pointsize', '72',
            '-density', str(int(max_dimensions[0] / 8.5)),  # A4 pages are 8.5 inches wide
            '-units', 'PixelsPerInch',
            f"{str(input_path)}[0]",
            '-resize', f"{max_dimensions[0]}x{max_dimensions[1]}>",
            '-flatten',
            '-strip',
            str(output_path),
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as exc:
        command = " ".join(exc.cmd)
        raise Exception(
            f'Could not generate image preview.\n'
            f"IMAGEMAGICK COMMAND:\n{command}\n"
            f"IMAGEMAGICK OUTPUT:\n{exc.stderr.decode('UTF-8')}"
        )


class VideoDurationError(ValueError):
    pass


def generate_video_preview(input_path: Path, output_path: Path, video_duration: int, max_dimensions: (int, int),
                           overwrite=False):
    if output_path.exists() and not overwrite:
        raise FileExistsError

    if video_duration is None or video_duration == 0:
        raise VideoDurationError(
            f'Could not generate video preview. Video duration is {video_duration}.'
        )

    try:
        sample_count = 10
        sample_duration = 2
        if video_duration <= 10:
            sample_count = 1
            sample_duration = video_duration
        elif video_duration <= 30:
            sample_count = 5
            sample_duration = 1
        elif video_duration <= 5 * 60:
            sample_count = 5
            sample_duration = 2

        # Take a [sample_duration] video sample at every 1/[sample_count] of the video
        preview_intervals = [
            (sample_start, sample_start + sample_duration)
            for sample_start in [
                int(i / sample_count * video_duration)
                for i in range(0, sample_count)
            ]
        ]

        # Cut the sample
        ffmpeg_filter = " ".join(
            f"[0:v]trim={start}:{end},setpts=PTS-STARTPTS[v{index}];"
            for index, (start, end) in enumerate(preview_intervals)  # noqa
        )

        # Concatenate the samples
        ffmpeg_filter += "".join(
            f"[v{i}]" for i in range(0, len(preview_intervals))
        )
        ffmpeg_filter += f"concat=n={sample_count}:v=1[allclips];"

        # Scale the output to fit max size, but don't enlarge, don't crop, and don't change aspect ratio
        ffmpeg_filter += \
            f"[allclips]scale=ceil(iw*min(1\\,min({max_dimensions[0]}/iw\\,{max_dimensions[1]}/ih))/2)*2:-2[out]"

        command = [
            'ffmpeg',
            '-y',  # Overwrite if exists, without asking
            '-i', str(input_path),
            '-filter_complex', ffmpeg_filter,
            '-map', '[out]',
            '-codec:v', 'libx264',
            '-profile:v', 'baseline',
            '-level', '3.0',
            '-preset', 'slow',
            '-threads', '0',
            '-movflags', '+faststart',
            str(output_path),
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as exc:
        command = " ".join(exc.cmd)
        raise Exception(
            f'Could not generate video preview.\n'
            f"FFMPEG COMMAND:\n{command}\n"
            f"FFMPEG OUTPUT:\n{exc.stderr.decode('UTF-8')}"
        )


def generate_image_preview(input_path: Path, output_path: Path, max_dimensions: (int, int), overwrite=False):
    if output_path.exists() and not overwrite:
        raise FileExistsError

    try:
        command = [
            'convert',
            '-auto-orient',
            '-flatten',
            '-strip',
            '-thumbnail', f"{max_dimensions[0]}x{max_dimensions[1]}>",
            f"{str(input_path)}[0]",
            str(output_path),
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as exc:
        command = " ".join(exc.cmd)
        raise Exception(
            f'Could not generate image preview.\n'
            f"IMAGEMAGICK COMMAND:\n{command}\n"
            f"IMAGEMAGICK OUTPUT:\n{exc.stderr.decode('UTF-8')}"
        )
