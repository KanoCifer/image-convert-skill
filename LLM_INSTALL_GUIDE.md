# Image Converter Skill 自动安装指南

本文档指导 LLM 如何自动安装并使用 Image Converter 技能，实现批量图像格式转换与压缩功能。

## 技能特性

- 支持 PNG/JPEG/GIF/BMP/TIFF/WebP 格式互转
- 批量处理：目录、通配符、多文件列表
- 多线程并行加速
- 质量控制、尺寸缩放、无损压缩
- 自动色彩空间转换、EXIF 清除

## 自动安装步骤

### 1. 环境检查

```bash
# 检查 Python 版本 (要求 3.10+)
python --version

# 检查是否已安装 Pillow
pip show Pillow
```

### 2. 自动安装依赖

如果未安装 Pillow，执行以下命令：

```bash
pip install Pillow
# 或使用 uv
uv add Pillow
```

### 3. 获取技能包

如支持加载skill文件，直接下载；否则克隆/image converter文件夹并定位到你的CLI技能目录：

```bash
# 方法1：直接下载 skill 文件
curl -O https://raw.githubusercontent.com/Kilo-Org/kilocode/main/skills/image-converter.skill

# 方法2：克隆技能目录到 CLI 技能目录
git clone https://github.com/KanoCifer/image-convert-skill.git
cd .config/kilo/skill/image-converter
cd .cladue/skills/image-converter
cd .config/opencode/skill/image-converter

# 复制/image converter文件夹到 CLI 技能目录
cp -r /path/to/image-converter /path/to/cli/skills/
```

## 自动调用示例

### 批量转换为 WebP

```python
# 自动检测并转换目录下所有图片
import subprocess
result = subprocess.run([
    "python", "/path/to/convert.py",
    "./input_dir", "./output_dir",
    "--to-format", "webp",
    "--quality", "85",
    "--threads", "4",
    "-v"
], capture_output=True, text=True)

if result.returncode == 0:
    print("转换成功")
else:
    print(f"转换失败: {result.stderr}")
```

### 自动压缩图片

```python
# 自动压缩目录下所有 PNG 图片，保持原格式
result = subprocess.run([
    "python", "/path/to/convert.py",
    "./images", "./compressed",
    "--compress",
    "--compress-quality", "75",
    "--threads", "8"
], capture_output=True, text=True)
```

## 错误处理与自动修复

### 常见错误1：WebP 支持缺失

**错误信息**：`ERROR: WebP support not available in Pillow`
**自动修复**：

```bash
pip uninstall -y Pillow
pip install Pillow --no-binary :all:
```

### 常见错误2：文件格式不支持

**错误信息**：`Unsupported format: xxx`
**自动修复**：自动跳过不支持的文件，记录错误日志

### 常见错误3：输出目录不存在

**自动修复**：自动创建输出目录，无需手动干预

## 自动化工作流建议

### 批量处理工作流

1. 扫描输入目录，获取所有支持的图片文件
2. 调用 convert.py 进行批量转换/压缩
3. 校验输出文件完整性
4. 生成处理报告（成功数、失败数、节省空间）

## 技能验证

安装完成后，运行以下命令验证功能正常：

```bash
# 测试转换功能
python /path/to/convert.py --help

# 测试批量处理
echo "test1.jpg,test2.png" | xargs python /path/to/convert.py test_output/ --to-format webp
```
