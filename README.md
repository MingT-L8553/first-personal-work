# first-personal-work
### 从git开始
- git config --global user.name 'MingT-L8553'
- git config --global user.email '1071252445@qq.com'
- git clone 远程仓库地址：克隆远程仓库到本地
- git branch：查看当前所有分支，前面有*号表示当前所在分支
- git branch crawl：创建crawl分支(该分支进行数据采集和处理代码的编写)
- git branch chart：创建chart分支(该分支进行数据的展示)
- git checkout crawl：切换当前分支到crawl分支
- git checkout -b chart：创建chart分支并切换至chart分支
- git push origin crawl：将crawl分支推送到远程仓库
- git merge crawl：将crawl分支合并到主分支上
- git branch -d chart：删除chart分支
- git status：查看当前版本库状态
- git add README.md：将修改后的README.md文件添加到暂存区
- git commit -m 'branch commit test'：将修改提交给版本库
- crawl分支添加的