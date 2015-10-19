# Vapour

Platformer RPG made in Python 3.2 and Pygame.

![Alt text](screenshot.png "Missile with additive particle effects")

###Controls in normal mode
- Arrow keys for movement
- Space to attack
- Esc to quit

###Controls in level editor mode

- 'g' to toggle grid
- 'e' to rotate block clockwise
- 'q' to rotate block counter-clockwise
- mouse to select blocks at the bottom

###Level file formatting
Files are loaded in '**.txt**' file format.

|Character          |Type           |
| ------------------|:-------------:|
|'**#**'            |Normal block   |
|'&nbsp;'           |Empty space    |
|'**$**'            |Top block      |
|'**@**'            |Top-Left corner block|
|'**!**'            |Top-Right corner block|
|'**^**'            |Right block    |
|'**%**'            |Left block     |

###Example of level file used in demo

    @$!                 @$$$$!                                                                         
    %#^                 %####^                                                                         
    %#^                 %####^                                                                         
    %#^       @$!       %####^                                                                         
    %#^       %#^       %####^                                                                         
    %##$$!    %#^    @$$#####^                                                                         
    %####^    %#^    %#######^                                                                         
    %####^    %#^    %#######^                                                                 
    
    
    
    
                @$!                                                                                    
                %#^                                                                                    
                %#^                                                                                    
              @$##^                                                                                    
              %###^                                                                                    
              %###^                                                                                     
    @$$$$$$$$$#####$$$$$$$$$!                                                                          
    %#######################^                                                                          
    %#######################^
    %#######################^
