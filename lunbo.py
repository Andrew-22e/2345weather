import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Timeline , Bar

# 读取天气数据CSV文件
df = pd.read_csv('爬虫/2345weather/2024年赣州历史weather.csv',encoding='utf-8')
# 将日期列转换为datetime类型以便处理
df['日期'] = df['日期'].apply(lambda x:pd.to_datetime(x))
# 提取月份信息作为新的列
df['month'] = df['日期'].dt.month
# 按月份和天气状况分组统计频次，并重置索引
df_agg = df.groupby(['month','天气']).size().reset_index()
# 重命名列名
df_agg.columns = ['month','tianqi','count']


# 创建时间轴对象用于制作动态图表
timeline = Timeline()
# 设置时间轴播放间隔为1000毫秒
timeline.add_schema(play_interval=1000)
# 遍历每个月份，生成对应的柱状图
for month in df_agg['month'].unique():
    # 筛选当前月份的数据并按计数升序排列
    data = (
        df_agg[df_agg['month'] == month] [['tianqi','count']]
        .sort_values(by = 'count',ascending = True)
        .values.tolist()
    )
    print(data)
    # 创建柱状图对象
    bar = Bar()
    # 添加X轴数据（天气状况）
    bar.add_xaxis([x[0] for x in data])
    # 添加Y轴数据（出现次数）
    bar.add_yaxis('',[x[1] for x in data])
    # 翻转坐标轴，使天气状况在Y轴上显示
    bar.reversal_axis()
    # 设置标签显示位置在右侧
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))
    # 设置图表标题
    bar.set_global_opts(title_opts=opts.TitleOpts(title='赣州2024年每月天气变化'))
    # 将当前月份的图表添加到时间轴中
    timeline.add(bar,f'{month}月')
# 渲染生成HTML文件
timeline.render(f'爬虫/2345weather/赣州weather.html')
print("Finish!")