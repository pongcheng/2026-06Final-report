from flask import Flask, render_template, request
from copy import deepcopy

app = Flask(__name__)


# =========================
# 7月新番推薦資料
# =========================
ANIME_DATA = [
    {
        "name": "BLEACH 千年血戰篇 - The Calamity",
        "type": "熱血 / 戰鬥",
        "reason": "適合喜歡戰鬥、隊長級角色、經典少年漫畫續作的觀眾。",
        "tags": ["熱血", "戰鬥", "續作", "少年"]
    },
    {
        "name": "攻殼機動隊 新作動畫",
        "type": "科幻 / 賽博龐克",
        "reason": "適合喜歡未來科技、AI、網路犯罪與哲學設定的觀眾。",
        "tags": ["科幻", "AI", "深度", "賽博龐克"]
    },
    {
        "name": "Bungo Stray Dogs Wan! 2",
        "type": "日常 / 搞笑",
        "reason": "適合想看輕鬆、角色互動、番外日常的人。",
        "tags": ["日常", "搞笑", "輕鬆", "續作"]
    },
    {
        "name": "Young Ladies Don't Play Fighting Games",
        "type": "校園 / 遊戲",
        "reason": "適合喜歡校園、格鬥遊戲、女性角色互動題材的觀眾。",
        "tags": ["校園", "遊戲", "輕鬆", "青春"]
    },
    {
        "name": "From Old Country Bumpkin to Master Swordsman S2",
        "type": "奇幻 / 劍術",
        "reason": "適合喜歡劍術、師徒、奇幻成長題材的觀眾。",
        "tags": ["奇幻", "戰鬥", "劍術", "成長"]
    }
]


# =========================
# 三角洲 S9 槍枝推薦資料
# =========================
DELTA_GUNS = [
    {
        "name": "M7 戰鬥步槍",
        "type": "T0 / 全距離萬金油",
        "reason": "中遠距離穩定，傷害與控制性平衡，適合大多數玩家當主武器。",
        "tags": ["全距離", "穩定", "新手", "中距離", "T0"]
    },
    {
        "name": "ASVAL 巨浪",
        "type": "T0 / 近距離爆發",
        "reason": "近戰秒人能力很高，適合室內清房、快速突臉與高機動玩法。",
        "tags": ["近距離", "爆發", "突臉", "室內", "T0"]
    },
    {
        "name": "SR-25",
        "type": "T0 / 連狙壓制",
        "reason": "適合中遠距離補槍、架點、精準輸出，滿改後穩定度高。",
        "tags": ["遠距離", "架點", "精準", "連狙", "T0"]
    },
    {
        "name": "M82A1 巴雷特",
        "type": "T0 / 反器材狙擊",
        "reason": "遠距離威懾力強，適合大壩、長街等開闊地圖架槍。",
        "tags": ["遠距離", "狙擊", "架點", "高傷害", "T0"]
    },
    {
        "name": "AR-57",
        "type": "T0.5 / 高射速突擊",
        "reason": "射速快、彈量大，適合清房與快速壓制。",
        "tags": ["近距離", "高射速", "清房", "突擊", "T0.5"]
    },
    {
        "name": "PKM",
        "type": "T0.5 / 火力支援",
        "reason": "彈量大、持續火力強，適合守點、封路與團隊壓制。",
        "tags": ["火力", "守點", "便宜", "壓制", "T0.5"]
    }
]


