# HASviolet


![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/hardware/HVDN_HASviolet_Git_Banner_1.jpg)

## Who is HVDN?

The Hudson Valley Digital Network or "HVDN" for short was created in 2017 to become a global ambassador for the Hudson Valley to highlight wireless experimentation and convergence between amateur radio and other hobby areas.

HVDN is a virtual organization and currently does not offer in person meetings at this time like traditional "ham radio clubs", but we do arrange special in person and virtual events as found on our "[Activity](https://hvdn.org/activity-1)" page.

While our roots are in amateur radio and are organized as an official club, including an FCC callsign of N2HVD, we are not affiliated with the [ARRL](http://www.arrl.org/home) so as to best encourage alignment outside of traditional amateur radio more easily. 

Our primary goal is to offer challenges to our members looking to try something new, rather than be weighted down by others that are too many steps behind.  All of HVDN members motivate each other to keep pushing forward and our HASviolet project showcases that well

You can read more about us at [hvdn.org ](https://hvdn.org) and of course at [hvdn.org/violet](https://hvdn.org/violet)

## Do you HASviolet?

Our goal was to promote experimentation in underutilized amateur radio spectrum and we chose the 900 MHz (33cm) band to do this.  

The 33cm band was a great choice because anyone even without an amateur radio license can experiment here, but may be later motivated to get the basic United States Technician class amateur radio license in order to experiement with higher power transmitters and antenna designs not available to the general hobbyist.

Project HASviolet consists of the following components:

    • Hardware
    • Antenna
    • Software
     
## Why “HASviolet”?

Creating an agnostic and universally appealing project name was important to us. 

The word "violet" was selected by first starting with a color and then looking for a story behind it. With all colors easily rendered by a standardized HTML CSS HEX code, the value of 8B0BB4 also translates to a decimal value of 911250. 

This value looks like the frequency of 911.250 MHz and thus is the main frequency to be used for our project.  We also hope others follow in our steps to use this frequency too for a certain level of "interoperability"  

The word "HAS" is a simple acronym made up of the first letter of the words "Hardware", "Antenna" and "Software". 

The full project name is "HASviolet" which is as fun to say as well as to find unique use cases for it!

## Who is behind HASviolet?

    • Joe Apuzzo N1JTA (Inital idea)
    • Joe Cupano NE2Z (Core Software & Product Manager)
    • Steve Bossert K2GOG (Antenna/RF Design & Public User Experience/Information)

    *Note: This is our first attempt at a Git repo....so go easy on us....  :)

## What is HASviolet?

Three different components make up the entirety of the HASviolet Project. They are: 

### Hardware 
HASviolet is comprised of low cost common off the shelf hardware or COTS. This approach reduced project design time and created a low barrier of entry for anyone interested in the project. 

The initial "HASviolet Certified" hardware includes the [Adafruit LoRa Radio Bonnet with OLED - RFM95W @ 915MHz - RadioFruit and the Raspberry Pi Zero Wireless](https://www.adafruit.com/product/4074) attached to a [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708).  We are also endorsing the [PiSugar](https://github.com/PiSugar/PiSugar) open source battery pack for portable use cases.

![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/hardware/HVDN_HASviolet_Git_Hardware_1.jpg)

Future hardware will include other microcontrollers using standard form factors (Example: [Featherwing](https://hvdnnotebook.blogspot.com/2018/11/hvdn-reset-is-feather-better.html)) with LoRa capability. 

Joe Apuzzo N1JTA led much of the selection of hardware for the project along with input from Joe Cupano NE2Z and Steve Bossert K2GOG.

### Antenna

The 902 to 928 MHz ISM spectrum for unlicensed communication in [ITU region 2](https://en.wikipedia.org/wiki/ITU_Region) has a few limitations to consider. Tolerance for interference from other users and maximum transmission power that creates a 50 mV/m of electrical field strength at 3 meters distance are what has to be considered in HASviolet. 

The (US) [Federal Communications Commission title 47 part 15](https://www.fcc.gov/wireless/bureau-divisions/technologies-systems-and-innovation-division/rules-regulations-title-47) provides further detail. 

The Amateur radio service in ITU region 2 is exempt from transmission power limitations that restrict range for unlicensed users, but has to accommodate interference from other licensed or unlicensed users, such as public utility and other "Internet Of Things" application use cases.

![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/antenna/HVDN_HASviolet_Git_Antenna_V1.jpg)

In order to maintain compliance, HVDN promotes the adoption of field strength measuring equipment and use of the appropriate antenna dependent on our primary HASviolet operating frequency of 911.250 MHz with or without an Amateur Radio license. 

Please visit our [blog](http://notebook.hvdn.org/2018/02/rssi-dbm-oh-my.html) for details about field strength measurements.

The HASviolet project includes an HVDN designed 900 MHz directional broadband ISM and amateur radio antenna to help create awareness of the benefits of gaining an amateur radio license for longer range communication. 

Unlicensed users may appreciate the antenna’s ability to send and receive signals from further away or limit reception or interference in certain directions by simply keeping the power level down on the HASviolet hardware.  

Our goal through our antenna example is to show immediate value in gaining an amateur radio license to help with further education and challenges.

Steve Bossert K2GOG led the antenna design and was helped with assembly instruction feedback from Joe Cupano NE2Z and Joe Apuzzo N1JTA plus members of the the [Squidwrench](http://squidwrench.org/) maker space. The design and assembly process has even gave us inspiration for an even more advanced design that is easier to build that will be available in our next release during the summer of 2020.


### Software 

By assembling project HASviolet from common off the shelf hardware, a simple software package was needed to provide easy setup and use of HASviolet.  

Our basic "Python" based demonstrator applications include stand alone receive, stand alone transmit, beacon mode and text based communicator modes easily accessible via any terminal application such as [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/) or [MobileSSH](https://play.google.com/store/apps/details?id=mobileSSH.feng.gao&hl=en_US)

There is a really great amount of documention showing how we built the code to help others easily experiment with it. This includes both built in application help functions using the "-h" command as well as our detailed installation, user guides and articles found on our blog.

Overall, we really wanted to make this easy to deploy to help you get up and running very quickly.

Joe Cupano NE2Z led the entire software development process and only had minimal input on its core functionality from others, including the [HVopen](https://hvopen.org/) open source software user group. User interface (UI) and user experience (UX) feedback were provided by Steve Bossert K2GOG and Joe Apuzzo N1JTA. Our goal is to provide quarterly software updates moving forward.

![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/development/HVDN_HASviolet_Git_Software.jpg)


## Getting Started

Start with reading the the [HASviolet Installation Guide](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/HASviolet-RPi_Guide_v26.pdf). 

It covers:

* Installing Raspbian Lite OS
* Configuring the RPi hardware (raspi-config settings)
* Installing HASviolet
* Usage details on HASviolet applications

If want to install while reading the guide just perform the following from the Pi home directory:

```
wget https://raw.githubusercontent.com/hudsonvalleydigitalnetwork/hasviolet/master/HASviolet_install.sh
chmod 755 HASviolet_install.sh
./HASviolet_install.sh
```

![alt-test](https://github.com/hudsonvalleydigitalnetwork/hasviolet/blob/master/hardware/hasviolet-hw-alternate.png)
