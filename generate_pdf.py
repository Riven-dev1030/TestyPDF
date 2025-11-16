#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單的 PDF 生成器
使用 reportlab 庫來生成 PDF 文件
"""

import os
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# ==================== 設定區 ====================
# 預設 PDF 輸出目錄（設為 None 則使用當前目錄）
OUTPUT_DIR = None  # 例如: "/path/to/your/pdfs" 或 "./output"
# ===============================================


def _read_text_file(filename):
    """
    讀取文字檔案，自動嘗試多種編碼格式

    Args:
        filename: 檔案路徑

    Returns:
        文件內容（行列表）

    Raises:
        FileNotFoundError: 檔案不存在
        Exception: 無法讀取檔案
    """
    # 嘗試的編碼列表（依常見程度排序）
    encodings = ['utf-8', 'big5', 'gbk', 'gb2312', 'utf-16', 'cp950', 'latin1']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.readlines()
            print(f"✓ 成功使用 {encoding.upper()} 編碼讀取檔案")
            return content
        except UnicodeDecodeError:
            # 這個編碼不對，嘗試下一個
            continue
        except Exception as e:
            # 其他錯誤（如檔案不存在），直接拋出
            raise e

    # 如果所有編碼都失敗
    raise Exception(f"無法讀取檔案，已嘗試的編碼: {', '.join(encodings)}")


def _get_output_path(filename):
    """
    取得完整的輸出路徑，並確保輸出目錄存在

    Args:
        filename: 檔案名稱

    Returns:
        完整的輸出路徑
    """
    if OUTPUT_DIR is None:
        return filename

    # 確保輸出目錄存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"已建立輸出目錄: {OUTPUT_DIR}")

    return os.path.join(OUTPUT_DIR, os.path.basename(filename))


def txt_to_pdf(txt_filename, pdf_filename=None):
    """
    讀取 txt 文件並轉換為 PDF

    Args:
        txt_filename: 要讀取的 txt 檔案路徑
        pdf_filename: 輸出的 PDF 檔案名稱（若未指定，則使用 txt 檔案名稱加上 .pdf）
    """
    # 如果沒有指定 PDF 檔案名稱，則使用 txt 檔案名稱
    if pdf_filename is None:
        pdf_filename = os.path.basename(txt_filename).rsplit('.', 1)[0] + '.pdf'

    # 取得完整的輸出路徑
    pdf_filename = _get_output_path(pdf_filename)

    # 讀取 txt 檔案內容
    try:
        text_content = _read_text_file(txt_filename)
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 {txt_filename}")
        return
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return

    # 建立 canvas 物件
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    # 設定字型和大小
    c.setFont("Helvetica", 12)

    # 設定起始位置和行距
    y_position = height - 2*cm
    line_height = 0.6*cm
    margin_left = 2*cm
    margin_right = width - 2*cm
    margin_bottom = 2*cm

    # 逐行寫入內容
    for line in text_content:
        line = line.rstrip('\n')  # 移除換行符號

        # 檢查是否需要換頁
        if y_position < margin_bottom:
            c.showPage()  # 新增頁面
            c.setFont("Helvetica", 12)
            y_position = height - 2*cm

        # 處理過長的行（簡單換行處理）
        if len(line) > 80:
            # 將長行分割成多個短行
            chunks = [line[i:i+80] for i in range(0, len(line), 80)]
            for chunk in chunks:
                c.drawString(margin_left, y_position, chunk)
                y_position -= line_height
                if y_position < margin_bottom:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 2*cm
        else:
            c.drawString(margin_left, y_position, line)
            y_position -= line_height

    # 儲存 PDF
    c.save()
    print(f"已將 {txt_filename} 轉換為 PDF: {pdf_filename}")


def txt_to_pdf_multiple(txt_filename, copies=1, base_pdf_filename=None):
    """
    讀取 txt 文件並生成多份 PDF

    Args:
        txt_filename: 要讀取的 txt 檔案路徑
        copies: 要生成的 PDF 份數（預設為 1）
        base_pdf_filename: 基礎 PDF 檔案名稱（若未指定，則使用 txt 檔案名稱）

    Returns:
        生成的 PDF 檔案路徑列表
    """
    if copies < 1:
        print("錯誤: 份數必須至少為 1")
        return []

    # 讀取 txt 檔案內容（只讀取一次，提高效率）
    try:
        text_content = _read_text_file(txt_filename)
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 {txt_filename}")
        return []
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return []

    # 決定基礎檔名
    if base_pdf_filename is None:
        base_pdf_filename = os.path.basename(txt_filename).rsplit('.', 1)[0]
    else:
        # 移除 .pdf 副檔名（如果有的話）
        base_pdf_filename = base_pdf_filename.rsplit('.pdf', 1)[0]

    generated_files = []

    # 生成多份 PDF
    for i in range(1, copies + 1):
        # 生成檔名
        if copies == 1:
            pdf_filename = f"{base_pdf_filename}.pdf"
        else:
            pdf_filename = f"{base_pdf_filename}_{i}.pdf"

        # 取得完整的輸出路徑
        pdf_filename = _get_output_path(pdf_filename)

        # 建立 canvas 物件
        c = canvas.Canvas(pdf_filename, pagesize=A4)
        width, height = A4

        # 設定字型和大小
        c.setFont("Helvetica", 12)

        # 設定起始位置和行距
        y_position = height - 2*cm
        line_height = 0.6*cm
        margin_left = 2*cm
        margin_right = width - 2*cm
        margin_bottom = 2*cm

        # 逐行寫入內容
        for line in text_content:
            line = line.rstrip('\n')  # 移除換行符號

            # 檢查是否需要換頁
            if y_position < margin_bottom:
                c.showPage()  # 新增頁面
                c.setFont("Helvetica", 12)
                y_position = height - 2*cm

            # 處理過長的行（簡單換行處理）
            if len(line) > 80:
                # 將長行分割成多個短行
                chunks = [line[i:i+80] for i in range(0, len(line), 80)]
                for chunk in chunks:
                    c.drawString(margin_left, y_position, chunk)
                    y_position -= line_height
                    if y_position < margin_bottom:
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y_position = height - 2*cm
            else:
                c.drawString(margin_left, y_position, line)
                y_position -= line_height

        # 儲存 PDF
        c.save()
        generated_files.append(pdf_filename)

        if copies == 1:
            print(f"已將 {txt_filename} 轉換為 PDF: {pdf_filename}")
        else:
            print(f"[{i}/{copies}] 已生成: {pdf_filename}")

    if copies > 1:
        print(f"\n✅ 成功生成 {copies} 份 PDF")

    return generated_files


def txt_to_pdf_random_lines(txt_filename, copies=1, base_pdf_filename=None):
    """
    讀取 txt 文件並生成多份 PDF，每份 PDF 隨機選擇不同的行數和內容

    Args:
        txt_filename: 要讀取的 txt 檔案路徑
        copies: 要生成的 PDF 份數（預設為 1）
        base_pdf_filename: 基礎 PDF 檔案名稱（若未指定，則使用 txt 檔案名稱）

    Returns:
        生成的 PDF 檔案路徑列表
    """
    if copies < 1:
        print("錯誤: 份數必須至少為 1")
        return []

    # 讀取 txt 檔案內容（只讀取一次，提高效率）
    try:
        text_content = _read_text_file(txt_filename)
    except FileNotFoundError:
        print(f"錯誤: 找不到檔案 {txt_filename}")
        return []
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return []

    total_lines = len(text_content)
    if total_lines == 0:
        print("錯誤: 檔案是空的")
        return []

    # 決定基礎檔名
    if base_pdf_filename is None:
        base_pdf_filename = os.path.basename(txt_filename).rsplit('.', 1)[0]
    else:
        # 移除 .pdf 副檔名（如果有的話）
        base_pdf_filename = base_pdf_filename.rsplit('.pdf', 1)[0]

    generated_files = []

    print(f"📄 原始檔案共有 {total_lines} 行")
    print(f"🎲 開始生成 {copies} 份隨機內容的 PDF...\n")

    # 生成多份 PDF
    for i in range(1, copies + 1):
        # 隨機決定要選幾行（至少 1 行，最多全部行數）
        num_lines = random.randint(1, total_lines)

        # 隨機選擇哪些行（從 0 開始的索引）
        selected_indices = sorted(random.sample(range(total_lines), num_lines))

        # 取得選中的行內容
        selected_lines = [text_content[idx] for idx in selected_indices]

        # 生成檔名
        if copies == 1:
            pdf_filename = f"{base_pdf_filename}.pdf"
        else:
            pdf_filename = f"{base_pdf_filename}_{i}.pdf"

        # 取得完整的輸出路徑
        pdf_filename = _get_output_path(pdf_filename)

        # 建立 canvas 物件
        c = canvas.Canvas(pdf_filename, pagesize=A4)
        width, height = A4

        # 設定字型和大小
        c.setFont("Helvetica", 12)

        # 設定起始位置和行距
        y_position = height - 2*cm
        line_height = 0.6*cm
        margin_left = 2*cm
        margin_right = width - 2*cm
        margin_bottom = 2*cm

        # 逐行寫入選中的內容
        for line in selected_lines:
            line = line.rstrip('\n')  # 移除換行符號

            # 檢查是否需要換頁
            if y_position < margin_bottom:
                c.showPage()  # 新增頁面
                c.setFont("Helvetica", 12)
                y_position = height - 2*cm

            # 處理過長的行（簡單換行處理）
            if len(line) > 80:
                # 將長行分割成多個短行
                chunks = [line[i:i+80] for i in range(0, len(line), 80)]
                for chunk in chunks:
                    c.drawString(margin_left, y_position, chunk)
                    y_position -= line_height
                    if y_position < margin_bottom:
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y_position = height - 2*cm
            else:
                c.drawString(margin_left, y_position, line)
                y_position -= line_height

        # 儲存 PDF
        c.save()
        generated_files.append(pdf_filename)

        # 顯示每份 PDF 的資訊
        line_numbers = [idx + 1 for idx in selected_indices]  # 轉換為 1-based 行號
        print(f"[{i}/{copies}] 已生成: {os.path.basename(pdf_filename)}")
        print(f"  → 隨機選擇了 {num_lines} 行: 第 {', '.join(map(str, line_numbers))} 行\n")

    print(f"✅ 成功生成 {copies} 份隨機內容的 PDF")

    return generated_files


def create_blank_pdf(filename="output.pdf"):
    """
    建立一個空白的 PDF 文件

    Args:
        filename: 輸出的 PDF 檔案名稱
    """
    # 取得完整的輸出路徑
    filename = _get_output_path(filename)

    # 建立 canvas 物件
    c = canvas.Canvas(filename, pagesize=A4)

    # 儲存空白 PDF
    c.save()
    print(f"已建立空白 PDF: {filename}")


if __name__ == "__main__":
    import sys

    # 解析命令列參數
    args = sys.argv[1:]
    copies = 1
    txt_file = None
    pdf_file = None
    random_mode = False

    # 處理命令列參數
    i = 0
    while i < len(args):
        if args[i] in ['--copies', '-c']:
            if i + 1 < len(args):
                try:
                    copies = int(args[i + 1])
                    i += 2
                    continue
                except ValueError:
                    print(f"錯誤: --copies 參數必須是數字")
                    sys.exit(1)
            else:
                print(f"錯誤: --copies 參數需要指定份數")
                sys.exit(1)
        elif args[i] in ['--random', '-r']:
            random_mode = True
            i += 1
        elif txt_file is None:
            txt_file = args[i]
            i += 1
        elif pdf_file is None:
            pdf_file = args[i]
            i += 1
        else:
            i += 1

    if txt_file:
        # 有 txt 檔案，轉換為 PDF
        if random_mode:
            # 隨機行數模式
            txt_to_pdf_random_lines(txt_file, copies, pdf_file)
        elif copies > 1:
            # 生成多份相同內容的 PDF
            txt_to_pdf_multiple(txt_file, copies, pdf_file)
        else:
            # 生成單份 PDF
            txt_to_pdf(txt_file, pdf_file)
    else:
        # 沒有參數時，生成空白 PDF
        create_blank_pdf("output.pdf")
