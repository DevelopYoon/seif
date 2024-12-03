import subprocess
import pandas as pd
import shutil
import requests
from PIL import Image
from io import BytesIO
import os
import tempfile
import pymysql
import json
import re
from django.conf import settings
from sqlalchemy import create_engine
from openpyxl.drawing.image import Image as OpenpyxlImage
import openpyxl

# SQLAlchemy 엔진 생성
def get_sqlalchemy_engine():
    db_info = settings.DATABASES['default']
    db_url = f"mysql+pymysql://{db_info['USER']}:{db_info['PASSWORD']}@{db_info['HOST']}:{db_info['PORT']}/{db_info['NAME']}"
    return create_engine(db_url)
            
def download_image(url):
    """URL에서 이미지를 다운로드합니다."""
    if pd.isna(url) or not url.startswith(('http://', 'https://')):
        print(f"유효하지 않은 URL: {url}")
        return None
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return BytesIO(response.content)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP 오류 발생: {err} - URL: {url}")
    except Exception as err:
        print(f"기타 오류 발생: {err} - URL: {url}")
    return None

def insert_image(sheet, url, cell):
    """엑셀 시트의 특정 셀에 이미지를 삽입합니다."""
    img_data = download_image(url)

    if img_data:
        try:
            # 임시 파일 생성 (자동 삭제를 위해 delete=True 사용)
            with tempfile.NamedTemporaryFile(dir='media/tmp', delete=False, suffix=".jpg") as temp_file:
                temp_file.write(img_data.getvalue())  # BytesIO 객체의 바이트 내용 기록
                temp_file_path = temp_file.name

            # 엑셀 파일에 이미지 삽입
            img = OpenpyxlImage(temp_file_path)
            img.width = 385
            img.height = 467
            img.anchor = cell
            sheet.add_image(img)

        except Exception as e:
            print(f"이미지 처리 중 오류 발생: {e}")
    else:
        print(f"이미지 다운로드 또는 삽입 실패: {url}")




def queryCoNum(co_Num):
    query = """
            SELECT  *
            FROM tb_safetyEducation
            WHERE co_Num = %s
            ORDER BY educationDate DESC, title DESC 
            """
    return query        

def queryPlace(co_Num, title, educationDate):
    query = """
            SELECT  *
            FROM tb_safetyEducation
            WHERE co_Num = %s
              AND title = %s
              AND educationDate = %s
            ORDER BY educationDate DESC, title DESC
            """
    return query   


def createEduExcel(process_type, co_number, title=None, educationDate=None):

    engine = get_sqlalchemy_engine()

    # SQL 쿼리 실행 (특정 테이블의 특정 변수만 선택)

    query = None
    params = None
    if process_type == 1:
        query = queryCoNum(co_number)
        params = (co_number,)
    elif process_type == 2:
        query = queryPlace(co_number, title, educationDate)
        params = (co_number, title, educationDate)
        


    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params=params)             
                       
        # 엑셀 파일 열기
        excel_path = "/home/safeit/seif/media/안전교육실시현황.xlsx"
        fileDir = f'/home/safeit/seif/media/exel/{co_number}'
        if process_type==2:
            output_path = f'{fileDir}/안전교육실시현황_{title}_{educationDate}.xlsx'
        elif process_type==1:
            output_path = f'{fileDir}/안전교육실시현황_총합본.xlsx'

        output_path = output_path.replace(" ", "_")

        if not os.path.exists(fileDir):
            os.makedirs(fileDir, exist_ok=True)
            print(f"디렉토리를 생성했습니다: {fileDir}")
        else:
            print(f"디렉토리가 이미 존재합니다: {fileDir}")

        if os.path.isfile(output_path):
            print(f"파일이 존재합니다: {output_path}")
        else:
            print(f"파일이 존재하지 않습니다: {output_path}")
            shutil.copy(excel_path, output_path)
         
             
        
        wb = openpyxl.load_workbook(output_path)

        # 템플릿 시트 선택
        template_sheet = wb['안전교육기록서']
    
        # 안전교육기록서   
        current_sheet = None
        current_sheet_name = ""
        
        # .strftime("%Y-%m-%d")
        # 시트 이름 생성 (최대 31자 제한)
        for i, row in df.iterrows():
            new_sheet_name = f'안전교육기록서_{row["title"]}_{row["educationDate"]}'[:31]

            if current_sheet_name != new_sheet_name:
                current_sheet = wb.copy_worksheet(template_sheet)
                current_sheet.title = new_sheet_name
                current_sheet_name = new_sheet_name
            
            peopleListPic = row["peopleListPic"]
            placePic = row["placePic"]
            
            current_sheet['G5'] = row['educationDate']
            current_sheet['W5'] = row['startEducationTime']
            current_sheet['AC5'] = row['endEducationTime']
            current_sheet['G7'] = row['place']
            current_sheet['W7'] = row['manager']
            current_sheet['G13'] = row['detail']
            

            # 이미지 삽입
            if peopleListPic:
                insert_image(current_sheet, peopleListPic, 'B20')
            else:
                print("이미지가 없습니다. 이미지 처리 생략")
                

            if placePic:
                insert_image(current_sheet, placePic, 'R20')
            else:
                print("이미지가 없습니다. 이미지 처리 생략")
                       
        # 템플릿 시트 삭제
        if '안전교육기록서' in wb.sheetnames:
            del wb['안전교육기록서']
        
        wb.save(output_path)
        wb.close()
        
        # /home/safeit/seif/ 디렉토리 추출
        file_path = '/'.join(output_path.split('/')[4:7]) + '/'

        # 결과물 파일명 .pdf
        file_name = output_path.split('/')[-1].replace('.xlsx', '.pdf')

        # PDF 변환
        subprocess.run(f"libreoffice --headless --convert-to pdf {output_path}", shell=True)

        # 변환된 PDF 파일의 경로
        pdf_output = '/'.join(output_path.split('/')[:4])+'/'+file_name

        # PDF 파일을 결과 경로로 이동
        if os.path.exists(pdf_output):
            destination = file_path + file_name
            
            # 동일한 이름의 파일이 있으면 삭제 후 이동
            if os.path.exists(destination):
                os.remove(destination)
            
            shutil.move(pdf_output, destination)
        else:
            raise FileNotFoundError(f"PDF 변환에 실패했습니다: {pdf_output}")

        # 엑셀 파일 삭제
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # 파일 URL 반환
        file_url = f"http://211.237.0.230:10123/{file_path + file_name}"
        return file_url
         
    except Exception as e:
        print(f"엑셀 애플리케이션 종료 중 오류 발생: {e}")

