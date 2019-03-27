from math_tools.tools import genscale, genperm, permsequence, Span

from math    import sqrt, sin, cos, pi
from sys     import maxint
from cPickle import load, dump

import copy, random



class ColourManager(object):
    """ Hands out colours from a pool of possibilities.
    
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
    > newManager = ColourManager()
    > newColour = newManager.nextColour()
    > print newColour
    > print newColour.colourvalues
    
    result:
    
    > Bright Goddamn Red
    > [255, 0, 0]
    
    
    (2)
    > newManager = ColourManager([0, 0, 0])
    > colours = []
    > for indx in range(7):
    >   colours.append(newManager.nextColour())
    > for entry in colours:
    >   print entry, entry.colourvalues
    
    result:
    
    > Bright Goddamn Red [255, 0, 0]
    > Burnt Andy [125, 255, 255]
    > Smear of Gold [190, 255, 0]
    > Let No Man Stand Against Me Violet [180, 0, 255]
    > Eurotrash Blue [0, 120, 165]
    > Buck Shot Eyes Pink [255, 150, 150]
    > The Green Mass Ecstatic [0, 255, 0]
    
    
    (3)
    > newManager = ColourManager([0, 0, 0])
    > sevenColours = newManager.colourList(7)
    > for colour in threeColours:
    >   print colour, colour.colourvalues
    
    result:
    
    > The Orange Mass Ecstatic [210, 125, 20]
    > Bible and a Rope Burgundy [230, 40, 100]
    > Ignominious Orange [235, 125, 125]
    > Soulless Middle-class Purple [255, 0, 255]
    > Yellow Cello [250, 255, 75]
    > Margaric Pink [255, 145, 255]
    > Schwa Aqua [75, 255, 255]  
    """
    
    colourDictionary      = {'Soulless Middle-class Purple' : [255, 0, 255], 'Bright Goddamn Red' : [255, 0, 0], 'The Green Mass Ecstatic' : [0, 255, 0], 'Walking on Sunset' : [235, 150, 160], 'Shipwreck Cyan' : [100, 205, 220], 'Bang to Rights Orange' : [190, 100, 50], 'Canny Blue' : [45, 25, 140], 'Missing Pink' : [225, 145, 190], 'Omoxicillin Pink' : [255, 230, 230], 'Orange Door Hinge' : [235, 125, 50], 'Crawling Down the Boulevard' : [100, 120, 100], 'Yellow-Green Remarkable' : [195, 240, 10], 'Dubious Grey' : [100, 115, 100], 'Silent Cues Grey' : [100, 105, 100], 'Vaudevillian Vermilion' : [225, 70, 50], "Fool's Gold" : [235, 255, 0], 'Mojave Phone Booth' : [255, 240, 245], 'Red Herring' : [85, 30, 0], 'Agomphious Green' : [180, 255, 200], 'Kid Charlemaine' : [125, 145, 125], 'Kerosene Green' : [110, 140, 110], 'Low-Rent Green' : [100, 135, 100], 'Indonesia Green' : [95, 130, 95], 'Crosstown Green' : [100, 125, 100], 'Fulmineous Green' : [0, 200, 125], 'Moon White Note' : [215, 245, 255], 'Lemonade Jade' : [85, 255, 190], 'Colletto Fava' : [60, 220, 0], 'Audiovisual Jade' : [0, 170, 105], 'Xerotic Violet' : [115, 70, 145], 'Consoled Gold' : [220, 170, 30], 'Reluctant Purple' : [200, 150, 255], 'Paroled Gold' : [255, 220, 0], "Florence Y'all" : [60, 200, 0], 'Lackadaisical Tan' : [215, 195, 170], 'Oversold Gold' : [255, 220, 100], 'Beluga Blue' : [120, 145, 250], 'Gazebo Green' : [125, 150, 125], 'Common Gold' : [210, 175, 55], 'Slubberdegullion Green' : [50, 235, 0], 'Pail of Milk' : [245, 215, 220], 'Piltdown Tan' : [125, 115, 70], 'Ferdinand Cheval' : [80, 180, 80], 'Lockjaw White' : [240, 245, 255], 'Parsimonious Pink' : [245, 235, 210], 'Sharkey Green' : [10, 235, 0], 'Bucolic Tan' : [150, 150, 80], 'Rented Unguents Aqua' : [215, 255, 255], 'Gatemouth Green' : [30, 230, 0], 'Company Tan' : [150, 140, 80], 'Moon on the Rise' : [110, 145, 110], 'Epithetic Grey' : [110, 135, 110], 'Coolhand White' : [240, 250, 255], 'Dagen H' : [95, 160, 0], 'Neanderthal Tan' : [145, 130, 80], 'Liquid Green' : [80, 145, 80], 'Cocksure Green' : [100, 150, 100], 'Eyes Rolled Back Grey' : [220, 240, 220], 'Sunnyland Green' : [60, 225, 0], 'By The Grey' : [230, 235, 230], 'Rise up from the River' : [30, 60, 30], 'Smithereen Green' : [0, 175, 0], 'Asinine Grey' : [170, 190, 170], 'All the Grey' : [205, 225, 205], 'Blue Note' : [30, 50, 70], 'Out of the Blue' : [25, 45, 75], 'Deep Blue' : [20, 40, 80], 'Wild Blue Yonder' : [10, 30, 85], 'Blue Moon' : [40, 70, 90], 'Blue Streak' : [0, 15, 110], 'Patch of Blue' : [40, 60, 105], 'Blue Iguana' : [0, 20, 95], 'Blue Haven' : [25, 40, 65], 'Blue Sierra' : [15, 40, 60], 'Blue Mountain' : [10, 30, 55], 'Cinerary Green' : [60, 120, 85], 'Break of Grey' : [205, 230, 210], 'Too Many Feet Grey' : [210, 230, 210], 'Mean Solar Grey' : [220, 220, 220], 'Genethliac Green' : [155, 200, 155], 'Every Which Grey' : [200, 225, 210], 'The Avi Waksberg Experience' : [0, 255, 215], 'Kentucky Wonder Green' : [80, 255, 0], 'Papilionaceous Orange' : [225, 180, 70], 'Mountweazel' : [20, 230, 0], 'Fraudulent Cream' : [255, 255, 210], 'Merry-go-round Horse Purple' : [245, 110, 190], 'Half-Pint White' : [245, 240, 255], 'Indelible Pink' : [255, 90, 170], 'Hollow Cane Blue' : [70, 90, 145], 'The Red Mass Ecstatic': [165, 15, 0], 'Twofold Gold': [210, 250, 0], 'Son of Monkdor Blue' : [0, 0, 115], 'Yellow Cello' : [250, 255, 75], 'Pendent Green' : [15, 165, 0], 'Courgette Cyan': [0, 115, 115], 'Last of the Ashes Lavender' : [225, 200, 220], 'Chinwag Purple': [105, 35, 115], 'Home Blue' : [0, 110, 130], 'Bunky Green' : [70, 220, 0], 'Heavy Metal Umlaut' : [30, 240, 0], 'Shifty Green' : [125, 255, 125], 'Bridgewater White' : [215, 250, 240], 'Whole Wheat Red' : [170, 0, 0], 'Judicial Miscarriage Yellow' : [255, 255, 125], 'Fire on the Ganges Orange': [255, 95, 0], 'Space Cowboy Green' : [90, 220, 0], 'Stood in the Road' : [105, 110, 105], 'Fat Man' : [60, 90, 60], 'Underhand Purple' : [80, 5, 80], 'Degenerate Backwater Green' : [0, 255, 120], 'Duplicitous Violet' : [70, 5, 90], 'Toots Mondello' : [85, 215, 0], 'White Lie': [220, 225, 215], 'Guileful Blue' : [0, 15, 120], 'Black Wavy Mane' : [0, 0, 0], 'Indian Heart': [255, 120, 0], 'Iceberg White': [215, 225, 220], 'Apple Shine' : [220, 255, 210], 'Fortnight Grey': [195, 220, 200], 'Smokestack Grey' : [190, 210, 190], 'Gormless Grey': [180, 200, 180], 'Loaf of Red' : [250, 120, 100], 'Bumble Bee White' : [240, 255, 245], 'Doctor Dawn' : [255, 230, 235], 'Sea of Cyan': [125, 250, 250], 'Bukka White' : [240, 255, 250], 'Mercy of the World' : [135, 150, 135], 'Blue Million Miles' : [195, 230, 255], 'Hundreds and Thousands': [145, 135, 185], 'Queen of the White' : [250, 255, 250], 'Bird Beak Grey' : [205, 240, 205], 'Peg Leg Green' : [20, 210, 0], 'Bucktooth White' : [245, 255, 240], 'Regression Toward the Green' : [75, 255, 75], 'Capital of Cyan' : [170, 255, 255], 'See the Sea Blue' : [180, 235, 250], 'Kat Man Blue' : [0, 175, 250], 'The Living Red' : [255, 40, 0], 'Jobsworth Yellow': [240, 255, 55], 'Deja Blue' : [0, 120, 250], 'Unmarked Van' : [40, 80, 40], 'Angle of Blue' : [75, 0, 245], 'Strawwood Claw Cyan' : [225, 235, 255], 'You Will Not Defeat Son of Monkdor Blue' : [0, 80, 255], 'Kerfuffle Pink': [240, 130, 110], 'Epoxy Blue' : [0, 40, 245], 'Forever and a Grey' : [210, 210, 210], 'Pink Anderson' : [245, 210, 210], 'Purple Hurple' : [245, 0, 240], 'Orange Lozenge' : [235, 100, 0], 'Mortal Clink Green' : [165, 195, 165], 'Hollow of Your Bourgeois Soul Orange' : [255, 150, 0], 'Bish Bash Bosh' : [125, 200, 135], 'Sky Turned White' : [250, 255, 255], 'Drinks The Blue Sky' : [220, 230, 245], 'Yaphet Kotto': [40, 255, 40], 'White Tie' : [255, 245, 255], 'Ten Gallon White' : [255, 250, 255], 'Salt Diamond Green' : [190, 250, 235], 'Smokey Hog White' : [250, 255, 240], "I Don't Recognise Myself" : [170, 185, 170], 'Downhome Legal Practice Grey': [150, 170, 150], 'Trocadero Green' : [45, 205, 0], 'Listen to the Ocean Blue' : [150, 220, 245], 'Golden Calf' : [235, 255, 195], 'Worn Machine Green' : [160, 190, 160], 'Santa Cruz Parliament Green' : [210, 255, 210], 'Brolly Grey': [140, 160, 140], 'Three Beaks Grey' : [130, 150, 130], 'Boffin Grey': [120, 140, 120], 'White Hat' : [245, 250, 245], 'Soviet-Era Apartment Grey' : [185, 185, 185], 'Green Gartside' : [40, 180, 20], 'Alan Greenspan' : [90, 175, 70], 'Short Pants Romance' : [160, 185, 160], 'Zane Grey' : [215, 235, 215], 'Sir Samuel White Baker' : [225, 245, 225], 'Alfred North Whitehead' : [250, 245, 240], 'Enter, The Shlubber' : [155, 180, 155], 'Whitey Herzog' : [250, 250, 240], 'Shoeless Green' : [130, 170, 110], 'Rainwater Grey' : [175, 185, 175], 'Purple Estoppel' : [90, 20, 105], 'The Grey Mass Ecstatic' : [210, 215, 210], 'Monte Blue' : [80, 160, 200], 'Touch the Sky' : [185, 200, 185], 'Orson Welles White' : [235, 250, 235], 'Proudhon Green' : [130, 155, 110], 'Adamite Green' : [235, 255, 235], 'Bobbins Green' : [220, 255, 55], 'Fire Piano Pink' : [255, 230, 220], 'Telephone Wire Grey' : [60, 65, 60], 'Cordwainer White' : [240, 245, 240], 'Watch Them Clamber, These Swift Monkeys Green': [180, 250, 180], 'Train Smoke Grey' : [165, 175, 165], 'Kropotkin Green' : [40, 150, 40], 'Bunny Suit White' : [250, 255, 245], 'Tecumseh Green' : [90, 145, 70], 'Smear of Gold' : [190, 255, 0], 'Martin County Sludge Spill' : [120, 235, 220], 'Pinochet White' : [250, 245, 255], 'Let No Man Stand Against Me Violet' : [180, 0, 255], 'White Knuckle' : [240, 240, 255], 'Aldous Huxley Green' : [50, 140, 30], 'Bottle Full of Rain' : [115, 125, 115], 'Fills up with Steam' : [155, 165, 155], 'Dunsany Green' : [100, 135, 80], 'Grey on Grey' : [95, 100, 95], 'Beethoven Blue' : [60, 130, 195], 'Crooked Lines Grey' : [155, 160, 155], 'Yoko Ono White' : [235, 240, 230], 'Lebowski White' : [230, 235, 225], 'Mark it Zero' : [110, 125, 90], 'Boudicca Blue' : [70, 120, 185], 'Tom Baker Blue' : [80, 115, 180], 'Strike a Match for Freedom' : [130, 155, 130], 'Grace Slick Green' : [90, 110, 70], 'Walls Grow Grey' : [140, 150, 140], 'Green Eternity' : [115, 150, 115], 'Dapple Grey' : [90, 105, 90], 'Green Iniquity' : [70, 105, 70], 'Grey Drips Drop' : [95, 110, 95], 'Belisha Beacon Orange' : [235, 200, 40], 'Babbitt Purple' : [255, 80, 255], 'Orange Flange' : [255, 170, 0], 'White Lightning' : [240, 255, 240], 'Sun Shine Through Pink' : [255, 230, 210], 'Anti-flash White' : [255, 240, 240], 'Mendacious Green' : [0, 255, 125], 'Moon to a Flea Green' : [170, 255, 230], 'Behold a Pale Horse White' : [255, 255, 240], 'Ignominious Orange' : [235, 125, 125], 'Callow Yellow' : [255, 255, 170], 'Argy-bargy Grey': [110, 130, 110], 'Whitewash' : [235, 240, 235], 'The Late Autumn of 1975' : [255, 135, 255], 'Polyester Green' : [135, 160, 135], 'Stanley Kubrick Grey' : [95, 105, 95], 'Laszlo Benedek' : [50, 110, 50], 'Rings of Smoke' : [90, 115, 90], 'Dashiell Hammett' : [80, 175, 80], 'Sydney Greenstreet' : [110, 170, 110], 'Asphalt Jungle' : [135, 165, 135], 'Peter Lorre White' : [245, 245, 245], 'Sterling Hayden' : [105, 165, 105], 'Gabardine Green' : [135, 155, 135], 'Shindig White' : [250, 250, 250], 'Moon Fill the Sky Purple' : [240, 180, 255], 'Acataleptic Green' : [165, 190, 165], 'Sasquatch': [195, 215, 0], 'White Flag' : [220, 245, 230], 'Whiteness of the Whale' : [245, 245, 255], 'Ragwort White' : [255, 255, 245], 'Adeciduate Green' : [95, 120, 95], 'White Elephant' : [210, 245, 230], 'Aeneous Green' : [115, 140, 115], 'Ctenoid Red' : [175, 75, 65], 'Diamond Back Grey' : [105, 120, 100], 'Schwa Aqua' : [75, 255, 255], 'Anallagmatic Grey' : [160, 175, 160], 'Pomaceous Green' : [220, 255, 200], 'Captain Grey Feather' : [185, 195, 185], 'Stirrupped in Syrup Blue' : [110, 220, 255], 'Talking Backwards' : [185, 190, 185], 'Amphetamine Stare' : [255, 245, 250], 'Archecentric Grey' : [215, 225, 215], 'Qiyas Blue' : [40, 10, 100], 'Walking in Neutral Grey' : [215, 215, 215], 'Indian Dream Green' : [190, 235, 215], 'Tiger Moon Pink' : [255, 200, 190], 'Margaric Pink' : [255, 145, 255], 'Bathybic Green' : [120, 160, 140], 'Derecho Grey' : [80, 95, 80], 'Twelfth Blue' : [0, 180, 180], 'Binotonous Grey' : [175, 180, 175], 'Monsoon Grey' : [120, 130, 120], 'Suede Jade' : [0, 80, 0], 'Hulla Blue': [0, 0, 180], 'Flat-foot White' : [255, 250, 245], 'Cacodoxical Grey' : [230, 240, 230], 'Staircase Red' : [180, 0, 0], 'Cynosural Grey' : [170, 180, 170], 'Beak of Solid Green' : [0, 180, 0], 'Light in the Tunnel Grey' : [150, 160, 150], 'Decrescent Grey' : [225, 235, 225], 'Bamboozled' : [175, 190, 175], 'Khaki Sweatband' : [140, 180, 100], 'Scrap Iron Grey' : [140, 155, 140], 'Dithyrambic Grey' : [170, 175, 170], 'Vitreous Aqua' : [0, 180, 255], 'Terpsichorean Cyan' : [160, 220, 215], 'Chain Link Fence Grey' : [175, 180, 170], 'Ebeneous Black' : [0, 35, 10], 'Haphazard Grey' : [140, 145, 140], 'Bucket of Tar' : [10, 45, 15], 'Overenthusiastic Green': [150, 255, 50], "Don't Get Trunky" : [180, 185, 180], 'Engender Lavender' : [255, 170, 255], 'Naked at the Bottom Grey' : [190, 200, 190], 'Railroad Rail Grey' : [105, 120, 105], 'Extrorse Grey' : [220, 230, 220], 'Lariat Grey' : [200, 210, 200], 'Oneiric Green' : [0, 75, 65], 'Raining Real Hard' : [75, 90, 75], 'Huddled in the Hollows' : [65, 70, 65], 'Blow the Sky off the Mountains' : [120, 150, 120], 'Through the Fog' : [110, 125, 110], 'Pale as Chalk' : [220, 235, 220], 'Gin-soaked Grey' : [215, 220, 215], 'Charcoal Eyes' : [90, 100, 90], 'Buck Shot Eyes Pink' : [255, 150, 150], 'Glass Eye Grey': [180, 190, 180], 'Shady Blue' : [0, 130, 205], 'Heaven or Home' : [135, 140, 135], 'Abode of God' : [90, 120, 90], 'Fuming Beaker' : [115, 135, 115], 'Candy Stripe Green' : [200, 255, 50], 'A Means To Our Own Excellence Cyan' : [0, 130, 125], 'Messianic Green' : [80, 120, 80], 'Big Blue' : [125, 130, 240], 'Nothing Looks the Same' : [105, 130, 105], 'Burnt-out Blue' : [95, 115, 220], 'The Moon Green' : [95, 125, 95], 'Mean Black Swan' : [5, 35, 10], 'Barroom Grey' : [80, 85, 80], 'Blow out the Sun' : [85, 120, 85], 'Sliver of Green' : [85, 115, 85], 'Pepper Tree Green' : [160, 215, 160], "I Equal Jesus" : [50, 65, 50], 'Mojave Grey' : [170, 190, 175], "White Man's Burden" : [235, 245, 235], 'White Water' : [230, 245, 230], 'White Buffalo' : [225, 240, 225], 'White Rush' : [220, 235, 230], 'Whitespace' : [215, 230, 225], 'White Star' : [240, 250, 245], 'White Pants' : [245, 250, 240], 'China White' : [235, 245, 240], 'Bayou Green' : [165, 185, 165], 'Grover Cleveland Green' : [160, 180, 160], 'Millard Fillmore' : [155, 195, 155], 'White Fever' : [235, 250, 240], 'White Line' : [240, 245, 235], 'White Panic' : [240, 250, 235], 'White Oak' : [225, 235, 230], 'White Elk' : [225, 240, 235], 'White City' : [225, 245, 230], 'White Australia' : [225, 255, 230], 'White Justice' : [230, 240, 225], 'White Heron' : [230, 245, 225], 'White King' : [230, 250, 225], 'White Reindeer' : [230, 255, 225], 'White Ensign' : [220, 230, 225], 'White Light' : [225, 230, 220], 'Martin Van Buren' : [145, 170, 145], 'I Have no Shame' : [85, 110, 85], 'Gamaliel Grey' : [150, 165, 150], 'Petrichor Grey' : [195, 200, 195], 'Peppermint Kite' : [150, 255, 130], 'Grey Weather' : [200, 205, 200], 'Clysmian Blue' : [15, 10, 110], 'Vigilante Grey' : [210, 220, 210], 'Feldgrau' : [75, 95, 85], 'Brumous Cyan' : [145, 255, 255], 'Watch and Chain Grey' : [90, 95, 90], "The God Within Me" : [175, 200, 175], 'Hydrophanous Grey' : [165, 170, 165], 'Hyetal Green' : [40, 120, 40], 'Aeolian Blue' : [125, 135, 205], 'Engine House Grey' : [85, 90, 85], 'Stormy Cyan' : [0, 150, 255], 'God on the Mountain Green' : [110, 150, 110], 'Idiomorphic Grey' : [205, 215, 205], 'Honey Wine' : [255, 70, 150], 'Burnt Andy' : [125, 255, 255], 'Venal Aqua' : [110, 255, 250], 'Blue Horizon' : [20, 40, 135], 'Blue Comet' : [30, 90, 140], 'Stretched out Alone' : [175, 195, 175], 'Close to Heaven' : [120, 145, 120], 'Blue Clay' : [40, 80, 130], 'Blue Moses' : [5, 20, 85], 'Robots Look Blue' : [5, 15, 80], 'Byzantine Blue' : [0, 5, 90], 'Blue Danube' : [5, 10, 95], 'Filled with Doubt Grey' : [90, 110, 90], 'Kedogenous Green' : [200, 240, 200], 'Isolation Psychosis Green' : [125, 255, 0], 'Seven Extra Eyes' : [100, 255, 100], 'Ku Klux Tan' : [125, 130, 0], 'Cottonwood Green' : [75, 100, 75], 'Kerygmatic Grey' : [165, 180, 165], 'Irksome Red' : [85, 10, 0], 'Medicine Chest Grey' : [70, 90, 70], 'Labile Grey' : [200, 215, 200], 'Bullet Proof Smile' : [125, 0, 255], 'Sea of Grey' : [105, 115, 105], 'Grey Heap of Stone' : [115, 120, 115], 'Bonnet Blanc et Blanc Bonnet' : [235, 250, 245], 'Grey in Vain' : [110, 120, 110], 'Ericaceous Green' : [85, 100, 75], 'Wet as the Sea Blue' : [70, 110, 215], 'Fire in the Air of Now Red' : [250, 80, 0], 'Lutulent Grey' : [145, 160, 145], 'Wagon of Rain Grey' : [70, 75, 70], 'The Blue Mass Ecstatic' : [110, 110, 255], 'Powder Blue Night' : [90, 130, 255], 'Sinistral Yellow' : [205, 230, 80], 'Numbskull Grey' : [60, 80, 60], 'Grey Eminence' : [195, 205, 195], 'Malleiform Grey' : [205, 210, 205], 'Green McQueen' : [170, 255, 0], 'Aluminium Rhythm Grey' : [125, 125, 140], 'Almond Eye' : [50, 70, 50], 'Multivious Grey' : [145, 155, 145], 'Grey Downpour' : [110, 125, 115], 'The Hot Front Part of my Head Orange' : [255, 140, 0], 'Heavy Rains Grey' : [40, 60, 40], 'Rhinestone' : [200, 200, 255], 'Smoked Him Out' : [30, 50, 30], 'Nemoral Green' : [145, 205, 145], 'Inside Black' : [5, 30, 10], 'Parole Officer Grey' : [190, 195, 190], 'Strigine Blue' : [50, 125, 160], 'Blue Murder' : [130, 170, 220], 'Obvallate Grey' : [145, 150, 145], 'Pluvial Blue' : [0, 0, 100], 'Otiant Grey' : [185, 200, 190], 'Hypnoid Green' : [150, 255, 0], 'Ramiferous Red' : [80, 0, 0], 'Obstinate Violet' : [160, 0, 255], 'Grey Fedora' : [125, 140, 125], 'Palladian Grey' : [130, 145, 130], 'No Blame Grey' : [165, 175, 170], 'Querulent Grey' : [195, 210, 195], 'Admiral of the Red' : [255, 0, 75], 'Farouche Grey' : [210, 225, 210], 'Passerine Blue' : [40, 60, 120], 'Quisguous Grey' : [130, 140, 130], 'Scurrilous Grey' : [190, 215, 190], 'Jello Biafra' : [170, 195, 170], 'Higgledy-piggledy Grey' : [160, 165, 160], 'Crepuscular Green' : [150, 205, 45], 'Watch the Horizon Red' : [250, 90, 0], 'Ravissant Grey' : [180, 195, 180], 'Beneath the Symbol Cyan' : [240, 255, 255], 'Rufous White' : [255, 250, 250], 'Fulgurant Yellow' : [240, 255, 0], 'Saliferous White' : [255, 255, 250], 'Blue Wine' : [50, 70, 225], 'Sixes and Sevens' : [220, 250, 220], 'Tonitruous White' : [250, 250, 255], 'Wounded Eyes Blue' : [70, 90, 230], 'Ultrafidian White' : [245, 255, 245], 'Rain on the Hill Grey' : [40, 50, 40], 'Velutinous White' : [245, 255, 250], 'Galvanic Yellow' : [240, 255, 65], 'Widdershins White' : [245, 255, 255], 'Auctorial Blue' : [10, 110, 115], 'Rainy Hammer Grey' : [60, 70, 60], 'Xyresic White' : [245, 250, 255], 'Wind in the Meadow Green' : [210, 240, 210], 'Gracile Grey' : [205, 220, 205], 'Chiropteran Blue' : [50, 70, 90], 'Turn of the Moon' : [200, 230, 200], 'Thunder Groaned Grey' : [185, 185, 180], 'Heliacal Yellow' : [240, 240, 125], 'Rain Shower Grey' : [80, 90, 80], 'Drag Strip Courage Blue' : [70, 110, 170], 'Quake and Roll Grey' : [30, 40, 30], 'Pipeline Green' : [160, 210, 160], 'Roll and Moan Grey' : [100, 110, 100], 'Walter Sobchak Blue' : [120, 140, 185], 'Cold Grey' : [115, 120, 110], 'Broken Cup Grey' : [180, 200, 185], 'Drunken Wail Grey' : [55, 60, 50], 'Sofa Red' : [180, 10, 50], 'Muddy Rain Grey' : [125, 130, 120], 'Wooden Coat' : [180, 150, 120], "Blind Man's Cane Grey" : [125, 140, 130], 'Intemperate Orange' : [235, 180, 100], 'Tulip Wine Orange' : [190, 150, 110], 'Parenthetic Blue' : [180, 210, 235], 'Hammer to the Floor Grey' : [150, 155, 150], 'Philippic Cyan' : [120, 220, 235], 'Cane Break Orange' : [200, 150, 100], 'Rodomontade Green' : [195, 225, 175], 'Fire and the Fury Red' : [255, 110, 0], "I Can't Believe Green" : [105, 255, 125], 'Petulant Red' : [155, 50, 55], 'Lighthouse Beacon Purple' : [150, 100, 135], 'Violet Volt' : [115, 75, 180], 'Ace of Love Green' : [195, 240, 125], 'The Gold Cloth Madonna' : [255, 160, 45], 'Mathematastic Yellow' : [245, 195, 0], 'Bulbous Green' : [135, 170, 55], 'Magnesium Kadabra Red' : [180, 45, 40], 'Tire Swing Grey' : [145, 150, 140], "Sun's Eye Orange" : [235, 120, 30], 'Ribbon in the Willow Green' : [50, 255, 30], 'Two Shadows At Noon' : [175, 95, 130], 'Weathervane Grey' : [170, 170, 170], 'Feet of Dust Aqua' : [30, 65, 60], 'Creek Bed Green' : [150, 255, 110], 'Shatter The Noon Yellow' : [240, 255, 175], 'Bonzai Calypso Green' : [65, 90, 60], 'Machine Gun Haste' : [15, 45, 160], 'Steeple Full of Swallows Green' : [85, 145, 25], 'Marimba Grey' : [160, 160, 160], 'Dream in the Straw Indigo' : [35, 10, 65], 'Hole In The Sky Green' : [145, 215, 180], 'Skew-whiff Grey' : [110, 125, 120], 'Sly Grin' : [75, 85, 40], 'Obnoxious Tan' : [95, 95, 55], 'Chutzpah Brown' : [115, 75, 45], 'Bowl Full of Stars Black' : [15, 5, 50], 'Shamshiel Guards the Gates of Eden Blue' : [0, 0, 255], 'Smokers Tooth' :  [255, 255, 0], 'Pipes Burn White' : [255, 255, 255], 'Furtive Yellow' : [230, 250, 100], 'The Cyan Mass Ecstatic' : [0, 255, 255], "Hollow of your Bourgeois Soul Red" : [135, 50, 85], 'Dust Bowl Orange' : [255, 130, 0], 'Painless Blue' : [180, 210, 240], "The South Will Not Rise Again Green" : [160, 220, 140], 'Ventripotent Tan' : [210, 215, 150], 'Recently Decriminalised Yellow' : [250, 210, 150], "Mangosteen Green" : [0, 90, 25], 'Whoa Doggie! Purple' : [150, 95, 135], "Satan's Nutsack Green" : [165, 205, 10], 'Thelemic Tan' : [225, 190, 110], 'Tried and Blue' : [150, 235, 250], 'Eurotrash Blue' : [0, 120, 165], 'Bible and a Rope Burgundy' : [230, 40, 100], 'Shamshiel Guards the Gates of Eden Pink' : [255, 210, 185], 'Sad Luck Green' : [55, 80, 55], 'Sweet Binkey' : [200, 200, 200], 'Sad Little Man Green' : [80, 170, 60], 'Can I Have An Orange' : [180, 80, 20], 'Pyknic Red' : [220, 90, 55], 'Blue Cloudburst' : [95, 145, 160], 'Perfidious Purple' : [100, 35, 110], 'Free As In Beer Green' : [105, 165, 20], 'BSoD Blue' : [0, 60, 100], 'Buckteeth Yellow' : [255, 210, 60], 'Routine Green' : [40, 155, 130], 'Quagmire of Mediocrity Grey' : [110, 115, 110], 'Ginglyform Black' : [0, 40, 0], 'Vagabond' : [30, 195, 195], 'Proletarian Blue' : [40, 105, 150], 'Fuscoferuginous Red' : [215, 75, 115], 'The Orange Mass Ecstatic' : [210, 125, 20], 'Plutocracy Grey' : [105, 130, 100], 'Concilliabule Pink' : [200, 115, 105], 'Bent Wookie Brown' : [60, 45, 30], 'Lapidary Indigo' : [170, 145, 205], 'Nudiustertain Green' : [100, 180, 145], 'Brontide Brown' : [125, 130, 100], 'Hobo Purple' : [80, 40, 90], 'They Lack Nothing But Power Grey' : [120, 125, 120], 'Algerining Orange' : [240, 160, 5], 'Cornfield Green' : [70, 110, 70], }
    continuationsFilename = '.\\continuations.pkl'
    preferredFirstColour  = ('Bright Goddamn Red', [255, 0, 0])
    minimumFirstDistance  = 10000


    def __init__(self, background=None):
        """ You may initialise ColourManager with an (optional) background 
        colour (use either a red-green-blue tuple or a Colour() object). When 
        handing out colours, the ColourManager will include the background 
        colour (if any) among the set of those to which it tries to maximize 
        the contrast of the new colour. For many purposes, it's useful to 
        initialise the colour manager with background=[0, 0, 0] (black).
        
        self.colourDict holds a dictionary containing the names (as keys) and
        red-green-blue tuples (as values) of the available colours. As the
        ColourManager hands out colours, it deletes the entries matching their
        names from self.colourDict. 
        
        self.removedValues holds a list of the red-green-blue tuples already
        handed out plus the red-green-blue tuple of the background colour (if
        any). 
        """
        
        self.background    = background
        self.colourDict    = copy.copy(ColourManager.colourDictionary)
        self.firstColour   = True
        self.continuations = ColourManager._loadContinuations()
        if self.background is None:
            self.removedValues = []
        else:
            if isinstance(background, Colour):
                self.background = background.colourvalues
            else:
                self.background = list(background)
            self.removedValues = [self.background]            


    def nextColour(self):
        """ Hands out (returns) a single colour as a Colour() object.
        Removes it from self.colourDict and adds its red-green-blue
        tuple to self.removedValues.
        
        If you need more than one colour at a time, calling 
        self.colourList instead will usually give colours with better 
        contrast than calling nextColour() multiple times (because it
        can take advantage of the fact that you know how many new
        colours you need from the outset).
        """
    
        if len(self.colourDict) == 0:
            return False
        if self.firstColour:
            self.firstColour = False
            if self.background is None or ColourManager._findDifference(self.background, ColourManager.preferredFirstColour[1]) >= ColourManager.minimumFirstDistance:           
                return Colour(self, *ColourManager.preferredFirstColour)     
        return Colour(self, *reduce(self._leastPair, self.colourDict.items(), (-1, None))[1])


    def colourList(self, numberOfColours):
        """ Hands out (returns) a list containing the specified number of 
        colours as Colour() objects.
        Removes each one from self.colourDict and adds its red-green-blue
        tuple to self.removedValues.
        
        If you need more than one colour, colourList will usually give
        colours with better contrast than calling nextColour() multiple 
        times (because it can take advantage of the fact that you know 
        how many new colours you need from the outset).
        """
        
        if numberOfColours < 1 or len(self.colourDict) == 0:
            return []
        if numberOfColours == 1:
            return [self.nextColour()] 
        removeList = [tuple(removedVal) for removedVal in self.removedValues]
        removeList.sort()
        removedTuples = tuple(removeList)
        key           = (removedTuples, numberOfColours)
        if self.continuations.has_key(key):
            return [Colour(self, *redGreenBlue) for redGreenBlue in self.continuations[key]]
        closestMatches = Cube().findPositions(numberOfBodies=numberOfColours, forceRandomStartingPositions=False, fixedPositions=removedTuples, sieve=lambda x: not x.frozen)
        if self.background in closestMatches:
            closestMatches.remove(self.background)
        self.continuations[key] = [self.findClosestMatch(*elements) for elements in closestMatches]
        continuationsFile       = open(ColourManager.continuationsFilename, 'wb')
        dump(self.continuations, continuationsFile)
        continuationsFile.close()
        if self.firstColour:
            self.firstColour = False
        return [Colour(self, *redGreenBlue) for redGreenBlue in self.continuations[key]]  


    def findClashes():
        """ Static method. Returns a dictionary containing any colours in 
        ColourManager.colourDictionary with duplicated red-green-blue
        tuples. The returned dictionary's keys are the red-green-blue 
        tuples that appear more than once. The corresponding values are
        lists of the names of those colours.
        """
        
        clashes   = {}
        namesdict = {}
        [ColourManager._testForClash(colourname, tuple(colour), namesdict, clashes) for colourname, colour in ColourManager.colourDictionary.items()]
        return clashes


    def findClosestMatch(self, red, green, blue):
        """ Returns the colour in self.colourDict whose red-green-blue
        tuple is nearest to [red, green, blue].
        
        If self.colourDict is empty, returns False.
        """
        
        if len(self.colourDict) == 0:
            return False
        return reduce(ColourManager._nearest([red, green, blue]), self.colourDict.items(), (maxint, None, None))[1:]


    def printColours(self):
        """ Calls self.nextColour() over-and-over, printing their names,
        until self.colourDict is empty.
        
        Usually used only for debugging.
        """
        printedColours = []
        while len(self.colourDict) > 0:
            nextCol = self.nextColour()
            printedColours.append(nextCol)
            print nextCol          


    def drawColourSamples(canvas, sampleStamp, imprint, fontClass, fontArguments={}, canvasSetup=lambda : None, canvasFinish=lambda : None, margin=2.0, sizeOfSampleSquares=130.0, spaceBetweenSamples=20.0, minimumNonZeroComponentDifference=5.0, firstTextOffset=30.0, textOffsetMargin=50.0):
        """ Static method. Draws a chart with all the colours from 
        ColourManager.colourDictionary.   
        """ 

        assert ColourManager.findClashes() == {}
        canvasSetup()
        cells                      = {}
        labelFont                  = fontClass(**fontArguments)
        canvasSize                 = min(canvas.get_height(), canvas.get_width())
        marginInPixels             = margin * sizeOfSampleSquares
        boxMargin                  = (marginInPixels / 2.0) + textOffsetMargin
        sizeOfCanvasMinusMargins   = canvasSize - marginInPixels
        distanceFromSampleToSample = sizeOfSampleSquares + spaceBetweenSamples
        sizeOfBoxLine              = sizeOfSampleSquares * distanceFromSampleToSample
        pixelsPerComponent         = sizeOfSampleSquares / minimumNonZeroComponentDifference
        [ColourManager._drawSingleSample(canvas, colourName, red, green, blue, cells, imprint, sizeOfSampleSquares, firstTextOffset, sizeOfBoxLine, boxMargin, pixelsPerComponent, sampleStamp, labelFont) for colourName, (red, green, blue) in ColourManager.colourDictionary.items()]
        canvasFinish()                 


    def _drawSingleSample(canvas, colourName, red, green, blue, cells, imprint, sizeOfSampleSquares, firstTextOffset, sizeOfBoxLine, boxMargin, pixelsPerComponent, sampleStamp, labelFont):
        """ Static method. Draws a single colour on to canvas. 
        Called by ColourManager.drawColourSamples  
        """ 
        
        if cells.has_key((red, green),):
            cells[(red, green)] += 1
        else:
            cells[(red, green)] = 1
        offset  = (cells[(red, green)] - 1) * sizeOfSampleSquares
        boxsize = int(sizeOfBoxLine / (2.0 * sizeOfSampleSquares + offset))
        if cells[(red, green)] == 1:
            textOffset = -firstTextOffset
        else:
            textOffset = boxsize
        boxX        = boxMargin + (red * pixelsPerComponent)
        boxY        = boxMargin + (green * pixelsPerComponent) + offset
        textSurface = labelFont.render(colourName, True, [255, 255, 255])
        textdepth   = textSurface.get_height()
        textlength  = textSurface.get_width()
        sampleStamp(canvas, (red, green, blue), [boxX, boxY, boxsize, boxsize])
        if hasattr(canvas, imprint):
            getattr(canvas, imprint)(textSurface, (boxX, boxY + textOffset))    


    def _testForClash(colourname, colourtuple, namesdict, clashes):
        """ Static method. Helps to check for duplicated red-green-blue tuples in
        ColourManager.colourDictionary. Checks to see if namesdict already contains
        colourtuple as a key. If it does, adds colourname and colourtuple to clashes.
        If it doesn't, adds colourtuple to namesdict.
        """    
    
        if colourtuple in namesdict.keys():
            if clashes.has_key(colourtuple):
                clashes[colourtuple].append(colourname)
            else:
                clashes[colourtuple] = [namesdict[colourtuple], colourname]
        else:
            namesdict[colourtuple] = colourname


    def _findDifference(firstColour, secondColour):
        """ Static method. Returns the square of the euclidian distance in the
        red-green-blue colourspace between firstColour and secondColour.
        """      
    
        return sum([(firstColourElement - secondColourElement) ** 2 for firstColourElement, secondColourElement in zip(firstColour, secondColour)])


    def _leastPair(self, existingPair, (colourname, colour)):
        """ Compares colour to each of the red-green-blue tuples in 
        self.removedValues. If the square of the distance between colour
        and the closest red-green-blue tuple in self.removedValues is
        greater than the first element of existingPair, returns a new
        tuple comprising that square of the distance followed by colourname
        and colour. If it isn't, returns existingPair instead.
        """
        
        mindifference = reduce(ColourManager._leastChange(colour), self.removedValues, maxint)
        if mindifference > existingPair[0]:
            return (mindifference, [colourname, colour])
        return existingPair


    def _loadContinuations():
        """ Static method. Tries to open ColourManager.continuationsFilename and return
        its contents as a dictionary. 
        """    
        
        try:
            continuationsFile = open(ColourManager.continuationsFilename, 'r')
            continuationsDictionary = load(continuationsFile)
            continuationsFile.close()
            return continuationsDictionary
        except IOError:
            return {}    


    def _leastChange(colour):
        """ Static method. Returns a function that tests whether the square
        of the distance in the red-green-blue colourspace between a 
        red-green-blue tuple and colour is less than a specified value. If
        it is, that function returns that square of the distance. Otherwise,
        it returns back the specified value.
        """      
    
        def leastDifference(existingminimum, existingcolour):
            """ Returns either existingminimum or the square of the distance
            between existingcolour and colour in the red-green-blue
            colourspace, whichever is less.
            """
        
            difference = ColourManager._findDifference(colour, existingcolour)
            if difference < existingminimum:
               return difference
            return existingminimum

        return leastDifference


    def _nearest(colour): 
        """ Static method. Returns a function that tests whether the square
        of the distance in the red-green-blue colourspace between a 
        red-green-blue tuple and colour is less than a specified value called
        'exisitingminimum'. If it is, that function returns a tuple comprising 
        that square of the distance, that red-green-blue tuple and a specified 
        name for it. Otherwise, it returns a tuple comprising existingminimum,
        and another specified red-green-blue tuple and name.
        """    
    
        def closerMatch((existingminimum, existingname, existingtuple), (nextname, nexttuple)):
            """ If the square of the distance between nexttuple and colour
            in the red-green-blue colourspace is less than existingminimum,
            returns a tuple comprising that square of the distance,
            nextname and nexttuple. Otherwise, returns a tuple comprising
            existingminimum, existingname and existingtuple.
            """
        
            difference = ColourManager._findDifference(colour, nexttuple)    
            if difference < existingminimum:
                return (difference, nextname, nexttuple)
            return (existingminimum, existingname, existingtuple)     
            
        return closerMatch


    _leastChange       = staticmethod(_leastChange)
    _drawSingleSample  = staticmethod(_drawSingleSample)
    _testForClash      = staticmethod(_testForClash)
    _loadContinuations = staticmethod(_loadContinuations)
    _findDifference    = staticmethod(_findDifference)
    _nearest           = staticmethod(_nearest)
    findClashes        = staticmethod(findClashes)
    drawColourSamples  = staticmethod(drawColourSamples)



