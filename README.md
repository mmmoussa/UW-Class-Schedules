# UW-Class-Schedules
Understanding the relationship between the time and day of week and the number of students scheduled to be in class

## Purpose
I was kind of curious about how UW does scheduling and when people normally have class, so I thought I'd find out. This project's goal is to provide an understanding of when students have class and what times are the best for reaching people, arranging meetings, etc.

## Getting started
Everything needed to reproduce my results is in this repo. This project requires you to have python 2.7 installed. You'll also need to `pip install requests` if you want to fetch the data yourself and `pip install plotly` if you want to create the result graph yourself.

If you want to start from the beginning and download the data yourself, [get an api key](https://api.uwaterloo.ca/apikey/), insert it into [fetch.py](fetch.py), and then run fetch.py. Once you've gathered the data, run [process.py](process.py) to get the results.

If you don't want to gather the data yourself, don't worry, I've included it in this repo. All you need to do is run [process.py](process.py) to get the results.

## Result
You can see the resulting graph [here]()

## Disclaimer
The data used by this project comes from the [University of Waterloo Open Data API](https://api.uwaterloo.ca). The accuracy of the data and results is not guaranteed and is provided without warranty.
