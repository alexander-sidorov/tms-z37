import abc
from typing import Dict


class ExtendedContextMixin(abc.ABC):
    def get_context_data(self, *args, **kwargs) -> Dict:
        parent_context = super().get_context_data()
        my_context = self.get_extended_context()
        context = {**parent_context, **my_context}
        return context

    @abc.abstractmethod
    def get_extended_context(self) -> Dict:
        raise NotImplementedError