class Colour(object):       
    """ Color in the red-green-blue colourspace managed by a 
    ColourManager() object.
    
    Has a name, a ColourManager() and a red-green-blue tuple of
    colour components. User can access the components as a tuple
    (self.colourvalues) or as individual elements (self.red,
    self.green and self.blue). 
    
    When something calls the __del__ method, the colour's name
    and red-green-blue tuple return to the colourDict belonging
    to the Colour's manager. The red-green-blue tuple also gets
    removed from that manager's list of removed red-green-blue
    tuples (.removedValues).   
    """
    
    def __init__(self, manager, colourname, colourvalues):
        """ Initialise Colour() with a ColourManager() object, a string
        that names the colour and a red-green-blue tuple.
        
        self.manager holds the ColourManager() that manages the Colour.
        self.colourname holds the colour's name.
        self.colourvalues holds the red-green-blue tuple of the colour's
        position in the colourspace. You can also access the components
        individually through self.red, self.green and self.blue
        """
        
        self.manager                    = manager
        self.colourname                 = colourname
        self.colourvalues               = colourvalues
        self.red, self.green, self.blue = colourvalues
        if colourvalues not in manager.removedValues:
            manager.removedValues.append(colourvalues)
        if manager.colourDict.has_key(colourname):
            del manager.colourDict[colourname]


    def __del__(self):
        """ Puts the colour's name and red-green-blue tuple back
        into the manager's colourDict and removes the 
        red-green-blue tuple from the manager's list of removed 
        values.         
        """
        
        if isinstance(self.manager, ColourManager):
            if self.colourvalues in self.manager.removedValues:
                self.manager.removedValues.remove(self.colourvalues)
            self.manager.colourDict[self.colourname] = copy.copy(self.colourvalues)


    def __str__(self):
        """ Returns just the colour's name.
        """
        
        return self.colourname
        
        
    def __repr__(self):
        """ returns a string containing the colour name and a 
        string representation of the rgb tuple.
        """
        
        return ", ".join([repr(self.manager), repr(self.colourname), repr(self.colourvalues)])



