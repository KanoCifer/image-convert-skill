#!/usr/bin/env python3
"""
Image Converter - Convert various image formats to WebP

Usage:
    python convert.py input output [--quality N] [--max-size N] [--lossless]
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


def check_webp_support() -> bool:
    """Check if Pillow has WebP support."""
    try:
        # Try to create a minimal WebP image to verify support
        test_img = Image.new("RGB", (1, 1), color="white")
        import io

        buffer = io.BytesIO()
        test_img.save(buffer, format="WEBP")
        return True
    except Exception:
        return False


def validate_input_path(path: str) -> Path:
    """Validate that input path exists."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")
    return p


def validate_quality(quality: int) -> int:
    """Validate quality is in range 1-100."""
    if not 1 <= quality <= 100:
        raise ValueError(f"Quality must be between 1 and 100, got {quality}")
    return quality


def validate_max_size(max_size: Optional[int]) -> Optional[int]:
    """Validate max_size is positive if provided."""
    if max_size is not None and max_size <= 0:
        raise ValueError(f"max_size must be positive, got {max_size}")
    return max_size


def get_output_path(
    input_path: Path, output_dir: Path, output_path: Optional[Path] = None
) -> Path:
    """Determine output path for conversion."""
    if output_path:
        return output_path

    # Change extension to .webp
    stem = input_path.stem
    return output_dir / f"{stem}.webp"


def load_image(path: Path) -> Image.Image:
    """Load and validate image file."""
    try:
        img = Image.open(path)
        # Force loading to detect errors early
        img.load()
        return img
    except Exception as e:
        raise IOError(f"Failed to load image {path}: {e}")


def convert_color_mode(img: Image.Image) -> Image.Image:
    """Convert image to suitable color mode for WebP."""
    # Handle different color modes
    if img.mode == "CMYK":
        # Convert CMYK to RGB
        img = img.convert("RGB")
    elif img.mode == "P" or img.mode == "PA":
        # Convert palette to RGBA
        if "transparency" in img.info:
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
    elif img.mode == "LA" or img.mode == "L":
        # Convert grayscale with alpha to RGBA, grayscale to RGB
        if img.mode == "LA":
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
    elif img.mode == "1":
        # Convert binary to RGB
        img = img.convert("RGB")

    return img


def calculate_new_size(img: Image.Image, max_size: Optional[int]) -> Tuple[int, int]:
    """Calculate new dimensions maintaining aspect ratio."""
    if max_size is None:
        return img.size

    width, height = img.size
    longest_edge = max(width, height)

    if longest_edge <= max_size:
        return img.size

    # Scale down maintaining aspect ratio
    if width > height:
        new_width = max_size
        new_height = int(height * (max_size / width))
    else:
        new_height = max_size
        new_width = int(width * (max_size / height))

    return (new_width, new_height)


def resize_image(img: Image.Image, max_size: Optional[int]) -> Image.Image:
    """Resize image if needed."""
    if max_size is None:
        return img

    new_size = calculate_new_size(img, max_size)
    if new_size == img.size:
        return img

    return img.resize(new_size, Image.Resampling.LANCZOS)


def strip_exif_keep_icc(img: Image.Image) -> Image.Image:
    """Strip EXIF data but preserve ICC profile."""
    # Extract ICC profile if present
    icc_profile = img.info.get("icc_profile")

    # Create new image without EXIF
    data = list(img.getdata())
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(data)

    # Restore ICC profile
    if icc_profile:
        new_img.info["icc_profile"] = icc_profile

    return new_img


def save_webp(img: Image.Image, path: Path, quality: int, lossless: bool) -> None:
    """Save image as WebP with specified settings."""
    # Ensure output directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    save_kwargs = {
        "format": "WEBP",
        "quality": quality,
        "lossless": lossless,
        "method": 4,  # Balanced compression
    }

    # Only add subsampling for lossy (not lossless)
    if not lossless:
        save_kwargs["subsampling"] = 0  # 4:4:4 for best quality

    try:
        img.save(path, **save_kwargs)
    except Exception as e:
        raise IOError(f"Failed to save WebP to {path}: {e}")


def process_single_file(
    input_path: Path,
    output_path: Path,
    quality: int,
    max_size: Optional[int],
    lossless: bool,
) -> bool:
    """Process a single image file."""
    try:
        # Load image
        img = load_image(input_path)

        # Convert color mode
        img = convert_color_mode(img)

        # Resize if needed
        img = resize_image(img, max_size)

        # Strip EXIF but keep ICC
        img = strip_exif_keep_icc(img)

        # Save as WebP
        save_webp(img, output_path, quality, lossless)

        return True

    except (IOError, ValueError) as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return False


def get_supported_extensions() -> set:
    """Get set of supported image extensions."""
    # Common image formats that can be converted to WebP
    return {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".tiff",
        ".tif",
        ".ppm",
        ".pgm",
        ".pbm",
        ".webp",
    }


def is_supported_image(path: Path) -> bool:
    """Check if file is a supported image format."""
    return path.suffix.lower() in get_supported_extensions()


def process_directory(
    input_dir: Path,
    output_dir: Path,
    quality: int,
    max_size: Optional[int],
    lossless: bool,
) -> Tuple[int, int]:
    """Process all images in a directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    total_count = 0

    # Find all image files
    for path in input_dir.rglob("*"):
        if not path.is_file():
            continue
        if not is_supported_image(path):
            continue

        total_count += 1

        # Calculate relative path and output path
        rel_path = path.relative_to(input_dir)
        output_path = output_dir / rel_path.with_suffix(".webp")

        # Create subdirectories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if process_single_file(path, output_path, quality, max_size, lossless):
            success_count += 1
            print(f"Converted: {path} -> {output_path}")
        else:
            print(f"Failed: {path}", file=sys.stderr)

    return success_count, total_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert images to WebP format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.jpg output.webp
  %(prog)s input.png output/ --quality 85
  %(prog)s photos/ webp_photos/ --max-size 1920
  %(prog)s image.png lossless.webp --lossless
        """,
    )

    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output", help="Output file or directory")
    parser.add_argument(
        "--quality",
        type=int,
        default=90,
        help="JPEG-like quality for lossy WebP (1-100, default: 90)",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        help="Maximum dimension in pixels (longest edge). No scaling if not specified.",
    )
    parser.add_argument(
        "--lossless",
        action="store_true",
        help="Use lossless compression (ignores --quality)",
    )

    args = parser.parse_args()

    # Check WebP support
    if not check_webp_support():
        print("ERROR: WebP support not available in Pillow.", file=sys.stderr)
        print(
            "Please install Pillow with WebP support: pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate inputs
    try:
        input_path = validate_input_path(args.input)
        quality = validate_quality(args.quality)
        max_size = validate_max_size(args.max_size)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Process based on input type
    output_path = Path(args.output)

    if input_path.is_file():
        # Single file mode
        if output_path.is_dir():
            # Output is directory, use input filename with .webp
            output_path = get_output_path(input_path, output_path)

        success = process_single_file(
            input_path, output_path, quality, max_size, args.lossless
        )

        if success:
            print(f"Converted: {input_path} -> {output_path}")
            sys.exit(0)
        else:
            sys.exit(1)

    elif input_path.is_dir():
        # Directory mode
        output_path.mkdir(parents=True, exist_ok=True)

        success, total = process_directory(
            input_path, output_path, quality, max_size, args.lossless
        )

        print(f"\nCompleted: {success}/{total} files converted successfully")

        if success < total:
            sys.exit(1)
        sys.exit(0)

    else:
        print(
            f"ERROR: Input path is neither a file nor a directory: {input_path}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
