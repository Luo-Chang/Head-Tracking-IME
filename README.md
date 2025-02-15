## ![screen](./misc/icon_small.png) Head Tracking IME

一款基于头部跟踪的为重度残障人士提供语言能力支持的中文输入、交流工具。

Chinese IME based on Head Tracking for Disabilities

![screen](./misc/image.png)


## 概览 Overview

该项目适用于重度脑梗致瘫病人无法活动、丧失语言能力，但是能听、能理解文字，头部能够运动的情况。通过**头部跟踪**使病人能够自主选择并输出文字从而恢复与家属的沟通和交流。

*下述`用户`指的是帮助`病人`启动并配置本程序的人员（如家属）

This project provides a Chinese Input Method Editor (IME) for individuals with disabilities, specifically those with severe conditions like brain strokes that have left them unable to move or speak but still capable of hearing and understanding text. The system leverages **head tracking** to enable text input.

**功能**:
1. 病人通过头部运动控制并选择文字输入，用户可自定义病人常用词典(位于`vocab/vocab.txt`，以英语`,`分割)
1. 通过`TTS`朗读输出的文字，病人可以获得类似霍金的对话能力

**原理**:
1. `opentrack` 头部跟踪输出 `X` 轴坐标并经过 UDP 发送到本程序
1. 根据头部 `X` 轴的移动控制并点选汉字组成句子，经由 `TTS` 朗读从而实现病人与家属的沟通



## 依赖 Dependencies

本项目依赖于 [opentrack](https://github.com/opentrack/opentrack/commit/c762f7128daf5691d4ce60b51ebfd6626bb0006f) 的 commit `c762f7128daf5691d4ce60b51ebfd6626bb0006f`。

This project depends on [opentrack](https://github.com/opentrack/opentrack/commit/c762f7128daf5691d4ce60b51ebfd6626bb0006f) at commit `c762f7128daf5691d4ce60b51ebfd6626bb0006f`.



## 项目平台 Platform

本项目目前仅适用于 **Windows** 平台，因其使用了 **PyWin32** 调用 Windows 的中文 TTS 服务。

Currently, this project is designed to run on **Windows** only, due to its use of **PyWin32** to call the Windows Chinese TTS service.


## 安装方法 Installation

1. 克隆当前项目到本地 Clone the repository:

    ```bash
    git clone https://github.com/Luo-Chang/Head-Tracking-IME.git
    cd Head-Tracking-IME
    ```

1. 安装依赖项 Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

1. 安装 [opentrack 2023.3.0 (commit c762f712)](https://github.com/opentrack/opentrack/commit/c762f7128daf5691d4ce60b51ebfd6626bb0006f) Install `opentrack 2023.3.0` (i.e. commit c762f712)

1. 确保 **Windows** 安装了中文 TTS 音声，比如 Microsoft Kangkang 或者 Microsoft Huihui；如果没有，可以通过**设置** > **时间和语言** > **语音** > **管理语音**来安装。
 Make sure you have **Windows** installed with a suitable Chinese TTS voice. You can install it via **Settings** > **Time & Language** > **Speech** > **Manage voices**.


## 使用方法 Usage

1. 启动 `opentrack`，设置`input`为`neuralnet tracker`，设置`output`为`UDP over network`，最后点击`Start`开始头部跟踪
1. 使用 `python main.py` 启动本程序，点击`开始输入`
1. 病人通过头部左右转动来选择汉字，并在准备输入的汉字处停留；在所预选的汉字处停留`2s`(可调整)后，汉字即选中并显示在输出区域
1. 病人可以通过右侧的控制按钮切换上下页汉字以及删除、朗读(TTS)输出内容
1. 用户可以通过`config.toml`更改相关时长、页面布局、头部跟踪灵敏度等设置
1. 用户可以通过修改`vocab/vocab.txt`添加常用字、调整字的顺序，注意字与字之间用英文逗号`,`分隔
1. `ESC`键退出程序

## 许可 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