class Frame(object):
    """ Space within which Body() objects move. Used to distribute
    points through a colourspace by allowing bodies to repel one
    another until they settle into a stable arangement within the
    space.
    """

    def __init__(self, bounds=[[0.0, 255.0], [0.0, 255.0]], bounce=0.7, drag=0.02):
        """ Initialise Frame() with an object giving the bounds
        of the space (by default a list of corners), the
        proportion of speed that a body it retains when it
        reflects off the edges of the space and the proportion
        of speed that a body loses each tick due to drag.
        
        self.bounds holds the object that define's the space's
        bounds (by default, a list of conrners).
        self.bound holds the proportion of speed that a body
        retains when it reflects off the bounds
        self.drag holds the proportion of speed that a body
        loses each tick due to drag.
        self.dimensions holds the number of dimensions the space
        has.
        self.numberOfColours, self.colourScheme and 
        self.colourSpan are only used when you want to draw a
        picture of the bodies in the space. They hold the
        information about the number of graduations of colour
        used to represent positions along one of the axes and 
        the specific way the colour varies across those
        graduations.
        self.axes holds a list of numbers naming each dimension.
        Where n is the number of dimension, it equals: [0, 1, 2,
        ..., n-1].
        self.length holds a list of the length of the space along
        each dimension.
        self.bodyList holds a list of all the bodies in the space.
        """
        
        self.bounds          = bounds
        self.bounce          = bounce
        self.drag            = drag
        self.dimensions      = self.__class__.dimensions
        self.numberOfColours = self.__class__.numberOfColours
        self.colourScheme    = self.__class__.colourScheme
        self.colourSpan      = Span(self.numberOfColours)
        self.axes            = range(0, self.dimensions)
        self.length          = [self.bounds[axis][1] - self.bounds[axis][0] for axis in self.axes]
        self.bodyList        = []
        
        
    def distancesquare(self, origin, destination):
        """ Returns the square of the euclidian distance between
        origin and destination. Origin and destination should be
        tuples with the same number of members as self.axes.
        """
        
        originCoordinates      = self._getCoordinates(origin)
        destinationCoordinates = self._getCoordinates(destination)
        displacement           = [originCoordinates[axis] - destinationCoordinates[axis] for axis in self.axes]
        return [sum([displacement[axis] * displacement[axis] for axis in self.axes]), []]
    
    
    def direction(self, origin, destination, squares=[]):
        """ Returns a list of the differences between the position
        of origin and destination along each axis. Origin and 
        destination should be tuples with the same number of
        members as self.axes. 
        """
        
        return [origin.position[axis] - destination.position[axis] for axis in self.axes]
    
    
    def inside(self, coordinates):
        """ Returns True if coordinates lie inside the bounds of
        the space. 
        Otherwise, returns False.
        """
    
        return reduce(bool.__and__, [(coordinates[axis] >= self.bounds[axis][0]) and (coordinates[axis] <= self.bounds[axis][1]) for axis in self.axes])
    
    
    def mapPositionFromFlat(self, flatPosition):
        """ If flatPosition lies within the bounds of the space,
        returns flatPosition. Otherwise, returns a tuple
        containing, for each axis: the position of flatPosition
        along that axis if it lies within the bounds for that axis,
        the lower bound for that axis if flatPosition lies below it
        or the upper bound for that axis if floatPosition lies
        above it.
        """
    
        return [max(self.bounds[axis][0], min(self.bounds[axis][1], flatPosition[axis])) for axis in self.axes]


    def mapVelocityFromFlat(self, flatVelocity, flatPosition):
        """ Returns a new velocity vector obtained by applying the drag
        and any change due to bouncing off the space's bounds.
        """
    
        projected    = [flatPosition[axis] + flatVelocity[axis] for axis in self.axes]               
        withoutDrag  = [self._reflect(projected[axis], flatVelocity[axis], self.bounds[axis]) for axis in self.axes]          
        oneMinusDrag = 1.0 - self.drag       
        return [withoutDrag[axis] * oneMinusDrag for axis in self.axes]


    def _drawBounds(self, displaySurface, stamp, canvasFinish):
        """ Uses the supplied stamp and canvasFinish methods to draw all
        the points outside the Frame on to this supplied displaySurface.
        Returns the length on the supplied displaySurface of one unit in
        the Frame.
        """
        
        if displaySurface is None:
            return None
        pixelsPerUnit = self.bodyList[0].getPixelsPerUnit(displaySurface)
        heightRange   = range(0, displaySurface.get_height())
        [[self._drawOutside(displaySurface, stamp, (x, y), pixelsPerUnit) for y in heightRange] for x in range(0, displaySurface.get_width())]
        canvasFinish()
        return pixelsPerUnit
        
        
    def _drawOutside(self, displaySurface, stamp, (x, y), pixelsPerUnit):
        """ If the supplied coordinate pair (x, y) lies on the Frame,
        uses the supplied stamp method to draw it on to the supplied
        displaySurface.
        """
        
        if not self.inside([x / pixelsPerUnit[0], y / pixelsPerUnit[1]] + [(self.bounds[axis][1] - self.bounds[axis][0]) / 2.0 for axis in self.axes[2:]]):
            stamp(displaySurface, (255, 255, 0), (x, y), 0)


    def _setupClassStartingPatterns(self):
        """ If this object's class has no startingPatterns, loads them
        from the file named by the class's 'startingPatternsFilename'
        attribute.
        """
    
        if not hasattr(self.__class__, 'startingPatterns') or self.__class__.startingPatterns is None:
            self.__class__.startingPatterns = self._getStartingPatterns()


    def showStartingPatterns(self):
        """ Returns a string with coordinates for each starting position
        in each of the startingPatterns.
        
        The string contains one chunk of text for each startingPattern,
        deliminated by double newline characters (i.e. blank lines). Each
        such chunk equals the number of starting positions in that pattern
        followed by a single newline character followed by the coordinates 
        of each of those starting positions delimited by single newline
        characters.
        For example, 
        
            > newFrame = Frame()
            > print newFrame.showStartingPatterns()
            
            result:
            
            > 2
            > +0.0000, +1.0000
            > +0.0000, -1.0000
            >
            > 3
            > +0.0000, +1.0000
            > +0.8660, -0.5000
            > -0.8660, -0.5000
            >
            > 4
            > +0.0000, +1.0000
            > +1.0000, +0.0000
            > +0.0000, -1.0000
            > -1.0000, +0.0000
            >
            > [etc.]
        
        """
        
        self._setupClassStartingPatterns()
        pairs = self.__class__.startingPatterns.items()
        pairs.sort()
        return "\n\n".join(["\n".join([str(key)] + [", ".join(["%+1.4f" % coord for coord in point]) for point in value]) for key, value in pairs])


    def findPositions(self, numberOfBodies, startingAreaProportion=None, cold=0.005, cyclesToFreeze=50, startingVelocityProportion=1000.0, displaySurface=None, stamp=None, canvasFinish=None, erase=True, borderWidth=1, charge=None, forceRandomStartingPositions=False, outlength=255, fixedPositions=[], sieve=lambda x: True):
        """ Tries to space the supplied numberOfBodies quite evenly through
        the Frame. 
        
        If this object's class has a startingPattern containing the supplied
        numberOfBodies and forceRandomStartingPositions is False, starts with 
        those positions and then lets the bodies to repel one another in
        the Frame until their motion through the Frame becomes slow. 
        Otherwise, starts the bodies in random positions and lets them repel
        each other.
        
        Returns a list of the coordinates of each the resulting positions.
        
        Although I've never encountered this in practice, in principle this
        method could run for a very long time (or fail to finish at all) if
        the bodies take a very long time to slow below the threshold (or never
        slow below it at all).
        """
        
        if startingAreaProportion is None:
            startingAreaProportion = sqrt(1.0 / self.dimensions) - self.__class__.defaultStartingMargin
        startingOffset = (1.0 - startingAreaProportion) / 2.0
        self._setupClassStartingPatterns()
        if forceRandomStartingPositions or self.__class__.startingPatterns is None or not self.__class__.startingPatterns.has_key(numberOfBodies):
            self.bodyList += [Body(position=[self.length[axis] * (startingOffset + (random.random() * startingAreaProportion)) for axis in self.axes], velocity=[cold * startingVelocityProportion * (random.random() - 0.5) for axis in self.axes], acceleration=[0.0] * self.dimensions, frame=self, charge=charge) for n in range(0, numberOfBodies)]        
        else:    
            startingPositions = [[(component + 1.0) / 2.0 for component in bodyPosition] for bodyPosition in self.__class__.startingPatterns[numberOfBodies]]
            self.bodyList    += [Body(position=[self.length[axis] * (startingOffset + (startPlace * startingAreaProportion)) for axis, startPlace in enumerate(startingPositions[n])], velocity=[cold * startingVelocityProportion * (element - 0.5) for element in startingPositions[n]], acceleration=[0.0] * self.dimensions, frame=self, charge=charge) for n in range(0, numberOfBodies)]                
        self.bodyList += [Body(position=fixPos, velocity=[0.0] * self.dimensions, acceleration=[0.0] * self.dimensions, frame=self, frozen=True) for fixPos in fixedPositions]        
        pixelsPerUnit  = self._drawBounds(displaySurface, stamp, canvasFinish)          
        coldCycles     = 0
        while coldCycles < cyclesToFreeze:
            if erase and (displaySurface is not None):
                [point.eraseDot(screen, stamp, pixelsPerUnit=pixelsPerUnit, borderWidth=borderWidth) for point in self.bodyList]
            [point.repelAll(self.bodyList) for point in self.bodyList]
            [Frame._movePoint(point, displaySurface, stamp, pixelsPerUnit, borderWidth) for point in self.bodyList]
            hot = False
            for point in self.bodyList:
                speedSquare = sum([point.velocity[axis] * point.velocity[axis] for axis in self.axes])
                if speedSquare > cold:
                    hot = True
                    break
            if hot:
                coldCycles = 0
            else:
                coldCycles += 1
            if displaySurface is not None:
                canvasFinish()
        return [[int(0.5 + float(outlength) * (point.position[axis] - self.bounds[axis][0]) / self.length[axis]) for axis in self.axes] for point in self.bodyList if sieve(point)]


    def _movePoint(point, displaySurface, stamp, pixelsPerUnit, borderWidth):
        """ Moves the supplied point through the Frame according to its
        velocity (and the bounds and other properties of the Frame).
        
        If the caller supplies a displaySurface and stamp method, will use
        that stamp method to draw the new position of the point on to the
        displaySurface.
        """
        point.move()
        if displaySurface is not None:
            point.drawDot(screen, stamp, pixelsPerUnit=pixelsPerUnit, borderWidth=borderWidth)


    def _setStartingArrangementsForFrame(maximumPointsInCircle=100):    
        """ Static method. Generates startingPatterns for the good,
        old-fashioned, two-dimensional Frame class by spacing the points
        for each startingPattern evenly around the edge of a circle,
        then saves them to the file named by the good, old-fashioned,
        two-dimensional Frame class's 'startingPatternsFilename'
        attribute.
        """
        
        arrangements = {}
        [arrangements.__setitem__(pointsPerCircle, [Frame._roundCoordinates([angleFunction(2.0 * point * pi / pointsPerCircle) for angleFunction in [sin, cos]]) for point in range(0, pointsPerCircle)]) for pointsPerCircle in range(2, maximumPointsInCircle + 1)]
        Frame._saveArrangementsFile(arrangements, Frame.startingPatternsFilename)
                
                
    def _saveArrangementsFile(arrangements, filename):
        """ Static method. Saves the supplied arrangements to the
        file named by the supplied filename. Not rocket science.
        """
        
        arrangementsFile = open(filename, 'wb')
        dump(arrangements, arrangementsFile)
        arrangementsFile.close()
    
    
    def _getCoordinates(self, place):
        """ Returns the position of the supplied place if it has one.
        Otherwise, just returns the place itself.
        """
        
        if hasattr(place, 'position'):
            return place.position
        return place


    def _reflect(self, place, velocity, boundaries):
        """ Used to work out the velocity when a body bounces off the
        Frame's bounds. 
        
        If the supplied place lies between the supplied boundaries, just
        returns the supplied velocity.
        
        Otherwise, returns the opposite of the velocity multiplied by
        the Frame's bounce proportion.
        """
        
        if (place <= boundaries[0]) or (place >= boundaries[1]):
            return -velocity * self.bounce
        return velocity


    def _getStartingPatterns(self):
        """ Tries to load the starting patterns from the file named by this
        object's class's 'startingPatternsFilename' attribute.
        
        If successful, returns them.
        
        Otherwise, if it can't find the file, returns None.
        """    
        
        try:
            patternFile = open(self.__class__.startingPatternsFilename, 'r')
            result      = load(patternFile)
            patternFile.close()
            return result
        except IOError:
            return None


    def _hasMemberLike(listOfMembers, itemToTest, minimumAngle=0.0001):
        """ Static method. Returns False if, for _every_ member of 
        listOfMembers: one or more element of that member is more than
        the supplied minimumAngle different from the corresponding
        element in the supplied itemToTest.
        Otherwise returns True.
        """
        
        for existingMember in listOfMembers:  
            if reduce(bool.__and__, [abs(elementOfExisting - elementOfItemToTest) < minimumAngle for elementOfExisting, elementOfItemToTest in zip(existingMember, itemToTest)]):
                return True
        return False


    def _roundCoordinates(unroundedCoordinates, minimumAngle=0.0001):
        """ Static method. Rounds each element of the supplied
        unroundedCoordinates to the nearest multiple of the supplied
        minimumAngle and returns the result as a new coordinate list.
        """
        
        return [minimumAngle * int(0.5 * cmp(unroundedCoord, 0.0) + (unroundedCoord / minimumAngle)) for unroundedCoord in unroundedCoordinates]
  
  
    dimensions               = 2
    defaultStartingMargin    = 0.01
    numberOfColours          = 10000.0
    colourScheme             = 'blue_thermal'
    startingPatternsFilename = '.\\startingFramePatterns.pkl'
    setStartingArrangements  = staticmethod(_setStartingArrangementsForFrame)
    _movePoint               = staticmethod(_movePoint)
    _saveArrangementsFile    = staticmethod(_saveArrangementsFile)
    _hasMemberLike           = staticmethod(_hasMemberLike)
    _roundCoordinates        = staticmethod(_roundCoordinates)
    


