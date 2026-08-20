---
name: minimalist-acrylic-split-poster
description: "Transform each supplied reference photo into its own complete premium 3:4 split editorial poster in one ImageGen pass: the upper half preserves the source photograph with high visual fidelity and subtle editorial grading, while the lower half reinterprets the same subject in a selectable art direction with integrated poster typography. Support LAKESIDE TERRAIN geometric architecture, East Asian negative-space acrylic, limited-palette travel relief prints, travel watercolor sticker journals, architectural collage and screen print, travel-memory field notes, architectural watercolor sketchbooks, monochrome etching, naive retro editorial illustration, and custom styles. Use for requests mentioning 上原图下重绘、双联海报、3:4竖版、多风格海报、LAKESIDE TERRAIN、旅行版画、限色丝网印刷、浮雕版画、旅行贴纸手账、水彩贴纸索引、建筑展览海报、东方丙烯、单色版画、旅行手记、复古稚拙插画、每张照片单独输出或不拼图. Default to prompt-native full-poster generation; use deterministic code compositing only when the user explicitly requires pixel-identical source photography or exact typography."
---

# 提示词原生双联编辑海报

把每张输入照片分别生成一张完整的 3:4 竖版海报。默认由 ImageGen 在一次生成中完成上半照片保真、下半艺术重构、整体版式与少量文字，不再先生成下半素材再用代码硬拼。

## 固定规则

- 一张照片对应一张独立海报；禁止把多张输入拼成一张。
- 画面为 3:4 竖版，上下视觉区域严格 1:1，各占约 50%。
- 上半以输入照片为唯一内容来源，最大限度保留主体身份、数量、姿态、表情、建筑结构、地形、空间关系、真实材质、自然光影和原有色彩氛围。
- 上半只做轻微高级摄影调色与极薄胶片颗粒，不把照片画成插画，不替换或移动主体。
- 适配画幅时允许自然延展天空、地面或周边环境；不得拉伸、扭曲、镜像复制或使用模糊照片副本补边。若自然延展不合理，宁可保留干净纸色边距。
- 下半保留同一主体和同一场景语义，再应用且只应用一个风格档案。
- 上下通过主体轮廓、颜色、姿态、轴线或叙事符号相互呼应，分界清晰但整体气质统一。
- 最终必须把每张成品作为可见图片显示在聊天中，并提供绝对保存路径。

## 执行模式

### 默认：完整海报一次生成

完整读取 [references/full-poster-prompt.md](references/full-poster-prompt.md)，再读取一个下半风格档案。把两者整合成一个提示词，以输入照片进行高保真图像编辑，直接生成完整 3:4 海报。

不要把不同风格档案混合。风格档案中的构图、材质、配色与避免项只作用于下半区域；不得污染上半照片。

### 可选：确定性代码合成

只有以下情况才使用 `scripts/compose_split_poster.py`：

- 用户明确说上半必须是原始像素、绝不允许模型重绘；
- 标题、年份或编号必须百分百准确；
- 需要自动化批量生产中严格一致的尺寸与文字位置；
- 用户明确要求使用代码拼接。

不要因为脚本存在就默认使用它。若选择纯提示词模式，应告知用户：上半可高度保真，但不保证逐像素等同原文件；模型生成的长文字也可能出错。

## 风格路由

- 东方留白纸本丙烯：读取 [references/illustration-prompt.md](references/illustration-prompt.md)。
- `LAKESIDE TERRAIN` 高级极简几何与建筑原型研究：读取 [references/geometric-architectural-prompt.md](references/geometric-architectural-prompt.md)。
- 限色粗颗粒旅行浮雕版画与打字机词条：读取 [references/travel-relief-print-prompt.md](references/travel-relief-print-prompt.md)。
- 城市水彩主插画、右侧贴纸索引与旅行观察页：读取 [references/travel-sticker-journal-prompt.md](references/travel-sticker-journal-prompt.md)。
- 建筑拼贴、丝网印刷与设计图：读取 [references/architectural-collage-screenprint-prompt.md](references/architectural-collage-screenprint-prompt.md)。
- 旅行记忆、水彩线稿与档案手记：读取 [references/travel-memory-field-note-prompt.md](references/travel-memory-field-note-prompt.md)。
- 建筑旅行钢笔水彩速写：读取 [references/architectural-travel-sketchbook-prompt.md](references/architectural-travel-sketchbook-prompt.md)。
- 复古稚拙、包豪斯与时尚编辑插画：读取 [references/naive-retro-editorial-prompt.md](references/naive-retro-editorial-prompt.md)。
- 单色建筑蚀刻、点描线刻与靛蓝版画：读取 [references/monochrome-architectural-etching-prompt.md](references/monochrome-architectural-etching-prompt.md)。

用户提供新风格时，把它规范为下半风格模块，明确媒介、形体语言、细节密度、表面质感、色盘、构图、文字气质和避免项；固定上半照片保真规则不变。

## 工作流

1. 枚举输入照片，保持顺序，为每张照片建立独立输出路径。
2. 识别主体身份、数量、姿态、方向、关键结构、空间关系、场景含义与标志性色彩。
3. 选择一个下半风格档案，不自动混搭。
4. 从照片地点、主体或情绪提炼 1–3 个英文单词标题，以及可选的 `No. 01` 和四位年份。优先使用短词，避免模型生成长段文字。
5. 合并完整海报骨架、照片场景摘要、下半风格模块和准确文字，调用 ImageGen 生成完整 3:4 海报。
6. 检查上半是否仍像原照片、上下是否约 50:50、下半是否一眼可识别原主体、文字是否正确。
7. 若上半主体被重绘或改变，进行一次定向编辑，明确只修复上半保真，不改变已通过的下半设计。
8. 若只有文字错误，优先缩短文字后重试；用户要求绝对准确时切换到代码合成模式。

## 文字规则

- 用户提供文字时逐字使用，并在提示词中用引号标明准确文本。
- 未提供时使用地点、建筑类型、动作或情绪形成短标题，例如 `PAVILION AXIS`、`STILL WATERS`、`SUNDAY WANDER`。
- 文字数量少、字距宽松、对比克制，并作为下半设计的一部分自然生长。
- 不添加虚构品牌、机构、长文案、二维码、多个 Logo 或无关装饰文字。

## 质量检查

- 每张输入对应一张独立 3:4 海报，没有拼贴其他照片。
- 上半照片主体、结构、姿态、光影和色彩氛围高度忠实；没有拉伸、扭曲、镜像或模糊副本补边。
- 上下视觉高度接近 1:1，边界清楚，不互相侵占。
- 下半风格明确且具有艺术重组，不是普通滤镜或廉价矢量描摹。
- 标题简短、拼写正确、未遮挡主体。
- 没有模板感、错误物体、意外边框、水印或多余场景。

若成品尚未在当前聊天显示为图片，不得声称完成。

## 资源

- [references/full-poster-prompt.md](references/full-poster-prompt.md)：完整海报共享骨架和上半照片保真提示词。
- [references/travel-relief-print-prompt.md](references/travel-relief-print-prompt.md)：限色粗颗粒旅行浮雕版画风格。
- [references/travel-sticker-journal-prompt.md](references/travel-sticker-journal-prompt.md)：旅行水彩主插画与贴纸视觉索引风格。
- `references/*-prompt.md`：可插拔下半风格模块。
- `scripts/compose_split_poster.py`：仅供像素级原图和准确文字等确定性需求使用。
