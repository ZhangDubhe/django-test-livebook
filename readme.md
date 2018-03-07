### Project : Data Collection System for Livebook 🚀

Created  2018/1/24, 452 Athabasca Hall,U of Alberta, Edmonton Alberta

#### About this Readme.md
This file contains instruction of this project and development logs.


#### Demo Instruction
There are user interface  and admin interface which all powered by Django. Although user interface is more important, we also need the admin one to look through our data.

You must log in the user interface first as you enter this website and there is temporarily no introduction page of this system. 

Every table is established followed this document, so you can find each explanation here.


- - -


#### Aim:
To develop a special-purpose case-authoring environment, to enable the collection of cases from a broader audience. Collect Information to enlarge Database Of Disease and symptom.


#### Webpage structure
User interface

    Login - if not admin, only home page and can start do collecting and valid.
            further more, if not admin, if student , then quiz page
            Not student, then poll page
            if admin - then show admin page link
            
    home - instruction of today's topic further more it's bettr to select the topic.
    
    quiz - Each question is randomly show from the back end  but all are in this topic.
            Here two types of question -- the collection one, the verification one.
            
            Collection can search new item and add it to system, also can select some already resisted, while another one only can select Yes or No.
            
            Here is a " Jump " button to make my developing work more quick and it also allow people who don't know this term to jump to next one because it will not send anything to backend.
    
Admin interface
    
    There are all important tables on this page and the admin can check whether the data is right when people uploading something.




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

##### 2918/2/16
-   Create topic question.
-   User can click the searching result and push.

##### 2018/2/22
-   Finish topic questions "Otitis".
-   Complete database and fix many bugs.
-   Simple interface with bootstrap as frontend framework.
-   Simple layout and harmonize colors.
    
##### 2018/2/23
-   Complete Login sys.
-   Fix searching terms bug.
-   Finish introduction of paper in ECNU.[Google Docs.](https://docs.google.com/document/d/1RF6SQaXc4lnWIeAocbxibxaHCsN1jYfsc43BOIY7xz8/edit?usp=sharing)
-   First Stay late at U of A.

##### 2018/3/1
-   Happy New Month.
-   Met with Eleni today and I only finished the login sys of live-book case editor.
-   Next meeting will be next Tuesday.
-   Add new question about verification.
-   New face of login page and register page.
-   Admin interface of database. 
