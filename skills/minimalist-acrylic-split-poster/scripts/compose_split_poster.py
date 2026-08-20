#!/usr/bin/env python3
"""Compose one original photo and one styled artwork into a strict 3:4 poster.

The top half preserves the complete original image over a soft, blurred edge extension.
The bottom half contains the illustration and, optionally, an editorial typography footer.
FFmpeg performs all pixel processing so the script has no third-party Python dependency.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_WIDTH = 1536
PAPER_COLOR = "eee9dd"
TEXT_COLOR = "454943"
RULE_COLOR = "8e918a"
DEFAULT_TITLE_FONT = Path("/System/Library/Fonts/Supplemental/Didot.ttc")
DEFAULT_TEXT_FONT = Path("/System/Library/Fonts/PingFang.ttc")
DEFAULT_SCRIPT_FONT = Path("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc")
DEFAULT_NAIVE_FONT = Path("/System/Library/Fonts/MarkerFelt.ttc")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a strict 3:4, 50/50 photo-and-artwork split poster."
    )
    parser.add_argument("--top", required=True, type=Path, help="Original photograph")
    parser.add_argument("--bottom", required=True, type=Path, help="Generated illustration")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG/JPEG/WebP")
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="Output width; must be positive and divisible by 3 (default: 1536)",
    )
    parser.add_argument("--title", default="", help="Editorial poster title")
    parser.add_argument("--subtitle", default="", help="Optional centered subtitle")
    parser.add_argument("--left-meta", default="", help="Small lower-left metadata")
    parser.add_argument("--right-meta", default="", help="Small lower-right metadata")
    parser.add_argument("--kicker", default="", help="Small exhibition or series label")
    parser.add_argument("--vertical-label", default="", help="Rotated field-note label")
    parser.add_argument("--archive-label", default="", help="Small lower archive label")
    parser.add_argument(
        "--type-layout",
        choices=(
            "footer-center",
            "panel-top-left",
            "field-note",
            "sketchbook",
            "naive-editorial",
        ),
        default="footer-center",
        help=(
            "Typography system: centered footer, panel top-left, field note, "
            "sketchbook, or naive editorial"
        ),
    )
    parser.add_argument(
        "--top-grain",
        type=int,
        default=0,
        help="Subtle film grain strength on the upper photograph, from 0 to 8",
    )
    parser.add_argument(
        "--footer-ratio",
        type=float,
        default=0.18,
        help="Share of the lower half reserved for typography when --title is set",
    )
    parser.add_argument(
        "--title-font",
        type=Path,
        default=DEFAULT_TITLE_FONT,
        help="Title font file; defaults to macOS Didot",
    )
    parser.add_argument(
        "--text-font",
        type=Path,
        default=DEFAULT_TEXT_FONT,
        help="Subtitle/meta font file; defaults to macOS PingFang",
    )
    parser.add_argument(
        "--script-font",
        type=Path,
        default=DEFAULT_SCRIPT_FONT,
        help="Handwritten title font; defaults to macOS Snell Roundhand",
    )
    parser.add_argument(
        "--naive-font",
        type=Path,
        default=DEFAULT_NAIVE_FONT,
        help="Naive editorial title font; defaults to macOS Marker Felt",
    )
    return parser.parse_args()


def require_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise SystemExit(f"{label} does not exist or is not a file: {resolved}")
    return resolved


def escape_drawtext(value: str) -> str:
    """Escape text for FFmpeg drawtext with expansion disabled."""
    return (
        value.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace(":", "\\:")
        .replace("%", "\\%")
        .replace("\n", " ")
        .strip()
    )


def tracked_title(value: str) -> str:
    """Add restrained editorial tracking to Latin uppercase titles."""
    cleaned = " ".join(value.split())
    if cleaned and cleaned.isascii():
        return "   ".join(" ".join(word) for word in cleaned.upper().split())
    return cleaned


def main() -> int:
    args = parse_args()
    top = require_file(args.top, "Top image")
    bottom = require_file(args.bottom, "Bottom image")
    output = args.output.expanduser().resolve()

    if args.width <= 0 or args.width % 3 != 0:
        raise SystemExit("--width must be a positive integer divisible by 3")
    if not 0 <= args.top_grain <= 8:
        raise SystemExit("--top-grain must be between 0 and 8")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg was not found on PATH")

    width = args.width
    height = width * 4 // 3
    if height % 2:
        raise SystemExit("Calculated height must be even")
    half_height = height // 2
    output.parent.mkdir(parents=True, exist_ok=True)

    title_source = (
        args.title
        if args.type_layout in {"sketchbook", "naive-editorial"}
        else tracked_title(args.title)
    )
    title = escape_drawtext(title_source)
    subtitle = escape_drawtext(args.subtitle)
    left_meta = escape_drawtext(args.left_meta)
    right_meta = escape_drawtext(args.right_meta)
    kicker = escape_drawtext(tracked_title(args.kicker))
    vertical_label = escape_drawtext(tracked_title(args.vertical_label))
    archive_label = escape_drawtext(tracked_title(args.archive_label))
    typography_enabled = bool(title)

    if (
        typography_enabled
        and args.type_layout == "footer-center"
        and not 0.12 <= args.footer_ratio <= 0.30
    ):
        raise SystemExit("--footer-ratio must be between 0.12 and 0.30")

    title_font = args.title_font.expanduser().resolve()
    text_font = args.text_font.expanduser().resolve()
    script_font = args.script_font.expanduser().resolve()
    naive_font = args.naive_font.expanduser().resolve()
    if typography_enabled:
        require_file(title_font, "Title font")
        require_file(text_font, "Text font")
        if args.type_layout == "sketchbook":
            require_file(script_font, "Script font")
        if args.type_layout == "naive-editorial":
            require_file(naive_font, "Naive editorial font")

    footer_height = (
        round(half_height * args.footer_ratio)
        if typography_enabled and args.type_layout == "footer-center"
        else 0
    )
    art_height = half_height - footer_height

    # Keep the original photo intact in the foreground. Only the background extension is
    # enlarged/cropped/blurred, which avoids stretching or discarding the photographed subject.
    if args.type_layout == "field-note":
        filters = "[0:v]split=3[top_bg_src][top_fg_src][inset_src];"
    else:
        filters = "[0:v]split=2[top_bg_src][top_fg_src];"

    filters += (
        f"[top_bg_src]scale={width}:{half_height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{half_height},gblur=sigma=36,"
        "eq=contrast=1.025:brightness=0.004:saturation=0.96[top_bg];"
        f"[top_fg_src]scale={width}:{half_height}:force_original_aspect_ratio=decrease,"
        "eq=contrast=1.025:brightness=0.004:saturation=0.96[top_fg];"
        "[top_bg][top_fg]overlay=(W-w)/2:(H-h)/2:format=auto,setsar=1[top_base];"
    )

    if args.top_grain:
        filters += f"[top_base]noise=alls={args.top_grain}:allf=u[top];"
    else:
        filters += "[top_base]null[top];"

    if args.type_layout == "field-note":
        art_box_width = round(width * 0.70)
        art_box_height = round(half_height * 0.84)
        art_x = width - art_box_width - round(22 * width / DEFAULT_WIDTH)
        art_y = round(70 * width / DEFAULT_WIDTH)
        inset_width = round(300 * width / DEFAULT_WIDTH)
        inset_height = round(210 * width / DEFAULT_WIDTH)
        inset_x = round(68 * width / DEFAULT_WIDTH)
        inset_y = round(706 * width / DEFAULT_WIDTH)
        frame_pad = max(5, round(8 * width / DEFAULT_WIDTH))

        filters += (
            f"color=c=0x{PAPER_COLOR}:s={width}x{half_height}[paper];"
            f"[1:v]scale={art_box_width}:{art_box_height}:"
            "force_original_aspect_ratio=decrease,setsar=1[bottom_fg];"
            f"[paper][bottom_fg]overlay={art_x}+({art_box_width}-w)/2:"
            f"{art_y}+({art_box_height}-h)/2:format=auto[bottom_art];"
            f"[inset_src]scale={inset_width}:{inset_height}:"
            "force_original_aspect_ratio=decrease,"
            f"pad={inset_width}:{inset_height}:(ow-iw)/2:(oh-ih)/2:color=0x{PAPER_COLOR},"
            "setsar=1[inset];"
            f"[bottom_art]drawbox=x={inset_x-frame_pad}:y={inset_y-frame_pad}:"
            f"w={inset_width+2*frame_pad}:h={inset_height+2*frame_pad}:"
            f"color=0x{RULE_COLOR}@0.55:t=1[bottom_frame];"
            f"[bottom_frame][inset]overlay={inset_x}:{inset_y}:format=auto,"
            "setsar=1[bottom_base];"
        )
    else:
        filters += (
            f"color=c=0x{PAPER_COLOR}:s={width}x{half_height}[paper];"
            f"[1:v]scale={width}:{art_height}:force_original_aspect_ratio=decrease,"
            "setsar=1[bottom_fg];"
            f"[paper][bottom_fg]overlay=(W-w)/2:({art_height}-h)/2:format=auto,"
            "setsar=1[bottom_base];"
        )

    if typography_enabled and args.type_layout == "footer-center":
        scale = width / DEFAULT_WIDTH
        title_size = max(30, round(56 * scale))
        subtitle_size = max(15, round(22 * scale))
        meta_size = max(12, round(16 * scale))
        title_y = art_height + round(20 * scale)
        rule_y = art_height + round(91 * scale)
        subtitle_y = art_height + round(105 * scale)
        meta_y = half_height - round(35 * scale)
        side_margin = round(66 * scale)
        rule_width = round(width * 0.23)
        rule_x = (width - rule_width) // 2

        filters += (
            f"[bottom_base]drawtext=fontfile='{title_font}':text='{title}':"
            f"expansion=none:fontcolor=0x{TEXT_COLOR}:fontsize={title_size}:"
            f"x=(w-text_w)/2:y={title_y}[bottom_title];"
            f"[bottom_title]drawbox=x={rule_x}:y={rule_y}:w={rule_width}:h=1:"
            f"color=0x{RULE_COLOR}@0.55:t=fill[bottom_rule];"
        )
        last_label = "bottom_rule"

        if subtitle:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{subtitle}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.78:fontsize={subtitle_size}:"
                f"x=(w-text_w)/2:y={subtitle_y}[bottom_subtitle];"
            )
            last_label = "bottom_subtitle"

        if left_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{left_meta}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.72:fontsize={meta_size}:"
                f"x={side_margin}:y={meta_y}[bottom_left_meta];"
            )
            last_label = "bottom_left_meta"

        if right_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{right_meta}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.72:fontsize={meta_size}:"
                f"x=w-text_w-{side_margin}:y={meta_y}[bottom];"
            )
            last_label = "bottom"

        if last_label != "bottom":
            filters += f"[{last_label}]null[bottom];"
    elif typography_enabled and args.type_layout == "panel-top-left":
        scale = width / DEFAULT_WIDTH
        title_size = max(27, round(44 * scale))
        subtitle_size = max(14, round(19 * scale))
        meta_size = max(12, round(16 * scale))
        side_margin = round(66 * scale)
        title_y = round(47 * scale)
        left_meta_y = round(111 * scale)
        right_meta_y = round(52 * scale)
        subtitle_y = round(142 * scale)

        filters += (
            f"[bottom_base]drawtext=fontfile='{title_font}':text='{title}':"
            f"expansion=none:fontcolor=0x{TEXT_COLOR}:fontsize={title_size}:"
            f"x={side_margin}:y={title_y}[bottom_title];"
        )
        last_label = "bottom_title"

        if left_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{left_meta}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.72:fontsize={meta_size}:"
                f"x={side_margin}:y={left_meta_y}[bottom_left_meta];"
            )
            last_label = "bottom_left_meta"

        if right_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{right_meta}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.72:fontsize={meta_size}:"
                f"x=w-text_w-{side_margin}:y={right_meta_y}[bottom_right_meta];"
            )
            last_label = "bottom_right_meta"

        if subtitle:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{subtitle}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.74:fontsize={subtitle_size}:"
                f"x={side_margin}:y={subtitle_y}[bottom_subtitle];"
            )
            last_label = "bottom_subtitle"

        filters += f"[{last_label}]null[bottom];"
    elif typography_enabled and args.type_layout == "field-note":
        scale = width / DEFAULT_WIDTH
        side_margin = round(68 * scale)
        kicker_size = max(12, round(15 * scale))
        meta_size = max(12, round(15 * scale))
        title_size = max(25, round(34 * scale))
        subtitle_size = max(20, round(29 * scale))
        archive_size = max(11, round(13 * scale))
        title_y = round(306 * scale)
        subtitle_y = round(365 * scale)
        rule_y = round(116 * scale)

        last_label = "bottom_base"

        if kicker:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{kicker}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}:fontsize={kicker_size}:"
                f"x={side_margin}:y={round(48*scale)}[field_kicker];"
            )
            last_label = "field_kicker"

        filters += (
            f"[{last_label}]drawbox=x={side_margin}:y={rule_y}:w={round(50*scale)}:h=1:"
            f"color=0x{RULE_COLOR}@0.62:t=fill[field_rule];"
        )
        last_label = "field_rule"

        if left_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{left_meta}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.82:fontsize={meta_size}:"
                f"x={side_margin}:y={round(158*scale)}[field_number];"
            )
            last_label = "field_number"

        filters += (
            f"[{last_label}]drawtext=fontfile='{title_font}':text='{title}':"
            f"expansion=none:fontcolor=0x{TEXT_COLOR}:fontsize={title_size}:"
            f"x={side_margin}:y={title_y}[field_title];"
        )
        last_label = "field_title"

        if subtitle:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{subtitle}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.88:fontsize={subtitle_size}:"
                f"x={side_margin}:y={subtitle_y}[field_subtitle];"
            )
            last_label = "field_subtitle"

        if right_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{right_meta}':"
                f"expansion=none:fontcolor=0xb46f50:fontsize={meta_size}:"
                f"x=w-text_w-{round(72*scale)}:y={round(913*scale)}[field_right_meta];"
            )
            last_label = "field_right_meta"

        if archive_label:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{archive_label}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.72:fontsize={archive_size}:"
                f"x=w-text_w-{round(72*scale)}:y={round(858*scale)}[field_archive];"
            )
            last_label = "field_archive"

        if vertical_label:
            label_width = round(174 * scale)
            label_height = round(28 * scale)
            filters += (
                f"color=c=black@0.0:s={label_width}x{label_height},format=rgba,"
                f"drawtext=fontfile='{text_font}':text='{vertical_label}':"
                f"expansion=none:fontcolor=0x{TEXT_COLOR}@0.74:fontsize={archive_size}:"
                "x=(w-text_w)/2:y=(h-text_h)/2,transpose=2[field_vertical];"
                f"[{last_label}][field_vertical]overlay={round(20*scale)}:"
                f"{round(211*scale)}:format=auto[bottom];"
            )
            last_label = "bottom"

        if last_label != "bottom":
            filters += f"[{last_label}]null[bottom];"
    elif typography_enabled and args.type_layout == "sketchbook":
        scale = width / DEFAULT_WIDTH
        script_size = max(38, round(74 * scale))
        location_size = max(15, round(24 * scale))
        year_size = max(19, round(31 * scale))
        note_size = max(12, round(17 * scale))
        right_margin = round(78 * scale)

        filters += (
            f"[bottom_base]drawtext=fontfile='{script_font}':text='{title}':"
            f"expansion=none:fontcolor=0x2f302e:fontsize={script_size}:"
            f"x=w-text_w-{right_margin}:y={round(42*scale)}[sketch_title];"
        )
        last_label = "sketch_title"

        if subtitle:
            filters += (
                f"[{last_label}]drawtext=fontfile='{script_font}':text='{subtitle}':"
                f"expansion=none:fontcolor=0x3f403d@0.84:fontsize={location_size}:"
                f"x=w-text_w-{right_margin}:y={round(123*scale)}[sketch_location];"
            )
            last_label = "sketch_location"

        if right_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{script_font}':text='{right_meta}':"
                f"expansion=none:fontcolor=0xd2643f:fontsize={year_size}:"
                f"x=w-text_w-{right_margin}:y={round(166*scale)}[sketch_year];"
            )
            last_label = "sketch_year"

        if left_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{script_font}':text='{left_meta}':"
                f"expansion=none:fontcolor=0x454943@0.78:fontsize={note_size}:"
                f"x={round(70*scale)}:y={round(768*scale)}[sketch_notes];"
            )
            last_label = "sketch_notes"

        if kicker:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{kicker}':"
                f"expansion=none:fontcolor=0x454943@0.68:fontsize={note_size}:"
                f"x={round(70*scale)}:y={round(48*scale)}[sketch_kicker];"
            )
            last_label = "sketch_kicker"

        filters += f"[{last_label}]null[bottom];"
    elif typography_enabled and args.type_layout == "naive-editorial":
        scale = width / DEFAULT_WIDTH
        title_size = max(38, round(70 * scale))
        subtitle_size = max(14, round(21 * scale))
        meta_size = max(12, round(17 * scale))
        kicker_size = max(12, round(15 * scale))
        side_margin = round(70 * scale)
        title_y = round(58 * scale)
        accent_offset_x = max(2, round(4 * scale))
        accent_offset_y = max(1, round(3 * scale))

        last_label = "bottom_base"

        if kicker:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{kicker}':"
                f"expansion=none:fontcolor=0x5a5a52@0.66:fontsize={kicker_size}:"
                f"x={side_margin}:y={round(28*scale)}[naive_kicker];"
            )
            last_label = "naive_kicker"

        filters += (
            f"[{last_label}]drawtext=fontfile='{naive_font}':text='{title}':"
            f"expansion=none:fontcolor=0xc66f54@0.42:fontsize={title_size}:"
            f"x={side_margin+accent_offset_x}:y={title_y+accent_offset_y}[naive_title_offset];"
            f"[naive_title_offset]drawtext=fontfile='{naive_font}':text='{title}':"
            f"expansion=none:fontcolor=0x343a36:fontsize={title_size}:"
            f"x={side_margin}:y={title_y}[naive_title];"
            f"[naive_title]drawbox=x={side_margin}:y={round(143*scale)}:"
            f"w={round(118*scale)}:h={max(2, round(3*scale))}:"
            f"color=0xd0a744@0.62:t=fill[naive_rule];"
        )
        last_label = "naive_rule"

        if subtitle:
            filters += (
                f"[{last_label}]drawtext=fontfile='{title_font}':text='{subtitle}':"
                f"expansion=none:fontcolor=0x4b4d47@0.80:fontsize={subtitle_size}:"
                f"x={side_margin+round(10*scale)}:y={round(158*scale)}[naive_subtitle];"
            )
            last_label = "naive_subtitle"

        if right_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{right_meta}':"
                f"expansion=none:fontcolor=0xb5654e@0.78:fontsize={meta_size}:"
                f"x=w-text_w-{side_margin}:y={round(52*scale)}[naive_year];"
            )
            last_label = "naive_year"

        if left_meta:
            filters += (
                f"[{last_label}]drawtext=fontfile='{naive_font}':text='{left_meta}':"
                f"expansion=none:fontcolor=0x424640@0.70:fontsize={meta_size}:"
                f"x={side_margin}:y=h-text_h-{round(48*scale)}[naive_number];"
            )
            last_label = "naive_number"

        if archive_label:
            filters += (
                f"[{last_label}]drawtext=fontfile='{text_font}':text='{archive_label}':"
                f"expansion=none:fontcolor=0x55584f@0.58:fontsize={kicker_size}:"
                f"x=w-text_w-{side_margin}:y=h-text_h-{round(49*scale)}[naive_archive];"
            )
            last_label = "naive_archive"

        filters += f"[{last_label}]null[bottom];"
    else:
        filters += "[bottom_base]null[bottom];"

    filter_graph = filters + "[top][bottom]vstack=inputs=2,format=rgb24[out]"

    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(top),
        "-i",
        str(bottom),
        "-filter_complex",
        filter_graph,
        "-map",
        "[out]",
        "-frames:v",
        "1",
    ]

    suffix = output.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        command.extend(["-q:v", "2"])
    elif suffix == ".png":
        command.extend(["-compression_level", "6"])
    elif suffix == ".webp":
        command.extend(["-quality", "95"])
    else:
        raise SystemExit("Output extension must be .png, .jpg, .jpeg, or .webp")

    command.append(str(output))
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        return result.returncode

    print(f"Created {output}")
    print(f"Canvas {width}x{height}; top {width}x{half_height}; bottom {width}x{half_height}")
    if typography_enabled:
        print(f"Typography layout {args.type_layout}")
        if footer_height:
            print(f"Bottom artwork {width}x{art_height}; typography footer {width}x{footer_height}")
    if args.top_grain:
        print(f"Top film grain strength {args.top_grain}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
