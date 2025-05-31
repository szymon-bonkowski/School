import json
import os
import time
import sys
from typing import Optional, List, Dict, Any

import entities
import items_skills
import world
import quests

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = Style.RESET_ALL = Fore.GREEN = Fore.YELLOW = Fore.CYAN = Fore.MAGENTA = Fore.WHITE = Fore.LIGHTWHITE_EX = Fore.LIGHTRED_EX = ""
    class Style:
        RESET_ALL = BRIGHT = ""
    class Back:
        BLACK = ""
    print("Ostrzeżenie: Biblioteka 'colorama' nie jest zainstalowana. Tekst nie będzie kolorowy.")
    print("Aby zainstalować, użyj: pip install colorama")

import os
SAVE_FILE_USER_PREFIX = "save_data_heist_"
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
MAP_FILE = os.path.join(DATA_FOLDER, "map_omnicorp.json")
USER_DATA_FILE = os.path.join(DATA_FOLDER, "users_data.json")
QUEST_FILE = os.path.join(DATA_FOLDER, "quests_data.json")
DIALOGUE_FILE = os.path.join(DATA_FOLDER, "dialogues.json")

def slow_print(text: str, delay: float = 0.03, color: str = Fore.WHITE, end: str = "\n", style: str = ""):
    full_text = style + color + text + Style.RESET_ALL
    for char_index, char in enumerate(full_text):
        if char_index < len(style) + len(color) and char in ['\x1b', '[']:
            sys.stdout.write(char)
            continue
        if char_index >= len(full_text) - len(Style.RESET_ALL) and char in ['\x1b', '[']:
            sys.stdout.write(char)
            continue

        sys.stdout.write(char)
        sys.stdout.flush()
        if not (char_index < len(style) + len(color) and char in ['\x1b', '[']) and \
           not (char_index >= len(full_text) - len(Style.RESET_ALL) and char in ['\x1b', '[']):
            time.sleep(delay)
    sys.stdout.write(end)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title: str, color: str = Fore.CYAN, char: str = "="):
    width = 60
    title_line = f"{char*5} {title.upper()} {char*5}"
    padding_total = width - len(title_line)
    padding_side = padding_total // 2
    print(color + Style.BRIGHT + char * width)
    print(color + Style.BRIGHT + char * padding_side + title_line + char * (padding_total - padding_side) )
    print(color + Style.BRIGHT + char * width + Style.RESET_ALL)

def get_player_input(prompt: str, color: str = Fore.YELLOW) -> str:
    return input(color + prompt + Style.RESET_ALL)

def show_loading_bar(duration: float = 1.5, message: str = "PRZETWARZANIE ŻĄDANIA...", color: str = Fore.MAGENTA):
    slow_print(message, delay=0.02, color=color)
    bar_length = 30
    for i in range(bar_length + 1):
        percent = 100.0 * i / bar_length
        bar = '█' * i + '-' * (bar_length - i)
        sys.stdout.write(Fore.GREEN + f"\r[{bar}] {percent:.0f}%")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    sys.stdout.write(Fore.GREEN + "\r[" + '█' * bar_length + "] 100% - Zakończono.\n" + Style.RESET_ALL)

