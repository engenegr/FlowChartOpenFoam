from Graph import Vertex
import os
import sys
#import PyFoam
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.TemplateFile import TemplateFileOldFormat


def check_dir(item):
    if not isinstance(item, str):
        raise TypeError('Type error')
    if not os.path.isdir(item):
        raise ValueError('Can not find case dir %s' %item) 

def check_file(item):
    if not isinstance(item, str):
        raise TypeError('Type error')
    if not os.path.isfile(item):
        raise ValueError('Can not find file %s' %item) 


class ParameterVariation(Vertex):
    def __init__(self, templateFile = '', variables = [], values = []):
        super(ParameterVariation, self).__init__(name='ParameterVariation')
        try:
            check_file(templateFile)
        except ValueError:
            raise ValueError('Template file should be provided by user')
        if len(variables) == 0 or len(values[0])==0:
            raise ValueError('ParameterVariation must have at least one Variable and one Value')
        self.__templateFile = templateFile
        self.__vars = variables
        self.__vals = values
        self.__counter = 0
        baseFile = str(self.__templateFile)
        savePath = (baseFile.split("."))[0]
        baseFile = (baseFile.split("/"))[-1]
        baseFile = (baseFile.split("."))[0]
        print savePath
        print baseFile
        t=TemplateFileOldFormat(name=self.__templateFile)
        #vals=eval("{%s: %i}") %(self.__vars[0], self.__vals[0][0])
        t.getString({self.__vars[0]: self.__vals[0][0]})
        t.writeToFile(savePath, {self.__vars[0]: self.__vals[0][0]})

    #pyFoamFromTemplate.py  system/blockMeshDict "{'nElem': 200}"

    def initialize(self, **kwargs):
        pass
             
    def action(self, **kwargs):
        print self
        print 'run ParameterVariation'
        try:
            check_dir(kwargs['path'])
        except:
            raise ValueError('Vertex ParameterVariation can not find path to case')
            
        os.system('blockMesh -case ' + kwargs['path'])
        #os.system('blockMesh')

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])

class BlockMesh(Vertex):
    def __init__(self, ofDictPath =''):
        super(BlockMesh, self).__init__(name='blockMesh')
        try:
            check_file(ofDictPath)
        except ValueError:
            raise ValueError('File blockMeshDict should be provided by user')

    def initialize(self, **kwargs):
        pass
             
    def action(self, **kwargs):
        print self
        print 'run blockMesh'
        try:
            check_dir(kwargs['path'])
        except:
            raise ValueError('Vertex blockMesh can not find path to case')
            
        os.system('blockMesh -case ' + kwargs['path'])
        #os.system('blockMesh')

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class Solver(Vertex):
    def __init__(self, tutorialPath=''):
        try:
            check_file(tutorialPath +'/system/controlDict')
        except ValueError:
            raise ValueError('Path to tutorial template case for Solver should be provided by user')
        self.__setupCase = tutorialPath
        parsedControlDict=ParsedParameterFile(tutorialPath+'/system/controlDict')    
        self.__solverNameFromTutorial = parsedControlDict["application"]
        
        #Very good way to control previously parsed OpenFOAM file
        #parsedControlDict["endTime"] = 1
        #parsedControlDict.writeFile()
        
        super(Solver, self).__init__(name='solver')

    @property
    def setupCase(self):
        return self.__setupCase
        
    def initCase(self, casePath):
        self.copyTutorialIfEmpty(casePath)
        return True
    
    def copyTutorialIfEmpty(self, casePath):
        try:
            check_dir(casePath)        
        except ValueError:
            raise ValueError('Vertex Solver error: case structure was not created')
        try:
            check_file(casePath +'/system/controlDict')
        except:
            os.system('cp -rn ' + self.setupCase + '/* ' + casePath)

    def initialize(self, **kwargs):
        self.copyTutorialIfEmpty(kwargs['path'])
        pass
         
    def action(self, **kwargs):
        print self
        print 'run ' + self.__solverNameFromTutorial
        os.system(self.__solverNameFromTutorial + ' -case ' + kwargs['path'])

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(path=kwargs['path'])


class ParaFoam(Vertex):
    def __init__(self):
        super(ParaFoam, self).__init__(name='paraFoam')

    def initialize(self, **kwargs):
        pass
     
    def action(self, **kwargs):
        os.system('paraFoam -case ' + kwargs['path'])
        print self
        print 'run paraFoam'

        if len(self.edges()) > 0:
            self.edges().keys()[0].action(kwargs)
