import re
import sys
import os
import configparser
import shutil
import logging
import codecs

# 项目基础路径
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

logfile = codecs.open(os.path.join(BASE_DIR, 'error_log.txt'), mode='a', encoding='utf-8')
# 配置日志输出的格式和级别
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    stream=logfile)


def classification_file(files_list, output, keyword_path):
    if os.path.exists(keyword_path) is False:
        logging.info(f"屏蔽关键字文件{keyword_path}不存在")
        print(f"屏蔽关键字文件{keyword_path}不存在")
        input("Press any key to exit...")
        exit(0)
    with open(keyword_path, "r", encoding="utf-8") as f:
        keyword = f.read().split("\n")
        print(f"屏蔽关键词个数:{len(keyword)}")
        print(f"屏蔽关键词：{keyword}")

    for file in files_list:
        file_name = file.split("\\")[-1]
        print(f"当前文件为：{file_name}")
        # 正则表达式模式，匹配[]中的内容
        pattern = r"\[(.*?)\]"

        # 使用re.findall方法进行匹配
        matches = re.findall(pattern, file)
        print(f"找到所有的[]:{matches}")
        remove_list = []
        if len(matches) == 0:
            folder_isexit(os.path.join(output, "其他"))
            # 将文件移动到其他文件夹中
            # os.rename(file, os.path.join(output, "其他", file_name))
            shutil.move(file, os.path.join(output, "其他", file_name))

        elif len(matches) > 1:
            for match in matches:
                for i in keyword:
                    if re.search(i, match):
                        print(f"发现字符'{i}'：{match}")
                        remove_list.append(match)

            matches = remove_keyword(remove_list, matches)
            print(f"去除关键字后的matches：{matches}")
            re_folder_name = matches[0]
            for i in matches:
                if judge_riwen(i):
                    re_folder_name = i
            re_folder_name = change_to_English_symbols(re_folder_name)
            print(f"最终的文件夹名字：{re_folder_name}")

            if search_keyword(re_folder_name, keyword):
                folder_isexit(os.path.join(output, "其他"))
                shutil.move(file, os.path.join(output, "其他", file_name))
            else:
                folder_isexit(os.path.join(output, re_folder_name))
            try:
                shutil.move(file, os.path.join(output, re_folder_name, file_name))
            except:
                logging.info("文件夹名不符合规范")
        else:
            re_folder_name = matches[0]
            if search_keyword(re_folder_name, keyword):
                folder_isexit(os.path.join(output, "其他"))
                shutil.move(file, os.path.join(output, "其他", file_name))
            else:
                re_folder_name = change_to_English_symbols(re_folder_name)
                try:
                    folder_isexit(os.path.join(output, re_folder_name))
                    # os.rename(file, os.path.join(output, re_folder_name, file_name))
                    shutil.move(file, os.path.join(output, re_folder_name, file_name))
                except:
                    logging.info("文件夹名不符合规范")


def search_keyword(name, keyword_list):
    for i in keyword_list:
        if re.search(i, name):
            return True
    return False


def folder_isexit(path):
    if os.path.exists(path) is False:
        os.makedirs(path)


def remove_keyword(remove_list, input_list):
    result_list = []
    for i in input_list:
        if i not in remove_list:
            result_list.append(i)
    return result_list


def get_all_files(path, files_list):
    # 如果该路径存在
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            # 如果该路径是文件夹
            if os.path.isdir(os.path.join(path, file)):
                get_all_files(os.path.join(path, file), files_list)
            # 如果该路径是文件
            else:
                # 文件是压缩包
                if file.endswith(".zip") or file.endswith(".rar") or file.endswith(".7z"):
                    files_list.append(os.path.join(path, file))
    else:
        print("输入文件夹不存在")
        input("Press any key to exit...")
        exit(0)

    return files_list


def delete_all_foldler(input_path):
    folers = os.listdir(input_path)
    for foler in folers:
        if os.path.isdir(os.path.join(input_path, foler)):
            if len(os.listdir(os.path.join(input_path, foler))) == 0:
                os.rmdir(os.path.join(input_path, foler))
            else:
                pass


def change_to_English_symbols(file_name):
    result = file_name.replace("（", "(").replace("）", ")").replace(" ", "").replace("。", "")
    return result


def judge_riwen(input_str):
    pattern = r'[\u3040-\u309F\u30A0-\u30FF]+'  # 平假名和片假名的Unicode范围
    matches = re.search(pattern, input_str)
    if matches:
        return True
    else:
        return False


def read_putpath(ini_path):
    # 读取INI文件
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='utf-8')

    # 获取配置项的值
    input_path = config.get('input_path', 'path')
    output_path = config.get('output_path', 'path')
    if input_path == "" or output_path == "" or \
            os.path.exists(input_path) is False or os.path.exists(output_path) is False:
        if input_path == "" or os.path.exists(input_path) is False:
            print("输入文件夹为空或不存在")
            input_path = input("请输入待处理的文件夹路径：")
        if output_path == "":
            print("输出文件夹为空")
            output_path = input("请输入输出文件夹路径：")

        # 修改配置项的值
        config.set('input_path', 'path', input_path)
        config.set('output_path', 'path', output_path)
        with open(ini_path, 'w', encoding="utf-8") as configfile:
            config.write(configfile)
        return input_path, output_path
    else:
        return input_path, output_path


if __name__ == '__main__':
    # input_path = r"F:\分类结果1"
    # input_path = r"F:\分类结果"
    # output_path = r"F:\分类结果2"
    # 三个路径
    ini_path = os.path.join(BASE_DIR, "putpath.ini")
    keyword_path = os.path.join(BASE_DIR, "keywords.txt")
    input_path, output_path = read_putpath(ini_path)

    # 显示输入文件夹和输出文件夹
    print(f"输入文件夹：{input_path}")
    print(f"输出文件夹：{output_path}")
    print("----- 文件夹路径可以在 \"putpath.ini\" 中修改 ------")
    # 获得所有压缩包路径
    all_files = get_all_files(input_path, [])
    print(f"所有文件：{all_files}")

    # 分类
    classification_file(all_files, output_path, keyword_path)
    # 删除空文件夹
    delete_all_foldler(input_path)

    # 显示分类完成
    print(f"{len(all_files)}个文件分类完成，输出文件夹为：", output_path)
    input("Press any key to exit...")
