class Genome:
    def __init__(self):
        self.synComp = [] # List of synthetic components

    def addSynComp(self, pos: int, compType: str):
        """
        Add a synthetic component to the genome
        
        Args:
        pos (int): The position of the synthetic component
        compType (str): The type of the synthetic component
        """
        self.synComp.append(SynComp(pos, compType))
    
    def removeSynComp(self, pos: int):
        """
        Remove a synthetic component from the genome by specifying its position

        Args:
        pos (int): The position of the synthetic component to remove
        """
        for synComp in self.synComp:
            if synComp.pos == pos:
                self.synComp.remove(synComp)
                break
    
    def report(self):
        """
        Report the synthetic components in the genome
        """
        for synComp in self.synComp:
            synComp.report()
    
class SynComp:
    def __init__(self, pos, compType):
        self.pos = pos
        self.compType = compType
    
    def report(self):
        print(f'{self.compType} at position {self.pos}')
    
    def changeType(self, newType):
        self.compType = newType

