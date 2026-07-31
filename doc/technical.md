# 《午夜酒店值班簿》技术文档

## 1. 技术栈

- React 18 + TypeScript 5 + Less + Vite 5，构建基址为 `./`。
- 主画面为响应式 DOM；每场建立画面使用本地 WebP，九种结果使用本地 H.264 MP4 与确定性的尾帧回退。
- Web Audio API 合成操作与结算反馈；`localStorage` 保存九份影像记录。
- 图片由 Aigram transit `gen-image` 制作，视频由正式首尾帧 `/video` 与 `/video_task` 接口生成。

## 2. 目录结构

```text
src/MidnightHotelLedger/
├── MidnightHotelLedger.tsx         # 三场状态机、轮换答案、媒体预载和收藏
├── MidnightHotelLedger.less        # 原有酒红皮革 / 黄铜终端视觉
├── refinement.less                 # 三步进度、极简选择与完整结局修订
├── components.tsx                  # 通用建立帧、视频舞台、回退与 SVG 图标
├── data.ts                          # 三场、九结果、媒体路径与双语文案
├── i18n/index.ts                    # 通用 zh / en 界面文本
├── utils/sounds.ts                  # 分级 Web Audio 反馈
└── types.ts                         # Scene、Outcome 与阶段类型
public/generated/                    # 三场首帧、九个尾帧和九条正式 MP4
_production/
├── generate_hotel_cinema.py        # 第一场制作流水线
├── hotel_cinema_manifest.json      # 第一场来源与任务记录
├── generate_extended_hotel_cinema.py
└── extended_hotel_cinema_manifest.json # 新六条影像的提示、URL 与 task ID
```

## 3. 核心模块

- `src/game-id.ts` 保存永久 UUID `03b3aa05-0634-47d8-bab6-4effc6271007`。
- 状态链为 `cover → setup → incident → footage → report → complete`。失败后重试当前场，通过后推进；第三场通过后显示章鱼接管夜班的完整结局。
- `data.ts` 以 `Scene[]` 绑定每场共享首帧和三个独立 `video/end`。`HotelStill` 与 `Footage` 使用相同建立帧，选择前、加载中和视频首帧连续；播放结束后直接显示指定尾帧。
- 视频使用 `autoPlay muted playsInline preload="auto"`。若解码失败，画面保留尾帧并按回退计时进入报告，媒体错误不会锁死故事。
- 每次进入或重试场景都会旋转三个答案；触屏和数字键共享 `displayedOutcomes`，避免通过选项形成固定位置规律。
- 手机端宽度始终铺满视口，390×844 与 320×568 都保持主画面优先；信息区只保留场景、问题、三个短答案和单一主按钮。
- 九种结果写入 `midnight_hotel_ledger_reports_v2`，键格式为 `sceneId:outcomeId`；声音设置使用独立 key。

## 4. 扩展点

- 新增案件：在 `data.ts` 添加场景和三个结果，同时为每个结果提供 MP4 与尾帧。
- 新增或重做媒体：复制 `_production/generate_extended_hotel_cinema.py` 的正式 transit 流程，并把 URL、任务 ID 和提示写入新 manifest。
- 调整 UI：基础皮革终端在 `MidnightHotelLedger.less`，三场进度、极简选项和结局在 `refinement.less`。
- 修改节奏：调整主组件的 setup 延时、视频结束回调和结果反馈，不要用固定文字替代真实演出。
- 接平台统计或云存档：在现有 `seen` 镜像外调用共享 runtime，保持永久 UUID 和 v2 语义键不变。
