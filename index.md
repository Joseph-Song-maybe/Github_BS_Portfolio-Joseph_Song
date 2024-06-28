# Choose-Your-Own Adventure Display


<img src="Picture.jpg" width="200" />



<!---
Replace this text with a brief description (2-3 sentences) of your project. This description should draw the reader in and make them interested in what you've built. You can include what the biggest challenges, takeaways, and triumphs from completing the project were. As you complete your portfolio, remember your audience is less familiar than you are with all that your project entails!

You should comment out all portions of your portfolio that you have not completed yet, as well as any instructions:

| **Engineer** | **School** | **Area of Interest** | **Grade** |
|:--:|:--:|:--:|:--:|
| Joseph S| Palo Alto Highschool | Software Engineering | 9th Grade


**Replace the BlueStamp logo below with an image of yourself and your completed project. Follow the guide [here](https://tomcam.github.io/least-github-pages/adding-images-github-pages-site.html) if you need help.**


![Headstone Image](logo.svg)
  
# Final Milestone

 **Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

 <iframe width="560" height="315" src="https://www.youtube.com/embed/F7M7imOVGug" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

 For your final milestone, explain the outcome of your project. Key details to include are:
 - What you've accomplished since your previous milestone
 - What your biggest challenges and triumphs were at BSE
 - A summary of key topics you learned about
 - What you hope to learn in the future after everything you've learned at BSE



 # Second Milestone

 **Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

 <iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

 For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
 - Technical details of what you've accomplished and how they contribute to the final goal
 - What has been surprising about the project so far
 - Previous challenges you faced that you overcame
 - What needs to be completed before your final milestone
-->
 # First Milestone



 <iframe width="560" height="315" src="https://www.youtube.com/embed/1DFSt7tJ0po?si=ZlgEAwYYKRw2jAyx" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
 
<img src="Picture.jpg" width="200" />

## Summary
For my main project, the Choose-Your-Own-Adventure Display(206), I've made significant progress. This project was chosen due to my interest in text adventures and the classic choose-your-own-adventure books. In addition, I was most excited about my ideas for modifications out of all the projects. I've successfully built the stand for the screen, installed the necessary programs, and debugged the code to make the PyPortal (The Display Machine) show an example adventure from the Project Book. This adventure includes coded buttons, music, different backgrounds, paths, and endings.

## Components & Code Explanation
The physical components were a PyPortal, a Stand, and a USB cable. The stand supports the screen, and the USB connects the portal to my MacBook. Everything comes from the portal, including the files and code from my computer. The files came from a built-in library in my CIRCUITPY drive, where many vital aspects, such as the buttons, touchscreen, and music, all come from files the code uses to create the experience. 

Out of all the files in the library, the most important file that makes the game function is the PYOA import. The PYOA import is the official framework for choosing your adventure for the portal. It is also the program that triggers the sound effects, sets the background and text, and displays transition animation.

/See Below for More Information/

The primary code’s purpose is to access JSON files using the load.game command, where a list of multiple dictionaries, each acting as “cards.”(Which is also part of PYOA) The cards are like a page in a slide deck, each showing a different visual. Each dictionary contains different aspects of the card, like the text, the color of said text, the background, and much more. The code tells the portal to change cards according to the user's button input, creating the game. 

<img src="Picture.jpg" width="200" />

## Challenges
My first two steps for the project, assembling the stand and gathering the correct programs, weren’t too difficult. The real challenge came from debugging the code from the project book. The code was built on a previous version of CircuitPython, the portal program, which meant some folders didn’t exist, and some code was outdated from the current version of Python. This meant I had to improvise, and most of my time was spent experimenting and seeing what worked and what didn’t. Constantly running into errors was frustrating, and some errors like a RunTimeError that happens in a file that doesn’t exist continuously appeared, even if I had made the slightest tweak. After many debugging and troubleshooting attempts, I discovered a folder filled with needed PYOA data, and adding the massive folder seemed to work. It wasn’t a pleasant experience, but I finished within my second week.

## What I Learned & What I’ll Do Next
In my first milestone, I primarily learned about coding. I learned about entering commands into the terminal and its usefulness for downloading resources with pip commands. I’ve learned many tips and tricks for CircuitPython, which will be especially important later in the project. Finally, I’ve found the basic principle of decoding and solving error messages, which is going to be something I’ll have to master if I want to code later in life. For what I’ll do next, I plan to start drafting my ideas for my adventure. Furthermore, I want to start on my visuals, in which I plan to use simple pixel art inspired by another text-based RPG I was inspired by. 



 ## Code
 Here's where you'll put your code. The syntax below places it into a block of code. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize it to your project needs. 

 ```c++
 void setup() {
   // put your setup code here, to run once:
   Serial.begin(9600);
   Serial.println("Hello World!");
 }

 void loop() {
   // put your main code here, to run repeatedly:

 }
```

 # Bill of Materials
 Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
 Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

 | **Part** | **Note** | **Price** | **Link** |
 |:--:|:--:|:--:|:--:|
 | Item Name | What the item is used for | $Price | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/"> Link </a> |
 | Item Name | What the item is used for | $Price | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/"> Link </a> |
 | Item Name | What the item is used for | $Price | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/"> Link </a> |


# Starter Project


<iframe width="560" height="315" src="https://www.youtube.com/embed/DByS1SLt-O0?si=E4YeEYrHOiGyVLPe" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Summary
My project was the BlueStamp Ardunio Starter. I chose this project because I enjoyed the creative freedom it gave me, which allowed me to tinker and create freely. It also offered incredibly convenient skills to have later in life, such as circuitry, soldering, and coding. I decided to build a simple ultrasonic detection system that measures the distance between the object it detects and itself and blinks an LED when the object is 20cm or closer.

## Components
The project comprised an Arduino Uno, a breadboard, an ultrasonic sensor, an LED, resistors, and numerous jumper cables. The main system moves the inputs from the sensor to the Arduino, and a mini system blinks the LED. The sensor is the main component of the whole system and functions by shooting a beam of ultrasound. The beam travels until it hits an object, bouncing back into the sensor. Then, the system calculates the object’s distance by using the time it took for the beam to return to the sensor and the speed of sound, using the formula distance = speed x time. After transporting the data to the computer, it prints in the serial monitor, is brought into an if statement that questions if the distance is less than 20cm, and lights the LED if true.

![Headstone Image](Ultrasonic-Sensor-Arduino-Interfacing_2.png)

## Challenges
The main challenges I faced were the technical and physical aspects. With zero experience with circuitry, I frequently made mistakes, such as plugging wires in the wrong parts, leading to obstacles that could have been solved within seconds with proper knowledge. In addition, I had some problems with soldering and ended up with a crooked proto shield, so I had to resort to the breadboard. However, the sensors were the most exhausting part of this project. I first worked on a motion sensor, but after receiving underwhelming accuracy in the readings, I restarted the project, switched to ultrasonic sensors, and went through two more buggy sensors until I finally found one that worked.

## What I Learned
Overall, this was an amazing experience and something that will come into use later. I learned many skills I expected, like soldering and circuitry. Still, I also learned niche things I wouldn’t find without physical experiences, such as double-checking technology and simplifying circuitry. It challenged my problem-solving skills and tested my patience and resilience. After this project, I want to move on to my main project, which I’m truly looking forward to. The skills I learned will be crucial to this much larger task.


# Other Resources/Examples

- [CircuitPython Pyoa Import](https://docs.circuitpython.org/projects/pyoa/en/latest/api.html)
- [Example 2](https://sviatil0.github.io/Sviatoslav_BSE/)
- [Example 3](https://arneshkumar.github.io/arneshbluestamp/)