class Disk(Frame):
    """ Circular Frame.
    Like other Frames, used to distribute points through a colourspace 
    by allowing bodies to repel one another until they settle into a 
    stable arangement within it.
    """
    
    def __init__(self, radius=127.5, bounce=0.9, drag=0.05):
        """ Initialise Disk() with a radius, the
        proportion of speed that a body it retains when it
        reflects off the edges of the space and the proportion
        of speed that a body loses each tick due to drag.
        
        As with other Frames, self.bounds holds the object 
        that define's the space's bounds.
        self.bound holds the proportion of speed that a body
        retains when it reflects off the bounds
        self.drag holds the proportion of speed that a body
        loses each tick due to drag.
        self.dimensions holds the number of dimensions the space
        has.
        self.numberOfColours, self.colourScheme and 
        self.colourSpan are only used when you want to draw a
        picture of the bodies in the space. They hold the
        information about the number of graduations of colour
        used to represent positions along one of the axes and 
        the specific way the colour varies across those
        graduations.
        self.axes holds a list of numbers naming each dimension.
        It equals: [0, 1].
        self.length holds a list of the length of the space along
        each dimension.
        self.bodyList holds a list of all the bodies in the space.
        """    
    
        Frame.__init__(self, [[0.0, radius * 2.0],] * self.__class__.dimensions, bounce, drag)
        self.radius = radius
        
        
    def inside(self, coordinates):
        """ Returns True if the euclidian distance from a point at
        the supplied coordinates to the centre of the Disk is less
        than or equal to the disk's radius.
        Otherwise, returns False.
        """
        
        return (self.distancesquare(coordinates, [self.radius] * self.dimensions)[0]) <= (self.radius * self.radius)
   
   
    def mapVelocityFromFlat(self, flatVelocity, flatPosition):       
        """ Returns a new velocity vector obtained by applying the drag
        and any change due to bouncing off the disk's bounds.
        """

        projected = [flatPosition[axis] + flatVelocity[axis] for axis in self.axes]                       
        if self.inside(projected):
            withoutDrag = flatVelocity
        else:         
            speed       = sqrt(sum([flatVelocity[axis] * flatVelocity[axis] for axis in self.axes]))
            withoutDrag = genscale([self.radius - projected[axis] for axis in self.axes], speed * self.bounce)            
        oneMinusDrag = 1.0 - self.drag
        return [withoutDrag[axis] * oneMinusDrag for axis in self.axes]


    dimensions = 2



