import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from markdown import markdown


default_site_url = "https://yourwordpresssite.com/xmlrpc.php"

default_username = "your_username"

default_password = "your_password"

## 文件夹路径
backups_origin_md_dir = (
    "G:\code\\blog\YuQueBackups\\backups\origin_md\博客\开源经历\hertzbeat"
)
## 无用的文件夹前缀
default_useless_folder_prefix = (
    "G:\\code\\blog\\YuQueBackups\\backups\\origin_md\\博客\\"
)
## 文件夹分隔符
default_split_symbol = "\\"
## 需要获取的文件后缀
default_suffix_tuple = ".md"

post = WordPressPost()  # 初始化post，我们要发表的文章就是post
count = 0


# 递归遍历文夹与子文件夹中的特定后缀文件
def search_all_file(
    file_dir=backups_origin_md_dir,
    target_suffix_tuple=default_suffix_tuple,
):
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
    useless_folder_prefix=default_useless_folder_prefix,
    split_symbol=default_split_symbol,
    suffix_tuple=default_suffix_tuple,
    site_url=default_site_url,
    username=default_username,
    password=default_password,
    count=count,
):
    file_list = search_all_file(file_dir, suffix_tuple)
    ## debug用
    # print(file_list)
    for file_path in file_list:
        upload_one_file(
            file_path, useless_folder_prefix, split_symbol, site_url, username, password
        )
        count += 1
        # print("File Content:", file_content)
        # print("Folders:", folders)
        # print()
    print("共上传了{}篇文章".format(count))


def upload_one_file(
    file_path,
    useless_folder_prefix=default_useless_folder_prefix,
    split_symbol=default_split_symbol,
    site_url=default_site_url,
    username=default_username,
    password=default_password,
):
    ## debug用
    # print(file_list)
    # 将文件路径分割为文件夹和文件名
    folders = file_path.split(
        ## 无用的文件夹前缀
        useless_folder_prefix
    )[1].split(split_symbol)[:-1]
    file_name = file_path.split(split_symbol)[-1]

    # 打开Markdown文件，以二进制模式读取
    with open(file_path, "rb") as f:
        file_content = f.read().decode("utf-8")  # 使用utf-8解码成字符串

    # 上传文件
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


def add_space_around_backticks(code):
    return code.replace("```", "\n ``` ")


def markdown_to_html(md_content):
    md_content = add_space_around_backticks(md_content)
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
