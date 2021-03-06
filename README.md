# Oto_dom_regression
  The project presented here is a practical example of using Machine Learning. It contains all the necessary elements from data acquisition, through data cleaning, analysis and processing, to training of various types of regression models. The aim is to create a model predicting prices on the Warsaw housing market, based on data coming from OtoDom.pl portal.

Chapters:

    I. Web Scraper

    II. Data cleaning and analysis
  
    III. Implementation of map usage with Geopy library

    IV. Machine Learning

        Histogram stretching (3 sigma rule)
        
        Box Plot Analysis
        
        Correleation, removing of correlated features
        
        Normalization

        1) Multiple Regression (Regresja wieloraka)
  
        2) Decision Tree Regressor
  
        3) SVR
        
        4) Random forest

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

With the apartment addresses included in the "Location" column, it became possible to use the Geopy library to visualize the placement of the apartments on the map.
Downloading longitude and latitude values takes quite a long time, so for the purpose of testing the correct operation of the code, the number of downloaded locations was limited to 200 positions.

The photo below shows the effect of the additive. On the map the locations of the apartments are marked by markers. After clicking on them additional information about the apartment appears, including the price. A proposal for development is to calculate the distance from the city center with the Manhattan Distance algorithm and create an additional feature to the model creation process.


![image](https://user-images.githubusercontent.com/83005003/168292058-d101789c-fdbd-4cc5-b866-ecc96c66456d.png)



__________________________________________________________________________________________________________________
      IV. Machine Learning


Before creating models, you need to perform effect enhancement operations on the collected data. These include detecting correlations between features or normalizing the data. These operations will be discussed in the current chapter.

    Histogram stretching
    
Histogram before stretching:

![image](https://user-images.githubusercontent.com/83005003/168494307-23c3ca35-9ee6-4f43-84e5-0fee0d5c70d5.png)


In order to make the distribution of prices on the histogram more symmetric (histogram stretching), a function using the 3 sigma rule was created. Its body can be viewed below:

![image](https://user-images.githubusercontent.com/83005003/168494416-71624b6d-1d1c-4a76-b2c1-3cb6d4f4def9.png)

The effect of using the above function twice for the labels you have:

![image](https://user-images.githubusercontent.com/83005003/168494439-d2697266-f131-45be-8baf-d99b50698d4e.png)


      Box Plot Analysis
      
It is a good idea to make sure that the data you have does not contain outliers that may interfere with the finished model. Box Plot is used for this purpose. As you can see in the image below no data is outside the whiskers of the box plot, this means no outliers.

![image](https://user-images.githubusercontent.com/83005003/168494587-4e7ca685-81ac-40d8-8816-f1cf5f244ac9.png)


      Correleation, removing of correlated features
      

Another improvement in model performance is the detection and removal of correlated features. A good method to visualize the correlation between features is to generate a heatmap plot. The absolute value between -1 (black color on the heatmap) and 1 (white color on the heatmap) tells you how correlated each feature is, values close to the absolute 1 are highly correlated, while correlation values close to 0 are not correlated.

![image](https://user-images.githubusercontent.com/83005003/168494722-c9cd4d8c-a29f-463b-b281-cb2f75e69d9d.png)

Magnified fragment:

![image](https://user-images.githubusercontent.com/83005003/168494780-633b17d7-8fc4-435b-9522-1e364312a253.png)


An upper trigonal matrix was created to detect correlated features. Iterating through the columns of such a matrix we checked if they contain values above an assumed threshold (thresh=0.55), if so, the feature corresponding to the analyzed column is correlated and was removed.

fragment of the upper trigonal correlation matrix:

![image](https://user-images.githubusercontent.com/83005003/168495260-307448a2-aabb-4814-8448-898ee39951ae.png)


correlated features:

![image](https://user-images.githubusercontent.com/83005003/168495295-06dd16ee-43bf-45d3-8bd5-7039c460774f.png)

simple calculation of correlations:

![image](https://user-images.githubusercontent.com/83005003/168495319-c81a0bea-f10e-473e-9987-d893dfd77422.png)


      Normalization
 
 ![image](https://user-images.githubusercontent.com/83005003/168495415-e38e19e3-0c06-443a-81c5-18b1aed26580.png)




      Results:


      1) Multiple Regression (Regresja wieloraka)
      
![image](https://user-images.githubusercontent.com/83005003/168580374-4ebde5d4-5c42-4c71-aa92-2a16e333f69d.png)
![image](https://user-images.githubusercontent.com/83005003/168581454-61a9a0ed-faee-45b4-be0a-ea5f65cc52bf.png)


      2) Decision Tree Regressor
      
![image](https://user-images.githubusercontent.com/83005003/168580550-8d0b48c4-5276-49bf-8581-cbd7f8e60f5d.png)
![image](https://user-images.githubusercontent.com/83005003/168581540-8c64db1b-0410-4f66-a33c-a9c4717267c7.png)

    
      3) SVR
      
![image](https://user-images.githubusercontent.com/83005003/168580654-d534892d-97ba-42e1-b087-3e438a203e5b.png)
![image](https://user-images.githubusercontent.com/83005003/168581592-20ef7811-6ac1-4083-8f1d-631c929dde84.png)


      4) Random forest
      
![image](https://user-images.githubusercontent.com/83005003/168580774-60d8f880-1425-45ab-82e4-40e437b45e18.png)
![image](https://user-images.githubusercontent.com/83005003/168581646-8c4fc8e7-969f-42eb-b483-c625f7009e7c.png)
