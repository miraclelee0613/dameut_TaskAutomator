from email.header import decode_header
import email.utils

# 인코딩된 헤더 값 예시
encoded_header = '&rBW80cax-T'

# 디코딩
decoded_header_parts = decode_header(encoded_header)

# 디코딩된 헤더를 하나의 문자열로 조합
decoded_string = ''.join(
    str(part[0], part[1] or 'utf-8') if isinstance(part[0], bytes) else part[0]
    for part in decoded_header_parts
)

print(decoded_string)