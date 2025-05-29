from typing import List, Optional, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from items_skills import Item, Skill, Inventory
else:
    Inventory = type('Inventory', (object,), {})
    Item = type('Item', (object,), {})
    Skill = type('Skill', (object,), {})

import items_skills

class Entity:
    def __init__(self, name: str, integrity: float, attack_power: float, defense_power: float):
        self.name: str = name
        self.max_integrity: float = integrity
        self.current_integrity: float = integrity
        self.attack_power: float = attack_power
        self.defense_power: float = defense_power

    def take_damage(self, amount: float) -> str:
        damage_taken = max(0, amount - self.defense_power)
        self.current_integrity -= damage_taken
        
        message = f"{self.name} otrzymuje {damage_taken:.2f} obrażeń sieciowych."
        if self.is_defeated():
            message += f" System {self.name} został zneutralizowany!"
        return message

    def attack(self, target: 'Entity') -> str:
        attack_message = f"{self.name} inicjuje atak na {target.name}!"
        damage_result_message = target.take_damage(self.attack_power)
        return f"{attack_message}\n{damage_result_message}"

    def is_defeated(self) -> bool:
        return self.current_integrity <= 0

    def __str__(self) -> str:
        return (f"{self.name} (Integralność: {self.current_integrity:.2f}/{self.max_integrity:.2f}, "
                f"Atak: {self.attack_power:.0f}, Obrona: {self.defense_power:.0f})")

class Player(Entity):
    def __init__(self, name: str, integrity: float, attack_power: float, defense_power: float):
        super().__init__(name, integrity, attack_power, defense_power)
        self.bandwidth: int = 100
        self.max_bandwidth: int = 100
        self.cpu_cycles: int = 0
        self.security_level: int = 1
        self.inventory: 'items_skills.Inventory' = items_skills.Inventory()
        self.skills: List['items_skills.Skill'] = [
            items_skills.SystemScanSkill("Skaner Podstawowy", "Skanuje system celu, ujawniając jego statystyki.", 5)
        ]
        self.data_currency: int = 0

    def learn_skill(self, new_skill: 'items_skills.Skill', silent: bool = False) -> str:
        if not any(skill.name == new_skill.name for skill in self.skills):
            self.skills.append(new_skill)
            if not silent:
                return f"Nowy program '{new_skill.name}' został zintegrowany z twoim systemem!"
            return ""
        if not silent:
            return f"Program '{new_skill.name}' jest już zainstalowany."
        return ""

    def list_skills(self) -> str:
        if not self.skills:
            return "Nie znasz żadnych specjalnych programów (umiejętności)."
        
        skill_list_str = "--- Dostępne Programy (Umiejętności) ---\n"
        for i, skill in enumerate(self.skills):
            skill_list_str += f"{i+1}. {skill}\n"
        skill_list_str += "--------------------------------------"
        return skill_list_str

    def use_skill(self, skill_index: int, target: Optional['Entity']) -> str:
        if 0 <= skill_index < len(self.skills):
            skill_to_use = self.skills[skill_index]
            return skill_to_use.activate(self, target)
        return "Nieprawidłowy numer programu."

    def use_item(self, item_index: int, target: Optional['Entity'] = None) -> str:
        if 0 <= item_index < len(self.inventory.items):
            item_to_use = self.inventory.items[item_index]
            if isinstance(item_to_use, items_skills.Software):
                message = item_to_use.use(self, target)
                if "Niewystarczające pasmo" not in message and "Brak widocznego efektu" not in message :
                    self.inventory.remove_item(item_to_use.name)
                return message
            elif isinstance(item_to_use, items_skills.HardwareUpgrade):
                return item_to_use.use(self)
            else:
                return item_to_use.use(target)
        return "Nieprawidłowy numer przedmiotu w repozytorium."

    def level_up(self) -> List[str]:
        messages = []
        self.security_level += 1
        self.max_integrity += 25
        self.current_integrity = self.max_integrity
        self.max_bandwidth += 15
        self.bandwidth = self.max_bandwidth
        self.attack_power += 6
        self.defense_power += 3
        messages.append(f"{self.name} osiągnął Poziom Bezpieczeństwa {self.security_level}!")
        messages.append(f"Integralność systemu wzrosła do {self.max_integrity:.0f}.")
        messages.append(f"Maksymalne pasmo zwiększone do {self.max_bandwidth}.")
        
        if self.security_level == 2:
            skill_msg = self.learn_skill(items_skills.ExploitSkill("Słaby Wirus", "Prosty wirus zadający niewielkie obrażenia.", 15, 25.0), silent=True)
            if "został zintegrowany" in skill_msg or "Nowy program" in skill_msg: messages.append(skill_msg)
        elif self.security_level == 3:
            skill_msg = self.learn_skill(items_skills.SystemPatchSkill("Łatka Systemowa", "Naprawia część integralności systemu.", 20, integrity_restore=35.0), silent=True)
            if "został zintegrowany" in skill_msg or "Nowy program" in skill_msg: messages.append(skill_msg)
        return messages

    def __str__(self) -> str:
        base_info = super().__str__()
        return (f"{base_info}\n"
                f"  Pasmo: {self.bandwidth}/{self.max_bandwidth}, Poziom Bezp.: {self.security_level}, Cykle CPU: {self.cpu_cycles}, Kredyty Danych: {self.data_currency}")

