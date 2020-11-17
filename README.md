# str2emoji

这是一个将文字（汉字）转化为 emoji 的工具。
灵感来源于 [抽象话生成器](https://chouxiang.ml/)。
但这是一个更简单（但覆盖内容更广？）的实现。

## 安装
```shell
git clone git@github.com:catbaron0/str2emoji.git && python setup.py install
```

## 如何使用

```python
from str2emoji import Str2Emoji
str2emoji = Str2Emoji()
text = "苟利国家生死以，岂因祸福避趋之"
print(str2emoji(text))
```
***结果***

`🐶🌰国🏠生💀🐜，7⃣🎵🔥🦇👃趋🈯`


