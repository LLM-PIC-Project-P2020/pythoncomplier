from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 获取用户输入的代码
        code = request.form.get("code")

        try:
            # 使用 subprocess 执行代码并捕获输出
            result = subprocess.run(
                ["python", "-c", code],  # 执行代码
                text=True,               # 以文本形式返回输出
                capture_output=True,    # 捕获标准输出和错误
                timeout=5,               # 设置超时时间（秒）
            )

            # 返回执行结果
            if result.returncode == 0:  # 执行成功
                output = result.stdout
            else:  # 执行失败
                output = result.stderr

        except subprocess.TimeoutExpired:  # 超时处理
            output = "Error: Code execution timed out."
        except Exception as e:  # 其他异常
            output = f"Error: {str(e)}"

        return jsonify({"output": output})  # 返回 JSON 格式的结果

    return render_template("index.html")  # 渲染输入页面

if __name__ == "__main__":
    app.run(debug=True)  # 启动 Flask 应用