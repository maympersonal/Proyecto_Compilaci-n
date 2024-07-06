import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name:str, param_names:list, params_types, return_type, body):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type
        self.body = body

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, attr):#comprobar
        try:
            print(attr)
            self.get_attribute(attr.name)
        except SemanticError:
            self.attributes.append(attr)
            return attr
        else:
            raise SemanticError(f'Attribute "{attr.name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
   
    def define_method(self,newMethod):#comprobar
        if newMethod.name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{newMethod.name}" already defined in {self.name}')
        self.methods.append(newMethod)
        return newMethod

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class Context:
    def __init__(self):
        self.types = {}
        self.methods = {}#agregado

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str,errors):
        try:
            return self.types[name]
        except KeyError:
            errors.append(SemanticError(f'Type "{name}" is not defined.'))
            return ErrorType(name)
    
    def get_type_cl(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def get_types(self, names:list,errors):
        return [self.get_type(name,errors) for name in names]
       
    def create_method(self, newMethod):#agregado
        try:
            key = Obtain_Key(newMethod.param_types)
            self.methods[newMethod.name,key]
            raise SemanticError(f'The Method ({name}) is already in context with those parameters.')#ver
        except KeyError:
            self.methods[newMethod.name,key] = newMethod
            return newMethod

    def get_method(self, name:str, param_types:list):
        try:
            return self.methods[name,param_types]
        except KeyError:
            raise SemanticError(f'Method "{name}" is not defined.')

    def semantic_get_method(self, name:str, param_types:list):
        methParams = filter_by_name(self.methods,name)
        for key in methParams:
            method =  methParams[key]
            if len(param_types) == len(method.param_types):
                correct = True
                for i in range(0,len(method.param_types)):
                    if not(param_types[i].conforms_to(method.param_types[i])):
                        correct = False
                if correct:
                    return method
        return None

    def __str__(self):# modificar
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype=None, data=None):
        self.name = name
        self.type = vtype
        self.data = data

class SemanticScope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = SemanticScope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

#herramientas
def Obtain_Key(param_types):
    string = ",".join([parType.name for parType in param_types])
    return string
def filter_by_name(data, name):
    return {key: value for key, value in data.items() if key[0] == name}