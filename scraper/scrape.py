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
    {"id": "aaron", "name": "Aaron A-shirt", "cat": "上衣", "desc": "基础A字背心"},
    {"id": "albert", "name": "Albert 围裙", "cat": "家居", "desc": "经典围裙，含口袋和绑带"},
    {"id": "bella", "name": "Bella 女装原型", "cat": "版型基础", "desc": "女装合体上衣原型，含胸省腰省"},
    {"id": "breanna", "name": "Breanna 女装原型", "cat": "版型基础", "desc": "女装宽松上衣原型"},
    {"id": "bruce", "name": "Bruce 拳击短裤", "cat": "裤装", "desc": "男士拳击短裤"},
    {"id": "charlie", "name": "Charlie 休闲裤", "cat": "裤装", "desc": "五袋休闲长裤"},
    {"id": "diana", "name": "Diana 连衣裙", "cat": "连衣裙", "desc": "裹身连衣裙"},
    {"id": "florence", "name": "Florence 口罩", "cat": "配饰", "desc": "立体口罩"},
    {"id": "hortensia", "name": "Hortensia 手提包", "cat": "包袋", "desc": "拉链手提包，含侧片和底片"},
    {"id": "hugo", "name": "Hugo 连帽衫", "cat": "上衣", "desc": "连帽卫衣，含插肩袖"},
    {"id": "lucy", "name": "Lucy 口袋裙", "cat": "裙装", "desc": "系带口袋裙"},
    {"id": "penelope", "name": "Penelope 铅笔裙", "cat": "裙装", "desc": "高腰铅笔裙"},
    {"id": "sandy", "name": "Sandy 圆裙", "cat": "裙装", "desc": "圆裙/半圆裙"},
    {"id": "simon", "name": "Simon 衬衫", "cat": "上衣", "desc": "经典男士衬衫"},
    {"id": "sven", "name": "Sven 卫衣", "cat": "上衣", "desc": "圆领卫衣"},
    {"id": "tamiko", "name": "Tamiko 上衣", "cat": "上衣", "desc": "零浪费T恤"},
    {"id": "teagan", "name": "Teagan T恤", "cat": "上衣", "desc": "基础合体T恤"},
    {"id": "titan", "name": "Titan 裤装原型", "cat": "版型基础", "desc": "裤装基础原型"},
    {"id": "wahid", "name": "Wahid 马甲", "cat": "上衣", "desc": "经典西装马甲"},
    {"id": "yuri", "name": "Yuri 连帽衫", "cat": "上衣", "desc": "拉链连帽衫"},
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
