# Multilevel feedback queue

This program simulate Multilevel Feedback Queue with following 3 queues
1- Highest priority queue with Round Robin and Time quantum of 50ms
2- Medium priority queue with Round Robin and Time quantum of 100ms
3- Lowest priority queue with SRTF

## Dependencies?
1- Install [python](https://www.python.org/downloads/source/), download the latest version I have used some python 3 syntax and features
2- Use package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependancies
```bash
pip install -r requirements.txt
```

## Usage
1- In command shell run 
```bash
python app.py
```
2- Enter input.csv or other file to read data from

## Note
If you don't see any gantt chart appear kindly use any other IDE. Online IDEs might not work.

## File Instruction
There are 3 csv files given
1- input.csv (This one have big processess so we can see process getting promoted)
2- lotOfIdle.csv (This one is to test scenario where CPU is idle for a long time)
3- bunchOfSmall.csv (This one is to test the script behavious on lots of small process and couple of large processes just for fun sake)

## Disclaimer
This script is using a color pallate of 10 colors each for unique colors
If you want to simulate more than one process please update the color pallete at line 264 are remove the error check at line 112

## Contribution
Contribution to this [repo](https://github.com) is highly appreciated. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.