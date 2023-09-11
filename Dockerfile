# 设置基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将当前目录下的文件复制到工作目录中
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir flask requests

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["python", "main.py"]
