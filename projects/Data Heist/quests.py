from typing import List, Dict, Optional, Any 
import json
import items_skills 
import entities

class QuestObjective:
    def __init__(self, description: str, objective_type: str, target: Any, required_amount: int = 1):
        self.description: str = description
        self.objective_type: str = objective_type
        self.target: Any = target
        self.required_amount: int = required_amount
        self.current_amount: int = 0
        self.is_completed: bool = False

    def update_progress(self, amount_added: int = 1) -> tuple[bool, str]:
        if not self.is_completed:
            self.current_amount += amount_added
            if self.current_amount >= self.required_amount:
                self.is_completed = True
                return True, f"Cel osiągnięty: {self.description}"
            return False, f"Postęp celu '{self.description}': {self.current_amount}/{self.required_amount}"
        return False, f"Cel '{self.description}' jest już ukończony."

    def __str__(self) -> str:
        status_symbol = "[X]" if self.is_completed else "[ ]"
        return f"{status_symbol} {self.description} ({self.current_amount}/{self.required_amount})"

class Quest:
    def __init__(self, quest_id: str, title: str, description: str, objectives_data: List[Dict],
                 xp_reward: int = 0, item_rewards_definitions: Optional[List[Dict]] = None,
                 starts_dialogue_key: Optional[str] = None, ends_dialogue_key: Optional[str] = None,
                 unlocks_quest_id: Optional[str] = None, required_level: int = 1):
        self.quest_id: str = quest_id
        self.title: str = title
        self.description: str = description
        self.objectives: List[QuestObjective] = []
        for obj_data in objectives_data:
            self.objectives.append(QuestObjective(
                obj_data.get("description", "Nieznany cel"),
                obj_data.get("type", "unknown"),
                obj_data.get("target", None),
                obj_data.get("amount", 1)
            ))
        self.xp_reward: int = xp_reward
        self.item_rewards_definitions: List[Dict] = item_rewards_definitions if item_rewards_definitions else []
        self.is_active: bool = False
        self.is_completed: bool = False
        self.starts_dialogue_key: Optional[str] = starts_dialogue_key
        self.ends_dialogue_key: Optional[str] = ends_dialogue_key
        self.unlocks_quest_id: Optional[str] = unlocks_quest_id
        self.required_level: int = required_level

    def activate_quest(self) -> str:
        self.is_active = True
        return f"\nNowe zadanie aktywowane: '{self.title}'"

    def check_completion(self) -> bool:
        if not self.is_active or self.is_completed:
            return self.is_completed
        
        if all(obj.is_completed for obj in self.objectives):
            self.is_completed = True
            self.is_active = False
            return True
        return False

    def get_status_string(self) -> str:
        status_str = f"\n--- Zadanie: {self.title} ---\n"
        status_str += f"{self.description}\n"
        status_str += "Cele:\n"
        for obj in self.objectives:
            status_str += f"  {obj}\n"
        
        if self.is_completed:
            status_str += "Status: Ukończone\n"
        elif self.is_active:
            status_str += "Status: Aktywne\n"
        else:
            status_str += "Status: Nieaktywne\n"
        status_str += "-------------------------"
        return status_str

