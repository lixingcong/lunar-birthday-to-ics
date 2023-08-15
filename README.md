# 农历生日导出到ics日历文件

## 依赖：

- [ics-py](https://github.com/ics-py/ics-py)

- [LunarCalendar](https://github.com/wolfhong/LunarCalendar)

## 使用

```
pip3 install ics
pip3 install LunarCalendar

# 生成从今年开始的未来50年的农历生日
python3 main.py -i config.json -c 50

# 或者直接导出到文件
python3 main.py -i config.json -c 50 > /tmp/exported.ics
```

注意[config.json](config-example.json)中的```birthday```字段为公历出生日期

## 导入到Google日历

1. 为确保不影响现有的日历，先在[Google日历](https://calendar.google.com)中创建一个单独的日历，如"我的农历生日"
2. 设置该日历的"全天日程"默认提醒方式，如"提前3日发邮件+提前4小时弹出提醒"
3. 将ics导入到该日历
4. 若有误操作，可以直接删除该日历

## 参考项目

- [农历事件生成器lcal](https://github.com/hotoo/lcal)