class Polyhedron(object):
    """ Holds the coordinates of the corners of a polyhedron.
        Includes non-data descriptors to return the number of corners
        and whether the Polyhedron belongs to the list of regular
        polyhedra (also called Platonic solids), uniform polyhedra
        or zonohedra.
        
        Used by in large to generate starting position patterns. 
    """

    def __init__(self, cornerCoordinates=[]):
        """ Initialise Polyhedron() with a list of cornerCoordinates.
        
        'Normalises' each element of each coordinate, dividing it by
        the biggest element among all the cornerCoordinates.
        """
        
        maxCoord               = max([max([abs(float(coord)) for coord in corner]) for corner in cornerCoordinates])
        self.cornerCoordinates = [[float(coord) / maxCoord for coord in corner] for corner in cornerCoordinates]


    def regularPolyhedra():
        """ Static method. Returns a list of the classes corresponding
        to the five regular polyhedra (also called Platonic solids).
        
        These are the five polyhedra in which the same number of faces
        meet at each vertex and each face is a regular, convex polygon
        of the same size and shape.
        """
            
        return [Tetrahedron, Octahedron, CubePolyhedron, Isosahedron, Dodecahedron]


    def uniformPolyhedra():
        """ Static method. Returns a list of the classes of uniform
        polyhedra.
        """
        
        return Polyhedron.regularPolyhedra() + [OmnitruncatedCuboctahedron, TruncatedCube, TruncatedDodecahedron]


    def zonohedra():
        """ Static method. Returns a list of the classes of zonohedra.
        """    
    
        return [CubePolyhedron, OmnitruncatedCuboctahedron, RhombicDodecahedron]


    def _getNumberOfCorners(self):
        """ Used to supply the value for the non-data descriptor 
        'numberOfCorners'.
        
        Returns the number of corners in the Polyhedron.
        """
        
        if not hasattr(self, '_numberOfCorners'):
            self._numberOfCorners = len(self.cornerCoordinates)
        return self._numberOfCorners
        
        
    def _getRegular(self):
        """ Used to supply the value for the non-data descriptor 
        'regular'.
        
        Returns True if the Polyhedron belongs to the list of
        regular polyhedra that Polyhedron.regularPolyhedra() returns.
        Otherwise returns False.
        """
        
        return self.__class__ in Polyhedron.regularPolyhedra()
        
        
    def _getUniform(self):
        """ Used to supply the value for the non-data descriptor 
        'uniform'.
        
        Returns True if the Polyhedron belongs to the list of
        uniform polyhedra that Polyhedron.regularPolyhedra() returns.
        Otherwise returns False.
        """    
        
        return self.__class__ in Polyhedron.uniformPolyhedra()


    def _getZonohedron(self):
        """ Used to supply the value for the non-data descriptor 
        'zonohedron'.
        
        Returns True if the Polyhedron belongs to the list of
        zonohedra that Polyhedron.regularPolyhedra() returns.
        Otherwise returns False.
        """    
        
        return self.__class__ in Polyhedron.zonohedra()
    
    
    phi              = (1.0 + sqrt(5.0)) / 2.0
    invPhi           = 1.0 / phi
    xi               = sqrt(2.0) - 1.0
    invXi            = 1.0 / xi
    numberOfCorners  = property(_getNumberOfCorners)
    regular          = property(_getRegular)
    uniform          = property(_getUniform)
    zonohedron       = property(_getZonohedron)
    regularPolyhedra = staticmethod(regularPolyhedra)
    uniformPolyhedra = staticmethod(uniformPolyhedra)
    zonohedra        = staticmethod(zonohedra)
    

    
