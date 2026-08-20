---
name: minimalist-acrylic-split-poster
description: "Convert every supplied reference photo into its own premium 3:4 split editorial poster: the upper half preserves and lightly grades the original photograph, while the lower half is a style-controlled reinterpretation with accurate code-rendered titles and metadata. Support switchable profiles such as LAKESIDE TERRAIN minimalist geometric editorial abstraction, East Asian negative-space acrylic, architectural collage with screen-print and blueprint details, travel-memory watercolor field notes, European architectural travel sketchbooks, monochrome architectural etching and stipple prints, naive retro hand-drawn editorial illustration, and user-defined custom styles. Use for requests mentioning LAKESIDE TERRAIN、上原图下重绘、多风格海报、高级极简几何、扁平色块、细线构成、大面积留白、极简抽象、建筑拼贴、丝网印刷、旅行手记、记忆档案、水彩线稿、钢笔建筑速写、单色建筑蚀刻、蓝图版画、点描线刻、靛蓝线稿、铜版画、稚拙插画、复古手绘、包豪斯、儿童绘本、时尚速写、粉蜡笔、旧套印、手写标题、建筑海报、艺术展览视觉、东方丙烯、海报文字、3:4 竖版、每张单独输出或不拼图. Use ImageGen only for the lower artwork and bundled code for the exact layout, source-photo inset, film grain, and typography."
---

# 通用双联编辑海报

把每张输入照片分别制成一张独立的 3:4 竖版海报。上半固定为原照片，下半按选定风格重新诠释同一场景，并加入克制、准确的编辑设计文字；上下两区高度严格相等。

## 不变骨架

- 一张照片对应一张海报。禁止多图拼贴、九宫格或把多个场景放在同一张图。
- 默认画布 1536×2048，上下各为 1536×1024。
- 上半区使用原始照片本身，只做轻微杂志摄影调色；不重绘、不换主体、不拉伸、不强制裁切。默认完整等比居中，比例不匹配时以米白纸色留白，不用模糊照片副本补边。
- 下半区保持主体身份、数量、姿态、动作、关键结构、相对位置、空间方向和场景含义。
- ImageGen 只生成无文字的下半艺术素材。标题、年份、编号与细线由代码绘制，避免乱码。
- 用 `scripts/compose_split_poster.py` 锁定尺寸、50/50 分区、原图适配、文字和逐张导出。
- 最终必须把每张成品作为可见图片显示在当前聊天中，并提供绝对保存路径。

## 风格路由

先确定风格，再生成下半素材。不要把多个风格档案自动混合。

### A. 东方留白丙烯绘本

用户要求东方留白、纸本丙烯、绘本、干笔、诗意自然场景时，完整读取 [references/illustration-prompt.md](references/illustration-prompt.md)。

### B. LAKESIDE TERRAIN 高级极简几何编辑

用户提到 `LAKESIDE TERRAIN`，或要求高级极简几何、可识别的抽象主体、扁平色块、细线构成、大面积留白、建筑海报或高级文化视觉时，完整读取 [references/geometric-architectural-prompt.md](references/geometric-architectural-prompt.md)。此档案强调建筑原型研究、语义重设计与结构诗意，不是照片轮廓矢量化；色彩、辅助几何和文字位置应根据原照适配，不固定为粉色叠层、冷灰蓝景观、镜像碎片或某一种版式。此档案只控制下半区，不把上半原图规则写入 ImageGen 提示词。

### C. 建筑拼贴丝网印刷

用户要求建筑拼贴、半透明色块、照片碎片、丝网印刷、设计图线条或向下渐融的竖长碎片时，完整读取 [references/architectural-collage-screenprint-prompt.md](references/architectural-collage-screenprint-prompt.md)。此档案默认使用 `panel-top-left` 文字布局和轻微上半胶片颗粒。

### D. 旅行记忆手记

用户要求旅行手账、记忆档案、透明水彩、铅笔或针管笔线稿、左侧文字栏、原照小图或田野笔记时，完整读取 [references/travel-memory-field-note-prompt.md](references/travel-memory-field-note-prompt.md)。此档案使用 `field-note` 代码布局，由脚本把原照片缩略图准确嵌入下半区左下。

### E. 建筑旅行速写本

用户要求欧洲建筑速写、钢笔透视线、透明水彩、地标研究、手写地点和材质批注时，完整读取 [references/architectural-travel-sketchbook-prompt.md](references/architectural-travel-sketchbook-prompt.md)。此档案使用 `sketchbook` 代码布局，右上绘制手写体地点、地区和年份。

### F. 复古稚拙手绘编辑插画

