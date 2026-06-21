# KMB 巴士即時到站監控面板 — 系統操作文件

- **系統名稱**: KMB Real-time Bus ETA Dashboard
- **程式碼位置**: `C:\Works\OpenCode\kmb-web`
- **GitHub**: `https://github.com/dannylky/kmb-web`
- **目前版本**: **v0.12.1**
- **上次更新**: 2026-06-21

---

## 1. 系統設計

### 1.1 架構概覽

```
┌──────────────────────────────────────────────────────┐
│                   瀏覽器 (Client)                       │
│  ┌──────────────────────────────────────┐            │
│  │        index.html (SPA)              │            │
│  │  ┌────────────────────────────────┐  │            │
│  │  │  分頁系統                       │  │            │
│  │  │  ├── ST330 恒大概覽              │  │            │
│  │  │  ├── YT262 柯士甸道西            │  │            │
│  │  │  ├── ST884 廣源                 │  │            │
│  │  │  ├── ST894 黃泥頭               │  │            │
│  │  │  ├── ST790 大老山               │  │            │
│  │  │  └── 我的路線 (自訂書籤)         │  │            │
│  │  └────────────────────────────────┘  │            │
│  └──────────────────────────────────────┘            │
│           │                  │                        │
│           ▼                                        │
│  ┌──────────────┐                                   │
│  │ KMB Open API  │                                   │
│  │ (CORS OK)     │                                   │
│  └──────┬───────┘                                   │
│         │                                           │
└─────────┼────────────────────────────────────────────┘
          │
          ▼
  data.etabus.gov.hk
  (KMB only)
```

### 1.2 元件說明

| 元件 | 位置 | 說明 |
|------|------|------|
| **index.html** | `kmb-web/index.html` | 單頁式應用 (SPA)，純前端，無需 build 工具。內含全部 HTML、CSS、JavaScript。 |

| **MCP-KMB-HK** | `C:\Works\OpenCode\MCP-KMB-HK` | FastMCP 伺服器，提供 8 個 KMB API 工具給 opencode 使用。與網頁獨立運作。 |

### 1.3 資料流

1. **KMB 到站資料**: 瀏覽器直接呼叫 `https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/{stopId}`（API 支援 CORS `*`）
2. **路線列表**: 瀏覽器直接呼叫 `https://data.etabus.gov.hk/v1/transport/kmb/route/`
3. **GMB 路線**: 前端硬編碼 route config，無 API 呼叫；路線顯示在「暫未服務」欄

### 1.4 API 端點一覽

| API | 基礎 URL | CORS 支援 |
|-----|---------|-----------|
| KMB Open API | `https://data.etabus.gov.hk/v1/transport/kmb` | ✅ 原生支援 |
| GMB API | `https://data.etagmb.gov.hk` | ❌ 不再使用 |

### 1.5 分頁配置

| 分頁 ID | 顯示名稱 | Stop IDs | 路線數 |
|---------|---------|----------|--------|
| hsuhk | 🏫 恒大概覽 (ST330) | `3F01C915E856B018`, `BC39BFC3C7BC3009` | 所有經停路線 |
| mplus | 🎨 柯士甸道西 (YT262) | `0CC0B21EFF42EE19` | 9 (固定) |
| st884 | 🚌 廣源 (ST884) | 4 個停車點 | 8 (固定) |
| st894 | 🚌 黃泥頭 (ST894) | 4 個停車點 | 6 (固定) |
| st790 | 🚌 大老山 (ST790) | `3114213F8975F536` | 24 (固定) |
| bookmarks | 📌 我的路線 | 動態（自訂） | 使用者自訂 |

### 1.6 更新機制

- 自動重新整理：每 10 秒一次（預設開啟）
- 只在目前活躍分頁重新整理
- 使用者可透過 checkbox 關閉自動更新
- 路線若無 ETA 資料，自動移至「暫未服務」頂欄

---

## 2. 操作程序

### 2.1 快速啟動

```powershell
cd C:\Works\OpenCode\kmb-web

# 1. 啟動網頁伺服器（選擇一種方式）
# 選項 A: Python HTTP server
python -m http.server 8080

# 選項 B: 直接開啟 HTML（部分瀏覽器不支援 file:// fetch）
# 直接雙擊 index.html

# 2. 開啟瀏覽器
# http://localhost:8080/
```

### 2.2 前置需求

- Python 3.8+（測試於 3.12）
- 瀏覽器：Chrome 90+ / Edge 90+ / Firefox 90+ / Safari 15+
- 無需後端伺服器，KMB API 直接從瀏覽器呼叫

### 2.3 發布至 GitHub Pages

```powershell
cd C:\Works\OpenCode\kmb-web
git add -A
git commit -m "vX.Y.Z: 變更說明"
git push origin master --tags
```

GitHub Pages URL: `https://dannylky.github.io/kmb-web/`

### 2.4 開發用啟動（含 opencode MCP）

```powershell
# 啟動 opencode（會自動啟動 MCP-KMB-HK 伺服器）
opencode
```

### 2.5 故障排除

| 問題 | 原因 | 解決方法 |
|------|------|---------|
| 所有路線顯示「暫未服務」 | KMB API 無法存取或網路問題 | 檢查網路連線，或 KMB API 暫時維護 |
| 搜尋無結果 | 路線列表未載入 | 重新整理頁面 |

---

