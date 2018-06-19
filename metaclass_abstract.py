# metaclass abstract for extended-abc

# TODO:
# separate parts of __new__()
# into functions to ease readability
#
# update documentation to take into account parameter object
# re-comment


from abstract_decorator import abstractmethod
from parameter_object import Parameter
from errors import formaterror


class Abstract(type):
    """Metaclass which creates abstract classes.

    These abstract classes cannot be instantiated and only derived from.

    Usage:

    class Parent(metaclass=Abstract):
        # ...


    Creating an instance of this class using Parent() will raise TypeError.
    This class must be derived from:

    class Child(Parent):
        # ...


    When deriving from an abstract class, subclasses must implement all methods
    in the parent class whose abstract attribute is True. This attribute can
    be set by placing an @abstractmethod decorator above the definition or by
    directly setting its abstract attribute to True:

    class Parent(metaclass=Abstract):
        @abstractmethod
        def foo(self): pass

        # or...

        def bar(self): pass
        bar.abstract = True

    All abstract methods that are not implemented inside the subclass of the
    abstract class will raise NotImplementedError. A list of the invalid
    methods is printed when the error is raised. Each line indicates an invalid
    method and contains: the method name, the child class, the parent class.
    Duplicate names resulting from checking class mro (see below) are omitted
    and only the first occurence is recorded.



    Additional functionality:

    Use the keyword arguement 'parameters' to pass in a Parameter object
    to specify custom behaviour of the metaclass
    #
    #
    #
    #
    #

    """


# update documentation
# re-comment
# consider error list for parameter object as well
# also consider printing all errors raised by __new__ at once

    def __new__(mcls, name, bases, dct, parameters=Parameter()):

        # print('\n\n\n__new__ of', name)

        cls = super().__new__(mcls, name, bases, dct)
        errors = []
        typeerrors = mcls._check_parameters(parameters)

