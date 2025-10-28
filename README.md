## Location Selection Analysis for Beverage Stores -A Case Study of Taipei 
Bubble tea and handshake beverages stores are a unique feature of Taiwanese culture. Although many new handshake beverages stores open every year, many also close down within just a few years. Beyond brand image and product offerings, we are curious — does the choice of store location also play a significant role in their success? What key factors do relatively successful chain beverage stores consider when selecting their locations?  
This project aims to analyze the location selection for handshake beverage stores in Taipei using open government data. The models employed include linear regression, logistic regression, decision tree, random forest, and gradient boosting decision tree.

### Analysis and Report
Analysis code and description: Please view the [website](https://hanshenghuang.github.io/LocationSelectionProject/report/LocationSelection_Analysis.html)

### System Implementation
This project not only provides a report but also implements a tool that helps beverage companies select optimal locations based on relevant information. By entering a Chinese address in Taipei, users can receive a predicted success probability for that location.  
The image below is the interface of the system. [Here](https://youtu.be/wQb_0LrNZpo) is the system demo video.  
![image](https://github.com/hanshenghuang/LocationSelectionProject/blob/main/report/interface.png)

### Try the system
This system is a Python application packaged as a standalone .exe file. To try it out, simply download the project and run the executable file LocationSelection_System.exe. After launching the application, you can input an address and receive the predicted outcome.  
Note: Since the system retrieves the latitude and longitude of the address using a web crawler, an internet connection and Chrome (version 141 or later) are required for proper functionality.