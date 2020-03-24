# HASviolet


![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/raw/master/hardware/hasviolet-hw.png)

:Project HASviolet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5.: 

## Do you HASviolet?

Goal: Utilize the 900 MHz unlicensed ISM band and parrallel licensed amateur radio spectrum to enable an open source data communicator to collectively promote the usage of emerging wireless protocols via converged wireless hobbyist circles in the Hudson Valley of New York and globally. Project HASviolet consists of the following components:

     •	Hardware
     •	Antenna
     •	Software
     
## Why “HASviolet”?

Creating an agnostic and universally appealing project name was important to create wider appeal for the project. The name of "Violet" was selected by first starting with a color and then looking for a story behind it. With all colors easily rendered by a standardized HTML CSS HEX code, the value of 8B0BB4 also translates to a decimal value of 911250. This value looks like the frequency of 911.250 MHz and thus is the main frequency to be used for the HVDN sponsored "Project HASviolet".  The word "HAS" is a simple acronym made up of the first letter of the words "Hardware", "Antenna" and "Software". The full project name is "HASviolet" which is as fun to say or promote its goal and use cases.

## What is HASviolet

Three different components make up the entirety of the HASviolet Project. They are: 

### Hardware 
> HASviolet is comprised of low cost common off the shelf hardware or COTS. This approach reduced project design time and created a low barrier of entry for anyone interested in the project. The initial approved hardware includes the [Adafruit LoRa Radio Bonnet with OLED - RFM95W @ 915MHz - RadioFruit and the Raspberry Pi Zero Wireless](https://www.adafruit.com/product/4074) attached to a [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708). Future hardware will include microcontrollers using standard form factors (ie Feathwerwing) with LoRa in other spectrum bands that offer additional convergence of ISM and amateur radio experimentation opportunities.

### Antenna
> The 902 to 928 MHz ISM spectrum for unlicensed communication in ITU region 2 has a few limitations to consider. Tolerance for interference from other users and maximum transmission power that creates a 50 mV/m of electrical field strength at 3 meters distance are what has to be considered in HASviolet. The (US) [Federal Communications Commission title 47 part 15](https://www.fcc.gov/wireless/bureau-divisions/technologies-systems-and-innovation-division/rules-regulations-title-47) provides further detail. 

> The Amateur Radio service however in ITU region 2 is exempt from transmission power limitations that restrict range for unlicensed users, but has to accommodate interference from other licensed or unlicensed users. In order to maintain compliance, HVDN promotes the adoption of field strength measuring equipment and use of the appropriate antenna dependent on the user’s frequency of 911.250 MHz with or without an Amateur Radio license.

> The HASviolet project includes an HVDN designed directional broadband multi-frequency (433/900) ISM and amateur radio antenna to help create awareness of the benefits of gaining an Amateur Radio license for longer range communication. Unlicensed users may appreciate the antenna’s ability to receive signals from further away and to show immediate value in gaining an Amateur Radio license.

### Software 
> By assembling project HASviolet from common off the shelf hardware, a simple software package was needed to provide easy setup and use of HASviolet.  The basic demonstrator application for HASviolet is a text based communicator that utilizes python libraries and all sorts of other crap that my collaborators will elaborate on. The overall goal though, is to make an image that is easy to deploy and get up and running very quickly.

## Getting Started

Start with reading the the [HASviolet Installation Guide](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/HASviolet_Installation_Guide_v1-1.pdf). It wil     l tell you what hardware you will need, installing Raspbian Lite OS, and downloading then running the [install automation script](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/HASviolet_install.sh).

## 2020-03-24 SPECIAL NOTICE

Because the repo is private until launch, the fresh installation and "Scorched Earth Update" scripts cannot be retrieved from this repo. Instead perform the following from within the /home/pi directory;

### Fresh Install Script
```
wget https://raw.githubusercontent.com/joecupano/launchtest/master/hasty.sh
chmod 755 hasty.sh
./hasty.sh
```

To include a working directory to test the development code append dev to the script when running it

```
./hasty.sh dev
```

### Scorched Earth Script
```
wget https://raw.githubusercontent.com/joecupano/launchtest/master/hastier.sh
chmod 755 hastier.sh
./hastier.sh
```

To include a working directory to test the development code append dev to the script when running it

```
./hastier.sh dev
```
