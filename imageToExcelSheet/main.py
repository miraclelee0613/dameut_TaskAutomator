# -*- coding: utf-8 -*-
# v240322
import os  # noqa: F401
import sys
from __init__ import source_folder_path
sys.path.append(source_folder_path)
from _workplace.library.junLib import strip_quotes
import pytesseract
import pandas as pd
from PIL import Image
import cv2

# Tesseract 경로 설정 (Windows의 경우)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def image_to_text(image_file_path):
    # 이미지 전처리 (옵션)
    image = cv2.imread(image_file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # 이미지에서 텍스트 추출
    text = pytesseract.image_to_string(Image.fromarray(thresh))
    print(text)
    return text

def text_to_excel(data, output_file_path='extracted_table.xlsx'):
    # 추출된 텍스트를 사용하여 Pandas DataFrame 생성 (여기서는 예시로 추출된 텍스트를 직접 사용)
    # 실제로는 텍스트를 분석하여 표 데이터로 변환하는 과정이 필요
    # data = {
    #     'Column1': ['Row1', 'Row2', 'Row3'],
    #     'Column2': ['Data1', 'Data2', 'Data3']
    # }
    df = pd.DataFrame(data)

    # DataFrame을 엑셀 파일로 저장
    df.to_excel(output_file_path, index=False)

if __name__ == "__main__":
    image_to_text(strip_quotes(input("Enter image file path : ")))