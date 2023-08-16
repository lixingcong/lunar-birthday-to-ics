# 农历生日导出到ics日历文件

## 依赖：

- Python 3.6+

- [ics-py](https://github.com/ics-py/ics-py)

- [LunarCalendar](https://github.com/wolfhong/LunarCalendar)

## 使用

```
pip install ics
pip install LunarCalendar

# 生成从今年开始的未来50年的农历生日
python3 main.py -i config.json -c 50

# 打印结果类似如下
BEGIN:VCALENDAR
VERSION:2.0
PRODID:ics.py - http://git.io/lLljaA
BEGIN:VEVENT
DTSTART;VALUE=DATE:20230813
DTSTAMP:20230816T020257Z
DESCRIPTION:祝生日快乐，2023年出生，又长大一岁
SUMMARY:小白的农历0岁生日
UID:85d259a9-5907-407d-be57-311c0f85bf81@85d2.org
END:VEVENT
BEGIN:VEVENT
DTSTART;VALUE=DATE:20230806
DTSTAMP:20230816T020257Z
DESCRIPTION:祝生日快乐，2020年出生，又长大一岁
SUMMARY:小明的农历3岁生日
UID:ed34efc1-e6c3-4672-a9a8-5ff96aaa2cb1@ed34.org
END:VEVENT
END:VCALENDAR
```

将脚本输出的内容，重定向到文件，即可导出为ics

```
python3 main.py -i config.json -c 50 > /tmp/exported.ics
```

注意[config.json](config-example.json)中的```birthday```字段为公历出生日期，须遵循```yyyy-mm-dd```格式

## 导入到Google日历

1. 为确保不影响现有的日历，先在[Google日历](https://calendar.google.com)中创建一个单独的日历，如"我的农历生日"
2. 设置该日历的"全天日程"默认提醒方式，如"提前3日发邮件+提前4小时弹出提醒"
3. 将ics导入到该日历
4. 若有误操作，可以直接删除该日历

## 参考项目

- [农历事件生成器lcal](https://github.com/hotoo/lcal)