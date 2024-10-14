# utils/html_helpers.py

def create_button_html(link: str, text: str, color: str) -> str:
    """HTML 버튼 템플릿을 생성하는 함수
    
    Args:
        link (str): 버튼이 이동할 링크
        text (str): 버튼에 표시될 텍스트
        color (str): 버튼 배경색

    Returns:
        str: HTML 코드로 된 버튼 템플릿
    """
    
    return f'''
    <a href="{url}" target="_blank" style="
        display: inline-block;
        padding: 8px 16px;
        background-color: {color};
        color: white;
        text-align: center;
        text-decoration: none;
        border-radius: 4px;
    ">{text}</a>
    '''
