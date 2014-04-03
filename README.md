##pyApriori

A python implementation of Apriori algorithm.

The training dataset can be downloaded from the [UCI machine learning](http://archive.ics.uci.edu/ml/).

###Usage
Implemented in Python 2.7.3
```
python apriori.py -i input_file.csv -g goods_name.csv [-s] [minimum support] [-c] [minimum confidence]
```

```
#defaut value of minimum support is set to 0.03, and that of the minimum confidence is set to 0.5
python apriori.py -i 20000/20000-out1.csv -g goods.csv
```

#### Example
```
python apriori.py -i 1000/1000-out1.csv -g goods.csv
```

This will genetate a set of association rules:

```
Marzipan Cookie --> Tuile Cookie [ confidence =  0.56 ]
Cheese Croissant --> Orange Juice [ confidence =  0.54 ]
Napoleon Cake --> Strawberry Cake [ confidence =  0.53 ]
Truffle Cake --> Gongolais Cookie [ confidence =  0.51 ]
Opera Cake, Cherry Tart --> Apricot Danish [ confidence =  0.94 ]
Opera Cake, Apricot Danish --> Cherry Tart [ confidence =  0.95 ]
Cherry Tart, Apricot Danish --> Opera Cake [ confidence =  0.78 ]
Coffee Eclair, Apple Pie --> Almond Twist [ confidence =  0.92 ]
Coffee Eclair, Almond Twist --> Apple Pie [ confidence =  0.94 ]
Apple Pie, Almond Twist --> Coffee Eclair [ confidence =  0.95 ]
Chocolate Cake, Casino Cake --> Chocolate Coffee [ confidence =  0.95 ]
Chocolate Cake, Chocolate Coffee --> Casino Cake [ confidence =  0.77 ]
Casino Cake, Chocolate Coffee --> Chocolate Cake [ confidence =  0.95 ]
Blueberry Tart, Apricot Croissant --> Hot Coffee [ confidence =  0.78 ]
Blueberry Tart, Hot Coffee --> Apricot Croissant [ confidence =  0.91 ]
Apricot Croissant, Hot Coffee --> Blueberry Tart [ confidence =  0.93 ]
```