# =========================
# J-POP 推薦資料
# =========================
JPOP_DATA = [
    {
        "name": "YOASOBI",
        "type": "雙人音樂組合 / 故事型流行",
        "reason": "適合喜歡旋律強、故事感、動漫主題曲風格的人。",
        "tags": ["動漫", "流行", "故事感", "高人氣"]
    },
    {
        "name": "Ado",
        "type": "女歌手 / 爆發型嗓音",
        "reason": "適合喜歡強烈情緒、爆發力、暗黑流行風格的人。",
        "tags": ["爆發", "女聲", "暗黑", "高音"]
    },
    {
        "name": "米津玄師 Kenshi Yonezu",
        "type": "創作歌手 / 抒情與流行",
        "reason": "適合喜歡細膩歌詞、獨特旋律與日劇動畫主題曲的人。",
        "tags": ["抒情", "創作", "男聲", "流行"]
    },
    {
        "name": "Official髭男dism",
        "type": "樂團 / 都會流行",
        "reason": "適合喜歡高音男聲、鋼琴流行、情感豐富歌曲的人。",
        "tags": ["樂團", "男聲", "抒情", "流行"]
    },
    {
        "name": "King Gnu",
        "type": "樂團 / 混合搖滾",
        "reason": "適合喜歡搖滾、節奏變化、成熟感與強烈編曲的人。",
        "tags": ["樂團", "搖滾", "成熟", "節奏"]
    },
    {
        "name": "Mrs. GREEN APPLE",
        "type": "樂團 / 青春流行",
        "reason": "適合喜歡青春、明亮、節奏感強、現場感的歌曲。",
        "tags": ["青春", "樂團", "明亮", "流行"]
    }
]


# =========================
# 無盡 / 星際獵人藍圖資料
# =========================
BLUEPRINT_TEMPLATE = [
    {
        "category": "航空母艦",
        "ships": [
            {
                "name": "CV3000",
                "tech": 53,
                "variants": [
                    {"name": "綜合戰機", "owned": True},
                    {"name": "綜合平台", "owned": True},
                    {"name": "大型機倉", "owned": False}
                ]
            },
            {
                "name": "太陽鯨",
                "tech": 91,
                "variants": [
                    {"name": "護航艇倉", "owned": True},
                    {"name": "大型載機", "owned": False},
                    {"name": "載機平台", "owned": True},
                    {"name": "維修飛機", "owned": True}
                ]
            },
            {
                "name": "FSV830",
                "tech": 65,
                "variants": [
                    {"name": "工程維修", "owned": True},
                    {"name": "戰略存儲", "owned": True},
                    {"name": "炮艇生產", "owned": True},
                    {"name": "戰機生產", "owned": False}
                ]
            }
        ]
    },
    {
        "category": "戰鬥巡洋艦",
        "ships": [
            {
                "name": "新君士坦丁大帝級",
                "tech": 1,
                "variants": [
                    {"name": "離子攻擊", "owned": True},
                    {"name": "離子投射", "owned": False},
                    {"name": "通用火炮", "owned": True},
                    {"name": "能源系統", "owned": True}
                ]
            },
            {
                "name": "烏拉諾斯之矛",
                "tech": 54,
                "variants": [
                    {"name": "重軌道炮", "owned": True},
                    {"name": "堡壘火炮", "owned": True},
                    {"name": "防空系統", "owned": True},
                    {"name": "附加裝甲", "owned": False}
                ]
            },
            {
                "name": "普魯圖斯之盾",
                "tech": 250,
                "variants": [
                    {"name": "綜合武器", "owned": True},
                    {"name": "綜合火炮", "owned": False},
                    {"name": "附加裝甲", "owned": False},
                    {"name": "反導攔截", "owned": False}
                ]
            },
            {
                "name": "ST59",
                "tech": 15,
                "variants": [
                    {"name": "重軌道炮", "owned": True},
                    {"name": "攻堅魚雷", "owned": True},
                    {"name": "軌道炮塔", "owned": True},
                    {"name": "電磁裝甲", "owned": True}
                ]
            }
        ]
    },
    {
        "category": "巡洋艦",
        "ships": [
            {
                "name": "艾奧級",
                "tech": 0,
                "variants": [
                    {"name": "離子炮", "owned": True},
                    {"name": "反艦型", "owned": False},
                    {"name": "攻城型", "owned": False}
                ]
            },
            {
                "name": "奇美拉級",
                "tech": 50,
                "variants": [
                    {"name": "炮彈型", "owned": True},
                    {"name": "重炮型", "owned": True},
                    {"name": "防衛型", "owned": True}
                ]
            },
            {
                "name": "卡利斯托級",
                "tech": 83,
                "variants": [
                    {"name": "魚雷型", "owned": True},
                    {"name": "反艦型", "owned": True},
                    {"name": "支援型", "owned": False}
                ]
            },
            {
                "name": "獵兵級",
                "tech": 50,
                "variants": [
                    {"name": "支援型", "owned": True},
                    {"name": "反艦型", "owned": True}
                ]
            },
            {
                "name": "CAS066級",
                "tech": 75,
                "variants": [
                    {"name": "綜合型", "owned": True},
                    {"name": "炮擊型", "owned": True},
                    {"name": "載機型", "owned": False}
                ]
            }
        ]
    }
]


