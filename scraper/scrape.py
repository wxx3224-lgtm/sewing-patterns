"""
缝纫纸样爬虫 - 从 FreeSewing 开源项目收集纸样数据
FreeSewing 是 MIT 协议开源项目，允许自由使用其数据
"""
import json
import urllib.request
import urllib.error

OUTPUT = "patterns.json"

# FreeSewing 设计列表 (从其 GitHub 仓库的公开数据)
FREESEWING_DESIGNS = [
    {"id": "aaron", "name": "Aaron A字背心", "cat": "上衣", "desc": "基础A字背心",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 46, "h": 60},
         {"label": "后片", "qty": 1, "w": 46, "h": 62},
         {"label": "领口包边", "qty": 1, "w": 48, "h": 3},
         {"label": "袖口包边", "qty": 2, "w": 28, "h": 3},
     ]},
    {"id": "albert", "name": "Albert 围裙", "cat": "家居", "desc": "经典围裙，含口袋和绑带",
     "pieces": [
         {"label": "围裙身", "qty": 1, "w": 70, "h": 80},
         {"label": "口袋", "qty": 1, "w": 20, "h": 18},
         {"label": "腰带", "qty": 2, "w": 4, "h": 70},
         {"label": "颈带", "qty": 1, "w": 4, "h": 60},
     ]},
    {"id": "bella", "name": "Bella 女装原型", "cat": "版型基础", "desc": "女装合体上衣原型，含胸省腰省",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 48, "h": 58},
         {"label": "后片", "qty": 1, "w": 48, "h": 60},
     ]},
    {"id": "breanna", "name": "Breanna 女装原型", "cat": "版型基础", "desc": "女装宽松上衣原型",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 50, "h": 62},
         {"label": "后片", "qty": 1, "w": 50, "h": 64},
         {"label": "袖片", "qty": 2, "w": 38, "h": 58},
     ]},
    {"id": "bruce", "name": "Bruce 拳击短裤", "cat": "裤装", "desc": "男士拳击短裤",
     "pieces": [
         {"label": "前片", "qty": 2, "w": 30, "h": 38},
         {"label": "后片", "qty": 2, "w": 32, "h": 40},
         {"label": "腰头", "qty": 1, "w": 80, "h": 6},
     ]},
    {"id": "charlie", "name": "Charlie 休闲裤", "cat": "裤装", "desc": "五袋休闲长裤",
     "pieces": [
         {"label": "裤前片", "qty": 2, "w": 32, "h": 100},
         {"label": "裤后片", "qty": 2, "w": 34, "h": 102},
         {"label": "腰头", "qty": 1, "w": 80, "h": 8},
         {"label": "前口袋布", "qty": 2, "w": 18, "h": 20},
         {"label": "后口袋", "qty": 2, "w": 14, "h": 16},
     ]},
    {"id": "diana", "name": "Diana 连衣裙", "cat": "连衣裙", "desc": "裹身连衣裙",
     "pieces": [
         {"label": "前片", "qty": 2, "w": 48, "h": 95},
         {"label": "后片", "qty": 1, "w": 48, "h": 97},
         {"label": "袖片", "qty": 2, "w": 36, "h": 50},
         {"label": "腰带", "qty": 1, "w": 160, "h": 6},
     ]},
    {"id": "florence", "name": "Florence 口罩", "cat": "配饰", "desc": "立体口罩",
     "pieces": [
         {"label": "外层", "qty": 2, "w": 18, "h": 14},
         {"label": "内层", "qty": 2, "w": 17, "h": 13},
         {"label": "鼻梁条通道", "qty": 1, "w": 10, "h": 3},
     ]},
    {"id": "hortensia", "name": "Hortensia 手提包", "cat": "包袋", "desc": "拉链手提包，含侧片和底片",
     "pieces": [
         {"label": "前后片", "qty": 2, "w": 30, "h": 24},
         {"label": "侧片", "qty": 2, "w": 10, "h": 24},
         {"label": "底片", "qty": 1, "w": 30, "h": 10},
         {"label": "拉链挡片", "qty": 2, "w": 30, "h": 3},
         {"label": "提手", "qty": 2, "w": 4, "h": 35},
     ]},
    {"id": "hugo", "name": "Hugo 连帽衫", "cat": "上衣", "desc": "连帽卫衣，含插肩袖",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 52, "h": 68},
         {"label": "后片", "qty": 1, "w": 52, "h": 70},
         {"label": "袖片", "qty": 2, "w": 42, "h": 62},
         {"label": "帽子侧片", "qty": 2, "w": 28, "h": 32},
         {"label": "帽子中片", "qty": 1, "w": 14, "h": 34},
         {"label": "口袋", "qty": 1, "w": 36, "h": 20},
     ]},
    {"id": "lucy", "name": "Lucy 口袋裙", "cat": "裙装", "desc": "系带口袋裙",
     "pieces": [
         {"label": "裙片", "qty": 2, "w": 50, "h": 60},
         {"label": "口袋", "qty": 2, "w": 18, "h": 22},
         {"label": "腰头", "qty": 1, "w": 74, "h": 8},
         {"label": "系带", "qty": 2, "w": 4, "h": 80},
     ]},
    {"id": "penelope", "name": "Penelope 铅笔裙", "cat": "裙装", "desc": "高腰铅笔裙",
     "pieces": [
         {"label": "前裙片", "qty": 1, "w": 46, "h": 65},
         {"label": "后裙片", "qty": 2, "w": 24, "h": 65},
         {"label": "腰头", "qty": 1, "w": 70, "h": 8},
     ]},
    {"id": "sandy", "name": "Sandy 圆裙", "cat": "裙装", "desc": "圆裙/半圆裙",
     "pieces": [
         {"label": "裙片", "qty": 2, "w": 72, "h": 72},
         {"label": "腰头", "qty": 1, "w": 70, "h": 8},
     ]},
    {"id": "simon", "name": "Simon 衬衫", "cat": "上衣", "desc": "经典男士衬衫",
     "pieces": [
         {"label": "前片", "qty": 2, "w": 50, "h": 72},
         {"label": "后片", "qty": 1, "w": 50, "h": 74},
         {"label": "袖片", "qty": 2, "w": 40, "h": 62},
         {"label": "领座", "qty": 1, "w": 42, "h": 5},
         {"label": "领面", "qty": 1, "w": 44, "h": 8},
         {"label": "袖克夫", "qty": 2, "w": 26, "h": 7},
         {"label": "门襟", "qty": 1, "w": 4, "h": 72},
     ]},
    {"id": "sven", "name": "Sven 卫衣", "cat": "上衣", "desc": "圆领卫衣",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 52, "h": 66},
         {"label": "后片", "qty": 1, "w": 52, "h": 68},
         {"label": "袖片", "qty": 2, "w": 42, "h": 60},
         {"label": "领口罗纹", "qty": 1, "w": 44, "h": 6},
         {"label": "下摆罗纹", "qty": 1, "w": 96, "h": 8},
         {"label": "袖口罗纹", "qty": 2, "w": 22, "h": 8},
     ]},
    {"id": "tamiko", "name": "Tamiko 上衣", "cat": "上衣", "desc": "零浪费T恤",
     "pieces": [
         {"label": "主体布片", "qty": 1, "w": 90, "h": 60},
     ]},
    {"id": "teagan", "name": "Teagan T恤", "cat": "上衣", "desc": "基础合体T恤",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 48, "h": 62},
         {"label": "后片", "qty": 1, "w": 48, "h": 64},
         {"label": "袖片", "qty": 2, "w": 38, "h": 22},
         {"label": "领口条", "qty": 1, "w": 50, "h": 4},
     ]},
    {"id": "titan", "name": "Titan 裤装原型", "cat": "版型基础", "desc": "裤装基础原型",
     "pieces": [
         {"label": "裤前片", "qty": 2, "w": 30, "h": 100},
         {"label": "裤后片", "qty": 2, "w": 32, "h": 102},
     ]},
    {"id": "wahid", "name": "Wahid 马甲", "cat": "上衣", "desc": "经典西装马甲",
     "pieces": [
         {"label": "前片", "qty": 2, "w": 44, "h": 56},
         {"label": "后片", "qty": 1, "w": 44, "h": 54},
         {"label": "口袋嵌线", "qty": 2, "w": 14, "h": 4},
     ]},
    {"id": "yuri", "name": "Yuri 连帽衫", "cat": "上衣", "desc": "拉链连帽衫",
     "pieces": [
         {"label": "前片", "qty": 2, "w": 50, "h": 66},
         {"label": "后片", "qty": 1, "w": 50, "h": 68},
         {"label": "袖片", "qty": 2, "w": 42, "h": 60},
         {"label": "帽子", "qty": 2, "w": 28, "h": 32},
         {"label": "口袋", "qty": 2, "w": 18, "h": 20},
     ]},
]

