---
name: image-converter
description: 使用 Pillow 将常见图像格式（PNG、JPEG、GIF、BMP、TIFF）批量转换为 WebP 或进行格式不变的压缩，支持质量控制、尺寸缩放和无损压缩模式。
---

# Image Converter Skill

将图像批量转换为 WebP 格式或保留原格式压缩的自动化工具，使用前请确保已安装 Pillow 库：

```bash
pip install Pillow

# 或使用uv
uv add Pillow
```

## 快速开始

```bash
# 转换单个文件为 WebP
python scripts/convert.py input.jpg output.webp

# 转换目录（保留原文件）
python scripts/convert.py ./images/ ./webp_output/

# 自定义质量压缩
python scripts/convert.py input.jpg output.webp --quality 80

# 无损压缩
python scripts/convert.py input.png output.webp --lossless

# 缩放图片（最长边 1920px）
python scripts/convert.py input.jpg output.webp --max-size 1920

# 压缩图片（保留原格式）
python scripts/convert.py input.png output.png --compress
python scripts/convert.py input.jpg output.jpg --compress --compress-quality 75

# 批量压缩目录
python scripts/convert.py ./images/ ./compressed/ --compress
```

## 功能列表

| 功能 | 说明 |
|------|------|
| 批量转换 | 支持目录和文件列表输入 |
| 质量控制 | 有损压缩质量 1-100 |
| 无损模式 | 保持原始像素质量 |
| 尺寸缩放 | 按最长边等比缩放 |
| 色彩空间 | 自动转换 CMYK→RGB，调色板→RGBA |
| 元数据 | 清除 EXIF，保留 ICC 配置文件 |
| 格式保留压缩 | 保留原格式进行压缩（PNG/JPEG/GIF/WebP/TIFF） |

## CLI 参数

### 转换参数（转换为 WebP）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--quality` | 压缩质量 (1-100) | 90 |
| `--max-size` | 最长边缩放像素 | 不缩放 |
| `--lossless` | 启用无损压缩 | False |

### 压缩参数（保留原格式）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--compress` | 启用压缩模式，保留原格式 | False |
| `--compress-quality` | 压缩质量 (1-100) | 85 |
| `--compress-level` | PNG/TIFF 压缩级别 (0-9) | 6 |

## 参考

详细 WebP 参数配置请查看 [webp_settings.md](./references/webp_settings.md)。
