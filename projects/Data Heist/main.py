from game_manager import GameManager, MAP_FILE, USER_DATA_FILE, QUEST_FILE, DIALOGUE_FILE, \
                         slow_print, clear_screen, display_header, get_player_input
import os 
import json 
import time
from colorama import Fore, Style

def ensure_data_files_exist():
    files_to_check = {
        USER_DATA_FILE: {"admin": {"password": "nimda", "type": "admin"}},
        MAP_FILE: [],
        QUEST_FILE: [],
        DIALOGUE_FILE: {}
    }
    for filename, default_content in files_to_check.items():
        if not os.path.exists(filename):
            slow_print(f"Plik '{filename}' nie istnieje. Tworzenie domyślnego pliku...", color=Fore.YELLOW)
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f, indent=4, ensure_ascii=False)
                slow_print(f"Utworzono '{filename}'.", color=Fore.GREEN)
            except Exception as e:
                slow_print(f"Błąd podczas tworzenia pliku '{filename}': {e}", color=Fore.RED)

def display_login_menu_ui():
    clear_screen()
    display_header("DATA HEIST v0.3 - System Logowania", color=Fore.RED)
    print(Fore.GREEN + "  1. Zaloguj się do istniejącego profilu")
    print(Fore.CYAN  + "  2. Stwórz nowy profil hakera")
    print(Fore.YELLOW+ "  3. Wyjdź z systemu")
    print(Fore.RED   + "="*60 + Style.RESET_ALL)

def display_user_main_menu_ui(username: str):
    clear_screen()
    display_header(f"Główny Interfejs Sieci - Haker: {username}", color=Fore.GREEN)
    print(Fore.CYAN  + "  1. Kontynuuj poprzednią sesję / Rozpocznij nową infiltrację")
    print(Fore.YELLOW+ "  2. Zsynchronizuj stan systemu (Zapisz)")
    print(Fore.RED   + "  3. Wyloguj się")
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)

def display_exploration_menu_ui(player_name: str, node_name: str, node_id: str, active_quests_count: int):
    display_header(f"Węzeł: {node_name} ({node_id}) | Haker: {player_name}", color=Fore.CYAN)
    print(Fore.YELLOW + "Dostępne komendy taktyczne:")
    cmds = [
        ("ruch [kierunek]", "Nawigacja (np. 'ruch dalej')"),
        ("rozejrzyj", "Ponowny skan aktualnego węzła"),
        (f"zadania ({active_quests_count})", "Wyświetl aktywne zadania systemowe"),
        ("podnies [nazwa]", "Pobierz dane/oprogramowanie (np. 'podnies Logi')"),
        ("ekwipunek / r", "Pokaż zawartość repozytorium danych"),
        ("programy / s", "Pokaż zainstalowane programy (umiejętności)"),
        ("uzyj_prog [nr]", "Uruchom program na celu (jeśli jest)"),
        ("uzyj_ekw [nr]", "Aktywuj oprogramowanie z repozytorium"),
        ("interakcja", "Spróbuj ominąć zabezpieczenie systemowe"),
        ("staty", "Wyświetl parametry swojego systemu"),
        ("zapisz", "Zsynchronizuj stan systemu (Zapisz sesję)"),
        ("pomoc", "Wyświetl tę listę komend"),
        ("menu", "Powrót do głównego interfejsu sieci")
    ]
    for cmd, desc in cmds:
        print(Fore.WHITE + f"  {cmd:<18} - {desc}")
    print(Fore.CYAN + "-"*60 + Style.RESET_ALL)