class Tetrahedron(Polyhedron):
    """ Regular polyhedron with four faces.
    
    Corners are at:
        (+1, +1, +1), 
        (-1, -1, +1), 
        (-1, +1, -1) and
        (+1, -1, -1)
    """

    def __init__(self):
        """ Just calls Polyhedron's __init__ method with a fixed list
        of the positions of the four corners.
        """    
    
        Polyhedron.__init__(self, [[1, 1, 1], [-1, -1, +1], [-1, 1, -1], [1, -1, -1]])



class CubePolyhedron(Polyhedron):
    """ Regular polyhedron with six faces.
    
    Corners are at:
         (-1, -1, -1),
         (-1, -1, +1),
         (-1, +1, -1),
         (-1, +1, +1),
         (+1, -1, -1),
         (+1, -1, +1),
         (+1, +1, -1) and
         (+1, +1, +1)
    """
    
    def __init__(self):
        """ Just calls Polyhedron's __init__ method with a fixed list
        of the positions of the eight corners.
        """      
        
        Polyhedron.__init__(self, [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]])



class Octahedron(Polyhedron):
    """ Regular polyhedron with eight faces.
    
    Corners are at:
        (-1, 0, 0), 
        (+1, 0, 0), 
        (0, -1, 0), 
        (0, +1, 0), 
        (0, 0, -1) and
        (0, 0, +1)    
    """
    
    def __init__(self):
        """ Just calls Polyhedron's __init__ method with a fixed list
        of the positions of the six corners.
        """          
        
        Polyhedron.__init__(self, [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]])



