---
name: image-converter
description: 使用 Pillow 将常见图像格式（PNG、JPEG、GIF、BMP、TIFF）批量转换为 WebP，支持质量控制、尺寸缩放和无损压缩模式
---

# Image Converter Skill

将图像批量转换为 WebP 格式的自动化工具。

## 快速开始

```bash
# 转换单个文件
python scripts/convert.py input.jpg output.webp

# 转换目录（保留原文件）
python scripts/convert.py ./images/ ./webp_output/

# 自定义质量压缩
python scripts/convert.py input.jpg output.webp --quality 80

# 无损压缩
python scripts/convert.py input.png output.webp --lossless

# 缩放图片（最长边 1920px）
python scripts/convert.py input.jpg output.webp --max-size 1920
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

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--quality` | 压缩质量 (1-100) | 90 |
| `--max-size` | 最长边缩放像素 | 不缩放 |
| `--lossless` | 启用无损压缩 | False |

## 参考

详细 WebP 参数配置请查看 [webp_settings.md](./references/webp_settings.md)。
