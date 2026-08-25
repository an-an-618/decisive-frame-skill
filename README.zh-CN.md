# 决定性一帧 · Decisive Frame

将用户提供的照片重新导演为 16:9 水墨电影静帧：只有一个经过确认的局部元素或色彩区域保留源照片颜色，其余世界在干净白底上被重新组织为疏朗水墨。

> 世界退入黑白，只有一个决定性存在仍然拥有颜色。

## Before → After

| 处理前 | 处理后 |
|---|---|
| ![林荫骑行处理前](examples/showcase/tree-lane-cyclist-before.jpg) | ![林荫骑行处理后](examples/showcase/tree-lane-cyclist-after.jpg) |
| ![城市橙红立面处理前](examples/showcase/orange-city-facade-before.jpg) | ![城市橙红立面处理后](examples/showcase/orange-city-facade-after.jpg) |

前往[公开 Showcase](examples/README.md)查看全部 7 组获准展示的对照案例。

## 它有什么不同

决定性一帧不是全局局部彩色滤镜，也不是黄色旧纸、撕纸或复古胶卷模板。它先阅读照片，再自动选择“决定性元素”或“决定性色彩”模式，提出 2–3 个导演候选，并等待用户选择后才生成图片。

被选中的锚点忠于原色，只允许克制地提纯、加深和调整明暗。人物锚点默认成为一体化的“动态线稿＋透明淡彩”：姿势、身材比例、服装轮廓和发型体块必须保留，脸部则按成片尺寸主动减笔，不再尝试重新生成一张写实人脸；非人物锚点继续忠实保留材质。其余场景遵循“保留／合并／省略／露白”：决定性结构留下，次要景物压成浅淡大块墨色，低价值细节直接消失，一块连续白场成为主动构图。主体需要分离时，只加入一个由邻近场景结构或柔和墨晕塑成的浅至中灰承托层；它必须比主体安静，不能成为第二主角。结果不能像照片简单去色，并加入低调的银盐电影质感。

## 工作流

```text
照片
→ 自动选择一种模式
→ 提出2–3个同模式候选
→ 用户选择，可同时提供准确时间
→ 生成16:9预览
→ 检查比例、场景真实性和彩色泄漏
→ 最多定向修正一次
→ 用户确认后保存
```

## 两种模式

- **决定性元素：**选择面积较小、可以分离、对照片意义重要的人物或物体。最终彩色元素绝不能达到画面一半。
- **决定性色彩：**只有不存在合格元素时才使用。只保留一种源色中最有叙事价值的局部，其他相同色相仍然变为黑白。

## 安装

使用 Codex 内置的 Skill Installer 直接从 GitHub 安装：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo an-an-618/decisive-frame-skill \
  --path skills/decisive-frame-v1
```

也可以从本地仓库复制可安装的 Skill：

```bash
mkdir -p ~/.codex/skills
cp -R skills/decisive-frame-v1 ~/.codex/skills/
```

如果没有立即出现，请重启 Codex。

可选的确定性检测脚本使用 Pillow。如果当前环境没有 Pillow，仍可继续进行视觉检查，但不得在用户任务中静默安装依赖。

## 使用

上传照片后调用：

```text
用 $decisive-frame-v1 处理这张照片。
```

Skill 会先返回候选。回复 `A`、`B` 或 `C` 进行选择。如需边缘时间，可以一起提供：

```text
B — 17:42
```

只回复 `B` 时，Skill 会直接生成，并保持画面完全无字。

## 仓库结构

```text
skills/decisive-frame-v1/   可安装 Skill
tests/                      检测脚本测试
evals/                      行为场景与本地测试清单
examples/                   仅存放逐张批准的公开案例
docs/                       设计与实施计划
```

## 隐私与案例媒体

原始照片只用于用户请求的当前任务。除非用户明确授权，不得浏览、分享、上传、提交或复制到项目中。

允许本地测试不等于允许公开。每个公开案例都必须单独获得原图和成品的发布授权。案例媒体权限独立于仓库代码和文档许可证。

## 许可证

Skill 代码和文档采用 [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)。商业用途需要获得许可方的单独授权。
