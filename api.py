"""
风水花卉推荐引擎 - Flask API 服务 v3.0
"""

from flask import Flask, request, jsonify, render_template
import sys
sys.path.insert(0, '/Users/sger/WorkBuddy/20260411082948')
from fengshui_engine import FengShuiFlowerEngine, Direction, RoomType, ChineseZodiac, quick_recommend

app = Flask(__name__, template_folder='templates', static_folder='static')

engine = FengShuiFlowerEngine()


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    推荐接口 v3.0

    请求体:
    {
        "direction": "东",          // 必填: 东/南/西/北/东南/西南/东北/西北/中
        "room": "客厅",             // 必填: 客厅/卧室/书房/厨房/卫生间/阳台/玄关/餐厅
        "zodiac": "虎",             // 可选: 鼠/牛/虎/兔/龙/蛇/马/羊/猴/鸡/狗/猪
        "wishes": ["招财", "桃花"]  // 可选: 招财/桃花/事业/健康
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "请提供JSON数据"}), 400

        direction = data.get('direction')
        room = data.get('room')
        zodiac = data.get('zodiac')
        wishes = data.get('wishes', [])

        if not direction:
            return jsonify({"success": False, "error": "缺少direction参数"}), 400
        if not room:
            return jsonify({"success": False, "error": "缺少room参数"}), 400

        # 验证生肖
        valid_zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        if zodiac and zodiac not in valid_zodiacs:
            return jsonify({"success": False, "error": f"无效生肖，可选: {valid_zodiacs}"}), 400

        # 验证诉求
        valid_wishes = ["招财", "桃花", "事业", "健康"]
        if wishes:
            if isinstance(wishes, str):
                wishes = [wishes]
            wishes = [w for w in wishes if w in valid_wishes]

        result = quick_recommend(direction, room, zodiac, wishes, top_n=3)

        return jsonify({
            "success": True,
            "data": result
        })

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"服务器错误: {str(e)}"}), 500


@app.route('/api/directions', methods=['GET'])
def get_directions():
    """获取所有方位选项"""
    return jsonify({
        "success": True,
        "data": [
            {"value": d.value[0], "label": d.value[0], "element": d.element, "colors": d.colors}
            for d in Direction
        ]
    })


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """获取所有房间选项"""
    return jsonify({
        "success": True,
        "data": [
            {"value": r.value[0], "label": r.value[0], "purpose": r.value[1]}
            for r in RoomType
        ]
    })


@app.route('/api/zodiacs', methods=['GET'])
def get_zodiacs():
    """获取所有生肖选项"""
    zodiac_info = {
        "鼠": "水｜机敏",
        "牛": "土｜勤勉",
        "虎": "木｜勇猛",
        "兔": "木｜温和",
        "龙": "土｜尊贵",
        "蛇": "火｜智慧",
        "马": "火｜热情",
        "羊": "土｜和谐",
        "猴": "金｜聪慧",
        "鸡": "金｜勤恳",
        "狗": "土｜忠诚",
        "猪": "水｜诚实"
    }
    return jsonify({
        "success": True,
        "data": [
            {"value": z.value[0], "label": z.value[0], "element": z.value[1], "desc": zodiac_info.get(z.value[0], "")}
            for z in ChineseZodiac
        ]
    })


@app.route('/api/wishes', methods=['GET'])
def get_wishes():
    """获取所有诉求选项"""
    return jsonify({
        "success": True,
        "data": [
            {"value": "招财", "label": "招财", "desc": "财运亨通"},
            {"value": "桃花", "label": "桃花", "desc": "姻缘感情"},
            {"value": "事业", "label": "事业", "desc": "学业事业"},
            {"value": "健康", "label": "健康", "desc": "身心康健"}
        ]
    })


if __name__ == '__main__':
    print("=" * 50)
    print("风水花卉推荐系统 API v3.0")
    print("=" * 50)
    print("访问地址: http://localhost:5678")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5678, debug=True)
