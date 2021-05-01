from typing import Optional
import re


def unpack_list(lst) -> str:
    return "\n".join(map(str, lst))


def get_id_command(text_command_id: str) -> Optional[int]:
    try:
        match = re.search(r'(\d+)$', text_command_id)
        return int(match.group(1))
    except:
        return None
