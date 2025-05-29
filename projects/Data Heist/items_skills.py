from typing import List, Optional, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from entities import Entity, Player 
else:
    Entity = type('Entity', (object,), {})
    Player = type('Player', (object,), {})

class Item:
    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description

    def use(self, user: Optional['Player'] = None, target: Optional['Entity'] = None) -> str:
        return f"Użyto '{self.name}', ale nie ma zdefiniowanego efektu."

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

class Software(Item):
    def __init__(self, name: str, description: str, damage: float = 0, integrity_restore: float = 0, 
                 bandwidth_cost: int = 0, effect_description: Optional[str] = None,
                 target_enemy_only: bool = False, self_target_only: bool = False):
        super().__init__(name, description)
        self.damage = damage
        self.integrity_restore = integrity_restore
        self.bandwidth_cost = bandwidth_cost
        self.effect_description = effect_description if effect_description else ""
        self.target_enemy_only = target_enemy_only
        self.self_target_only = self_target_only

    def use(self, user: 'Player', target: Optional['Entity'] = None) -> str:
        if user.bandwidth < self.bandwidth_cost:
            return f"Niewystarczające pasmo ({user.bandwidth}/{self.bandwidth_cost}), aby uruchomić '{self.name}'."
        
        if self.target_enemy_only and (not target or target == user):
            return f"'{self.name}' musi być użyty na systemie wroga."
        if self.self_target_only and target and target != user:
             return f"'{self.name}' może być użyty tylko na własnym systemie."

        user.bandwidth -= self.bandwidth_cost
        
        actual_target = target
        if self.self_target_only:
            actual_target = user

        base_message = f"{user.name} uruchamia program '{self.name}'. {self.effect_description}\n"
        effect_details = []

        if self.damage > 0 and actual_target:
            damage_info = actual_target.take_damage(self.damage)
            effect_details.append(damage_info)
        if self.integrity_restore > 0 and isinstance(actual_target, Player):
            healed_amount = min(self.integrity_restore, actual_target.max_integrity - actual_target.current_integrity)
            actual_target.current_integrity += healed_amount
            effect_details.append(f"Przywrócono {healed_amount:.2f} integralności systemu {actual_target.name}.")
        
        if not effect_details:
             effect_details.append("Brak widocznego bezpośredniego efektu.")
        return base_message + "\n".join(effect_details)

class HardwareUpgrade(Item):
    def __init__(self, name: str, description: str, stat_boost: Dict[str, float]):
        super().__init__(name, description)
        self.stat_boost: Dict[str, float] = stat_boost

    def use(self, user: 'Player', target: Optional['Entity'] = None) -> str:
        message = f"Instalowanie ulepszenia '{self.name}'...\n"
        boost_messages = []
        for stat, value in self.stat_boost.items():
            if hasattr(user, stat):
                current_val = getattr(user, stat)
                setattr(user, stat, current_val + value)
                boost_messages.append(f"  {stat.replace('_', ' ').capitalize()} zwiększone o {value:.0f}.")
                if stat == "max_integrity":
                    user.current_integrity += value
                elif stat == "max_bandwidth":
                    user.bandwidth += value
            else:
                boost_messages.append(f"  Nie można ulepszyć nieznanej statystyki: {stat}.")
        if not boost_messages:
            return message + "Brak zdefiniowanych ulepszeń statystyk."
        return message + "\n".join(boost_messages) + "\nUlepszenie zintegrowane z systemem."

class DataFragment(Item):
    def __init__(self, name: str, description: str, value: int = 0, is_quest_item: bool = False):
        super().__init__(name, description)
        self.value = value
        self.is_quest_item = is_quest_item

    def use(self, user: Optional['Player'] = None, target: Optional['Entity'] = None) -> str:
        message = f"Przeanalizowano '{self.name}'. {self.description}"
        if self.value > 0 and not self.is_quest_item:
            message += f" Szacunkowa wartość: {self.value} kredytów danych."
        elif self.is_quest_item:
            message += " Ten fragment wydaje się kluczowy dla twojej misji."
        return message

class Skill:
    def __init__(self, name: str, description: str, bandwidth_cost: int, 
                 target_required: bool = True, cooldown_max: int = 0):
        self.name: str = name
        self.description: str = description
        self.bandwidth_cost: int = bandwidth_cost
        self.target_required: bool = target_required
        self.cooldown_max: int = cooldown_max
        self.cooldown_current: int = 0

    def is_ready(self) -> bool:
        return self.cooldown_current == 0

    def activate(self, caster: 'Player', target: Optional['Entity'] = None) -> str:
        if not self.is_ready():
            return f"Program '{self.name}' jest w trakcie ponownej kompilacji (pozostało tur: {self.cooldown_current})."
        if caster.bandwidth < self.bandwidth_cost:
            return f"Niewystarczające pasmo ({caster.bandwidth}/{self.bandwidth_cost}), aby aktywować '{self.name}'."
        if self.target_required and not target:
            return f"Program '{self.name}' wymaga celu."
            
        caster.bandwidth -= self.bandwidth_cost
        if self.cooldown_max > 0:
            self.cooldown_current = self.cooldown_max + 1
        return f"{caster.name} aktywuje program '{self.name}'..."

    def tick_cooldown(self):
        if self.cooldown_current > 0:
            self.cooldown_current -= 1
            
    def __str__(self) -> str:
        cooldown_info = f" (Kompilacja: {self.cooldown_current}t)" if self.cooldown_current > 0 else ""
        return f"{self.name} (Pasmo: {self.bandwidth_cost}{cooldown_info}): {self.description}"