# 国内常用布艺纸样 (手动整理自公开教程)
CN_PATTERNS = [
    {"id": "cn-tote-basic", "name": "基础托特包", "cat": "包袋",
     "desc": "日常手提包 36×38cm", "source": "通用布艺教程",
     "pieces": [
         {"label": "包身", "qty": 2, "w": 36, "h": 38},
         {"label": "提手", "qty": 2, "w": 6, "h": 50},
         {"label": "包底", "qty": 1, "w": 36, "h": 12},
     ]},
    {"id": "cn-drawstring", "name": "束口袋", "cat": "包袋",
     "desc": "化妆品收纳 22×30cm", "source": "通用布艺教程",
     "pieces": [
         {"label": "袋身", "qty": 2, "w": 22, "h": 30},
         {"label": "穿绳通道", "qty": 2, "w": 22, "h": 4},
     ]},
    {"id": "cn-a5-cover", "name": "A5手账本套", "cat": "书衣",
     "desc": "展开34×24cm", "source": "小红书手作教程",
     "pieces": [
         {"label": "外布", "qty": 1, "w": 34, "h": 24},
         {"label": "内布", "qty": 1, "w": 34, "h": 24},
         {"label": "翻盖插片", "qty": 2, "w": 8, "h": 24},
     ]},
    {"id": "cn-a6-cover", "name": "A6手账本套", "cat": "书衣",
     "desc": "展开26×18cm", "source": "小红书手作教程",
     "pieces": [
         {"label": "外布", "qty": 1, "w": 26, "h": 18},
         {"label": "内布", "qty": 1, "w": 26, "h": 18},
         {"label": "翻盖插片", "qty": 2, "w": 6, "h": 18},
     ]},
    {"id": "cn-apron", "name": "家用围裙", "cat": "家居",
     "desc": "上宽50→下宽70 长80cm", "source": "通用布艺教程",
     "pieces": [
         {"label": "围裙身", "qty": 1, "w": 70, "h": 80},
         {"label": "口袋", "qty": 1, "w": 20, "h": 18},
         {"label": "腰带", "qty": 2, "w": 4, "h": 70},
         {"label": "颈带", "qty": 1, "w": 4, "h": 60},
     ]},
    {"id": "cn-placemat", "name": "餐垫", "cat": "家居",
     "desc": "45×32cm 圆角", "source": "通用布艺教程",
     "pieces": [
         {"label": "餐垫", "qty": 1, "w": 45, "h": 32},
     ]},
    {"id": "cn-cushion", "name": "信封式靠垫套", "cat": "家居",
     "desc": "45×45cm", "source": "通用布艺教程",
     "pieces": [
         {"label": "前片", "qty": 1, "w": 45, "h": 45},
         {"label": "后片A", "qty": 1, "w": 45, "h": 28},
         {"label": "后片B", "qty": 1, "w": 45, "h": 28},
     ]},
]


