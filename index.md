# Ball Tracking Robot with Computer Vision 
<!---
Replace this text with a brief description (2-3 sentences) of your project. This description should draw the reader in and make them interested in what you've built. You can include what the biggest challenges, takeaways, and triumphs from completing the project were. As you complete your portfolio, remember your audience is less familiar than you are with all that your project entails!
-->

Derin Gurses | Cuperitno High School | General Engineering | Rising Junior

<!---
**Replace the BlueStamp logo below with an image of yourself and your completed project. Follow the guide [here](https://tomcam.github.io/least-github-pages/adding-images-github-pages-site.html) if you need help.**

![Headstone Image](Derin-Headshot.png){: height="50%" width="50%"}

  
# Final Milestone
<!---
For your final milestone, explain the outcome of your project. Key details to include are:
- What you've accomplished since your previous milestone
- What your biggest challenges and triumphs were at BSE
- A summary of key topics you learned about
- What you hope to learn in the future after everything you've learned at BSE

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

<iframe width="560" height="315" src="https://www.youtube.com/embed/F7M7imOVGug" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


# Second Milestone
<!-- 
For your second milestone, explain what you've worked on since your previous milestone. You can highlight:
- Technical details of what you've accomplished and how they contribute to the final goal
- What has been surprising about the project so far
- Previous challenges you faced that you overcame
- What needs to be completed before your final milestone 

**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

<iframe width="560" height="315" src="https://www.youtube.com/embed/y3VAmNlER5Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
--->

# First Milestone

I am building a ball tracking robot using computer vision which is meant to follow a red ball by doing image processing to track the ball. The main components of my project are the DC motors, Raspberry Pi micro-controller board, L298N motor driver board, Raspberry Pi camera, and ultrasonic sensors.

The end goal for my project is for the camera to be able to detect the red ball and to be able to maneuver the robot accordingly to follow the ball through my Python code. Up until this first milestone, I've build the starting prototype of my robot, set up my Raspberry Pi micro-controller, wired my two motors to my L298N motor driver board and to a power source (battery pack), and wrote some simple lines of code to test the functionality of both my Raspberry Pi camera and DC motors. 

Some of the most challenging obstacles I faced was to figure out how work and display my Raspberry Pi, and to troubleshoot with one of my motors originally not working. I've managed to overcome both of these major challenges so far, and now have a functioning Raspberry Pi and two functioning DC motors. Additional challenges that I have yet to overcome include the installation of the 3 ultrasonic sensors and the trainnig of the machine learning model meant to track the color red with computer vision.

In the future, I plan to research how to overcome the challenge of building a machine learning model and figuring out how to wire my ultrasonic sensors by studying past circuit diagrams and getting a fundamental understanding of how an ultrasonic sensor works.  
<!--
**Don't forget to replace the text below with the embedding for your milestone video. Go to Youtube, click Share -> Embed, and copy and paste the code to replace what's below.**

<iframe width="560" height="315" src="https://www.youtube.com/embed/CaCazFBhYKs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


# Schematics 
<!---
Here's where you'll put images of your schematics. [Tinkercad](https://www.tinkercad.com/blog/official-guide-to-tinkercad-circuits) and [Fritzing](https://fritzing.org/learning/) are both great resoruces to create professional schematic diagrams, though BSE recommends Tinkercad becuase it can be done easily and for free in the browser. 


# Code
<!---
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
<!--
Here's where you'll list the parts in your project. To add more rows, just copy and paste the example rows below.
Don't forget to place the link of where to buy each component inside the quotation marks in the corresponding row after href =. Follow the guide [here]([url](https://www.markdownguide.org/extended-syntax/)) to learn how to customize this to your project needs. 

| **Part** | **Note** | **Price** | **Link** |
|:--:|:--:|:--:|:--:|
| Item Name | What the item is used for | $Price | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/"> Link </a> |
|:--:|:--:|:--:|:--:|
| Item Name | What the item is used for | $Price | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/"> Link </a> |
|:--:|:--:|:--:|:--:|
| Item Name | What the item is used for | $Price | <a href="https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/"> Link </a> |
|:--:|:--:|:--:|:--:|

# Other Resources/Examples
<!---
One of the best parts about Github is that you can view how other people set up their own work. Here are some past BSE portfolios that are awesome examples. You can view how they set up their portfolio, and you can view their index.md files to understand how they implemented different portfolio components.
- [Example 1](https://trashytuber.github.io/YimingJiaBlueStamp/)
- [Example 2](https://sviatil0.github.io/Sviatoslav_BSE/)
- [Example 3](https://arneshkumar.github.io/arneshbluestamp/)
-->

# Starter Project

## Summary
As a starter project, I chose to make a digital clock. This project makes use of a variety of different components which all work together to provide the time display that you see as an end result. The main conceptual understanding of how a digital clock works comes with understanding the **time base**, which is essentially the internal clock of the digital clock, providing the project with functionality. The component that makes this internal clock possible is the **crystal oscillator**. 

The function of a digital clock revolves around a quartz crystal inside which oscillates, and therefore is named the crystal oscillator. Quartz is the ideal material to use as these oscillators due to the uniformity in its structure at the molecular level, which ultimately resutls in more consistent oscillations/vibrations, bettering the time base as opposed to how it would be using a different material. When the electric charge (coming from the power source) reaches this crystal, it begins to oscillate at a frequency of approximately 33,000 oscillations per second (Hz). For each 33,000 oscillations of the crystal (or one second of real time), the circuit releases an electric pulse, effectively converting the oscillations of the crystal into seconds. 

### Components Used
- Resistors, thermistors, photoresistors, and transistors
- Ceramic capacitors and electrolytic capacitors
- Diode
- A crystal oscillator 
- A lithium battery
- Buzzer
- DIP-20 IC

<iframe width="560" height="315" src="https://www.youtube.com/embed/G0spfXQhkr8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