class ExploitSkill(Skill):
    def __init__(self, name: str, description: str, bandwidth_cost: int, base_damage: float, cooldown: int = 1):
        super().__init__(name, description, bandwidth_cost, target_required=True, cooldown_max=cooldown)
        self.base_damage = base_damage 

    def activate(self, caster: 'Player', target: Optional['Entity'] = None) -> str:
        activation_message = super().activate(caster, target)
        if not activation_message.endswith("..."):
            return activation_message
        
        if target:
            skill_power_modifier = 1 + (caster.security_level * 0.15) 
            actual_damage = (self.base_damage + caster.attack_power * 0.1) * skill_power_modifier 
            damage_info = target.take_damage(actual_damage)
            return f"{activation_message}\nCel: {target.name}.\n{damage_info}"
        return activation_message + f"\nProgram '{self.name}' nie znalazł celu."

class SystemScanSkill(Skill):
    def __init__(self, name: str, description: str, bandwidth_cost: int, cooldown: int = 2):
        super().__init__(name, description, bandwidth_cost, target_required=True, cooldown_max=cooldown)

    def activate(self, caster: 'Player', target: Optional['Entity'] = None) -> str:
        activation_message = super().activate(caster, target)
        if not activation_message.endswith("..."):
            return activation_message

        if target:
            return f"{activation_message}\nWynik skanowania systemu {target.name}:\n{target}"
        return activation_message + f"\nProgram '{self.name}' nie znalazł celu do przeskanowania."

class SystemPatchSkill(Skill):
    def __init__(self, name: str, description: str, bandwidth_cost: int, integrity_restore_base: float, cooldown: int = 3):
        super().__init__(name, description, bandwidth_cost, target_required=False, cooldown_max=cooldown)
        self.integrity_restore_base = integrity_restore_base

    def activate(self, caster: 'Player', target: Optional['Entity'] = None) -> str:
        activation_message = super().activate(caster, caster)
        if not activation_message.endswith("..."):
            return activation_message
        
        restore_power_modifier = 1 + (caster.security_level * 0.1)
        actual_restore = self.integrity_restore_base * restore_power_modifier
        
        healed_amount = min(actual_restore, caster.max_integrity - caster.current_integrity)
        if healed_amount <= 0:
             return activation_message + f"\nSystem {caster.name} ma już pełną integralność."

        caster.current_integrity += healed_amount
        return activation_message + f"\nPrzywrócono {healed_amount:.2f} integralności systemu {caster.name}."

class Inventory:
    def __init__(self, capacity: int = 10):
        self.items: List[Item] = []
        self.capacity: int = capacity

    def add_item(self, item: Item) -> tuple[bool, str]:
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True, f"Pobrany program/dane '{item.name}' dodane do repozytorium."
        return False, "Repozytorium danych jest pełne. Nie można dodać więcej."

    def remove_item(self, item_name: str) -> Optional[Item]:
        for i, item in enumerate(self.items):
            if item.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def get_item(self, item_name: str) -> Optional[Item]:
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def list_items(self) -> str:
        if not self.items:
            return "Repozytorium danych jest puste."
        
        inventory_str = "--- Repozytorium Danych ---\n"
        for i, item in enumerate(self.items):
            inventory_str += f"{i+1}. {item}\n"
        inventory_str += "-------------------------"
        return inventory_str

    def to_dict(self) -> List[Dict]:
        item_list_data = []
        for item in self.items:
            item_data = {"name": item.name, "type": item.__class__.__name__, "description": item.description}
            if isinstance(item, Software):
                item_data["damage"] = item.damage
                item_data["integrity_restore"] = item.integrity_restore
                item_data["bandwidth_cost"] = item.bandwidth_cost
                item_data["effect_description"] = item.effect_description
            elif isinstance(item, HardwareUpgrade):
                item_data["stat_boost"] = item.stat_boost
            elif isinstance(item, DataFragment):
                item_data["value"] = item.value
                item_data["is_quest_item"] = item.is_quest_item
            item_list_data.append(item_data)
        return item_list_data

    @classmethod
    def from_dict(cls, data: List[Dict]) -> 'Inventory':
        inventory = cls()
        if not isinstance(data, list):
            return inventory

        for item_data in data:
            if not isinstance(item_data, dict): continue

            item_type = item_data.get("type", "Item")
            name = item_data.get("name", "Nieznany przedmiot")
            description = item_data.get("description", "")
            
            created_item = None
            if item_type == "Software":
                created_item = Software(name, description, 
                                        damage=item_data.get("damage",0),
                                        integrity_restore=item_data.get("integrity_restore",0),
                                        bandwidth_cost=item_data.get("bandwidth_cost",0),
                                        effect_description=item_data.get("effect_description"))
            elif item_type == "HardwareUpgrade":
                created_item = HardwareUpgrade(name, description, stat_boost=item_data.get("stat_boost", {}))
            elif item_type == "DataFragment":
                created_item = DataFragment(name, description, 
                                            value=item_data.get("value",0),
                                            is_quest_item=item_data.get("is_quest_item", False))
            else:
                created_item = Item(name, description)
            
            if created_item:
                inventory.add_item(created_item)
        return inventory