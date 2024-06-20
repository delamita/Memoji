import os
import shutil
import re

def filter_and_rename_svg_files(base_dir):
    source_dir = os.path.join(base_dir, 'origin')
    release_dir = os.path.join(base_dir, 'release')
    example_dir = os.path.join(base_dir, 'example')
    
    # 创建目标目录，如果不存在则创建
    for directory in [release_dir, example_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # 正则表达式用于匹配文件名中的信息
    pattern = re.compile(r'(Character|Person)=(.*?), Skin Tone=(.*?), Posture=\d+ (.*)\.svg', re.IGNORECASE)
    
    # 用于记录每个character已复制到example文件夹的文件数量
    example_count = {}

    for root, dirs, files in os.walk(source_dir):
        # 获取相对于source_dir的相对路径，并创建对应的release目录结构
        relative_path = os.path.relpath(root, source_dir)
        release_subdir = os.path.join(release_dir, relative_path)
        if not os.path.exists(release_subdir):
            os.makedirs(release_subdir)
        
        for filename in files:
            # 只处理SVG文件
            if filename.endswith('.svg'):
                # 构建源文件路径
                source_file_path = os.path.join(root, filename)
                
                # 使用正则表达式提取信息并重命名
                match = pattern.match(filename)
                if match:
                    character = match.group(2).strip()
                    skin_tone = match.group(3).strip()
                    others = match.group(4).strip().replace(' ', '_')  # 替换空格为下划线

                    new_filename = f"{character}.{skin_tone}.{others}.svg"
                    
                    # 在release目录的相应子目录下按character创建子文件夹
                    character_dir = os.path.join(release_subdir, character)
                    if not os.path.exists(character_dir):
                        os.makedirs(character_dir)

                    destination_file_path = os.path.join(character_dir, new_filename)
                    
                    # 复制文件到release目录
                    shutil.copy(source_file_path, destination_file_path)
                    print(f"Copied: {source_file_path} -> {destination_file_path}")
                    
                    # 如果 skin tone 不是 black，且 example 文件夹中的数量不足 2，则复制到 example 文件夹
                    if skin_tone.lower() != 'black':
                        if character not in example_count:
                            example_count[character] = 0
                        
                        if example_count[character] < 2:
                            example_file_path = os.path.join(example_dir, new_filename)
                            shutil.copy(source_file_path, example_file_path)
                            example_count[character] += 1
                            print(f"Copied to example: {source_file_path} -> {example_file_path}")

if __name__ == "__main__":
    # 获取脚本所在目录
    base_directory = os.path.dirname(os.path.abspath(__file__))
    filter_and_rename_svg_files(base_directory)