def filter_items(items, selected_tags):
    if not selected_tags:
        return items

    result = []
    for item in items:
        score = len(set(item["tags"]) & set(selected_tags))
        if score > 0:
            new_item = item.copy()
            new_item["score"] = score
            result.append(new_item)

    result.sort(key=lambda x: x["score"], reverse=True)
    return result


def get_all_tags(items):
    tags = []
    for item in items:
        for tag in item["tags"]:
            if tag not in tags:
                tags.append(tag)
    return tags


def calculate_blueprint(data):
    total = 0
    owned = 0
    total_tech = 0

    for category in data:
        category_total = 0
        category_owned = 0
        category_tech = 0

        for ship in category["ships"]:
            category_tech += ship["tech"]
            total_tech += ship["tech"]

            for variant in ship["variants"]:
                total += 1
                category_total += 1

                if variant["owned"]:
                    owned += 1
                    category_owned += 1

        category["total"] = category_total
        category["owned"] = category_owned
        category["percent"] = round(category_owned / category_total * 100, 1) if category_total else 0
        category["tech_sum"] = category_tech

    percent = round(owned / total * 100, 1) if total else 0

    return {
        "total": total,
        "owned": owned,
        "percent": percent,
        "total_tech": total_tech
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/anime", methods=["GET", "POST"])
def anime():
    selected_tags = request.form.getlist("tags")
    result = filter_items(ANIME_DATA, selected_tags)

    return render_template(
        "recommend.html",
        page_title="7月新番推薦系統",
        page_desc="依照你喜歡的題材，推薦適合觀看的 7 月新番。",
        items=result,
        tags=get_all_tags(ANIME_DATA),
        selected_tags=selected_tags
    )


@app.route("/delta", methods=["GET", "POST"])
def delta():
    selected_tags = request.form.getlist("tags")
    result = filter_items(DELTA_GUNS, selected_tags)

    return render_template(
        "recommend.html",
        page_title="三角洲 S9 強力槍枝推薦系統",
        page_desc="依照作戰距離、打法與槍枝定位，推薦 S9 適合使用的武器。",
        items=result,
        tags=get_all_tags(DELTA_GUNS),
        selected_tags=selected_tags
    )


@app.route("/jpop", methods=["GET", "POST"])
def jpop():
    selected_tags = request.form.getlist("tags")
    result = filter_items(JPOP_DATA, selected_tags)

    return render_template(
        "recommend.html",
        page_title="J-POP 歌曲／歌手／團體推薦系統",
        page_desc="依照曲風、情緒與歌手特色，推薦適合的 J-POP 歌手或團體。",
        items=result,
        tags=get_all_tags(JPOP_DATA),
        selected_tags=selected_tags
    )


@app.route("/blueprint", methods=["GET", "POST"])
def blueprint():
    data = deepcopy(BLUEPRINT_TEMPLATE)

    if request.method == "POST":
        for c_index, category in enumerate(data):
            for s_index, ship in enumerate(category["ships"]):
                tech_key = f"tech_{c_index}_{s_index}"
                if tech_key in request.form:
                    try:
                        ship["tech"] = int(request.form.get(tech_key, 0))
                    except ValueError:
                        ship["tech"] = 0

                for v_index, variant in enumerate(ship["variants"]):
                    checkbox_key = f"owned_{c_index}_{s_index}_{v_index}"
                    variant["owned"] = checkbox_key in request.form

    summary = calculate_blueprint(data)

    return render_template(
        "blueprint.html",
        data=data,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)