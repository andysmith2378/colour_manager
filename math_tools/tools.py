from math    import ceil, floor, fmod, sqrt
from pickle  import load




#   Arithmetic

def polynomial(x, coefficents):
    x = float(x)
    return reduce(float.__add__, [coeff * x ** power for power, coeff in enumerate(coefficents)])

def absceil(x):
    if x >= 0.0:
        return ceil(x)
    return floor(x)

def roundFloat(x, places=1):
    order = 10.0 ** places
    return int(x * order + 0.5) / order

def scale(x, y, length=1.0):
    if y != 0.0:
        c = abs(x / y)
        lengthSquare = length * length
        cSquare = c * c
        newX = cmp(length, 0.0) * cmp(x, 0.0) * sqrt((lengthSquare * cSquare) / (cSquare + 1.0))
        newXSquare = newX * newX
        squareDifference = lengthSquare - newXSquare
        if squareDifference > 0.0:
            newY = cmp(length, 0.0) * cmp(y, 0.0) * sqrt(squareDifference)
            return (newX, newY)
        return (newX, 0.0)
    if x != 0.0:
        return (cmp(x, 0.0) * length, 0.0)
    return (0.0, 0.0)     
    
def genscale(componentList, length=1.0):
    divisor = sqrt(sum([component * component for component in componentList]))
    if divisor == 0.0:
        return (0.0,) * len(componentList)
    return tuple([component * length / divisor for component in componentList])

def compoundFunction(*functions):
    functionList = list(functions)
    functionList.reverse()
    def result(argument, cutoff=None):
        partialResult = argument
        for funct in functionList:
            partialResult = funct(partialResult)
            if partialResult is None or ((cutoff is not None) and (abs(partialResult) >= cutoff)):
                return None
        return partialResult
    return result


#   Permutations

def genperm(sequencesequence):
    def advance(indexsequence, indexindex):
        indexsequence[indexindex] = 0
        indexsequence[indexindex + 1] += 1

    indices = [0] * len(sequencesequence)
    while indices[-1] < len(sequencesequence[-1]):
        result = [sequence[indices[n]] for n, sequence in enumerate(sequencesequence)]
        indices[0] += 1
        [advance(indices, n) for n, sequence in enumerate(sequencesequence[:-1]) if indices[n] == len(sequence)]
        yield result

def perm(numThings, indx = None):
    if numThings == 1:
        return [[1],]
    result = []
    lastPermSet = perm(numThings - 1, indx)
    for lastPerm in lastPermSet:
        for position in range(numThings):
            newPerm = lastPerm[:position]
            newPerm.append(numThings)
            newPerm += lastPerm[position:]
            result.append(newPerm)
    return result

def recursiveperm(numThings, indx = None):
    def newPermutation(position, lastPerm, numThings, result):
        newPerm = lastPerm[:position]
        newPerm.append(numThings)
        newPerm += lastPerm[position:]
        result.append(newPerm)
        return result

    def inLoop(lastIndx, newFunction, lastPermSet, numThings, result):
        return loop([], newFunction, 0, numThings, (lastPermSet[lastIndx], numThings, result))[0]

    if numThings == 1:
        return [[1],]
    result = []
    lastPermSet = recursiveperm(numThings - 1, indx)
    result = loop([], inLoop, 0, len(lastPermSet), (newPermutation, lastPermSet, numThings, result))[0]
    return result

def permsequence(listOfThings):
    return [[listOfThings[indx - 1] for indx in indices] for indices in perm(len(listOfThings))]        

def rangePair(*arguments):
    for one in range(*arguments):
        for two in range(*arguments):
            yield (one, two)



#   Control functions

def loop(resultList, body, indx, upperBound, otherArguments):
    if indx == upperBound:
        return resultList
    else:
        resultList.append(body(indx, *otherArguments))
        loop(resultList, body, indx + 1, upperBound, otherArguments)
        return resultList

def twirl(sequence, function):
    return [sum(member) for member in zip(*[function(element) for element in sequence])]



#   Containers

class RangeTable(dict):
    def __init__(self, dictionary = None):
        if dictionary:
            dict.__init__(self, dictionary)
        else:
            dict.__init__(self)
        self._setLimits()

    def getUppermostLimit(self):
        return self._upperLimits[-1]
    uppermostLimit = property(getUppermostLimit)

    def __getitem__(self, ind):
        """ Overrides dict.__getitem__() """
        key = self._nextLimit(ind)
        if key is not None:
            return dict.__getitem__(self, key)
        raise "KeyError"

    def __setitem__(self, ind, item):
        """ Overrides dict.__setitem__() """
        dict.__setitem__(self, ind, item)
        if ind not in self._upperLimits:
            self._upperLimits.append(ind)
            self._upperLimits.sort()

    def __delitem__(self, ind):
        """ Overrides dict.__delitem__() """
        dict.__delitem__(self, ind)
        list.__delitem__(self._upperLimits, ind)

    def has_key(self, key):
        """ Overrides dict.has_key() """
        ind = self._nextLimit(key)
        if ind is not None:
            return dict.has_key(self, ind)
        return None

    def clear(self):
        """ Overrides dict.clear() """
        dict.clear(self)
        self._upperLimits = []

    def pop(self, key):
        """ Overrides dict.pop() """
        value = dict.pop(self, key)
        self._upperLimits.remove(key)
        return value

    def popitem(self):
        """ Overrides dict.popitem() """
        key, value = dict.popitem(self)
        self._upperLimits.remove(key)
        return (key, value)

    def update(self, dictionary):
        """ Overrides dict.update() """
        dict.update(self, dictionary)
        self._setLimits()

    def _nextLimit(self, ind):
        for limit in self._upperLimits:
            if ind <= limit:
                return limit
        return None

    def _setLimits(self):
        self._upperLimits = list(dict.keys(self))
        self._upperLimits.sort()



#   Structures

def relationshipMeld(*instances):
    def prefix(objcts, ind):
        idString = ""
        for i in range(len(objcts)):
            idString += str(id(objcts[i]))
        return '_' + idString + '_'

    class Intersection(tuple):
        def __new__(cls, *arguments):
            return tuple.__new__(cls, arguments)

        def __setattr__(self, attributeName, attributeValue):
            self._pad(attributeName, attributeValue, '__setattr__')

        def __getattr__(self, attributeName):
            if hasattr(self, attributeName):
                return object.__getattr__(attributeName)
            pool = fusion(*self)
            if pool.has_key(attributeName):
                return pool[attributeName]
            raise AttributeError

        def __delattr__(self, attributeName):
            self._pad(attributeName, None, '__delattr__')

        def _pad(self, attributeName, attributeValue, objectMethod):
            for indx in range(len(self)):
                member     = self[indx]
                paddedName = prefix(self, indx) + attributeName
                if attributeValue is not None:
                    getattr(member, objectMethod)(paddedName, attributeValue)
                else:
                    getattr(member, objectMethod)(paddedName)
            if attributeValue is not None:
                getattr(object, objectMethod)(self, attributeName, attributeValue)
            else:
                getattr(object, objectMethod)(self, attributeName)

    def fusion(*objects):
       result       = {}
       potentials   = {}
       orderedUnion = []
       for indx in range(len(objects)):
           orderedUnion.append([])
           inst = objects[indx]
           pfix = prefix(objects, indx)
           for attribName, attribValue in inst.__dict__.items():
               if attribName.startswith(pfix):
                   strippedName             = attribName[len(pfix):]
                   potentials[strippedName] = attribValue
                   orderedUnion[indx].append(strippedName)
       for possibleAttribute, possibleValue in potentials.items():
           actualFlag = True
           for attribSequence in orderedUnion:
               if possibleAttribute not in attribSequence:
                   actualFlag = False
                   break
           if actualFlag:
               result[possibleAttribute] = possibleValue
       return result

    intersectionInstance = Intersection(*instances)
    intersectionInstance.__dict__.update(fusion(*instances))
    return intersectionInstance

r = relationshipMeld

def evaluableNames(*toponyms):
    class NamedInteger(int):
        def __init__(self, value, toponym):
            self.toponym = toponym

        __new__ = lambda x, y, z: int.__new__(x, y)
        __str__ = lambda x: x.toponym

    class ValueList(object):
        def names():
            result = ValueList.__dict__.keys()
            map(lambda x: result.remove(x), ('names', '__iter__', '__module__', '__doc__'))
            return result

        def __iter__(self):
            for nym in toponyms:
                yield getattr(self, nym)

        names   = staticmethod(names)
        __len__ = lambda x: len(toponyms)

    [setattr(ValueList, toponyms[indx], NamedInteger(indx, toponyms[indx])) for indx in range(len(toponyms))]
    return ValueList  

class Metalink(type):
    unlinkedPrefix = '_unlinked_'

    def __init__(cls, identity, bases, dictionary):
        [cls.chainMethod(methodName) for methodName in dictionary['linkedMethods']]

    def chainMethod(cls, methodName):
        def chainVersion(self, *arguments, **keywordArguments):
            getattr(self, Metalink.unlinkedPrefix + methodName)(*arguments, **keywordArguments)
            [child.linkMethod(*arguments, **keywordArguments) for child in self.children]
        setattr(cls, methodName, chainVersion)

class Link(object):
    __metaclass__ = Metalink
    linkedMethods = []

    def __init__(self, children):
        self.children = children

    def linkMethod(self, *arguments, **keywordArguments):
        [getattr(self, method)(*arguments, **keywordArguments) for method in self.__class__.linkedMethods]

class Keyword(str, Link):
    linkedMethods = ['pipe']

    def __new__(self, stringvalue, factorDictionary, children=[]):
        return str.__new__(self, stringvalue)

    def __init__(self, stringvalue, factorDictionary, children=[]):
        Link.__init__(self, children)
        self.factorDictionary = factorDictionary

    def _unlinked_pipe(self, source, target, *otherArguments, **otherKeywordArguments):
        sourceValue = source.get(self, 0.0)
        [target.__setitem__(key, target[key] + sourceValue * factor) for key, factor in self.factorDictionary.items()]

class Weir(Keyword):
    linkedMethods = ['pipe']

    def _unlinked_pipe(self, source, target):
        target += [self for key, limit in self.factorDictionary.items() if source[key] > limit]



#   Text display

def table(rowlist, breakWidth=3, breakChar=" "):
    width  = {}
    result = ''
    for row in rowlist:
        for n, cell in enumerate(row):
            cellLength = len(str(cell))
            if width.has_key(n):
                width[n] = max(width[n], cellLength)
            else:
                width[n] = cellLength
    for row in rowlist:
        for n, cell in enumerate(row):
            cellString = str(cell)
            result    += cellString + breakChar*(breakWidth + width[n] - len(cellString))
        result = result.strip() + "\n"
    return result

