# Writeup for EEnemies

author: sophisticated.space

category: misc

## Step 0
The first realization about this challenge is that it is written in Verilog, a hardware description language. Verilog has two assignments, blocking (=) and nonblocking (<=). 

Blocking assignments operate like other coding languages' assign statements, where each line is evaluated before the next one can begin. For example, `a = b; b = a;` would result in both a and b equaling b. However, nonblocking works differently. With nonblocking assignments, each line is evaluated at the edge of a "clock tick," meaning everything updates at once, and uses the previous cycle's values to evaluate its new values. For example, `a = b; b = a;` would result in a and b swapping values.

Once you understand this, you can begin to understand the challenge script. It swaps letters and also does Caesar cipher-ish stuff on each index.

## Step 1
Create a reverse Verilog file. Undo the swapping and caesar shifting by swapping the inputs/outputs (what is on each side of the <=) and changing additions to subtractions (and visa versa).

## Step 2
Create your testbench file. Copy the challenge TB and change the line "CYBORG{XXXXXXX}" to "CXCOSF{CR,majnrr-stbj-mol}"

## Step 3
Run your solver script. I used Modelsim. Make sure your code compiles and then simulate it and watch the waveform. Run the simulation and change the radix to ASCII. Voilà!
