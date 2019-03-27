# colour_manager
Hands out colours from a pool of possibilities.

Each colour it hands out is a Colour() object, with a name and a 
red-green-blue tuple of colour components.

When asked for a new colour, tries to select one that maximizes the 
contrast will all the colours it has already handed out.

When a colour is no longer in use (when something calls the Colour() 
object's __del__ method), returns it to the pool.

To get one new colour, call nextColour().

To get several at a time, call colourList().

You may initialise a ColourManager with an (optional) background colour
(use either a red-green-blue tuple or a Colour() object). When handing
out colours, the ColourManager will include the background colour (if 
any) among the set of those to which it tries to maximize the contrast
of the new colour. For many purposes, it's useful to initialise the
colour manager with background=[0, 0, 0] (black).

Examples of use:

(1)    
`
newManager = ColourManager()

newColour = newManager.nextColour()

print newColour

print newColour.colourvalues

`

result:

`
Bright Goddamn Red
[255, 0, 0] 
`


(2) 
`
newManager = ColourManager([0, 0, 0])
colours = []
for indx in range(7):
colours.append(newManager.nextColour())
for entry in colours:
print entry, entry.colourvalues
`

result:

`
Bright Goddamn Red [255, 0, 0]
Burnt Andy [125, 255, 255]
Smear of Gold [190, 255, 0]
Let No Man Stand Against Me Violet [180, 0, 255]
Eurotrash Blue [0, 120, 165]
Buck Shot Eyes Pink [255, 150, 150]
The Green Mass Ecstatic [0, 255, 0]
`


(3)
`
newManager = ColourManager([0, 0, 0])
sevenColours = newManager.colourList(7)
for colour in threeColours:
print colour, colour.colourvalues
`

result:

`
The Orange Mass Ecstatic [210, 125, 20]
Bible and a Rope Burgundy [230, 40, 100]
Ignominious Orange [235, 125, 125]
Soulless Middle-class Purple [255, 0, 255]
Yellow Cello [250, 255, 75]
Margaric Pink [255, 145, 255]
Schwa Aqua [75, 255, 255]
`
