from flask import Flask,render_template,request
import subprocess

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("law_subject.html")

@app.route('/script',methods=['POST','GET'])
def script():
    if request.method == 'GET':
        return render_template("law_script.html")
    else:
        result = request.form
        # print(result)

        fact_value = result.get('fact')

        if fact_value:
            # 打开test.py文件以读取内容
            with open('test.py', 'r', encoding='utf-8') as test_file:
                test_lines = test_file.readlines()

            # 找到第24行
            line_number_to_replace = 23  # 行数从0开始计数

            # 获取第24行的内容
            line_to_replace = test_lines[line_number_to_replace]

            # 找到双引号位置
            start_quote = line_to_replace.find('"')
            end_quote = line_to_replace.find('"', start_quote + 1)

            if start_quote != -1 and end_quote != -1:
                # 替换双引号内的内容为data.txt的内容
                updated_line = (
                        line_to_replace[:start_quote + 1]
                        + fact_value
                        + line_to_replace[end_quote:]
                )

                # 更新第24行的内容
                test_lines[line_number_to_replace] = updated_line

                # 重新打开test.py文件以写入更改
                with open('test.py', 'w', encoding='utf-8') as test_file:
                    test_file.writelines(test_lines)
            subprocess.run(["python", "test.py"])

        return render_template("law_script.html")

@app.route('/login')
def login():
    return render_template("law_login.html")


@app.route('/calculator')
def calculator():
    return render_template("law_calculator.html")

@app.route('/calculator/work')
def work_calculator():
    return render_template("work_calculator.html")

@app.route('/calculator/borrow')
def borrow_calculator():
    return render_template("borrow_calculator.html")

@app.route('/calculator/traffic')
def traffic_calculator():
    return render_template("traffic_calculator.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
