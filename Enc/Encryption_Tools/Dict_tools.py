from .keys_tools import Keys
from .characters_list import get_characters_list

from typing import List,Dict,Tuple
class Dict_Tools:

    @classmethod
    def convert_to_dict(cls, character_list: List[str]) -> Dict[int,str]:
        return {idx:_char for idx,_char in enumerate(character_list) }

    # returns a new dict where the keys are the value and vice versa
    @classmethod
    def reverse_dict(cls, dict1: Dict) -> Dict:
        new_dict = {}

        for key, value in dict1.items():
            new_dict[value] = key

        return new_dict

    """take a key and generates a new list with different order  of the letters (changes the index of each letter and give a new_list)
    which means every key have different order of letter which makes it a bit harder to crack it """
    @classmethod
    def generate_character_list(cls, key: str)-> List[str]:
        character_list = get_characters_list()

        new_character_list = []
        keys = Keys.generate_keylist(len(character_list), key,case='A')

        for idx in range(len(character_list)):
            new_character_list.append(character_list.pop(
                keys[idx] % len(character_list)))

        return new_character_list

    @classmethod
    def get_dicts(cls, key: str,character_list: List[str] = None) -> Tuple[Dict,Dict]:
        if character_list is None:
            character_list = cls.generate_character_list(key)
        dict1 = cls.convert_to_dict(character_list)
        dict2 = cls.reverse_dict(dict1)

        return dict1, dict2

    