用户要求稚拙手绘、复古编辑插画、包豪斯构成、成熟儿童绘本、时尚速写、水彩水粉彩铅粉蜡笔、幽默隐喻或旧印刷套色时，完整读取 [references/naive-retro-editorial-prompt.md](references/naive-retro-editorial-prompt.md)。此档案使用 `naive-editorial` 代码布局，以手写主标题、轻微错位叠色和温和辅助字体准确呈现文字。

### G. 单色建筑蚀刻版画

用户要求单色靛蓝或墨色建筑线刻、铜版画、蚀刻版画、点描、蓝图线稿、古典雕版、细密排线、图像在象牙色纸张中渐隐或 `STILL WATERS` 类型海报时，完整读取 [references/monochrome-architectural-etching-prompt.md](references/monochrome-architectural-etching-prompt.md)。此档案默认使用 `panel-top-left` 文字布局，与钢笔水彩旅行速写分开。

### H. 用户自定义风格

用户提供新风格时，把描述规范化成一张临时“风格卡”，至少明确：

- 表达媒介与写实程度
- 形体语言与细节密度
- 材质或表面质感
- 配色来源与饱和度
- 主体位置、留白和空间组织
- 可用的图形辅助元素
- 文字气质与元信息格式
- 强制避免项

保留用户风格中的关键差异，不用默认丙烯词覆盖它。若这种风格会重复使用，再把它新增为独立的 `references/<style>-prompt.md`；版式脚本无需改变。

## 工作流

### 1. 建立逐图任务

枚举所有输入照片并保持顺序。为每张照片建立原图路径、下半素材路径、成品路径、风格档案、标题、副标题、年份和系列编号。默认输出到 `outputs/split-editorial-posters/`。

### 2. 理解照片

逐张识别最重要的主体、轮廓、结构、姿态、方向、关键物体、空间层次、场景含义与标志性色彩。区分“必须保留的识别信息”和“可以删除的环境细节”。

### 3. 生成下半素材

使用内置 `image_gen`，把当前照片作为唯一主体参考，并应用所选风格档案：

- 只生成一张独立横向 3:2 素材，不生成双联海报、上半原照、文字、边框或拼贴。
- 保持语义与主体识别，改变视觉语言；不要做普通滤镜。
- 配色优先从原照片提取，除非用户明确指定其他色系。
- 根据风格的文字布局预留空间：`footer-center` 在底部留白；`panel-top-left` 在左上和右上留白；`field-note` 保留左侧档案栏；`sketchbook` 保留右上手记区；`naive-editorial` 保留左上手写标题区及角落元信息区。
- 生成后检查主体是否仍可识别、风格是否纯粹、是否误带文字。
- 保存每张素材，不覆盖其他照片或其他风格版本。

### 4. 设计文字

用户提供文字时逐字使用；否则从地点、结构、情绪或故事中提炼：

- 2–4 个英文单词，例如 `LAKESIDE SILENCE`、`VILLAGE GEOMETRY`。
- 或 4–8 个汉字，可附一行小号中英文副标题。
- 左下放年份，例如 `2026`；右下放编号，例如 `STUDY 02`、`FORM 01`。

文字只作为编辑设计层。保持低对比、宽松字距、细线、充足留白；避免营销口号、发光、描边、粗黑大字和装饰堆积。按风格选择以下代码布局：

- `footer-center`：标题在下半区独立页脚居中，年份与编号分列左右。
- `panel-top-left`：标题位于下半区左上，编号在其下，年份位于右上。
- `field-note`：左侧档案文字与纵排标签、右侧主插画、左下原照片索引图、右下档案编号。
- `sketchbook`：右上手写体地点与年份、左下观察词，适合建筑与地标旅行速写。
- `naive-editorial`：左上手写标题带轻微错位套色，辅助文字与编号分散在留白区，适合复古稚拙编辑插画。

### 5. 用代码合成

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/styled-artwork.png \
  --output /absolute/path/to/poster.png \
  --title "VILLAGE GEOMETRY" \
  --subtitle "湖岸构成" \
  --left-meta "2026" \
  --right-meta "FORM STUDY 02"
```

脚本会创建精确 3:4 画布、严格 50/50 分区、轻调上半原照、等比适配两张图片，并在下半区内部保留默认 18% 的文字页脚。上半默认使用 `--top-fit contain-paper`：完整保留照片比例并以纸色填补空余位置；只有用户明确需要时才使用兼容模式 `--top-fit blur-extend`。省略 `--title` 可输出无文字版本；用 `--footer-ratio 0.16` 至 `0.24` 调整页脚。

LAKESIDE TERRAIN 高级极简几何编辑档案使用：

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/minimal-geometric-editorial.png \
  --output /absolute/path/to/poster.png \
  --title "LAKESIDE TERRAIN" \
  --left-meta "2026" \
  --right-meta "STUDY 01" \
  --top-fit contain-paper \
  --top-grain 1
```

