import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from markdown import markdown


site_url = "https://yourwordpresssite.com/xmlrpc.php"

username = "your_username"

password = "your_password"

## 文件夹路径
backups_origin_md_dir = (
    "G:\code\\blog\YuQueBackups\\backups\origin_md\博客\开源经历\hertzbeat"
)
## 无用的文件夹前缀
useless_folder_prefix = "G:\\code\\blog\\YuQueBackups\\backups\\origin_md\\博客\\"
## 文件夹分隔符
split_symbol = "\\"
## 需要获取的文件后缀
suffix_tuple = ".md"

post = WordPressPost()  # 初始化post，我们要发表的文章就是post


# 递归遍历文夹与子文件夹中的特定后缀文件
def search_all_file(file_dir=backups_origin_md_dir, target_suffix_tuple=suffix_tuple):
    file_list = []
    # 切换到目录下
    os.chdir(file_dir)
    file_name_list = os.listdir(os.curdir)
    for file_name in file_name_list:
        # 获取文件绝对路径
        file_path = "{}{}{}".format(os.getcwd(), os.path.sep, file_name)
        # 判断是否为目录，是往下递归
        if os.path.isdir(file_path):
            file_list.extend(search_all_file(file_path, target_suffix_tuple))
            os.chdir(os.pardir)
        elif target_suffix_tuple is not None and file_name.endswith(
            target_suffix_tuple
        ):
            file_list.append(file_path)
        else:
            pass
    return file_list


def batch_upload_to_wordpress(
    file_dir=backups_origin_md_dir,
    site_url=site_url,
    username=username,
    password=password,
):
    file_list = search_all_file(file_dir)
    # print(file_list)
    for file_path in file_list:
        # 将文件路径分割为文件夹和文件名
        folders = file_path.split(
            ## 无用的文件夹前缀
            useless_folder_prefix
        )[1].split(split_symbol)[:-1]
        file_name = file_path.split(split_symbol)[-1]

        # Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        # 获取文章标题,内容,标签
        upload_to_wordpress(
            file_name,
            markdown_to_html(file_content),
            folders,
            folders,
            site_url,
            username,
            password,
        )
        print(file_path, "上传成功")
        # print("File Content:", file_content)
        # print("Folders:", folders)
        # print()


def markdown_to_html(md_content):
    html = markdown(md_content)
    return html


def upload_to_wordpress(
    title,
    content,
    tags,
    category,
    site_url,
    username,
    password,
):
    # post的一些属性
    post.title = title[:-3]  # 标题 [:-3]是为了去掉.md后缀
    post.content = content  # 内容
    post.post_status = "publish"  # 类型（publish发布、draft草稿、private隐私）
    post.terms_names = {
        "post_tag": tags,  # 标签(可以写多个)
        "category": category,  # 分类(可以写多个)
    }  # 如果标签、分类没有的话会自动创建，有的话也不影响
    post.comment_status = "open"  # 开启评论

    # 客户端
    client = Client(
        # "https://jwblog.xyz/xmlrpc.php", "账号", "密码"
        site_url,
        username,
        password,
    )  # 改成自己的账号密码，jwblog.xyz改成你自己的域名
    client.call(NewPost(post))
