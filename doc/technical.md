# 《午夜酒店值班簿》技术文档

## 1. 技术栈

- React 18 + TypeScript 5 + Less + Vite 5，构建基址为 `./`。
- 主画面为 390 × 844 的响应式 DOM；建立镜头和结果使用本地 WebP，三条演出使用本地 H.264 MP4。
- Web Audio API 合成五拍反馈；`localStorage` 保存三份案件档案。
- 图片由 Aigram transit `gen-image` 制作；视频由正式首尾帧 `/video` 与 `/video_task` 接口串行制作。

## 2. 目录结构

```text
src/MidnightHotelLedger/
├── MidnightHotelLedger.tsx         # 状态机、媒体预载、输入和收藏
├── MidnightHotelLedger.less        # 酒红皮革 / 黄铜终端 UI
├── components.tsx                  # 共享首帧、视频舞台、回退和 SVG 图标
├── data.ts                          # 三条处置与报告文案
├── i18n/index.ts                    # zh / en
├── utils/sounds.ts                  # Web Audio 五拍反馈
└── types.ts                         # 状态与结局类型
public/generated/
├── hotel_start.webp                # 三条视频共同精确首帧
├── plug_cinema.mp4 / plug_end.webp
├── maintenance_cinema.mp4 / maintenance_end.webp
└── suite_cinema.mp4 / suite_end.webp
_production/
├── generate_hotel_cinema.py        # 串行首尾帧与视频制作、重试和修订
├── hotel_cinema_manifest.json      # URL、提示词和任务 ID
├── generate_poster.py              # 正式海报与定向修图
├── poster_manifest.json            # 海报追溯证据
└── rejected/                       # 未发布的海景首帧和人物重复版本
```

## 3. 核心模块

- `src/game-id.ts` 注入永久 UUID `03b3aa05-0634-47d8-bab6-4effc6271007`，供平台会话能力统一识别。

- 状态机为 `cover → incident → footage → report → incident`；三条分支统一在 650 / 2200 / 4100 / 5200 ms 推进。
- `HotelStill`、`Footage` 静态层和视频 `poster` 都引用 `./generated/hotel_start.webp`，确保选择前、点击当帧和媒体等待态像素来源一致。
- `Footage` 以 `plug / maintenance / suite` 映射独立视频、尾帧和四段字幕；`canplay` 后 180 ms 淡入，`error` 时保留首帧并继续结果时间线。
- 结果态直接渲染分支尾帧，不依赖解码器停在视频最后一帧。
- 三条视频均为 H.264 + AAC、768 × 1024、24 fps、5.041667 秒，并在封面或案件页通过临时 video 元素预载。
- 手机宽度不超过 520px 时，视口比例只取 `clientWidth / 390`，终端始终横向铺满；缩放后的内容高度写入 `--mhl-height`，短屏通过页面纵向滚动访问完整内容，不再按高度二次缩小。桌面端保持 390 × 844 居中展示。
- 收藏写入 `midnight_hotel_ledger_reports_v1`；Web Audio、视频和预载失败均不阻塞归档。

## 4. 扩展点

- 新增案件：增加场景层状态与共享首帧，为每条处置在 `components.tsx` 注册视频、尾帧及字幕。
- 新增或重做媒体：修改 `_production/generate_hotel_cinema.py`，先用 `--start-only` 审首帧，再生成尾帧和视频。
- 修改终端 UI：编辑 Less 中的 `wine / brass / night / paper / sea / alarm` 视觉 token 和屏幕区块。
- 修改双语文案：编辑 `i18n/index.ts` 与 `data.ts`。
- 调整节奏：同步修改 `MidnightHotelLedger.tsx` 定时点、视频提示词和音效节拍。
- 发布：保留 `base: './'`、永久 UUID、七个本地媒体文件和专属存储键。
