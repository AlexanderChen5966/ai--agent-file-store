# Changelog

所有此 Agent Skill 的重要變更都會記錄在此文件中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，
並且遵循 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [1.0.0] - 2026-01-28

### Added
- 初始版本發布
- 支援 API 文件轉 PDF
- 支援 Postman Collection 生成
- 支援 UML 流程圖生成
- 支援資料庫架構圖生成
- 完整的錯誤處理指引
- 中文字型支援
- macOS 和 Linux 平台支援

### Features
- 一鍵執行 `generate_all.sh`
- 個別腳本獨立執行
- 自動環境檢查與依賴安裝
- Python 虛擬環境自動管理

### Documentation
- 完整的 SKILL.md 說明文件
- README.md 使用指南
- CHANGELOG.md 版本記錄

### Scripts
- `generate_all.sh` - 主建置腳本
- `api_to_postman.py` - Postman Collection 生成器
- `convert_api_pdf.py` - PDF 生成器
- `convert_api_to_uml_flow.py` - UML 流程圖生成器
- `dbml_to_png.py` - DBML 架構圖生成器
- `draw_schema.py` - SQL Schema 架構圖生成器
- `template.html` - PDF 模板

## [Unreleased]

### Planned
- 支援 OpenAPI/Swagger 格式輸出
- 英文多語言支援
- 平行處理優化
- Windows 原生支援
- 自動化測試腳本