默认使用 `footer-center`；若下半构图在左上和右上有明确安全留白，也可使用 `--type-layout panel-top-left`。不要为了迁就文字强制改变主体识别关系。

建筑拼贴丝网印刷档案沿用 `panel-top-left` 布局，但使用与 `LAKESIDE TERRAIN` 不同的标题，例如：

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/collage-artwork.png \
  --output /absolute/path/to/poster.png \
  --type-layout panel-top-left \
  --title "REGIONAL LAYERS" \
  --left-meta "No. 03" \
  --right-meta "2026" \
  --top-grain 2
```

`--top-grain` 接受 0–8；高级杂志摄影通常使用 1–2，避免明显噪点。

旅行记忆手记档案使用：

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/watercolor-field-note.png \
  --output /absolute/path/to/poster.png \
  --type-layout field-note \
  --kicker "ONE-DAY EXHIBITION" \
  --vertical-label "FIELD NOTE" \
  --title "MEMORY WALK" \
  --subtitle "沿岸而行" \
  --left-meta "NO. 004" \
  --archive-label "MEMORY ARCHIVE" \
  --right-meta "2026"
```

`field-note` 会直接使用上半原图生成左下索引照片，不把缩略图交给 ImageGen 模拟。

建筑旅行速写本档案使用：

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/architectural-sketch.png \
  --output /absolute/path/to/poster.png \
  --type-layout sketchbook \
  --title "Lakeside" \
  --subtitle "Village Study" \
  --right-meta "2026" \
  --left-meta "light  stone  glass  water"
```

`sketchbook` 默认使用系统手写字体；可用 `--script-font /absolute/path/to/font.ttf` 替换。

复古稚拙手绘编辑插画档案使用：

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/naive-editorial-artwork.png \
  --output /absolute/path/to/poster.png \
  --type-layout naive-editorial \
  --kicker "A SMALL STORY" \
  --title "SUNDAY WANDER" \
  --subtitle "soft light, odd little moments" \
  --left-meta "No. 06" \
  --right-meta "2026"
```

`naive-editorial` 默认使用系统 Marker Felt 手写字体，并以低透明度暖色偏移层模拟旧印刷套色。可用 `--naive-font /absolute/path/to/font.ttf` 替换。

单色建筑蚀刻版画档案使用：

```bash
python3 scripts/compose_split_poster.py \
  --top /absolute/path/to/original.jpg \
  --bottom /absolute/path/to/monochrome-etching.png \
  --output /absolute/path/to/poster.png \
  --type-layout panel-top-left \
  --title "STILL WATERS" \
  --left-meta "OBSERVATION 01" \
  --right-meta "2026" \
  --top-grain 1
```

### 6. 质量检查

- 成品精确 3:4，分界位于高度 50%。
- 上半原图主体无形变、替换、裁切或过度调色；默认补位区域是均匀纸色，不出现模糊副本、镜像延展或复制背景。
- 下半一眼可识别原主体，但视觉语言明确属于所选风格。
- 自定义风格的关键特征没有被默认丙烯、水彩或几何元素污染。
- 标题拼写准确，元信息清晰，不遮挡主体。
- 没有普通滤镜感、廉价模板感、错误文字、意外边框或多图拼贴。

若成品尚未在当前聊天显示为图片，不得声称完成。

## 资源

- [references/illustration-prompt.md](references/illustration-prompt.md)：东方留白纸本丙烯风格档案。
- [references/geometric-architectural-prompt.md](references/geometric-architectural-prompt.md)：LAKESIDE TERRAIN 高级极简几何编辑与艺术展览海报风格档案。
- [references/architectural-collage-screenprint-prompt.md](references/architectural-collage-screenprint-prompt.md)：建筑拼贴、丝网印刷与设计图风格档案。
- [references/travel-memory-field-note-prompt.md](references/travel-memory-field-note-prompt.md)：旅行记忆、水彩线稿与档案手记风格档案。
- [references/architectural-travel-sketchbook-prompt.md](references/architectural-travel-sketchbook-prompt.md)：建筑旅行钢笔水彩与手写观察风格档案。
- [references/naive-retro-editorial-prompt.md](references/naive-retro-editorial-prompt.md)：复古稚拙手绘、包豪斯构成与时尚编辑插画风格档案。
- [references/monochrome-architectural-etching-prompt.md](references/monochrome-architectural-etching-prompt.md)：单色建筑蚀刻、点描线刻、靛蓝版画与渐隐纸面风格档案。
- `scripts/compose_split_poster.py`：通用版式、原图适配、准确文字和逐图导出脚本。
