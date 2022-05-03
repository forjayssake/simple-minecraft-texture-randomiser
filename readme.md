# Simple Minecraft texture randomiser
This script creates a Minecraft texture pack for a given version by randomly reordering the png file names in /textures/block.
  
Optionally you can choose to run just the commands to setup the files needed to create your own custom texture pack (`setup`), and then to make your custom texture pack available to use in Minecraft (`complete`). 

![Example result](example.png)

## Dependencies 
* Currently only Windows compatible until I sort out file paths properly
* Python 3x. Download: https://www.python.org/downloads/

## Modes
`random` Create a randomised texture pack. This is the defaul mode  
`setup`  Run the commands required to create a custom texture pack  
`complete` Run the commands required to complete a custom texture pack  

## Arguments
    -h --help # display help text and exit
    -d --directory # [Required] Mincraft verison directory to create the texture pack against
    -m --mode # [Optional] Defaults to 'random'
    -f --format # [Optional] Pack format to use for the selected Minecraft version. defaults to 8 for versions 1.18+

## Pack formats  

| Pack format | Minecraft version |
|-------------|-------------------|
| 1	          | 1.6.1 – 1.8.9     |
| 2	          | 1.9 – 1.10.2      |
| 3	          | 1.11 – 1.12.2     |
| 4	          | 1.13 – 1.14.4     |
| 5	          | 1.15 – 1.16.1     |
| 6	          | 1.16.2 – 1.16.5   |
| 7	          | 1.17 - 1.17.1     |
| 8	          | 1.18+             |


## Examples
  
Create a randomised texture pack:  

    python .\mc_random_tp.py -d C:\Users\<user_name>\AppData\Roaming\.minecraft\versions\<required_version>
  
Create a randomised texture pack for a specific Minecraft version:  

    python .\mc_random_tp.py -d C:\Users\<user_name>\AppData\Roaming\.minecraft\versions\<required_version> -f 7
  
Setup a custom texture pack structure:  

     python .\mc_random_tp.py -d C:\Users\<user_name>\AppData\Roaming\.minecraft\versions\<required_version> -m setup
  
Complete  a previously setup custom texture pack:

     python .\mc_random_tp.py -d C:\Users\<user_name>\AppData\Roaming\.minecraft\versions\<required_version> -m complete