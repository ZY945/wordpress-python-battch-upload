from utils import batch_upload_to_wordpress

## 文件夹路径,b开头的字符串是转义字符,记得在前面加\转义,例如\\blog
folder_path = "G:\code\\blog\YuQueBackups\\backups\origin_md\博客"
## 无用的文件夹前缀
useless_folder_prefix = "G:\\code\\blog\\YuQueBackups\\backups\\origin_md\\博客\\"
## 文件夹分隔符
split_symbol = "\\"
## 需要获取的文件后缀
suffix_tuple = ".md"


if __name__ == "__main__":
    ## 填写你的wordpress站点信息
    site_url = "https://yourwordpresssite.com/xmlrpc.php"
    username = "your_username"
    password = "your_password"
    batch_upload_to_wordpress(folder_path, site_url, username, password)
