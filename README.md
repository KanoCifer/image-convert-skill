# Image Converter Skill

使用 Pillow 将常见图像格式转换为 WebP 格式，或进行格式不变的压缩。

## 功能特性

- **格式支持**: PNG, JPEG, GIF, BMP, TIFF → WebP
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

默认质量为 90。

```bash
# 转换单个文件
python image-converter/scripts/convert.py input.jpg output.webp

# 自定义质量
python image-converter/scripts/convert.py input.jpg output.webp --quality 85

# 智能缩放 (最长边 1920px)
python image-converter/scripts/convert.py input.jpg output.webp --max-size 1920

# 无损压缩
python image-converter/scripts/convert.py input.png output.webp --lossless

# 批量处理目录
python image-converter/scripts/convert.py photos/ webp_photos/
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
