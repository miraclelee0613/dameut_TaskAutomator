# -*- coding: utf-8 -*-
# v240322
import os  # noqa: F401
import sys
from __init__ import source_folder_path
sys.path.append(source_folder_path)
from _workplace.library.junLib import create_folder, join_folder_path, path_exist, clear
from _workplace.library.junLib_datetime import DateTimer
# from library.junLib import
import imaplib
import email
from email.header import decode_header
from email.parser import Parser
from email.utils import parsedate_tz, mktime_tz, formatdate
from imapclient.imap_utf7 import decode as decode_utf7
import time
# from email.header import decode_header

# 네이버 이메일 계정 설정
USERNAME = 'damt0321'
PASSWORD = 'dm.9500266'
imap_url = 'imap.naver.com'

# IMAP 서버에 연결
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(USERNAME, PASSWORD)

mail_folder_path = join_folder_path(source_folder_path, 'mailing')
if not path_exist(mail_folder_path): create_folder(mail_folder_path)
# "&rBW80cax-T","&rBXWTa1s-T","&waGuMMK5-T","&wuDCudYE-B","&x3S80cIY-E","&yBWz2dY4-B","&1mmzxMd1-D","&1mnBHNds-B","&wuCy5MgV-S"
"""
"&rBW80cax-T", # 강병욱-T
"&rBXWTa1s-T", # 강홍구-T
"&waGuMMK5-T", # 송기승-T
"&wuDCudYE-B", # 신승현-B
"&x3S80cIY-E", # 이병수-E
"&yBWz2dY4-B", # 정동호-B
"&1mmzxMd1-D", # 
"&1mnBHNds-B", # 
"&wuCy5MgV-S", # 신다정-S

"""
vip_list = [
    b"&rBW80cax-T", # 강병욱T
    b"&rBXWTa1s-T",
    b"&waGuMMK5-T",
    b"&wuDCudYE-B",
    b"&x3S80cIY-E",
    b"&yBWz2dY4-B",
    b"&1mmzxMd1-D",
    b"&1mnBHNds-B",
    b"&wuCy5MgV-S",
    ]

# IMAPClient로 연결
# server = IMAPClient(imap_url, use_uid=True, ssl=True)
# server.login(USERNAME, PASSWORD)

# 인코딩된 메일함 이름 예시
# encoded_name = "&rBW80cax-T"

# 디코딩된 메일함 이름 얻기
# decoded_name = server.decode_folder_name(encoded_name)

# 제목을 디코딩하는 함수
def decode_subject(subject):
    decoded_header = decode_header(subject)
    # 디코딩된 헤더의 각 부분을 처리
    subject_parts = []
    for part, encoding in decoded_header:
        if encoding:
            part = part.decode(encoding)
        elif isinstance(part, bytes):
            # 인코딩 정보가 없지만 바이트 타입인 경우 utf-8로 가정
            part = part.decode('utf-8')
        subject_parts.append(part)
    return ''.join(subject_parts)

def parse_date(raw_email:bytes, time_format:str="%Y-%m-%d %H:%M:%S"):
    # raw_email = """From: sender@example.com
    # To: recipient@example.com
    # Subject: Test Email
    # Date: Fri, 12 Jun 2020 14:31:05 -0700

    # This is a test email message."""

    # 이메일 파싱
    # parser = Parser()
    email_message = email.message_from_bytes(raw_email)


    # 'Date' 헤더에서 날짜와 시간대 추출
    date_header = email_message['Date']
    # print("Original Date Header:", date_header)

    # parsedate_tz를 사용하여 파싱
    parsed_date = parsedate_tz(date_header)
    # print("Parsed Date:", parsed_date)

    # mktime_tz를 사용하여 로컬 타임스탬프로 변환
    timestamp = mktime_tz(parsed_date)
    print("Timestamp:", timestamp)

    # localtime을 사용하여 struct_time 객체로 변환
    local_time = time.localtime(timestamp)
    result = time.strftime(time_format, local_time)
    print("Local Time:", result)

    # formatdate를 사용하여 사람이 읽을 수 있는 형태로 변환 (옵션: localtime=True 사용)
    # readable_date = formatdate(timestamp, localtime=True)
    # print("Readable Date:", readable_date)
    
    """ 
    # 시간대 정보 추출
    timezone_offset = parsed_date[-1]
    # 시간대 오프셋을 시간 단위로 변환
    offset_hour = timezone_offset // 3600
    offset_min = (timezone_offset % 3600) // 60
    print(f"Timezone Offset: {offset_hour:+03d}:{offset_min:02d}") 
    """
    return result

# 파일 이름 디코딩
def decode_filename(encoded_filename):
    decoded_parts = decode_header(encoded_filename)
    filename = ''.join(
        str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else part[0]
        for part in decoded_parts
    )
    return filename

# 파일 이름에서 유효하지 않은 문자 대체
def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def check_mailbox():
    result, mailboxes = mail.list()
    if result == 'OK':
        print("메일함 목록:")
        for mailbox in mailboxes:
            print(mailbox.decode())

def download_content():
    timer = DateTimer()
    downloaded_files = []
    for index, vip in enumerate(vip_list, 1):
        clear()
        mail.select(vip) # 받은편지함 선택

        email_box_name = decode_utf7(vip)
        # input(f"{type(vip)}\t{(email_box_name)}")
        print(f"{type(vip)}\t{(email_box_name)}")

        # 모든 이메일 검색
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()

        # # 가장 최근 이메일 선택
        # latest_email_id = email_ids[-1]
        count = 0
        for i, email_id in enumerate(email_ids):
            
            print(f"{index}/{len(vip_list)}\n\t{email_box_name}")
            print(count)
            # 해당 이메일에서 데이터 가져오기
            result, data = mail.fetch(email_id, '(RFC822)')
            # clear()
            # time.sleep(1)
            # input(data)
            raw_email = data[0][1]
            
            # 이메일 메시지 파싱
            email_message = email.message_from_bytes(raw_email)
            title = decode_subject(email_message.get("Subject")).replace('FW: ', '').replace(':', '')
            # send_time = parse_date(raw_email, "%Y%m%d_%H%M")
            send_time = parse_date(raw_email, "%Y%m%d")
            if int(send_time) < int(timer.get_current_datetime("yyyyMMdd")) - 2: 
                continue
            print(f"title\t{title}")

            # input("Enter to continue.")

            # 첨부 파일 다운로드
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                
                filename = part.get_filename()
                if bool(filename):
                    mail_title_folder_path = join_folder_path(mail_folder_path, f"{send_time}", f'{email_box_name}', f"{title}")
                    if not path_exist(mail_title_folder_path): create_folder(mail_title_folder_path)
                    decoded_filename = decode_filename(filename)
                    safe_filename = sanitize_filename(decoded_filename)
                    print("found file")
                    count += 1
                    filepath = join_folder_path(mail_title_folder_path, f'{safe_filename}')
                    if path_exist(filepath): continue
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                        # f.write(part.get_payload())
                    print(f'Downloaded {count}: {safe_filename}')
                    downloaded_files.append(filepath)
    return downloaded_files

if __name__ == "__main__":
    # check_mailbox()
    downloaded_files = download_content()
    clear()
    print('\n'.join(downloaded_files))