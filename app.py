from utils import batch_upload_to_wordpress, search_all_file, upload_one_file

## 文件夹路径,b开头的字符串是转义字符,记得在前面加\转义,例如\\blog
folder_path = "G:\code\\blog\YuQueBackups\\backups\origin_md\博客\文章管理\个人博客"
## 无用的文件夹前缀
useless_folder_prefix = "G:\code\\blog\YuQueBackups\\backups\origin_md\博客\文章管理\\"
## 文件夹分隔符
split_symbol = "\\"
## 需要获取的文件后缀
suffix_tuple = ".md"


upload_one_file_path = (
    "G:\code\\blog\YuQueBackups\\backups\origin_md\博客\文章管理\个人博客\博客-hexo.md"
)

if __name__ == "__main__":
    ## 填写你的wordpress站点信息
    site_url = "https://jwblog.xyz/xmlrpc.php"
    username = "username"
    password = "password"
    upload_type = input("请输入：\n " + "1.上传单个文章.\n 2.批量上传.\n")
    if upload_type == "1":
        upload_one_file(
            upload_one_file_path,
            useless_folder_prefix,
            split_symbol,
            site_url,
            username,
            password,
        )
    elif upload_type == "2":
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
