from flask import Flask, request, Response
import requests
import os
import gzip

app = Flask(__name__)

OPENAI_API_HOST = "api.openai.com"


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if path == "":
        env_file_path = os.path.join(os.getcwd(), '.env')
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
        return Response(content, mimetype='text/plain')
    else:
        url = f"https://{OPENAI_API_HOST}/{path}"
        headers = {key: value for (
            key, value) in request.headers.items() if key != 'Host'}

        data = request.get_data()
        response = requests.request(
            request.method, url, headers=headers, data=data, allow_redirects=False
        )

        # 检查响应是否使用了 gzip 压缩编码
        if response.headers.get("Content-Encoding") == "gzip":
            # 解压缩 gzip 数据
            compressed_data = response.content
            uncompressed_data = gzip.decompress(compressed_data)
        else:
            # 如果未使用 gzip 压缩，则使用原始数据
            uncompressed_data = response.content

        # 将 OpenAI API 的响应转发给客户端
        return Response(uncompressed_data, response.status_code, headers=response.headers.items())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