## 3. 版本編號系統

### 3.1 規則

採用 **Semantic Versioning (SemVer) 2.0**：

```
vMAJOR.MINOR.PATCH
```

| 層級 | 定義 | 範例 |
|------|------|------|
| **MAJOR** | 重大重新設計、不相容的 API 或架構變更 | `v1.0.0` — 首次穩定版本 |
| **MINOR** | 新增功能（新分頁、新路線組、新 Proxy） | `v0.9.0` — 新增 GMB Proxy |
| **PATCH** | 問題修正、樣式調整、效能改善 | `v0.8.1` — 修正某路線 ETA 顯示錯誤 |

- v0.x.x：開發階段（正式版前）
- v1.0.0：首次穩定版本

### 3.2 版本標記方式

- Git tag: `git tag vX.Y.Z`
- commit message 格式: `vX.Y.Z: 變更說明`
- 每次功能變更（MINOR）或修正（PATCH）即產生新版本

---

## 4. 變更歷史

| 版本 | 日期 | 類型 | 說明 | Commit |
|------|------|------|------|--------|
| **v0.1.0** | 2026-06-20 | — | 初始版本：KMB ETA bookmarks 面板，含 HSUHK 及 M+ 儀表板 | `8c879e5` |
| **v0.2.0** | 2026-06-20 | MINOR | 儀表板改為 4 欄網格顯示 | `564d98d` |
| **v0.3.0** | 2026-06-20 | MINOR | 新增 ST884（廣源）分頁，含 3 條 KMB 路線 | `a75bff6` |
| **v0.4.0** | 2026-06-20 | MINOR | ST884 擴充為多站點查詢，加入 82X、82C、85A、49X、804、806A | `6aeb232` |
| **v0.5.0** | 2026-06-20 | MINOR | 新增 ST894（黃泥頭）分頁，含 6 條 KMB 路線 + GMB 65K、806A | `976a079` |
| **v0.6.0** | 2026-06-20 | MINOR | 新增 ST790（大老山隧道）分頁，含 24 條 KMB 路線 | `6882e70` |
| **v0.6.1** | 2026-06-20 | PATCH | HSUHK 分頁更名為 ST330 | `c3df0b1` |
| **v0.6.2** | 2026-06-20 | PATCH | M+ 分頁更名為 YT262 | `aa2b8df` |
| **v0.6.3** | 2026-06-20 | PATCH | 統一全部分頁標題格式為 `名稱 (編號)` | `1a0a4a6` |
| **v0.7.0** | 2026-06-20 | MINOR | 流動裝置響應式版面改善（可滾動分頁、縮小間距） | `2a5de6b` |
| **v0.7.1** | 2026-06-21 | PATCH | ST884 加入 84M 路線 | `321fb25` |
| **v0.8.0** | 2026-06-21 | MINOR | 無服務路線改為頂欄「暫未服務」統一顯示 | `5acaf41` |
| **v0.8.1** | 2026-06-21 | PATCH | 無服務路線 ETA 恢復時自動回到正常卡片區 | `5acaf41`（同次修正） |
| **v0.9.0** | 2026-06-21 | MINOR | 新增 `gmb_proxy.py` CORS Proxy；index.html 切換至 proxy URL 解決 GMB CORS 封鎖 | — |
| **v0.10.0** | 2026-06-21 | MINOR | KMB-first：綠Van路線先查 KMB API（有資料則用），無資料時才 fallback 至 GMB proxy | `17ffc30` |
| **v0.11.0** | 2026-06-21 | MINOR | 移除所有 GMB proxy 相關程式碼，只保留 KMB API；刪除 `gmb_proxy.py`、GMB route configs、GMB fetch 函數、綠Van badge 及相關渲染邏輯 | `1276d38` |
| **v0.12.0** | 2026-06-21 | MINOR | 重新加入 GMB 路線 config 作為靜態佔位符，顯示於各 dashboard 的「暫未服務」欄（僅 KMB API，無 proxy） | `1191574` |
| **v0.12.1** | 2026-06-21 | PATCH | 從「暫未服務」欄排除所有 GMB 路線（靜態佔位符只會佔用版面，無實際用途） | `181d662` |

---

## 5. 相關檔案

| 檔案 | 說明 |
|------|------|
| `index.html` | 主網頁（單頁應用） |

| `opencode.json` | opencode MCP 設定檔 |
| `OPERATIONS.md` | 本文件 |
| `MCP-KMB-HK/server.py` | FastMCP KMB API 工具伺服器 |
| `MCP-KMB-HK/pyproject.toml` | Python 專案設定與相依性 |
| `MCP-KMB-HK/KMB_API.txt` | KMB API 文件記錄 |

---

## 6. 附錄

### 6.1 KMB API 常用端點

```
GET /route/                             — 所有路線
GET /route/{route}/{dir}/{st}           — 路線詳細資料
GET /stop/{stopId}                      — 站點詳細資料
GET /stop-eta/{stopId}                  — 站點 ETA
GET /route-stop/{route}/{dir}/{st}      — 路線經停站
```

### 6.2 開發備註

- KMB API 回傳的 `eta` 欄位為 ISO 8601 時間字串，由前端計算剩餘分鐘數
- GMB API 回傳的 `diff` 欄位為整數分鐘數
- 路線排序規則：純數字路線按數值排序，英數字混合路線按自然排序
