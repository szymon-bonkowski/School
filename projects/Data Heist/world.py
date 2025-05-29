from typing import List, Dict, Optional
import json
import entities 
import items_skills

class ServerNode:
    def __init__(self, node_id: str, name: str, description: str,
                 enemies_definitions: Optional[List[Dict]] = None,
                 items_definitions: Optional[List[Dict]] = None,
                 connected_nodes: Optional[Dict[str, str]] = None,
                 puzzle_definition: Optional[Dict] = None):
        self.node_id: str = node_id
        self.name: str = name
        self.description: str = description
        
        self.enemies: List['entities.Enemy'] = []
        if enemies_definitions:
            for enemy_def in enemies_definitions:
                enemy_type = enemy_def.get("type", "Generic")
                enemy_name = enemy_def.get("name", f"Program Strażniczy {enemy_type}")
                integrity = enemy_def.get("integrity", 50)
                attack = enemy_def.get("attack", 10)
                defense = enemy_def.get("defense", 3)
                xp = enemy_def.get("xp", 20)
                loot_defs = enemy_def.get("loot_definitions")
                
                if enemy_type == "Antivirus":
                    self.enemies.append(entities.Antivirus(enemy_name, integrity, attack, defense, xp, loot_defs))
                elif enemy_type == "FirewallDaemon":
                    self.enemies.append(entities.FirewallDaemon(enemy_name, integrity, attack, defense, xp, loot_defs))
                elif enemy_type == "IDSGuardian":
                    self.enemies.append(entities.IDSGuardian(enemy_name, integrity, attack, defense, xp, loot_defs))
                else: 
                     self.enemies.append(entities.Enemy(enemy_name, integrity, attack, defense, 
                                                        enemy_type, xp_value=xp, loot_definitions=loot_defs))

        self.items_on_ground: List['items_skills.Item'] = []
        if items_definitions:
            for item_def in items_definitions:
                temp_inventory = items_skills.Inventory.from_dict([item_def])
                if temp_inventory.items:
                    self.items_on_ground.append(temp_inventory.items[0])

        self.connected_nodes: Dict[str, str] = connected_nodes if connected_nodes is not None else {}
        self.is_explored: bool = False
        self.puzzle: Optional[Dict] = puzzle_definition
        self.puzzle_solved: bool = False

    def get_description(self) -> str:
        desc = f"{self.description}\n"
        
        living_enemies_in_node = [e for e in self.enemies if not e.is_defeated()]
        if living_enemies_in_node:
            desc += "\n[Aktywne Systemy Obronne:]\n"
            for enemy in living_enemies_in_node:
                desc += f" - {enemy.name} [{enemy.enemy_type}] (Integralność: {enemy.current_integrity:.0f})\n"
        else:
            desc += "\n[Systemy Obronne: Zneutralizowane lub Brak Zagrożeń]\n"

        if self.items_on_ground:
            desc += "\n[Wykryte Pakiety Danych/Oprogramowanie:]\n"
            for item in self.items_on_ground:
                desc += f" - {item.name} ({item.description[:30]}...)\n"
        
        if self.puzzle and not self.puzzle_solved:
            desc += f"\n[Zabezpieczenie Systemowe: {self.puzzle.get('type', 'Nieznane').upper()}]\n"
            desc += f" {self.puzzle.get('prompt_examine', 'Wymaga interakcji.')}\n"
        elif self.puzzle and self.puzzle_solved:
            desc += "\n[Zabezpieczenie Systemowe: Zneutralizowane]\n"

        desc += "\n[Dostępne Połączenia Sieciowe:]\n"
        if self.connected_nodes:
            for direction, node_id_or_action in self.connected_nodes.items():
                desc += f" - {direction.capitalize():<10} -> {node_id_or_action}\n"
        else:
            desc += " Brak bezpośrednich połączeń z tego węzła.\n"
        return desc

    def has_living_enemies(self) -> bool:
        return any(not enemy.is_defeated() for enemy in self.enemies)

    def remove_item_from_ground(self, item_name: str) -> Optional['items_skills.Item']:
        for i, item in enumerate(self.items_on_ground):
            if item.name.lower() == item_name.lower():
                return self.items_on_ground.pop(i)
        return None

class ServerMap:
    def __init__(self):
        self.nodes: Dict[str, ServerNode] = {}
        self.start_node_id: Optional[str] = None

    def add_node(self, node_data: Dict, is_start: bool = False) -> None:
        node = ServerNode(
            node_id=node_data.get("node_id", f"unknown_node_{len(self.nodes)}"),
            name=node_data.get("name", "Nieznany Węzeł"),
            description=node_data.get("description", "Tajemniczy segment sieci."),
            enemies_definitions=node_data.get("enemies_definitions"),
            items_definitions=node_data.get("items_definitions"),
            connected_nodes=node_data.get("connected_nodes"),
            puzzle_definition=node_data.get("puzzle")
        )
        self.nodes[node.node_id] = node
        if is_start and not self.start_node_id:
            self.start_node_id = node.node_id

    def get_node(self, node_id: str) -> Optional[ServerNode]:
        return self.nodes.get(node_id)

    def load_map_from_json(self, file_path: str) -> bool:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                map_data_list = json.load(f)
            
            if not isinstance(map_data_list, list):
                print(f"BŁĄD KRYTYCZNY: Format mapy w '{file_path}' jest nieprawidłowy (oczekiwano listy).")
                return False

            self.nodes.clear()
            self.start_node_id = None 

            for i, node_data in enumerate(map_data_list):
                self.add_node(node_data, is_start=(i == 0 and not self.start_node_id)) 
            
            if not self.start_node_id and self.nodes:
                self.start_node_id = list(self.nodes.keys())[0]
            return True
        except FileNotFoundError:
            return False
        except json.JSONDecodeError:
            print(f"BŁĄD KRYTYCZNY: Nie można zdekodować pliku mapy '{file_path}'. Sprawdź format JSON.")
            return False
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas wczytywania mapy '{file_path}': {e}")
            return False

    def build_default_map_if_json_fails(self) -> None:
        default_nodes_definitions = [
            {
                "node_id": "entry_01", "name": "Brama Wejściowa (Tryb Awaryjny)",
                "description": "System pracuje w trybie awaryjnym. Dostępny jest tylko podstawowy punkt wejścia.",
                "connected_nodes": {"dalej": "corridor_emergency", "wyloguj": "EXIT"}
            },
            {
                "node_id": "corridor_emergency", "name": "Korytarz Awaryjny",
                "description": "Prosty korytarz. Wygląda na to, że większość systemów jest offline.",
                "enemies_definitions": [{"type": "Antivirus", "name": "Prosty Skaner", "integrity": 20, "attack": 5, "defense": 1, "xp": 10}],
                "connected_nodes": {"wstecz": "entry_01"}
            }
        ]
        self.nodes.clear()
        self.start_node_id = None
        for i, node_data in enumerate(default_nodes_definitions):
            self.add_node(node_data, is_start=(i == 0))
        
        if not self.start_node_id and self.nodes:
            self.start_node_id = list(self.nodes.keys())[0]