class Dodecahedron(Polyhedron):
    """ Regular polyhedron with twelve faces.
    """

    def __init__(self):
        """ Just calls Polyhedron's __init__ method with a fixed list
        of the positions of the twenty corners.
        """      
        
        Polyhedron.__init__(self, [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1], [0, -Polyhedron.invPhi, -Polyhedron.phi], [0, -Polyhedron.invPhi, Polyhedron.phi], [0, Polyhedron.invPhi, -Polyhedron.phi], [0, Polyhedron.invPhi, Polyhedron.phi], [-Polyhedron.invPhi, -Polyhedron.phi, 0], [-Polyhedron.invPhi, Polyhedron.phi, 0], [Polyhedron.invPhi, -Polyhedron.phi, 0], [Polyhedron.invPhi, Polyhedron.phi, 0], [-Polyhedron.phi, 0, -Polyhedron.invPhi], [-Polyhedron.phi, 0, Polyhedron.invPhi], [Polyhedron.phi, 0, -Polyhedron.invPhi], [Polyhedron.phi, 0, Polyhedron.invPhi]])



class Isosahedron(Polyhedron):
    """ Regular polyhedron with twenty faces.
    """

    def __init__(self):
        """ Just calls Polyhedron's __init__ method with a fixed list
        of the positions of the twelve corners.
        """      
    
        Polyhedron.__init__(self, [[0, -1, -Polyhedron.phi], [0, -1, Polyhedron.phi], [0, 1, -Polyhedron.phi], [0, 1, Polyhedron.phi], [-1, -Polyhedron.phi, 0], [-1, Polyhedron.phi, 0], [1, -Polyhedron.phi, 0], [1, Polyhedron.phi, 0], [-Polyhedron.phi, 0, -1], [-Polyhedron.phi, 0, 1], [Polyhedron.phi, 0, -1], [Polyhedron.phi, 0, 1]])



class OmnitruncatedCuboctahedron(CubePolyhedron):
    """ Uniform polyhedron with twenty-six faces.
    """

    def __init__(self):
        """ Calls Polyhedron's __init__ method with a fixed list of 
        the positions of the forty-eight corners.
        """     
        
        CubePolyhedron.__init__(self)
        Polyhedron.__init__(self, reduce(list.__add__, [[entry for entry in genperm([[absolute, -absolute] for absolute in schema])] for schema in permsequence([1, sqrt(2.0) + 1.0, sqrt(8.0) + 1.0])]))



class TruncatedCube(CubePolyhedron):
    """ Uniform polyhedron with fourteen faces.
    """

    def __init__(self):
        """ Calls Polyhedron's __init__ method with a fixed list of 
        the positions of the twenty-four corners.
        """  
        
        CubePolyhedron.__init__(self)
        Polyhedron.__init__(self, [[-Polyhedron.xi, -1, -1], [-Polyhedron.xi, -1, 1], [-Polyhedron.xi, 1, -1], [-Polyhedron.xi, 1, 1], [Polyhedron.xi, -1, -1], [Polyhedron.xi, -1, 1], [Polyhedron.xi, 1, -1], [Polyhedron.xi, 1, 1], [-1, -Polyhedron.xi, -1], [-1, -Polyhedron.xi, 1], [-1, Polyhedron.xi, -1], [-1, Polyhedron.xi, 1], [1, -Polyhedron.xi, -1], [1, -Polyhedron.xi, 1], [1, Polyhedron.xi, -1], [1, Polyhedron.xi, 1], [-1, -1, -Polyhedron.xi], [-1, -1, Polyhedron.xi], [-1, 1, -Polyhedron.xi], [-1, 1, Polyhedron.xi], [1, -1, -Polyhedron.xi], [1, -1, Polyhedron.xi], [1, 1, -Polyhedron.xi], [1, 1, Polyhedron.xi]])      



class TruncatedDodecahedron(Dodecahedron):
    """ Uniform polyhedron with thirty-two faces.
    """

    def __init__(self):
        """ Calls Polyhedron's __init__ method with a fixed list of 
        the positions of the sixty corners.
        """     
        
        Dodecahedron.__init__(self)
        phiPlusTwo = Polyhedron.phi + 2.0
        twoPhi     = Polyhedron.phi * 2.0
        phiSquared = Polyhedron.phi * Polyhedron.phi
        Polyhedron.__init__(self, [[0, -Polyhedron.invPhi, -phiPlusTwo], [0, -Polyhedron.invPhi, phiPlusTwo], [0, Polyhedron.invPhi, -phiPlusTwo], [0, Polyhedron.invPhi, phiPlusTwo], [-phiPlusTwo, 0, -Polyhedron.invPhi], [-phiPlusTwo, 0, Polyhedron.invPhi], [phiPlusTwo, 0, -Polyhedron.invPhi], [phiPlusTwo, 0, Polyhedron.invPhi], [-Polyhedron.invPhi, -Polyhedron.phi, -twoPhi], [-Polyhedron.invPhi, -Polyhedron.phi, twoPhi], [-Polyhedron.invPhi, Polyhedron.phi, -twoPhi], [-Polyhedron.invPhi, Polyhedron.phi, twoPhi], [Polyhedron.invPhi, -Polyhedron.phi, -twoPhi], [Polyhedron.invPhi, -Polyhedron.phi, twoPhi], [Polyhedron.invPhi, Polyhedron.phi, -twoPhi], [Polyhedron.invPhi, Polyhedron.phi, twoPhi], [-Polyhedron.invPhi, -phiPlusTwo, 0], [-Polyhedron.invPhi, phiPlusTwo, 0], [Polyhedron.invPhi, -phiPlusTwo, 0], [Polyhedron.invPhi, phiPlusTwo, 0], [-twoPhi, -Polyhedron.invPhi, -Polyhedron.phi], [-twoPhi, -Polyhedron.invPhi, Polyhedron.phi], [-twoPhi, Polyhedron.invPhi, -Polyhedron.phi], [-twoPhi, Polyhedron.invPhi, Polyhedron.phi], [twoPhi, -Polyhedron.invPhi, -Polyhedron.phi], [twoPhi, -Polyhedron.invPhi, Polyhedron.phi], [twoPhi, Polyhedron.invPhi, -Polyhedron.phi], [twoPhi, Polyhedron.invPhi, Polyhedron.phi], [-Polyhedron.phi, -twoPhi, -Polyhedron.invPhi], [-Polyhedron.phi, -twoPhi, Polyhedron.invPhi], [-Polyhedron.phi, twoPhi, -Polyhedron.invPhi], [-Polyhedron.phi, twoPhi, Polyhedron.invPhi], [Polyhedron.phi, -twoPhi, -Polyhedron.invPhi], [Polyhedron.phi, -twoPhi, Polyhedron.invPhi], [Polyhedron.phi, twoPhi, -Polyhedron.invPhi], [Polyhedron.phi, twoPhi, Polyhedron.invPhi], [-Polyhedron.phi, -2, -phiSquared], [-Polyhedron.phi, -2, phiSquared], [-Polyhedron.phi, 2, -phiSquared], [-Polyhedron.phi, 2, phiSquared], [Polyhedron.phi, -2, -phiSquared], [Polyhedron.phi, -2, phiSquared], [Polyhedron.phi, 2, -phiSquared], [Polyhedron.phi, 2, phiSquared], [-phiSquared, -Polyhedron.phi, -2], [-phiSquared, -Polyhedron.phi, 2], [-phiSquared, Polyhedron.phi, -2], [-phiSquared, Polyhedron.phi, 2], [phiSquared, -Polyhedron.phi, -2], [phiSquared, -Polyhedron.phi, 2], [phiSquared, Polyhedron.phi, -2], [phiSquared, Polyhedron.phi, 2],[-2, -phiSquared, -Polyhedron.phi], [-2, -phiSquared, Polyhedron.phi], [-2, phiSquared, -Polyhedron.phi], [-2, phiSquared, Polyhedron.phi], [2, -phiSquared, -Polyhedron.phi], [2, -phiSquared, Polyhedron.phi], [2, phiSquared, -Polyhedron.phi], [2, phiSquared, Polyhedron.phi]])       



class RhombicDodecahedron(Dodecahedron):
    """ Zonohedron with twelve faces.
    """
        
    def __init__(self):
        """ Calls Polyhedron's __init__ method with a fixed list of 
        the positions of the fourteen corners.
        """  
        
        Dodecahedron.__init__(self)
        Polyhedron.__init__(self, [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1], [0, 0, -2], [0, 0, 2], [0, -2, 0], [0, 2, 0], [-2, 0, 0], [2, 0, 0]])
        


