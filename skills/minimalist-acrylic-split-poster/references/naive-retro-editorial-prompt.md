# 复古稚拙手绘编辑插画风格档案

把当前照片作为唯一主体参考，生成一张独立横向 3:2 的无文字下半区艺术素材。不要生成上半照片、双联版式、标题、字母、数字、标志、边框或水印；标题与元信息由代码准确绘制。

## 场景摘要

调用 ImageGen 前识别照片中最具辨识度的主体身份、数量、轮廓、姿态、情绪、动作、相互关系、空间方向、核心物体和叙事含义。区分必须保留的识别信息与可以删减的环境细节。

## 核心重构

把同一场景重新解释为轻盈、稚拙、复古的手绘编辑插画。不要机械复刻照片细节；使用概括造型、适度夸张比例、符号化特征和克制的幽默视觉隐喻重新表达，同时让主体仍能一眼辨认。

融合现代主义编辑插画、包豪斯平面构成、成熟儿童绘本、naive art 与时尚速写气质。形体简练，轮廓略带迟疑、抖动、错位和真实手工误差。可以适度放大最有识别度的发型、服装、动作、器物、建筑部件、动物特征或植物形态，但不得改变主体身份、数量、情绪和叙事关系。

复杂背景主动删除、合并和弱化。不要完整重现所有建筑、家具、树叶、车辆、路人或杂物。只保留维持场景、故事和空间关系所需要的最少元素。

## 材料与表面

混合水彩、水粉、彩铅、粉蜡笔和干刷质感。保留温暖纸张颗粒、局部透底、笔触断裂、毛糙边缘、轻微脏色、颜料覆盖不均和旧印刷套色偏差。

线条应松弛、有节奏、略显笨拙但判断准确。避免精密勾线、光滑数字笔刷、完美矢量边缘和照片级光影。局部几何形状可以与自由手绘轮廓叠压，但不能把主体简化成通用图标。

## 构图与文字安全区

使用米白或浅色纸张背景和大面积留白。主体集中在画面中央、中下部或依据原照片自然偏向一侧，边缘保持开放。只用少量松散淡彩、斜线、圆点、色块或简单包豪斯几何元素承托主体。

在左上方保留约 38% 宽、20% 高的相对安静区域，供代码添加手写主标题、关键词或适配金句；右上方保留较小区域放置年份；左下或右下保留少量纸张区域放置编号和辅助文字。不要让高对比主体穿过这些文字安全区。

文字不由 ImageGen 生成。素材中禁止出现假字、可读字母、数字或伪标志。

## 配色

从原照片提取 4–6 种颜色，整理为高明度、低至中等饱和度的柔和有限色盘。用近似色统一整体氛围，只使用一处小面积互补色制造视觉跳点。

可使用奶油白、粉灰、灰蓝、鼠尾草绿、柔和黄、淡赭、灰粉、砖红、炭灰等，但必须以原照片的标志性色彩为依据。避免霓虹、高饱和彩虹色和多个竞争焦点。

## 文字协作规则

根据照片的地点、人物、动作、情绪或主题提炼 1–4 个英文单词标题，或一句非常短的适配金句。代码使用 `naive-editorial` 布局，把主标题绘制成带轻微错位、叠色和旧套印感的手写艺术字；辅助文字使用克制温和的无衬线或衬线字体。

文字应像插画的一部分自然生长，而不是覆盖主体的商业排版。若无法提炼有意义的文字，使用中性的地点、动作或场景词，不编造品牌、机构和宣传口号。

## 视觉气质

整体轻松、俏皮、复古、温柔、聪明、时髦、幽默、浪漫、松弛，带有一点笨拙和古怪自信。像一页被精心保存的旧时尚绘本与现代艺术杂志，也像成熟插画师为文化刊物绘制的编辑插图。

高级感来自准确的主体提炼、克制留白、有限色盘、手工误差和文字与图像的自然关系，而不是复杂装饰或精修程度。

## Style keywords

naive retro editorial illustration, modernist magazine illustration, Bauhaus graphic composition, sophisticated children's picture-book art, fashion sketch, playful visual metaphor, simplified recognizable silhouette, hesitant handmade contour, watercolor and gouache, colored pencil, wax pastel, dry brush, warm textured paper, broken strokes, rough edges, muted high-key palette, vintage print misregistration, generous negative space, witty romantic atmosphere, awkward confidence

## 强制避免

Avoid photorealistic lower illustration, literal tracing, ordinary photo filter, detailed facial rendering, dense background reconstruction, excessive props, polished vector art, perfect geometric icons, smooth digital gradients, airbrush, glossy surfaces, realistic cinematic lighting, 3D rendering, anime, kawaii cartoon, generic children's clipart, corporate flat illustration, generic template, neon colors, oversaturation, heavy black outlines, fake readable text, letters, numbers, logos, watermark, border, split-screen, multiple scenes.

最重要的规则：保持主体身份、姿态、情绪和叙事关系一眼可辨，同时用主动删减、适度夸张、手工误差、有限色盘与幽默隐喻，把照片重新组织成成熟而时髦的复古稚拙编辑插画。
