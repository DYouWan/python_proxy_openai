# 基于Python实现的OpenAi反代 LangChain

###  1.使用 Railway 部署
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app?referralCode=3IMB0X)

1、将本项目Fork到自己的github仓库中

2、访问Railway后使用github登录，然后选择新建项目，再选择从 GitHub 存储库部署
![image](https://github.com/DYouWan/python_proxy_openai/assets/18019108/7b1c37b1-7d43-471d-8697-9fa931feb326)

3、从项目列表中选择本项目
![image](https://github.com/DYouWan/python_proxy_openai/assets/18019108/ae8bef14-f43e-42d9-8535-ad747c07dda2)

4、配置环境变量，PORT默认为5000，不要修改此端口
![image](https://github.com/DYouWan/python_proxy_openai/assets/18019108/b018b9c0-3d8a-4352-829b-bae6a2056405)

5、选择Settings->Networking->Generate Domain,点击后会生成一个域名，支持自定义



# 2.代码示例
from langchain.llms import OpenAI

llm = OpenAI(

  openai_api_base="https://xxxxx.railway.app/v1",  #生成的域名是不带v1的，实际请求时后面要带v1
  
  openai_api_key="填入自己的Key"
  
)

result = llm("给我讲个笑话")

print(result)
