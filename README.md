## Location Selection Analysis for Beverage Stores -A Case Study of Taipei 
This project aims to analyze the location selection for hand-shake beverage stores in Taipei using open government data. The models employed include linear regression, logistic regression, decision tree, random forest, and gradient boosting decision tree.

### Analysis and Report
Analysis code and description: Please view the [website](https://hanshenghuang.github.io/LocationSelectionProject/LocationSelection_Analysis.html)

### System Implementation
This project not only provides a report but also implements a tool that helps beverage companies select optimal locations based on relevant information. By entering a Chinese address in Taipei, users can receive a predicted success probability for that location.
The image below is the interface of the system. [Here](https://youtu.be/O-T8adiqFRU) is the system demo video.   
  
![image](https://github.com/hanshenghuang/LocationSelectionProject/blob/main/interface.png)

### Download the system
The system is a python application and  was packaged into a single folder, which can be downloaded [here](https://drive.google.com/drive/folders/19RO0BDYo3bNgDFYa31kFZ3YahBSVRWbF). Users just need to download the whole folder and click the execution file "LocationSelection_System.exe". Then, users can input the address and get the predicted outcome.  
Because the system need to get the latitude and longitude of the address by web crawler, this system need to execute with internet and Chrome (version 99). 
