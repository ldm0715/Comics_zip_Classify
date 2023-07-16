## 简介
一个漫画压缩包分类程序。

下载的资源必须满足**文件的信息写在文件名的[]中**，比如：
```
[作者][分类][二次创作][其他信息].zip
```
### 效果
默认的使用效果为**按照作者分类**，下面是一个例子：

处理前：

<div align="center">
<img src="https://z4a.net/images/2023/07/16/mess.png
" width="75%" alt="mess">
</div>
处理后：
<div align="center">
<img src="https://z4a.net/images/2023/07/16/classify.png" alt="classify" width="75%">
</div>

## 使用方法
项目结构：
```
Comics_Classify
├─ error_log.txt
├─ keywords.txt
├─ main.exe
└─ putpath.ini
```
* `main.exe`：**主程序，双击即可运行**。
* `error_log.txt`：错误日志，记录程序运行的错误信息。
* `keywords.txt`：屏蔽关键词列表，可以自行添加，确保文件夹名称的准确性。
* `putpath.ini`：配置文件,储存着**待处理路径**与**输出路径**，请自行修改。
  * `input_path`：待处理路径
  * `output_path`：输出路径

## 注意事项
* 由于文件名的命名没有统一规范，所以很可能出现文件夹名称不合法的情况，这时候会结束程序，错误信息会写入`error_log.txt`。
* * 由于[]中的信息是多样的，所以可以根据自己的要求进行修改`keyword.txt`，默认按照作者进行分类。
* 有时候文件名中不包含作品信息，或者被`keyword.txt`过滤后未找到分类的信息，此时会将文件放入`输出文件夹\其他`文件夹中。
* 目前只支持"zip"，"rar"，"7z"的压缩包格式。