class QuestManager:
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.active_quests_ids: List[str] = []
        self.completed_quests_ids: List[str] = []

    def load_quests_from_json(self, file_path: str) -> str:
        messages = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                quests_data_list = json.load(f)
            for quest_data in quests_data_list:
                quest = Quest(
                    quest_id=quest_data["quest_id"],
                    title=quest_data["title"],
                    description=quest_data["description"],
                    objectives_data=quest_data.get("objectives", []),
                    xp_reward=quest_data.get("xp_reward", 0),
                    item_rewards_definitions=quest_data.get("item_rewards"),
                    starts_dialogue_key=quest_data.get("starts_dialogue_key"),
                    ends_dialogue_key=quest_data.get("ends_dialogue_key"),
                    unlocks_quest_id=quest_data.get("unlocks_quest_id"),
                    required_level=quest_data.get("required_level", 1)
                )
                self.quests[quest.quest_id] = quest
            messages.append(f"Zadania wczytane pomyślnie z '{file_path}'.")
        except FileNotFoundError:
            messages.append(f"BŁĄD: Plik z zadaniami '{file_path}' nie został znaleziony.")
        except json.JSONDecodeError:
            messages.append(f"BŁĄD: Nie można zdekodować pliku z zadaniami '{file_path}'.")
        except Exception as e:
            messages.append(f"Nieoczekiwany błąd podczas wczytywania zadań: {e}")
        return "\n".join(messages)

    def activate_quest_by_id(self, quest_id: str, player: entities.Player, game_dialogues: Optional[Dict[str, str]] = None) -> List[str]:
        messages = []
        quest = self.quests.get(quest_id)
        if not quest:
            messages.append(f"Nie znaleziono zadania o ID '{quest_id}'.")
            return messages
        
        if player.security_level < quest.required_level:
            messages.append(f"Nie możesz jeszcze podjąć zadania '{quest.title}'. Wymagany Poziom Bezpieczeństwa: {quest.required_level}.")
            return messages

        if quest_id in self.active_quests_ids:
            messages.append(f"Zadanie '{quest.title}' jest już aktywne.")
            return messages
        if quest_id in self.completed_quests_ids:
            messages.append(f"Zadanie '{quest.title}' zostało już ukończone.")
            return messages

        quest.is_active = True
        quest.is_completed = False
        for obj in quest.objectives:
            obj.current_amount = 0
            obj.is_completed = False
            
        self.active_quests_ids.append(quest_id)
        messages.append(quest.activate_quest())
        
        if quest.starts_dialogue_key and game_dialogues:
            messages.append("\n" + game_dialogues.get(quest.starts_dialogue_key, "Tajemnicza wiadomość..."))
        return messages

    def update_objective_progress(self, objective_type: str, target_achieved: Any, 
                                  amount: int = 1, player: Optional[entities.Player] = None, 
                                  game_dialogues: Optional[Dict[str, str]] = None) -> List[str]:
        progress_messages = []
        newly_completed_quests = []

        for quest_id in list(self.active_quests_ids):
            quest = self.quests.get(quest_id)
            if not quest or quest.is_completed:
                continue

            made_progress_in_this_quest = False
            for objective in quest.objectives:
                if not objective.is_completed and objective.objective_type == objective_type:
                    match = False
                    if objective_type == "collect_item" and isinstance(target_achieved, str) and objective.target.lower() == target_achieved.lower():
                        match = True
                    elif objective_type == "defeat_enemy":
                        if isinstance(target_achieved, entities.Enemy) and (objective.target.lower() == target_achieved.enemy_type.lower() or objective.target.lower() == target_achieved.name.lower()):
                            match = True
                    elif objective_type == "reach_node" and isinstance(target_achieved, str) and objective.target == target_achieved:
                        match = True
                    elif objective_type == "solve_puzzle" and isinstance(target_achieved, str) and objective.target == target_achieved:
                        match = True
                    
                    if match:
                        just_completed_obj, obj_message = objective.update_progress(amount)
                        progress_messages.append(f"[{quest.title}] {obj_message}")
                        made_progress_in_this_quest = True
            
            if made_progress_in_this_quest and quest.check_completion():
                newly_completed_quests.append(quest)
        
        for completed_quest in newly_completed_quests:
            completion_messages = self.handle_quest_completion(completed_quest, player, game_dialogues)
            progress_messages.extend(completion_messages)
            
        return progress_messages

    def handle_quest_completion(self, quest: Quest, player: Optional[entities.Player] = None, game_dialogues: Optional[Dict[str, str]] = None) -> List[str]:
        messages = []
        if not player: return ["Błąd: Brak gracza do przyznania nagród za zadanie."]

        messages.append(f"Nagroda za zadanie '{quest.title}': {quest.xp_reward} cykli CPU.")
        player.cpu_cycles += quest.xp_reward
        
        if quest.item_rewards_definitions:
            messages.append("Otrzymane przedmioty/oprogramowanie:")
            for item_def in quest.item_rewards_definitions:
                item_name = item_def.get("name", "Nieznana Nagroda")
                item_desc = item_def.get("description", "")
                item_type = item_def.get("type", "Item")
                created_item = None

                if item_type == "DataFragment":
                    created_item = items_skills.DataFragment(item_name, item_desc, item_def.get("value", 0), item_def.get("is_quest_item", False))
                elif item_type == "Software":
                    created_item = items_skills.Software(item_name, item_desc,
                                                          damage=item_def.get("damage",0),
                                                          integrity_restore=item_def.get("integrity_restore",0),
                                                          bandwidth_cost=item_def.get("bandwidth_cost",0),
                                                          effect_description=item_def.get("effect_description"))
                elif item_type == "HardwareUpgrade":
                     created_item = items_skills.HardwareUpgrade(item_name, item_desc, item_def.get("stat_boost", {}))
                
                if created_item:
                    added, add_msg = player.inventory.add_item(created_item)
                    messages.append(f"- {created_item.name} ({add_msg if not added else 'Dodano do repozytorium'})")

        level_up_messages = []
        current_level = player.security_level
        while player.cpu_cycles >= player.security_level * (100 + (player.security_level-1) * 30):
            if player.security_level > current_level :
                 level_up_messages.extend(player.level_up())
            else:
                current_level = player.security_level
                level_up_messages.extend(player.level_up())

        if level_up_messages:
            messages.extend(level_up_messages)

        if quest.ends_dialogue_key and game_dialogues:
            messages.append("\n" + game_dialogues.get(quest.ends_dialogue_key, "Misja zakończona pomyślnie."))

        if quest.quest_id in self.active_quests_ids:
            self.active_quests_ids.remove(quest.quest_id)
        if quest.quest_id not in self.completed_quests_ids:
            self.completed_quests_ids.append(quest.quest_id)
        
        quest.is_active = False
        quest.is_completed = True

        if quest.unlocks_quest_id:
            unlocked_quest = self.quests.get(quest.unlocks_quest_id)
            if unlocked_quest:
                messages.append(f"Odblokowano nowe zadanie: '{unlocked_quest.title}'")
            else:
                messages.append(f"Próbowano odblokować nieznane zadanie ID: {quest.unlocks_quest_id}")
        return messages

    def display_active_quests_string(self) -> str:
        if not self.active_quests_ids:
            return "\nBrak aktywnych zadań w logu systemowym."
        
        output_str = "\n--- Aktywne Zadania Systemowe ---\n"
        for quest_id in self.active_quests_ids:
            quest = self.quests.get(quest_id)
            if quest:
                output_str += quest.get_status_string() + "\n"
        output_str += "---------------------------------"
        return output_str
        
    def get_quests_save_data(self) -> Dict:
        active_quests_data = []
        for quest_id in self.active_quests_ids:
            quest = self.quests.get(quest_id)
            if quest:
                active_quests_data.append({
                    "quest_id": quest.quest_id,
                    "objectives_progress": [{"desc": obj.description, "current": obj.current_amount} for obj in quest.objectives]
                })
        return {
            "active_quests_data": active_quests_data,
            "completed_quest_ids": self.completed_quests_ids,
        }

    def load_quests_from_save_data(self, save_data: Dict):
        self.completed_quests_ids = save_data.get("completed_quest_ids", [])
        self.active_quests_ids = []
        
        active_quests_data_loaded = save_data.get("active_quests_data", [])
        for active_quest_entry in active_quests_data_loaded:
            quest_id = active_quest_entry.get("quest_id")
            quest = self.quests.get(quest_id)
            if quest and quest_id not in self.completed_quests_ids:
                quest.is_active = True
                quest.is_completed = False
                
                objective_progress_list = active_quest_entry.get("objectives_progress", [])
                for obj_prog_data in objective_progress_list:
                    for objective_in_quest in quest.objectives:
                        if objective_in_quest.description == obj_prog_data.get("desc"):
                            objective_in_quest.current_amount = obj_prog_data.get("current", 0)
                            if objective_in_quest.current_amount >= objective_in_quest.required_amount:
                                objective_in_quest.is_completed = True
                            else:
                                objective_in_quest.is_completed = False
                            break 
                self.active_quests_ids.append(quest_id)