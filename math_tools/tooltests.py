from math_tools.tools import genperm, perm, recursiveperm, bargraph, RangeTable, rotate, table, padzip, Keyword, scale

import unittest
class TestCase01(unittest.TestCase):
    def setUp(self):
        self.data1           = {0: 176, 2: 62, 3: 14, 4: 1, -7: 1, -6: 6, -5: 34, -4: 141, -3: 262, -2: 303}
        self.data2           = {0: 40, 1: 36, 5: 162, 10: 114, 4: 101, -9: 1, -6: 6, -5: 134, -4: 101, -3: 162, -1: 203}
        self.data3           = {3: 1000}
        self.data01          = [1, 2, 3, 4]
        self.data02          = ['a', 'c', 'd']
        self.data03          = ['!', '@']
        self.data04          = [1, 'a', '!']
        self.data05          = [2, 'b', '@', '%', 5, 4]
        self.row01           = ["abacus", "baby", "Edgar Allen Poe", "milk"]
        self.row02           = ["jeep", "king", "leaf", "nail"]
        self.row03           = ["cane", "dog", "fig", "orange"]
        self.row04           = ["grain", "heap", "igloo", "pail"]
        self.row05           = [5, 25, 125, 625]
        self.row06           = [2.0, 1.0, 3.0, 4.0]
        self.row07           = ["England:", 0, "Wales:", 1]
        self.defaultArgument = 'X'                     
        self.source          = {'Andy': 0.4, 'Colin': 0.5, 'Rohan':1.0}
        self.fDict1          = {'Marlow': 1.0, 'Hamlet': 2.0}
        self.fDict2          = {'Marlow': 10.0, 'Frodo': 20.0}
        self.fDict3          = {'Hamlet': 100.0, 'Frodo': 200.0}

    def check_01(self):
        gp = genperm([[1, 2, 3, 4, 5, 6], [1, 4, 9, 16, 25, 36], [1, 1, 2, 3, 5, 8]])
        assert [i for i in gp] == [[1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 1, 1], [5, 1, 1], [6, 1, 1], [1, 4, 1], [2, 4, 1], [3, 4, 1], [4, 4, 1], [5, 4, 1], [6, 4, 1], [1, 9, 1], [2, 9, 1], [3, 9, 1], [4, 9, 1], [5, 9, 1], [6, 9, 1], [1, 16, 1], [2, 16, 1], [3, 16, 1], [4, 16, 1], [5, 16, 1], [6, 16, 1], [1, 25, 1], [2, 25, 1], [3, 25, 1], [4, 25, 1], [5, 25, 1], [6, 25, 1], [1, 36, 1], [2, 36, 1], [3, 36, 1], [4, 36, 1], [5, 36, 1], [6, 36, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 1, 1], [5, 1, 1], [6, 1, 1], [1, 4, 1], [2, 4, 1], [3, 4, 1], [4, 4, 1], [5, 4, 1], [6, 4, 1], [1, 9, 1], [2, 9, 1], [3, 9, 1], [4, 9, 1], [5, 9, 1], [6, 9, 1], [1, 16, 1], [2, 16, 1], [3, 16, 1], [4, 16, 1], [5, 16, 1], [6, 16, 1], [1, 25, 1], [2, 25, 1], [3, 25, 1], [4, 25, 1], [5, 25, 1], [6, 25, 1], [1, 36, 1], [2, 36, 1], [3, 36, 1], [4, 36, 1], [5, 36, 1], [6, 36, 1], [1, 1, 2], [2, 1, 2], [3, 1, 2], [4, 1, 2], [5, 1, 2], [6, 1, 2], [1, 4, 2], [2, 4, 2], [3, 4, 2], [4, 4, 2], [5, 4, 2], [6, 4, 2], [1, 9, 2], [2, 9, 2], [3, 9, 2], [4, 9, 2], [5, 9, 2], [6, 9, 2], [1, 16, 2], [2, 16, 2], [3, 16, 2], [4, 16, 2], [5, 16, 2], [6, 16, 2], [1, 25, 2], [2, 25, 2], [3, 25, 2], [4, 25, 2], [5, 25, 2], [6, 25, 2], [1, 36, 2], [2, 36, 2], [3, 36, 2], [4, 36, 2], [5, 36, 2], [6, 36, 2], [1, 1, 3], [2, 1, 3], [3, 1, 3], [4, 1, 3], [5, 1, 3], [6, 1, 3], [1, 4, 3], [2, 4, 3], [3, 4, 3], [4, 4, 3], [5, 4, 3], [6, 4, 3], [1, 9, 3], [2, 9, 3], [3, 9, 3], [4, 9, 3], [5, 9, 3], [6, 9, 3], [1, 16, 3], [2, 16, 3], [3, 16, 3], [4, 16, 3], [5, 16, 3], [6, 16, 3], [1, 25, 3], [2, 25, 3], [3, 25, 3], [4, 25, 3], [5, 25, 3], [6, 25, 3], [1, 36, 3], [2, 36, 3], [3, 36, 3], [4, 36, 3], [5, 36, 3], [6, 36, 3], [1, 1, 5], [2, 1, 5], [3, 1, 5], [4, 1, 5], [5, 1, 5], [6, 1, 5], [1, 4, 5], [2, 4, 5], [3, 4, 5], [4, 4, 5], [5, 4, 5], [6, 4, 5], [1, 9, 5], [2, 9, 5], [3, 9, 5], [4, 9, 5], [5, 9, 5], [6, 9, 5], [1, 16, 5], [2, 16, 5], [3, 16, 5], [4, 16, 5], [5, 16, 5], [6, 16, 5], [1, 25, 5], [2, 25, 5], [3, 25, 5], [4, 25, 5], [5, 25, 5], [6, 25, 5], [1, 36, 5], [2, 36, 5], [3, 36, 5], [4, 36, 5], [5, 36, 5], [6, 36, 5], [1, 1, 8], [2, 1, 8], [3, 1, 8], [4, 1, 8], [5, 1, 8], [6, 1, 8], [1, 4, 8], [2, 4, 8], [3, 4, 8], [4, 4, 8], [5, 4, 8], [6, 4, 8], [1, 9, 8], [2, 9, 8], [3, 9, 8], [4, 9, 8], [5, 9, 8], [6, 9, 8], [1, 16, 8], [2, 16, 8], [3, 16, 8], [4, 16, 8], [5, 16, 8], [6, 16, 8], [1, 25, 8], [2, 25, 8], [3, 25, 8], [4, 25, 8], [5, 25, 8], [6, 25, 8], [1, 36, 8], [2, 36, 8], [3, 36, 8], [4, 36, 8], [5, 36, 8], [6, 36, 8]]

    def check_02(self):
        assert perm(1, None) == [[1]]
        assert perm(2, None) == [[2, 1], [1, 2]]
        assert perm(3, None) == [[3, 2, 1], [2, 3, 1], [2, 1, 3], [3, 1, 2], [1, 3, 2], [1, 2, 3]]
        assert perm(4, None) == [[4, 3, 2, 1], [3, 4, 2, 1], [3, 2, 4, 1], [3, 2, 1, 4], [4, 2, 3, 1], [2, 4, 3, 1], [2, 3, 4, 1], [2, 3, 1, 4], [4, 2, 1, 3], [2, 4, 1, 3], [2, 1, 4, 3], [2, 1, 3, 4], [4, 3, 1, 2], [3, 4, 1, 2], [3, 1, 4, 2], [3, 1, 2, 4], [4, 1, 3, 2], [1, 4, 3, 2], [1, 3, 4, 2], [1, 3, 2, 4], [4, 1, 2, 3], [1, 4, 2, 3], [1, 2, 4, 3], [1, 2, 3, 4]]
        for i in range(1, 6):
            assert perm(i, None) == recursiveperm(i, None)

    def check_03(self):
        assert bargraph(self.data1, height=50, leftOffset=4, rightOffset=3, valueDivisor=None) == '-7  *   1\n-6  **   6\n-5  ******   34\n-4  ************************   141\n-3  ********************************************   262\n-2  ***************************************************   303\n0   ******************************   176\n2   ***********   62\n3   ***   14\n4   *   1\n'

    def check_04(self):
        assert bargraph(self.data1, height=10, leftOffset=4, rightOffset=3, valueDivisor=None) == '-7  *   1\n-6  *   6\n-5  **   34\n-4  *****   141\n-3  *********   262\n-2  ***********   303\n0   ******   176\n2   ***   62\n3   *   14\n4   *   1\n' 

    def check_05(self):
        assert bargraph(self.data1, height=40, leftOffset=8, rightOffset=3, valueDivisor=None) == '-7      *   1\n-6      *   6\n-5      *****   34\n-4      *********************   141\n-3      **************************************   262\n-2      ********************************************   303\n0       **************************   176\n2       *********   62\n3       ***   14\n4       *   1\n'
        
    def check_06(self):
        assert bargraph(self.data1, height=40, leftOffset=5, rightOffset=12, valueDivisor=None) == '-7   *            1\n-6   *            6\n-5   *****            34\n-4   *********************            141\n-3   **************************************            262\n-2   ********************************************            303\n0    **************************            176\n2    *********            62\n3    ***            14\n4    *            1\n'
        
    def check_07(self):
        assert bargraph(self.data1, height=50, leftOffset=4, rightOffset=3, valueDivisor=1000) == '-7  *   0.1 %\n-6  **   0.6 %\n-5  ******   3.4 %\n-4  ************************   14.1 %\n-3  ********************************************   26.2 %\n-2  ***************************************************   30.3 %\n0   ******************************   17.6 %\n2   ***********   6.2 %\n3   ***   1.4 %\n4   *   0.1 %\n'

    def check_08(self):
        assert bargraph(self.data2, height=50, leftOffset=4, rightOffset=3, valueDivisor=1000) == '-9  *   0.1 %\n-6  **   0.6 %\n-5  **********************************   13.4 %\n-4  **************************   10.1 %\n-3  *****************************************   16.2 %\n-1  ***************************************************   20.3 %\n0   ***********   4.0 %\n1   **********   3.6 %\n4   **************************   10.1 %\n5   *****************************************   16.2 %\n10  *****************************   11.4 %\n'

    def check_09(self):
        assert bargraph(self.data3, height=50, leftOffset=4, rightOffset=3, valueDivisor=None) == '3   **************************************************   1000\n'
        
    def check_10(self):
        assert bargraph(self.data3, height=50, leftOffset=4, rightOffset=3, valueDivisor=1000) == '3   **************************************************   100.0 %\n'

    def check_11(self):
        rt = RangeTable()
        assert str(rt) == '{}'      
        
    def check_12(self):
        d  = {2: 1, 3: 2, 5: 3}
        rt = RangeTable(dictionary=d)
        for k, v in d.items():
            assert k in rt._upperLimits
            assert k in rt.keys()
            assert v in rt.values()
    
    def check_13(self):
        rt = RangeTable({2: (2, 'two'), 3: (4, 'four'), 5: (8, 'eight')})
        assert rt._nextLimit(0) == 2
        assert rt._nextLimit(1) == 2
        assert rt._nextLimit(2) == 2
        assert rt._nextLimit(3) == 3
        assert rt._nextLimit(4) == 5
        assert rt._nextLimit(5) == 5

    def check_14(self):
        d  = {1:'Kether', 2:'Chokmah', 3:'Binah', 4:'Chesed', 5:'Geburah', 6:'Tiphereth', 7:'Netzach'}
        rt = RangeTable(d)
        assert rt.uppermostLimit == 7
        rt[8]  = 'Hod'
        rt[9]  = 'Yesod'
        rt[10] = 'Malkuth'
        assert rt.uppermostLimit == 10

    def check_15(self):
        rt = RangeTable(dictionary={2: 2, 3: 4, 5: 8})
        assert rt[0] == 2
        assert rt[1] == 2
        assert rt[2] == 2
        assert rt[3] == 4
        assert rt[4] == 8
        assert rt[5] == 8

    def check_16(self):
        d  = {0: 1, 1: 'one', 2: (2,), 3: {6: 720}, 4: 24, 5: 120.0}
        rt = RangeTable(dictionary=d)
        for k, v in d.items():
            assert rt[k] == v
            
    def check_17(self):
        rt = RangeTable({1: 1, 2: 7})
        assert rt[2] == 7
        rt[2] = 6
        assert rt[2] == 6
        rt[3] = 14
        rt[4] = 8
        assert rt[3] == 14
        assert rt[4] == 8

    def check_18(self):
        rt = RangeTable({0: 9.0, 1: 6.7, 2: 2, 3: 6, 4: ('6', 6)})        
        assert 3 in rt._upperLimits
        del rt[3]
        assert 3 not in rt._upperLimits

    def check_19(self):
        rt = RangeTable({4: 'Marlow', 13: 'Nostromo', 18: 'Jim', 19: 'Wait'})
        assert rt.has_key(7)
        assert rt.has_key(18)
        assert not rt.has_key(40)
        assert not rt.has_key(580)
        assert not rt.has_key('Kurtz')
    
    def check_20(self):
        rt = RangeTable({0: 1, 2: 1, 4: 2, 6: 3, 8: 5})
        assert len(rt) == 5
        assert len(rt._upperLimits) == 5
        rt.clear()
        assert len(rt) == 0
        assert len(rt._upperLimits) == 0
    
    def check_21(self):
        rt = RangeTable({1415: 'Agincourt', 1690: 'Boyne', 1805: 'Trafalgar'})
        assert 1415 in rt
        assert 1415 in rt._upperLimits
        assert len(rt) == 3
        assert len(rt._upperLimits) == 3
        assert rt.pop(1415) == 'Agincourt'
        assert 1415 not in rt
        assert 1415 not in rt._upperLimits
        assert 1690 in rt
        assert rt.pop(1690) == 'Boyne'
        assert 1690 not in rt
        assert 1690 not in rt._upperLimits
        rt[1815] = 'Waterloo'
        assert 1805 in rt
        assert 1815 in rt
        assert 1815 in rt._upperLimits
        assert len(rt) == 2
        assert rt.pop(1805) == 'Trafalgar'
        assert rt.pop(1815) == 'Waterloo'
        assert 1805 not in rt
        assert 1815 not in rt
        assert 1805 not in rt._upperLimits
        assert 1815 not in rt._upperLimits
        assert len(rt) == 0
        assert len(rt._upperLimits) == 0

    def check_22(self):
        rt1 = RangeTable({2: (0, 2), 3: (1, 0), 5: (1, 2), 7: (2, 1), 11: (3, 2), 13: (4, 1)})
        rt2 = rt1.copy()
        while len(rt1) > 0:
            key, value = rt1.popitem()
            assert rt2[key] == value
            assert key, value in rt2.items()
        assert len(rt1) == 0
        assert len(rt1._upperLimits) == 0

    def check_23(self):
        rt = RangeTable({2: (1,), 5: (0, 0, 1), 8: (3, 0, 0)})
        d  = {3: (0, 1), 4: (2, 0), 6: (1, 1, 0), 7:(0, 0, 0, 1)}
        assert 2 in rt
        assert 6 not in rt
        assert rt._upperLimits.index(8) == 2
        rt.update(d)
        assert 2 in rt
        assert 3 in rt._upperLimits
        assert rt[4] == (2, 0)
        assert rt[5] == (0, 0, 1)
        assert 6 in rt._upperLimits
        assert rt.has_key(7)
        assert rt._upperLimits.index(8) == 6
        assert 9 not in rt._upperLimits
        assert not rt.has_key(10)

    def check_24(self):
        assert rotate([[]]) == []
    
    def check_25(self):
        assert rotate([[[],[],[]],[[],[]],[[]]]) == [[[],[],[]],[[],[]],[[]]]
    
    def check_26(self):
        assert rotate([[[]],[]]) == [[[]]]
        
    def check_27(self):
        assert rotate([[[[],[]]],[[],[],[],[]]]) == [[[[],[]],[]],[[]],[[]],[[]]]

    def check_28(self):
        assert rotate([[[[]],[]]]) == [[[[]]],[[]]]

    def check_29(self):
        assert rotate([[],[[]],[]]) == [[[]]]

    def check_30(self):
        assert rotate([[[],[[]],[]],[],[],[]]) == [[[]],[[[]]],[[]]]

    def check_31(self):
        assert rotate([[],[],[],[],[],[[]],[]]) == [[[]]]

    def check_32(self):
        assert rotate([[],[[]],[],[[[],[]]],[],[[]],[]]) == [[[],[[],[]],[]]]
    
    def check_33(self):
        assert rotate([[((),)]]) == [[((),)]]
        
    def check_34(self):
        assert rotate([[((),),((),())]]) == [[((),)],[((),())]]
       
    def check_35(self):
        assert rotate([[((),)],[((),())]]) == [[((),),((),())]]

    def check_36(self):
        assert rotate([[((),),((),()),(([]),)],[(([]),()),(([]),([],)),(([()]),([],)), 
                     (([()]),([()],))],[(([(),()]),([()],)),(([(),()]),([(),()],)),(([(),
                     (),()]),([(),()],)),(([(),(),([],)]),([(),()],)),(([(),(),([],)]),
                     ([([],[],[]),()],))]]) == [[((),),(([]),()),(([(),()]),([()],))], 
                     [((),()),(([]),([],)),(([(),()]),([(),()],))],[(([]),),(([()]),
                     ([],)),(([(),(),()]),([(),()],))],[(([()]),([()],)),(([(),(),
                     ([],)]),([(),()],))],[(([(),(),([],)]),([([],[],[]),()],))]]

    def check_37(self):
        assert rotate([[((),),(([]),()),(([(),()]),([()],))],[((),()),(([]),([],)),(([(),
                     ()]),([(),()],))],[(([]),),(([()]),([],)),(([(),(),()]),([(),()],))], 
                     [(([()]),([()],)),(([(),(),([],)]),([(),()],))],[(([(),(),([],)]),([([],
                     [],[]),()],))]]) == [[((),),((),()),(([]),),(([()]),([()],)),(([(),(),
                     ([],)]),([([],[],[]),()],))],[(([]),()),(([]),([],)),(([()]),([],)), 
                     (([(),(),([],)]),([(),()],))],[(([(),()]),([()],)),(([(),()]),([(),()],)), 
                     (([(),(),()]),([(),()],))]]
 
                        
    def check_38(self):
        result = table([self.row01, self.row02, self.row03, self.row04], breakWidth=2)
        assert result == 'abacus  baby  Edgar Allen Poe  milk\njeep    king  leaf             nail\ncane    dog   fig              orange\ngrain   heap  igloo            pail\n'

    def check_39(self):
        result = table([self.row01, self.row03, self.row05, self.row07])
        assert result == 'abacus     baby   Edgar Allen Poe   milk\ncane       dog    fig               orange\n5          25     125               625\nEngland:   0      Wales:            1\n'

    def check_40(self):
        result = table([self.row07, self.row06, self.row05, self.row06])
        assert result == 'England:   0     Wales:   1\n2.0        1.0   3.0      4.0\n5          25    125      625\n2.0        1.0   3.0      4.0\n'

    def check_41(self):
        result = padzip(self.defaultArgument, self.data01, self.data02, self.data03)
        assert result == [[1, 'a', '!'], [2, 'c', '@'], [3, 'd', 'X'], [4, 'X', 'X']]
        
    def check_42(self):
        result = padzip(self.defaultArgument, self.data04, self.data01, self.data05)
        assert result == [[1, 1, 2], ['a', 2, 'b'], ['!', 3, '@'], ['X', 4, '%'], ['X', 'X', 5], ['X', 'X', 4]]
        
    def check_43(self):
        result = padzip(self.defaultArgument, self.data03, self.data01, self.data03, self.data05)
        assert result == [['!', 1, '!', 2], ['@', 2, '@', 'b'], ['X', 3, 'X', '@'], ['X', 4, 'X', '%'], ['X', 'X', 'X', 5], ['X', 'X', 'X', 4]]        
 
    def check_44(self):
        k1     = Keyword('Andy', self.fDict1)
        k2     = Keyword('Colin', self.fDict2, [k1])
        k3     = Keyword('Rohan', self.fDict3, [k1, k2])
        target = {'Marlow': 0.0, 'Hamlet': 0.0, 'Frodo': 0.0}
        assert target == {'Marlow': 0.0, 'Frodo': 0.0, 'Hamlet': 0.0}
        k1.pipe(self.source, target)
        assert target == {'Marlow': 0.40000000000000002, 'Frodo': 0.0, 'Hamlet': 0.80000000000000004}
        k2.pipe(self.source, target)
        assert target == {'Marlow': 5.8000000000000007, 'Frodo': 10.0, 'Hamlet': 1.6000000000000001}
        k3.pipe(self.source, target)
        assert target == {'Marlow': 11.600000000000001, 'Frodo': 220.0, 'Hamlet': 103.19999999999999}

    def check_45(self):
        assert scale(4.5, 0.4)       == (0.99607264069268653, 0.088539790283793759)
        assert scale(3.2, -5.6)      == (0.49613893835683387, -0.86824314212445919)
        assert scale(0.0, 5.23)      == (0.0, 1.0)
        assert scale(-4.3, 0.0, 2.5) == (-2.5, 0.0)
        assert scale(0.0, 0.0, 6.0)  == (0.0, 0.0)                

 
def suite():
    def numberSuffix(x,y):
        return cmp(x[-2:], y[-2:])
    
    suite1 = unittest.makeSuite(TestCase01, 'check', sortUsing = numberSuffix)
    alltests = unittest.TestSuite((suite1,))
    return alltests
    
def main():
    runner = unittest.TextTestRunner(descriptions = 0, verbosity = 2)
    runner.run(suite())
    
if __name__ == '__main__':
    main()