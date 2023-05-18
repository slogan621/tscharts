# Thousand Smiles Data Notebooks

This folder contains notebooks to analyze Thousand Smiles Data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Recommend Anaconda or Similar Environment
```

### File Locations

The TSD.py file will need to be updated

```
file_prefix = '../../../../../1000_Smiles/Data/tscharts-output/' #change to match location of your data
```

To assist in finding the location...

```
from os import listdir
from os.path import isfile, join

mypath = '../../../../../1000_Smiles/Data/'
print(listdir(mypath))
```

## Running the Notebooks

Simply execute the frames in order, make sure the TSD.py file is in the same folder.


## Built With

* [Amazon SageMaker Studio Lab](https://studiolab.sagemaker.aws/users/<YOUR_USER_NAME>) - The development environment used

## Contributing

All necessary file links and merged data can be accessed through the TSD.py file. All TSD data frames use the prefix "df_" and can be located using auto complete by entering "TSD.df_"

## Authors

* **William Wilsonn** - *Initial work* - 


## License

Licensed under the Apache License, Version 2.0 (the "License")

## Acknowledgments

* Syd Logan-data and example scripts
