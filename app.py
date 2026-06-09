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
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "綜合戰機", "owned": True},
                    {"code": "M2", "name": "綜合平台", "owned": True},
                    {"code": "M3", "name": "大型機倉", "owned": False},
                    {"code": "A1", "name": "龍石火炮", "owned": True},
                    {"code": "A2", "name": "防空導彈", "owned": True},
                    {"code": "B1", "name": "導彈防禦", "owned": True},
                    {"code": "B2", "name": "炮艇平台", "owned": True},
                    {"code": "B3", "name": "無人機台", "owned": False},
                ],
            },
            {
                "name": "太陽鯨",
                "tech": 91,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "護航艇倉", "owned": True},
                    {"code": "M2", "name": "大型載機", "owned": False},
                    {"code": "A1", "name": "綜合武器", "owned": True},
                    {"code": "A2", "name": "投射平台", "owned": True},
                    {"code": "A3", "name": "綜合火炮", "owned": False},
                    {"code": "B1", "name": "載機維護", "owned": True},
                    {"code": "B2", "name": "炮艇平台", "owned": False},
                    {"code": "C1", "name": "載機平台", "owned": True},
                    {"code": "C2", "name": "攻城飛機", "owned": True},
                    {"code": "C3", "name": "防空導彈", "owned": False},
                ],
            },
            {
                "name": "南十字元帥級",
                "tech": 0,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "綜合武器", "owned": True},
                    {"code": "M2", "name": "綜合武器", "owned": False},
                    {"code": "A1", "name": "載機平台", "owned": True},
                    {"code": "A2", "name": "護航艇倉", "owned": False},
                    {"code": "B1", "name": "載機平台", "owned": False},
                    {"code": "B2", "name": "導彈防禦", "owned": False},
                    {"code": "B3", "name": "偵查飛機", "owned": False},
                    {"code": "C1", "name": "能源系統", "owned": True},
                    {"code": "C2", "name": "火控輔助", "owned": False},
                ],
            },
            {
                "name": "永恆蒼穹級",
                "tech": 0,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "機庫一型", "owned": True},
                    {"code": "M2", "name": "機庫二型", "owned": False},
                    {"code": "M3", "name": "機庫三型", "owned": False},
                    {"code": "A1", "name": "火炮系統", "owned": True},
                    {"code": "A2", "name": "離子炮塔", "owned": False},
                    {"code": "A3", "name": "脈衝防空", "owned": False},
                    {"code": "B1", "name": "反艦投射", "owned": False},
                    {"code": "B2", "name": "防禦攔截", "owned": False},
                    {"code": "B3", "name": "防空平台", "owned": False},
                    {"code": "C1", "name": "大型載機", "owned": False},
                    {"code": "C2", "name": "火控輔助", "owned": False},
                    {"code": "C3", "name": "維修飛機", "owned": False},
                ],
            },
            {
                "name": "FSV830",
                "tech": 65,
                "owned": True,
                "modules": [
                    {"code": "A1", "name": "工程維修", "owned": True},
                    {"code": "A2", "name": "戰略存儲", "owned": True},
                    {"code": "B1", "name": "護衛生產", "owned": True},
                    {"code": "B2", "name": "炮艇生產", "owned": True},
                    {"code": "B3", "name": "戰機生產", "owned": False},
                    {"code": "C1", "name": "載機平台", "owned": True},
                    {"code": "C2", "name": "維修飛機", "owned": True},
                    {"code": "D1", "name": "預警指揮", "owned": True},
                    {"code": "D2", "name": "協同指揮", "owned": True},
                    {"code": "D3", "name": "干擾指揮", "owned": False},
                    {"code": "E1", "name": "區域防空", "owned": False},
                    {"code": "E2", "name": "護航艇倉", "owned": False},
                ],
            },
            {
                "name": "埃迪卡拉級",
                "tech": 0,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "堡壘重炮", "owned": True},
                    {"code": "M2", "name": "堡壘軌道", "owned": False},
                    {"code": "B1", "name": "護衛生產", "owned": True},
                    {"code": "B2", "name": "炮艇生產", "owned": True},
                    {"code": "B3", "name": "驅逐生產", "owned": False},
                    {"code": "C1", "name": "大型載機", "owned": False},
                    {"code": "C2", "name": "炮艇船塢", "owned": False},
                    {"code": "D1", "name": "苔原攔截", "owned": True},
                    {"code": "D2", "name": "蜂鳥偵查", "owned": False},
                    {"code": "D3", "name": "巨像護衛", "owned": False},
                    {"code": "E1", "name": "重型裝甲", "owned": False},
                    {"code": "E2", "name": "納米維修", "owned": False},
                ],
            },
        ],
    },

    {
        "category": "戰鬥巡洋艦",
        "ships": [
            {
                "name": "新君士坦丁大帝級",
                "tech": 1,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "離子攻擊", "owned": True},
                    {"code": "M2", "name": "離子投射", "owned": False},
                    {"code": "A1", "name": "投射攻擊", "owned": True},
                    {"code": "A2", "name": "投射攻擊", "owned": False},
                    {"code": "B1", "name": "通用火炮", "owned": True},
                    {"code": "B2", "name": "脈衝防空", "owned": False},
                    {"code": "B3", "name": "防空導彈", "owned": True},
                    {"code": "C1", "name": "能源系統", "owned": True},
                    {"code": "C2", "name": "艦載機倉", "owned": False},
                    {"code": "C3", "name": "偵察機倉", "owned": True},
                    {"code": "D1", "name": "防空系統", "owned": True},
                    {"code": "D2", "name": "防護模組", "owned": False},
                    {"code": "D3", "name": "損管系統", "owned": False},
                ],
            },
            {"name": "安東塔斯持劍者級", "tech": 0, "owned": False},
            {
                "name": "烏拉諾斯之矛",
                "tech": 54,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "重軌道炮", "owned": True},
                    {"code": "M2", "name": "離子炮塔", "owned": False},
                    {"code": "A1", "name": "堡壘火炮", "owned": True},
                    {"code": "A2", "name": "堡壘火炮", "owned": True},
                    {"code": "A3", "name": "堡壘火炮", "owned": False},
                    {"code": "B1", "name": "礦車投射", "owned": False},
                    {"code": "B2", "name": "護航艇倉", "owned": False},
                    {"code": "B3", "name": "損管系統", "owned": False},
                    {"code": "C1", "name": "防空系統", "owned": True},
                    {"code": "C2", "name": "附加裝甲", "owned": False},
                    {"code": "C3", "name": "攔截系統", "owned": True},
                ],
            },
            {
                "name": "普魯圖斯之盾",
                "tech": 250,
                "owned": True,
                "modules": [
                    {"code": "M1", "name": "綜合武器", "owned": True},
                    {"code": "M2", "name": "綜合火炮", "owned": False},
                    {"code": "M3", "name": "礦車投射", "owned": False},
                    {"code": "A1", "name": "堡壘護衛", "owned": True},
                    {"code": "A2", "name": "火控A型", "owned": False},
                    {"code": "A3", "name": "火控B型", "owned": False},
                    {"code": "B1", "name": "綜合維修", "owned": False},
                    {"code": "B2", "name": "附加裝甲", "owned": False},
                    {"code": "B3", "name": "反導攔截", "owned": False},
                    {"code": "C1", "name": "多重反擊", "owned": False},
                    {"code": "C2", "name": "防空攔截", "owned": False},
                    {"code": "C3", "name": "重型投射", "owned": False},
                ],
            },
            {"name": "永恆風暴", "tech": 0, "owned": True},
            {"name": "ST59", "tech": 15, "owned": True},
            {"name": "雷火之星", "tech": 0, "owned": True},
        ],
    },

    {
        "category": "巡洋艦",
        "ships": [
            {"name": "艾奧級", "tech": 0, "owned": True, "variants": [
                {"name": "離子炮", "owned": True, "progress": ""},
                {"name": "反艦型", "owned": False, "progress": "20%"},
                {"name": "攻城型", "owned": False, "progress": "20%"},
            ]},
            {"name": "奇美拉級", "tech": 50, "owned": True, "variants": [
                {"name": "炮彈型", "owned": True, "progress": ""},
                {"name": "重炮型", "owned": True, "progress": ""},
                {"name": "防衛型", "owned": True, "progress": ""},
            ]},
            {"name": "卡利斯托級", "tech": 83, "owned": True, "variants": [
                {"name": "魚雷型", "owned": True, "progress": ""},
                {"name": "反艦型", "owned": True, "progress": ""},
                {"name": "支援型", "owned": False, "progress": "0%"},
            ]},
            {"name": "獵兵級", "tech": 50, "owned": True, "variants": [
                {"name": "支援型", "owned": True, "progress": ""},
                {"name": "反艦型", "owned": True, "progress": ""},
            ]},
            {"name": "康納混沌級", "tech": 0, "owned": True, "variants": [
                {"name": "軌道炮", "owned": True, "progress": ""},
                {"name": "電漿型", "owned": False, "progress": "35%"},
            ]},
            {"name": "光錐級", "tech": 20, "owned": True, "variants": [
                {"name": "通用型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": True, "progress": ""},
                {"name": "突擊型", "owned": True, "progress": ""},
            ]},
            {"name": "狩獵者級", "tech": 70, "owned": True, "variants": [
                {"name": "通用型", "owned": True, "progress": ""},
                {"name": "戰術型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": False, "progress": "20%"},
            ]},
            {"name": "CAS066級", "tech": 75, "owned": True, "variants": [
                {"name": "綜合型", "owned": True, "progress": ""},
                {"name": "炮擊型", "owned": True, "progress": ""},
                {"name": "載機型", "owned": False, "progress": "20%"},
                {"name": "支援型", "owned": False, "progress": "80%"},
            ]},
            {"name": "KCCPV2.0", "tech": 9, "owned": True, "variants": [
                {"name": "綜合型", "owned": True, "progress": ""},
                {"name": "載機型", "owned": True, "progress": ""},
                {"name": "軌道炮", "owned": False, "progress": "0%"},
                {"name": "脈衝型", "owned": True, "progress": ""},
            ]},
            {"name": "遊騎兵級", "tech": 0, "owned": False, "variants": [
                {"name": "綜合型", "owned": False, "progress": ""},
                {"name": "離子炮", "owned": False, "progress": ""},
            ]},
        ],
    },

    {
        "category": "驅逐艦",
        "ships": [
            {"name": "鬥牛級", "tech": 0, "owned": True, "variants": [
                {"name": "攻擊型", "owned": True, "progress": ""},
                {"name": "突擊型", "owned": True, "progress": ""},
                {"name": "防禦型", "owned": False, "progress": "50%"},
            ]},
            {"name": "鬩神星級", "tech": 132, "owned": True, "variants": [
                {"name": "火炮型", "owned": True, "progress": ""},
                {"name": "重炮型", "owned": True, "progress": ""},
                {"name": "裝甲型", "owned": True, "progress": ""},
            ]},
            {"name": "亞達伯拉級", "tech": 100, "owned": True, "variants": [
                {"name": "通用型", "owned": True, "progress": ""},
                {"name": "裝甲型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": False, "progress": "0%"},
            ]},
            {"name": "創神星級", "tech": 75, "owned": True, "variants": [
                {"name": "軌道炮", "owned": True, "progress": ""},
                {"name": "魚雷型", "owned": True, "progress": ""},
            ]},
            {"name": "槍騎兵級", "tech": 111, "owned": True, "variants": [
                {"name": "反艦型", "owned": True, "progress": ""},
                {"name": "綜合型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": True, "progress": ""},
            ]},
            {"name": "衛士級", "tech": 3, "owned": True, "variants": [
                {"name": "支援型", "owned": True, "progress": ""},
                {"name": "兩棲型", "owned": False, "progress": "25%"},
                {"name": "脈衝炮", "owned": False, "progress": "50%"},
            ]},
            {"name": "苔原級", "tech": 15, "owned": True, "variants": [
                {"name": "支援型", "owned": True, "progress": ""},
                {"name": "載機型", "owned": True, "progress": ""},
            ]},
            {"name": "谷神星級", "tech": 185, "owned": True, "variants": [
                {"name": "載機型", "owned": True, "progress": ""},
                {"name": "支援型", "owned": True, "progress": ""},
                {"name": "戰術型", "owned": False, "progress": "25%"},
            ]},
            {"name": "AC721級", "tech": 85, "owned": True, "variants": [
                {"name": "通用型", "owned": True, "progress": ""},
                {"name": "載機型", "owned": True, "progress": ""},
                {"name": "飛彈型", "owned": False, "progress": "0%"},
            ]},
        ],
    },

    {
        "category": "護衛艦",
        "ships": [
            {"name": "刺水母級", "tech": 225, "owned": True, "variants": [
                {"name": "特種型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": True, "progress": ""},
                {"name": "登陸型", "owned": False, "progress": "0%"},
            ]},
            {"name": "鋯石級", "tech": 0, "owned": False, "variants": [
                {"name": "突擊型", "owned": False, "progress": ""},
                {"name": "特種型", "owned": False, "progress": ""},
            ]},
            {"name": "雷里亞特級", "tech": 75, "owned": True, "variants": [
                {"name": "反艦型", "owned": True, "progress": ""},
                {"name": "魚雷型", "owned": True, "progress": ""},
                {"name": "隱身型", "owned": True, "progress": ""},
            ]},
            {"name": "紅寶石級", "tech": 95, "owned": True, "variants": [
                {"name": "軌道炮", "owned": True, "progress": ""},
                {"name": "粒子炮", "owned": True, "progress": ""},
                {"name": "防衛型", "owned": False, "progress": "35%"},
            ]},
            {"name": "雨海級", "tech": 0, "owned": False, "variants": [
                {"name": "軌道炮", "owned": False, "progress": ""},
                {"name": "脈衝型", "owned": False, "progress": ""},
            ]},
            {"name": "卡里萊恩級", "tech": 100, "owned": True, "variants": [
                {"name": "偵查型", "owned": True, "progress": ""},
                {"name": "重炮型", "owned": True, "progress": ""},
                {"name": "特種型", "owned": True, "progress": ""},
            ]},
            {"name": "澄海級", "tech": 0, "owned": True, "variants": [
                {"name": "反艦型", "owned": True, "progress": ""},
                {"name": "飛彈型", "owned": False, "progress": "0%"},
                {"name": "防空型", "owned": False, "progress": "0%"},
            ]},
            {"name": "諾瑪級", "tech": 106, "owned": True, "variants": [
                {"name": "攻城型", "owned": True, "progress": ""},
                {"name": "支援型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": True, "progress": ""},
            ]},
            {"name": "靜海級", "tech": 66, "owned": True, "variants": [
                {"name": "綜合型", "owned": True, "progress": ""},
                {"name": "脈衝型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": True, "progress": ""},
            ]},
            {"name": "雲海級", "tech": 0, "owned": True, "variants": [
                {"name": "突擊型", "owned": True, "progress": ""},
                {"name": "防空型", "owned": True, "progress": ""},
            ]},
            {"name": "狼蜥級", "tech": 0, "owned": False, "variants": [
                {"name": "防禦型", "owned": False, "progress": ""},
                {"name": "突擊型", "owned": False, "progress": ""},
                {"name": "特種型", "owned": False, "progress": ""},
            ]},
            {"name": "FG300級", "tech": 45, "owned": True, "variants": [
                {"name": "多功能", "owned": True, "progress": ""},
                {"name": "裝甲型", "owned": True, "progress": ""},
                {"name": "偵察型", "owned": True, "progress": ""},
            ]},
        ],
    },

    {
        "category": "護航艇",
        "ships": [
            {"name": "星雲追逐者", "tech": 105, "owned": True, "variants": [
                {"name": "彈炮型", "owned": True, "progress": ""},
                {"name": "脈衝型", "owned": True, "progress": ""},
            ]},
            {"name": "CV-T800", "tech": 123, "owned": True},
            {"name": "蜂巢守衛者", "tech": 50, "owned": True},
            {"name": "S-列維9號", "tech": 69, "owned": True},
            {"name": "虛靈", "tech": 0, "owned": True},
            {"name": "海爾波普", "tech": 0, "owned": False, "variants": [
                {"name": "多功能", "owned": False, "progress": ""},
                {"name": "對接型", "owned": False, "progress": ""},
            ]},
            {"name": "坦普爾1號", "tech": 0, "owned": False, "variants": [
                {"name": "干擾型", "owned": False, "progress": ""},
                {"name": "預警型", "owned": False, "progress": ""},
            ]},
            {"name": "RB7-13", "tech": 0, "owned": True, "variants": [
                {"name": "攻擊型", "owned": True, "progress": ""},
                {"name": "突防型", "owned": False, "progress": "0%"},
            ]},
            {"name": "鰩", "tech": 5, "owned": True, "variants": [
                {"name": "高速型", "owned": True, "progress": ""},
                {"name": "防禦型", "owned": False, "progress": "0%"},
            ]},
            {"name": "CV-M011", "tech": 100, "owned": True, "variants": [
                {"name": "導彈型", "owned": True, "progress": ""},
                {"name": "火炮型", "owned": False, "progress": "35%"},
                {"name": "高速型", "owned": True, "progress": ""},
            ]},
            {"name": "CV-II003", "tech": 8, "owned": True},
        ],
    },

    {
        "category": "戰機",
        "ships": [
            {"name": "密斯托拉", "tech": 90, "owned": True},
            {"name": "雷火V022", "tech": 0, "owned": False, "variants": [
                {"name": "防空型", "owned": False, "progress": ""},
                {"name": "特種型", "owned": False, "progress": ""},
                {"name": "干擾型", "owned": False, "progress": ""},
            ]},
            {"name": "海氏追隨者", "tech": 0, "owned": False},
            {"name": "林鴞A100", "tech": 0, "owned": True},
            {"name": "砂龍", "tech": 41, "owned": True},
            {"name": "維塔斯 A021", "tech": 0, "owned": False},
            {"name": "孢子A404", "tech": 0, "owned": True},
            {"name": "新大地B192", "tech": 0, "owned": True},
            {"name": "佩刀Aer410", "tech": 5, "owned": True},
            {"name": "平衡安德森", "tech": 0, "owned": True},
            {"name": "SC002", "tech": 4, "owned": True},
            {"name": "AT021", "tech": 0, "owned": True, "variants": [
                {"name": "脈衝型", "owned": True, "progress": ""},
                {"name": "干擾型", "owned": False, "progress": "20%"},
                {"name": "多功能", "owned": False, "progress": "0%"},
            ]},
            {"name": "維塔斯 B010", "tech": 106, "owned": True},
            {"name": "刺鰩", "tech": 58, "owned": True},
            {"name": "牛蛙", "tech": 10, "owned": True},
            {"name": "BR050", "tech": 0, "owned": True, "variants": [
                {"name": "反艦型", "owned": True, "progress": ""},
                {"name": "多用途", "owned": False, "progress": "0%"},
                {"name": "魚雷型", "owned": False, "progress": "0%"},
            ]},
        ],
    },
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
    total_ship = 0
    owned_ship = 0

    total_variant = 0
    owned_variant = 0

    total_module = 0
    owned_module = 0

    total_tech = 0

    for category in data:
        category_ship_total = 0
        category_ship_owned = 0

        category_variant_total = 0
        category_variant_owned = 0

        category_module_total = 0
        category_module_owned = 0

        category_tech = 0

        for ship in category["ships"]:
            total_ship += 1
            category_ship_total += 1

            if ship.get("owned", False):
                owned_ship += 1
                category_ship_owned += 1

            tech = int(ship.get("tech", 0))
            total_tech += tech
            category_tech += tech

            for variant in ship.get("variants", []):
                total_variant += 1
                category_variant_total += 1

                if variant.get("owned", False):
                    owned_variant += 1
                    category_variant_owned += 1

            for module in ship.get("modules", []):
                total_module += 1
                category_module_total += 1

                if module.get("owned", False):
                    owned_module += 1
                    category_module_owned += 1

        category["ship_total"] = category_ship_total
        category["ship_owned"] = category_ship_owned
        category["variant_total"] = category_variant_total
        category["variant_owned"] = category_variant_owned
        category["module_total"] = category_module_total
        category["module_owned"] = category_module_owned
        category["tech_sum"] = category_tech

        category_total = category_ship_total + category_variant_total + category_module_total
        category_owned = category_ship_owned + category_variant_owned + category_module_owned

        category["total"] = category_total
        category["owned"] = category_owned
        category["percent"] = round(category_owned / category_total * 100, 1) if category_total else 0

    total_all = total_ship + total_variant + total_module
    owned_all = owned_ship + owned_variant + owned_module

    return {
        "ship_total": total_ship,
        "ship_owned": owned_ship,
        "variant_total": total_variant,
        "variant_owned": owned_variant,
        "module_total": total_module,
        "module_owned": owned_module,
        "total": total_all,
        "owned": owned_all,
        "percent": round(owned_all / total_all * 100, 1) if total_all else 0,
        "total_tech": total_tech,
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