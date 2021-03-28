# Table of Contents

- [Description](#description)
- [Setup instructions](#setup)
- [More Samples](#more-samples)

## Description

Tool to assist with comic translation. 

Features include:
- Text extraction from source image and segmented by panel / speech bubble.
  - OCR performed by Google's Cloud Vision API and Microsoft's Azure API.
- Automatic dictionary suggestions and machine translations.
  - (wip) Dictionary lookup powered by the [National Institute of Korean Language's API](https://krdict.korean.go.kr/openApi/openApiInfo) (한국어기초사전 오픈 API).
  - Translation performed by Papago.
- (todo) Exporting to text doc / spreadsheet.

## Setup

1. Clone this repo `git clone https://github.com/LiteralGenie/TranslationThingy`

1. Install requirements `python3 -m pip install -r requirements.txt`

1. Replace `data/chromedriver.exe` with a version matching your Chrome installation.

1. Run `main.py`

## Samples

demo video: https://www.youtube.com/watch?v=6YsrUMtCD4A

![](https://files.catbox.moe/w51sa7.png)