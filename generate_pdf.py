#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單的 PDF 生成器
使用 reportlab 庫來生成 PDF 文件
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# ==================== 設定區 ====================
# 預設 PDF 輸出目錄（設為 None 則使用當前目錄）
OUTPUT_DIR = None  # 例如: "/path/to/your/pdfs" 或 "./output"
# ===============================================


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
        with open(txt_filename, 'r', encoding='utf-8') as f:
            text_content = f.readlines()
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

    if len(sys.argv) > 1:
        # 如果有命令列參數，將 txt 轉為 PDF
        txt_file = sys.argv[1]
        pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
        txt_to_pdf(txt_file, pdf_file)
    else:
        # 沒有參數時，生成空白 PDF
        create_blank_pdf("output.pdf")
