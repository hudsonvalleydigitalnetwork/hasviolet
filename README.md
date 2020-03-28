# HASviolet


![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/raw/master/hardware/hasviolet-hw.png)

## Who is HVDN?

The Hudson Valley Digital Network or "HVDN" for short was created in 2017 to become a safe place where Hudson valley residents or those interested in our beautiful area can focus on emerging aspects of amateur radio and converge them with other hobby interests that benefit through the inclusion of wireless technology.  

HVDN is a virtual organization and currently does not offer in person meetings at this time, but we do arrange special events as well as virtual communications. While our roots are in amateur radio and are organized as an official club, including an FCC callsign of N2HVD, we are not affiliated with the ARRL so as to encourage alignment outside of traditional amateur radio more easily. 

Our primary goal is to offer a challenge to our members looking to try something new, rather than be weighted down by others that are too many steps behind.  All of HVDN members motivate each other to keep pushing forward.

You can read more about us at hvdn.org 

## Do you HASviolet?

Goal: Utilize the 900 MHz unlicensed ISM band and parrallel licensed amateur radio spectrum to enable an open source data communicator to collectively promote the usage of emerging wireless protocols via converged wireless hobbyist circles. 

Project HASviolet consists of the following components:

     •	Hardware
     •	Antenna
     •	Software
     
## Why “HASviolet”?

Creating an agnostic and universally appealing project name was important to create wider appeal for the project. 

The name of "Violet" was selected by first starting with a color and then looking for a story behind it. With all colors easily rendered by a standardized HTML CSS HEX code, the value of 8B0BB4 also translates to a decimal value of 911250. 

This value looks like the frequency of 911.250 MHz and thus is the main frequency to be used for the HVDN sponsored "Project HASviolet".  

The word "HAS" is a simple acronym made up of the first letter of the words "Hardware", "Antenna" and "Software". 

The full project name is "HASviolet" which is as fun to say or promote its goal and use cases.

## Who is behind HASviolet?

     • Joe Apuzzo N1JTA (Core Software & Git Project Documentation)
     • Joe Cupano NE2Z (Hardware Certification & General Do'er of Stuff)
     • Steve Bossert K2GOG (Antenna/RF Design & Public User Experience/Information)

       *Note: This is our first attempt at a Git repo....so go easy on us....  :)

## What is HASviolet

Three different components make up the entirety of the HASviolet Project. They are: 

### Hardware 
HASviolet is comprised of low cost common off the shelf hardware or COTS. This approach reduced project design time and created a low barrier of entry for anyone interested in the project. 

The initial approved hardware includes the [Adafruit LoRa Radio Bonnet with OLED - RFM95W @ 915MHz - RadioFruit and the Raspberry Pi Zero Wireless](https://www.adafruit.com/product/4074) attached to a [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708). 

Future hardware will include microcontrollers using standard form factors (ie Feathwerwing) with LoRa in other spectrum bands that offer additional convergence of ISM and amateur radio experimentation opportunities.

### Antenna
The 902 to 928 MHz ISM spectrum for unlicensed communication in ITU region 2 has a few limitations to consider. Tolerance for interference from other users and maximum transmission power that creates a 50 mV/m of electrical field strength at 3 meters distance are what has to be considered in HASviolet. The (US) [Federal Communications Commission title 47 part 15](https://www.fcc.gov/wireless/bureau-divisions/technologies-systems-and-innovation-division/rules-regulations-title-47) provides further detail. 

The Amateur Radio service however in ITU region 2 is exempt from transmission power limitations that restrict range for unlicensed users, but has to accommodate interference from other licensed or unlicensed users, such as public utility and other "Internet Of Things" applications. 

In order to maintain compliance, HVDN promotes the adoption of field strength measuring equipment and use of the appropriate antenna dependent on our primary HASviolet operating frequency of 911.250 MHz with or without an Amateur Radio license.

The HASviolet project includes an HVDN designed directional broadband ISM and amateur radio antenna to help create awareness of the benefits of gaining an Amateur Radio license for longer range communication. 

Unlicensed users may appreciate the antenna’s ability to send and receive signals from further away or limit reception or interference in certain directions.  Our goal through this antenna example is to show immediate value in gaining an Amateur Radio license to help with further education and challenges.

### Software 

By assembling project HASviolet from common off the shelf hardware, a simple software package was needed to provide easy setup and use of HASviolet.  Our basic demonstrator applications for HASviolet include a stand alone receive, stand alone transmit, beacon mode and text based communicator.

These all utilize python libraries and all sorts of other crap that we feel we did a good job in documenting as part of our project journey. 

The overall goal though, is to make an image that is easy to deploy and get up and running very quickly.

## Getting Started

Start with reading the the [HASviolet Installation Guide](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/HASviolet_Installation_Guide_v1-1.pdf). It wil     l tell you what hardware you will need, installing Raspbian Lite OS, and downloading then running the [install automation script](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/HASviolet_install.sh).
