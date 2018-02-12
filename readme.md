### Project : Data Collection System for Livebook

Created  2018/1/24, 452 Athabasca Hall,U of Alberta, Edmonton Alberta

#### Aim:
To develop a special-purpose case-authoring environment, to enable the collection of cases from a broader audience. Collect Information to enlarge Database Of Disease and symptom.


#### Webpage structure
Page
    
    Welcome page : describe this project information
    Poll page
    Quiz page

Banner Nav

    Logo _ welcome page
    Poll
    Quiz
    Own
    Admin ( only admin user when log in)
    
User
    
    Login - if not admin, if student , then quiz page
            Not student, then poll page
    admin , then admin page, but also get in other page in 



* * *

#### RESEARCH PLANNING
##### RESEARCH STEPS
    1. Prepare for the database, describe the structure and link between each tables.
    2. Design for the question that how to ask and how to present.
    3. Strategy to present the different step questions.
    4. Explain to sina and make  comments.
    5. Make interface and database as a demo, then talk to Doctors
    6. Design screen and UI 
    7. Build the web page
##### TIMELINE
    1 - 2 weeks: Database (including design and communicate with doctor and Sina)
    3 - 5 weeks: Collection Interactive Panel ( communicate with doctor)
    6th week: Log-in System and recording user
    7th week: Test
    8th week: Transfer Data & Presentation

#### Medical Knowledge Base
The objective is to crowdsource the data-collection around diseases and their symptoms underlying LiveBook.


##### Database Table Design
    1. Disease Table To store information from UMLS diseases lists
    2. Symptoms Table Information from UMLS symptoms lists 
    3. Link Between Disease and symptoms Table  Contain counts of approve or against of each relationship
    4. Properties of Symptom Table  Symptom is isolate from different disease,  Each symptom will have lots of properties, Contains the relationship between symptoms and properties
    5. Values of each Property of different Symptom Table  Each values record is different from different properties, Recording all kinds of value



#### UMLS Database

1.Download UMLS database from where it release in official website. 
> Each UMLS release includes MetamorphoSys, required to install Knowledge Sources files, and to create, search and browse customized Metathesaurus subsets. MetamorphoSys requires a minimum of 30 GB of free hard disk and takes 2-10 hours to run on a range of platforms tested. The actual time will depend on your configuration, hardware and operating system platforms.
[UMLS release](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)

2.Install UMLS to Rich Text Format or Mysql whatever you like.
> TIPs: If you want to transfer the data to Mysql or Other software, it's necessary to have enough space for it.

3.Load UMLS into Mysql. I only want to use the word list of diseases and symptoms, so I try to find this two, but the structure look so confuse.

Here is the link of [Loading UMLS into MYSQL](http://groups.csail.mit.edu/medg/projects/text/Load_UMLS_mysql.html)


#### Using UMLS-API 

##### 1. Authenticating and calling
    
3 steps

1.Generate TGT ( valid 8 hours)
    
    https://utslogin.nlm.nih.gov/cas/v1/api-key
    Body:
    apikey: <your apikey>
     
    Response:
    HTTP/1.1 201 Created
    Server: Apache-Coyote/1.1
    Cache-Control: no-store
    Location: https://utslogin.nlm.nih.gov/cas/v1/api-key/TGT-58510-CJztXeHbYL4U4LcURLx4KJoFFRgigPN7tLEkH7vse1imydsvdM-cas
    Content-Type: text/html;charset=UTF-8

2.Generate ST  ( valid 5 mins but single use)

    https://utslogin.nlm.nih.gov/cas/v1/tickets/<TGT-....>
    Body:
    service:http://umlsks.nlm.nih.gov
    
    Response:
    ST-503827-rvULlxP4kEDPcq1ED2Ap-cas
    
    HTTP/1.1 200 OK
   
3.API call                     
example
    
    Get:
    https://uts-ws.nlm.nih.gov
    /rest/content/current/CUI/C0018787
    ?ticket=ST-503827-rvULlxP4kEDPcq1ED2Ap-cas

if invalid:
       
      HTTP/1.1 403 Forbidden
       A new service ticket must be generated for each request to the API.                      


## DevLog:
##### 2018/2/7 1518059603.698126
Hardly believe Eleni ask me to have a meeting with her today. While my webapp still in a begin    ning process.
Django seems like very easy, but when you have many problem in fundation knowledge, it seems like very hard.
完成UMLS的API对接，一开始的思路不清晰浪费了很多时间，认证接口看似很简单的我花了很长时间。
目前 认证接口包括后台长时间保存的tgt数据（create Ticket-grant ticket 并存储 ） + 前端API调用过程（cookie获取tgt + tgt获取service ticket， 由于st只是单次使用）
即：
    back —— - query auth 
            - - is_exist(tgt) - response tgt and st
            - - is_not_exist or is_not_valid - post tgt + save
            - - ------------------------------ response tgt and st
    front—— - query 'search'
            - - - check cookie 
            - - - - isset - post st - get 'search'
            - - - - not - - query auth
    tgt in cookie has an expiration - 8 * 60 * 60 * 1000 (js - ms)

##### 2018/2/12 1518458737.093284
距离上一次记录已经过了40万秒，40万这个数字也不过这么大，五天瞬息而过

今天得知UofA的申请季已过，突然不知道该怎么办，不敢去找教授谈自己想留下来，好像觉得想留下只是找不到去处，可怜可怜我把我收下一样，还是一样的逃避现实。
不知道这次的雅思会有低
肯定不会像托福一样是第二次的十分之一，如果是那我会很愉快进行明年的申请。
然后还可以从容的过完这一年。

人不该过这么安逸的生活。

但自己一味的流落就罢了，现在可不能这么想啊

但实力距离目标还那么远，真的是很艰难呢。

该怎么做能快一点
快一点

可以无压力的听懂老外说的话，
可以无压力解决工作上的问题
可以从容的应对毕业论文和研究课题还有外快实习的各方压力
还能给女朋友从容地规划未来的道路

仿佛和暑假的心态已经不一样了

首先应该解决是拖延症吧
然后 还有 听力，每天坚持和人对话，好好利用耳机，练习精听
定期浏览各个学校的网站
做阅读背单词
看文献写综述
我准备放弃出去玩了
好像自从上次考完雅思就松懈了
一下再也没有硬起来
怠惰的人生啊

是不是真的压力太大挺不起腰来


