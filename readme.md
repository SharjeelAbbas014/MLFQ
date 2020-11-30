# Multilevel feedback queue

This program simulate Multilevel Feedback Queue with following 3 queues
* Highest priority queue with Round Robin and Time quantum of 50ms
* Medium priority queue with Round Robin and Time quantum of 100ms
* Lowest priority queue with SRTF

## Dependencies?
* Install [python](https://www.python.org/downloads/source/), download the latest version I have used some python 3 syntax and features
* Use package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependancies
```bash
pip install -r requirements.txt
```

## Usage
* In command shell run 
```bash
python app.py
```
* Enter input.csv or other file to read data from

## Note
If you don't see any gantt chart appear kindly use any other IDE. Online IDEs might not work.

## File Instruction
There are 3 csv files given
* input.csv (This one have big processess so we can see process getting promoted)
* lotOfIdle.csv (This one is to test scenario where CPU is idle for a long time)
* bunchOfSmall.csv (This one is to test the script behavious on lots of small process and couple of large processes just for fun sake)

## Disclaimer
This script is using a color pallate of 10 colors each for unique colors
If you want to simulate more than one process please update the color pallete at line 264 are remove the error check at line 112

## Contribution
Contribution to this [repo](https://github.com/SharjeelAbbas014/MLFQ) is highly appreciated. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.