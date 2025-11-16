# TestyPDF

一個使用 Python 生成 PDF 文件的簡單專案。

## 功能

- 使用 ReportLab 庫生成 PDF
- 支援文字、圖形等元素
- **將 TXT 文件轉換為 PDF**
- 自動處理換行和分頁
- 支援 UTF-8 編碼
- **可自訂 PDF 輸出目錄**
- 易於擴展和自訂

## 安裝

```bash
pip install -r requirements.txt
```

## 設定

### 自訂 PDF 輸出目錄

打開 `generate_pdf.py`，在檔案開頭找到設定區：

```python
# ==================== 設定區 ====================
# 預設 PDF 輸出目錄（設為 None 則使用當前目錄）
OUTPUT_DIR = None  # 例如: "/path/to/your/pdfs" 或 "./output"
# ===============================================
```

修改 `OUTPUT_DIR` 來設定您想要的輸出目錄：

```python
# 使用絕對路徑
OUTPUT_DIR = "/home/user/my_pdfs"

# 或使用相對路徑
OUTPUT_DIR = "./pdf_output"

# 使用當前目錄（預設）
OUTPUT_DIR = None
```

如果指定的目錄不存在，程式會自動建立。

## 使用方法

### 1. 將 TXT 文件轉換為 PDF

```bash
# 基本用法（PDF 檔名自動生成）
python generate_pdf.py input.txt

# 指定輸出的 PDF 檔名
python generate_pdf.py input.txt output.pdf
```

### 2. 生成空白 PDF

```bash
python generate_pdf.py
```

執行後會在當前目錄生成空白的 `output.pdf` 文件。

### 3. 在程式中使用

```python
from generate_pdf import txt_to_pdf, create_blank_pdf

# 將 txt 轉換為 PDF
txt_to_pdf("my_text.txt", "my_output.pdf")

# 生成空白 PDF
create_blank_pdf("blank.pdf")
```

## 需求

- Python 3.6+
- reportlab

## 授權

MIT License
