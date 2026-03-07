import os
import json

from typing import Any

from Spell import Spell
from TieredSpell import TieredSpell


MANIFEST_PATH: str = 'Root/TemplateManifest.de.xml'
SPELL_GROUP_PATH: str = 'Root/TieredSpells.de.xml'
TIERED_SPELL_PATH: str = 'Root/Spells/Tiered Spells'

SPELL_LANG_PATH: str = 'Root/Locale/en-US/Spell.lang'
SPELLS_LANG_PATH: str = 'Root/Locale/en-US/Spells.lang'


SPELL_GROUP_EXCEPTIONS: dict[str, str] = {
    'Catalan': 'Catalan the Lightning Lizard',
    'Savage Paw': 'Jaguar Shaman',
    'Winter Moon': 'MoonSkull Priestess',
    'Lord of Night': 'ThunderHorn Mummy',
    'Skeletal Dragon': 'Bone Dragon',
    'Woolly Mammoth': 'Wooly Mammoth',
    'Gnomes': 'Gnomes!',
}

SPELL_CODE_EXCEPTIONS: dict[str, str] = {
    'Colossal_00000003': 'Nightbringer',
    'Colossal_00000004': 'Daybreaker',
}


def get_object_name_by_group(
    spell_group_path: str = SPELL_GROUP_PATH
) -> dict[int, str]:
    """
    Load the tiered spell group list and map each group index to its tier-one spell object name.

    Args:
        spell_group_path (str): Path to the tiered spell group JSON file. Defaults to SPELL_GROUP_PATH.

    Returns:
        dict[int, str]: A mapping of group index to tier-one spell object name.
    """

    with open(spell_group_path, 'r', encoding='utf-8') as spell_group_file:
        data: dict[str, Any] = json.load(spell_group_file)

    object_name_by_group: dict[int, str] = {
        index: str(entry['m_tierOneSpell']).strip()
        for index, entry in enumerate(data['m_tieredSpellGroupList'])
    }

    return object_name_by_group


def get_spell_id_by_object_name(manifest_path: str = MANIFEST_PATH) -> dict[str, int]:
    """
    Load the template manifest and map each tiered spell object name to its spell ID.

    Args:
        manifest_path (str): Path to the template manifest JSON file. Defaults to MANIFEST_PATH.

    Returns:
        dict[str, int]: A mapping of tiered spell object name to spell ID.
    """

    with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
        data: dict[str, Any] = json.load(manifest_file)

    spell_id_by_object_name: dict[str, int] = {
        (
            str(obj['m_filename'])
            .replace('Spells/Tiered Spells/', '')
            .replace('.xml', '')
            .strip()
        ): int(obj['m_id'])

        for obj in data['m_serializedTemplates']
        if 'Spells/Tiered Spells/' in obj.get('m_filename', '')
    }

    return spell_id_by_object_name


def main() -> None:
    """
    Entry point for the Tiered Spells processing pipeline.
    """

    # {TieredSpellGroup: ObjectName}
    object_name_by_group: dict[int, str] = get_object_name_by_group(SPELL_GROUP_PATH)

    # {ObjectName: SpellID}
    spell_id_by_object_name: dict[str, int] = get_spell_id_by_object_name(MANIFEST_PATH)


if __name__ == '__main__':
    main()