def bargraph(dataDictionary, height=50, leftOffset=4, rightOffset=3, valueDivisor=None):
    def bar(prefix, suffix, leftOff, rightOff, length):
        return prefix + ' ' * (leftOff - len(prefix)) + '*' * length + ' ' * rightOff + suffix + '\n'

    def barseries(suffixFunction, data, dKeys, spread, leftOff, rightOff, divisor=None):
        return reduce(str.__add__, [bar(rowString, suffixFunction(data[row], divisor), leftOff, rightOff,
                     ((data[row] / spread) + 1)) for row, rowString in zip(dKeys, [str(k) for k in dKeys])])

    assert valueDivisor is None or valueDivisor >= 1000
    dataValues = dataDictionary.values()
    ySpread    = (max(dataValues) - min(dataValues)) / height
    dataKeys   = dataDictionary.keys()
    if ySpread == 0:
        row = dataKeys[0]
        if valueDivisor is None:
            suffix = str(dataDictionary[row])
        else:
            suffix = '100.0 %'
        return bar(str(row), suffix, leftOffset, rightOffset, height)
    dataKeys.sort()
    if valueDivisor is None:
        return barseries(lambda x, y: str(x), dataDictionary, dataKeys, ySpread, leftOffset, rightOffset)
    return barseries(lambda x, y: "%#3.1f %%" % (ceil(1000.0 * x / y) / 10.0), dataDictionary, dataKeys,
                     ySpread, leftOffset, rightOffset, valueDivisor)




#   Colours

