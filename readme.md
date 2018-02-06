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
   
   