class Cube(Frame, CubePolyhedron):
    """ Three-dimensional Frame with the shape of a cube.
    
    Like other Frames, used to distribute points through a colourspace 
    by allowing bodies to repel one another until they settle into a 
    stable arangement within it.
    """

    def __init__(self, bounds=[[0.0, 255.0], [0.0, 255.0], [0.0, 255.0]], bounce=0.75, drag=0.02):
        """ Initialise Cube() with a list of the bounds in each
        of the three dimensions, the proportion of speed that a 
        body it retains when it reflects off the edges of the 
        space and the proportion of speed that a body loses each 
        tick due to drag.
        
        As with other Frames, self.bounds holds the object 
        that define's the space's bounds.
        self.bound holds the proportion of speed that a body
        retains when it reflects off the bounds
        self.drag holds the proportion of speed that a body
        loses each tick due to drag.
        self.dimensions holds the number of dimensions the space
        has.
        self.numberOfColours, self.colourScheme and 
        self.colourSpan are only used when you want to draw a
        picture of the bodies in the space. They hold the
        information about the number of graduations of colour
        used to represent positions along one of the axes and 
        the specific way the colour varies across those
        graduations.
        self.axes holds a list of numbers naming each dimension.
        It equals: [0, 1, 2].
        self.length holds a list of the length of the space along
        each dimension.
        self.bodyList holds a list of all the bodies in the space.
        """

        Frame.__init__(self, bounds, bounce, drag)
        CubePolyhedron.__init__(self)


    def _setStartingArrangementsForCube(maximumPointsInCircle=6):    
        """ Static method. Generates startingPatterns for the Cube
        class, using the corners of the uniform polyhedra, the
        corners of the rhombic dodecahedron and the intersections
        of great circles centred around the centre of the cube.
        Saves them to the file named by the Cube class's 
        startingPatternsFilename attribute.
        """

        assert isinstance(maximumPointsInCircle, int)
        arrangements = {} 
        for polyClass in Polyhedron.uniformPolyhedra() + [RhombicDodecahedron]:
            poly                               = polyClass()
            arrangements[poly.numberOfCorners] = poly.cornerCoordinates        
        rangeOfPoints = range(2, maximumPointsInCircle + 1)        
        for pointsPerCircle in rangeOfPoints:
            intersections         = Cube._arrangePointsByIntersections(pointsPerCircle, rangeOfPoints)
            numberOfIntersections = len(intersections)
            if numberOfIntersections not in arrangements.keys():
                arrangements[numberOfIntersections] = intersections                
        for pointsPerCircle in rangeOfPoints:
            alongAxes               = Cube._arrangePointsAlongAxes(pointsPerCircle)
            numberOfPointsAlongAxes = len(alongAxes)
            if numberOfPointsAlongAxes not in arrangements.keys():
                arrangements[numberOfPointsAlongAxes] = alongAxes                       
        Cube._saveArrangementsFile(arrangements, Cube.startingPatternsFilename)


    def _arrangePointsByIntersections(pointsPerCircle, rangeOfPoints=None):
        """ Static method. Returns a list of the points at which great 
        circles intersect.
        """ 

        result = []
        if rangeOfPoints is None:
            rangeOfPoints = range(0, pointsPerCircle)
        [Cube._findIntersections(result, pi / float(pointsPerCircle), outerCircle, rangeOfPoints) for outerCircle in rangeOfPoints]
        return result                   
                  
                  
    def _arrangePointsAlongAxes(pointsPerCircle, firstFunctions=[sin, cos, lambda angle: 0.0]):
        dimensionList = range(0, Cube.dimensions)    
        result        = []
        [Cube._arrangeAroundCircle(result, [firstFunctions[(circleNumber + dimension) % Cube.dimensions] for dimension in dimensionList], 2.0 * pi / float(pointsPerCircle), pointsPerCircle) for circleNumber in dimensionList]
        return result


    def _findIntersections(coordList, angleDifference, outerCircle, rangeOfPoints):
        """ Static method. Where the supplied coordList doesn't already have 
        points near them, adds the intersections between different circles 
        given by the supplied rangeOfPoints and the supplied outerCircle.
        """        
        
        outerAngle         = outerCircle * angleDifference
        sineOfOuterAngle   = sin(outerAngle)
        cosineOfOuterAngle = cos(outerAngle)
        [Cube._addIntersection(coordList, innerCircle, angleDifference, sineOfOuterAngle, sineOfOuterAngle * sineOfOuterAngle, cosineOfOuterAngle * cosineOfOuterAngle) for innerCircle in rangeOfPoints]   


    def _addIntersection(coordList, innerCircle, angleDifference, sineOfOuterAngle, squareOfSineOfOuterAngle, squareOfCosineOfOuterAngle):
        """ Static method. Where the supplied coordList doesn't already have points 
        near them, adds the intersections between the supplied innerCircle and the 
        circle implied it and the supplied sine and cosine.
        """
        
        innerAngle              = innerCircle * angleDifference            
        denominator             = cos(innerAngle) * cos(innerAngle) * squareOfSineOfOuterAngle + 1
        squareRootOfDenominator = sqrt(denominator)
        x                       = -sqrt(1 - squareOfCosineOfOuterAngle / denominator)
        y                       = -sineOfOuterAngle / squareRootOfDenominator
        z                       = -1 / squareRootOfDenominator
        for unroundedPoint in [x, y, z], [x, -y, -z], [-x, y, z], [-x, -y, -z]:
            point = Frame._roundCoordinates(unroundedPoint)
            if not Frame._hasMemberLike(coordList, point):
                coordList.append(point)   


    def _arrangeAroundCircle(coordList, functionList, angleDifference, numberOfPoints):
        """ Static method. Where the supplied coordList doesn't 
        already have points near them, adds points arranged 
        around a circle.
        
        The supplied functionList should contain a list of the
        functions to generate the positions in each dimension.
        """
        
        for point in range(0, numberOfPoints):
            coordinates = Frame._roundCoordinates([angleFunction(angleDifference * float(point)) for angleFunction in functionList])
            if not Frame._hasMemberLike(coordList, coordinates):
                coordList.append(coordinates)


    dimensions                    = 3      
    startingPatternsFilename      = '.\\startingCubePatterns.pkl'
    setStartingArrangements       = staticmethod(_setStartingArrangementsForCube)
    _arrangeAroundCircle          = staticmethod(_arrangeAroundCircle)
    _arrangePointsAlongAxes       = staticmethod(_arrangePointsAlongAxes)
    _arrangePointsByIntersections = staticmethod(_arrangePointsByIntersections)
    _addIntersection              = staticmethod(_addIntersection)
    _findIntersections            = staticmethod(_findIntersections)



class Sphere(Disk):
    """ Spherical Frame.
    
    Like other Frames, used to distribute points through a colourspace 
    by allowing bodies to repel one another until they settle into a 
    stable arangement within it.
    """

    def __init__(self, radius=127.5, bounce=0.8, drag=0.05):       
        """ Initialise Sphere() with a radius, the
        proportion of speed that a body it retains when it
        reflects off the edges of the space and the proportion
        of speed that a body loses each tick due to drag.
        
        As with other Frames, self.bounds holds the object 
        that define's the space's bounds.
        self.bound holds the proportion of speed that a body
        retains when it reflects off the bounds
        self.drag holds the proportion of speed that a body
        loses each tick due to drag.
        self.dimensions holds the number of dimensions the space
        has.
        self.numberOfColours, self.colourScheme and 
        self.colourSpan are only used when you want to draw a
        picture of the bodies in the space. They hold the
        information about the number of graduations of colour
        used to represent positions along one of the axes and 
        the specific way the colour varies across those
        graduations.
        self.axes holds a list of numbers naming each dimension.
        It equals: [0, 1, 2].
        self.length holds a list of the length of the space along
        each dimension.
        self.bodyList holds a list of all the bodies in the space.
        """ 
        
        Disk.__init__(self, radius, bounce, drag)
    
    
    dimensions               = 3
    startingPatternsFilename = '.\\startingCubePatterns.pkl'

            

class Body(object):
    """ Masses that move through Frame objects, distributing
    themselves at positions later translated into colour
    values. 
    
    Inside a Frame they repel each other until they settle
    into a fairly stable arrangement within the space.
    """


    defaultCharge = 20.0


    def __init__(self, velocity=[0.0, 0.0], acceleration=[0.0, 0.0], position=[0.0, 0.0], frame=Frame(), charge=None, frozen=False):
        """ Initialise Body with a Frame and starting
        position, velocity and acceleration. 
        
        self.frame holds the Frame object through which
        the body moves
        self.frozen holds a flag that indicates if the
        body can still move through its frame (False) or
        instead if it's frozen in place (True)
        self.position holds the coordinates of the body's
        position.
        self.velocity holds the coordinates of the vector
        indicating the body's velocity.
        self.acceleration holds the coordinates of the
        vector indicating the body's acceleration
        """
        
        self.frozen       = frozen
        self.velocity     = copy.copy(velocity)
        self.acceleration = copy.copy(acceleration)
        self.position     = copy.copy(position)
        self.frame        = frame
        self.dimensions   = len(self.position)
        self.axes         = range(0, self.dimensions)
        if charge is None:
            self.charge = Body.defaultCharge
        else:
            self.charge = charge


    def accelerate(self):
        """ Add the body's acceleration to its velocity then set
        the body's acceleration to a zero vector and make any
        further adjustments to the body's velocity due to its
        position in its frame (for instance, striking the frame's
        boundary may reverse the direction of the body's velocity)
        """
        
        flatVelocity      = [self.velocity[axis] + self.acceleration[axis] for axis in self.axes]
        self.velocity     = self.frame.mapVelocityFromFlat(flatVelocity, self.position)
        self.acceleration = [0.0] * self.dimensions
        
        
    def displace(self):
        """ Add the body's velocity to its position then make any
        further adjustments to the body's position due to its
        position in its frame (for instance, straying beyond the
        frame's boundary may return it to just inside the point
        through which it would've passed)
        """    
    
        self.position = self.frame.mapPositionFromFlat([self.position[axis] + self.velocity[axis] for axis in self.axes])
        
        
    def move(self):
        """ If the body isn't frozen in place (as indicated by
        its 'frozen' attribute), add its acceleration to its
        velocity then add its velocity to its position, as
        above.
        """
        
        if not self.frozen:
            self.accelerate()
            self.displace()
        
        
    def repelforce(self, other):
        """ Returns a vector that indicates how the body
        pushes on the supplied other body.
        
        Its magnitude falls of with the square of the
        distance between the two bodies.
        """
        
        distSquare, squares = self.frame.distancesquare(self, other)
        if distSquare <= 0.0:
            return [0.0] * self.dimensions
        return genscale(self.frame.direction(other, self, squares), self.charge / distSquare)
            
            
    def repel(self, other, force):
        """ Add the supplied force to the supplied other
        body's acceleration.
        """
        
        other.acceleration = [other.acceleration[axis] + force[axis] for axis in self.axes]


    def repelAll(self, bodylist):
        """ Determine how the body pushes on each of the
        other bodies in the supplied bodylist and add those
        vectors to their accelerations, as above.
        """
        
        for other in bodylist:
            if other is not self:
                self.repel(other, self.repelforce(other))


    def drawDot(self, surface, stamp, baseRadius=10.0, borderColour=[255, 255, 255], borderWidth=1, pixelsPerUnit=None):
        """ Finds a position on the supplied surface corresponding
        to the body's position in its frame and then uses the
        supplied stamp method to draw a picture of the body
        there.
        """

        if pixelsPerUnit is None:
            pixelsPerUnit = self.getPixelsPerUnit(surface)
        if self.dimensions == 1:
            dotColour = [255, 255, 255]
            radius    = baseRadius
        else:
            if self.dimensions == 2:
                dotColour = [int(255.0 *(self.position[axis] - self.frame.bounds[axis][0]) / self.frame.length[axis]) for axis in [0, 1]] + [200]
                radius    = baseRadius
            else:               
                radius, proportionAlongAxisTwo = self._getRadiusAndProportionByPosition(2, baseRadius)
                dotColour                      = self.frame.colourSpan.colour(self.frame.numberOfColours * proportionAlongAxisTwo, basis=self.frame.colourScheme)
        self._stampDot(surface, stamp, dotColour, pixelsPerUnit, radius, borderWidth, borderColour)


    def eraseDot(self, surface, stamp, baseRadius=10.0, borderWidth=1, pixelsPerUnit=None):
        """ Use the supplied stamp method to erase the body
        from the supplied surface.
        """

        if pixelsPerUnit is None:
            pixelsPerUnit = self.getPixelsPerUnit(surface)
        if self.dimensions < 3:
            radius = baseRadius
        else:
            radius, proportionAlongAxisTwo = self._getRadiusAndProportionByPosition(2, baseRadius)
        self._stampDot(surface, stamp, (0, 0, 0), pixelsPerUnit, radius, borderWidth, (0, 0, 0))
    
    
    def getPixelsPerUnit(self, surface):
        """ Returns the length on the supplied displaySurface of one unit in
        the body's frame.
        """

        return [surface.get_width() / self.frame.length[0], surface.get_height() / self.frame.length[1]]

    def _getRadiusAndProportionByPosition(self, axis, baseRadius):      
        """ Returns a list containing (a) a proportion that indicates 
        how far the body's position in the relevant dimension is
        along the supplied axis and (b) a value equal to that
        same proportion of the supplied baseRadius
        """

        proportionAlongAxis = (self.position[axis] - self.frame.bounds[axis][0]) / self.frame.length[axis]
        return [(0.5 + proportionAlongAxis) * baseRadius, proportionAlongAxis]


    def _stampDot(self, surface, stamp, dotColour, pixelsPerUnit, radius, borderWidth, borderColour):
        """ Use the supplied stamp method to draw the body on to
        the supplied surface at its current position.
        """

        locus = (int(pixelsPerUnit[0] * self.position[0]), int(pixelsPerUnit[1] * self.position[1]))
        stamp(surface, dotColour, locus, int(abs(radius)))
        if (self.dimensions > 2) and (borderWidth is not None):
            stamp(surface, borderColour, locus, int(abs(radius)), borderWidth)