class Enemy(Entity):
    def __init__(self, name: str, integrity: float, attack_power: float, defense_power: float, 
                 enemy_type: str, special_ability_name: Optional[str] = None, 
                 xp_value: int = 20, loot_definitions: Optional[List[Dict]] = None):
        super().__init__(name, integrity, attack_power, defense_power)
        self.enemy_type: str = enemy_type
        self.special_ability_name = special_ability_name
        self.special_ability_cooldown_max: int = 3
        self.special_ability_cooldown_current: int = 0
        self.xp_value: int = xp_value
        self.loot: List['items_skills.Item'] = []
        if loot_definitions:
            for loot_def in loot_definitions:
                item_type = loot_def.get("type", "DataFragment")
                item_name = loot_def.get("name", "Nieznany Łup")
                item_desc = loot_def.get("description", "Tajemnicze dane.")
                if item_type == "Software":
                    self.loot.append(items_skills.Software(item_name, item_desc,
                                                           damage=loot_def.get("damage", 0),
                                                           integrity_restore=loot_def.get("integrity_restore", 0),
                                                           bandwidth_cost=loot_def.get("bandwidth_cost", 0)))
                elif item_type == "DataFragment":
                    self.loot.append(items_skills.DataFragment(item_name, item_desc, value=loot_def.get("value", 5)))

    def perform_special_ability(self, target: 'Player') -> str:
        if self.special_ability_cooldown_current > 0:
            return f"{self.name} przygotowuje specjalną akcję..."

        self.special_ability_cooldown_current = self.special_ability_cooldown_max
        
        ability_message = ""
        if self.special_ability_name == "OverloadPulse":
            damage = self.attack_power * 1.7
            damage_info = target.take_damage(damage)
            ability_message = f"{self.name} wyzwala <<Impuls Przeciążenia>>!\n{damage_info}"
        elif self.special_ability_name == "DataDrain":
            drained_bw = 20
            target.bandwidth = max(0, target.bandwidth - drained_bw)
            healed_amount = min(drained_bw, self.max_integrity - self.current_integrity)
            self.current_integrity += healed_amount
            ability_message = f"{self.name} uruchamia <<Wyssanie Danych>>! Wysysa {drained_bw} pasma od {target.name} i regeneruje {healed_amount:.0f} integralności."
        else:
            return self.attack(target)
        return ability_message

    def enemy_turn(self, player_target: 'Player') -> str:
        action_message = ""
        if self.special_ability_name and self.special_ability_cooldown_current == 0:
            action_message = self.perform_special_ability(player_target)
        else:
            action_message = self.attack(player_target)
        
        if self.special_ability_cooldown_current > 0:
             self.special_ability_cooldown_current -=1
        return action_message

class Antivirus(Enemy):
    def __init__(self, name: str = "Program Antywirusowy", integrity: float = 50, attack_power: float = 12, defense_power: float = 4,
                 xp_value: int = 30, loot_definitions: Optional[List[Dict]] = None):
        if loot_definitions is None:
            loot_definitions = [{"type": "DataFragment", "name": "Fragment Kodu Antywirusa", "value": 10}]
        super().__init__(name, integrity, attack_power, defense_power, "Antywirus", 
                         special_ability_name="DataDrain", xp_value=xp_value, loot_definitions=loot_definitions)

class FirewallDaemon(Enemy):
    def __init__(self, name: str = "Demon Zapory Sieciowej", integrity: float = 80, attack_power: float = 15, defense_power: float = 7,
                 xp_value: int = 50, loot_definitions: Optional[List[Dict]] = None):
        if loot_definitions is None:
            loot_definitions = [{"type": "Software", "name": "Mini-Tarcza", "description": "Chwilowo zwiększa obronę.", "bandwidth_cost": 10, "integrity_restore": 5}]
        super().__init__(name, integrity, attack_power, defense_power, "Zapora Sieciowa",
                         special_ability_name="OverloadPulse", xp_value=xp_value, loot_definitions=loot_definitions)

class IDSGuardian(Enemy): 
    def __init__(self, name: str = "Strażnik Systemu Wykrywania Włamań", integrity: float = 120, attack_power: float = 18, defense_power: float = 10,
                 xp_value: int = 75, loot_definitions: Optional[List[Dict]] = None):
        if loot_definitions is None:
            loot_definitions = [{"type": "DataFragment", "name": "Logi Systemu IDS", "value": 25},
                                {"type": "Software", "name": "Impuls EMP (Słaby)", "description": "Może chwilowo osłabić cel.", "damage": 5, "bandwidth_cost": 15}]
        super().__init__(name, integrity, attack_power, defense_power, "Strażnik IDS",
                         special_ability_name="OverloadPulse",
                         xp_value=xp_value, loot_definitions=loot_definitions)