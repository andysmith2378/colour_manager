import colourmanager

from copy import copy

import unittest



class TestCase01(unittest.TestCase):
    """ Unit tests for the ColourManager and Colour classes
    """
    
    def setUp(self):
        """ Create an example ColourManager() and Colour() to use in the tests
        """
        
        self.manager            = colourmanager.ColourManager()
        self.exampleColourTuple = [190, 200, 192]
        self.exampleColourName  = 'Ecstatic Green'
        self.exampleColour      = colourmanager.Colour(self.manager, self.exampleColourName, self.exampleColourTuple)


    def check_01(self):
        """ Check passing arguments to Colour()
        """
        
        assert hasattr(self.exampleColour, 'manager')
        assert self.exampleColour.manager is self.manager
        assert hasattr(self.exampleColour, 'colourname')
        assert self.exampleColour.colourname == self.exampleColourName
        assert hasattr(self.exampleColour, 'colourvalues')
        assert self.exampleColour.colourvalues == self.exampleColourTuple
        assert hasattr(self.exampleColour, 'red')
        assert self.exampleColour.red == self.exampleColourTuple[0]
        assert hasattr(self.exampleColour, 'green')
        assert self.exampleColour.green == self.exampleColourTuple[1]
        assert hasattr(self.exampleColour, 'blue')
        assert self.exampleColour.blue == self.exampleColourTuple[2]


    def check_02(self):
        """ Check that after creating a colour with a manager that that 
        manger's removed values include the example colour's rgb tuple
        """
        
        assert hasattr(self.manager, 'removedValues')
        assert self.exampleColourTuple in self.manager.removedValues


    def check_03(self):
        """ Check colour str method returns the colour name
        """
        
        colourString = str(self.exampleColour)
        assert isinstance(colourString, str)
        assert colourString == self.exampleColourName


    def check_04(self):
        """ Check colour repr method returns a string containing the colour name 
        and a string representation of the rgb tuple
        """
        
        representation = repr(self.exampleColour)
        assert isinstance(representation, str)
        assert self.exampleColourName in representation
        assert str(self.exampleColourTuple) in representation


    def check_05(self):
        """ Check that new ColourManager has a list of removed values and that it's empty
        """
        
        newManager = colourmanager.ColourManager()
        assert hasattr(newManager, 'removedValues')
        assert newManager.removedValues == []


    def check_06(self):
        """ Check passing background tuple to new ColourManager
        """
        
        newManager = colourmanager.ColourManager(self.exampleColourTuple)
        assert hasattr(newManager, 'background')
        assert newManager.background == self.exampleColourTuple
        assert newManager.removedValues == [self.exampleColourTuple]
        
        
    def check_07(self):
        """ Check passing background Colour to new ColourManager
        """
        
        newManager = colourmanager.ColourManager(self.exampleColour)
        assert newManager.background == self.exampleColourTuple
        assert newManager.removedValues == [self.exampleColourTuple]  
    
    
    def check_08(self):
        """ Check that we can call for ten new colours one at a time with a 
        new manager, checking that each one is different and belongs to the 
        class Colour() and that the manager adds the rgb tuple of each one 
        to its list of removedValues
        """ 
        
        newManager       = colourmanager.ColourManager(self.exampleColour)
        extractedColours = [newManager.nextColour() for i in range(0, 10)]
        for entry in extractedColours:
            assert extractedColours.count(entry) == 1
            assert isinstance(entry, colourmanager.Colour)
            assert entry.colourvalues in newManager.removedValues


    def check_09(self):
        """ Check that we can call for a list of ten colours (all at once) using the 
        colourList method with a new manager, checking that each one is different and 
        belongs to the class Colour() and that the manager adds the rgb tuple of each 
        one to its list of removedValues
        """ 
        
        newManager       = colourmanager.ColourManager(self.exampleColour)
        extractedColours = newManager.colourList(10)
        assert isinstance(extractedColours, list)
        assert len(extractedColours) == 10
        for entry in extractedColours:
            assert extractedColours.count(entry) == 1
            assert isinstance(entry, colourmanager.Colour)
            assert entry.colourvalues in newManager.removedValues


    def check_11(self):
        """ Check that we can call for a list of ten colours (all at once) using the 
        colourList method with a new manager, checking that each one is different and 
        belongs to the class Colour() and that the manager adds the rgb tuple of each 
        one to its list of removedValues
        """ 
        
        for x in range(1, 61):
            print x
            newManager       = colourmanager.ColourManager([0, 0, 0])
            extractedColours = newManager.colourList(x)
            assert isinstance(extractedColours, list)
            assert len(extractedColours) == x
            for entry in extractedColours:
                assert extractedColours.count(entry) == 1
                assert isinstance(entry, colourmanager.Colour)
                assert entry.colourvalues in newManager.removedValues


    def _check_10(self):
        """ Use pygame to generate a chart with all the colours 
        """ 
        
        import pygame  
        screen = pygame.display.set_mode((7168, 8192), 0, 24)
        colourmanager.ColourManager.drawColourSamples(screen, pygame.draw.rect, 'blit', pygame.font.SysFont, {'name' : 'garamond', 'size' : 18, 'bold' : 0, 'italic' : 0}, pygame.font.init, pygame.display.flip)
        pygame.image.save(screen, "coloursArrangedByRedAndGreen.jpg")     
        

def suite():
    def numberSuffix(x,y):
        return cmp(x[-2:], y[-2:])

    suite1   = unittest.makeSuite(TestCase01, 'check', sortUsing=numberSuffix)
    alltests = unittest.TestSuite((suite1,))
    return alltests


def main():
    runner = unittest.TextTestRunner(descriptions=0, verbosity=2)
    runner.run(suite())



if __name__ == '__main__':
    main()