import requests

def get_user_bands(access_token):
    """사용자가 속한 밴드 목록을 가져오는 함수"""
    url = "https://openapi.band.us/v2.1/bands"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['result_data']['bands']
    else:
        print(f"Error: {response.status_code}")
        return []

def save_posts_to_file(posts, filename):
    """게시글 내용을 파일로 저장하는 함수"""
    with open(filename, 'w', encoding='utf-8') as file:
        for post in posts:
            file.write(post['content'] + '\n\n')

# 사용 예시
access_token = 'ZQAAATYtqgQq21PMSyi-HGjVblzjbkIOSz7zJYwXev_aAyGnusgPAHts0TP8YM84mfjHaNnJRGlEWtWmIYQ_ZgOAag3TSgDkzxHyU91rbnimo15H' # 실제 액세스 토큰 값으로 대체
bands = get_user_bands(access_token)
posts = None

for band in bands:
    # 여기서 각 밴드의 게시글을 조회하고, 읽지 않은 게시글을 필터링하는 로직을 추가
    band['band_key']
    # 예제에서는 해당 부분이 생략되어 있습니다.
    # 조회된 게시글을 파일로 저장
    save_posts_to_file(posts, f"{band['name']}_posts.txt")