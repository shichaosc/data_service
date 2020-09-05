# data_service
0. python3.7.5
1. python虚拟环境环境安装, 进入虚拟环境  
  
2. 安装项目所需要的包  
   pip install -r requirements.txt  
  
3. python manage.py migrate --setting=data_service.settings.prod进行数据库迁移
3. 利用gunicorn启动django项目  
    进入data_service文件夹下执行命令  
    gunicorn -c gunicorn.conf.py data_service.wsgi:application    

4. 安装supervisor，sudo yum install supervisor,利用supervisor管理gunicorn进程  
    supervisor添加配置文件 data_service.conf：  
    [program:data_service]  
    command=/虚拟环境/bin/gunicorn  -c gunicorn.conf.py data_service.wsgi:application   
    directory=/data/work/data_service  (代码地址)  
    #项目所在目录  
    autostart=true  
    autorestart=true   
    #崩掉自动重启  
    startsecs=3   
    #程序重启时候停留在runing状态的秒数  
    stdout_logfile=/data/logs/data_service/stdout.log  (日志路径)  
    stderr_logfile=/data/logs/data_service/stderr.log  
      
5. 启动supervisor:  
    supervisord -c /etc/supervisord.conf  
    进入supervisor界面：supervisorctl  
    启动项目：start data_service  
    重启项目：restart data_service  
    停止项目：stop data_service  