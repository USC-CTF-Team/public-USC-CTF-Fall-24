# Buildings

challenge author: gysabell

category: osint

writeup author: neonlian

## Solution

Reverse image search each of the places. Use the associated number to choose the character out of the building's three letter acronym. 

If the acronym doesn't appear on the website you found for a picture, you can find the acronym in USC's [building directory](https://web-app.usc.edu/ws/soc_archive/soc/term-20143/building-directory/) 
or by looking up the building name at https://maps.usc.edu.

Building list
```
C - Robert Zemeckis Center for Digital Arts (RZC), 3
Y - Royal St. House (ROY), 3
B - Bing Theatre (BIT), 1
O - Alpha Gamma Omega (AGO), 3 
R - Bridge Memorial Hall (BRI), 2
G - University Gardens (UGB), 2
{
B - Parkside Arts & Humanities / Parkside Residential Building (PRB), 3
R - Birnkrant Residential College (BSR), 3
I - Dornsife Neuroscience Imaging Center (DNI), 3
C - Cardinal Gardens (CAR), 1
K - Kaprielian Hall (KAP), 1
S - Laird J. Stabler Memorial Hall (LJS), 3
}
```

Flag: `CYBORG{BRICKS}`
