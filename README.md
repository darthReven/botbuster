#About BotBuster
BotBuster presents a comprehensive and highly adaptive tool framework designed to discern artificial, unethical, and otherwise fake content via a range of detection engines. An all-encompassing tool, it actively handles diverse input formats and summarises analysis results with graph visualisations and annotated text. To enhance its accuracy, BotBuster seamlessly integrates multiple user-selectable APIs and category labels, ensuring continuous improvement and effectiveness in combating deceptive information.

##Project Objectives
During the course of the project, the team decided to specify three categories of text analysis to implement. The category labels of AI-Generated Content, Misinformation, and Hate Speech were chosen; however, BotBuster functionalities can be expanded beyond the default categories by integrating new APIs and category labels accordingly to address a wider range of other content-related challenges. In terms of architecture compatibility, the team will focus on hosting the solution and basing tests on Windows servers and devices to ensure optimal performance. Botbuster was developed to meet the following objectives:
- Analyse bulk blocks of data from various sources (e.g. forums, websites and reports)
* Provide an analysis overview from various detection engines and suggest parts of the text that are potentially AI-generated
+ Integrate new detection engines into the framework seamlessly

#Solution Specifications
The framework is built to have both a user interface and an API for users to call. The API is built on the Windows operating system and may not be fully compatible with Linux or any other operating system.
The team strived to make the solution as robust as possible. However, due to the limited amount of time, the framework will be more functional and efficient in more favourable conditions. The optimal conditions to run BotBuster are listed in the subsections below. The subsections will also include the data stored and the resources needed when using the system.

##Physical Environment and Requirements
Since BotBuster makes multiple requests to various different APIs and it could potentially get millions of words to process, it is vital for the server hosting the BotBuster framework to have a high-speed internet connection. Moreover, in order to handle many requests and data at the same time, the server would also require sufficient RAM and CPU resources. Taking these requirements into account, the team recommends that the server hosting the BotBuster framework should meet the following minimum requirements:
-A high-speed gigabit internet connection
*8 GB RAM
+A quadcore CPU

BotBuster’s In-house Misinformation model requires a lot of CPU utilisation, memory as well as an Nvidia GPU to speed up the training process. However, the model only has to be trained once, after which the model weights can be saved. The model can simply be loaded subsequently, eliminating the need to train the model upon restarts. As a result, the model can be trained on a server with higher specifications, after which the model can simply be loaded and hosted on another less powerful server. Taking these requirements into consideration, the team recommends that the server hosting the misinformation model should have the same specifications as the server hosting the BotBuster framework while the server training the misinformation model should meet the following minimum requirements:
-8 GB RAM
*A quadcore CPU
+A Nvidia GPU
The room in which the servers should be stored should follow the requirements of the hardware bought (i.e. the room temperature should not be high, etc.). The room should also be secure from unauthorised personnel. However, since the system does not currently store personally identifiable information or critical information, the resources invested in the security of the room in which the servers are running do not need to be extremely high. 

##Functionality Requirement
Botbuster was designed, built, and tested in a Windows 10/11 environment. Therefore, the team recommends hosting the servers on a Windows Server 2016. The system is coded using Python on the Backend and Misinformation servers, and HTML, CSS, and Javascript on the front end. As such, it may be capable of running on Linux or other operating systems with little to no modifications to the code/installed software. However, this was not a priority and therefore not tested by the team.
A full list of Python modules that were used to develop BotBuster and their used functionalities may be found in the dependencies section. These Python modules will need to be installed prior to running the servers. The team has provided a requirements.txt file to list all non-pre-installed modules. The modules may be installed using the pip install -r requirements.txt command on the command line. 

#Possible Future Expansions
As a framework dedicated to scrutinising and identifying fake content, the growth and further expansion of BotBuster is a huge step forward in our continuous battle against the rising tide of digital deception. The platform has developed from a simple tool to a comprehensive one, responsible for preserving the integrity of online conversation.
The progress BotBuster has achieved is defined by its unwavering commitment to innovation and adaptability to the changing digital landscape. The platform now supports a wide range of detection categories from AI-generated content, misinformation, and hate speech over various inputs like text, document, and image uploads as well as web scraping. This all-encompassing approach acknowledges the multifaceted nature of the issue being addressed.
While BotBuster has made tremendous advances in detecting fake content, it is critical to remember that the framework still has a lot of room for improvement. As the digital landscape evolves, so do the methods used by malevolent actors to propagate bogus content. BotBuster must continue to spend in research and development to handle new difficulties as they arise to stay ahead in this continuing struggle.