#        for attr, value in parameters.all.items():
#            setattr(cls, '_{}'.format(attr), value)
        setattr(cls, '_parameters', parameters)

        # perform regardless if class is abstract or subclass
        for name, value in cls.__dict__.items():
            if callable(value):
                # only applies to callable (method)
                value.abstract = getattr(value, 'abstract', False)
                # add an abstract attribute to the method or return its
                # current value if it already has one

        cls.abstractmethods = [*parameters.abstractmethods, *[
            name for name, value in cls.__dict__.items()
            if callable(value) if getattr(value, 'abstract', False)]]

        cls._methods = mcls._get_methods(cls, bases, parameters)

        # defines where to look for abstract methods
        if parameters.checkforabstract == 'bases':
            _bases = bases
            # keyword arguement that sets whether to check for method
            # implementations in *just* base abstract classes or *all* classes
            # in cls.mro() excluding the class itself and 'object'
        else:
            _bases = cls.mro()[1:-1]

        for base in bases:
            base.abstract = getattr(base, 'abstract', False)
            # give each base class an abstract attribute if not already given

        # determine whether this class should be abstract or not
        # depending on its base class

        if not _bases:
            cls.abstract = True
            # return the class as abstract if it has no bases

        for base in _bases:
            if base.abstract:
                cls.abstract = False
                break
                # return the class as a subclass as one of its bases is already
                # abstract therefore this must be a subclass which is permitted
            else:
                cls.abstract = True
                # if no bases are abstract return this class as abstract

        if parameters.abstractclass is True:
            # check whether the class is defined with an abstract=True
            # keyword arguement and if it is then override the previous
            # setting of its abstract/subclass status
            cls.abstract = True

        if parameters.allabstractmethods is True:
            for name, value in cls.__dict__.items():
                if callable(value):
                    value = abstractmethod(value)
                    # print(value.abstract)

        if parameters.checkforparameters == 'bases':
            parameterbase = bases
        else:
            parameterbase = cls.mro()[1:-1]

        # print('parameterbase:', cls.__name__, '\n\n', parameterbase)
        for base in parameterbase:
            if getattr(base, 'abstract', False):
                for parameter, value in base._parameters.all.items():
                    # check for:
                    # docstrings
                    # abstract subclass number (highest number)
                    # !! abstract methods(merge) !!
                    # !! abstract attributes (merge) !!
                    if parameter == 'docstrings':
                        if value is True \
                           and cls._parameters.overrideimplementation is False:
                            cls._parameters.docstrings = True
            # space to check for new methods

        if cls._parameters.docstrings is True:
            try:
                if not getattr(cls, '__doc__', False):
                    raise NotImplementedError('subclass \
\'{}\' must have docstring'.format(cls.__name__))
            except NotImplementedError as e:
                errors.append(e)
            for name, value in cls.__dict__.items():
                try:
                    if callable(value):
                        if not getattr(value, '__doc__', False):
                            raise NotImplementedError('method \'{}\' in subclass \
\'{}\' must have docstring'.format(name, cls.__name__))
                except NotImplementedError as e:
                    errors.append(e)

        if parameters.overrideimplementation is False:
            # perform if its abstract or if it's a subclass regardless unless
            # overriden creates a list of abstract methods from abstract parent
            # classes:
            basemethods = {**{name: base for base in _bases
                           for name, value in base.__dict__.items()
                           if getattr(base, 'abstract', False)
                           if callable(value) and
                           getattr(value, 'abstract', False)},
                           **{name: base for base in _bases
                           if getattr(base, 'abstract', False)
                           for name in base.abstractmethods}}

            for name, base in basemethods.items():
                try:
                    if name not in cls._methods:
                        raise NotImplementedError(
                            'method \'{}\' must implemented in subclass \'{}\' \
from class \'{}\''.format(
                                name, cls.__name__, base.__name__))
                except NotImplementedError as e:
                    # catch all errors raised and add to list
                    # if name not in [error[1] for error in errors]:
                    # (this won't add it to the list if the method name is
                    # already there)
                    # errors.append([e, name])
                    errors.append(e)

            if parameters.checkforattributes == 'class':
                cls._attributes = [name for name, value in cls.__dict__.items()
                                   if not callable(value)]

            elif parameters.checkforattributes == 'bases':
                cls._attributes = [*[name for name, value in
                                   cls.__dict__.items()
                                   if not callable(value)],
                                   *[name for base in bases
                                   for name, value in base.__dict__.items()
                                   if getattr(base, 'abstract', False)
                                   if not callable(value)]]

            else:
                cls._attributes = [*[name for name, value in
                                   cls.__dict__.items()
                                   if callable(value)],
                                   *[name for base in cls.mro()[1:-1]
                                   for name, value in base.__dict__.items()
                                   if getattr(base, 'abstract', False)
                                   if not callable(value)]]

            for base in parameterbase:
                if getattr(base, 'abstract', False):
                    for name in base._parameters.abstractattributes:
                        # print(base.__name__, ':', name)
                        # print(hasattr(cls, name))
                        try:
                            if name not in cls._attributes:
                                raise NotImplementedError('attribute \'{}\' \
must be implemented in subclass \'{}\' from class \'{}\''.format(
                                    name, cls.__name__, base.__name__))
                        except NotImplementedError as e:
                            # errors.append([e, name])
                            errors.append(e)

        if errors or typeerrors:
            # if errors list contains values, re-raise
            # TypeError with the list of errors
            # raise NotImplementedError(
            #     ',\n                     '.join(str(error[0])
            #                                     for error in errors))
            totalerrors = {'NotImplementedError':
                           [str(e) for e in errors],
                           'TypeError':
                           [str(e) for e in typeerrors]}
            formaterror(totalerrors)
        return cls
        # return the class (if no errors are raised above)

    def __call__(cls, *args, **kwargs):
        instance = type.__call__(cls, *args, **kwargs)

        if cls.abstract:
            # if the class being instantiated is abstract
            raise TypeError('abstract class \'{}\' cannot \
                be instantiated'.format(cls.__name__))
            # raise error as abstract classes cannot be instantiated
            # and only derived from
        return instance
        # return the new instance if no error raised

    def __init__(cls, name, bases, dct, **kwargs):
        return super().__init__(name, bases, dct)

    def _get_methods(cls, bases, parameters):
        # this adds adds a list of methods available to the class
        # from the class itself and abstract parent classes
        if parameters.checkformethods == 'class':
            methods = [name for name, value in cls.__dict__.items()
                       if callable(value)]

        elif parameters.checkformethods == 'bases':
            methods = [*[name for name, value in cls.__dict__.items()
                       if callable(value)],
                       *[name for base in bases
                       for name, value in base.__dict__.items()
                       if getattr(base, 'abstract', False)
                       if callable(value)]]

        else:
            methods = [*[name for name, value in cls.__dict__.items()
                       if callable(value)],
                       *[name for base in cls.mro()[1:-1]
                       for name, value in base.__dict__.items()
                       if getattr(base, 'abstract', False)
                       if callable(value)]]
        return methods

    def _check_parameters(parameters):
        typeerrors = []
        """checks the input of parameter object is valid"""
        if parameters.overrideimplementation not in (True, False):
            try:
                raise TypeError('parameter \'overrideimplementation\' must be \
either True or False ({} given)'.format(parameters.overrideimplementation))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.checkforabstract not in ('bases', 'mro'):
            try:
                raise TypeError('parameter \'check\' must be either \'bases\' \
or \'mro\' (\'{}\' given)'.format(parameters.checkforabstract))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.checkforattributes not in ('class', 'bases', 'mro'):
            try:
                raise TypeError('parameter \'checkforattributes\' must be \
either \'class\', \'bases\' or \
\'mro\' (\'{}\' given)'.format(parameters.checkforattributes))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.checkformethods not in ('class', 'bases', 'mro'):
            try:
                raise TypeError('parameter \'checkformethods\' must be either \
\'class\', \'bases\' or \'mro\' \
(\'{}\' given)'.format(parameters.checkformethods))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.abstractclass not in (True, False):
            try:
                raise TypeError('parameter \'abstractclass\' must be either \
True or False ({} given)'.format(parameters.abstractclass))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.allabstractmethods not in (True, False):
            try:
                raise TypeError('parameter \'allabstractmethods\' must be \
either True or False ({} given)'.format(parameters.allabstractmethods))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.docstrings not in (True, False):
            try:
                raise TypeError('parameter \'docstring\' must be either True \
or False ({} given)'.format(parameters.docstrings))
            except TypeError as e:
                typeerrors.append(e)

        if not isinstance(parameters.abstractmethods, list):
            try:
                raise TypeError('parameter \'abstractmethods\' must be type \
\'list\' ({} given)'.format(type(parameters.abstractmethods)))
            except TypeError as e:
                typeerrors.append(e)

        if not isinstance(parameters.abstractattributes, list):
            try:
                raise TypeError('parameter \'abstractattributes\' must be \
type \'list\' ({} given)'.format(type(parameters.abstractattributes)))
            except TypeError as e:
                typeerrors.append(e)

        if parameters.checkforparameters not in ('bases', 'mro'):
            try:
                raise TypeError('parameter \'checkforparameters\' must be \
either \'bases\' or \
\'mro\'(\'{}\' given)'.format(parameters.checkforparameters))
            except TypeError as e:
                typeerrors.append(e)

        if not isinstance(parameters, Parameter):
            try:
                # parameters = Parameter()
                raise TypeError('\'parameters\' keyword arguement must be \
\'Parameter\' instance')
            except TypeError as e:
                typeerrors.append(e)
