## This is a project without the necessary csv's. You can make your own data to work with this project though or use it as d3.js and Angular inspiration. To see the final result, watch the final_video.mov.

### Customer Insights for 100 DAYS BOOST 

#### How to add new Clustering Method

##### Prerequisites 
1. Angular: https://angular.io/guide/quickstart
2. Jupyter Notebook: https://jupyter.readthedocs.io/en/latest/install.html
3. DataGrip: https://www.jetbrains.com/datagrip/
4. An Code IDE like WebStorm: https://www.jetbrains.com/webstorm/


##### Format Data with Python

To not overload the connection from database to website, you try to have only the necessary data in the database and seperate it in smaller tables for overview. For this you can use the Python scripts which are included in the Python Scripts Folder

There are a two specific cases you want to edit your data first: 
1. you have new data for a new clustering method
2. you have new data for the special equipment for a clustering. 

Usually you start with the raw table, which includes specs as, e.g. clustering method, the x and y coordinates and demographics. Please reduce this as much as possible, whithout loosing important data. Please use this data as the source of the following three tables. Also have no have no spaces, slashes or '-' symbols in the column names. Stay with letters and underscores. 

**Reduced Data:** First you reduce it to a table which only includes the columns of your coordinates and clustering methods, as you see in the "getting reduced data" script. This is the basis of our big main graph in the final web interface. 
If you just want to add a new clustering method, add the column to the already existing columns and import the data like in the "Import the Data" Step 3.

**Averages Data:** Then you want to get the averages of (in our case) the glvt-data per clustering method. The final table should only include the clustering method and the averages of the glvt-data. Here though only the three highest values per cluster as you can see in the 'clu_15_pur_SA_dummy_averages.csv'-file.
You can do this via the 'getting the averages data'-python script. Here you have to alter the input and the output csv-name and also glvt-data-column you want to include.

**Demographics Data:** Next table you need is the demographics table, you can get via the 'getting demographics data' python script. This script does push a new column to an empty table per demograhphic unique value and gives it the summed up value per cluster. 

**Special Equipment Data:** To connect our interface also with the special equipment data, we can use this new data information and should reduce it similarly as the averages data before. In the 'getting averages data' script you can find at the bottom a commented simplified script which can help you, to reduce it further. 



##### Import the data in the database on MartinBox via Datagraip


1. Add a Datasource witch following credentials:  
    Name:***
    Host: ***:*** 
    Database: ****
    user: **** 
    password: ***
    URL: *****


2. Create a PostrgreSQL table like this: 
    ```SQL
    create table clu_15_pur_SA_averages
    (
    clu_15_pur real,
    SA40C_M_Carbondach real
    );

    alter table clu_15_pur_SA_averages
    owner to "user";
    ```


3. Find your table in the file hirarchy on the left and right click it. Select _import from file_ and select your file. Here check if _Comma-Seperated_ is selected as same as _First row is header_. Check the Preview and click _OK_.


##### Edit the Flask Application 

1. Mailing Martin Rohrmeier to get access to the Martin Box


2. Connecting to the Martinbox via `ssh *** + anmelden` in the terminal enter there your Q-number and password.


3. To get into the docker container, enter `docker exec -t -i *** /bin/bash`.


4. Now you can edit the flask application with vim with `vim app.py`
    You can add a code here like this, but remember to change the `clu_15_pur_SA_averages` every time to your new table name: 
    ```Python
    @mlfgp_service.route('/api/clu_15_pur_SA_averages', methods=['GET'])
    def get_tais_clu_15_pur_SA_averages():
    """
    This module returns TAIS IPA data pertaining to single derivate and KO-group for the 3 target dates after request
    date.

    :return: A JSON Data that is a result the parsing of the full excels handed as IPA/TAIS extracts.
    """
    try:
        if request.method == 'GET':
            return pg.get_clu_15_pur_SA_averages().to_json(orient='records')
    except Exception as e:
        raise Exception(e)
    ```

    and `cd postgres` and `vim postgres.py` and add another method, similar to this:
    ```Python
    def get_clu_15_pur_SA_averages():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  clu_15_pur_SA_averages"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='clu_15_pur')
    ```

5. Finally you have to open a new terminal window, connect to the MartinBox like in Step 1 and restart the container with `docker container stop 6e382f1df2c9` and `docker container start 6e382f1df2c9`.



#### First steps with the angular project

This project is created with the angular framework and includes the d3.js and bootstrap. In this Documentation it is not explained how to use those three, but here are some helpful links:

**Angular:**  Documentation: https://angular.io/docs.

**D3.js:** Examples: https://bl.ocks.org/ , especially those of mbostock https://bl.ocks.org/mbostock. 

            Article on combining D3.js with Angular: https://medium.com/@balramchavan/integrating-d3js-with-angular-5-0-848ed45a8e19.
**Bootstrap:** Documentation https://getbootstrap.com/docs/4.0/getting-started/introduction/

**Start**
 $ git clone https://bdp.bmwgroup.net:8888/bitbucket/scm/~q474427/customersegmentationinsights.git


From here on you can use the angular cli in the terminal, e.g to run the project in a browser with `ng serve`. Please refer to Angular Documenation for more Info.

##### Structure of Angular Project

It is a very simple project structure. There are 6 components. The landing component which includes all the other 5 graph-components and one service. The *main-data.service* has all methods to connect to the flask application, so the database and to format the received data in a usable format. 

##### Make the Changes in the Angular Project

1. To receive the data in the angular project, you need to create a method for method you created in the flask app in the *main-data.service.ts* like following: 
```TypeScript
    load_clu_15_averages() {
    const requestURL = this.base_url + '/clu_15_averages'; // change respectively to the api you put in the flask method
    return this.http.get(requestURL).pipe(
      map((data: any[]) => {
        // change the 'clu_15_pur' to the clustering method name + 'averages' to either 'demographics' or 'SA_Averages', if the method receives these instead of the averages data.
        this.averages['clu_15_pur'] = data; 
      }), catchError( (error) => {
        return throwError('Error: ' + error);
      })
    );
  }
```

2. Next step is to add your function in the switch case method in one of those functions: `load_averagesOf`,`load_demographicsOf` or `load_SA_averages` and agan once above them. 

3. The last step is edit the *landing.component.ts* in two ways: 
    1. Add the new clustering method name to this array: `  clusteringMethods = ['clu_15_pur', 'kmean15'];`
    2. Add a `false` to the array `buttonActivity = [true, false];`


##### How to Generate a new Graph Component

1. You generate an empty component via the angular cli in the terminal with following command `ng g c` + *component name*.

2. 

**how to connect project to database**

**how to add clustering method**

# overview_of_customer_characteristics
# overview_of_customer_characteristics
# overview_of_customer_characteristics
