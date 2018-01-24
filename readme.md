### Project : Data Collection System for Livebook

Created  2018/1/24, 452 Athabasca Hall,U of Alberta, Edmonton Alberta

#### Aim:
To develop a special-purpose case-authoring environment, to enable the collection of cases from a broader audience. Collect Information To enlarge Database Of Disease and symptom

#### Main Step about the work:
	1. Prepare for the database, describe the structure and link between each tables.
	2. Design for the question that how to ask and how to present.
	3. Strategy to present the different step questions.
	4. Explain to Sina and make  comments.
	5. Make interface and database as a demo, then talk to Doctors
	6. Design screen and UI
    7. Build the web page



#### Prepare for Information Retrivel   -  First Week
	A. Sign for UMLS
	B. How to use UMLS
	C. How to use MetaMap


#### Medical Knowledge Base
	A. Database Table
		a. Disease Table
			To store information from UMLS diseases lists
		b. Symptons Table
			Information from UMLS symptons lists
		c. Link Between Disease and symptons Table
			Contain counts of approve or against of each relationship
		d. Properties of Sympton
			Symton is isolate from different disease,
			Each sympton will have lots of properties
			Contains the relationship between symptons and properties
		e. Values of each Property of different Sympton
			Each values record is different from different properties.
			Recording all kinds of value.

		Disease
		| Disease_ID    |   Disease_Name	|   Other attributes    |
		|   1	        |   Orihs           |   	                |
		|   2	        |                   |                       |

		Symptons
		Sympton_ID	Sympton_Name	Sympton_Other_attribute
		1	Fever
		2		..
		3		.

		Link between Disease and Sympton
		D_S_Link_Id	Disease_id	Sympton_id	Count_agree	Count_disagree	Is_Valid(boolean)
		1	1	1	5	1	true
		2	1	2	1	5	false
		3

		Properties of Symptons
		Property_id	Sympton_id	Property	Count_fillin
		1	1	Duration	4
		2	1	Temperature	10
		3	1	…	4

		Values of each Property
		Record_id	Disease_id	Sympton_id	Property_id	Value	Count_fill
		/				(Varchar)
		Value_record_id
		1	1	1	1	3	10
		2	1	1	2	38	2
		3	2	1	2	35	10
