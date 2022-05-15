# Oto_dom_regression
  The project presented here is a practical example of using Machine Learning. It contains all the necessary elements from data acquisition, through data cleaning, analysis and processing, to training of various types of regression models. The aim is to create a model predicting prices on the Warsaw housing market, based on data coming from OtoDom.pl portal.

Chapters:

    I. Web Scraper

    II. Data cleaning and analysis
  
    III. Implementation of map usage with Geopy library

    IV. Machine Learning

        a) 
  
        b)
  
        c)

    V. MongoDB introduction

________________________________________________________________________________________________________________
    I. Web Scraper:
 
In my opinion nowadays data is a new kind of raw material - it is acquired, processed, stored and traded, and all this because it is a fuel for AI technology which is developing faster and faster. A regression or classification model is only as good as the data that trained it. The work on new models always starts with the acquisition of data, therefore the first step in the described project is to create a Web Scrapper, which will allow to take the existing housing offers from the OtoDom.pl classifieds portal. Then the data will be saved to a file in .csv format.
  
As mentioned, the model's area of operation was narrowed down to an area with a radius of 5 km from the Polish capital city - Warsaw.   
The result of the Scrapper program is shown below. You can see the raw data ready for processing.

![image](https://user-images.githubusercontent.com/83005003/164995134-a50d93d8-0c01-46f4-9cf5-f1dbdabfb34b.png)

__________________________________________________________________________________________________________________
     II. Data cleaning and analysis
  
The next step is to prepare the collected data so that they can be used to create models. In the following fragment of the data frame, you can see some of the work that needs to be done so that the final frame contains only numerical values. This is the most time consuming process, as well as the one with the greatest impact on the quality of future model predictions, so it should be done carefully.
 
![image](https://user-images.githubusercontent.com/83005003/168078902-c85b432c-9473-4c81-9f11-bd32c1da497c.png)

First, records that do not contain a price are removed because data without labels is not useful.
![image](https://user-images.githubusercontent.com/83005003/168093603-2665dc09-28b1-4725-8b76-8ed1b8380037.png)

Subsequent actions consisted of standardizing the content of records, converting them into numbers, or removing useless data. Data deviating in value from the rest were also removed if their number was a small percentage.

For some column cases it is most convenient to use "one hot encoding", the "get_dummies()" method from the Pandas library was used for this. It creates additional columns with values 0 and 1 being the description of the actual state in the original column. 

![image](https://user-images.githubusercontent.com/83005003/168099681-d28b41de-4d64-4173-bb5e-44f62f15e9ce.png)

Finally, check that no NaN values appear in the table and that all values are numeric and not, for example, of string type.

![image](https://user-images.githubusercontent.com/83005003/168100372-58125c48-e8e2-4674-85de-4c110beaa602.png)

![image](https://user-images.githubusercontent.com/83005003/168100501-50fe1757-1cd9-48e3-8647-bfcd1afba1f7.png)

The finished data frame is saved as a .csv file.

_____________________________________________________________________________________________________________________
    III. Implementation of map usage with Geopy library

With the apartment addresses included in the "Location" column, it became possible to use the Geopa library to visualize the placement of the apartments on the map.
Downloading longitude and latitude values takes quite a long time, so for the purpose of testing the correct operation of the code, the number of downloaded locations was limited to 200 positions.

The photo below shows the effect of the additive. On the map the locations of the apartments are marked by markers. After clicking on them additional information about the apartment appears, including the price. A proposal for development is to calculate the distance from the city center with the Manhattan Distance algorithm and create an additional feature to the model creation process.


![image](https://user-images.githubusercontent.com/83005003/168292058-d101789c-fdbd-4cc5-b866-ecc96c66456d.png)



__________________________________________________________________________________________________________________
      IV. Machine Learning


Before creating models, you need to perform effect enhancement operations on the collected data. These include detecting correlations between features or normalizing the data. These operations will be discussed in the current chapter.

    histogram stretching
    
Histogram before stretching:

![image](https://user-images.githubusercontent.com/83005003/168494307-23c3ca35-9ee6-4f43-84e5-0fee0d5c70d5.png)


In order to make the distribution of prices on the histogram more symmetric (histogram stretching), a function using the 3 sigma rule was created. Its body can be viewed below:

![image](https://user-images.githubusercontent.com/83005003/168494416-71624b6d-1d1c-4a76-b2c1-3cb6d4f4def9.png)

The effect of using the above function twice for the labels you have:

![image](https://user-images.githubusercontent.com/83005003/168494439-d2697266-f131-45be-8baf-d99b50698d4e.png)

