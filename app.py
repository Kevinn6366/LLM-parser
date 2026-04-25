from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
app = Flask(__name__)
# 允许前端跨域访问
CORS(app)

# Dify密钥,请在根目录的.env文件进行配置

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_URL =os.getenv("DIFY_URL")

@app.route('/api/compile', methods=['POST'])
def compile_cultural_resource():
    data = request.json
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "请输入活动构想"}), 400

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "Lixin-Flask-Backend"
    }
    # 确保这里的test和你 Dify里的变量名一致
    payload = {
        "inputs": {"test": user_query},
        "response_mode": "blocking",
        "user": "lixin_univ_user"
    }
    try:
        response = requests.post(DIFY_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            res_data = response.json()
            content = res_data['data']['outputs'].get('text', '未生成内容')
            return jsonify({"status": "success", "data": content})
        else:
            return jsonify({"status": "error", "message": f"Dify接口异常: {response.status_code}"}), 500       
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # 运行在 5000 端口
    app.run(host='0.0.0.0', port=5000, debug=True)