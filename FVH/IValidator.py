import abc
from ENUM_RESPONSES import Responses
from django.db import models

class IValidator(abc.ABC):
   
    @abc.abstractmethod
    def validate(self, data, serializer):
        """
        Validate the given data.

        :param data: The data to validate.
        :return: An instance of Responses indicating the validation result.
        """
        
        pass