class Span(object):
    colourDictionary = {
        'silk'               : lambda ind, object : object.silkColour(ind / float(object.numColours), 2.0, 2.0, 2.0) ,
        'unlimited'          : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0) ,
        'water'              : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1) ,
        'autumn'             : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2) ,
        'brass'              : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0) ,
        'slick'              : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1) ,
        'emerald'            : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0) ,
        'sharp'              : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 1, 2, Span._sharpValue) ,
        'liquid'             : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1, Span._sharpValue) ,
        'rust'               : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2, Span._sharpValue) ,
        'fire'               : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0, Span._sharpValue) ,
        'shine'              : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1, Span._sharpValue) ,
        'moss'               : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0, Span._sharpValue) ,
        'sleek'              : lambda ind, object : object.silkColour(object._modFraction(ind), 2.0, 2.0, 4.0) ,
        'pale_silk'          : lambda ind, object : object.silkColour(object._modFraction(ind), 2.1, 1.4, 2.1) ,
        'pale'               : lambda ind, object : object.paleColour(ind, 0.75, 1.0, 0.4) ,
        'warm'               : lambda ind, object : object.warmColour(ind, object.bright / 3.0, 0.9, 0.2, 0.65, 0.8, 0.7, 3.2) ,
        'pink'               : lambda ind, object : object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.8, 0.4, 0.55, 1.6, 0.6, 6.4) ,
        'bronze'             : lambda ind, object : object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8) ,
        'ruddy'              : lambda ind, object : object.splitColour(ind, 0.375, 0.4, 1.2, 0.15, 4.8, 1.125, 0.2, 19.2) ,
        'hard_spiral'        : lambda ind, object : object.hardColour(ind, 8.0, lambda x, y : x) ,
        'soft_spiral'        : lambda ind, object : object.softColour(ind, 8.0, lambda x, y : x) ,
        'balanced_cube'      : lambda ind, object : object.hardColour(ind, 8.0, lambda x, y : 0.5 + (4.0 * ((x - 0.5) ** 3))) ,
        'magenta_cube'       : lambda ind, object : object.hardColour(ind, 8.0, lambda x, y : {0 : 0.5 + (4.0 * ((x - 0.5) ** 3)), 1 : x, 2 : x}[y]) ,
        'yellow_cube'        : lambda ind, object : object.hardColour(ind, 8.0, lambda x, y : {0 : x, 1 : 0.5 + (4.0 * ((x - 0.5) ** 3)), 2 : x}[y]) ,
        'cyan_cube'          : lambda ind, object : object.hardColour(ind, 8.0, lambda x, y : {0 : x, 1 : x, 2 : 0.5 + (4.0 * ((x - 0.5) ** 3))}[y]) ,
        'balanced_soft_cube' : lambda ind, object : object.softColour(ind, 8.0, lambda x, y : 0.5 + (4.0 * ((x - 0.5) ** 3))) ,
        'magenta_soft_cube'  : lambda ind, object : object.softColour(ind, 8.0, lambda x, y : {0 : 0.5 + (4.0 * ((x - 0.5) ** 3)), 1 : x, 2 : x}[y]) ,
        'yellow_soft_cube'   : lambda ind, object : object.softColour(ind, 8.0, lambda x, y : {0 : x, 1 : 0.5 + (4.0 * ((x - 0.5) ** 3)), 2 : x}[y]) ,
        'cyan_soft_cube'     : lambda ind, object : object.softColour(ind, 8.0, lambda x, y : {0 : x, 1 : x, 2 : 0.5 + (4.0 * ((x - 0.5) ** 3))}[y]) ,
        'black_rgbcmy'       : lambda ind, object : object.polyColour(ind, 6.0, (3.0357142857166299, 737.37499999998204, -695.93749999998204, 217.81249999999301, -26.562499999998899, 1.0624999999999301) ,  (-8.5551948051937394, 65.102272727257201, -27.528409090889799, 32.357954545446198, -11.107954545453101, 1.0624999999999101) ,  (3.0357142857191199, -6.3750000000082103, -69.062499999994898, 69.062499999998394, -15.937499999999799, 1.06249999999999)) ,
        'white_rgbcmy'       : lambda ind, object : object.polyColour(ind, 6.0, (251.964285714287, -261.37500000001103, -26.562499999987001, 69.0624999999946, -15.937499999999099, 1.06249999999994) ,  (8.5551948052001006, 517.14772727271804, -450.59659090908701, 148.26704545454501, -20.7670454545454, 1.0625) ,  (3.0357142857191199, -6.3750000000082103, -69.062499999994898, 69.062499999998394, -15.937499999999799, 1.06249999999999)) ,
        'grey_rgbcmy'        : lambda ind, object : object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) ,
        'black_rgb'          : lambda ind, object : object.polyColour(ind, 3.0, (38.249999999999901, 165.75, -63.75) ,  (-38.25, 216.75, -63.75) ,  (12.75, -114.75, 63.75)) ,
        'white_rgb'          : lambda ind, object : object.polyColour(ind, 3.0, (255.0, -382.5, 127.5) ,  (51.0, 51.0, -1.8756697583999199e-015) ,  (-25.5, 102.0, -9.6790057275126193e-015)) ,
        'grey_rgb'           : lambda ind, object : object.polyColour(ind, 4.0, (10.9285714285711, 500.89285714285802, -364.28571428571502, 63.750000000000099) ,  (-25.500000000000099, 233.75, -127.5, 21.25) ,  (10.9285714285714, -179.107142857143, 145.71428571428601, -21.25) ) ,
        'black_ymc'          : lambda ind, object : object.polyColour(ind, 3.0, (-1.9873011852667399e-169, 382.5, -127.5) ,  (51.0, 51.0, -1.8756697583999199e-015) ,  (-25.5, 102.0, -9.6790057275126193e-015) ) ,
        'white_ymc'          : lambda ind, object : object.polyColour(ind, 3.0, (293.25, -216.75, 63.75) ,  (216.75, -165.75, 63.75) ,  (12.75, 267.75, -63.75) ) ,
        'grey_ymc'           : lambda ind, object : object.polyColour(ind, 4.0, (-10.9285714285714, 646.607142857143, -400.71428571428601, 63.75) ,  (25.5, 233.75, -127.5, 21.25) ,  (-10.9285714285714, -33.392857142857402, 109.28571428571399, -21.25) ) ,
        'slide'              : lambda ind, object : object.polyColour(ind, 8.0, (1.81235431926472, -575.91654183329297, 1831.3570318571799, -1478.3581730404501, 537.13675211555903, -99.312499995113697, 9.1111111106027796, -0.32886904759921498) ,  (0.18453767669757201, 1101.9707931373, -1651.55979668694, 913.11992518134105, -232.24715097807999, 28.590277773345299, -1.5601851847204899, 0.025297619029346501) ,  (0.61888111063391904, 1295.54453052125, -2389.13799533668, 1709.86298072006, -603.58974356087401, 111.73749999324799, -10.3666666659543, 0.37946428568613699) ) ,
        'tangerine'          : lambda ind, object : object.polyColour(ind, 4.0, (125.485714285714, 251.42857142857201, -182.857142857143, 32.0) ,  (67.200000000000003, 117.333333333333, -64.0, 10.6666666666667) ,  (65.485714285714295, -89.904761904761997, 73.142857142857196, -10.6666666666667) ) ,
        'amethyst'           : lambda ind, object : object.polyColour(ind, 9.0, (0.55664335664339, 43.8912198912198, -4.69638694638693, 0.269036519036518), (-9.91361559223872E-03, -466.88848181749, 1091.06770182383, -918.083355323809, 387.264644605019, -90.2741094765932, 11.7995098038869, -0.809442110178009, 2.26686507937573E-02), (4.95888522953844, 887.331564592294, -1796.23019754885   , 1493.28384866374 , -630.26283189476, 147.294285125609 , -19.2936989367522 , 1.32531804376938, -3.71403769799287E-02)) ,
        'peach'              : lambda ind, object : object.polyColour(ind, 10.0, (2.00148319905218, 25.128746197997899, 70.597567772986807, -93.489213795030494, 51.433394313059203, -14.951826352151899, 2.4931209685633902, -0.24030560673780299, 0.012472586622306501, -0.00027006170177582402) ,  (-0.017229319024289699, 276.069696435183, -599.80749128679201, 574.06767791094796, -286.44042029161199, 81.883452899456401, -13.892518403974201, 1.3818220323796599, -0.074376688342424294, 0.0016713512016449401) ,  (10.02784736778, -750.97962255013999, 1887.82041927772, -1760.2733013158099, 846.49430092030298, -234.735097583726, 38.995408042183598, -3.8284213055216898, 0.20462090097556701, -0.00458553727974531)) ,
        'ametrine'           : lambda ind, object : object.polyColour(ind, 11.0, (5.5018315018315, 50.240574240574198, -7.8753468753468798, 0.48692048692048701) ,  (0.011370270415339299, 318.45977712590502, -636.15106229686398, 631.264420389772, -358.00092451904101, 123.753541046267, -26.8269111977284, 3.6540958980244702, -0.303068604318733, 0.013961882913996901, -0.00027350639223039201) ,  (-0.0050538490573181598, 1659.7335806477199, -3886.42736723907, 3711.23972291993, -1892.4950389278799, 574.94735494577105, -109.050287223918, 13.0265845400905, -0.95210900893849304, 0.038883540924870799, -0.00067970126858454404)) ,
        'bittersweet'        : lambda ind, object : object.polyColour(ind, 11.0, (-2.8350281457388599e-005, 53.684373801873697, -27.6936659074806, 15.8506722579239, -5.90201476845795, 1.14267829306482, -0.073157975628387897, -0.0107364298198518, 0.00235142622718815, -0.00016462215490623599, 4.1335974703717298e-006) ,  (0.044190020185951397, -243.170510987391, 848.11511608259605, -933.64481714611202, 528.68148878157695, -174.998328997139, 35.690347329828001, -4.5393577453710297, 0.35053824943855399, -0.0150294664401288, 0.00027433310846011402) ,  (8.0930692736682399, 3.3389555217229199, 425.53684970952497, -711.78539051734595, 517.46917772968595, -202.04407191523001, 46.2758096423902, -6.4140930274139203, 0.52942235573989904, -0.023947047766939001, 0.00045690034856080201)) ,
        'butterscotch'       : lambda ind, object : object.polyColour(ind, 11.0, (0.00028326228980435797, 171.60189703551001, -148.76860184638801, 102.03421048454901, -43.954886162615203, 11.959213913769799, -2.0952146072505, 0.23580351285349799, -0.0164623501169055, 0.00064864689456652102, -1.10229300345892e-005) ,  (1.9790893626600901, -297.66621807288902, 943.94947519080199, -957.93499502907002, 501.91109618409098, -153.94647139112101, 29.151055944890999, -3.4522857722968099, 0.24911865357427501, -0.0100215141718955, 0.00017237102704012) ,  (6.9944195610714699, -2067.7184358009299, 5567.9404089162799, -5746.2771701650699, 3090.0780397018002, -974.29512988591603, 189.83778053400101, -23.148962662084699, 1.7204485946211501, -0.071271132961203104, 0.00126171184353297) ) ,
        'periwinkle'         : lambda ind, object : object.polyColour(ind, 11.0, (-0.00047497773299858502, -40.3648149739075, 125.038080176056, -117.941535452254, 62.865139372997596, -20.144248447720202, 4.0196811711382203, -0.50348152821659198, 0.038489405392055698, -0.0016410055101301799, 2.9899690383007699e-005) ,  (0.039724062911812803, 1676.5840434433401, -4225.81408378383, 4257.8792001026004, -2259.9963900395401, 709.81104437720103, -138.78563480542701, 17.0780819205788, -1.28612261280841, 0.054143537595820003, -0.00097594244875772005) ,  (0.056254738552211997, 1686.0362048075201, -4311.9731203687497, 4368.3084274439097, -2316.77856008157, 724.58104843525996, -140.826059479067, 17.211118098479101, -1.28695080849652, 0.053797201138845001, -0.000963128295253347) ) ,
        'arabian'            : lambda ind, object : object.polyColour(ind, 11.0, (3.6805900918122897e-005, 21.227575880321599, 47.931299144607401, -72.098196269194005, 46.369916047304898, -16.567608240120698, 3.5767979982389901, -0.47693300469320599, 0.038381636603850702, -0.0017077007811613699, 3.22420623973061e-005) ,  (0.0070593262004717602, 1076.3520469241, -2512.3082558736901, 2385.2403755116802, -1219.82747058323, 374.52085587107899, -72.248817411956296, 8.8201893926726207, -0.66084419076046097, 0.027704159996116199, -0.00049713403159139702) ,  (0.027949938606128599, 1288.8006986728101, -3045.5870760350099, 2907.4479351517298, -1488.78824182928, 456.86699118334701, -88.043205001491003, 10.738594771219701, -0.80421301224208697, 0.033719758670014498, -0.00060557208115862102) ) ,
        'zircon'             : lambda ind, object : object.polyColour(ind, 11.0, (1.9994541292815899, 97.335206884518499, -76.501451210492903, 25.740018584283, 3.2031745197874502, -5.2956985337876903, 1.8126225863460099, -0.31660320799133002, 0.030834572732514699, -0.00158890905100123, 3.37577148508431e-005) ,  (11.0045533989497, -671.52670107746496, 1844.44113430894, -1780.60265328116, 874.79319212860196, -249.31658355006101, 43.592034764915603, -4.7345511884723104, 0.31053712482752199, -0.011219306071016601, 0.000170579799418555) ,  (7.9905989605094003, -914.54023424658806, 2542.1095310106102, -2515.92677824374, 1269.6986631547099, -372.27107005387097, 67.074524920807406, -7.52430398286418, 0.51141462633889501, -0.019239010762693399, 0.00030671295439500698) ) ,
        'lemon'              : lambda ind, object : object.polyColour(ind, 11.0, (-0.00076117996877593996, 50.657479140973997, -40.058409095700199, 27.0749993385304, -11.0894105013996, 2.8460800760203502, -0.468696028753123, 0.050478785385937301, -0.0035333408717828801, 0.00014910481182666099, -2.89351931753768e-006) ,  (1.03154635626008, 29.4435338148343, 82.193754036067801, -121.119703479534, 77.458395661895693, -27.4873217341867, 5.8337319372368501, -0.75747813423696297, 0.059018918845192697, -0.0025368480002493999, 4.6296294586718502e-005) ,  (0.027648600378010701, -1580.1215496897, 4137.6528231567499, -4188.3644494074497, 2245.6543195848699, -716.09877588195297, 142.479719796897, -17.842298492901499, 1.3656899416869599, -0.058324540528082502, 0.00106426365429228) ) ,
        'salmon'             : lambda ind, object : object.polyColour(ind, 11.0, (4.67816160084048e-005, 130.49786651775901, -98.847659142599696, 48.548659728813199, -14.689335545574901, 2.8035526122185601, -0.33733776911740798, 0.024650888648146699, -0.00097228185902058304, 1.34834302753397e-005, 1.3778604846242401e-007) ,  (0.053111839029008998, 670.84258348958394, -1462.4514806796501, 1388.20861872252, -711.04681051369698, 215.99224538048301, -40.630520770415401, 4.7758905415630002, -0.341186870441677, 0.0135445206689728, -0.00022913910682986901) ,  (11.0531516378327, 211.02969589176601, -327.55006906238299, 267.682831911454, -124.75239994146, 33.824892987288102, -5.3162365282098101, 0.46186405508716299, -0.0184603530696082, 4.6486601569094799e-005, 1.25385792970179e-005) ) ,
        'sunset'             : lambda ind, object : object.polyColour(ind, 11.0, (-5.8227442708578703e-005, 61.214771703544997, -52.114569145449799, 42.036107795234699, -20.051894860533299, 5.9051796666573804, -1.1145585588217899, 0.13548741795048899, -0.010258114235099799, 0.00043957208752041702, -8.1294101932669107e-006) ,  (-0.018292457584570099, -369.899982622327, 1620.1196805070599, -1941.5169861448301, 1119.24124736822, -368.28563922719002, 74.209053304852205, -9.3329150897863808, 0.71502739285934303, -0.030535215285148801, 0.00055720898762603099) ,  (0.0077850915759022704, 978.78406176704095, -2023.5144826348601, 1926.40933123527, -1041.4913360016601, 342.94790834545103, -70.663607430827398, 9.1182547882730702, -0.71394084834711202, 0.030957564099817699, -0.00056960978372742302) ) ,
        'apricot'            : lambda ind, object : object.polyColour(ind, 255.0, (-2.5804074896801499, 2.4502272689561901, -0.037038441729460199, 0.00024777070529063202, 9.9371471664329705e-006, -2.8285763584043501e-007, 3.33944195793395e-009, -2.1608132086367399e-011, 7.9618528091256205e-014, -1.5667728689377699e-016, 1.2777556958372501e-019) ,  (40.243415456840303, -11.349282254576501, 1.4579307875116301, -0.072215169155821796, 0.00184961205619947, -2.7400793223153301e-005, 2.47698045264638e-007, -1.38619207438381e-009, 4.6847298388144997e-012, -8.7559878908869306e-015, 6.9470432554704293e-018) ,  (21.8259376290831, -2.1637148177651202, 0.43378993025100498, -0.022343331173210499, 0.000574922473283908, -8.4381792629057005e-006, 7.4911023364613596e-008, -4.0885703836338099e-010, 1.33924048985793e-012, -2.4118983018661001e-015, 1.8335794306971501e-018) ) ,
        'thea'               : lambda ind, object : object.polyColour(ind, 4898.0, (38.6163342703931, 3.52960945578193E-02, 1.97649736331153E-04, -6.62610980543087E-07, 9.47957505377445E-10, -7.60635557147666E-13, 3.7036175951177E-16, -1.11289388601947E-19, 2.01331419599276E-23, -2.00925196427511E-27, 8.49771597357908E-32), (7.76853640597202, 6.82746309113932E-02, 5.66619812017531E-05, -4.39381101189964E-07, 7.83759960108692E-10, -7.12082383041518E-13, 3.763656288968E-16, -1.19883400934137E-19, 2.26651371000468E-23, -2.34304684719006E-27, 1.02062396271791E-31), (8.57794780575146, 0.103608929866892, -1.33402974818553E-04, -1.17592515619097E-08, 2.51555252393189E-10, -3.18016943318326E-13, 1.96028280540034E-16, -6.84930111978641E-20, 1.37960995893249E-23, -1.49505180312647E-27, 6.75938366281296E-32)) ,
        'red_malevich'       : lambda ind, object : object.tableColour(Span.malevichTable, ind, 0, 1, 2) ,
        'red_blue_malevich'  : lambda ind, object : object.tableColour(Span.malevichTable, ind, 0, 2, 1) ,
        'blue_malevich'      : lambda ind, object : object.tableColour(Span.malevichTable, ind, 2, 1, 0) ,
        'blue_red_malevich'  : lambda ind, object : object.tableColour(Span.malevichTable, ind, 2, 0, 1) ,
        'green_malevich'     : lambda ind, object : object.tableColour(Span.malevichTable, ind, 1, 0, 2) ,
        'green_blue_malevich': lambda ind, object : object.tableColour(Span.malevichTable, ind, 1, 2, 0) ,
        'red_thermal'        : lambda ind, object : object.tableColour(Span.thermalTable, ind, 0, 1, 2) ,
        'red_blue_thermal'   : lambda ind, object : object.tableColour(Span.thermalTable, ind, 0, 2, 1) ,
        'blue_thermal'       : lambda ind, object : object.tableColour(Span.thermalTable, ind, 2, 1, 0) ,
        'blue_red_thermal'   : lambda ind, object : object.tableColour(Span.thermalTable, ind, 2, 0, 1) ,
        'green_thermal'      : lambda ind, object : object.tableColour(Span.thermalTable, ind, 1, 0, 2) ,
        'green_blue_thermal' : lambda ind, object : object.tableColour(Span.thermalTable, ind, 1, 2, 0) ,
        'dark_thermal'       : lambda ind, object : object.tableColour(Span.thermalTable, ind, 2, 1, 0, 0.64, 0.64, 2.0) ,
        'pale_thermal'       : lambda ind, object : object.tableColour(Span.thermalTable, ind, 2, 1, 0, 1.2, 0.8, 0.6) ,
        'red_rainbow'        : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 0, 1, 2) ,
        'blue_rainbow'       : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 2, 1, 0) ,
        'green_rainbow'      : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 1, 0, 2) ,
        'red_blue_rainbow'   : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 0, 2, 1) ,
        'blue_red_rainbow'   : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 2, 0, 1) ,
        'green_blue_rainbow' : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 1, 2, 0) ,
        'dark_rainbow'       : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 0, 2, 1, 0.64, 0.64, 2.0) ,
        'pale_rainbow'       : lambda ind, object : object.tableColour(Span.rainbowTable, ind, 0, 2, 1, 1.2, 0.8, 0.6) ,
        'cloudy'             : lambda ind, object : object.tableColour(Span.clayTable, ind, 2, 1, 0) ,
        'sky'                : lambda ind, object : object.tableColour(Span.clayTable, ind, 0, 1, 2) ,
        'dark_clay'          : lambda ind, object : object.tableColour(Span.clayTable, ind, 2, 1, 0, 0.64, 0.64, 2.0) ,
        'pale_clay'          : lambda ind, object : object.tableColour(Span.clayTable, ind, 2, 1, 0, 1.2, 0.8, 0.6) ,
        'jade'               : lambda ind, object : object.tableColour(Span.stoneTable, ind, 2, 1, 0) ,
        'sapphire'           : lambda ind, object : object.tableColour(Span.stoneTable, ind, 0, 2, 1) ,
        'dark_stone'         : lambda ind, object : object.tableColour(Span.stoneTable, ind, 2, 1, 0, 0.64, 0.64, 2.0) ,
        'pale_stone'         : lambda ind, object : object.tableColour(Span.stoneTable, ind, 2, 1, 0, 1.2, 0.8, 0.6) ,
        'arc'                : lambda ind, object : object.tableColour(Span.arcTable, ind, 0, 1, 2) ,        
        'red'                : lambda ind, object : object._matchTotal(ind, *object._colourRatio(ind, 'red')) ,
        'green'              : lambda ind, object : object._matchTotal(ind, *object._colourRatio(ind, 'green')) ,
        'blue'               : lambda ind, object : object._matchTotal(ind, *object._colourRatio(ind, 'blue')) ,
        'mixed'              : lambda ind, object : object._matchTotal(ind, *object._colourRatio(ind, 'mixed')) ,
        'sea'                : lambda ind, object : object.crossColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 1, 0, 2), Span.greencross | Span.bluecross) ,
        'gold'               : lambda ind, object : object.crossColour(ind, object.tableColour(Span.thermalTable, ind, 1, 0, 2), object.tableColour(Span.thermalTable, ind, 0, 1, 2), Span.redcross | Span.greencross) ,
        'rose'               : lambda ind, object : object.crossColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 0, 1, 2), Span.redcross | Span.bluecross) ,
        'pastel'             : lambda ind, object : object.crossColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.tableColour(Span.thermalTable, ind, 2, 1, 0), Span.redcross | Span.greencross | Span.bluecross) ,
        'copper'             : lambda ind, object : object.metalColour(ind, object.tableColour(Span.thermalTable, ind, 0, 1, 2), object.tableColour(Span.thermalTable, ind, 1, 0, 2)) ,
        'steel'              : lambda ind, object : object.metalColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.paleColour(ind, 0.75, 1.0, 0.4)) ,
        'smoke'              : lambda ind, object : object.blendColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'mist'               : lambda ind, object : object.blendColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'dust'               : lambda ind, object : object.blendColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'steam'              : lambda ind, object : object.blendColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 1)) ,
        'tin'                : lambda ind, object : object.blendColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'river'              : lambda ind, object : object.blendColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'blend'              : lambda ind, object : object.blendColour(ind, object.polyColour(ind, 4898.0, (38.6163342703931, 3.52960945578193E-02, 1.97649736331153E-04, -6.62610980543087E-07, 9.47957505377445E-10, -7.60635557147666E-13, 3.7036175951177E-16, -1.11289388601947E-19, 2.01331419599276E-23, -2.00925196427511E-27, 8.49771597357908E-32), (7.76853640597202, 6.82746309113932E-02, 5.66619812017531E-05, -4.39381101189964E-07, 7.83759960108692E-10, -7.12082383041518E-13, 3.763656288968E-16, -1.19883400934137E-19, 2.26651371000468E-23, -2.34304684719006E-27, 1.02062396271791E-31), (8.57794780575146, 0.103608929866892, -1.33402974818553E-04, -1.17592515619097E-08, 2.51555252393189E-10, -3.18016943318326E-13, 1.96028280540034E-16, -6.84930111978641E-20, 1.37960995893249E-23, -1.49505180312647E-27, 6.75938366281296E-32)), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), base = 1.2) ,
        'twist'              : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), base = 1.0) ,
        'wood'               : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), base = 1.0) ,
        'lime'               : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), base = 1.0) ,
        'marine'             : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1), base = 1.0) ,
        'even'               : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0), base = 1.0) ,
        'purple'             : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), base = 1.0) ,
        'quarters'           : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), base = 1.0) ,
        'beach'              : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1), base = 1.0) ,
        'glow'               : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0), base = 1.0) ,
        'candy'              : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), base = 1.0) ,
        'teal'               : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1), base = 1.0) ,
        'orange'             : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0), base = 1.0) ,
        'lavender'           : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1), base = 1.0) ,
        'yellow'             : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0), base = 1.0) ,
        'cyan'               : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0), base = 1.0) ,
        'tan'                : lambda ind, object : object.greyColour(ind, 1.0, 0.98, 0.68) ,
        'grey'               : lambda ind, object : object.greyColour(ind, 1.02, 1.0, 0.98) ,
        'paperGrey'          : lambda ind, object : object.greyColour(ind, 1.0, 1.0, 1.0, lambda x: 1.0 - x) ,
        'paperGreyParab'     : lambda ind, object : object.greyColour(ind, 1.0, 1.0, 1.0, lambda x: 1.0 - x * x) ,
        'paperGreyBend'      : lambda ind, object : object.tableColour(Span.thermalGreyTable, ind, 0, 1, 2) ,
        'chalk'              : lambda ind, object : object.greyColour(ind, 1.02, 0.68, 0.51) ,
        'banded'             : lambda ind, object : object.greyColour(ind, *[clr / 130.0 for clr in object.silkColour(object._modFraction(ind), 2.0, 2.0, 4.0)]) ,
        'earth'              : lambda ind, object : object.tableColour(Span.dullTable, ind, 0, 1, 2) ,
        'blush'              : lambda ind, object : object.tableColour(Span.dullTable, ind, 0, 2, 1) ,
        'forest'             : lambda ind, object : object.tableColour(Span.dullTable, ind, 1, 0, 2) ,
        'magenta'            : lambda ind, object : object.tableColour(Span.dullTable, ind, 1, 2, 0) ,
        'turquoise'          : lambda ind, object : object.tableColour(Span.dullTable, ind, 2, 0, 1) ,
        'aqua'               : lambda ind, object : object.tableColour(Span.dullTable, ind, 2, 1, 0) ,
        'dark_blush'         : lambda ind, object : object.tableColour(Span.dullTable, ind, 0, 2, 1, 0.64, 0.64, 2.0) ,
        'pale_blush'         : lambda ind, object : object.tableColour(Span.dullTable, ind, 0, 2, 1, 1.2, 0.8, 0.6) ,
        'night'              : lambda ind, object : object.tableColour(Span.darkTable, ind, 0, 1, 2) ,
        'red_to_cyan'        : lambda ind, object : object.simpleColour(ind, 0, 1, 2) ,
        'red_to_yellow'      : lambda ind, object : object.tableColour(Span.threeTable, ind, 0, 1, 2) ,
        'red_to_magenta'     : lambda ind, object : object.tableColour(Span.threeTable, ind, 0, 2, 1) ,
        'blue_to_cyan'       : lambda ind, object : object.tableColour(Span.threeTable, ind, 2, 1, 0) ,
        'blue_to_yellow'     : lambda ind, object : object.simpleColour(ind, 2, 1, 0) ,
        'blue_to_magenta'    : lambda ind, object : object.tableColour(Span.threeTable, ind, 1, 2, 0) ,
        'green_to_cyan'      : lambda ind, object : object.tableColour(Span.threeTable, ind, 2, 0, 1) ,
        'green_to_magenta'   : lambda ind, object : object.simpleColour(ind, 2, 0, 1) ,
        'green_to_yellow'    : lambda ind, object : object.tableColour(Span.threeTable, ind, 1, 0, 2) ,
        'dark_three'         : lambda ind, object : object.tableColour(Span.threeTable, ind, 0, 2, 1, 0.64, 0.64, 2.0) ,
        'pale_three'         : lambda ind, object : object.tableColour(Span.threeTable, ind, 0, 2, 1, 1.2, 0.8, 0.6) ,
        'dark_simple'        : lambda ind, object : object.simpleColour(ind, 0, 1, 2, 0.64, 0.64, 2.0) ,
        'pale_simple'        : lambda ind, object : object.simpleColour(ind, 0, 1, 2, 1.2, 0.8, 0.6) ,
        'glass'              : lambda ind, object : object.blendColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 4.0), object._matchTotal(ind, *object._colourRatio(ind, 'blue'))) ,
        'quartz'             : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.tableColour(Span.thermalTable, ind, 2, 1, 0)) ,
        'beryl'              : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 2, 0, 1)) ,
        'apatite'            : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 2, 1, 0)) ,
        'feldspar'           : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 1, 2, 0)) ,
        'garnet'             : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 1, 0, 2)) ,
        'opal'               : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.tableColour(Span.thermalTable, ind, 0, 2, 1)) ,
        'slate'              : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.tableColour(Span.clayTable, ind, 0, 1, 2)) ,
        'pulse'              : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.clayTable, ind, 2, 1, 0), object.greyColour(ind, 1.2, 0.8, 0.6)) ,
        'agate'              : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.greyColour(ind, 1.2, 0.8, 0.6)) ,
        'sudden_red'         : lambda ind, object : object.tableColour(Span.abruptTable, ind, 0, 1, 2) ,
        'sudden_red_blue'    : lambda ind, object : object.tableColour(Span.abruptTable, ind, 0, 2, 1) ,
        'sudden_blue'        : lambda ind, object : object.tableColour(Span.abruptTable, ind, 2, 1, 0) ,
        'sudden_blue_red'    : lambda ind, object : object.tableColour(Span.abruptTable, ind, 2, 0, 1) ,
        'sudden_green'       : lambda ind, object : object.tableColour(Span.abruptTable, ind, 1, 0, 2) ,
        'sudden_green_blue'  : lambda ind, object : object.tableColour(Span.abruptTable, ind, 1, 2, 0) ,
        'falling_red'        : lambda ind, object : object.tableColour(Span.fallingTable, ind, 0, 1, 2) ,
        'falling_red_blue'   : lambda ind, object : object.tableColour(Span.fallingTable, ind, 0, 2, 1) ,
        'falling_blue'       : lambda ind, object : object.tableColour(Span.fallingTable, ind, 2, 1, 0) ,
        'falling_blue_red'   : lambda ind, object : object.tableColour(Span.fallingTable, ind, 2, 0, 1) ,
        'falling_green'      : lambda ind, object : object.tableColour(Span.fallingTable, ind, 1, 0, 2) ,
        'falling_green_blue' : lambda ind, object : object.tableColour(Span.fallingTable, ind, 1, 2, 0) ,
        'dark_falling'       : lambda ind, object : object.tableColour(Span.fallingTable, ind, 0, 1, 2, 0.64, 0.64, 2.0) ,
        'pale_falling'       : lambda ind, object : object.tableColour(Span.fallingTable, ind, 0, 1, 2, 1.2, 0.8, 0.6) ,
        'rising_red'         : lambda ind, object : object.tableColour(Span.risingTable, ind, 0, 1, 2) ,
        'rising_red_blue'    : lambda ind, object : object.tableColour(Span.risingTable, ind, 0, 2, 1) ,
        'rising_blue'        : lambda ind, object : object.tableColour(Span.risingTable, ind, 2, 1, 0) ,
        'rising_blue_red'    : lambda ind, object : object.tableColour(Span.risingTable, ind, 2, 0, 1) ,
        'rising_green'       : lambda ind, object : object.tableColour(Span.risingTable, ind, 1, 0, 2) ,
        'rising_green_blue'  : lambda ind, object : object.tableColour(Span.risingTable, ind, 1, 2, 0) ,
        'dark_rising'        : lambda ind, object : object.tableColour(Span.risingTable, ind, 0, 1, 2, 0.64, 0.64, 2.0) ,
        'pale_rising'        : lambda ind, object : object.tableColour(Span.risingTable, ind, 0, 1, 2, 1.2, 0.8, 0.6) ,
        'sharp_red'          : lambda ind, object : object.tableColour(Span.sharpTable, ind, 0, 1, 2) ,
        'sharp_red_blue'     : lambda ind, object : object.tableColour(Span.sharpTable, ind, 0, 2, 1) ,
        'sharp_blue'         : lambda ind, object : object.tableColour(Span.sharpTable, ind, 2, 1, 0) ,
        'sharp_blue_red'     : lambda ind, object : object.tableColour(Span.sharpTable, ind, 2, 0, 1) ,
        'sharp_green'        : lambda ind, object : object.tableColour(Span.sharpTable, ind, 1, 0, 2) ,
        'sharp_green_blue'   : lambda ind, object : object.tableColour(Span.sharpTable, ind, 1, 2, 0) ,
        'dark_sharp'         : lambda ind, object : object.tableColour(Span.sharpTable, ind, 0, 1, 2, 0.64, 0.64, 2.0) ,
        'pale_sharp'         : lambda ind, object : object.tableColour(Span.sharpTable, ind, 0, 1, 2, 1.2, 0.8, 0.6) ,
        'fast_red'           : lambda ind, object : object.tableColour(Span.fastTable, ind, 0, 1, 2) ,
        'fast_red_blue'      : lambda ind, object : object.tableColour(Span.fastTable, ind, 0, 2, 1) ,
        'fast_blue'          : lambda ind, object : object.tableColour(Span.fastTable, ind, 2, 1, 0) ,
        'fast_blue_red'      : lambda ind, object : object.tableColour(Span.fastTable, ind, 2, 0, 1) ,
        'fast_green'         : lambda ind, object : object.tableColour(Span.fastTable, ind, 1, 0, 2) ,
        'fast_green_blue'    : lambda ind, object : object.tableColour(Span.fastTable, ind, 1, 2, 0) ,
        'dark_fast'          : lambda ind, object : object.tableColour(Span.fastTable, ind, 0, 1, 2, 0.64, 0.64, 2.0) ,
        'pale_fast'          : lambda ind, object : object.tableColour(Span.fastTable, ind, 0, 1, 2, 1.2, 0.8, 0.6) ,
        'low_red'            : lambda ind, object : object.tableColour(Span.lowTable, ind, 0, 1, 2) ,
        'low_red_blue'       : lambda ind, object : object.tableColour(Span.lowTable, ind, 0, 2, 1) ,
        'low_blue'           : lambda ind, object : object.tableColour(Span.lowTable, ind, 2, 1, 0) ,
        'low_blue_red'       : lambda ind, object : object.tableColour(Span.lowTable, ind, 2, 0, 1) ,
        'low_green'          : lambda ind, object : object.tableColour(Span.lowTable, ind, 1, 0, 2) ,
        'low_green_blue'     : lambda ind, object : object.tableColour(Span.lowTable, ind, 1, 2, 0) ,
        'dark_low'           : lambda ind, object : object.tableColour(Span.lowTable, ind, 0, 1, 2, 0.64, 0.64, 2.0) ,
        'pale_low'           : lambda ind, object : object.tableColour(Span.lowTable, ind, 0, 1, 2, 1.2, 0.8, 0.6) ,
        'chartreuse'         : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'cornflower'         : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'neon'               : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'melon'              : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'olive'              : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'orchid'             : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'electric'           : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'prussian'           : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'thistle'            : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'strawberry'         : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'spring'             : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'plum'               : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'turquoise'          : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'navy'               : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'blizzard'           : lambda ind, object : object.pulseColour(ind, object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'maize'              : lambda ind, object : object.pulseColour(ind, object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'shock'              : lambda ind, object : object.pulseColour(ind, object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'asparagus'          : lambda ind, object : object.pulseColour(ind, object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'mauve'              : lambda ind, object : object.pulseColour(ind, object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'jungle'             : lambda ind, object : object.pulseColour(ind, object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'mahogony'           : lambda ind, object : object.pulseColour(ind, object.warmColour(ind, object._lightTotal(ind, 4.0) / 3.0, 0.6, 0.8, 0.35, 3.2, 0.4, 12.8), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'displaced'          : lambda ind, object : object.pulseColour(ind, object.hardColour(ind, 8.0, lambda x, y : x), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'pacific'            : lambda ind, object : object.pulseColour(ind, object.hardColour(ind, 8.0, lambda x, y : x), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'apple'              : lambda ind, object : object.pulseColour(ind, object.hardColour(ind, 8.0, lambda x, y : x), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'vivid'              : lambda ind, object : object.pulseColour(ind, object.hardColour(ind, 8.0, lambda x, y : x), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'shadow'             : lambda ind, object : object.pulseColour(ind, object.hardColour(ind, 8.0, lambda x, y : x), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'cerulean'           : lambda ind, object : object.pulseColour(ind, object.hardColour(ind, 8.0, lambda x, y : x), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'canary'             : lambda ind, object : object.pulseColour(ind, object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) , object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'spectrum'           : lambda ind, object : object.pulseColour(ind, object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) , object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'dandelion'          : lambda ind, object : object.pulseColour(ind, object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) , object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'antique'            : lambda ind, object : object.pulseColour(ind, object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) , object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'shamrock'           : lambda ind, object : object.pulseColour(ind, object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) , object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'caribbean'          : lambda ind, object : object.pulseColour(ind, object.polyColour(ind, 7.0, (1.6346153846133, 824.33653846156506, -828.34134615389098, 283.605769230796, -39.639423076930299, 1.9615384615393601, -4.2326711502807597e-014) ,  (-4.6066433566321203, -179.97115384619599, 345.60970279725501, -153.05944055946799, 25.7451923077004, -1.4711538461550999, 7.3709159435775299e-014) ,  (1.6346153846120099, 80.586538461564103, -201.46634615387501, 134.85576923078401, -29.0144230769268, 1.96153846153894, -2.4313478856444599e-014)) , object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'deep'               : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'well'               : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'fern'               : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'shimmer'            : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'bluebell'           : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'timber'             : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.thermalTable, ind, 2, 1, 0), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'torch'              : lambda ind, object : object.pulseColour(ind, object._matchTotal(ind, *object._colourRatio(ind, 'red')), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'flamingo'           : lambda ind, object : object.pulseColour(ind, object._matchTotal(ind, *object._colourRatio(ind, 'red')), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'pig'                : lambda ind, object : object.pulseColour(ind, object._matchTotal(ind, *object._colourRatio(ind, 'red')), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'berry'              : lambda ind, object : object.pulseColour(ind, object._matchTotal(ind, *object._colourRatio(ind, 'red')), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'alternating'        : lambda ind, object : object.pulseColour(ind, object._matchTotal(ind, *object._colourRatio(ind, 'red')), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'jam'                : lambda ind, object : object.pulseColour(ind, object._matchTotal(ind, *object._colourRatio(ind, 'red')), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'chalkyellow'        : lambda ind, object : object.pulseColour(ind, object.greyColour(ind, 1.02, 0.68, 0.51), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'chalkblue'          : lambda ind, object : object.pulseColour(ind, object.greyColour(ind, 1.02, 0.68, 0.51), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'chalkred'           : lambda ind, object : object.pulseColour(ind, object.greyColour(ind, 1.02, 0.68, 0.51), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'chalkorange'        : lambda ind, object : object.pulseColour(ind, object.greyColour(ind, 1.02, 0.68, 0.51), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'chalkgreen'         : lambda ind, object : object.pulseColour(ind, object.greyColour(ind, 1.02, 0.68, 0.51), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'chalkpurple'        : lambda ind, object : object.pulseColour(ind, object.greyColour(ind, 1.02, 0.68, 0.51), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        'bars'               : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.fallingTable, ind, 0, 1, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0)) ,
        'flare'              : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.fallingTable, ind, 0, 1, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 0, 2, 1)) ,
        'solar'              : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.fallingTable, ind, 0, 1, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 0, 2)) ,
        'plasma'             : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.fallingTable, ind, 0, 1, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 1, 2, 0)) ,
        'wind'               : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.fallingTable, ind, 0, 1, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 1, 0)) ,
        'cabbage'            : lambda ind, object : object.pulseColour(ind, object.tableColour(Span.fallingTable, ind, 0, 1, 2), object.silkColour(object._modFraction(ind), 2.0, 2.0, 2.0, 2, 0, 1)) ,
        }
    thermalTable = RangeTable({
        255.0  : lambda x: (x, 0.0, 0.0),
        382.0  : lambda x: (510.0 - x, (2.0 * x) - 510.0, 0.0),
        425.0  : lambda x: (510.0 - x, 254.0, (2.0 * x) - 764.0),
        509.0  : lambda x: (85.0, 679.0 - x, (2.0 * x) - 764.0),
        537.0  : lambda x: ((2.0 * x) - 933.0, 679.0 - x, 254.0),
        593.0  : lambda x: (678.0 - x, (2.0 * x) - 932.0, 254.0),
        679.0  : lambda x: ((2.0 * x) - 1101.0, 254.0, 847.0 - x),
        721.0  : lambda x: (255.0, 932.0 - x, (2.0 * x) - 1187.0),
        765.0  : lambda x: (255.0, x - 510.0, 255.0),
        })
    clayTable = RangeTable({
        153.6  : lambda x: ((5.0 / 4.0) * x, 0.0, 0.0),
        307.2  : lambda x: (192.0 - ((75.0 / 144.0) * (x - 153.6)), (105.0 / 144.0) * (x - 153.6), 0.0),
        307.2  : lambda x: (192.0 - ((75.0 / 144.0) * (x - 153.6)), (105.0 / 144.0) * (x - 153.6), 0.0),
        460.8  : lambda x: (112.0 - ((105.0 / 144.0) * (x - 307.2)), 112.0 + ((75.0 / 144.0) * (x - 307.2)), (5.0 / 4.0) * (x - 307.2)),
        921.6  : lambda x: ((25.0 / 72.0) * (x - 460.8), 192.0 - ((5.0 / 72.0) * (x - 460.8)), 192.0 + ((5.0 / 36.0) * (x - 460.8))),
        1075.2 : lambda x: (160.0 + ((5.0 / 8.0) * (x - 921.6)), 160.0 + ((5.0 / 8.0) * (x - 921.6)), 256.0),
        })
    malevichTable = RangeTable({
        45.0   : lambda x: ((3.0 / 2.0) * x, x, (1.0 / 5.0) * x),
        48.5   : lambda x: (22.5 + x, 45.0, 9.0),
        113.5  : lambda x: (119.5 - x, 54.7 - (1.0 / 5.0) * x, 9.0 + ((4.0 / 3.0) * (x - 48.5))),
        115.5  : lambda x: (119.5 - x, 32.0, 9.0 + ((4.0 / 3.0) * (x - 48.5))),
        116.0  : lambda x: (4.0, 32.0, 11.375 + (1.0 / 3.0) + (3.0 / 4.0) * x),
        182.0  : lambda x: (x - 112.0, (4.0 / 3.0) * x - 122.0 - (2.0 / 3.0), 157.0 - (1.0 / 2.0) * x),
        184.0  : lambda x: (70.0, x - 62.0, 66.0),
        220.0  : lambda x: (x - 114.0, 30.0 + (1.0 / 2.0) * x, (16.0 / 9.0) * x - 261.0 - (1.0 / 9.0)),
        253.0  : lambda x: (x - 114.0, 140.0, (5.0 / 6.0) * x - 53.0 - (1.0 / 3.0)),
        253.5  : lambda x: (139.0, 140.0, x - 95.5),
        367.0  : lambda x: (75.625 + (1.0 / 4.0) * x, 393.5 - x, 506.5625 - (11.0 / 8.0) * x),
        369.5  : lambda x: (75.625 + (1.0 / 4.0) * x, 393.5 - x, 2.0),
        374.5  : lambda x: (x - 201.5, 24.0, 2.0),
        411.5  : lambda x: (60.65 + (3.0 / 10.0) * x, (10.0 / 7.0) * x - 511.0, x - 372.5),
        411.6  : lambda x: (x - 227.4, (10.0 / 7.0) * x - 511.0, x - 372.5),
        412.4  : lambda x: (x - 227.4, 77.0, x - 372.5),
        496.4  : lambda x: (116.2 + (1.0 / 15.0) + (1.0 / 6.0) * x, x - 335.4, 90.55 - (1.0 / 8.0) * x),
        499.4  : lambda x: (199.0, x - 335.4, 90.55 - (1.0 / 8.0) * x),
        500.5  : lambda x: (199.0, 164.0, 527.525 - x),
        651.5  : lambda x: (157.0 + (7.0 / 24.0) + (1.0 / 12.0) * x, 164.0, x - 473.5),
        654.5  : lambda x: (157.0 + (7.0 / 24.0) + (1.0 / 12.0) * x, x - 487.5, x - 473.5),
        656.5  : lambda x: (157.0 + (7.0 / 24.0) + (1.0 / 12.0) * x, 167.0, 181.0),
        826.5  : lambda x: (168.2 + (1.0 / 30.0) + (1.0 / 15.0) * x, 232.65 - (1.0 / 10.0) * x, 837.5 - x),
        828.0  : lambda x: ((4.0 / 9.0) * x - 144.0, 232.65 - (1.0 / 10.0) * x, 11.0),
        829.0  : lambda x: ((4.0 / 9.0) * x - 144.0, 853.65 - (17.0 / 20.0) * x, 11.0),
        923.0  : lambda x: (131.0 + (8.0 / 9.0) + (1.0 / 9.0) * x, (1.0 / 5.0) * x - 16.8, x - 818.0),
        928.0  : lambda x: (131.0 + (8.0 / 9.0) + (1.0 / 9.0) * x, (1.0 / 5.0) * x - 16.8, 105.0),
        934.0  : lambda x: (235.0, (1.0 / 5.0) * x - 16.8, x - 823.0),
        972.0  : lambda x: (235.0, x - 764.0, x - 823.0),
        982.0  : lambda x: (x - 737.0, x - 764.0, 149.0),
        987.0  : lambda x: ((2.0 * x) - 1719.0, 219.0, 149.0),
        1093.0 : lambda x: (255.0, (1.0 / 4.0) * x - 26.75, x - 838.0),
        1093.4 : lambda x: (255.0, (1.0 / 4.0) * x - 26.75, 254.5),
        1096.0 : lambda x: (255.0, (2.0 * x) - 1939.8, 1347.9 - x),
        1097.0 : lambda x: (255.0, (2.0 * x) - 1939.8, 252.0),
        1097.5 : lambda x: (255.0, 255.0 , 252.0),
        })        
    abruptTable = RangeTable({
        256.0  : lambda x: (0.0, 0.0, x),
        512.0  : lambda x: (0.0, (x - 256.0), 256.0 - (x - 256.0)),
        768.0  : lambda x: ((x - 512.0), 256.0 - (x - 512.0), 0.0),
        1024.0 : lambda x: (256.0 - (.6875 * (x - 768.0)), .2083333 * (x - 768.0), .15625 * (x - 768.0)),
        1280.0 : lambda x: (80.0 - (.3125 * (x - 1024.0)), 53.3333 + (.7916667 * (x - 1024.0)), 40.0 + (.84375 * (x - 1024.0))),
        1536.0 : lambda x: ((x - 1280.0), 256.0 - (x - 1280.0), 256.0),
        1792.0 : lambda x: (256.0, (x - 1536.0), 256.0 - (x - 1536.0)),
        2048.0 : lambda x: (256.0 - (.375 * (x - 1792.0)), 256.0 - (.583333 * (x - 1792.0)), .3125 * (x - 1792.0)),
        3072.0 : lambda x: (160.0 + (.078125 * (x - 2048.0)), 106.6667 + (.05208333 * (x - 2048.0)), 80.0 + (.0390625 * (x - 2048.0))),
        3568.0 : lambda x: (240.0 + (.032258145 * (x - 3072.0)), 160.0 + (.193548387 * (x - 3072.0)), 120.0 + (.274193548 * (x - 3072.0))),
        })
    fallingTable = RangeTable({
        256.0  : lambda x: (0.0, 256.0 - x, 256.0),
        512.0  : lambda x: (x - 256.0, x - 256.0, 256.0),
        640.0  : lambda x: (256.0, 256.0 - (2.0 * (x - 512.0)), 256.0 - (x - 512.0)),
        768.0  : lambda x: (256.0, 0.0, 128.0 - (x - 640.0)),
        })
    risingTable = RangeTable({
        128.0  : lambda x: (256.0, 0.0, x),
        256.0  : lambda x: (256.0, 2 * (x - 128.0), 128.0 + (x - 128.0)),
        512.0  : lambda x: (256.0 - (x - 256.0), 256.0 - (x - 256.0), 256.0),
        768.0  : lambda x: (0.0, (x - 512.0), 256.0),
        })
    sharpTable = RangeTable({
        128.0  : lambda x: (0.0, x, 256.0),
        256.0  : lambda x: (0.0, 128.0 + (x - 128.0), 256.0 - (2.0 * (x - 128.0))),
        512.0  : lambda x: (x - 256.0, 256.0 - (x - 256.0), x - 256.0),
        640.0  : lambda x: (256.0, x - 512.0, 256.0 - (2.0 * (x - 512.0))),
        768.0  : lambda x: (256.0, 128.0 - (x - 640.0), 0.0),
        })
    fastTable = RangeTable({
        64.0   : lambda x: (0.0, 256.0 - x, 256.0),
        128.0  : lambda x: (0.0, 192.0 + (x - 64.0), 256.0 - (2.0 * (x - 64.0))),
        192.0  : lambda x: (3.0 * (x - 128.0), 256.0, 128.0 + (2.0 * (x - 128.0))),
        256.0  : lambda x: (192.0 - (3.0 * (x - 192.0)), 256.0 - (4.0 * (x - 192.0)), 256.0),
        320.0  : lambda x: ((x - 256.0), 4.0 * (x - 256.0), 256.0 - (4.0 * (x - 256.0))),
        384.0  : lambda x: (64.0 + (3.0 * (x - 320.0)), 256.0 - (2.0 * (x - 320.0)), 4.0 * (x - 320.0)),
        448.0  : lambda x: (256.0 - (4.0 * (x - 384.0)), 128.0 - (2.0 * (x - 384.0)), 256.0 - (3.0 * (x - 384.0))),
        512.0  : lambda x: (4.0 * (x - 448.0), 4.0 * (x - 448.0), 64.0 - (x - 448.0)),
        576.0  : lambda x: (256.0, 256.0 - (4.0 * (x - 512.0)), 3.0 * (x - 512.0)),
        640.0  : lambda x: (256.0, 0.0, 192.0 - (x - 576.0)),
        704.0  : lambda x: (256.0, (x - 640.0), 129.0 - (2.0 * (x - 640.0))),
        768.0  : lambda x: (256.0, 64.0 - (x - 704.0), 0.0),
        })
    threeTable = RangeTable({
        256.0  : lambda x: (x, 0.0, 0.0),
        512.0  : lambda x: (255.0, x - 256.0, 0.0),
        768.0  : lambda x: (255.0, 255.0, x - 512.0),
        })
    lowTable = RangeTable ({
        256.0  : lambda x: (0.0, x, x),
        512.0  : lambda x: (x - 256.0, 256.0 - (0.33333 * (x - 256.0)), 256.0 - (0.5 * (x - 256.0))),
        768.0  : lambda x: (256.0, 170.6667 + (0.3333 * (x - 512.0)), 128.0 + (0.5 * (x - 512.0))),
        1024.0 : lambda x: (256.0, 256.0 - (x - 768.0), 256.0),
        1280.0 : lambda x: (256.0, x - 1024.0, 256.0),
        })
    dullTable = RangeTable({
        80.0   : lambda x: (x, (3.0 / 4.0) * x, (1.0 / 4.0) * x),
        200.0  : lambda x: (80.0 + (1.0 / 4.0) * (x - 80.0), 60.0 + (5.0 / 12.0) * (x - 80.0), 20.0 + (3.0 / 4.0) * (x - 80.0)),
        320.0  : lambda x: (110.0 + (11.0 / 12.0) * (x - 200.0), 110.0 + (11.0 / 12.0) * (x - 200.0), 110.0 + (11.0 / 12.0) * (x - 200.0)),
        440.0  : lambda x: (220.0 - (1.0 / 2.0) * (x - 320.0), 220.0 - (5.0 / 6.0) * (x - 320.0), 220.0 - (3.0 / 2.0) * (x - 320.0)),
        620.0  : lambda x: (160.0 + (1.0 / 2.0) * (x - 440.0), 120.0 + (3.0 / 4.0) * (x - 440.0), 40.0 - (1.0 / 4.0) * (x - 440.0)),
        })
    darkTable = RangeTable({
        40.0   : lambda x: (2.0 * x, 0.0, 0.0),
        120.0  : lambda x: (80.0 - (x - 40.0), (x - 40.0), 0.0),
        380.0  : lambda x: (0.0, 80 - (1.0 / 2.0) * (x - 120.0), (8.0 / 5.0) * (x - 120.0)),
        420.0  : lambda x: (2.0 * (x - 380.0), 0.0, 255.0),
        460.0  : lambda x: (80.0, 2.0 * (x - 420.0), 255.0),
        })
    stoneTable = RangeTable({
        153.6  : lambda x: ((5.0 / 4.0) * x, 0.0, 0.0),
        307.2  : lambda x: (192.0 - ((75.0 / 144.0) * (x - 153.6)), (105.0 / 144.0) * (x - 153.6), 0.0),
        460.8  : lambda x: (112.0 - ((105.0 / 144.0) * (x - 307.2)), 112.0 + ((15.0 / 16.0) * (x - 307.2)), 0.0),
        614.4  : lambda x: (0.0, 256.0 - ((5.0 / 12.0) * (x - 460.8)), (5.0 / 4.0) * (x - 460.8)),
        921.6  : lambda x: ((75.0 / 144.0) * (x - 614.4), 192.0 - ((15.0 / 144.0) * (x - 614.4)), 192.0 + ((15.0 / 72.0) * (x - 614.4))),
        1075.2 : lambda x: (160.0 + ((5.0 / 8.0) * (x - 921.6)), 160.0 + ((5.0 / 8.0) * (x - 921.6)), 256.0),
        })
    arcTable = RangeTable({
        64.0   : lambda x: (2.0 * x, x, 0.0),
        192.0  : lambda x: (64.0 + x, 71.0 - (x / 8.0), (x / 16.0) - 4.0),
        363.0  : lambda x: (255.0, x - 145.0, x - 184.0),
        385.0  : lambda x: (255.0, 218.0, x - 184.0),
        400.0  : lambda x: (640.0 - x, x - 167.0, x - 184.0),
        422.0  : lambda x: (240.0, x - 167.0, x - 184.0),
        512.0  : lambda x: (662.0 - x, 255.0, 660.0 - x),
        550.0  : lambda x: (150.0, 255.0, 660.0 - x),
        695.0  : lambda x: (184.0 - (x / 16.0), 530.0 - (x / 2.0), x - 440.0),
        708.0  : lambda x: (141.0, 530.0 - (x / 2.0), 255.0),
        711.0  : lambda x: (x / 5.0, 1592.0 - (2.0 * x), 255.0),       
        780.0  : lambda x: (x / 5.0, x - 538.0, 255.0),
        793.0  : lambda x: (156.0, x - 538.0, 255.0),
        877.0  : lambda x: (x - 637.0, 413.0 - (x / 5.0), 354.0 - (x / 8.0)),       
        900.0  : lambda x: (240.0, (x / 10.0) + 150.0, 369.0 - (x / 7.0)),
        1040.0 : lambda x: (420.0 - (x / 5.0), 420.0 - (x / 5.0), 1140.0 - x),
        1050.0 : lambda x: (1250.0 - x, 1250.0 - x, 100.0),
        1110.0 : lambda x: (725.0 - (x / 2.0), 725.0 - (x / 2.0), 1150.0 - x),
        1120.0 : lambda x: (1280.0 - x, 1280.0 - x, 40.0),
        1160.0 : lambda x: ((x / 2.0) - 400.0, (x / 2.0) - 400.0, 1160.0 - x),
        1880.0 : lambda x: (470 - (x / 4.0), 470 - (x / 4.0), (x / 3.0) - 386.0),
        })             
    rainbowTable = RangeTable({
        255.0  : lambda x: (x, 0.0, 0.0),
        382.0  : lambda x: (510.0 - x, (2.0 * x) - 510.0, 0.0),
        425.0  : lambda x: (510.0 - x, 254.0, (2.0 * x) - 764.0),
        509.0  : lambda x: (85.0, 679.0 - x, (2.0 * x) - 764.0),
        537.0  : lambda x: ((2.0 * x) - 933.0, 679.0 - x, 254.0),
        593.0  : lambda x: (678.0 - x, 679.0 - x, 254.0),
        678.0  : lambda x: ((2.0 * x) - 1101.0, 679.0 - x, 847.0 - x),
        721.0  : lambda x: (255.0, 679.0 - x, 847.0 - x),
        765.0  : lambda x: (255.0, 679.0 - x, 847.0 - x),
        })
    thermalGreyTable = RangeTable({
        58.33  : lambda x: (255.0 - (x * 2.0), 255.0 - (x * 2.0), 255.0 - (x * 2.0)),
        228.33 : lambda x: (167.5 - (x * 0.5), 167.5 - (x * 0.5), 167.5 - (x * 0.5)),
        255.0  : lambda x: (510.0 - (x * 2.0), 510.0 - (x * 2.0), 510.0 - (x * 2.0)),
        })        
    colouredZero = ('pink', 'bronze', 'ruddy', 'thea')
    nocross, redcross, greencross, bluecross = 0, 2, 4, 8

    def __init__(self, numColours, dim = 100.0, bright = 600.0, redRatio = 1.09, greenRatio = 1.0, blueRatio = 3.21, redGreenContrast = 1.0, blueContrast = 2.0):
        self.numColours       = numColours
        self.dim              = dim
        self.bright           = bright
        self.redRatio         = redRatio
        self.greenRatio       = greenRatio
        self.blueRatio        = blueRatio
        self.redGreenContrast = redGreenContrast
        self.blueContrast     = blueContrast
        self.colourLookup     = {}

    def colour(self, ind, brighter = False, basis = 'silk'):
        try:
            return self.colourLookup[(ind, brighter, basis)]
        except:
            if ind == 0 and basis not in Span.colouredZero:
                return (0,0,0)
            red, green, blue = Span.colourDictionary[basis](ind, self)
            result = self.constrain(red, green, blue, brighter)
            self.colourLookup[(ind, brighter, basis)] = result
            return result

    def brighten(red, green, blue, limit = 255.0):
        colours = (red, green, blue)
        lratio  = Span._limitRatio
        for rgb in ((0, 1, 2), (1, 0, 2), (2, 1, 0)):
            if colours[rgb[0]] > colours[rgb[1]] and colours[rgb[0]] > colours[rgb[2]]:
                newColours = (lambda x, y, z, w: (x, x / lratio(limit, y, z), x / lratio(x, y, w)))(limit, colours[rgb[0]], colours[rgb[1]], colours[rgb[2]])
                return (newColours[rgb[0]], newColours[rgb[1]], newColours[rgb[2]])
        return colours
    brighten = staticmethod(brighten)

    def distributeExcess(one, two, three, ratio):
        if one > 255.0:
            return (255.0, two + ((one - 255.0) / (2.0 * ratio)), three + ((one - 255.0) / (2.0 * ratio)))
        return (one, two, three)
    distributeExcess = staticmethod(distributeExcess)

    def constrain(self, red, green, blue, brighter = False):
        while ((red > 255.0) or (green > 255.0) or (blue > 255.0)):
            red, green, blue = Span.distributeExcess(red, green, blue, self.redRatio)
            green, red, blue = Span.distributeExcess(green, red, blue, self.greenRatio)
            blue, red, green = Span.distributeExcess(blue, red, green, self.blueRatio)
        if brighter:
           red, green, blue = Span.brighten(red, green, blue)
        return (max(red,0), max(green,0), max(blue,0))

    def clearLookup(self):
        self.colourLookup = {}

    def tableColour(self, table, ind, first, second, third, redFactor = 1.0, greenFactor = 1.0, blueFactor = 1.0):
        scalar = self._scaledIndex(ind, table.uppermostLimit)
        clr    = table[scalar](scalar)
        return (redFactor * clr[first], greenFactor * clr[second], blueFactor * clr[third])

    def silkColour(self, fract, slowFactor, midFactor, fastFactor, slow = 0, mid = 1, fast = 2, fractFunction = lambda x: x):
        slowColour = slowFactor * self.bright * fractFunction(abs((fract - 0.5) / 2.0))
        midColour  = midFactor  * self.bright * fractFunction(abs(abs(fract - 0.5) - 0.25))
        fastColour = fastFactor * self.bright * fractFunction(abs(abs(abs(fract - 0.5) - 0.25) - 0.125))
        colours = (slowColour, midColour, fastColour)
        return colours[slow], colours[mid], colours[fast]

    def simpleColour(self, ind, first, second, third, redFactor = 1.0, greenFactor = 1.0, blueFactor = 1.0):
        thirdScalar = self._scaledIndex(ind, 768.0) / 3.0
        clr         = (256.0 - thirdScalar, thirdScalar, thirdScalar)
        return (redFactor * clr[first], greenFactor * clr[second], blueFactor * clr[third])

    def polyColour(self, ind, maximum, redCoefficients, greenCoefficients, blueCoefficients):
        x = self._scaledIndex(ind, maximum)
        return (polynomial(x, redCoefficients), polynomial(x, greenCoefficients), polynomial(x, blueCoefficients))

    def hardColour(self, ind, numSpirals, positionFunction):
        arcNum, arcPosition, length = self._arc(ind, numSpirals)
        red, green, blue = Span._arcAssignment(arcNum, (lambda x, y: (0.0, x * y, x * (1.0 - y)))(length, positionFunction(arcPosition, arcNum)))
        hardComponent = lambda x, y: x * ((self.dim / 3.0) + (((y / self.numColours) + ((((2.0 * ind) - length) / self.numColours) / 2.0)) * ((self.bright - self.dim) / 3.0)))
        return (hardComponent(self.redGreenContrast, red), hardComponent(self.redGreenContrast, green), hardComponent(self.blueContrast, blue))

    def softColour(self, ind, numSpirals, positionFunction):
        arcNum, arcPosition, length = self._arc(ind, numSpirals)
        red, green, blue = Span._arcAssignment(arcNum, (lambda x, y, z, u, w: (max(x * y, z), z + (u * w), z + (u * (1.0 - w))))(ind, float(4.0 * (0.25 - ((arcPosition - 0.5) ** 2))), ((2.0 * ind) - length) / 2.0, length, positionFunction(arcPosition, arcNum)))
        softComponent = lambda x: (x / self.numColours) * (self.bright / 3.0)
        return (softComponent(red), softComponent(green), softComponent(blue))

    def warmColour(self, ind, thirdBright, redBase, redFactor, greenBase, greenFactor, blueBase, blueFactor):
        fract, quarter, sixteenth = self._indexFractions(ind)
        red   = (redBase   + (redFactor   * fract))     * thirdBright
        green = (greenBase + (greenFactor * quarter))   * thirdBright
        blue  = (blueBase  + (blueFactor  * sixteenth)) * thirdBright
        return (red, green, blue)

    def paleColour(self, ind, redFactor, greenFactor, blueFactor):
        fract = self._modFraction(ind)
        red   = self.redGreenContrast * redFactor   * self.bright * abs(fract - 0.5)
        green = self.redGreenContrast * greenFactor * self.bright * abs(abs(fract - 0.5) - 0.25)
        blue  = self.blueContrast     * blueFactor  * self.bright * (1.0 - (0.5 * abs(fract - 0.25)))
        return (red, green, blue)

    def greyColour(self, ind, redNum, greenNum, blueNum, fractionFunction=lambda x: x):
        fract = fractionFunction(self._modFraction(ind))
        red, green, blue = self._matchTotal(fract * self.numColours, redNum / self.redRatio, greenNum / self.greenRatio, blueNum / self.blueRatio)
        return Span.brighten(red, green, blue, limit = (768.0 * fract / (redNum + greenNum + blueNum)))

    def crossColour(self, ind, firstColour, secondColour, crossFlags):
        clr = [0.0, 0.0, 0.0]
        for cross, indx in ((((crossFlags & Span.redcross) == Span.redcross), 0), (((crossFlags & Span.greencross) == Span.greencross), 1), (((crossFlags & Span.bluecross) == Span.bluecross), 2)):
            if cross:
                clr[indx] = (firstColour[indx] + secondColour[indx]) / 2.0
            else:
                clr[indx] = firstColour[indx]
        return clr

    def blendColour(self, ind, firstColour, secondColour, base = 1.5):
        hr, hg, hb = firstColour
        lr, lg, lb = secondColour
        ratio      = min(base * (float(ind) / self.numColours), 1.0)
        return ((ratio * hr) + ((1.0 - ratio) * lr), (ratio * hg) + ((1.0 - ratio) * lg), (ratio * hb) + ((1.0 - ratio) * lb))

    def metalColour(self, ind, firstColour, secondColour):
        scalar = self._scaledIndex(ind, 765.0)
        green  = (firstColour[1] + secondColour[1]) / 2.0
        red    = min(scalar / (0.5 + self.redGreenContrast), max(firstColour[0], secondColour[0]))
        blue   = secondColour[2] - max(scalar - self.bright, 0.0)
        return (red, green, blue)

    def splitColour(self, ind, split, redBase, redFactor, greenBase, greenFactor, greenLimit, blueBase, blueFactor):
        fract, quarter, sixteenth = self._indexFractions(ind)
        thirdBright = self._lightTotal(ind, 2.0) / 3.0
        red  = (redBase  + (redFactor  * fract))     * thirdBright
        blue = (blueBase + (blueFactor * sixteenth)) * thirdBright
        if fract >= split:
            green = (greenBase + (greenFactor * quarter)) * thirdBright
        else:
            green = (greenLimit - fract) * max(thirdBright, self.bright / 4.0)
        return (red, green, blue)

    def pulseColour(self, ind, firstColour, secondColour):
        lr, lg, lb = firstColour
        hr, hg, hb = secondColour
        r = 8.0 * abs(abs(abs(self._modFraction(ind) - 0.5) - 0.25) - 0.125)
        return (r * hr + (1.0 - r) * lr, r * hg + (1.0 - r) * lg, r * hb + (1.0 - r) * lb)

    def _arc(self, ind, numSpirals):
        spiralFactor = numSpirals / self.numColours
        halfSize     = 0.5 * self.numColours
        length       = 2.0 * (halfSize - abs(halfSize - ind))
        arc          = fmod((spiralFactor * ind), 3.0)
        arcNum       = int(arc)
        arcPosition  = fmod(arc, 1.0)
        return (arcNum, arcPosition, length)

    def _arcAssignment(arcNum, colour):
        if arcNum == 0:
            green, red, blue = colour
        elif arcNum == 1:
            blue, green, red = colour
        else:
            red, blue, green = colour
        return (red, green, blue)
    _arcAssignment = staticmethod(_arcAssignment)

    def _limitRatio(limit, one, two):
        if two != 0:
            return one / two
        return limit
    _limitRatio = staticmethod(_limitRatio)

    def _sharpValue(fractVal):
        absVal = fractVal - 0.125
        if float(fractVal) <= (0.75 / 12.0):
            return ((5.0 / 3.0) * absVal) + 0.125 + ((2.0 / 3.0) * 0.125)
        if float(fractVal) <= (2.25 / 12.0):
            return ((1.0 / 3.0) * absVal) + 0.125
        return ((5.0 / 3.0) * absVal) + 0.125 - ((2.0 / 3.0) * 0.125)
    _sharpValue = staticmethod(_sharpValue)

    def _total(self, ind):
        return max(self.dim + ind * ((self.bright - self.dim) / float(self.numColours)), 0)

    def _lightTotal(self, ind, lightness):
        return min(self._total(lightness * ind), self.bright)

    def _modFraction(self, ind):
        return (ind % self.numColours) / float(self.numColours)

    def _jointedCurve(self, fract, leftCurve, rightCurve, joiningPoint):
        if fract < joiningPoint:
            return leftCurve(fract)
        return rightCurve(fract)

    def _scaledIndex(self, ind, maximum):
        return ind * (maximum / float(self.numColours))

    def _matchTotal(self, ind, redRat, greenRat, blueRat):
        divisor  = redRat + greenRat + blueRat
        if divisor:
            red   = self.redRatio   * (redRat   / float(divisor)) * self._total(ind)
            green = self.greenRatio * (greenRat / float(divisor)) * self._total(ind)
            blue  = self.blueRatio  * (blueRat  / float(divisor)) * self._total(ind)
            return (red, green, blue)
        return (dim / 3.0, dim / 3.0, dim / 3.0)

    def _colourRatio(self, ind, basis):
        fract    = ind / float(self.numColours)
        quarter  = 4.0 * abs(abs(abs(fract - .25) - .25) - .25)
        eighth   = 8.0 * abs(abs(abs(abs(abs(abs(abs(fract - .125) - .125) - .125) - .1250) - .125) - .125) - .125)
        return {'red'  :(self.redGreenContrast,  eighth / self.greenRatio,  quarter / self.blueRatio),
                'green':(eighth / self.redRatio, self.redGreenContrast,     quarter / self.blueRatio),
                'blue' :(eighth / self.redRatio, quarter / self.greenRatio, self.blueContrast),
                'mixed':(eighth / self.redRatio, quarter / self.greenRatio, fract / self.blueRatio)}[basis]

    def _indexFractions(self, ind):
        fract     = self._modFraction(ind)
        quarter   = abs(abs(fract - 0.5) - 0.25)
        sixteenth = abs(abs(quarter - 0.125) - 0.0625)
        return (fract, quarter, sixteenth)




#   Sequence math_tools

def deepversion(function, arg):
    if isinstance(arg, list) or isinstance(arg, tuple):
        return function(arg.__class__([deepversion(function, element) for element in arg]))
    if isinstance(arg, dict):
        return function(arg.__class__([[deepversion(function, key), deepversion(function, value)] for key, value in arg.items()]))
    return function(arg)

def padzip(defaultArgument, *arguments):
    maxlength = max([len(arg) for arg in arguments])
    result    = []
    for i in range(0, maxlength):
        newArgument = []
        for arg in arguments:
            if i < len(arg):
                newArgument.append(arg[i])
            else:
                newArgument.append(defaultArgument)
        result.append(newArgument)
    return result

def rotate(outerSequence):
    """
        For any sequence of sequences, X, rotate returns a new sequence, Y, in which, for any m, n such
        that m is an index into X and n is an index into the sequence X[m], the element Y[n][m] is the
        element X[m][n]. For example, for any elements, a, b, c, d, e, f, h, i, j, k, l, rotate([[a, b,
        c], [d, e, f, g], [h, i, j, k, l]]) is the sequence [[a, d, h], [b, e, i], [c, f, j], [g, k],
        [l]].
    """
    result = outerSequence.__class__(outerSequence[0].__class__())
    for innerSequence in outerSequence:
        for ind, element in enumerate(innerSequence):
            try:
                result[ind].append(element)
            except IndexError:
                result.append([element])
    return result