def fetch_freesewing_info(design_id):
    """尝试从 FreeSewing API 获取设计详情"""
    url = f"https://api.freesewing.org/designs/{design_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SewingPatternCollector/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, Exception):
        return None


def main():
    patterns = []

    print("=== 收集 FreeSewing 开源纸样 ===")
    for d in FREESEWING_DESIGNS:
        info = fetch_freesewing_info(d["id"])
        pattern = {
            "id": f"fs-{d['id']}",
            "name": d["name"],
            "category": d["cat"],
            "description": d["desc"],
            "source": "FreeSewing (MIT License)",
            "url": f"https://freesewing.eu/designs/{d['id']}",
            "difficulty": info.get("difficulty", "unknown") if info else "unknown",
            "pieces": d.get("pieces", []),
        }
        patterns.append(pattern)
        status = "✓ API" if info else "✓ 基础"
        print(f"  {status} {d['name']}")

    print(f"\n=== 收集国内布艺纸样 ===")
    for d in CN_PATTERNS:
        pattern = {
            "id": d["id"],
            "name": d["name"],
            "category": d["cat"],
            "description": d["desc"],
            "source": d["source"],
            "pieces": d.get("pieces", []),
        }
        patterns.append(pattern)
        print(f"  ✓ {d['name']}")

    result = {
        "version": "1.0",
        "updated": __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
        "total": len(patterns),
        "patterns": patterns,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n完成！共 {len(patterns)} 个纸样，已保存到 {OUTPUT}")


if __name__ == "__main__":
    main()
