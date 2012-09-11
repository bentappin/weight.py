from decimal import Decimal


class Weight(object):
    """
    Store and convert between weights.
    
    >>> me = Weight(st=13)
    >>> me
    Weight(st=13.0)
    >>> me.kg
    82.55381134000001
    
    >>> new_me = me - Weight(kg=5)
    >>> new_me
    Weight(st=12.2126347779)
    >>> new_me.kg
    77.55381134000001
    >>> new_me.st_lbs
    (12.0, 2.9768868907561341)
    
    This is basically a port/copy 'n' paste job of the geodjango Distance class by
    Robert Coup and Justin Bronn.
    """
        
    UNITS = {
        'g': 0.001,
        'kg': 1.0,
        'lbs': 0.45359237,
        'st': 6.35029318,
    }
    
    ALIAS = {
        'gram': 'g',
        'grammes': 'g',
        'kilogram': 'kg',
        'pounds': 'lbs',
        'stone': 'st',
    }
    LALIAS = dict([(k.lower(), v) for k, v in ALIAS.items()])
        
    def __init__(self, default_unit=None, **kwargs):
        self.kg, self._default_unit = self.default_units(kwargs)
        if default_unit and isinstance(default_unit, str):
            self._default_unit = default_unit

    def default_units(self, kwargs):
        """
        Return the unit value and the default units specified
        from the given keyword arguments dictionary.
        """
        val = 0.0
        for unit, value in kwargs.iteritems():
            if not isinstance(value, float): value = float(value)
            if unit in self.UNITS:
                val += self.UNITS[unit] * value
                default_unit = unit
            elif unit in self.ALIAS:
                u = self.ALIAS[unit]
                val += self.UNITS[u] * value
                default_unit = u
            else:
                lower = unit.lower()
                if lower in self.UNITS:
                    val += self.UNITS[lower] * value
                    default_unit = lower
                elif lower in self.LALIAS:
                    u = self.LALIAS[lower]
                    val += self.UNITS[u] * value
                    default_unit = u
                else:
                    raise AttributeError('Unknown unit type: %s' % unit)
        return val, default_unit
    
    @property
    def st_lbs(self):
        """ Returns a tuple of the stone and pounds for this Weight instance. """
        return divmod(self.lbs, 14)
    
    def __getattr__(self, name):
        if name in self.UNITS:
            return self.kg / self.UNITS[name]
        else:
            raise AttributeError('Unknown unit type: %s', name)
            
    def __repr__(self):
        return 'Weight(%s=%s)' % (self._default_unit, getattr(self, self._default_unit))
        
    def __str__(self):
        return '%s %s' % (getattr(self, self._default_unit), self._default_unit)
    
    def __cmp__(self, other):
        if isinstance(other, Weight):
            return cmp(self.kg, other.kg)
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Weight):
            return Weight(default_unit=self._default_unit, kg=(self.kg + other.kg))
        else:
            raise TypeError('Weight must be added with Weight')

    def __iadd__(self, other):
        if isinstance(other, Weight):
            self.kg += other.kg
            return self
        else:
            raise TypeError('Weight must be added with Weight')

    def __sub__(self, other):
        if isinstance(other, Weight):
            return Weight(default_unit=self._default_unit, kg=(self.kg - other.kg))
        else:
            raise TypeError('Weight must be subtracted from Weight')

    def __isub__(self, other):
        if isinstance(other, Weight):
            self.kg -= other.kg
            return self
        else:
            raise TypeError('Weight must be subtracted from Weight')

    def __mul__(self, other):
        if isinstance(other, (int, float, long, Decimal)):
            return Weight(default_unit=self._default_unit, kg=(self.kg * float(other)))
        else:
            raise TypeError('Weight must be multiplied with number')

    def __imul__(self, other):
        if isinstance(other, (int, float, long, Decimal)):
            self.kg *= float(other)
            return self
        else:
            raise TypeError('Weight must be multiplied with number')

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if isinstance(other, (int, float, long, Decimal)):
            return Weight(default_unit=self._default_unit, kg=(self.kg / float(other)))
        else:
            raise TypeError('Weight must be divided with Weight')

    def __idiv__(self, other):
        if isinstance(other, (int, float, long, Decimal)):
            self.kg /= float(other)
            return self
        else:
            raise TypeError('Weight must be divided with number')
            
    def __nonzero__(self):
        return bool(self.kg)