class GameManager:
    def move(self, direction: str) -> None:
        node = self.get_current_node()
        if not node:
            slow_print("Nie jesteś połączony z żadnym węzłem.", color=Fore.RED)
            return
        direction = direction.lower()
        if direction not in node.connected_nodes:
            slow_print(f"Nie można przejść w kierunku '{direction}'. Dostępne: {', '.join(node.connected_nodes.keys())}", color=Fore.YELLOW)
            return
        target_node_id = node.connected_nodes[direction]
        if target_node_id == "locked":
            slow_print("To połączenie jest zablokowane.", color=Fore.RED)
            return
        self.current_node_id = target_node_id
        slow_print(f"Przemieszczono do: {direction.capitalize()} -> {target_node_id}", color=Fore.CYAN)
        self.look_around()

    def look_around(self) -> None:
        node = self.get_current_node()
        if not node:
            slow_print("Nie jesteś połączony z żadnym węzłem.", color=Fore.RED)
            return
        display_header(f"WĘZEŁ: {node.name}", color=Fore.CYAN)
        slow_print(node.get_description(), color=Fore.WHITE)
        if self.player:
            slow_print(f"Status systemu: {self.player}", color=Fore.LIGHTGREEN_EX)
    def __init__(self):
        self.player: Optional[entities.Player] = None
        self.server_map: world.ServerMap = world.ServerMap()
        map_load_success = self.server_map.load_map_from_json(MAP_FILE)
        if not map_load_success:
            slow_print(f"Ostrzeżenie: Nie udało się wczytać mapy z '{MAP_FILE}'. Tworzenie mapy domyślnej.", color=Fore.YELLOW)
            self.server_map.build_default_map_if_json_fails()
            if not os.path.exists(MAP_FILE):
                self._save_default_map_if_needed()
        self.current_node_id: Optional[str] = self.server_map.start_node_id
        self.game_state: str = "splash_screen"
        self.current_user: Optional[str] = None
        self.users: Dict[str, Dict[str, Any]] = self._load_user_data()
        self.quest_manager: quests.QuestManager = quests.QuestManager()
        qm_load_msg = self.quest_manager.load_quests_from_json(QUEST_FILE)
        self.game_dialogues: Dict[str, str] = self._load_dialogues()

    def _save_default_map_if_needed(self):
        if not self.server_map.nodes:
            self.server_map.build_default_map_if_json_fails()
        if self.server_map.nodes and not os.path.exists(MAP_FILE):
            slow_print(f"Tworzenie domyślnego pliku mapy '{MAP_FILE}'...", color=Fore.CYAN)
            default_map_data_to_save = []
            for node_obj in self.server_map.nodes.values():
                enemies_defs = [{"type": e.enemy_type, "name": e.name, "integrity": e.max_integrity, 
                                 "attack": e.attack_power, "defense": e.defense_power, "xp": e.xp_value,
                                 "loot_definitions": [{"type": li.__class__.__name__, "name": li.name, "description": li.description} for li in e.loot]
                                 } for e in node_obj.enemies]
                items_defs = []
                for i in node_obj.items_on_ground:
                    item_data = {"type": i.__class__.__name__, "name": i.name, "description": i.description}
                    if isinstance(i, items_skills.DataFragment): item_data["value"] = i.value
                    items_defs.append(item_data)
                default_map_data_to_save.append({
                    "node_id": node_obj.node_id, "name": node_obj.name, "description": node_obj.description,
                    "connected_nodes": node_obj.connected_nodes, "enemies_definitions": enemies_defs,
                    "items_definitions": items_defs, "puzzle": node_obj.puzzle
                })
            try:
                with open(MAP_FILE, 'w', encoding='utf-8') as f_map:
                    json.dump(default_map_data_to_save, f_map, indent=4, ensure_ascii=False)
                slow_print(f"Domyślna mapa serwera została zapisana do '{MAP_FILE}'.", color=Fore.GREEN)
            except Exception as e:
                slow_print(f"Nie udało się zapisać domyślnej mapy: {e}", color=Fore.RED)

    def display_splash_screen_and_init(self):
        clear_screen()
        print(Fore.MAGENTA + Style.BRIGHT + r"""
________          __             ___ ___         .__          __   
\______ \ _____ _/  |______     /   |   \   ____ |__| _______/  |_ 
 |    |  \\__  \\   __\__  \   /    ~    \_/ __ \|  |/  ___/\   __\
 |    `   \/ __ \|  |  / __ \_ \    Y    /\  ___/|  |\___ \  |  |  
/_______  (____  /__| (____  /  \___|_  /  \___  >__/____  > |__|  
        \/     \/          \/         \/       \/        \/        
            """)
        print(Fore.CYAN + Style.BRIGHT + "            Wersja 0.3 - 'System Core Breach'\n")
        slow_print("Inicjalizacja Głównego Systemu...", delay=0.04, color=Fore.GREEN)
        show_loading_bar(duration=1.5, message="Łączenie z Matrycą Danych OmniCorp...")
        slow_print("System gotowy do operacji.", color=Fore.GREEN)
        time.sleep(1)
        self.game_state = "login_menu"

    def _load_dialogues(self) -> Dict[str, str]:
        try:
            with open(DIALOGUE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
        return {}

    def _load_user_data(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                pass
        return {"admin": {"password": "nimda", "type": "admin"}}

    def _save_user_data(self) -> None:
        try:
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
        except IOError:
            slow_print("KRYTYCZNY BŁĄD SYSTEMU: Nie można zapisać danych użytkowników.", color=Fore.RED)

    def create_new_user_account(self) -> None:
        clear_screen()
        display_header("Tworzenie Nowego Profilu Hakera", color=Fore.MAGENTA)
        while True:
            username = get_player_input("Podaj nowy login (min. 3 znaki): ")
            if len(username) < 3:
                slow_print("Login musi mieć co najmniej 3 znaki.", color=Fore.RED)
                continue
            if username in self.users:
                slow_print("Ten login jest już zajęty. Wybierz inny.", color=Fore.RED)
            else:
                break
        while True:
            password = get_player_input("Podaj hasło (min. 5 znaków): ")
            if len(password) < 5:
                slow_print("Hasło musi mieć co najmniej 5 znaków.", color=Fore.RED)
                continue
            password_confirm = get_player_input("Potwierdź hasło: ")
            if password == password_confirm:
                break
            else:
                slow_print("Hasła nie pasują do siebie. Spróbuj ponownie.", color=Fore.RED)
        self.users[username] = {"password": password, "type": "user"}
        self._save_user_data()
        slow_print(f"Profil '{username}' został pomyślnie utworzony w systemie!", color=Fore.GREEN)
        slow_print("Możesz się teraz zalogować, używając swoich danych.", color=Fore.CYAN)
        time.sleep(2)

    def attempt_login(self) -> None:
        clear_screen()
        display_header("Logowanie do Systemu OmniCorp", color=Fore.RED)
        username = get_player_input("Login: ")
        password = get_player_input("Hasło: ") 
        user_info = self.users.get(username)
        if user_info and user_info["password"] == password:
            self.current_user = username
            show_loading_bar(duration=1, message=f"Uwierzytelnianie sesji dla {username}...")
            slow_print(f"Zalogowano pomyślnie jako: {username} (Typ: {user_info['type']}).", color=Fore.GREEN)
            time.sleep(0.5)
            if user_info['type'] == 'admin':
                self.game_state = "admin_panel"
            else:
                self.game_state = "user_main_menu"
        else:
            slow_print("Błąd: Nieprawidłowy login lub hasło. Dostęp zabroniony.", color=Fore.RED)
            time.sleep(1.5)
            
    def admin_panel_actions(self):
        clear_screen()
        display_header("Panel Administratora Systemu", color=Fore.MAGENTA)
        slow_print("Dostępne operacje:", color=Fore.CYAN)
        print(Fore.GREEN + "1. Wyświetl dane użytkownika i jego zapis gry")
        print(Fore.GREEN + "2. Zmień hasło użytkownika")
        print(Fore.RED   + "4. Wyloguj z panelu admina")
        choice = get_player_input("Wybierz operację: ")
        if choice == '1':
            user_to_view = get_player_input("Podaj login użytkownika do wglądu: ")
            if user_to_view in self.users:
                slow_print(f"Dane profilu dla '{user_to_view}': {self.users[user_to_view]}", color=Fore.LIGHTWHITE_EX)
                save_file_path_admin = f"{SAVE_FILE_USER_PREFIX}{user_to_view}.json"
                if os.path.exists(save_file_path_admin):
                    try:
                        with open(save_file_path_admin, 'r', encoding='utf-8') as f:
                            game_data = json.load(f)
                        slow_print(f"Zapisana sesja dla '{user_to_view}':", color=Fore.CYAN)
                        print(json.dumps(game_data, indent=2, ensure_ascii=False))
                    except Exception as e:
                        slow_print(f"Nie można wczytać zapisu sesji dla '{user_to_view}': {e}", color=Fore.RED)
                else:
                    slow_print(f"Brak zapisanej sesji dla '{user_to_view}'.", color=Fore.YELLOW)
            else:
                slow_print("Użytkownik o podanym loginie nie istnieje.", color=Fore.RED)
        elif choice == '4':
            slow_print("Wylogowywanie z panelu administratora...", color=Fore.MAGENTA)
            self.current_user = None
            self.game_state = "login_menu"
        else:
            slow_print("Nieznana operacja.", color=Fore.YELLOW)
        if choice != '4': input(Fore.CYAN + "\nNaciśnij Enter, aby kontynuować w panelu admina...")

    def start_new_game(self) -> None:
        if not self.current_user:
            slow_print("KRYTYCZNY BŁĄD: Brak zalogowanego użytkownika do rozpoczęcia nowej sesji.", color=Fore.RED)
            self.game_state = "login_menu"
            return
        clear_screen()
        display_header("Inicjalizacja Nowej Sesji Hakera", color=Fore.GREEN)
        player_name_choice = ""
        while player_name_choice not in ['t', 'n']:
            player_name_choice = get_player_input(f"Chcesz użyć nazwy '{self.current_user}' dla swojego hakera? (t/n): ").lower()
        if player_name_choice == 't':
            player_name = self.current_user
        else:
            while True:
                player_name = get_player_input("Wpisz unikalną nazwę (alias) swojego hakera: ")
                if player_name: break
                slow_print("Nazwa hakera nie może być pusta.", color=Fore.RED)
        self.player = entities.Player(name=player_name, integrity=100, attack_power=8, defense_power=2)
        self.current_node_id = self.server_map.start_node_id
        if self.player:
            self.player.inventory = items_skills.Inventory(capacity=8)
            self.player.skills = [
                items_skills.SystemScanSkill(
                    "Skaner Podstawowy v1.0",
                    "Skanuje system celu, ujawniając jego podstawowe parametry.",
                    5
                )
            ]
            self.quest_manager.active_quests_ids = []
            self.quest_manager.completed_quests_ids = []
            if "EV001" in self.quest_manager.quests:
                 messages = self.quest_manager.activate_quest_by_id("EV001", self.player, self.game_dialogues)
                 for msg in messages: slow_print(msg, color=Fore.MAGENTA if "Nowe zadanie" in msg else Fore.LIGHTWHITE_EX)
            else:
                slow_print("Ostrzeżenie: Startowe zadanie 'EV001' nie zostało znalezione w definicjach zadań.", color=Fore.YELLOW)
        self.game_state = "exploration"
        slow_print(f"\nUstanowiono połączenie dla hakera: {self.player.name if self.player else 'Anonim'}", color=Fore.CYAN)
        show_loading_bar(duration=1.5, message="Wczytywanie środowiska wirtualnego...")
        if self.player: self.look_around()

    def get_save_file_path(self) -> Optional[str]:
        if self.current_user:
            return f"{SAVE_FILE_USER_PREFIX}{self.current_user}.json"
        return None

    def save_game(self) -> None:
        if not self.player or not self.current_node_id:
            slow_print("Brak aktywnej sesji do zsynchronizowania (zapisu).", color=Fore.YELLOW)
            return
        save_file_path = self.get_save_file_path()
        if not save_file_path:
            slow_print("KRYTYCZNY BŁĄD SYSTEMU: Nie można określić ścieżki zapisu (brak aktywnego użytkownika).", color=Fore.RED)
            return
        player_data = {
            "name": self.player.name, "max_integrity": self.player.max_integrity,
            "current_integrity": self.player.current_integrity, "attack_power": self.player.attack_power,
            "defense_power": self.player.defense_power, "bandwidth": self.player.bandwidth,
            "max_bandwidth": self.player.max_bandwidth, "cpu_cycles": self.player.cpu_cycles,
            "security_level": self.player.security_level, "data_currency": self.player.data_currency,
            "inventory": self.player.inventory.to_dict(),
            "skills": [{"name": s.name, "cooldown_current": s.cooldown_current} for s in self.player.skills]
        }
        nodes_state_data = {nid: {"puzzle_solved": node.puzzle_solved, 
                                  "enemies_defeated_permanently": [e.name for e in node.enemies if e.is_defeated()]} 
                            for nid, node in self.server_map.nodes.items()}
        save_data = {
            "player": player_data, "current_node_id": self.current_node_id,
            "nodes_state": nodes_state_data, "quests": self.quest_manager.get_quests_save_data()
        }
        try:
            with open(save_file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)
            slow_print("System zsynchronizowany (Sesja zapisana). Stan twojego profilu jest aktualny.", color=Fore.GREEN)
        except IOError:
            slow_print("BŁĄD KRYTYCZNY: Nie można zsynchronizować systemu (zapisać sesji).", color=Fore.RED)

    def load_game(self) -> bool:
        save_file_path = self.get_save_file_path()
        if not save_file_path or not os.path.exists(save_file_path):
            return False
        show_loading_bar(0.5, f"Wczytywanie zapisanego stanu dla {self.current_user}...")
        try:
            with open(save_file_path, 'r', encoding='utf-8') as f:
                load_data = json.load(f)
            player_data = load_data["player"]
            self.player = entities.Player(
                name=player_data["name"], integrity=player_data["max_integrity"],
                attack_power=player_data["attack_power"], defense_power=player_data["defense_power"]
            )
            self.player.current_integrity = player_data["current_integrity"]
            self.player.bandwidth = player_data["bandwidth"]
            self.player.max_bandwidth = player_data.get("max_bandwidth", 100)
            self.player.cpu_cycles = player_data["cpu_cycles"]
            self.player.security_level = player_data["security_level"]
            self.player.data_currency = player_data["data_currency"]
            self.player.inventory = items_skills.Inventory.from_dict(player_data.get("inventory", []))
            loaded_skills_data = player_data.get("skills", [])
            self.player.skills = []
            all_possible_skills_map = {
                "Skaner Podstawowy v1.0": items_skills.SystemScanSkill("Skaner Podstawowy v1.0", "Skanuje system celu.", 5, cooldown=1),
                "Słaby Wirus 'Robak'": items_skills.ExploitSkill("Słaby Wirus 'Robak'", "Prosty wirus.", 15, 20.0, cooldown=2),
                "Mini-Naprawa": items_skills.SystemPatchSkill("Mini-Naprawa", "Naprawia integralność.", 20, 25.0, cooldown=3),
                "Zaawansowany Backdoor": items_skills.ExploitSkill("Zaawansowany Backdoor", "Potężniejszy exploit.", 25, 35.0, cooldown=3)
            }
            for skill_data in loaded_skills_data:
                skill_name = skill_data.get("name")
                skill_obj_template = all_possible_skills_map.get(skill_name)
                if skill_obj_template:
                    if isinstance(skill_obj_template, items_skills.ExploitSkill):
                        new_skill_instance = type(skill_obj_template)(
                            skill_obj_template.name,
                            skill_obj_template.description,
                            skill_obj_template.bandwidth_cost,
                            skill_obj_template.base_damage,
                            skill_obj_template.cooldown_max
                        )
                    elif isinstance(skill_obj_template, items_skills.SystemPatchSkill):
                        new_skill_instance = type(skill_obj_template)(
                            skill_obj_template.name,
                            skill_obj_template.description,
                            skill_obj_template.bandwidth_cost,
                            skill_obj_template.integrity_restore_base,
                            skill_obj_template.cooldown_max
                        )
                    elif isinstance(skill_obj_template, items_skills.SystemScanSkill):
                        new_skill_instance = type(skill_obj_template)(
                            skill_obj_template.name,
                            skill_obj_template.description,
                            skill_obj_template.bandwidth_cost,
                            skill_obj_template.cooldown_max
                        )
                    else:
                        new_skill_instance = type(skill_obj_template)(
                            skill_obj_template.name,
                            skill_obj_template.description,
                            skill_obj_template.bandwidth_cost,
                            skill_obj_template.cooldown_max
                        )
                    new_skill_instance.cooldown_current = skill_data.get("cooldown_current", 0)
                    self.player.skills.append(new_skill_instance)
            self.current_node_id = load_data["current_node_id"]
            nodes_state_data = load_data.get("nodes_state", {})
            for node_id, state_data in nodes_state_data.items():
                if node_id in self.server_map.nodes:
                    node_to_update = self.server_map.nodes[node_id]
                    node_to_update.puzzle_solved = state_data.get("puzzle_solved", False)
            quests_save_data = load_data.get("quests")
            if quests_save_data and self.player:
                self.quest_manager.load_quests_from_save_data(quests_save_data)
            self.game_state = "exploration"
            slow_print(f"Zapisany stan systemu dla '{self.player.name if self.player else ''}' wczytany pomyślnie.", color=Fore.GREEN)
            if self.player: self.look_around()
            return True
        except (IOError, json.JSONDecodeError, KeyError, TypeError) as e:
            slow_print(f"KRYTYCZNY BŁĄD: Nie można wczytać zapisanego stanu systemu. Plik może być uszkodzony lub niekompletny. ({e})", color=Fore.RED)
            slow_print("Rozpoczynanie nowej sesji może być konieczne.", color=Fore.YELLOW)
            self.player = None 
            return False

    def get_current_node(self) -> Optional[world.ServerNode]:
        if self.current_node_id:
            return self.server_map.get_node(self.current_node_id)
        return None

    def pick_up_item(self, item_name_query: str) -> None:
        if not self.player: return
        node = self.get_current_node()
        if node:
            item_to_pick = node.remove_item_from_ground(item_name_query)
            if item_to_pick:
                added, add_msg = self.player.inventory.add_item(item_to_pick)
                slow_print(add_msg, color=Fore.GREEN if added else Fore.YELLOW)
                if added:
                    update_msgs = self.quest_manager.update_objective_progress("collect_item", item_to_pick.name, player=self.player, game_dialogues=self.game_dialogues)
                    for msg in update_msgs: slow_print(msg, color=Fore.MAGENTA)
                    if item_to_pick.name == "Moduł Wirusa 'Robak'":
                        skill_msg = self.player.learn_skill(items_skills.ExploitSkill("Słaby Wirus 'Robak'", "Prosty wirus zadający niewielkie obrażenia.", 15, 20.0, cooldown=2))
                        if skill_msg: slow_print(skill_msg, color=Fore.CYAN)
                else:
                    node.items_on_ground.append(item_to_pick)
            else:
                slow_print(f"Nie znaleziono '{item_name_query}' w tym węźle.", color=Fore.YELLOW)

    def interact_with_puzzle(self) -> None:
        if not self.player: return
        node = self.get_current_node()
        if node and node.puzzle and not node.puzzle_solved:
            puzzle_type = node.puzzle.get("type")
            puzzle_id_for_quest = node.puzzle.get("puzzle_id", node.node_id + "_puzzle")
            slow_print(f"Próbujesz wejść w interakcję z zabezpieczeniem typu: {puzzle_type.upper()}", color=Fore.CYAN)
            if puzzle_type == "password_unlock":
                solution_attempt = get_player_input(node.puzzle.get("prompt_interact", "Podaj hasło deszyfrujące: "))
                if solution_attempt == node.puzzle.get("solution"):
                    slow_print(node.puzzle.get("success_message", "Zabezpieczenie pokonane! Dostęp przyznany."), color=Fore.GREEN)
                    node.puzzle_solved = True
                    update_msgs = self.quest_manager.update_objective_progress("solve_puzzle", puzzle_id_for_quest, player=self.player, game_dialogues=self.game_dialogues)
                    for msg in update_msgs: slow_print(msg, color=Fore.MAGENTA)
                    item_reward_def = node.puzzle.get("item_reward_on_solve")
                    if item_reward_def and self.player:
                        temp_inv_reward = items_skills.Inventory.from_dict([item_reward_def])
                        if temp_inv_reward.items:
                            reward_item = temp_inv_reward.items[0]
                            added, add_msg = self.player.inventory.add_item(reward_item)
                            slow_print(f"Otrzymano nagrodę: {reward_item.name} ({add_msg if not added else 'Dodano do repozytorium'})", color=Fore.YELLOW)
                            update_msgs_collect = self.quest_manager.update_objective_progress("collect_item", reward_item.name, player=self.player, game_dialogues=self.game_dialogues)
                            for msg_c in update_msgs_collect: slow_print(msg_c, color=Fore.MAGENTA)
                    unlocks_node_id = node.puzzle.get("unlocks_node_id")
                    if unlocks_node_id:
                        for direction, target_node in list(node.connected_nodes.items()):
                            if target_node == "locked": 
                                node.connected_nodes[direction] = unlocks_node_id
                                slow_print(f"Odblokowano nową ścieżkę sieciową: {direction.capitalize()} -> {unlocks_node_id}", color=Fore.CYAN)
                                break
                else:
                    slow_print(node.puzzle.get("failure_message", "Nieprawidłowa sekwencja. System wykrył próbę obejścia."), color=Fore.RED)
            else:
                slow_print("Nie można bezpośrednio wejść w interakcję z tym typem zabezpieczenia.", color=Fore.YELLOW)

    def initiate_combat(self, enemies_in_node: List[entities.Enemy]) -> None:
        if not self.player: return
        living_enemies = [e for e in enemies_in_node if not e.is_defeated()]
        if not living_enemies:
            if self.game_state == "combat": self.game_state = "exploration"
            return
        self.game_state = "combat"
        clear_screen()
        display_header("KONFRONTACJA SYSTEMOWA", color=Fore.RED)
        show_loading_bar(0.7, "Analiza wektorów ataku...", color=Fore.LIGHTRED_EX)
        enemy_to_fight = living_enemies[0]
        slow_print(f"Naprzeciwko staje: {Fore.RED + Style.BRIGHT + enemy_to_fight.name}{Style.RESET_ALL} [{enemy_to_fight.enemy_type}]", delay=0.02)
        turn_count = 1
        while self.player and not self.player.is_defeated() and not enemy_to_fight.is_defeated():
            for skill_in_list in self.player.skills:
                skill_in_list.tick_cooldown()
            print(Fore.CYAN + f"\n--- TURA {turn_count} ---")
            slow_print(f"TY: {self.player}", delay=0.01, color=Fore.GREEN)
            slow_print(f"WRÓG: {enemy_to_fight}", delay=0.01, color=Fore.RED)
            print(Fore.YELLOW + "\nTwoje akcje:")
            print(Fore.WHITE + "  a - Atak podstawowy (niska skuteczność, nie zużywa pasma)")
            print(Fore.WHITE + "  u [numer] - Użyj programu (umiejętności)")
            print(Fore.WHITE + "  p [numer] - Użyj oprogramowania (przedmiotu z repozytorium)")
            print(Fore.WHITE + "  s - Pokaż dostępne programy (umiejętności)")
            print(Fore.WHITE + "  r - Pokaż zawartość repozytorium (ekwipunek)")
            action_input = get_player_input("Wybierz akcję taktyczną: ").lower().split()
            command = action_input[0] if action_input else ""
            args_combat = action_input[1:]
            action_performed_msg = ""
            if command == 'a':
                action_performed_msg = self.player.attack(enemy_to_fight)
            elif command == 'u':
                if args_combat and args_combat[0].isdigit():
                    skill_idx = int(args_combat[0]) - 1
                    action_performed_msg = self.player.use_skill(skill_idx, enemy_to_fight)
                else:
                    action_performed_msg = "Podaj numer programu do użycia (np. 'u 1'). Użyj 's' aby zobaczyć listę."
            elif command == 'p':
                 if args_combat and args_combat[0].isdigit():
                    item_idx = int(args_combat[0]) - 1
                    action_performed_msg = self.player.use_item(item_idx, enemy_to_fight)
                 else:
                    action_performed_msg = "Podaj numer oprogramowania (np. 'p 1'). Użyj 'r' aby zobaczyć listę."
            elif command == 's':
                slow_print(self.player.list_skills(), color=Fore.LIGHTBLUE_EX)
                continue 
            elif command == 'r':
                slow_print(self.player.inventory.list_items(), color=Fore.LIGHTGREEN_EX)
                continue
            else:
                action_performed_msg = "Nieznane polecenie taktyczne."
            if action_performed_msg:
                slow_print(action_performed_msg, delay=0.02, color=Fore.LIGHTWHITE_EX)
            if enemy_to_fight.is_defeated():
                slow_print(f"\n{Fore.GREEN + Style.BRIGHT}{enemy_to_fight.name} zneutralizowany!{Style.RESET_ALL}", delay=0.02)
                xp_gain = enemy_to_fight.xp_value
                slow_print(f"Przejęto {xp_gain} cykli CPU.", color=Fore.YELLOW)
                if self.player: self.player.cpu_cycles += xp_gain 
                if enemy_to_fight.loot:
                    slow_print("Przejęte dane/oprogramowanie z systemu wroga:", color=Fore.CYAN)
                    for item_loot in enemy_to_fight.loot:
                        if self.player: 
                            added, add_msg = self.player.inventory.add_item(item_loot)
                            slow_print(f"- {item_loot.name} ({Fore.GREEN if added else Fore.YELLOW}{add_msg.split(':')[-1].strip()}{Fore.CYAN})", color=Fore.CYAN, delay=0.01)
                q_update_msgs = []
                if self.player:
                    q_update_msgs.extend(self.quest_manager.update_objective_progress("defeat_enemy", enemy_to_fight, player=self.player, game_dialogues=self.game_dialogues))
                for msg in q_update_msgs: slow_print(msg, color=Fore.MAGENTA, delay=0.01)
                if self.player:
                    level_up_msgs = []
                    current_player_level = self.player.security_level
                    while self.player.cpu_cycles >= self.player.security_level * (100 + (self.player.security_level-1) * 30):
                        if self.player.security_level > current_player_level:
                            level_up_msgs.extend(self.player.level_up())
                        else:
                            current_player_level_before_up = self.player.security_level
                            level_up_msgs.extend(self.player.level_up())
                            if self.player.security_level == current_player_level_before_up:
                                break 
                    for msg in level_up_msgs: slow_print(msg, color=Fore.MAGENTA, style=Style.BRIGHT, delay=0.02)
                break
            if self.player and self.player.is_defeated():
                slow_print(f"\n{Fore.RED + Style.BRIGHT}System {self.player.name} krytycznie uszkodzony... Rozłączanie...{Style.RESET_ALL}", delay=0.02)
                self.game_state = "game_over"
                break
            time.sleep(0.5)
            slow_print(Fore.LIGHTRED_EX + "\n--- Tura Systemu Wroga ---", delay=0.02)
            enemy_action_msg = enemy_to_fight.enemy_turn(self.player)
            slow_print(enemy_action_msg, delay=0.02, color=Fore.LIGHTRED_EX)
            if self.player and self.player.is_defeated():
                slow_print(f"\n{Fore.RED + Style.BRIGHT}System {self.player.name} krytycznie uszkodzony... Rozłączanie...{Style.RESET_ALL}", delay=0.02)
                self.game_state = "game_over"
                break
            turn_count +=1
            input(Fore.CYAN + "\nNaciśnij Enter, aby kontynuować konfrontację...")
            clear_screen()
            display_header("KONFRONTACJA SYSTEMOWA", color=Fore.RED)
        if self.game_state == "combat":
            self.game_state = "exploration"
        slow_print("*"*15 + f" {Fore.GREEN if not (self.player and self.player.is_defeated()) else Fore.RED}KONIEC KONFRONTACJI{Style.RESET_ALL} " + "*"*15, delay=0.02)
        if self.game_state == "exploration" and self.player and not self.player.is_defeated():
            self.look_around()