import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin  # 导入 urljoin 用于处理相对链接



def scrap_a():
    # 目标网址
    url1 = 'https://www.bkjx.sdu.edu.cn/sanji_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1010'

    # 发送请求获取网页内容
    response = requests.get(url1)
    response.encoding = response.apparent_encoding  # 设置编码
    html = response.text

    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')

    # 找到通知的列表
    notices = soup.find_all('div', class_='leftNews3')  # 根据网页结构找到通知条目

    # 存储结果的列表
    data_a= []

    # 提取通知信息
    for notice in notices:
        title_tag = notice.find('a')  # 通知标题在<a>标签中
        if title_tag:
            title = title_tag.get_text()
            link = urljoin(url1, title_tag['href'])  # 转换为绝对链接
            date = notice.find(style='float:right;').text.strip('[]')
            
            # 发送请求获取通知具体内容
            response = requests.get(link)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析页面内容
                soup = BeautifulSoup(response.text, 'html.parser')

                # 根据网页结构提取具体内容
                description = soup.find('meta', attrs={'name': 'description'})
                content = description['content'] if description and 'content' in description.attrs else "未找到 description 的内容"
            else:
                content = "请求失败"

            # 记录数据
            data_a.append({
                '标题': title,
                '链接': link,
                '发布时间': date,
                '通知具体内容': content
            })
    return data_a
def scrap_b():
    # 目标网址
    url2 = 'https://online.sdu.edu.cn/txtlist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'

    # 发送请求获取网页内容
    response = requests.get(url2)
    response.encoding = response.apparent_encoding  # 设置编码
    html = response.text

    # 解析网页内容
    soup = BeautifulSoup(html, 'html.parser')

    # 找到通知的列表
    items = soup.find_all('a', class_='item')  # 根据网页结构找到通知条目

    # 存储结果的列表
    data_b= []

    # 提取通知信息
    for item in items:
        title_tag = item.find('div',class_='title')  # 通知标题在<div>标签中
        if title_tag:
            title=title_tag.get_text()
            link = urljoin(url2, item['href'])  # 转换为绝对链接
            date = item.find('div',class_='date').text.strip('[]')
            
            # 发送请求获取通知具体内容
            response = requests.get(link)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析页面内容
                soup = BeautifulSoup(response.text, 'html.parser')

                # 根据网页结构提取具体内容
                description = soup.find('meta', attrs={'name': 'description'})
                content = description['content'] if description and 'content' in description.attrs else "未找到 description 的内容"
            else:
                content = "请求失败"

            # 记录数据
            data_b.append({
                '标题': title,
                '链接': link,
                '发布时间': date,
                '通知具体内容': content
            })
    return data_b


data_a = scrap_a()
data_b = scrap_b()
combined_data = data_a+data_b

# 创建 DataFrame 并保存到 Excel
df = pd.DataFrame(combined_data)
df.to_excel('通知.xlsx', index=False)

print("数据已成功保存到通知.xlsx")
