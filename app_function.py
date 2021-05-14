import requests
import win32api
import sys
import os
import random
import re
import json
import difflib
import time
from datetime import datetime
import locale
locale.setlocale(locale.LC_CTYPE, 'chinese')

table = [
    ('AED', '阿联酋迪拉姆'),
    ('AFN', '阿富汗尼'),
    ('ALL', '阿尔巴尼亚列克'),
    ('AMD', '亚美尼亚德拉姆'),
    ('ANG', '荷属安的列斯盾'),
    ('AOA', '安哥拉宽扎'),
    ('ARS', '阿根廷比索'),
    ('AUD', '澳大利亚元'),
    ('AWG', '阿鲁巴弗罗林'),
    ('AZN', '阿塞拜疆马纳特'),
    ('BAM', '波斯尼亚和黑塞哥维那可兑换马克'),
    ('BBD', '巴巴多斯元'),
    ('BDT', '孟加拉塔卡'),
    ('BGN', '保加利亚列弗'),
    ('BHD', '巴林第纳尔'),
    ('BIF', '布隆迪法郎'),
    ('BMD', '百慕大元'),
    ('BND', '文莱元'),
    ('BOB', '玻利维亚诺'),
    ('BRL', '巴西雷亚尔'),
    ('BSD', '巴哈马元'),
    ('BTN', '不丹努尔特鲁姆'),
    ('BWP', '博茨瓦纳普拉'),
    ('BYN', '白俄罗斯卢布'),
    ('BZD', '伯利兹元'),
    ('CAD', '加拿大元'),
    ('CDF', '刚果法郎'),
    ('CHF', '瑞士法郎'),
    ('CLP', '智利比索'),
    ('CNY', '人民币元'),
    ('COP', '哥伦比亚比索'),
    ('CRC', '哥斯达黎加科朗'),
    ('CUC', '古巴可兑换比索'),
    ('CUP', '古巴比索'),
    ('CVE', '佛得角埃斯库多'),
    ('CZK', '捷克克朗'),
    ('DJF', '吉布提法郎'),
    ('DKK', '丹麦克朗'),
    ('DOP', '多米尼加比索'),
    ('DZD', '阿尔及利亚第纳尔'),
    ('EGP', '埃及镑'),
    ('ERN', '厄立特里亚纳克法'),
    ('ETB', '埃塞俄比亚比尔'),
    ('EUR', '欧元'),
    ('FJD', '斐济元'),
    ('FKP', '福克兰群岛镑'),
    ('GBP', '英镑'),
    ('GEL', '格鲁吉亚拉里'),
    ('GHS', '加纳塞地'),
    ('GIP', '直布罗陀镑'),
    ('GMD', '冈比亚达拉西'),
    ('GNF', '几内亚法郎'),
    ('GTQ', '危地马拉格查尔'),
    ('GYD', '圭亚那元'),
    ('HKD', '港元'),
    ('HNL', '洪都拉斯伦皮拉'),
    ('HRK', '克罗地亚库纳'),
    ('HTG', '海地古德'),
    ('HUF', '匈牙利福林'),
    ('IDR', '印尼盾'),
    ('ILS', '以色列新谢克尔'),
    ('INR', '印度卢比'),
    ('IQD', '伊拉克第纳尔'),
    ('IRR', '伊朗里亚尔'),
    ('ISK', '冰岛克朗'),
    ('JMD', '牙买加元'),
    ('JOD', '约旦第纳尔'),
    ('JPY', '日圆'),
    ('KES', '肯尼亚先令'),
    ('KGS', '吉尔吉斯斯坦索姆'),
    ('KHR', '柬埔寨瑞尔'),
    ('KMF', '科摩罗法郎'),
    ('KPW', '朝鲜圆'),
    ('KRW', '韩圆'),
    ('KWD', '科威特第纳尔'),
    ('KYD', '开曼群岛元'),
    ('KZT', '哈萨克斯坦坚戈'),
    ('LAK', '老挝基普'),
    ('LBP', '黎巴嫩镑'),
    ('LKR', '斯里兰卡卢比'),
    ('LRD', '利比里亚元'),
    ('LSL', '莱索托洛蒂'),
    ('LYD', '利比亚第纳尔'),
    ('MAD', '摩洛哥迪尔汗'),
    ('MDL', '摩尔多瓦列伊'),
    ('MGA', '马达加斯加阿里亚里'),
    ('MKD', '马其顿代纳尔'),
    ('MMK', '缅元'),
    ('MNT', '蒙古图格里克'),
    ('MOP', '澳门币'),
    ('MRU', '毛里塔尼亚乌吉亚'),
    ('MUR', '毛里求斯卢比'),
    ('MVR', '马尔代夫拉菲亚'),
    ('MWK', '马拉维克瓦查'),
    ('MXN', '墨西哥比索'),
    ('MXV', '墨西哥发展单位'),
    ('MYR', '马来西亚令吉'),
    ('MZN', '莫桑比克梅蒂卡尔'),
    ('NAD', '纳米比亚元'),
    ('NGN', '尼日利亚奈拉'),
    ('NIO', '尼加拉瓜科多巴'),
    ('NOK', '挪威克朗'),
    ('NPR', '尼泊尔卢比'),
    ('NZD', '新西兰元'),
    ('OMR', '阿曼里亚尔'),
    ('PAB', '巴拿马巴波亚'),
    ('PEN', '秘鲁索尔'),
    ('PGK', '巴布亚新几内亚基那'),
    ('PHP', '菲律宾比索'),
    ('PKR', '巴基斯坦卢比'),
    ('PLN', '波兰兹罗提'),
    ('PYG', '巴拉圭瓜拉尼'),
    ('QAR', '卡塔尔里亚尔'),
    ('RON', '罗马尼亚列伊'),
    ('RSD', '塞尔维亚第纳尔'),
    ('RUB', '俄罗斯卢布'),
    ('RWF', '卢旺达法郎'),
    ('SAR', '沙特里亚尔'),
    ('SBD', '所罗门群岛元'),
    ('SCR', '塞舌尔卢比'),
    ('SDG', '苏丹镑'),
    ('SEK', '瑞典克朗'),
    ('SGD', '新加坡元'),
    ('SHP', '圣赫勒拿镑'),
    ('SLL', '塞拉利昂利昂'),
    ('SOS', '索马里先令'),
    ('SRD', '苏里南元'),
    ('SSP', '南苏丹镑'),
    ('STN', '圣多美和普林西比多布拉'),
    ('SYP', '叙利亚镑'),
    ('SZL', '斯威士兰里兰吉尼'),
    ('THB', '泰铢'),
    ('TJS', '塔吉克斯坦索莫尼'),
    ('TMT', '土库曼斯坦马纳特'),
    ('TND', '突尼斯第纳尔'),
    ('TOP', '汤加潘加'),
    ('TRY', '土耳其里拉'),
    ('TTD', '特立尼达和多巴哥元'),
    ('TWD', '新台币'),
    ('TZS', '坦桑尼亚先令'),
    ('UAH', '乌克兰格里夫纳'),
    ('UGX', '乌干达先令'),
    ('USD', '美元'),
    ('UYU', '乌拉圭比索'),
    ('UZS', '乌兹别克斯坦索姆'),
    ('VES', '委内瑞拉玻利瓦尔'),
    ('VND', '越南盾'),
    ('VUV', '瓦努阿图瓦图'),
    ('WST', '萨摩亚塔拉'),
    ('YER', '也门里亚尔'),
    ('ZAR', '南非兰特'),
    ('ZMW', '赞比亚克瓦查')]


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def exchange_rate(instance, from_str, to_str):
    try:
        from_code = sorted(map(lambda item: (item[0], string_similar(from_str, item[1])), table), key=lambda x: x[1], reverse=True)[0][0]
        to_code = sorted(map(lambda item: (item[0], string_similar(to_str, item[1])), table), key=lambda x: x[1], reverse=True)[0][0]
        url = f"http://webforex.hermes.hexun.com/forex/quotelist?code=FOREX{from_code}{to_code}&column=Code,Price"
        print(from_str, to_str, url)
        res = requests.get(url, headers={'User-Agent':
                                         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
                                         'Accept-Language':
                                         'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                                         'Host':
                                         'webforex.hermes.hexun.com'})
        rate = json.loads(res.text[1:-2])["Data"][0][0][1]/10000
        instance.ui.status.setText(f'从{from_str}到{to_str}的汇率是: {rate}')
    except Exception as ex:
        instance.ui.status.setText(random.choice(['这超出了我的知识范围了呢', '我还需要学习']))
        print(ex)


