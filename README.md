# flask-api

## flask+uwsgi+nginx

## 服务器

 ####  安装centos7系统

1. 1.  系统选择CentOS系统（推荐选择CentOS7系统）
   2.  用户名：root
   3.  密码自己设定（记住！！！）

    4.  通过ssh工具登录服务器
        1. 这里推荐大家使用Putty进行登录。（可以自己百度下载一个，putty开源） 注意要开放ssh连接的端口，一般默认是22，（重装系统是默认开启的）为了网站安全推荐大家更换ssh登录端口。设置为不常用的端口。
2. putty登录服务器方法。只需要设置好IP地址，端口号，选择SSH。再点击open即可连接服务器（第一次连接会出来一个安全信息，后面就不会再有，点确定就好了）
3. 输入账号密码（账号就是root，密码是安装系统的时候）登录。（lunix下输入密码是没有光标提示操作的，直接输入完了直接回车）

   3. 安装宝塔面板。
      1. 执行以下代码进行安装宝塔6.9免费版。

```
yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh
```

​			复制对应的命令在putty中执行，然后再输入y即可。（等待安装完成）

4. 注意！安装成功的时候账号密码一定要保存下来。（可以复制写在记事本）
   制账号上面的：http：//xxx.xxx.xxx.xxx:8888/(这个就是你的IP地址：8888端口)
   在浏览器的网址输入，登录到宝塔面板的后台。

​	5.刷新浏览器页面即可。

​	6.在网站选项添加一个新站并加上自己的域名及端口号

#### python3安装

```                        cd .. 到   root
which python
mkdir /usr/local/python3 
cd /usr/local/python3                   
安装依赖
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

安装python3（3.6.2）
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz

蓝奏云下载:https://www.lanzous.com/i7x8kxg 密码:3bhk（下载好后传入刚创建的python3文件夹）

tar -xvJf  Python-3.6.2.tar.xz
cd Python-3.6.2
./configure --prefix=/usr/local/python3
make && make install

创建软链接
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

#### 搭建web环境

* 创建虚拟环境
* 安装flask
* 安装和配置uwsgi
* 配置nginx

```
pip3 install --upgrade virtualenv
mkdir test
cd test             (这个test在是/usr/local/python3/Python-3.6.2的/www/wwwroot/里)
virtualenv -p python3 .env

进入虚拟环境安装flask
source .env/bin/activate
（（（pip3 install flask     pip3 install datetime   pip3 install flask_redis）））
deactivate  
```

* 在test文件夹把代码放入test.py（例如下面的测试代码）

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787, debug=True)
```

* 安装和配置uwsgi

1. 安装uwsgi

```
pip3 install uwsgi
find / -name uwsgi
ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
```

2. 创建uwsgi.ini配置文件 

```
[uwsgi]
chdir=/www/wwwroot/test # 工程目录
home=/www/wwwroot/test/.env # 虚拟环境目录
module=test  # 启动flask应用的文件名，不用加.py
callable=app # 应用名
master=true
processes=2 # worker的进程个数
chmod-socket=666
logfile-chmod=644
procname-prefix-spaced=test # uwsgi的进程名称前缀，启动后可通过ps -ef | grep test查找到这个进程
py-autoreload=1 #py文件修改，自动加载，也就是设置热启动了
#http=0.0.0.0:8080 #监听端口，测试时使用

vacuum=true # 退出uwsgi是否清理中间文件，包含pid、sock和status文件
socket=%(chdir)/uwsgi/uwsgi.sock # socket文件，配置nginx时候使用
stats=%(chdir)/uwsgi/uwsgi.status # status文件，可以查看uwsgi的运行状态
pidfile=%(chdir)/uwsgi/uwsgi.pid # pid文件，通过该文件可以控制uwsgi的重启和停止
daemonize=%(chdir)/uwsgi/uwsgi.log # 设置后台模式，然后将日志输出到uwsgi.log。当调试时，可先注释掉此内容
***************************************************************************

**********************************************************************************
[uwsgi]
chdir=/www/wwwroot/test
home=/www/wwwroot/test/.env
module=test
callable=app
master=true
processes=2
chmod-socket=666
logfile-chmod=644
procname-prefix-spaced=test
py-autoreload=1
#http=0.0.0.0:8080

vacuum=true
socket=%(chdir)/uwsgi/uwsgi.sock
stats=%(chdir)/uwsgi/uwsgi.status
pidfile=%(chdir)/uwsgi/uwsgi.pid
daemonize=%(chdir)/uwsgi/uwsgi.log

```

```
mkdir uwsgi
cd uwsgi
vi uwsgi.pid
vi uwsgi.sock
vi uwsgi.status
vi uwsgi.log
​```     
然后应该cd ..回到test文件夹
* 常用命令：
```

```
uwsgi --ini uwsgi.ini             # 启动（在test文件夹下启动）
uwsgi --reload uwsgi.pid          # 重启（在uwsgi文件夹下启动）
uwsgi --stop uwsgi.pid            # 关闭（在uwsgi文件夹下启动）
```


* 配置nginx(加入宝塔对应域名的配置文件中并注释 include enable-php-56.conf;)

```
location / {
        include uwsgi_params;
        uwsgi_pass unix:/www/wwwroot/test/uwsgi/uwsgi.sock;
}
```

```
[1]:./img/系统.png
[2]:./img/IP地址.png
[3]:./img/putty.png 
[4]:./img/SSH登录.png 
[5]:./img/SSH连接.png 
[6]:./img/SSH登录成功.png 
[7]:./img/安装宝塔.png 
[8]:./img/宝塔安装成功.png 
[9]:./img/登录宝塔界面.png 
[10]:./img/删除安全入口.png 
[11]:./img/宝塔登录页面.png 
```
