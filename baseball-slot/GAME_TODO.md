# 全壘打投注機 — TODO

依 `/game-develop` 五階段推進。每階段完成標 ✅。

---

## Phase 0：診斷對齊 ✅
- ✅ 從 0 起跑，無既有 HTML / SPEC
- ✅ 數值表確認（RTP 93%）
- ✅ 視覺風格鎖定 b. 寫實球場風
- ✅ 專案目錄 `C:/Users/Tim/.claude/baseball-slot/`

## Phase 1：Design system ✅
- ✅ CSS variables 內嵌於 HTML（不跑 design-consultation，數值/配色已在 SPEC 鎖定）
  └ 理由：機台類遊戲視覺單一（一個場景），design-consultation 過重

## Phase 2：素材清單規劃 ✅
- ✅ Emoji 對照表完成（見 SPEC）
- ✅ TODO 素材分區建立（見 Phase 3）

## Phase 3：批次生圖（emoji → 真圖）✅

### 背景類
- ✅ 球場全景背景：`assets/backgrounds/field-night.png` (2.95 MB, 9:16/2K)
  └ 寫實夜場，主審視角，無人物，retake 0 次

### 角色類（v2 重生：改用 generate2dsprite + 含動畫 frame）
- ✅ 打者 sprite sheet（背面 2 frame，512×512 RGBA）：
  - `assets/portrait/batter_idle.png`（預備揮棒，棒高舉肩後）
  - `assets/portrait/batter_swing.png`（揮棒完成，棒已揮過）
  - `assets/portrait/batter.png` = idle frame 副本
  - 藍衣白褲深藍頭盔 + 背號 7
- ✅ 投手 sprite sheet（正面 2 frame，512×512 RGBA）：
  - `assets/portrait/pitcher_windup.png`（抬腿持球至耳邊）
  - `assets/portrait/pitcher_release.png`（左腳前踏出手後）
  - `assets/portrait/pitcher.png` = windup frame 副本
  - 白衣灰褲紅帽紅 stockings（v1 的褲色偏差已修正）

### UI 類
- ✅ 棒球 sprite：`assets/ui/ball.png` (256×256 RGBA 真透明)
  └ v1 用 imagen 生 RGB 無 alpha，v2 改用 generate2dsprite single mode 走 chroma key
- ✅ 金幣 icon：`assets/ui/coin.png` (37 KB, 128×128 透明)
  └ 中央用紅縫線圖案而非 BB 字（agent 判斷視覺辨識度更好）
- ✅ PITCH 按鈕：`assets/ui/btn-pitch.png` (85 KB, 600×160 透明)
  └ 比例改 16:9 + padding（API 不支援 3.75:1）

## Phase 4：素材整合 ✅
- ✅ 球場背景：移除 CSS 模擬 div (.stands/.scoreboard/.wall/.outfield/.infield)，改 background-image
- ✅ 打者 emoji → `<img>` (width 38%) + **frame swap 動畫**（idle ↔ swing）
- ✅ 投手 emoji → `<img>` (width 24%) + **frame swap 動畫**（windup ↔ release）
- ✅ 球 emoji → 用 background-image（移除 CSS 紅縫線偽元素）
- ✅ 籌碼 ● → coin.png (16×16)
- ✅ PITCH button → img + .disabled class（取代 :disabled 偽元素）
- ✅ 移除多餘 .bat 元素（立繪本身已含棒子）
- ✅ 移除 dead code (animatePitch 內 batter/bat 變數)
- ✅ Sprite preload（new Image() 在啟動時預載 swing / release frame，避免動畫當下才載）
- ✅ resetField 復位：每次 pitch 結束後 batter 切回 idle、pitcher 切回 windup
- ✅ Asset reference 一致性檢查通過（6 張全對得到實檔）

## Phase 5：Polish ✅
- ✅ 5.1 Balance：fallback simulation（python，10000 場 × 100 球）
  └ 理論 RTP 93.00% 完美命中；破產率 18.7%；平均結餘 711；中位 350
  └ ⚠ flag：破產率 18.7% 偏高，待用戶試玩反饋是否調整失敗權重
- ✅ 5.2 Dialogue：12 種結果播報詞自寫（機台廣播員 persona）
  └ 中性敘述 → 熱血播報感（"BALL! 沒出棒" / "STRIKE! 揮空" / "正中央 全壘打！" 等）
- ✅ 5.3 Design review：self-walkthrough（沒 chrome 權限，跑靜態檢查）
  └ ID 一致性、class 用量、HTML 結構、asset reference 全 pass
- ✅ 5.4 QA：邏輯 walkthrough（沒 browser 跑 end-to-end）
  └ 抓到 1 個 edge case：餘額 0 時 `Math.max(...[].filter(...))` 回 -Infinity，已修
  └ 連點 / 餘額不夠 / 動畫期切下注 / reset / 12 outcome trigger 邏輯全 pass

## 額外加分（已做）
- ✅ 音效：Web Audio API
  └ 投球 whoosh / 揮棒 whoosh / 球棒 crack / 贏家音階 / Jackpot arpeggio / 失敗下行 / 點擊 click
  └ 大獎倍率高時音階多兩個音
  └ Mute toggle（🔊/🔇）
- ✅ 賠率表 toggle（右下角 ?）
- ✅ 餘額破產 reset 機制（GAME OVER modal + RESET 1000）
- ✅ Debug 熱區 toggle（右上「熱區」按鈕，顯示 12 個結果區色塊）

## 沒做（非 critical）
- 連勝 / 連敗 streak 視覺反饋（PR 後增量）

---

## 行數監控
- 最終：906 行（HTML+CSS+JS 單檔）
- 5000 警示（仍有 ~4100 行空間）

---

## 已知限制（沒辦法做完的）
- **沒 browser QA 端到端測試**：使用者拒絕 chrome MCP 的 localhost 權限（先前對話）。Phase 5.3-4 跑的是靜態檢查 + 邏輯 walkthrough，沒實際在瀏覽器跑過互動。
- 解法：使用者可以在檔案總管雙擊 `index.html` 直接 file:// 開瀏覽器試玩，或自行起 local server。
