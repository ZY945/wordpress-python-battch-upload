```bash
# 1.创建虚拟环境
python -m venv test-env
# 2.进入虚拟环境
.\test-env\Scripts\activate
# 3.更新pip
python.exe -m pip install --upgrade pip
# 4.下载所需模块
pip install -r requirements.txt
# 5.启动脚本(可以现根据所需进行修改)
py.exe .\app.py
```