# TestyPDF

一個使用 Python 生成 PDF 文件的簡單專案。

## 功能特色

### 核心功能
- ✅ **TXT 轉 PDF** - 將純文字檔案轉換為 PDF 文件
- ✅ **生成空白 PDF** - 快速建立空白的 PDF 文件
- ✅ **生成多份副本** - 一次生成多份相同內容的 PDF
- 🎲 **隨機行數生成** - 每份 PDF 隨機選擇不同的行數和內容
- 🌏 **多編碼支援** - 自動偵測並支援多種編碼（UTF-8、Big5、GBK、GB2312 等）

### 文件處理
- 📄 **自動換行處理** - 當文字過長時自動分行（每行最多 80 字元）
- 📑 **自動分頁** - 內容超過一頁時自動建立新頁面
- 📏 **版面配置** - 預設 A4 紙張大小，內建適當的邊距設定

### 設定與自訂
- 🗂️ **自訂輸出目錄** - 可設定 PDF 檔案的預設輸出位置
- 🔧 **自動建立目錄** - 若輸出目錄不存在會自動建立
- 📝 **彈性檔名處理** - 可自動生成或手動指定輸出檔名
- 🐍 **Python API** - 可作為模組匯入到其他 Python 程式中使用

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

### 2. 生成多份 PDF 副本

```bash
# 生成 3 份相同內容的 PDF
python generate_pdf.py input.txt --copies 3
# 產生: input_1.pdf, input_2.pdf, input_3.pdf

# 使用簡短參數 -c
python generate_pdf.py input.txt -c 5
# 產生: input_1.pdf, input_2.pdf, input_3.pdf, input_4.pdf, input_5.pdf

# 指定基礎檔名並生成多份
python generate_pdf.py input.txt output --copies 3
# 產生: output_1.pdf, output_2.pdf, output_3.pdf
```

### 3. 隨機行數生成（每份 PDF 內容不同）

```bash
# 生成 3 份 PDF，每份隨機選擇不同的行數和內容
python generate_pdf.py input.txt --random --copies 3
# 範例輸出：
#   第 1 份：隨機選擇了 6 行（第 1, 5, 6, 7, 9, 10 行）
#   第 2 份：隨機選擇了 10 行（全部）
#   第 3 份：隨機選擇了 8 行（第 1, 2, 3, 4, 5, 6, 8, 9 行）

# 使用簡短參數 -r
python generate_pdf.py input.txt -r -c 5

# 指定基礎檔名
python generate_pdf.py input.txt output -r -c 3
# 產生: output_1.pdf, output_2.pdf, output_3.pdf（每份內容隨機）
```

### 4. 生成空白 PDF

```bash
python generate_pdf.py
```

執行後會在當前目錄生成空白的 `output.pdf` 文件。

### 5. 在程式中使用

```python
from generate_pdf import txt_to_pdf, txt_to_pdf_multiple, txt_to_pdf_random_lines, create_blank_pdf

# 將 txt 轉換為 PDF
txt_to_pdf("my_text.txt", "my_output.pdf")

# 生成多份 PDF 副本（相同內容）
txt_to_pdf_multiple("my_text.txt", copies=5)
# 產生: my_text_1.pdf, my_text_2.pdf, ..., my_text_5.pdf

# 生成多份隨機內容的 PDF（每份內容不同）
txt_to_pdf_random_lines("my_text.txt", copies=3)
# 每份 PDF 隨機選擇不同的行數和行號

# 指定基礎檔名生成多份
txt_to_pdf_multiple("my_text.txt", copies=3, base_pdf_filename="custom_name")
# 產生: custom_name_1.pdf, custom_name_2.pdf, custom_name_3.pdf

# 生成空白 PDF
create_blank_pdf("blank.pdf")
```

## 需求

- Python 3.6+
- reportlab

## 授權

MIT License
