# nursery24 Web Application

#### Developed a web application which will provide the freedom to users to buy all nursery related products anytime from anywhere.

![Image description](https://github.com/rkasale28/nursery24/blob/master/nursery24/static/images/banner1.png)

> The consumers can shop with ease at their own comfort.

> This app will prove beneficial to providers as well as courier services. Not only, the providers could reach to their customer easily, but can view the summary of all products sold within certain time period. This summary is supported by visualization in terms of bar graphs and line graphs. These graphs represent the daily analysis of sales of a product as well as overall analyis. 

> Similarly, the courier services could monitor their delivery personnels, sitting at one place. Also, they can visualize the performance of their delivery personnels.

<br />

**Significance:**
* There are four types of users:
  - Consumer
  - Provider
  - Courier Service
  - Delivery Personnel
* Consumers 
  - Can order nursery related items from the site and track the order. 
  - Receive invoice as mail. 
  - Can cancel the order. 
  - Can rate a particular product.
* Providers
  - Can view 
    - Placed items
    - Ready to Ship items
    - Not returned items
    - Cancelled items.
  - Can track the delivery personnel
    - Before Shipping the product
    - If the product gets cancelled, after the product has been shipped.
  - Can add items as well as branches. 
  - Can view the overall summary of products.
  - Can visualize this summary with the help of graphs.
* Courier Services
  - Can add delivery personnel
  - Can view records of the delivery personnels.
  - Can visualize this summary based on 
  - Based on this analysis, they can provide salaries.
* Delivery Personnels
  - Can update their location
  - Can view consumers' as well as providers' location on map with routing controls.

<br />

**Important Features:**
* This web application is being designed using Django Framework
* This web application uses Postgres and postgis for database.
* Datatables API is used for display of summary.
* This summary is visualized with the help of Charts API.
* Leaflet API is used for display of maps.
* Leaflet-Routing-Machine API is used for display of routes on maps.
* For generating invoice as PDF, wEasyPrint API is used.
* For executing payments, Stripe API is used.