def main():
    ensure_data_files_exist()
    gm = GameManager()
    
    if gm.game_state == "splash_screen":
        gm.display_splash_screen_and_init()

    while True:
        if gm.game_state == "login_menu":
            display_login_menu_ui()
            choice = get_player_input("Wybierz operację (1-3): ")
            if choice == '1':
                gm.attempt_login()
            elif choice == '2':
                gm.create_new_user_account()
            elif choice == '3':
                slow_print("Rozłączanie z systemu Data Heist... Do następnego włamania!", color=Fore.MAGENTA, delay=0.04)
                break
            else:
                slow_print("Nieznana operacja. Wybierz numer z dostępnych opcji.", color=Fore.YELLOW)
                time.sleep(1)

        elif gm.game_state == "admin_panel":
            if gm.current_user and gm.users.get(gm.current_user, {}).get("type") == "admin":
                gm.admin_panel_actions()
            else:
                slow_print("BŁĄD: Brak uprawnień administratora. Przekierowywanie do logowania.", color=Fore.RED)
                gm.current_user = None
                gm.game_state = "login_menu"
                time.sleep(1.5)
        
        elif gm.game_state == "user_main_menu":
            if not gm.current_user:
                gm.game_state = "login_menu"
                continue
            display_user_main_menu_ui(gm.current_user)
            choice = get_player_input("Wybierz opcję (1-3): ")
            if choice == '1':
                clear_screen()
                if gm.player:
                    slow_print(f"Wznawianie sesji dla {gm.player.name}...", color=Fore.CYAN)
                    gm.game_state = "exploration"
                    gm.look_around() 
                elif not gm.load_game():
                    gm.start_new_game() 
            elif choice == '2':
                gm.save_game()
                time.sleep(1)
            elif choice == '3':
                slow_print("Wylogowywanie z interfejsu sieciowego...", color=Fore.YELLOW)
                gm.current_user = None
                gm.player = None 
                gm.game_state = "login_menu"
                time.sleep(1)
            else:
                slow_print("Nieznana opcja.", color=Fore.YELLOW)
                time.sleep(1)

        elif gm.game_state == "exploration":
            if not gm.player or not gm.current_node_id:
                slow_print("KRYTYCZNY BŁĄD SYSTEMU: Utracono dane sesji gracza lub połączenie z węzłem. Powrót do logowania.", color=Fore.RED, delay=0.04)
                gm.game_state = "login_menu"
                gm.current_user = None; gm.player = None
                time.sleep(2)
                continue

            current_node_obj = gm.get_current_node()
            node_display_name = current_node_obj.name if current_node_obj else "Nieznany Węzeł"
            
            active_quests_count = len(gm.quest_manager.active_quests_ids) if gm.quest_manager else 0
            display_exploration_menu_ui(gm.player.name, node_display_name, gm.current_node_id, active_quests_count)
            
            action_input_raw = get_player_input(f"{Fore.GREEN}{gm.player.name}{Style.RESET_ALL}@{Fore.CYAN}{node_display_name}{Style.RESET_ALL}$: ")
            action_input = action_input_raw.lower().split()
            
            if not action_input:
                continue

            command = action_input[0]
            args = action_input[1:]
            clear_screen_after_action = True

            if command == "ruch":
                if args: gm.move(args[0])
                else: slow_print("Podaj kierunek ruchu (np. 'ruch dalej').", color=Fore.YELLOW)
            elif command == "rozejrzyj":
                gm.look_around()
            elif command == "zadania":
                slow_print(gm.quest_manager.display_active_quests_string(), color=Fore.LIGHTMAGENTA_EX, delay=0.01)
                clear_screen_after_action = False
            elif command == "podnies":
                if args:
                    item_name_to_pick = " ".join(args)
                    gm.pick_up_item(item_name_to_pick)
                else: slow_print("Podaj nazwę pakietu/programu do podniesienia (np. 'podnies Logi Dostępu').", color=Fore.YELLOW)
            elif command == "ekwipunek" or command == "r":
                if gm.player: slow_print(gm.player.inventory.list_items(), color=Fore.LIGHTGREEN_EX, delay=0.01)
                clear_screen_after_action = False
            elif command == "programy" or command == "s":
                if gm.player: slow_print(gm.player.list_skills(), color=Fore.LIGHTBLUE_EX, delay=0.01)
                clear_screen_after_action = False
            elif command == "uzyj_prog":
                if gm.player and args and args[0].isdigit():
                    skill_idx = int(args[0]) - 1
                    target_enemy = None
                    current_node = gm.get_current_node()
                    if current_node and current_node.has_living_enemies():
                        living_enemies_list = [e for e in current_node.enemies if not e.is_defeated()]
                        if living_enemies_list: target_enemy = living_enemies_list[0]
                    
                    skill_use_msg = gm.player.use_skill(skill_idx, target_enemy)
                    slow_print(skill_use_msg, color=Fore.LIGHTWHITE_EX, delay=0.02)
                    if target_enemy and target_enemy.is_defeated():
                        gm.initiate_combat([])
                    elif current_node and current_node.has_living_enemies() and "wymaga celu" not in skill_use_msg and "Niewystarczające pasmo" not in skill_use_msg and "jest w trakcie" not in skill_use_msg:
                        slow_print(Fore.LIGHTRED_EX + "\n--- System Wroga Odpowiada ---", delay=0.02)
                        if target_enemy and not target_enemy.is_defeated():
                             enemy_action_msg = target_enemy.enemy_turn(gm.player)
                             slow_print(enemy_action_msg, delay=0.02, color=Fore.LIGHTRED_EX)
                             if gm.player.is_defeated(): gm.game_state = "game_over"

                else: slow_print("Format: 'uzyj_prog [numer]'. Użyj 's', aby zobaczyć listę.", color=Fore.YELLOW)
            elif command == "uzyj_ekw":
                if gm.player and args and args[0].isdigit():
                    item_idx = int(args[0]) - 1
                    item_use_msg = gm.player.use_item(item_idx)
                    slow_print(item_use_msg, color=Fore.LIGHTWHITE_EX, delay=0.02)
                    slow_print(f"Aktualny stan systemu: {gm.player}", color=Fore.GREEN, delay=0.01)
                else: slow_print("Format: 'uzyj_ekw [numer]'. Użyj 'r', aby zobaczyć listę.", color=Fore.YELLOW)
            elif command == "interakcja":
                gm.interact_with_puzzle()
                if gm.game_state == "exploration":
                    gm.look_around() 
            elif command == "staty":
                if gm.player: slow_print(str(gm.player), color=Fore.GREEN, delay=0.01)
                clear_screen_after_action = False
            elif command == "zapisz":
                gm.save_game()
            elif command == "pomoc":
                slow_print("Lista dostępnych komend jest wyświetlana powyżej.", color=Fore.MAGENTA)
                clear_screen_after_action = False
            elif command == "menu":
                slow_print("Powrót do głównego interfejsu sieci...", color=Fore.YELLOW)
                gm.game_state = "user_main_menu"
            else:
                slow_print(f"Nieznane polecenie '{command}'. Wpisz 'pomoc' aby zobaczyć listę dostępnych komend.", color=Fore.YELLOW)
            
            if gm.game_state == "exploration" and clear_screen_after_action :
                if command not in ["rozejrzyj", "ruch", "interakcja"]:
                    input(Fore.CYAN + "\nNaciśnij Enter, aby kontynuować eksplorację...")
                    clear_screen()
                    gm.look_around()

        elif gm.game_state == "combat":
            if gm.player and not gm.player.is_defeated() and gm.game_state == "combat":
                slow_print("BŁĄD: Niespodziewany stan systemu walki. Próba powrotu do eksploracji...", color=Fore.RED)
                gm.game_state = "exploration"
                if gm.player: gm.look_around()
            elif gm.player and gm.player.is_defeated():
                gm.game_state = "game_over"

        elif gm.game_state == "game_over":
            clear_screen()
            display_header("SYSTEM KRYTYCZNY - POŁĄCZENIE ZERWANE", color=Fore.RED, char="#")
            slow_print("Twoja ostatnia aktywność została zarejestrowana przez systemy monitorujące OmniCorp.", delay=0.04, color=Fore.LIGHTRED_EX)
            slow_print("Wygląda na to, że ich zabezpieczenia okazały się zbyt potężne... tym razem.", delay=0.04, color=Fore.LIGHTRED_EX)
            slow_print("Może następnym razem uda ci się zinfiltrować Matrycę.", delay=0.04, color=Fore.YELLOW)
            print(Fore.RED + "#"*60 + Style.RESET_ALL)
            get_player_input("Naciśnij Enter, aby wrócić do ekranu logowania...")
            gm.current_user = None
            gm.player = None
            gm.game_state = "login_menu"

if __name__ == "__main__":
    ensure_data_files_exist()
    main()