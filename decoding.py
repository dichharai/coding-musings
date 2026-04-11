import re

import requests
from requests import Response
from bs4 import BeautifulSoup
from bs4.element import ResultSet



def decode_message(url: str) -> any:
    response: Response = requests.get(url)
    response.encoding = 'utf-8'

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    rows: ResultSet = soup.find_all('tr')
    # print(soup.text[:500])

    # print(f"Found {len(rows)} rows.\n") 
    # print(f"1st row: {rows[0]}")

    clean_lines: list[str] = []
    for _, row in enumerate(rows[1:]):  # skipping header
        text = row.get_text()
        parts = re.split(r'(\D+)', text)
        clean_lines.append(parts)      

    positions: tuple[str, int, int] = []
    i = 0

    while i < len(clean_lines):
        x = int(clean_lines[i][0])
        char = clean_lines[i][1]
        y = int(clean_lines[i][2])
        positions.append((char, x, y))

        i += 1

    if not positions:
        print("No valid data found.")
        return
    
    # print(positions)
    max_x: int = max(p[1] for p in positions)
    max_y: int = max(p[2] for p in positions)
    # print(max_x, max_y)

    # empty string for grid without character
    grid: list[list[str]] = [[' ' for _ in range(max_x+1)] for _ in range(max_y+1)]

    for char, x, y in positions:
        grid[max_y-y][x] = char
    
    for row in grid:
        print(''.join(row))
    

decode_message("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")
# decode_message("https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub")