# parameter object for extended-abc


class Parameter:
    """Parameter object for use inside Abstract metaclasses.

    Parameter list (accessed through Parameter.parameters)...

        abstractclass = False or True
            # defines whether class is an abstract class (overriding function)

        checkforabstract = 'mro' or 'bases'
            # defines where to look for abstract methods

        allabstractmethods = False  or True
            # defines whether all methods in the class should be considered
            # abstract without explicitly doing so by means of...
            # using 'function.abstract = True'
            # @abstractmethod above the method definition
            # class AbstractClass(metaclass=Abstract,
            #                     abstractmethds=['function'])

        overrideimplementation = False or True
            # defines if a class should ignore forced implementation
            # of abstract methods defined in parent classes

        docstrings = False or True
            # defines whether subclasses should implement docstring on the the
            # class itself or in methods

        abstractmethods = []
            # defines a list of abstract methods subclasses must implement
            # rather than using...
            # @abstractmethod decorator
            # using 'function.abstract = True'

        abstractattributes = []
            # defines a list of attributes the subclass must implement

        checkforattributes = 'class' or 'bases' or 'mro'
            # defines whether to check for attributes (not methods) in...
            # the class, direct base classes, or all base classes (mro)

        checkforparameters = 'bases' or 'mro'
            # defines where to check for other parameters such as...
            # docstrings

        checkformethods = 'class' or 'bases' or 'mro'
            # defines whether to check for methods in...
            # the class, direct base classes, or all base classes (mro)
    """
    parameters = [
        'abstractclass',            # done
        'checkforabstract',         # done, I think
        'allabstractmethods',       # done
        'overrideimplementation',   # partially done
        'docstrings',               # done
        'abstractmethods',          # done
        'abstractattributes',       # done and recognises properties, yay!
        'checkforattributes',       # done
        'checkforparameters',       # done
        'checkformethods'           # done
    ]

    def __init__(self):
        self.abstractclass = False  # or True
        self.checkforabstract = 'mro'  # or 'bases'
        self.allabstractmethods = False  # or True
        self.overrideimplementation = False  # or True
        self.docstrings = False  # or True
        self.abstractmethods = []
        self.abstractattributes = []
        self.checkforattributes = 'class'  # or 'bases' or 'mro'
        self.checkforparameters = 'bases'  # or 'mro'
        self.checkformethods = 'class'  # or 'bases' or 'mro'

# consider adding dict with possible values for attributes

    def __setattr__(self, name, value):
        if name not in self.parameters:
            raise AttributeError('attribute must be in parameter list')
        else:
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        if name == 'all':
            return {name: super(Parameter, self).__getattribute__(name)
                    for name in self.parameters}
        else:
            try:
                return super().__getattribute__(name)
            except KeyError:
                return None
