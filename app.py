from utils import batch_upload_to_wordpress, search_all_file

## 文件夹路径,b开头的字符串是转义字符,记得在前面加\转义,例如\\blog
folder_path = "G:\code\\blog\\note-book\个人理解"
## 无用的文件夹前缀
useless_folder_prefix = "G:\code\\blog\\note-book\个人理解\\"
## 文件夹分隔符
split_symbol = "\\"
## 需要获取的文件后缀
suffix_tuple = ".md"


if __name__ == "__main__":
    ## 填写你的wordpress站点信息
    site_url = "https://yourwordpresssite.com/xmlrpc.php"
    username = "your_username"
    password = "your_password"
    fileList = search_all_file(folder_path, suffix_tuple)
    print("共扫描到{}个文件".format(len(fileList)))
    isUpload = input("请输入是否上传所有文件(y or n)：")
    if isUpload == "y":
        batch_upload_to_wordpress(
            folder_path,
            useless_folder_prefix,
            split_symbol,
            suffix_tuple,
            site_url,
            username,
            password,
        )
    else:
        print("取消上传")
