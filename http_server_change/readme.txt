环境：
	python 3.6+

功能：	
	1. 多用户凭个人账户登录（hash存储）
	2. 文件下载
	3. 文件上传
	4. 图片预览
	5. 文件共享

技术路线：
	基于socketserver框架


操作：
	1. 试验账户信息为：
		B17040819 密码：123456
		B17040818 密码：znw
	
	2. 如需其他账号请手动在disk目录下新建文件夹，并创建admin.txt
	    文件，存储账户和密码（密码为hashlib生成的）
	3. python xfile.py即可运行 