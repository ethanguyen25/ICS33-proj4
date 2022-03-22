# Submitter: ethandn1(Nguyen, Ethan)
# Partner  : anamava1(Namavar,Arian)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # We start by binding the class attribute to True meaning checking can occur
    #   (but only when the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # For checking the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # We start by comparing check's function annotation to its arguments

#         print(param, annot, value) 
        if annot is None: pass 
        elif type(annot) is type:
            assert isinstance(value, annot), f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)} ...should be type {annot}" + '\n'+ check_history
        elif isinstance(annot, list):
            assert isinstance(value, list), f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)} ...should be type {annot}" + '\n'+ check_history
            if len(annot) == 1:
                for x in value:
                    self.check(param, annot[0], x)
            else:
                assert len(value) == len(annot), f"length of value is not equal to the length of annot" + '\n'+ check_history
                for x in value:
                    self.check(param, annot[value.index(x)], x)
        elif isinstance(annot, tuple):
            assert isinstance(value, tuple), f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)} ...should be type {annot}" + '\n'+ check_history
            if len(annot) == 1:
                for x in value:
                    self.check(param, annot[0], x)
            else:
                assert len(value) == len(annot), f"length of value is not equal to the length of annot" + '\n'+ check_history
                for x in value:
                    self.check(param, annot[value.index(x)], x)
        elif isinstance(annot, dict):
            assert isinstance(value, dict), f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)} ...should be type {annot}"+ '\n'+ check_history
            assert len(annot) == 1, "length of annot does not equal to 1" + '\n'+ check_history
            for k, v in value.items():
                for kk, vv in annot.items():
                    self.check(param, kk, k)
                    self.check(param, vv, v)
        elif isinstance(annot, set):
            assert isinstance(value, set), f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)} ...should be type {annot}" + '\n'+ check_history
            assert len(annot) == 1, "length of annot does not equal to 1" + '\n'+ check_history
            for x in value:
                self.check(param, tuple(annot)[0], x) 
        elif isinstance(annot, frozenset):
            assert isinstance(value, frozenset), f"'{param}' failed annotation check(wrong type): value = {value} was type {type(value)} ...should be type {annot}" + '\n'+ check_history
            assert len(annot) == 1, "length of annot does not equal to 1" + '\n'+ check_history   
            for x in value:
                self.check(param, tuple(annot)[0], x)  
        elif inspect.isfunction(annot):
            assert (len(annot.__code__.co_varnames)) == 1, f"'{param}' annotation inconsistency: predicate should have 1 parameter but had {len(annot.__code__.co_varnames)} predicate = {annot}" + '\n'+ check_history
            try:
               assert annot(value), f"'{param}' failed annotation check: value = {value} and predicate = {annot}" + '\n'+ check_history
            except Exception: 
                raise AssertionError(f"'{param}' failed annotation check: value = {value} and predicate = {annot}" + '\n'+ check_history)
        else:
            if isinstance(annot, str):
#                 assert isinstance(value, str)
                try:
                    assert eval(annot, self.pabs), "failed annotation check" + '\n'+ check_history
                except Exception:
                    raise AssertionError(f"{param} failed annotation check(str predicate: {annot} args for evaluation:" + ', '.join([str(k) + '->' + str(v) for k,v in self.pabs.items()]) + '\n' +check_history)
            else:
                try:
                   annot.__check_annotation__(self.check,param,value,check_history)
                except Exception:
                    raise AssertionError(f"'{param}' undecipherable: {annot}" + '\n'+ check_history)
                    
            
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Returns the parameter->argument bindings as an ordereddict, derived
        #   from dict, binding the function header's parameters in order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        self.pabs = param_arg_bindings()
        annotation = self._f.__annotations__
        if not self._checking_on and not Check_Annotation.checking_on:
            return self._f(*args,**kargs)
        try:
            # Check the annotation for each of the annotated parameters
            
#             print("1",param_arg_bindings())
#             print("2",self._f.__annotations__)
            for i,j in self.pabs.items():
#                 print("IJ",i,j)
                if i in annotation:
                    self.check(i,annotation[i], j)
                      
            # Compute/remember the value of the decorated function
            result = self._f(*args, **kargs)
            
            # If 'return' is in the annotation, check it
#             print("ANNOTATION", annotation)
            if "return" in annotation:
                self.pabs["_return"] = result
                self.check("_return", annotation["return"], result)
            
            # Return the decorated answer
            return result
            #pass #remove after adding real code in try/except
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
#             print(80*'-')
#             for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
#                 print(l.rstrip())
#             print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
#     def f(x:int): pass
#     f = Check_Annotation(f)
#     f([1,2])
#     f = Check_Annotation(f)
#     f(3)
#     f('a')

#     def f(x : 'x>=0'): pass
#     f = Check_Annotation(f)
#     f = ('a')
    
#     driver tests
    import driver
    driver.default_file_name = 'bscp4W20.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
