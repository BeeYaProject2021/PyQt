# 引入 requests 模組
import requests

# # 要上傳的檔案
my_files = {'file': open('my_file.txt', 'rb')}
params = ( ( 'model',1 ),( 'model',2 ),( 'model',3 ) )

# 將檔案加入 POST 請求中
r = requests.post('http://140.136.151.88:8000/upload/', files = my_files, data=params)