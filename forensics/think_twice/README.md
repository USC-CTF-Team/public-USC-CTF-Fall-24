# think_twice

Challenge author: nguyen-huong

Category: forensics

Writeup author: neonlian

## Solution

You are given an image file that has the flag encoded in the metadata. 

Use an exif tool to view the metadata:
```
> exif metadata.png
--------------------+----------------------------------------------------------
Tag                 |Value
--------------------+----------------------------------------------------------
Orientation         |Top-left
X-Resolution        |144
Y-Resolution        |144
Resolution Unit     |Inch
Software            |UTNsaU1ISm5lMDFqUTJGeWRHaDVmU0E9
User Comment        |Screenshot
Pixel X Dimension   |1014
Pixel Y Dimension   |1162
Exif Version        |Exif Version 2.1
FlashPixVersion     |FlashPix Version 1.0
Color Space         |Uncalibrated
--------------------+----------------------------------------------------------
```

The "Software" tag has a base-64 encoded string in it. Use a tool like CyberChef to decode the string to get:
```
Q3liMHJne01jQ2FydGh5fSA=
```

This is another base-64 encoded string. Do one more base-64 decoding to get:
```
Cyb0rg{McCarthy} 
```

## Fun fact

This picture is taken from [when a car crashed into a wall in the McCarthy Way Parking Structure](https://dailytrojan.com/2024/04/04/vehicle-crashes-into-wall-of-mccarthy-way-parking-structure/). Thankfully the driver was safe so this can be labeled as a fun fact and not a sad fact.