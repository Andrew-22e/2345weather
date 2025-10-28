import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
import time
from concurrent.futures import as_completed


def GetWeather_sync(year, month):
    """
    获取指定年月的天气数据
    
    Args:
        year (str): 年份
        month (str): 月份
        
    Returns:
        list: 包含每日天气信息的字典列表
    """
    # 存储天气信息的列表
    weather_info = []
    # 请求头信息，模拟浏览器访问
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            "referer": "https://tianqi.2345.com/wea_history/57993.htm",
        }
    # 目标URL
    url = "https://tianqi.2345.com/Pc/GetHistory"
    # 请求参数
    params = {
    "areaInfo[areaId]": "57993",
    "areaInfo[areaType]": "2",
    "date[year]": year,
    "date[month]": month,
    }
    # 发送GET请求获取数据
    response = requests.get(url, headers=headers, params=params)
    # 解析JSON响应
    json_data = response.json()
    # 提取HTML数据部分
    html_data = json_data['data']
    # 解析HTML
    tree = etree.HTML(html_data)
    # 使用XPath定位天气表格中的数据行（排除表头）
    weather_list = tree.xpath('//table[@class="history-table"]//tr[position()>1]')
    # 提取需要元素
    for weather in weather_list:
        # 存储单日天气信息的字典
        day_weather_info = {}
        # 提取日期
        date_text = weather.xpath('./td[1]/text()')
        # 提取最高温度
        high_text = weather.xpath('./td[2]//text()')
        # 提取最低温度
        low_text = weather.xpath('./td[3]//text()')
        # 提取天气状况
        weather_text = weather.xpath('./td[4]/text()')
        
        # 处理日期数据
        if date_text:
            day_weather_info['date'] = date_text[0].strip()
        # 处理最高温度数据
        if high_text:
            # 合并文本节点并提取温度数值
            high_temp = ''.join(high_text).strip()
            day_weather_info['high_temp'] = high_temp.replace('°', '℃')
        # 处理最低温度数据
        if low_text:
            # 合并文本节点并提取温度数值
            low_temp = ''.join(low_text).strip()
            day_weather_info['low_temp'] = low_temp.replace('°', '℃')
        # 处理天气状况数据
        if weather_text:
            day_weather_info['weather'] = weather_text[0].strip()
        
        # 只有当有数据时才添加到列表中
        if day_weather_info:
            weather_info.append(day_weather_info)
    return weather_info

def save_to_csv(weather_data, filename):
    """
    将天气数据保存到CSV文件
    
    Args:
        weather_data (list): 天气数据列表
        filename (str): 保存的文件名
    """
    """将天气数据保存到CSV文件"""
    # 检查是否有数据可保存
    if not weather_data:
        print("没有数据可保存")
        return
    
    # 定义CSV文件的列名
    fieldnames = ['日期', '最高气温', '最低气温', '天气']
    
    # 写入CSV文件
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 写入表头
        writer.writeheader()
        
        # 写入数据
        for data in weather_data:
            # 处理日期，去除星期几信息
            date_str = data.get('date', '')
            # 如果日期中包含星期信息，则只保留日期部分
            if '周' in date_str:
                date_str = date_str.split('周')[0]
            
            writer.writerow({
                '日期': date_str,
                '最高气温': data.get('high_temp', ''),
                '最低气温': data.get('low_temp', ''),
                '天气': data.get('weather', '')
            })
    
    print(f"数据已保存到 {filename} 文件中")

# 使用ThreadPoolExecutor实现GetWeather_sync方法的并发调用
def fetch_year_weather_data(year):
    """
    使用线程池并发获取一年12个月的天气数据
    
    Args:
        year (str): 年份
        
    Returns:
        list: 全年天气数据列表
    """
    # 创建包含12个月份的参数列表
    months = [str(i).zfill(2) for i in range(1, 13)]  # 生成01-12的月份
    
    # 存储所有天气数据的列表
    all_weather_data = []
    
    # 使用ThreadPoolExecutor进行并发处理
    with ThreadPoolExecutor(max_workers=5) as executor:  # 设置最大并发线程数为5
        # 提交任务到线程池，创建future到月份的映射
        future_to_month = {
            executor.submit(GetWeather_sync, year, month): month 
            for month in months
        }
        
        # 获取任务结果
        for future in as_completed(future_to_month):
            # 获取当前完成的任务对应的月份
            month = future_to_month[future]
            try:
                # 获取执行结果
                weather_data = future.result()
                # 将数据添加到总列表中
                all_weather_data.extend(weather_data)
                print(f"{year}年{month}月数据获取完成，共{len(weather_data)}条记录")
            except Exception as e:
                # 处理异常情况
                print(f"{year}年{month}月数据获取失败: {e}")
    
    return all_weather_data


# 程序入口点
if __name__ == "__main__":
    # 获取2024年全年的天气数据
    year = "2024"
    print(f"开始获取{year}年全年天气数据...")
    
    # 记录开始时间
    start_time = time.time()
    # 获取全年天气数据
    weather_data = fetch_year_weather_data(year)
    
    # 对获取的数据按日期排序
    weather_data.sort(key=lambda x: x['date'])
    
    # 记录结束时间
    end_time = time.time()
    
    print(f"\n{year}年全年天气数据获取完成！")
    print(f"总共获取到{len(weather_data)}条数据")
    print(f"耗时: {end_time - start_time:.2f}秒")
    
    # 保存数据到CSV文件
    csv_filename = f"爬虫/2345weather/{year}年赣州历史weather.csv"
    save_to_csv(weather_data, csv_filename)