##Unlimited Word Count 
Despite the tremendous development and growth of the BotBuster framework from scratch, it is not without limitations. With the detection engines being accessed through external API calls separate from the overall framework, the constraints of the external detection engines may impede the functionality of the framework. One such constraint would be the limited word count imposed on the API, which poses a significant issue for users who rely on free or trial versions of the detection engines. For instance, Writer has a limit of 2000 words per request or Sapling AI which has a daily word limit of 1500. Other detection engines have their own varying restrictions which will snowball and cause implications to the framework.
A viable solution to the various constraints would be to simply purchase the premium services offered by the respective detection engines. In doing so, the previous constraints like word limits would be removed. Do bear in mind that various detection engines would offer different functionality based on the amount paid. Another solution would be to find and add additional detection engines without these constraints, although external ones might be difficult to find.

##Multi-User System
In spite of its capabilities in changing and storing configuration details, the BotBuster framework faces a prominent limitation in its design, being that it runs as a single-user system. Relying on a shared configuration file provides a straightforward approach to storing and changing settings as needed, being sufficient if a singular user were to utilise the framework. 

However, if multiple users or a team of users were required to utilise the framework, changes made to the configuration file would be shared across all users. While this has the advantage of easily sharing configurations with other users, it lacks the individualisation of configurations for each user and might cause potential issues with the configuration file being overwritten. This might cause the framework to behave in an unexpected or unfamiliar way for the user based on the previous user's settings.
To overcome this constraint, the BotBuster system would highly benefit from having a multi-user system. The system would employ the use of databases, potentially MySQL, to store individual data. A database-centric approach would allow for further expansion, allowing users to register and log in to store personalised settings and data. Additionally, logs of previously analysed data could be stored as a history for users to backtrack to. Creating accounts on the system would allow for different roles to be assigned based on the requirements of the team.

##Misinformation Model Training
Although the BotBuster framework is aimed at combating fake content and has made substantial progress in combating it, one significant limitation is the in-house misinformation model that may not be as dependable as desired. As a paramount component in the framework's analysis, serving as a default detection engine and the only detection engine under the misinformation category, it plays an important role in detecting misinformation in content. With the reliability of the model being highly dependent on factors such as the quality of training data, training method and effectiveness of algorithms, the team had limited time to train and fine-tune the model to produce highly reliable results.
To address this, BotBuster's in-house misinformation model would require more time invested into it to fine-tune the model optimally to detect misinformation. With the usage of ALBERT, the team could experiment and implement more optimal pre-trained models such as XLNET or GPT-3 , more comprehensive and up-to-date datasets would also aid in the model's fine-tuning process.

##Repetition Model
With the goal of accurately identifying and flagging fake content including bot accounts, one common indicator would be repetitive content. As such, the BotBuster framework has the constraint of lacking a repetition detection engine. Although repetition in online posts and comments could come in the form of exact copies of the same text, many bot accounts post repetitive content with variations which is a common technique to optimise the effectiveness of the message they are spreading.
As such, to handle this constraint, the team would have to employ a repetition model which works on word clustering. Word clustering is a technique that will group similar texts based on their content, which depending on the clustering method, either hard or soft, will have different clusters that may overlap. This method can help identify the variation in content posted by a specific account, low variation and high repetition would indicate a high probability of it being a bot account. Training and implementing such a model, would work well in conjunction with the other categories in identifying bot or fake accounts and the purpose of them, such as spreading misinformation, hate speech, or utilising AI-generated content.

#User Guide and Documentation

#Installation Guide

#Dependencies
urllib
json
base64
os
time
requests
re
html
asyncio
platform
random
sys
pyPDF2
PIL
textract
pytesseract
cv2
numpy
pydantic
docx
plotly
nltk
pandas
pyppeteer
Fastapi
bs4
transformers
torch
sklearn
