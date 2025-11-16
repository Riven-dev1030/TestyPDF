# TestyPDF

一個使用 Python 生成 PDF 文件的簡單專案。

## 功能

- 使用 ReportLab 庫生成 PDF
- 支援文字、圖形等元素
- **將 TXT 文件轉換為 PDF**
- 自動處理換行和分頁
- 支援 UTF-8 編碼
- 易於擴展和自訂

## 安裝

```bash
pip install -r requirements.txt
```

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