def play_music(instance):
    win32api.ShellExecute(0, 'open', '8071.mp3', '', 'assets', 1)
    instance.ui.status.setText('请欣赏《难忘今宵》')


def report_date(instance):
    instance.ui.status.setText(f'今天是{datetime.now().strftime("%Y年%m月%d日星期%w")}')


def report_time(instance):
    instance.ui.status.setText(f'现在是北京时间{datetime.now().strftime("%H时%M分%S秒")}')


def open_program(instance, program_name):
    if '浏览器' in program_name:
        win32api.ShellExecute(0, 'open', 'www.hao123.com', '', '', 1)

    elif '文本编辑器' in program_name or '记事本' in program_name or '文本文件' in program_name:
        win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)

    elif '计算器' in program_name:
        win32api.ShellExecute(0, 'open', 'calc.exe', '', '', 1)

    elif '日历' in program_name:
        win32api.ShellExecute(0, 'open', 'calender.exe', '', '', 1)

    elif '微信' in program_name:
        win32api.ShellExecute(0, 'open', "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe", '', '', 1)

    elif '音乐播放器' in program_name:
        win32api.ShellExecute(0, 'open', '8071.mp3', '', 'assets', 1)

    else:
        instance.ui.status.setText(random.choice(['这超出了我的知识范围了呢', '我还需要学习']))


def search(instance, keyword, engine):
    win32api.ShellExecute(0, 'open', f'www.{engine}.com/{"s?wd" if engine == "baidu" else "search?q"}={keyword}', '', '', 1)
