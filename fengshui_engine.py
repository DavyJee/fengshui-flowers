"""
风水花卉推荐引擎 v3.0
Feng Shui Flower Recommendation Engine

基于五行、方位、房间功能、生肖诉求的风水花卉推荐系统
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ==================== 枚举定义 ====================

class Direction(Enum):
    """房屋方位/朝向"""
    EAST = ("东", "木", "青绿")
    SOUTHEAST = ("东南", "木", "青绿")
    SOUTH = ("南", "火", "红紫")
    SOUTHWEST = ("西南", "土", "黄棕")
    WEST = ("西", "金", "白金")
    NORTHWEST = ("西北", "金", "白金")
    NORTH = ("北", "水", "蓝黑")
    NORTHEAST = ("东北", "土", "黄咖")
    CENTER = ("中", "土", "黄紫")

    def __init__(self, name_cn: str, element: str, colors: str):
        self._name_cn = name_cn
        self._element = element
        self._colors = colors

    @property
    def name_cn(self):
        return self._name_cn

    @property
    def element(self):
        return self._element

    @property
    def colors(self):
        return self._colors


class RoomType(Enum):
    """房间类型"""
    LIVING_ROOM = ("客厅", "招财旺宅、待客", ["大门对角线财位", "电视柜两侧", "主位旁"])
    BEDROOM = ("卧室", "助眠安神、夫妻和睦", ["床头柜", "窗台", "梳妆台旁"])
    STUDY = ("书房", "旺文昌、聚精会神", ["书桌", "书架", "文昌位"])
    KITCHEN = ("厨房", "去油净气、添活力", ["窗台", "橱柜上方", "冰箱顶"])
    BATHROOM = ("卫生间", "去晦气、转运势", ["洗手台旁", "角落", "窗台"])
    BALCONY = ("阳台", "接气纳财、旺宅", ["阳光充足处", "角落"])
    ENTRANCE = ("玄关", "迎气送气、第一印象", ["鞋柜上方", "入门两侧"])
    DINING = ("餐厅", "增进食欲、和睦", ["餐桌旁", "餐边柜"])

    def __init__(self, name_cn: str, purpose: str, good_positions: list):
        self._name_cn = name_cn
        self._purpose = purpose
        self._good_positions = good_positions

    @property
    def name_cn(self):
        return self._name_cn

    @property
    def purpose(self):
        return self._purpose

    @property
    def good_positions(self):
        return self._good_positions


class ChineseZodiac(Enum):
    """十二生肖"""
    RAT = ("鼠", "水")
    OX = ("牛", "土")
    TIGER = ("虎", "木")
    RABBIT = ("兔", "木")
    DRAGON = ("龙", "土")
    SNAKE = ("蛇", "火")
    HORSE = ("马", "火")
    GOAT = ("羊", "土")
    MONKEY = ("猴", "金")
    ROOSTER = ("鸡", "金")
    DOG = ("狗", "土")
    PIG = ("猪", "水")

    def __init__(self, name: str, element: str):
        self._name = name
        self._element = element

    @property
    def name(self):
        return self._name

    @property
    def element(self):
        return self._element


# ==================== 花种数据库 ====================

FLOWER_DATABASE = {
    "绿萝": {
        "element": "木", "colors": ["绿"], "flower_language": "坚韧、善良",
        "feng_shui": "旺财、净化空气", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "书房", "卫生间"],
        "wishes": ["招财", "健康"]
    },
    "吊兰": {
        "element": "木", "colors": ["绿", "白"], "flower_language": "无奈、无奈的爱",
        "feng_shui": "去煞气、旺宅", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "阳台", "卧室"],
        "wishes": ["健康", "招财"]
    },
    "文竹": {
        "element": "木", "colors": ["绿"], "flower_language": "永恒、友情",
        "feng_shui": "旺文昌、利学业", "toxic": False, "difficulty": 3,
        "bloom_season": "全年", "light": "散光", "positions": ["书房", "客厅"],
        "wishes": ["事业"]
    },
    "虎皮兰": {
        "element": "金", "colors": ["绿", "黄"], "flower_language": "刚毅、坚强",
        "feng_shui": "旺财、去煞气", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "卧室", "玄关"],
        "wishes": ["招财", "健康"]
    },
    "发财树": {
        "element": "木", "colors": ["绿"], "flower_language": "招财进宝、事业有成",
        "feng_shui": "旺财、旺事业", "toxic": False, "difficulty": 2,
        "bloom_season": "5-11月", "light": "散光", "positions": ["客厅", "办公室"],
        "wishes": ["招财", "事业"]
    },
    "幸福树": {
        "element": "木", "colors": ["绿"], "flower_language": "幸福美满",
        "feng_shui": "家庭和睦、旺宅", "toxic": False, "difficulty": 2,
        "bloom_season": "5-9月", "light": "散光", "positions": ["客厅", "阳台"],
        "wishes": ["健康", "桃花"]
    },
    "平安树": {
        "element": "木", "colors": ["绿"], "flower_language": "平安吉祥",
        "feng_shui": "保平安、护健康", "toxic": False, "difficulty": 2,
        "bloom_season": "冬季", "light": "散光", "positions": ["客厅", "玄关"],
        "wishes": ["健康", "招财"]
    },
    "鸿运当头": {
        "element": "火", "colors": ["红"], "flower_language": "好运连连、完美",
        "feng_shui": "招好运、旺家运", "toxic": False, "difficulty": 2,
        "bloom_season": "全年", "light": "散光", "positions": ["客厅", "卧室"],
        "wishes": ["招财", "事业", "桃花"]
    },
    "红掌": {
        "element": "火", "colors": ["红"], "flower_language": "热情、大展宏图",
        "feng_shui": "招财、旺人缘", "toxic": True, "difficulty": 2,
        "bloom_season": "全年", "light": "散光", "positions": ["客厅", "办公室"],
        "wishes": ["招财", "事业"]
    },
    "白掌": {
        "element": "金", "colors": ["白"], "flower_language": "纯洁、和平",
        "feng_shui": "事业顺利、一帆风顺", "toxic": False, "difficulty": 1,
        "bloom_season": "5-8月", "light": "散光", "positions": ["客厅", "书房"],
        "wishes": ["事业", "健康"]
    },
    "君子兰": {
        "element": "火", "colors": ["红", "黄"], "flower_language": "高贵、君子之风",
        "feng_shui": "旺家运、利人际关系", "toxic": False, "difficulty": 3,
        "bloom_season": "冬春", "light": "散光", "positions": ["客厅", "书房"],
        "wishes": ["事业", "桃花", "健康"]
    },
    "蝴蝶兰": {
        "element": "木", "colors": ["粉", "紫"], "flower_language": "幸福飞来、爱你",
        "feng_shui": "旺姻缘、增感情", "toxic": False, "difficulty": 4,
        "bloom_season": "2-5月", "light": "散光", "positions": ["客厅", "卧室"],
        "wishes": ["桃花", "健康"]
    },
    "茉莉花": {
        "element": "金", "colors": ["白"], "flower_language": "纯洁、忠贞",
        "feng_shui": "旺感情、添香气", "toxic": False, "difficulty": 3,
        "bloom_season": "5-8月", "light": "全阳", "positions": ["阳台", "庭院"],
        "wishes": ["桃花", "健康"]
    },
    "栀子花": {
        "element": "金", "colors": ["白"], "flower_language": "坚强、永恒的爱",
        "feng_shui": "旺桃花、旺学业", "toxic": False, "difficulty": 3,
        "bloom_season": "5-7月", "light": "全阳", "positions": ["阳台", "庭院"],
        "wishes": ["桃花", "事业"]
    },
    "薄荷": {
        "element": "木", "colors": ["绿"], "flower_language": "真诚、温暖",
        "feng_shui": "去晦气、清醒头脑", "toxic": False, "difficulty": 1,
        "bloom_season": "5-10月", "light": "全阳", "positions": ["厨房", "阳台"],
        "wishes": ["健康", "事业"]
    },
    "铜钱草": {
        "element": "水", "colors": ["绿"], "flower_language": "财运滚滚、花开富贵",
        "feng_shui": "旺财、水生金", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "散光", "positions": ["客厅", "书房"],
        "wishes": ["招财"]
    },
    "水仙": {
        "element": "水", "colors": ["白", "黄"], "flower_language": "自恋、思念",
        "feng_shui": "旺文才、增智慧", "toxic": True, "difficulty": 2,
        "bloom_season": "冬季", "light": "全阳", "positions": ["客厅", "书房"],
        "wishes": ["事业"]
    },
    "风信子": {
        "element": "水", "colors": ["蓝", "紫"], "flower_language": "胜利、竞技",
        "feng_shui": "旺事业、聚人气", "toxic": True, "difficulty": 2,
        "bloom_season": "3-4月", "light": "全阳", "positions": ["阳台", "窗台"],
        "wishes": ["事业", "桃花"]
    },
    "仙人掌": {
        "element": "金", "colors": ["绿"], "flower_language": "坚强、奇迹",
        "feng_shui": "防辐射、去煞气", "toxic": False, "difficulty": 1,
        "bloom_season": "夏季", "light": "全阳", "positions": ["阳台", "书桌"],
        "wishes": ["健康"]
    },
    "多肉植物": {
        "element": "金", "colors": ["绿", "红", "黄"], "flower_language": "坚韧、可爱",
        "feng_shui": "旺土气、防小人", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "全阳", "positions": ["阳台", "书桌"],
        "wishes": ["健康", "招财"]
    },
    "月季": {
        "element": "火", "colors": ["红", "粉"], "flower_language": "爱情、美丽",
        "feng_shui": "旺姻缘、添魅力", "toxic": False, "difficulty": 2,
        "bloom_season": "4-9月", "light": "全阳", "positions": ["阳台", "庭院"],
        "wishes": ["桃花", "健康"]
    },
    "绣球": {
        "element": "火", "colors": ["蓝", "粉"], "flower_language": "希望、团聚",
        "feng_shui": "旺人缘、助姻缘", "toxic": False, "difficulty": 2,
        "bloom_season": "5-7月", "light": "散光", "positions": ["阳台", "庭院"],
        "wishes": ["桃花", "健康"]
    },
    "三角梅": {
        "element": "火", "colors": ["红", "紫"], "flower_language": "热情、坚韧",
        "feng_shui": "旺财运、增活力", "toxic": False, "difficulty": 1,
        "bloom_season": "4-11月", "light": "全阳", "positions": ["阳台", "庭院"],
        "wishes": ["招财", "事业"]
    },
    "常春藤": {
        "element": "木", "colors": ["绿"], "flower_language": "忠诚、永恒",
        "feng_shui": "去煞气、保平安", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "阳台"],
        "wishes": ["健康", "事业"]
    },
    "龟背竹": {
        "element": "木", "colors": ["绿"], "flower_language": "健康、长寿",
        "feng_shui": "旺健康、增福寿", "toxic": False, "difficulty": 2,
        "bloom_season": "全年", "light": "散光", "positions": ["客厅", "卧室"],
        "wishes": ["健康", "招财"]
    },
    "薰衣草": {
        "element": "火", "colors": ["紫"], "flower_language": "等待、浪漫",
        "feng_shui": "助睡眠、旺姻缘", "toxic": False, "difficulty": 3,
        "bloom_season": "5-8月", "light": "全阳", "positions": ["卧室", "阳台"],
        "wishes": ["桃花", "健康"]
    },
    "黄金葛": {
        "element": "木", "colors": ["绿", "黄"], "flower_language": "财运亨通、吉祥",
        "feng_shui": "旺财、水生金", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "书房"],
        "wishes": ["招财"]
    },
    "万年青": {
        "element": "土", "colors": ["绿"], "flower_language": "健康长寿、吉祥",
        "feng_shui": "旺宅、保平安", "toxic": True, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "玄关"],
        "wishes": ["健康", "事业"]
    },
    "富贵竹": {
        "element": "木", "colors": ["绿"], "flower_language": "富贵吉祥、竹报平安",
        "feng_shui": "旺财、旺学业", "toxic": False, "difficulty": 1,
        "bloom_season": "全年", "light": "耐阴", "positions": ["客厅", "书房"],
        "wishes": ["招财", "事业"]
    },
}


# ==================== 房间禁忌 ====================

ROOM_RESTRICTIONS = {
    "卧室": {
        "avoid_flowers": ["仙人掌"],
        "avoid_features": ["有毒", "过香", "大叶"],
    },
    "厨房": {
        "avoid_flowers": ["水仙", "风信子"],
        "avoid_features": ["花粉过多", "招蚊虫"],
    },
    "卫生间": {
        "avoid_flowers": [],
        "avoid_features": ["喜阳", "干燥"],
    },
    "书房": {
        "avoid_flowers": ["仙人掌"],
        "avoid_features": ["过于艳丽"],
    },
}


# ==================== 推荐结果数据类 ====================

@dataclass
class Recommendation:
    """推荐结果"""
    flower: str
    color: str
    position: str
    reason: str
    element_match: str
    feng_shui_benefit: str
    matched_wishes: list
    warnings: list


@dataclass
class RecommendationSet:
    """完整推荐结果集"""
    direction: str
    room: str
    element: str
    zodiac: str
    wishes: list
    recommendations: list
    summary: str


# ==================== 推荐引擎核心 ====================

class FengShuiFlowerEngine:
    """风水花卉推荐引擎"""

    def __init__(self):
        self.flower_db = FLOWER_DATABASE
        self.room_restrictions = ROOM_RESTRICTIONS

    @staticmethod
    def get_zodiac_element(zodiac: str) -> str:
        """根据生肖获取五行"""
        zodiac_map = {
            "鼠": "水", "牛": "土", "虎": "木", "兔": "木",
            "龙": "土", "蛇": "火", "马": "火", "羊": "土",
            "猴": "金", "鸡": "金", "狗": "土", "猪": "水"
        }
        return zodiac_map.get(zodiac, "木")

    def filter_by_room(self, room: RoomType) -> list:
        """根据房间筛选花种"""
        restrictions = self.room_restrictions.get(room.name_cn, {})
        avoid_flowers = restrictions.get("avoid_flowers", [])
        avoid_features = restrictions.get("avoid_features", [])

        candidates = []
        for name, data in self.flower_db.items():
            if name in avoid_flowers:
                continue
            if "有毒" in avoid_features and data["toxic"]:
                continue
            if "过香" in avoid_features and data["difficulty"] >= 4:
                continue
            if "大叶" in avoid_features and "龟背竹" in name:
                continue
            if room.name_cn in data["positions"]:
                candidates.append(name)

        return candidates if candidates else list(self.flower_db.keys())[:10]

    def filter_by_wishes(self, wishes: list, candidates: list) -> tuple:
        """根据诉求筛选，返回(优先列表, 次选列表)"""
        if not wishes:
            return candidates, []

        primary = []
        secondary = []

        for flower in candidates:
            data = self.flower_db[flower]
            flower_wishes = data.get("wishes", [])

            if any(w in flower_wishes for w in wishes):
                primary.append(flower)
            else:
                secondary.append(flower)

        return primary, secondary

    def rank_by_match(
        self,
        direction: Direction,
        room: RoomType,
        flowers: list,
        wishes: list,
        user_element: str = None
    ) -> list:
        """综合评分排序"""
        target_element = user_element if user_element else direction.element
        target_colors = direction.colors.split("、")

        scored = []
        for flower in flowers:
            data = self.flower_db[flower]
            score = 0

            # 五行匹配得分
            if data["element"] == target_element:
                score += 10
            elif target_element == "木" and data["element"] in ["水", "火"]:
                score += 5

            # 用户生肖五行额外加成
            if user_element and data["element"] == user_element:
                score += 5  # 生肖五行匹配额外加分

            # 颜色匹配得分
            if any(c in target_colors for c in data["colors"]):
                score += 5

            # 房间位置匹配得分
            if room.name_cn in data["positions"]:
                score += 3

            # 诉求匹配得分（核心！）
            if wishes:
                flower_wishes = data.get("wishes", [])
                if any(w in flower_wishes for w in wishes):
                    score += 15  # 诉求匹配权重最高

            scored.append((flower, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [f for f, _ in scored]

    def generate_reason(
        self,
        direction: Direction,
        room: RoomType,
        flower: str,
        matched_wishes: list,
        zodiac: str = None
    ) -> str:
        """生成推荐原因"""
        data = self.flower_db[flower]
        reasons = []

        # 生肖原因
        if zodiac:
            zodiac_element = self.get_zodiac_element(zodiac)
            reasons.append(f"您属{zodiac}（{zodiac_element}行），{flower}属{data['element']}性，与您相生相助")

        # 方位五行原因
        if data["element"] == direction.element:
            reasons.append(f"{direction.element}气旺盛，{flower}属{data['element']}性，契合{direction.name_cn}方位")
        else:
            reasons.append(f"{flower}属{data['element']}性，可调和{direction.name_cn}方位的{direction.element}气")

        # 房间功能原因
        room_reasons = {
            "客厅": "客厅放此花可招财旺宅",
            "卧室": "其清香有助睡眠，净化卧室空气",
            "书房": "文雅之气有助于提升学业事业运",
            "厨房": "可吸收油烟，净化厨房空气",
            "卫生间": "耐阴去阴气，改善卫生间风水",
            "阳台": "向阳而生，吸纳天地灵气",
            "玄关": "迎气送气，开门见绿添生机",
            "餐厅": "增添用餐愉悦氛围",
        }
        if room.name_cn in room_reasons:
            reasons.append(room_reasons[room.name_cn])

        # 诉求原因
        if matched_wishes:
            wish_reasons = {
                "招财": "利于招财进宝，增强财运",
                "桃花": "利于姻缘感情，增添桃花运",
                "事业": "利于事业发展，提升事业运",
                "健康": "利于身体健康，增强体质",
            }
            for w in matched_wishes[:1]:
                if w in wish_reasons:
                    reasons.append(wish_reasons[w])

        return "；".join(reasons)

    def get_warnings(self, room: RoomType, flower: str) -> list:
        """获取注意事项"""
        warnings = []
        data = self.flower_db[flower]

        if data["toxic"]:
            warnings.append("此花有一定毒性，避免儿童和宠物接触")
        if data["difficulty"] >= 4:
            warnings.append("此花养护难度较高，需要细心照料")

        return warnings

    def recommend(
        self,
        direction: Direction,
        room: RoomType,
        zodiac: str = None,
        wishes: list = None,
        top_n: int = 3
    ) -> RecommendationSet:
        """
        推荐函数

        Args:
            direction: 房屋朝向/方位
            room: 房间类型
            zodiac: 用户生肖（可选）
            wishes: 客户诉求列表（可选），如["招财", "桃花"]
            top_n: 返回推荐数量
        """
        wishes = wishes or []
        user_element = self.get_zodiac_element(zodiac) if zodiac else None
        target_element = user_element if user_element else direction.element

        # 1. 筛选候选：五行符合 + 房间适合
        candidates = [
            name for name, data in self.flower_db.items()
            if data["element"] == target_element
        ]
        room_candidates = self.filter_by_room(room)
        candidates = list(set(candidates) & set(room_candidates))

        # 放宽条件
        if len(candidates) < top_n:
            candidates = list(set(list(self.flower_db.keys())) & set(room_candidates))
        if len(candidates) < top_n:
            candidates = list(self.flower_db.keys())[:top_n * 2]

        # 2. 诉求筛选
        primary, secondary = self.filter_by_wishes(wishes, candidates)
        candidates = primary + secondary

        # 3. 综合评分排序
        candidates = self.rank_by_match(direction, room, candidates, wishes, user_element)

        # 4. 生成推荐结果
        recommendations = []
        for flower in candidates[:top_n]:
            data = self.flower_db[flower]

            # 匹配到的诉求
            matched = [w for w in wishes if w in data.get("wishes", [])]

            # 推荐颜色
            recommended_colors = [c for c in data["colors"] if c in direction.colors.split("、")]
            if not recommended_colors:
                recommended_colors = data["colors"]

            # 摆放位置
            position = room.good_positions[0] if room.good_positions else "角落"

            rec = Recommendation(
                flower=flower,
                color="、".join(recommended_colors),
                position=position,
                reason=self.generate_reason(direction, room, flower, matched, zodiac),
                element_match=data["element"],
                feng_shui_benefit=data["feng_shui"],
                matched_wishes=matched,
                warnings=self.get_warnings(room, flower)
            )
            recommendations.append(rec)

        # 5. 生成总结
        zodiac_str = f"您属{zodiac}，" if zodiac else ""
        wish_str = "、".join(wishes) if wishes else "综合运势"
        summary = (
            f"根据{zodiac_str}{direction.name_cn}方位（{direction.element}气）、{room.name_cn}功能及您的诉求（{wish_str}），"
            f"为您精选以上花种。摆放时注意："
            f"{recommendations[0].warnings[0] if recommendations and recommendations[0].warnings else '暂无特殊注意事项'}"
        )

        return RecommendationSet(
            direction=direction.name_cn,
            room=room.name_cn,
            element=target_element,
            zodiac=zodiac,
            wishes=wishes,
            recommendations=recommendations,
            summary=summary
        )


# ==================== 便捷函数 ====================

def quick_recommend(
    direction: str,
    room: str,
    zodiac: str = None,
    wishes: list = None,
    top_n: int = 3
) -> dict:
    """
    快速推荐接口

    Args:
        direction: 方位（东/南/西/北/东南/西南/东北/西北/中）
        room: 房间（客厅/卧室/书房/厨房/卫生间/阳台/玄关/餐厅）
        zodiac: 用户生肖（可选），如"鼠"
        wishes: 诉求列表（可选），如["招财", "桃花"]
        top_n: 推荐数量，默认3

    Returns:
        dict: 推荐结果字典
    """
    engine = FengShuiFlowerEngine()

    direction_map = {d.value[0]: d for d in Direction}
    if direction not in direction_map:
        raise ValueError(f"无效方位: {direction}，可选: {list(direction_map.keys())}")
    dir_enum = direction_map[direction]

    room_map = {r.value[0]: r for r in RoomType}
    if room not in room_map:
        raise ValueError(f"无效房间: {room}，可选: {list(room_map.keys())}")
    room_enum = room_map[room]

    # 验证生肖
    valid_zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    if zodiac and zodiac not in valid_zodiacs:
        raise ValueError(f"无效生肖: {zodiac}，可选: {valid_zodiacs}")

    result = engine.recommend(dir_enum, room_enum, zodiac, wishes, top_n)

    return {
        "direction": result.direction,
        "element": result.element,
        "zodiac": result.zodiac,
        "room": result.room,
        "wishes": result.wishes,
        "recommendations": [
            {
                "flower": r.flower,
                "color": r.color,
                "position": r.position,
                "reason": r.reason,
                "element_match": r.element_match,
                "feng_shui_benefit": r.feng_shui_benefit,
                "matched_wishes": r.matched_wishes,
                "warnings": r.warnings
            }
            for r in result.recommendations
        ],
        "summary": result.summary
    }


def print_recommendation(result: dict):
    """格式化打印推荐结果"""
    zodiac_str = f"属{result.get('zodiac', '')}，" if result.get('zodiac') else ""
    wishes_str = "、".join(result.get("wishes", [])) or "综合"
    print(f"\n{'='*60}")
    print(f"生肖: {zodiac_str}方位: {result['direction']}（{result['element']}气）")
    print(f"房间: {result['room']} | 诉求: {wishes_str}")
    print(f"{'='*60}")

    for i, rec in enumerate(result['recommendations'], 1):
        matched = f" [匹配: {','.join(rec['matched_wishes'])}]" if rec['matched_wishes'] else ""
        print(f"\n推荐 {i}: {rec['flower']}{matched}")
        print(f"   颜色: {rec['color']} | 位置: {rec['position']}")
        print(f"   功效: {rec['feng_shui_benefit']}")
        print(f"   原因: {rec['reason']}")
        if rec['warnings']:
            for w in rec['warnings']:
                print(f"   ⚠️ {w}")

    print(f"\n总结: {result['summary']}")
    print(f"{'='*60}\n")


# ==================== 示例 ====================

if __name__ == "__main__":
    print("\n【示例1】东向客厅 + 属虎 + 招财")
    result1 = quick_recommend("东", "客厅", zodiac="虎", wishes=["招财"])
    print_recommendation(result1)

    print("\n【示例2】南向卧室 + 属马 + 桃花")
    result2 = quick_recommend("南", "卧室", zodiac="马", wishes=["桃花"])
    print_recommendation(result2)

    print("\n【示例3】北向书房 + 属鼠 + 事业")
    result3 = quick_recommend("北", "书房", zodiac="鼠", wishes=["事业"])
    print_recommendation(result3)

    print("\n【示例4】西向阳台 + 属猴 + 招财+健康")
    result4 = quick_recommend("西", "阳台", zodiac="猴", wishes=["招财", "健康"])
    print_recommendation(result4)
