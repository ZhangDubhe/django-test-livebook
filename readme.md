# Project : Data Collection System for Livebook 🚀

> Created  2018/1/24, 452 Athabasca Hall,U of Alberta, Edmonton, Alberta 🇨🇦

## About this Readme.md
This file contains instruction of this project and development logs.
<!-- TOC -->

- [Project : Data Collection System for Livebook 🚀](#project--data-collection-system-for-livebook-🚀)
    - [About this Readme.md](#about-this-readmemd)
    - [Deployment](#deployment)
        - [1. Install python (3.6) and pip3](#1-install-python-36-and-pip3)
            - [Ubuntu](#ubuntu)
            - [MacOS](#macos)
        - [2. Install django](#2-install-django)
        - [3. clone the project](#3-clone-the-project)
        - [4. runserver](#4-runserver)
    - [Demo Instruction](#demo-instruction)
        - [RESEARCH PLANNING](#research-planning)
            - [RESEARCH STEPS](#research-steps)
            - [TIMELINE](#timeline)
        - [Webpage structure](#webpage-structure)
        - [Deploy on Cybera](#deploy-on-cybera)
            - [log in instance by shh key](#log-in-instance-by-shh-key)
            - [Create Security group](#create-security-group)
            - [Bind the float IP address](#bind-the-float-ip-address)
    - [Medical Knowledge Base](#medical-knowledge-base)
    - [Database Table Design](#database-table-design)
    - [UMLS Database](#umls-database)
        - [Using UMLS-API](#using-umls-api)
            - [1 Generate TGT ( valid 8 hours)](#1-generate-tgt--valid-8-hours)
            - [2 Generate ST  ( valid 5 mins but single use)](#2-generate-st---valid-5-mins-but-single-use)
            - [3 API call](#3-api-call)
    - [DevLog](#devlog)

<!-- /TOC -->
## Deployment
Following code are all in the terminal.
### 1. Install python (3.6) and pip3
#### Ubuntu
```
sudo apt-get update && sudo apt-get install python-pip3
```
#### MacOS
Download python3 from [this website](https://www.python.org/downloads/mac-osx/) and install it.
```
# download and install pip
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
```
### 2. Install django
```
pip3 install django
pip3 install requests  lxml  django-table2
```
### 3. clone the project 
Use git to get the latest release on master branch.
```git
git clone https://github.com/ZhangDubhe/django-test-livebook.git
```

### 4. runserver
```bash
cd django-test-livebook/collection
python3 manage.py runserver
```


## Demo Instruction
There are user interface  and admin interface which all powered by Django. Although user interface is more important, we also need the admin one to look through our data.

You must log in the user interface first as you enter this website and there is temporarily no introduction page of this system. 

Every table is established followed this document, so you can find each explanation here.

Project Aim:
To develop a special-purpose case-authoring environment, to enable the collection of cases from a broader audience. Collect Information to enlarge Database Of Disease and symptom.

### RESEARCH PLANNING
#### RESEARCH STEPS
    1. Prepare for the database, describe the structure and link between each tables.
    2. Design for the question that how to ask and how to present.
    3. Strategy to present the different step questions.
    4. Explain to sina and make  comments.
    5. Make interface and database as a demo, then talk to Doctors
    6. Design screen and UI 
    7. Build the web page
#### TIMELINE
    1 - 2 weeks: Database (including design and communicate with doctor and Sina)
    3 - 5 weeks: Collection Interactive Panel ( communicate with doctor)
    6th week: Log-in System and recording user
    7th week: Test
    8th week: Transfer Data & Presentation

### Webpage structure
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

Watching the video of operating of admin user.
Click the [video](https://drive.google.com/file/d/1HOHV6S964LC5v_y6paMQbNyBboI6oOaV/view?usp=sharing)
and know more.

### Deploy on Cybera
#### log in instance by shh key
Before instances can be created, users will require a key pair that will be injected into the instance to permit access; any instance launched from an image in the Rapid Access Cloud **must** use key pairs to access the virtual machine for the first time, as password sign-on is disabled by default, key pairs being much more secure than a default password, though it does introduce extra steps. However, once a key pair is created, it can be used for any future instances that are created; further additional key pairs can be generated for different instances if there is a need to restrict access to various systems among different users.

Key Pairs are how you login to your instance after it is launched.

Choose a key pair name you will recognise and paste your SSH public key into the space provided.

SSH key pairs can be generated with the ssh-keygen command:
```
ssh-keygen -t rsa -f cloud.key
```
This generates a pair of keys: a key you keep private (cloud.key) and a public key (cloud.key.pub). Paste the contents of the public key file here.

After launching an instance, you login using the private key (the username might be different depending on the image you launched):
```
sudo ssh -i cloud.key <username>@<instance_ip> 
#sudo is neccessary sometimes
```
Detail in [Document](https://wiki.cybera.ca/display/RAC/Part+1+-+Basic+Guide%3A+Using+the+Cybera+Rapid+Access+Cloud)

#### Create Security group
1. Log-in to the Rapid Access Cloud dashboard at https://cloud.cybera.ca.

2. In the left-hand panel under “Compute”, click “Access & Security”.

3. Click the “Security Groups” tab, click the “Manage Rules” button on the right hand side associated with the “default” security group. The list is initially empty, however we are going to add rules that:

    a.  permit ICMP for ping and traceroute, from any IPv4 or IPv6 address

    b.  permit ssh from any IPv4 or IPv6 address

4. Click “+Add Rule” in the top right. We are going to be adding four rules. For each rule input the values, then click the blue “Add” button. Note, the first and third rules are for IPv4 access, while the second and fourth are for IPv6:
#### Bind the float IP address
1. Log-in to the Rapid Access Cloud dashboard at https://cloud.cybera.ca.

2. In the left-hand panel under “Compute”, click “Instances”.

3. Click the Action drop-down button on the right-hand side and select “Associate Floating IP”.

4. Click on the “+” sign next to “Select an IP address”.

5. There is only one pool of addresses available (nova) and the quota shows only one IP address from that pool, so simply click “Allocate IP”.

6. After the IP address has been allocated, click the “Associate” button the the right hand side. Under the Instances summary, your Instance should now have three IP addresses, including a publicly accessible IPv4 address.


## Medical Knowledge Base
The objective is to crowdsource the data-collection around diseases and their symptoms underlying LiveBook.

## Database Table Design
1. **Disease Table** 
    To store information from UMLS diseases lists
2. **Symptoms Table** 
    Information from UMLS symptoms lists 
3. **Link Between Disease and symptoms Table**  
    Contain counts of approve or against of each relationship
4. **Properties of Symptom Table**  
    Symptom is isolate from different disease,  Each symptom will have lots of properties, Contains the relationship between symptoms and properties
5. **Values of each Property of different Symptom Table**  
    Each values record is different from different properties, Recording all kinds of value
6. **User Table** 
    Store name and psw of user.
7. **UserLog Table** Link between user and details about values
    Each type of question can be related to one style of recording, such as link between disease and symptom only records the id of disease_link( table show relationship between disease and symptom.), and link between symptom and property records the property id because in property table stored the relationships between properties and symptoms.
8. **Question table** 
    Store the priority of each question and sort by it when present the question to users. Change the value of the priority while every question is done and updated by user. 


## UMLS Database
1.Download UMLS database from where it release in official website. 
> Each UMLS release includes MetamorphoSys, required to install Knowledge Sources files, and to create, search and browse customized Metathesaurus subsets. MetamorphoSys requires a minimum of 30 GB of free hard disk and takes 2-10 hours to run on a range of platforms tested. The actual time will depend on your configuration, hardware and operating system platforms.
[UMLS release](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)

2.Install UMLS to Rich Text Format or Mysql whatever you like.
> TIPs: If you want to transfer the data to Mysql or Other software, it's necessary to have enough space for it.

3.Load UMLS into Mysql. I only want to use the word list of diseases and symptoms, so I try to find this two, but the structure look so confuse.

Here is the link of [Loading UMLS into MYSQL](http://groups.csail.mit.edu/medg/projects/text/Load_UMLS_mysql.html)


### Using UMLS-API     

3 steps to auth

#### 1 Generate TGT ( valid 8 hours)
    
    https://utslogin.nlm.nih.gov/cas/v1/api-key
    Body:
    apikey: <your apikey>
     
    Response:
    HTTP/1.1 201 Created
    Server: Apache-Coyote/1.1
    Cache-Control: no-store
    Location: https://utslogin.nlm.nih.gov/cas/v1/api-key/TGT-58510-CJztXeHbYL4U4LcURLx4KJoFFRgigPN7tLEkH7vse1imydsvdM-cas
    Content-Type: text/html;charset=UTF-8

#### 2 Generate ST  ( valid 5 mins but single use)

    https://utslogin.nlm.nih.gov/cas/v1/tickets/<TGT-....>
    Body:
    service:http://umlsks.nlm.nih.gov
    
    Response:
    ST-503827-rvULlxP4kEDPcq1ED2Ap-cas
    
    HTTP/1.1 200 OK
   
#### 3 API call                     
example
    
    Get:
    https://uts-ws.nlm.nih.gov
    /rest/content/current/CUI/C0018787
    ?ticket=ST-503827-rvULlxP4kEDPcq1ED2Ap-cas

if invalid:
       
      HTTP/1.1 403 Forbidden
       A new service ticket must be generated for each request to the API.
## DevLog
* 2018/2/7 1518059603.698126

    Hardly believe Eleni ask me to have a meeting with her today. While my webapp still in a begin    ning process.
    Django seems like very easy, but when you have many problem in fundation knowledge, it seems like very hard.
        back —— - query auth 
                - - is_exist(tgt) - response tgt and st
                - - is_not_exist or is_not_valid - post tgt + save
                - - ------------------------------ response tgt and st
        front—— - query 'search'
                - - - check cookie 
                - - - - isset - post st - get 'search'
                - - - - not - - query auth
        tgt in cookie has an expiration - 8 * 60 * 60 * 1000 (js - ms)

* 2018/2/16
    -   Create topic question.
    -   User can click the searching result and push.

* 2018/2/22
    -   Finish topic questions "Otitis".
    -   Complete database and fix many bugs.
    -   Simple interface with bootstrap as frontend framework.
    -   Simple layout and harmonize colors.
    
* 2018/2/23
    -   Complete Login sys.
    -   Fix searching terms bug.
    -   Finish introduction of paper in ECNU.[Google Docs.](https://docs.google.com/document/d/1RF6SQaXc4lnWIeAocbxibxaHCsN1jYfsc43BOIY7xz8/edit?usp=sharing)
    -   First Stay late at U of A.

* 2018/3/1
    -   Happy New Month.
    -   Met with Eleni today and I only finished the login sys of live-book case editor.
    -   Next meeting will be next Tuesday.
    -   Add new question about verification.
    -   New face of login page and register page.
    -   Admin interface of database.

* 2018/3/8
    -   After meeting with eleni, with many questions about the database to make the system did not run fluency. 
    -   Interface need change a lot. Less thinking makes work worse.
    -   user log to suggest people how many question they finish.
    -   clean up the multiple definition entries. It's so weird.
    -   Add data from UMLS-NCI database to get definition. (Including disease only with otitis, symptoms with semantic type is symptom, property with Organism Attribute and qualitative concept)

* 2018/3/13
    -   add Class of table of history


* 2018/3/23
    -   Upload to blog.dubheee.com

* 2018/3/28
    -   Fix update value and add more question type of same category by random_int
    -   fix verify method of property and value
    -   Need to think about the strategy of asking question.

* 2018/4/4
    -   New strategy to present the question by the priority.
    -   Add new table of Question model.
    -   Add interact method of Models.Question in view.py

* 2018/4/5
    -   Create Cybera Network cloud.
    -   Test successfully.

* 2018/4/6
    -   Need one have higer capacity.
    -   Cloud rebuild failed.

* 2018/4/12
    -   Create some function about topic and disease update.
    -   Connect using "sudo ssh -i livebook.key ubuntu@204.209.76.221" in MacOS, succeed finally.
    -   Transfer data of disease.
    -   Deploy on Cybera
