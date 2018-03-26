
from typing import Optional, Union, Callable, Any


class classproperty(object):
    """ Decorator to allow properties on the class level """

    def __init__(self, fget: Callable[[type], Any]) -> None:
        self.fget = fget

    def __get__(self, _, owner_cls: type) -> Any:
        return self.fget(owner_cls)


class I2B2Coding:
    _prefix = None
    
    @classmethod
    def _code(cls, base: str, code: Optional[Union[str, int]] = None) -> str:
        return cls._prefix + '|' + base + ':{}'.format(code if code is not None else '@')

    
class I2B2DemographicsCodes(I2B2Coding):
    """
    Representations of the I2B2 coding model -- the general format being {type}|{domain}[:{code or '@'}]
    Examples:
        DEM|RACE:mid.eastern is the I2B2 concept dimension code for the middle eastern religion
        DEM|DATE:birth  -- birth date
        DEM|DATE:death  -- death date
        DEM|AGE:17 -- 17 years old
        DEM|AGE:-1 -- age unrecorded
        DEM|SEX:m -- male sex
        DEM|SEX:@ -- sex not recorded
    """
    _prefix = "DEM"

    @classmethod
    def age(cls,  age: Optional[int] = -1) -> str:
        return cls._code('AGE', age)

    @classproperty
    def birthdate(cls) -> str:
        return cls._code('DATE', 'birth')

    @classproperty
    def deathdate(cls) -> str:
        return cls._code('DATE', 'death')

    @classmethod
    def language(cls,  language: Optional[str]) -> str:
        return cls._code('LANGUAGE', language)

    @classmethod
    def marital_status(cls,  status: Optional[str]) -> str:
        return cls._code('MARITAL', status)

    @classmethod
    def race(cls,  race: Optional[str]) -> str:
        return cls._code('RACE', race)

    @classmethod
    def religion(cls,  religion: Optional[str]) -> str:
        return cls._code('RELIGION', religion)

    @classproperty
    def sex_male(cls) -> str:
        return cls._code('SEX', 'm')

    @classproperty
    def sex_female(cls) -> str:
        return cls._code('SEX', 'f')

    @classproperty
    def sex_undifferentiated(cls) -> str:
        return cls._code('SEX', 'u')

    @classproperty
    def sex_unknown(cls) -> str:
        return cls._code('SEX', None)

    @classproperty
    def vital_living(cls) -> str:
        return cls._code('VITAL', 'n')

    @classproperty
    def vital_dead(cls) -> str:
        return cls._code('VITAL', 'y')

    @classproperty
    def vital_deferred(cls) -> str:
        # TODO: find out what 'deferred' means in this context
        return cls._code('VITAL', 'x')

    @classproperty
    def vital_unknown(cls) -> str:
        return cls._code('VITAL', None)

    @classmethod
    def zip(cls,  zip_code: int) -> str:
        return cls._code('ZIP', zip_code)
