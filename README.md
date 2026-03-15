# Image Converter Skill

使用 Pillow 在常见图像格式之间进行 mutual conversion（互相转换），或进行格式不变的压缩。

## 功能特性

- **格式支持**: 全面支持常见图像格式 mutual conversion（互相转换）
  - 输入格式: PNG, JPEG, GIF, BMP, TIFF, WebP
  - 输出格式: PNG, JPEG, GIF, BMP, TIFF, WebP
- **质量控制**: 1-100 可配置 (默认 90)
- **智能缩放**: 保持宽高比的最长边限制
- **批量处理**: 支持目录批量转换
- **色彩转换**: 自动转换 CMYK→RGB，调色板→RGBA
- **元数据**: 清除 EXIF，保留 ICC 色彩配置
- **格式保留压缩**: 保留原格式进行压缩

## 安装依赖

使用前需安装 Pillow：

```bash
pip install Pillow

# 或使用uv
uv add Pillow
```

确保 Pillow 版本支持 WebP 编码（默认从 Pillow 2.7 开始支持）。

## 快速开始

默认转换为 WebP 格式，质量为 90。

```bash
# 转换单个文件（默认 WebP）
python image-converter/scripts/convert.py input.jpg output.webp

# 自定义质量
python image-converter/scripts/convert.py input.jpg output.webp --quality 85

# 智能缩放 (最长边 1920px)
python image-converter/scripts/convert.py input.jpg output.webp --max-size 1920

# 无损压缩
python image-converter/scripts/convert.py input.png output.webp --lossless

# 批量处理目录
python image-converter/scripts/convert.py photos/ webp_photos/

# 批量处理多个文件（逗号分隔）
python image-converter/scripts/convert.py "img1.png,img2.jpg,img3.gif" output_dir/ --to-format webp

# 使用通配符批量处理
python image-converter/scripts/convert.py "*.jpg" output_dir/ --to-format png

# 并行批量处理（4线程）
python image-converter/scripts/convert.py "*.jpg" output_dir/ --threads 4 -v
```

### 格式 mutual conversion（互相转换）

根据输出文件扩展名自动确定目标格式：

```bash
# PNG → JPEG
python image-converter/scripts/convert.py input.png output.jpg

# JPEG → PNG
python image-converter/scripts/convert.py input.jpg output.png

# 任意格式 → WebP
python image-converter/scripts/convert.py input.bmp output.webp

# WebP → PNG
python image-converter/scripts/convert.py input.webp output.png

# GIF → BMP
python image-converter/scripts/convert.py input.gif output.bmp

# JPEG → TIFF
python image-converter/scripts/convert.py input.jpg output.tiff
```

### 使用 --to-format 显式指定目标格式

```bash
# 强制输出为 WebP（忽略输出文件扩展名）
python image-converter/scripts/convert.py input.png output.jpg --to-format webp
# 输出: output.webp

# 批量转换为 PNG
python image-converter/scripts/convert.py photos/ png_photos/ --to-format png

# 批量转换为 JPEG
python image-converter/scripts/convert.py photos/ jpeg_photos/ --to-format jpeg
```

### 格式保留压缩

保留原格式进行压缩，不转换为 WebP：

```bash
# 压缩 PNG
python image-converter/scripts/convert.py input.png output.png --compress

# 压缩 JPEG（质量 75）
python image-converter/scripts/convert.py input.jpg output.jpg --compress --compress-quality 75

# 批量压缩目录
python image-converter/scripts/convert.py photos/ compressed/ --compress
```

压缩参数：
- `--compress-quality`: 压缩质量 (1-100，默认 85)
- `--compress-level`: PNG/TIFF 压缩级别 (0-9，默认 6)

常用参数：
- `--to-format`: 显式指定目标格式 (jpeg/jpg, png, webp, gif, bmp, tiff/tif)

## 格式转换优先级

目标格式确定的优先级顺序：

1. **`--to-format` 标志**（最高优先级）: 显式指定目标格式
2. **输出文件扩展名**: 根据输出文件的扩展名确定格式
3. **默认行为**: 
   - 普通转换模式: 默认为 WebP
   - `--compress` 压缩模式: 保留输入格式

## 项目结构

```
.
├── image-converter/          # Skill 目录
│   ├── SKILL.md          # 技能定义文件
│   ├── scripts/
│   │   └── convert.py    # 核心转换脚本
│   └── references/
│   │   └── webp_settings.md  # WebP 参数参考
│   └── assets/
│
├── image-converter.skill  # 打包的 skill 文件
└── scripts/
    └── package_skill.py  # 打包脚本
```

## 使用 skill

### 直接使用脚本

如上面的"快速开始"部分所示，直接运行 Python 脚本即可。

### 加载 Skill 文件

如果您的平台支持 `.skill` 文件加载：

1. 将 `image-converter.skill` 文件导入到您的技能系统或将`image-converter`文件夹放置在指定的技能目录中。
2. 根据平台文档使用技能

详细使用说明请参考 `image-converter/SKILL.md` 和 `image-converter/references/webp_settings.md`。
