# 📊 2345weather：赣州2024年天气数据采集与可视化

一个基于 Python 的数据爬取 + 分析 + Echarts 可视化项目，用于展示 **2024 年赣州历史天气变化**，支持并发爬虫、动态图表时间轴、多维度天气状况分类等功能。


---

## 🚀 项目亮点

- 🌐 **爬虫模块（`spider.py`）**
  - 来源网站：[2345天气网历史数据](https://tianqi.2345.com/wea_history/)
  - 使用 `requests + lxml` 发起请求与解析
  - 支持通过多线程并发爬取全年 12 个月的数据
  - 数据字段包括：日期、最高气温、最低气温、天气状况
  - 自动写入为 UTF-8 编码的 CSV 文件（保留中文）

- 📈 **数据可视化模块（`lunbo.py`）**
  - 使用 `pyecharts` 动态构建时间轴柱状图（Timeline + Bar）
  - 显示每月不同天气状况的出现频率分布
  - 自动生成可交互 HTML 页面（含播放功能）
  - 支持 `reversal_axis()` 横向图展示，更清晰直观

- 🧾 **数据源示例**
  - 文件：`2024年赣州历史weather.csv`
  - 结构：
    | 日期 | 最高气温 | 最低气温 | 天气 |
    |------|----------|----------|------|
    | 2024-01-01 | 12℃ | 6℃ | 阴转多云 |
    | ...  | ...      | ...      | ...  |

- 📊 **输出图表**
  - 文件：`赣州weather.html`
  - 图例：每个月份的天气类型（如“阴~晴”、“多云~小雨”）与出现次数
  - 演示：
    - ![静态图示意图]<img width="1251" height="746" alt="image" src="https://github.com/user-attachments/assets/7f43ee03-9b38-4e2a-a54c-85125947eae5" />


    _注：实际图表请打开本地 HTML 文件查看交互效果_

---

## 🗂️ 项目结构

```
2345weather/
├── spider.py               # 天气爬虫主程序
├── lunbo.py                # 数据可视化模块
├── 2024年赣州历史weather.csv   # 原始爬取数据
└── 赣州weather.html         # 输出动态图表页面
```

---

## 🔧 使用方法

1. 安装依赖项（建议使用虚拟环境）：
```bash
pip install requests lxml pyecharts pandas
```

2. 运行爬虫（爬取并保存全年数据）：
```bash
python spider.py
```

3. 运行可视化脚本（读取 CSV 并生成图表）：
```bash
python lunbo.py
```

4. 查看结果：
   - 打开 `赣州weather.html`，查看动态图表
   - 查看 `2024年赣州历史weather.csv` 数据内容

---

## 📌 技术栈

- 数据获取：`requests`, `lxml`, `concurrent.futures`
- 数据处理：`pandas`
- 图表构建：`pyecharts`
- 可视化输出：`HTML5 + ECharts Timeline`

---

## 📅 未来计划

- [ ] 增加湿度/风速等维度采集  
- [ ] 添加城市选择参数  
- [ ] 导出为静态图片或PDF报告  
- [ ] 整合 Flask/Django 构建 Web 服务版本  

---

## 📄 License

本项目遵循 [MIT License](https://opensource.org/licenses/MIT)。
