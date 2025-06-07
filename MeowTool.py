import os
import sys
import time
import random
import asyncio
from shutil import copyfile, rmtree
import datetime
from re import compile, sub, search
from tomlkit import loads, dumps, document, nl, comment, table
import requests # ‾\
import socks    #  | в планах на удаление
import socket   # _/
from aiohttp import ClientSession, TCPConnector, ClientOSError, ContentTypeError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError
from aiohttp_socks import ProxyConnector, ProxyConnectionError, ProxyTimeoutError
import aiofiles
# from fake_useragent import UserAgent; ua = UserAgent()
from emoji import replace_emoji
from columnar import columnar
import colorama; colorama.init()
from msvcrt import getch

# MeowTool

'''
<|> TO DO

    [*] - задача
    [!] - высокий приоритет
    [~] - код для 'Ctrl + F'
    [?] - отложено на неопределённый срок

    [*] Detect Libraries (if not: install)

    Fixes
      Roblox
        [~] fix_it_1 - Нормальная проверка на валид в рефрешере
        [~] fix_it_2 - Работать с датой вида: XX.XX.XXXX XX:XX:XX, а не XX:XX:XX или, если время >60 секунд - сбрасывать таймер, но тогда возникнет ситуация, когда рефреш будет в 23:59:59, то таймер сбросится и следующий рефреш провалится
            Вывод в основном чекере почему-то происходит при условии, что все задачи выполнены
        [~] fix_it_3 - Общий вывод может проспамиться несколько раз
            Редкая ошибка, когда при сохранении информации в файл определённая часть куки переносится на новую строку

    Updates
      Roblox
        [*] [?] Нет проверки валидности в функциях проверки данных - возможен краш
        [*] Улучшить функции с while
        [*] Оптимизация основного чекера
        [*] Переписать автоматическое завершение сессий (async with) на ручное (из-за проблем с прокси, а именно 'Session is closed' без причины)
        [*] В массовором рефрешере настройка для удаления рефрешнутых куки из файла (сохранять файл после каждых 50 рефрешнутых куков)
        [*] Исправить поиск кастомных геймпассов когда он не имеет смысла при выводе количества, а не названий + количества
        [*] [?] Выгрузить все классы игр с бейджами и геймпассами в .json на GitHub и загружать файл от туда
        [*] [?] Парсер разных видов прокси (возможно, дать пользователю самому выбрать вид прокси из предложенных или сделать конструктор вида прокси)
        [*] [?] Поддержка публичных IPv4 прокси (HTTP, HTTPS, SOCKS4, SOCKS5)
        [*] Подсчёт потраченных робуксов в каждом плейсе отдельно [Примеры: Adopt Me: (99 (Может быть писать тут кол-во геймпассов), 9999R$ (А тут их общую ценность)), Murder Mystery 2: (234 (Может быть писать тут кол-во геймпассов), 298526R$ (А тут их общую ценность))]
        [*] Сделать выбор для параметров, которые могут выводить данные в виде массива, а не только числа
        [*] [?] Сортировка с промежуточными значениями [Примеры: 100-200, >99 & <201, >=100 & <=200] (Учесть невозможность использования [<, >] в названиях файлов и папок)
        [*] [?] Режим чекера с топ-N куков (обновление каждые N куков + последний)
        [*] [?] Массовый парсинг бейджей и геймпассов при вводе нескольких айдишников плейсов через запятую/пробел, в случае ввода одного - вывести данные в консоль и сохранить
        [*] [?] Отправка итоговых данных в [Telegram, Discord]
        [*] [?] Возможность сохранения данных в [Excel (CSV, XLS(X)), Access (MDB, ACCDB)]
        [>] [?] Панель управления куками
          [*] Состояние валидности
          [*] Обновление всех данных
        [*] [?] Log:Pass чекер
        [*] [?] Снятие почты

      Configs
        [*] [?] Переписать систему создания и написать проверку целостности при запуске и там, где это нужно

      Proxy
        [*] Раздел нуждается в полном рерайте на библиотеках aiohttp(_socks), asyncio, aiofiles (а также в нормальном коде, а не то, что сейчас)
        [*] Парсер разных видов прокси (возможно, дать пользователю самому выбрать вид прокси из предложенных или сделать конструктор вида прокси)
        [*] Асинхронность
        [*] Многозадачность
        [*] Записывать все прокси из файла в память и там менять

    Global Updates
      [*] [?] Полный рерайт скрипта + интерфейс
      [*] [?] Нормальная система конфигов с проверкой целостности
      [*] [?] Нормальная система переводов в отдельном файле



<|> MAYBE USEFUL INFORMATION

    Roblox
      [*] AssetType: https://create.roblox.com/docs/reference/engine/enums/AssetType
      
      [*] APIs:

        [?] Need cookie: [C+] - Yes, [C-] - No, [C=] - 'Yes' if (profile == Privacy) else 'No'
        [?] Methods:     [G]  - GET, [P]  - POST
        [?] {UserId}:    User ID (without {})
        
        [?] Flags in APIs:

                ?userId=           (User ID)
          [LIM] &limit=            (maximum items per page)
          [CNT] &count=            (maximum items per page)
          [IPP] &itemsPerPage=     (maximum items per page)
          [CSR] &cursor=           (next page)
          [NSR] &nextCursor=       (next page)
          [ESI] &exclusiveStartId= (next page, ID of the last item)
        
        [C+] [G]             Validity:               https://users.roblox.com/v1/users/authenticated
        [C+] [G]             Main Information:       https://www.roblox.com/my/settings/json
        [C+] [G]             Country Registration:   https://users.roblox.com/v1/users/authenticated/country-code
        [C-] [G]             Registration Date:      https://users.roblox.com/v1/users/{UserId}
        [C+] [G]             Robux:                  https://economy.roblox.com/v1/users/{UserId}/currency
        [C+] [G]             Billing:                https://apis.roblox.com/credit-balance/v1/get-conversion-metadata
        [C+] [G]             Transactions For Year:  https://economy.roblox.com/v2/users/{UserId}/transaction-totals?timeFrame=Year&transactionType=summary
        [C+] [G] [LIM] [CSR] Purchases For All Time: https://economy.roblox.com/v2/users/{UserId}/transactions?transactionType=2&limit=100
        [C=] [G] [LIM] [CSR] Rap:                    https://inventory.roblox.com/v1/users/{UserId}/assets/collectibles?sortOrder=Asc&limit=100
        [C+] [G]             Cards:                  https://apis.roblox.com/payments-gateway/v1/payment-profiles
        [C=] [G] [CNT] [ESI] Gamepasses:             https://apis.roblox.com/game-passes/v1/users/{UserId}/game-passes?count=100
        [C=] [G] [LIM] [CSR] Badges:                 https://badges.roblox.com/v1/users/{UserId}/badges?limit=100&sortOrder=Desc
        [C-] [G] [IPP] [CSR] Favorite Places:        https://games.roblox.com/v2/users/{UserId}/favorite/games?limit=100
        [C=] [G] [LIM] [CSR] Bundles:                https://catalog.roblox.com/v1/users/{UserId}/bundles?limit=100
        [C+] [G]             Inventory Privacy:      https://apis.roblox.com/user-settings-api/v1/user-settings/settings-and-options
        [C+] [G]             Trade Privacy:          https://accountsettings.roblox.com/v1/trade-privacy
        [C+] [G]       [NSR] Sessions:               https://apis.roblox.com/token-metadata-service/v1/sessions
        [C+] [G]             Phone:                  https://accountinformation.roblox.com/v1/phone
        [C+] [G]             Verified Age:           https://apis.roblox.com/age-verification-service/v1/age-verification/verified-age
        [C+] [G]             Verified Voice:         https://voice.roblox.com/v1/settings
        [C-] [G]             Friends Count:          https://friends.roblox.com/v1/users/{UserId}/friends/count
        [C-] [G]             Followers Count:        https://friends.roblox.com/v1/users/{UserId}/followers/count
        [C-] [G]             Followings Count:       https://friends.roblox.com/v1/users/{UserId}/followings/count
        [C-] [G]             Roblox Badges:          https://accountinformation.roblox.com/v1/users/{UserId}/roblox-badges
        [C+] [P]             X-CSRF-Token:           https://auth.roblox.com/v2/logout
'''

### ANSI коды

class ANSI:
    class FG: # text colors
        BLACK       = '\033[30m'
        RED         = '\033[31m' # BAD
        GREEN       = '\033[32m' # GOOD
        YELLOW      = '\033[33m' # UI / WARN
        BLUE        = '\033[34m' # UI
        PURPLE      = '\033[35m' # UI
        CYAN        = '\033[36m' # UI / INFO
        WHITE       = '\033[37m'
        GRAY        = '\033[90m' # UI
        LIGHTRED    = '\033[91m'
        LIGHTGREEN  = '\033[92m'
        LIGHTYELLOW = '\033[93m'
        LIGHTBLUE   = '\033[94m'
        PINK        = '\033[95m' # UI
        LIGHTCYAN   = '\033[96m' # UI
        LIGHTWHITE  = '\033[97m'
    class BG: # background colors
        BLACK       = '\033[40m'
        RED         = '\033[41m'
        GREEN       = '\033[42m'
        YELLOW      = '\033[43m'
        BLUE        = '\033[44m'
        PURPLE      = '\033[45m'
        CYAN        = '\033[46m'
        WHITE       = '\033[47m'
        GRAY        = '\033[100m'
        LIGHTRED    = '\033[101m'
        LIGHTGREEN  = '\033[102m'
        LIGHTYELLOW = '\033[103m'
        LIGHTBLUE   = '\033[104m'
        PINK        = '\033[105m'
        LIGHTCYAN   = '\033[106m'
        LIGHTWHITE  = '\033[107m'
    class DECOR: # text decorations
        BOLD            = '\033[1m'
        NOTBOLD         = '\033[2m'
        CURSIVE         = '\033[3m'
        UNDERLINE1      = '\033[4m'  # close to the text
        UNDERLINE2      = '\033[52m' # just below the text
        DOUBLEUNDERLINE = '\033[21m'
        FLASHING1       = '\033[5m'  # [Doesn't Work On Windows 10]
        FLASHING2       = '\033[6m'  #           ^ same ^
        CROSSEDOUT      = '\033[9m'
    # clear colors and decorations
    CLEAR = '\033[0m'

### Переводы

def translateMT(language: str):
    global MT_Number_Of_Threads_For_Valid_Checker, MT_Number_Of_Threads_For_Main_Checker, MT_Incorrect_Number_Of_Threads, MT_Enter_Number_Of_Threads, MT_First_We_Check_For_Valid, MT_Valid, MT_Invalid, MT_First_Check_All_Cookies_For_Valid, MT_No_Proxy_Was_Found, MT_Auto_Protocol, MT_Use_Proxy, MT_Auto_Protocol_If_Not_Specified, MT_Any, MT_Key_To_Continue, MT_File_Is_Missing, MT_Incorrect_Cookies_Removed, MT_Error, MT_50_Cookies_In_Once, MT_50_Cookies_In_60_Seconds, MT_Send_Some_Requests_Through_RoProxy, MT_Rate_Limit_Has_Been_Reached, MT_Checker, MT_Proxy, MT_The_Name_Cannot_Be_Empty, MT_Do_Not_Use_Characters_Such_As, MT_Enter_A_New_Title, MT_Console_Title, MT_Show_Place_ID_Next_To_The_Name, MT_Disable_All_Warnings, MT_Show_Cookie, MT_Data, MT_Find, MT_Save_Invalid_Cookies, MT_Save_Cookies_Added_Manually, MT_History_Manual, MT_Save_Cookies_Checked_By_Checker, MT_History_Checker, MT_Cookie_Control_Panel, MT_Start_Refresher, MT_Wait, MT_Waiting, MT_Can_Continue, MT_Do_You_Sure, MT_I_Am_Sure, MT_Not_Yet, MT_Reset_To_Default_Settings, MT_Reload_Config, MT_New_Cookie, MT_In, MT_Enter_A_Cookie1, MT_Enter_A_Cookie2, MT_Incorrect_Cookie, MT_Invalid_Cookie, MT_Single_Mode, MT_Mass_Mode, MT_Could_Not_Connect_To_The_API, MT_Trying_To_Connect_Again, MT_Bind, MT_Show_Lable_MeowTool, MT_Show_Lable_by_h1kken, MT_The_Parameter_Can_Only_Be_A_Number, MT_Add_A_Parameter, MT_Create_Backups, MT_Save_To_A_File, MT_Sort, MT_Sorting, MT_The_Place_Has_No_Gamepasses_And_Badges, MT_Custom_Places, MT_Enable_All, MT_Disable_All, MT_Id, MT_Name, MT_Link, MT_Duplicated_Cookies_Removed, MT_Unique_Cookies_Found, MT_Successfully_Uploaded_In, MT_Place_ID, MT_Place_Name, MT_Place_Link, MT_Gamepasses, MT_Badges, MT_Remove_Emojies, MT_Remove_Round_Brackets, MT_Remove_Square_Brackets, MT_Upload_All_Info_Gamepasses_And_Badges, MT_Enable_Something_To_Start_Checking, MT_Save_Without_Protocol, MT_Save_In, MT_The_Data_Is_Saved_In, MT_Incorrect_Length_Of_ID_20, MT_Incorrect_Length_Of_Parameter_20, MT_Incorrect_Length_Of_Name_50, MT_Incorrect_Length_Of_Config_Name_60, MT_Gamepass_With_This_Name_Already_Exists, MT_Add_A_Gamepass_Name, MT_Found_Data_On, MT_The_Place_Has_No_Gamepasses, MT_The_Place_Has_No_Badges, MT_Gamepasses_Parser_From_The_Place, MT_Badges_Parser_From_The_Place, MT_Misc, MT_Seconds, MT_Waiting_Time, MT_Output_Total, MT_Found, MT_Lines, MT_Start_Parsing, MT_Enter_The_Parameter_Value, MT_Enter_The_Waiting_Time, MT_Enter_The_Gamepass_Name, MT_Enter_The_Place_ID, MT_Enter_The_Bundle_ID, MT_Gamepasses, MT_Badges, MT_Fix_Console, MT_Settings, MT_General, MT_Main, MT_Places, MT_Language, MT_Configs, MT_Check, MT_Save, MT_Auto_Save_Changes, MT_Update_List, MT_Back, MT_Close_Program, MT_Add_Bundle, MT_Add_ID_Place, MT_Enter_Something, MT_Create_Config, MT_Cancel, MT_Load_On_Launch, MT_Load, MT_File_Location, MT_Rename, MT_Delete, MT_Enter_Name_For_New_Config, MT_Enter_New_Name_For_Config, MT_User_Agreement, MT_User_Agreement_1, MT_User_Agreement_2, MT_User_Agreement_3, MT_User_Agreement_4, MT_Parameter_With_This_Value_Already_Exists, MT_Bundle_With_This_ID_Already_Exists, MT_Place_With_This_ID_Already_Exists, MT_Incorrent_Bundle_ID, MT_Incorrent_Place_ID, MT_Incorrect_File_Name, MT_File_With_This_Name_Already_Exists, MT_Incorrect_Waiting_Time, MT_Incorrect_Value, MT_Of, MT_Start_Checking_File, MT_Finish_Checking_File, MT_Start_Parsing_File, MT_Finish_Parsing_File, MT_Press_Any_Key_To_Continue, MT_Press_Enter_To_Continue, MT_Request, MT_Everything_Or_Something_Is_On, MT_Everything_Is_On_Or_Off, MT_Total, MT_Roblox, MT_Checker, MT_Cookie_Parser, MT_Cookie_Checker, MT_Cookie_Refresher, MT_Beta
    match str(language).upper():
        case 'EN':
            MT_Number_Of_Threads_For_Valid_Checker      = 'Number of threads for valid checker'
            MT_Number_Of_Threads_For_Main_Checker       = 'Number of threads for main checker'
            MT_Incorrect_Number_Of_Threads              = 'Do not exceed the 500 thread limit'
            MT_Enter_Number_Of_Threads                  = 'Enter number of threads'
            MT_First_We_Check_For_Valid                 = 'First we check for valid'
            MT_Valid                                    = 'Valid'
            MT_Invalid                                  = 'Invalid'
            MT_First_Check_All_Cookies_For_Valid        = 'First check all cookies for valid'
            MT_No_Proxy_Was_Found                       = 'No proxy was found, the check was canceled'
            MT_Auto_Protocol                            = 'Auto protocol'
            MT_Use_Proxy                                = 'Use proxy'
            MT_Auto_Protocol_If_Not_Specified           = 'The protocol, if it isn\'t specified in file'
            MT_Any                                      = 'Any'
            MT_Key_To_Continue                          = 'Key to continue'
            MT_File_Is_Missing                          = 'File is missing somewhere, strange...'
            MT_Incorrect_Cookies_Removed                = 'Incorrect cookies removed'
            MT_Error                                    = 'Error'
            MT_50_Cookies_In_Once                       = '50 cookies in once'
            MT_50_Cookies_In_60_Seconds                 = '50 cookies in 60 seconds'
            MT_Send_Some_Requests_Through_RoProxy       = 'Send some requests through RoProxy'
            MT_Rate_Limit_Has_Been_Reached              = 'Rate-Limit has been reached'
            MT_Checker                                  = 'Checker'
            MT_Proxy                                    = 'Proxy'
            MT_The_Name_Cannot_Be_Empty                 = 'The name cannot be empty'
            MT_Do_Not_Use_Characters_Such_As            = 'Do not use characters such as'
            MT_Enter_A_New_Title                        = 'Enter a new title'
            MT_Console_Title                            = 'Console title'
            MT_Show_Place_ID_Next_To_The_Name           = 'Show place ID next to the name'
            MT_Disable_All_Warnings                     = 'Disable all warnings'
            MT_Show_Cookie                              = 'Show cookie'
            MT_Data                                     = 'Data'
            MT_Find                                     = 'Find'
            MT_Save_Invalid_Cookies                     = 'Save invalid cookies'
            MT_Save_Cookies_Added_Manually              = 'Save cookies added manually'
            MT_History_Manual                           = 'History (manual)'
            MT_Save_Cookies_Checked_By_Checker          = 'Save cookies checked by checker'
            MT_History_Checker                          = 'History (checker)'
            MT_Cookie_Control_Panel                     = 'Cookie control panel'
            MT_Start_Refresher                          = 'Start refresher'
            MT_Wait                                     = 'Wait'
            MT_Waiting                                  = 'Waiting'
            MT_Can_Continue                             = 'Can continue'
            MT_Do_You_Sure                              = 'Do you sure?'
            MT_I_Am_Sure                                = 'I am sure'
            MT_Not_Yet                                  = 'Not yet'
            MT_Reset_To_Default_Settings                = 'Reset to default settings'
            MT_Reload_Config                            = 'Reload config'
            MT_New_Cookie                               = 'New cookie'
            MT_In                                       = 'In'
            MT_Enter_A_Cookie1                          = 'Enter a cookie'
            MT_Enter_A_Cookie2                          = 'Enter a cookie'
            MT_Incorrect_Cookie                         = 'Incorrect cookie'
            MT_Invalid_Cookie                           = 'Invalid cookie'
            MT_Single_Mode                              = 'Single mode'
            MT_Mass_Mode                                = 'Mass mode'
            MT_Could_Not_Connect_To_The_API             = 'Couldn\'t connect to the API'
            MT_Trying_To_Connect_Again                  = 'Trying to connect again'
            MT_Bind                                     = 'Bind'
            MT_Show_Lable_MeowTool                      = 'Show lable \'MeowTool\''
            MT_Show_Lable_by_h1kken                     = 'Show lable \'by h1kken :3\''
            MT_The_Parameter_Can_Only_Be_A_Number       = 'The parameter can only be a number'
            MT_Add_A_Parameter                          = 'Add a parameter'
            MT_Create_Backups                           = 'Create backups'
            MT_Save_To_A_File                           = 'Save to a file'
            MT_Sort                                     = 'Sort'
            MT_Sorting                                  = 'Sorting'
            MT_The_Place_Has_No_Gamepasses_And_Badges   = 'The place has no gamepasses and badges'
            MT_Custom_Places                            = 'Custom places'
            MT_Enable_All                               = 'Enable all'
            MT_Disable_All                              = 'Disable all'
            MT_Id                                       = 'ID'
            MT_Name                                     = 'Name'
            MT_Link                                     = 'Link'
            MT_Duplicated_Cookies_Removed               = 'Duplicated cookies removed'
            MT_Unique_Cookies_Found                     = 'Unique cookies found'
            MT_Successfully_Uploaded_In                 = 'Successfully uploaded in'
            MT_Place_ID                                 = 'Place\'s ID'
            MT_Place_Name                               = 'Place\'s name'
            MT_Place_Link                               = 'Place\'s link'
            MT_Gamepasses                               = 'Gamepasses'
            MT_Badges                                   = 'Badges'
            MT_Remove_Emojies                           = 'Remove emojies from the name'
            MT_Remove_Round_Brackets                    = 'Remove (and what is inside them) from the name'
            MT_Remove_Square_Brackets                   = 'Remove [and what is inside them] from the name'
            MT_Upload_All_Info_Gamepasses_And_Badges    = 'Upload all information about gamepasses and badges from the script'
            MT_Enable_Something_To_Start_Checking       = 'Enable something to start checking'
            MT_Save_Without_Protocol                    = 'Save without protocol'
            MT_Save_In                                  = 'Save in'
            MT_The_Data_Is_Saved_In                     = 'The data is saved in'
            MT_Incorrect_Length_Of_ID_20                = 'ID length cannot exceed 20 characters'
            MT_Incorrect_Length_Of_Parameter_20         = 'Parameter length cannot exceed 20 numbers'
            MT_Incorrect_Length_Of_Name_50              = 'Name length cannot exceed 50 characters'
            MT_Incorrect_Length_Of_Config_Name_60       = 'Config name length cannot exceed 60 characters'
            MT_Gamepass_With_This_Name_Already_Exists   = 'Gamepass with this name already exists'
            MT_Add_A_Gamepass_Name                      = 'Add a gamepasse\'s name'
            MT_Found_Data_On                            = 'Found data on'
            MT_The_Place_Has_No_Gamepasses              = 'The place has no gamepasses'
            MT_The_Place_Has_No_Badges                  = 'The place has no badges'
            MT_Gamepasses_Parser_From_The_Place         = 'Gamepasses parser from the place'
            MT_Badges_Parser_From_The_Place             = 'Badges parser from the place'
            MT_Misc                                     = 'Misc'
            MT_Seconds                                  = 'sec'
            MT_Waiting_Time                             = 'Waiting time'
            MT_Output_Total                             = 'Output total'
            MT_Found                                    = 'Found'
            MT_Lines                                    = 'Lines'
            MT_Start_Parsing                            = 'Start parsing'
            MT_Enter_The_Parameter_Value                = 'Enter the parameter value'
            MT_Enter_The_Waiting_Time                   = 'Enter the waiting time in seconds'
            MT_Enter_The_Gamepass_Name                  = 'Enter the gamepasse\'s name'
            MT_Enter_The_Place_ID                       = 'Enter the place\'s ID'
            MT_Enter_The_Bundle_ID                      = 'Enter the bundle\'s ID'
            MT_Gamepasses                               = 'Gamepasses'
            MT_Badges                                   = 'Badges'
            MT_Fix_Console                              = 'Fix console'
            MT_Settings                                 = 'Settings'
            MT_General                                  = 'General'
            MT_Main                                     = 'Main'
            MT_Places                                   = 'Places'
            MT_Language                                 = 'Language'
            MT_Configs                                  = 'Configs'
            MT_Check                                    = 'Check'
            MT_Save                                     = 'Save', 'Save'
            MT_Auto_Save_Changes                        = 'Auto. save changes'
            MT_Update_List                              = 'Update list'
            MT_Back                                     = 'Back'
            MT_Close_Program                            = 'Close the program'
            MT_Add_Bundle                               = 'Add a bundle\'s ID'
            MT_Add_ID_Place                             = 'Add a place\'s ID'
            MT_Enter_Something                          = 'Enter something'
            MT_Create_Config                            = 'Create config'
            MT_Cancel                                   = 'Cancel'
            MT_Load_On_Launch                           = 'Load on launch'
            MT_Load                                     = 'Load'
            MT_File_Location                            = 'File location'
            MT_Rename                                   = 'Rename'
            MT_Delete                                   = 'Delete'
            MT_Enter_Name_For_New_Config                = 'Enter the name for new config'
            MT_Enter_New_Name_For_Config                = 'Enter a new name for config'
            MT_Parameter_With_This_Value_Already_Exists = 'Parameter with this value already exists'
            MT_Bundle_With_This_ID_Already_Exists       = 'Bundle with this ID already exists'
            MT_Place_With_This_ID_Already_Exists        = 'Place with this ID already exists'
            MT_Incorrent_Bundle_ID                      = 'Incorrect bundle\'s ID'
            MT_Incorrent_Place_ID                       = 'Incorrect place\'s ID'
            MT_Incorrect_File_Name                      = 'Incorrect filename'
            MT_File_With_This_Name_Already_Exists       = 'File with this name already exists'
            MT_Incorrect_Waiting_Time                   = 'The waiting time cannot be more than 3600 seconds'
            MT_Incorrect_Value                          = 'Incorrect value'
            MT_Of                                       = 'of'
            MT_Start_Checking_File                      = 'Checking the file'
            MT_Finish_Checking_File                     = 'Checking complete'
            MT_Start_Parsing_File                       = 'Parsing the file'
            MT_Finish_Parsing_File                      = 'Parsing complete'
            MT_Press_Any_Key_To_Continue                = 'Press any key to continue'
            MT_Press_Enter_To_Continue                  = 'Press Enter to continue'
            MT_Request                                  = 'Request'
            MT_Everything_Or_Something_Is_On            = 'everything or something is on, always'
            MT_Everything_Is_On_Or_Off                  = 'everything is on or off, always'
            MT_Total                                    = 'T', 'O', 'T', 'A', 'L'
            MT_Roblox                                   = 'Roblox'
            MT_Cookie_Parser                            = 'Cookie Parser'
            MT_Cookie_Checker                           = 'Cookie Checker'
            MT_Cookie_Refresher                         = 'Cookie Refresher'
            MT_Beta                                     = '[BETA]'
        case _: # 'RU'
            MT_Number_Of_Threads_For_Valid_Checker      = 'Количество потоков на чек валидности'
            MT_Number_Of_Threads_For_Main_Checker       = 'Количество потоков на основной чекер'
            MT_Incorrect_Number_Of_Threads              = 'Не превышай ограничение на 500 потоков'
            MT_Enter_Number_Of_Threads                  = 'Введи количество потоков'
            MT_First_We_Check_For_Valid                 = 'Сначала проверяем на валид'
            MT_Valid                                    = 'Валидных'
            MT_Invalid                                  = 'Невалидных'
            MT_First_Check_All_Cookies_For_Valid        = 'Сначала проверять все куки на валид'
            MT_No_Proxy_Was_Found                       = 'Ни одного прокси не найдено, проверка отменена'
            MT_Auto_Protocol                            = 'Авто протокол'
            MT_Use_Proxy                                = 'Использовать прокси'
            MT_Auto_Protocol_If_Not_Specified           = 'Протокол, если не указан в файле'
            MT_Any                                      = 'Любая'
            MT_Key_To_Continue                          = 'Клавиша для продолжения'
            MT_File_Is_Missing                          = 'Файл куда-то пропал, странно...'
            MT_Incorrect_Cookies_Removed                = 'Удалено некорректных куков'
            MT_Error                                    = 'Ошибка'
            MT_50_Cookies_In_Once                       = '50 куков за раз'
            MT_50_Cookies_In_60_Seconds                 = '50 куков в 60 секунд'
            MT_Send_Some_Requests_Through_RoProxy       = 'Отправлять некоторые запросы через RoProxy'
            MT_Rate_Limit_Has_Been_Reached              = 'Достигнут Rate-Limit'
            MT_Checker                                  = 'Чекер'
            MT_Proxy                                    = 'Прокси'
            MT_The_Name_Cannot_Be_Empty                 = 'Название не может быть пустым'
            MT_Do_Not_Use_Characters_Such_As            = 'Не используй такие символы, как'
            MT_Enter_A_New_Title                        = 'Введи новое название'
            MT_Console_Title                            = 'Название консоли'
            MT_Show_Place_ID_Next_To_The_Name           = 'Показывать ID плейса рядом с названием'
            MT_Disable_All_Warnings                     = 'Отключить все предупреждения'
            MT_Show_Cookie                              = 'Показать куки'
            MT_Data                                     = 'Данные'
            MT_Find                                     = 'Найти'
            MT_Save_Invalid_Cookies                     = 'Сохранять невалидные куки'
            MT_Save_Cookies_Added_Manually              = 'Сохранять куки, добавленные вручную'
            MT_History_Manual                           = 'История (ручная)'
            MT_Save_Cookies_Checked_By_Checker          = 'Сохранять куки, проверенные чекером'
            MT_History_Checker                          = 'История (чекер)'
            MT_Cookie_Control_Panel                     = 'Панель управления куком'
            MT_Start_Refresher                          = 'Запустить рефрешер'
            MT_Wait                                     = 'Подожди'
            MT_Waiting                                  = 'Ожидание'
            MT_Can_Continue                             = 'Можно продолжать'
            MT_Do_You_Sure                              = 'Ты уверен?'
            MT_I_Am_Sure                                = 'Я уверен'
            MT_Not_Yet                                  = 'Ещё нет'
            MT_Reset_To_Default_Settings                = 'Сбросить настройки по умолчанию'
            MT_Reload_Config                            = 'Перезагрузить конфиг'
            MT_New_Cookie                               = 'Новый куки'
            MT_In                                       = 'В'
            MT_Enter_A_Cookie1                          = 'Введи кук'
            MT_Enter_A_Cookie2                          = 'Ввести кук'
            MT_Incorrect_Cookie                         = 'Некорретный кук'
            MT_Invalid_Cookie                           = 'Невалидный куки'
            MT_Single_Mode                              = 'Одиночный режим'
            MT_Mass_Mode                                = 'Массовый режим'
            MT_Could_Not_Connect_To_The_API             = 'Не удалось подключиться к API'
            MT_Trying_To_Connect_Again                  = 'Пытаемся подключиться ещё раз'
            MT_Bind                                     = 'Бинд'
            MT_Show_Lable_MeowTool                      = 'Показывать надпись \'MeowTool\''
            MT_Show_Lable_by_h1kken                     = 'Показывать надпись \'by h1kken :3\''
            MT_The_Parameter_Can_Only_Be_A_Number       = 'Параметр может быть только числом'
            MT_Add_A_Parameter                          = 'Добавить параметр'
            MT_Create_Backups                           = 'Создавать резервные копии'
            MT_Save_To_A_File                           = 'Сохранять в файл'
            MT_Sort                                     = 'Сортировать'
            MT_Sorting                                  = 'Сортировка'
            MT_The_Place_Has_No_Gamepasses_And_Badges   = 'У плейса нет геймпассов и бейджей'
            MT_Custom_Places                            = 'Кастомные плейсы'
            MT_Enable_All                               = 'Включить всё'
            MT_Disable_All                              = 'Выключить всё'
            MT_Id                                       = 'Айди'
            MT_Name                                     = 'Название'
            MT_Link                                     = 'Ссылка'
            MT_Duplicated_Cookies_Removed               = 'Удалено одинаковых куков'
            MT_Unique_Cookies_Found                     = 'Найдено уникальных куков'
            MT_Successfully_Uploaded_In                 = 'Успешно выгружено в'
            MT_Place_ID                                 = 'ID плейса'
            MT_Place_Name                               = 'Название плейса'
            MT_Place_Link                               = 'Ссылка на плейс'
            MT_Gamepasses                               = 'Геймпассы'
            MT_Badges                                   = 'Бейджи'
            MT_Remove_Emojies                           = 'Удалять эмодзи из названия'
            MT_Remove_Round_Brackets                    = 'Удалять (и то, что внутри них) из названия'
            MT_Remove_Square_Brackets                   = 'Удалять [и то, что внутри них] из названия'
            MT_Upload_All_Info_Gamepasses_And_Badges    = 'Выгрузить всю информацию о геймпассах и бейджах из скрипта'
            MT_Enable_Something_To_Start_Checking       = 'Включи что-нибудь, чтобы начать проверку'
            MT_Save_Without_Protocol                    = 'Сохранять без протокола'
            MT_Save_In                                  = 'Сохранять в'
            MT_The_Data_Is_Saved_In                     = 'Данные сохранены в'
            MT_Incorrect_Length_Of_ID_20                = 'Длина ID не может превышать 20 символов'
            MT_Incorrect_Length_Of_Parameter_20         = 'Длина параметра не может превышать 20 цифр'
            MT_Incorrect_Length_Of_Name_50              = 'Длина названия не может превышать 50 символов'
            MT_Incorrect_Length_Of_Config_Name_60       = 'Длина названия конфига не может превышать 60 символов'
            MT_Gamepass_With_This_Name_Already_Exists   = 'Геймпасс с таким именем уже существует'
            MT_Add_A_Gamepass_Name                      = 'Добавить название геймпасса'
            MT_Found_Data_On                            = 'Найденные данные по'
            MT_The_Place_Has_No_Gamepasses              = 'У плейса нет геймпассов'
            MT_The_Place_Has_No_Badges                  = 'У плейса нет бейджей'
            MT_Gamepasses_Parser_From_The_Place         = 'Парсер геймпассов плейса'
            MT_Badges_Parser_From_The_Place             = 'Парсер бейджей плейса'
            MT_Misc                                     = 'Разное'
            MT_Seconds                                  = 'сек'
            MT_Waiting_Time                             = 'Время ожидания'
            MT_Output_Total                             = 'Выводить итоговые данные'
            MT_Found                                    = 'Найдено'
            MT_Lines                                    = 'Строк'
            MT_Start_Parsing                            = 'Запустить парсинг'
            MT_Enter_The_Parameter_Value                = 'Введи значение параметра'
            MT_Enter_The_Waiting_Time                   = 'Введи время в секундах'
            MT_Enter_The_Gamepass_Name                  = 'Введи название геймпасса'
            MT_Enter_The_Place_ID                       = 'Введи ID плейса'
            MT_Enter_The_Bundle_ID                      = 'Введи ID бандла'
            MT_Gamepasses                               = 'Геймпассы'
            MT_Badges                                   = 'Бейджи'
            MT_Fix_Console                              = 'Починить консоль'
            MT_Settings                                 = 'Настройки'
            MT_General                                  = 'Общие'
            MT_Main                                     = 'Основное'
            MT_Places                                   = 'Плейсы'
            MT_Language                                 = 'Язык'
            MT_Configs                                  = 'Конфиги'
            MT_Check                                    = 'Проверять'
            MT_Save                                     = 'Сохранить', 'Сохранять'
            MT_Auto_Save_Changes                        = 'Авто. сохранение изменений'
            MT_Update_List                              = 'Обновить список'
            MT_Back                                     = 'Назад'
            MT_Close_Program                            = 'Закрыть программу'
            MT_Add_Bundle                               = 'Добавить ID бандла'
            MT_Add_ID_Place                             = 'Добавить ID плейса'
            MT_Enter_Something                          = 'Введи что-то'
            MT_Create_Config                            = 'Создать конфиг'
            MT_Cancel                                   = 'Отмена'
            MT_Load_On_Launch                           = 'Загружать при запуске'
            MT_Load                                     = 'Загрузить'
            MT_File_Location                            = 'Расположение файла'
            MT_Rename                                   = 'Переименовать'
            MT_Delete                                   = 'Удалить'
            MT_Enter_Name_For_New_Config                = 'Введи название нового конфига'
            MT_Enter_New_Name_For_Config                = 'Введи новое название конфига'
            MT_Parameter_With_This_Value_Already_Exists = 'Параметр с таким значением уже существует'
            MT_Bundle_With_This_ID_Already_Exists       = 'Бандл с таким ID уже существует'
            MT_Place_With_This_ID_Already_Exists        = 'Плейс с таким ID уже существует'
            MT_Incorrent_Bundle_ID                      = 'Некорректный ID бандла'
            MT_Incorrent_Place_ID                       = 'Некорректный ID плейса'
            MT_Incorrect_File_Name                      = 'Некорректное имя файла'
            MT_File_With_This_Name_Already_Exists       = 'Файл с таким именем уже существует'
            MT_Incorrect_Waiting_Time                   = 'Время ожидания не может быть больше 3600 секунд'
            MT_Incorrect_Value                          = 'Некорректное значение'
            MT_Of                                       = 'из'
            MT_Start_Checking_File                      = 'Проверяем файл'
            MT_Finish_Checking_File                     = 'Проверка завершена'
            MT_Start_Parsing_File                       = 'Парсим файл'
            MT_Finish_Parsing_File                      = 'Парсинг завершён'
            MT_Press_Any_Key_To_Continue                = 'Нажми любую клавишу чтобы продолжить'
            MT_Press_Enter_To_Continue                  = 'Нажми Enter чтобы продолжить'
            MT_Request                                  = 'Запрос'
            MT_Everything_Or_Something_Is_On            = 'всё или что-то включено, всегда'
            MT_Everything_Is_On_Or_Off                  = 'всё включено или выключено, всегда'
            MT_Total                                    = 'В', 'С', 'Е', 'Г', 'О'
            MT_Roblox                                   = 'Роблокс'
            MT_Cookie_Parser                            = 'Куки Парсер'
            MT_Cookie_Checker                           = 'Куки Чекер'
            MT_Cookie_Refresher                         = 'Куки Рефрешер'
            MT_Beta                                     = '[БЕТА]'

### Основные функции

async def lableASCII(start=False):
    # MeowTool + by h1kken :3
    if start: await cls()
    if config['General']['Show_Lable_MeowTool'] or config['General']['Show_Lable_by_h1kken']:
        ASCII_MeowTool = r'''  __    __     ______     ______     __     __     ______     ______     ______     __
 /\ "-./  \   /\  ___\   /\  __ \   /\ \  _ \ \   /\__  _\   /\  __ \   /\  __ \   /\ \
 \ \ \-./\ \  \ \  __\   \ \ \ \ \  \ \ \/ ".\ \  \/_/\ \/   \ \ \ \ \  \ \ \ \ \  \ \ \____
  \ \ \ \ \ \  \ \    ‾\  \ \ ‾‾  \  \ \  /". \ \    \ \ \    \ \ ‾‾  \  \ \ ‾‾  \  \ \     \
   \/‾/  \/‾/   \/‾‾‾‾‾/   \/‾‾‾‾‾/   \/‾/   \/‾/     \/‾/     \/‾‾‾‾‾/   \/‾‾‾‾‾/   \/‾‾‾‾‾/
    ‾‾    ‾‾     ‾‾‾‾‾‾     ‾‾‾‾‾‾     ‾‾     ‾‾       ‾‾       ‾‾‾‾‾‾     ‾‾‾‾‾‾     ‾‾‾‾‾‾'''
        by_h1kken = r''' /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\ by h1kken :3 /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
 ‾‾‾ ‾ ‾‾  ‾‾  ‾‾  ‾‾‾  ‾‾  ‾‾  ‾‾ ‾ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾ ‾‾  ‾‾  ‾‾  ‾‾‾  ‾‾  ‾‾  ‾‾ ‾ ‾‾‾'''
        sys.stdout.write(f'\r{f'{ANSI.FG.PINK + ANSI.DECOR.BOLD + ASCII_MeowTool + ANSI.CLEAR}\n' if config['General']['Show_Lable_MeowTool'] else ''}{f'{'\n' if not config['General']['Show_Lable_MeowTool'] else ''}{ANSI.FG.RED + ANSI.DECOR.BOLD + by_h1kken + ANSI.CLEAR}\n' if config['General']['Show_Lable_by_h1kken'] else ''}')
    else:
        sys.stdout.write('\n')
    sys.stdout.flush()
        
async def cls():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

async def removeLines(amountOfLines: int):
    if amountOfLines:
        sys.stdout.write(f'\033[{amountOfLines}A\033[J')
        sys.stdout.flush()

def removeTwoSpaces(string: str) -> str:
    return ' '.join(string.split()).strip()

def removeBracketsAndIn(string: str, removeRound: bool, removeSquare: bool) -> str:
    newString = ''
    skip = 0
    for char in string:
        if char == '(' and removeRound or char == '[' and removeSquare:
            skip += 1
        elif char in (')', ']') and skip > 0:
            skip -= 1
        elif skip == 0:
            newString += char
    return newString

def removeSpecialCharsAndOrEmojies(string: str, removeSpecialChars: bool, removeEmojies: bool) -> str:
    if removeSpecialChars: string = sub('[^A-Za-z0-9 ]+', '', string)
    if removeEmojies:      string = replace_emoji(string, replace=' ')
    string = removeTwoSpaces(string).strip()
    return string

def amountOfLines(folder: str, file: str) -> str:
    if os.path.exists(f'{folder}\\{file}.txt'):
        lines = open(f'{folder}\\{file}.txt', 'r', encoding='UTF-8').readlines()
        if   len(lines) == 1: return f'({len(lines)} line)'
        elif len(lines)  > 1: return f'({len(lines)} lines)'
    return '(0 lines)'

async def waitingInput():
    sys.stdout.flush()
    if config['General']['Press_Any_Key_To_Continue']:
        getch() 
        sys.stdout.write('\n')
        sys.stdout.flush()
    else:
        input()
    await cls()
    await lableASCII()

async def errorOrCorrectHandler(isError: bool, removeLines_: int, message: str, path=''):
    await removeLines(removeLines_)
    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{path}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n {f'[{ANSI.FG.RED}X{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if isError else f'[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} ┃ {message}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
    await waitingInput()

async def AutoSaveConfig():
    if configLoader['Saver']['Auto_Save_Changes']:
        async with aiofiles.open(f'Settings\\Configs\\{configLoader['Loader']['Current_Config']}.toml', 'w', encoding='UTF-8') as file:
            await file.write(dumps(config))

### Proxy Checker

async def proxyChecker(file: str): # http, https, socks4, socks5
    await removeLines(15)
    sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}{file}.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')
    if not os.path.exists(f'Proxy\\Checker\\{file}.txt'): open(f'Proxy\\Checker\\{file}.txt', 'w')
    proxyList = open(f'Proxy\\Checker\\{file}.txt', 'r', encoding='UTF-8').readlines()
    timeoutProxy = config['Proxy']['Checker']['Timeout']
    proxyCount = 0
    resetProxySocks = socket.socket

    def proxySave(protocol: str, protocolUpper: str, filename: str, validity: str, proxy: str, color, goodbad: str):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{color}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {proxyCount} {MT_Of} {len(proxyList)} ┃ {ANSI.FG.CYAN}[{protocolUpper}] {ANSI.CLEAR + ANSI.DECOR.BOLD + color}[{goodbad}] {proxy + ANSI.CLEAR}')
        with open(f'Proxy\\Checker\\{filename}_{validity}.txt', 'a+', encoding='UTF-8') as file:
            file.seek(0)
            if f'{protocol}{proxy}' not in file.read():
                file.write(f'{protocol}{proxy.replace('\n', '')}\n')

    def unknownProxySave(protocol: str, filename: str, validity: str, proxy: str):
        with open(f'Proxy\\Checker\\{filename}_{validity}.txt', 'a+', encoding='UTF-8') as file:
            file.seek(0)
            if f'{protocol}{proxy}' not in file.read():
                file.write(f'{protocol}{proxy.replace('\n', '')}\n')
        
    for proxy in proxyList:
        if 'http://' in proxy or 'https://' in proxy: # http / https
            proxy = proxy.lower().replace('http://', '').replace('https://', '')
            
            try:
                if len(proxy.split(':')) == 4:
                    ip, port, login, password = proxy.strip().split(':')
                    HTTPproxies = {
                        'http': f'http://{login}:{password}@{ip}:{port}',
                        'https': f'https://{login}:{password}@{ip}:{port}'
                    }
                else:
                    ip, port = proxy.strip().split(':')
                    HTTPproxies = {
                        'http': f'http://{ip}:{port}',
                        'https': f'https://{ip}:{port}'
                    }
                
                response = requests.get('http://ipinfo.io/json', proxies=HTTPproxies, timeout=timeoutProxy)
                
                if response.status_code >= 200 and response.status_code < 300:
                    proxyCount += 1
                    if   config['Proxy']['Checker']['Save_In_Custom_Folder'] and config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',        'H', 'custom', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    elif config['Proxy']['Checker']['Save_In_Custom_Folder']:                                                         proxySave('http://', 'H', 'custom', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    elif config['Proxy']['Checker']['Save_Without_Protocol']:                                                         proxySave('',        'H', 'http',   'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    else:                                                                                                             proxySave('http://', 'H', 'http',   'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                else:
                    proxyCount += 1
                    if config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',        'H', 'http', 'invalid', proxy, ANSI.FG.RED, 'BAD')
                    else:                                                   proxySave('http://', 'H', 'http', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except requests.RequestException:
                proxyCount += 1
                if config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',        'H', 'http', 'invalid', proxy, ANSI.FG.RED, 'BAD')
                else:                                                   proxySave('http://', 'H', 'http', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except Exception:
                pass
        elif 'socks4://' in proxy: # socks4
            proxy = proxy.lower().replace('socks4://', '')
            try:
                if len(proxy.split(':')) == 4:
                    ip, port, login, password = proxy.strip().split(':')
                    socks.set_default_proxy(proxy_type=socks.SOCKS4, addr=ip, port=int(port), username=login, password=password)
                else:
                    ip, port = proxy.strip().split(':')
                    socks.set_default_proxy(proxy_type=socks.SOCKS4, addr=ip, port=int(port))
                socket.socket = socks.socksocket
                response = requests.get('http://ipinfo.io/json', timeout=timeoutProxy)
                if response.status_code >= 200 and response.status_code < 300:
                    proxyCount += 1
                    if   config['Proxy']['Checker']['Save_In_Custom_Folder'] and config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',          'S4', 'custom', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    elif config['Proxy']['Checker']['Save_In_Custom_Folder']:                                                         proxySave('socks4://', 'S4', 'custom', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    elif config['Proxy']['Checker']['Save_Without_Protocol']:                                                         proxySave('',          'S4', 'socks4', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    else:                                                                                                             proxySave('socks4://', 'S4', 'socks4', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                else:
                    proxyCount += 1
                    if config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',          'S4', 'socks4', 'invalid', proxy, ANSI.FG.RED, 'BAD')
                    else:                                                   proxySave('socks4://', 'S4', 'socks4', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except requests.RequestException:
                proxyCount += 1
                if config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',          'S4', 'socks4', 'invalid', proxy, ANSI.FG.RED, 'BAD')
                else:                                                   proxySave('socks4://', 'S4', 'socks4', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except Exception:
                pass
        elif 'socks5://' in proxy: # socks5
            proxy = proxy.lower().replace('socks5://', '')
            try:
                if len(proxy.split(':')) == 4:
                    ip, port, login, password = proxy.strip().split(':')
                    socks.set_default_proxy(proxy_type=socks.SOCKS5, addr=ip, port=int(port), username=login, password=password)
                else:
                    ip, port = proxy.strip().split(':')
                    socks.set_default_proxy(proxy_type=socks.SOCKS5, addr=ip, port=int(port))
                socket.socket = socks.socksocket
                response = requests.get('http://ipinfo.io/json', timeout=timeoutProxy)
                if response.status_code >= 200 and response.status_code < 300:
                    proxyCount += 1
                    if   config['Proxy']['Checker']['Save_In_Custom_Folder'] and config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',          'S5', 'custom', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    elif config['Proxy']['Checker']['Save_In_Custom_Folder']:                                                         proxySave('socks5://', 'S5', 'custom', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    elif config['Proxy']['Checker']['Save_Without_Protocol']:                                                         proxySave('',          'S5', 'socks5', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                    else:                                                                                                             proxySave('socks5://', 'S5', 'socks5', 'valid', proxy, ANSI.FG.GREEN, 'GOOD')
                else:
                    proxyCount += 1
                    if config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',          'S5', 'socks5', 'invalid', proxy, ANSI.FG.RED, 'BAD')
                    else:                                                   proxySave('socks5://', 'S5', 'socks5', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except requests.RequestException:
                proxyCount += 1
                if config['Proxy']['Checker']['Save_Without_Protocol']: proxySave('',          'S5', 'socks5', 'invalid', proxy, ANSI.FG.RED, 'BAD')
                else:                                                   proxySave('socks5://', 'S5', 'socks5', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except Exception:
                pass
        else:
            try:
                list_types = []

                try: # http / https
                    if len(proxy.split(':')) == 4:
                        ip, port, login, password = proxy.strip().split(':')
                        HTTPproxies = {
                            'http': f'http://{login}:{password}@{ip}:{port}',
                            'https': f'https://{login}:{password}@{ip}:{port}'
                        }
                    else:
                        ip, port = proxy.strip().split(':')
                        HTTPproxies = {
                            'http': f'http://{ip}:{port}',
                            'https': f'https://{ip}:{port}'
                        }

                    response = requests.get('http://ipinfo.io/json', proxies=HTTPproxies, timeout=timeoutProxy)
                    if response.status_code >= 200 and response.status_code < 300:
                        list_types.append('H')
                except Exception:
                    pass

                try: # socks4
                    if len(proxy.split(':')) == 4:
                        ip, port, login, password = proxy.strip().split(':')
                        socks.set_default_proxy(proxy_type=socks.SOCKS4, addr=ip, port=int(port), username=login, password=password)
                    else:
                        ip, port = proxy.strip().split(':')
                        socks.set_default_proxy(proxy_type=socks.SOCKS4, addr=ip, port=int(port))
                    socket.socket = socks.socksocket
                    response = requests.get('http://ipinfo.io/json', timeout=timeoutProxy)
                    if response.status_code >= 200 and response.status_code < 300:
                        list_types.append('S4')
                    socket.socket = resetProxySocks
                except Exception:
                    pass

                try: # socks5
                    if len(proxy.split(':')) == 4:
                        ip, port, login, password = proxy.strip().split(':')
                        socks.set_default_proxy(proxy_type=socks.SOCKS5, addr=ip, port=int(port), username=login, password=password)
                    else:
                        ip, port = proxy.strip().split(':')
                        socks.set_default_proxy(proxy_type=socks.SOCKS5, addr=ip, port=int(port))
                    socket.socket = socks.socksocket
                    response = requests.get('http://ipinfo.io/json', timeout=timeoutProxy)
                    if response.status_code >= 200 and response.status_code < 300:
                        list_types.append('S5')
                    socket.socket = resetProxySocks
                except Exception:
                    pass

                if len(list_types) > 0:
                    proxyCount += 1
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {str(proxyCount)} {MT_Of} {len(proxyList)} ┃ {ANSI.FG.CYAN}[{'/'.join(list_types)}] {ANSI.CLEAR + ANSI.DECOR.BOLD + ANSI.FG.GREEN}[GOOD] {proxy}{ANSI.CLEAR}')
                    if 'H' in list_types:
                        if   config['Proxy']['Checker']['Save_In_Custom_Folder'] and config['Proxy']['Checker']['Save_Without_Protocol']: unknownProxySave('',          'custom', 'valid', proxy)
                        elif config['Proxy']['Checker']['Save_In_Custom_Folder']:                                                         unknownProxySave('http://',   'custom', 'valid', proxy)
                        elif config['Proxy']['Checker']['Save_Without_Protocol']:                                                         unknownProxySave('',          'http',   'valid', proxy)
                        else:                                                                                                             unknownProxySave('http://',   'http',   'valid', proxy)
                    if 'S4' in list_types:
                        if   config['Proxy']['Checker']['Save_In_Custom_Folder'] and config['Proxy']['Checker']['Save_Without_Protocol']: unknownProxySave('',          'custom', 'valid', proxy)
                        elif config['Proxy']['Checker']['Save_In_Custom_Folder']:                                                         unknownProxySave('socks4://', 'custom', 'valid', proxy)
                        elif config['Proxy']['Checker']['Save_Without_Protocol']:                                                         unknownProxySave('',          'socks4', 'valid', proxy)
                        else:                                                                                                             unknownProxySave('socks4://', 'socks4', 'valid', proxy)
                    if 'S5' in list_types:
                        if   config['Proxy']['Checker']['Save_In_Custom_Folder'] and config['Proxy']['Checker']['Save_Without_Protocol']: unknownProxySave('',          'custom', 'valid', proxy)
                        elif config['Proxy']['Checker']['Save_In_Custom_Folder']:                                                         unknownProxySave('socks5://', 'custom', 'valid', proxy)
                        elif config['Proxy']['Checker']['Save_Without_Protocol']:                                                         unknownProxySave('',          'socks5', 'valid', proxy)
                        else:                                                                                                             unknownProxySave('socks5://', 'socks5', 'valid', proxy)
                elif len(list_types) == 0:
                    proxyCount += 1
                    proxySave('', 'UNK', 'unknown', 'invalid', proxy, ANSI.FG.RED, 'BAD')
            except requests.RequestException:
                proxyCount += 1
                proxySave('', 'UNK', 'unknown', 'invalid', proxy, ANSI.FG.RED, 'BAD')
        socket.socket = resetProxySocks

    # Выравнивание после проверки
    if len(proxyList) > 0 and proxyList[-1] != '\n' and proxyList[-1] != '' and proxyList[-1] != ' ':
        os.makedirs('Proxy\\Checker\\cached', exist_ok=True)
        copyfile(f'Proxy\\Checker\\{file}.txt', f'Proxy\\Checker\\cached\\{file}_cached.txt')
        while proxyList[-1] != '\n' and proxyList[-1] != '' and proxyList[-1] != ' ':
            open(f'Proxy\\Checker\\cached\\{file}_cached.txt', 'a').write('\n')
            sys.stdout.write('\n')
            proxyList = open(f'Proxy\\Checker\\cached\\{file}_cached.txt', 'r').readlines()
        if os.path.exists('Proxy\\Checker\\cached'): rmtree('Proxy\\Checker\\cached')
        await removeLines(1)

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Finish_Checking_File}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
    await waitingInput()

### Roblox Cookie Parser

COOKIE_PATTERN = compile(r'_\|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.\|_[^?=\s|$\r\n]+')

async def robloxCookieParser():
    fileName = str(config['Roblox']['CookieParser']['Save_To_A_File'])
    if any(char in fileName for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']) or fileName.strip() == '':
        fileName = 'outputs'

    await removeLines(6)
    lengthOfCookies = 0
    files = [file for file in os.listdir('Roblox\\Cookie Parser')
             if file.endswith('.txt')]

    for file in files:
        lengthOfCookies += len(open(f'Roblox\\Cookie Parser\\{file}', 'r', encoding='UTF-8').readlines())
    
    countParserUniqueCookies     = 0
    countParserDuplicatedCookies = 0
    countParserIncorrectCookies  = 0

    dateOfCookieParsing = datetime.datetime.now().strftime('%d.%m.%Y - %H.%M.%S')
    os.makedirs(f'Roblox\\Cookie Parser\\outputs\\{dateOfCookieParsing}', exist_ok=True)

    for file in files:
        counterOfCookies = 0
        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Parsing_File} \'{ANSI.DECOR.UNDERLINE1}{file}{ANSI.CLEAR}\': 0 {MT_Of} {len(open(f'Roblox\\Cookie Parser\\{file}', 'r', encoding='UTF-8').readlines())}')
        outputFile = open(f'Roblox\\Cookie Parser\\outputs\\{dateOfCookieParsing}\\{fileName}.txt', 'a+', encoding='UTF-8')
        for line in open(f'Roblox\\Cookie Parser\\{file}', 'r', encoding='UTF-8').readlines():
            cookie = search(COOKIE_PATTERN, line)
            try:
                outputFile.seek(0)
                if cookie.group(0) not in outputFile.read():
                    outputFile.write(cookie.group(0) + '\n')
                    countParserUniqueCookies += 1
                else:
                    countParserDuplicatedCookies += 1
            except AttributeError:
                countParserIncorrectCookies += 1
            counterOfCookies += 1
            sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Parsing_File} \'{ANSI.DECOR.UNDERLINE1}{file}{ANSI.CLEAR + ANSI.DECOR.BOLD}\': {counterOfCookies} {MT_Of} {len(open(f'Roblox\\Cookie Parser\\{file}', 'r', encoding='UTF-8').readlines())}')
    
    sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Finish_Parsing_File}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Unique_Cookies_Found}: {countParserUniqueCookies}\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Duplicated_Cookies_Removed}: {countParserDuplicatedCookies}\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Incorrect_Cookies_Removed}: {countParserIncorrectCookies}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
    await waitingInput()

### Roblox Cookie Checker

#       [Var Name]             = [Lable Name],             [ID],      [Name In Config]

class AUniversalTime: # https://www.roblox.com/games/5130598377
    placeNames = 'A Universal Time', 'A_Universal_Time', 'AUT', 5130598377
    class Gamepasses:
        Plus3StandStorageSlots = '3+ Stand Storage Slots', 10397197,  '3_Plus_Stand_Storage_Slots'
        Plus3BankSlotsStorage  = '3+ Bank Slots Storage',  10479192,  '3_Plus_Bank_Slots_Storage'
        ItemNotifier           = 'Item Notifier',          10562035,  'Item_Notifier'
        Donation               = 'Donation',               10753254,  'Donation'
        CustomChatColor        = 'Custom Chat Color',      11491183,  'Custom_Chat_Color'
        ChatBackgroundColor    = 'Chat Background Color',  11581293,  'Chat_Background_Color'
        EmotesPackv1           = 'Emotes Pack v1',         13675608,  'Emotes_Pack_v1'
        EmotePackv2            = 'Emote Pack v2',          14014491,  'Emote_Pack_v2'
        EmotePackv3            = 'Emote Pack v3',          822694616, 'Emote_Pack_v3'
        EmotePackv4            = 'Emote Pack v4',          822666635, 'Emote_Pack_v4'
        EmotePackv5            = 'Emote Pack v5',          837754540, 'Emote_Pack_v5'
        JJKEmotePack           = 'JJK Emote Pack',         920471052, 'JJK_Emote_Pack'
        SmartAssistant         = 'Smart Assistant',        939773206, 'Smart_Assistant'
        CommunityEmotePack     = 'Community Emote Pack',   948648926, 'Community_Emote_Pack'
        # List Of Gamepasses
        listOfGamepasses = [Plus3StandStorageSlots, Plus3BankSlotsStorage, ItemNotifier, Donation, CustomChatColor, ChatBackgroundColor, EmotesPackv1, EmotePackv2, EmotePackv3, EmotePackv4, EmotePackv5, JJKEmotePack, SmartAssistant, CommunityEmotePack]
    class Badges:
        AUTWinterXMas = 'AUT Winter/X-Mas', 2124647551,       'AUT_Winter_XMas'
        NewUniverse   = 'New Universe',     2124749486,       'New_Universe'
        AHauntingTime = 'A Haunting Time',  3072215579952874, 'A_Haunting_Time'
        AJollyTime    = 'A Jolly Time',     500904421623568,  'A_Jolly_Time'
        # List Of Badges
        listOfBadges = [AUTWinterXMas, NewUniverse, AHauntingTime, AJollyTime]

class AdoptMe: # https://www.roblox.com/games/920587237
    placeNames = 'Adopt Me', 'Adopt_Me', 'AM', 920587237
    class Gamepasses:
        VIP                     = 'VIP',                        3196348,   'VIP'
        Glider                  = 'Glider',                     3745845,   'Glider'
        StarterPack             = 'Starter Pack',               4785795,   'Starter_Pack'
        DJ                      = 'DJ',                         4796463,   'DJ'
        CandyCannon             = 'Candy Cannon',               5246776,   'Candy_Cannon'
        PremiumPlots            = 'Premium Plots',              5300198,   'Premium_Plots'
        PremiumFaces            = 'Premium Faces',              5704158,   'Premium_Faces'
        SupercarPack            = 'Supercar Pack',              5785139,   'Supercar_Pack'
        HeartHoverboard         = 'Heart Hoverboard',           5885873,   'Heart_Hoverboard'
        RoyalCarriages          = 'Royal Carriages',            5904007,   'Royal_Carriages'
        MillionairePack         = 'Millionaire Pack',           6040696,   'Millionaire_Pack'
        MermaidMansion          = 'Mermaid Mansion',            6164327,   'Mermaid_Mansion'
        CelebrityMansion        = 'Celebrity Mansion',          6408694,   'Celebrity_Mansion'
        PetHorse                = 'Pet Horse',                  6558811,   'Pet_Horse'
        PetGriffin              = 'Pet Griffin',                6558813,   'Pet_Griffin'
        LemonadeStand           = 'Lemonade Stand',             6858591,   'Lemonade_Stand'
        HotdogStand             = 'Hotdog Stand',               7124470,   'Hotdog_Stand'
        ModernMansion           = 'Modern Mansion',             6965379,   'Modern_Mansion'
        CozyHomeLure            = 'Cozy Home Lure',             189425850, 'Cozy_Home_Lure'
        SchoolandHospitalHomes  = 'School and Hospital Homes',  951065968, 'Schooland_Hospital_Homes'
        SoccerStadium           = 'Soccer Stadium',             951395729, 'Soccer_Stadium'
        FossilIsleReturnsBundle = 'Fossil Isle Returns Bundle', 951441773, 'Fossil_Isle_Returns_Bundle'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Glider, StarterPack, DJ, CandyCannon, PremiumPlots, PremiumFaces, SupercarPack, HeartHoverboard, RoyalCarriages, MillionairePack, MermaidMansion, CelebrityMansion, PetHorse, PetGriffin, LemonadeStand, HotdogStand, ModernMansion, CozyHomeLure, SchoolandHospitalHomes, SoccerStadium, FossilIsleReturnsBundle]
    class Badges:
        TinyIsles                   = 'Tiny Isles',                            2124439922,       'Tiny_Isles'
        AncientRuins                = 'Ancient Ruins',                         2124439923,       'Ancient_Ruins'
        CoastalClimb                = 'Coastal Climb',                         2124439924,       'Coastal_Climb'
        LonelyPeak                  = 'Lonely Peak',                           2124439925,       'Lonely_Peak'
        Miniworld                   = 'Miniworld',                             2124439926,       'Miniworld'
        Pyramid                     = 'Pyramid',                               2124439927,       'Pyramid'
        ShipwreckBay                = 'Shipwreck Bay',                         2124439928,       'Shipwreck_Bay'
        RobloxEggHunt2020           = 'Roblox Egg Hunt 2020',                  2124520917,       'Roblox_Egg_Hunt_2020'
        RBBattlesChallenge          = 'RB Battles Challenge',                  2129488028,       'RB_Battles_Challenge'
        Unnamed                     = '???',                                   2129488030,       'Unnamed'
        Garden                      = 'Garden',                                135520552767917,  'Garden'
        RobloxTheGamesAdoptMeQuest1 = 'Roblox The Games: Adopt Me! - Quest 1', 1048893619880427, 'Roblox_The_Games_Adopt_Me_Quest_1'
        RobloxTheGamesAdoptMeQuest2 = 'Roblox The Games: Adopt Me! - Quest 2', 763171671267524,  'Roblox_The_Games_Adopt_Me_Quest_2'
        RobloxTheGamesAdoptMeQuest3 = 'Roblox The Games: Adopt Me! - Quest 3', 925260774262149,  'Roblox_The_Games_Adopt_Me_Quest_3'
        RobloxTheGamesAdoptMeShine1 = 'Roblox The Games: Adopt Me! - Shine 1', 89650026776535,   'Roblox_The_Games_Adopt_Me_Shine_1'
        RobloxTheGamesAdoptMeShine2 = 'Roblox The Games: Adopt Me! - Shine 2', 292596439745713,  'Roblox_The_Games_Adopt_Me_Shine_2'
        RobloxTheGamesAdoptMeShine3 = 'Roblox The Games: Adopt Me! - Shine 3', 1683279614525471, 'Roblox_The_Games_Adopt_Me_Shine_3'
        RobloxTheGamesAdoptMeShine4 = 'Roblox The Games: Adopt Me! - Shine 4', 1065569517641022, 'Roblox_The_Games_Adopt_Me_Shine_4'
        RobloxTheGamesAdoptMeShine5 = 'Roblox The Games: Adopt Me! - Shine 5', 3865916040798951, 'Roblox_The_Games_Adopt_Me_Shine_5'
        HunterBadge                 = 'Hunter Badge',                          160677344563654,  'Hunter_Badge'
        WhereBearBadge              = 'Where Bear? Badge',                     211728180632535,  'Where_Bear_Badge'
        SurvivorBadge               = 'Survivor Badge',                        639601989428398,  'Survivor_Badge'
        # List Of Badges
        listOfBadges = [TinyIsles, AncientRuins, CoastalClimb, LonelyPeak, Miniworld, Pyramid, ShipwreckBay, RobloxEggHunt2020, RBBattlesChallenge, Unnamed, Garden, RobloxTheGamesAdoptMeQuest1, RobloxTheGamesAdoptMeQuest2, RobloxTheGamesAdoptMeQuest3, RobloxTheGamesAdoptMeShine1, RobloxTheGamesAdoptMeShine2, RobloxTheGamesAdoptMeShine3, RobloxTheGamesAdoptMeShine4, RobloxTheGamesAdoptMeShine5, HunterBadge, WhereBearBadge, SurvivorBadge]

class AnimeAdventures: # https://www.roblox.com/games/8304191830
    placeNames = 'Anime Adventures', 'Anime_Adventures', 'AA', 8304191830
    class Gamepasses:
        VIP             = 'VIP',               55372677, 'VIP'
        ShinyHunter     = 'Shiny Hunter',      55373046, 'Shiny_Hunter'
        UnitStorage     = 'Unit Storage',      55373124, 'Unit_Storage'
        Display3Units   = 'Display 3 Units',   55373224, 'Display_3_Units'
        DisplayAllUnits = 'Display All Units', 99127218, 'Display_All_Units'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, UnitStorage, Display3Units, DisplayAllUnits]

class AnimeDefenders: # https://www.roblox.com/games/17017769292
    placeNames = 'Anime Defenders', 'Anime_Defenders', 'AD', 17017769292
    class Gamepasses:
        VIP                    = 'VIP',                      812679198,  'VIP'
        ShinyHunter            = 'Shiny Hunter',             812891077,  'Shiny_Hunter'
        MoreBoothSpace         = 'More Booth Space',         812985318,  'More_Booth_Space'
        DivineDragonBattlepass = 'Divine Dragon Battlepass', 857122763,  'Divine_Dragon_Battlepass'
        AthenyxsBattlepass     = 'Athenyx\'s Battlepass',    895533720,  'Athenyxs_Battlepass'
        x3Speed                = '3x Speed',                 903541948,  '3x_Speed'
        x50Unboxing            = '50x Unboxing',             903895415,  '50x_Unboxing'
        ChristmasBattlepass    = 'Christmas Battlepass',     1004747738, 'Christmas_Battlepass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, MoreBoothSpace, DivineDragonBattlepass, AthenyxsBattlepass, x3Speed, x50Unboxing, ChristmasBattlepass]

class AnimeVanguards: # https://www.roblox.com/games/16146832113
    placeNames = 'Anime Vanguards', 'Anime_Vanguards', 'AV', 16146832113
    class Gamepasses:
        AnimeVanguardsTester = 'Anime Vanguards Tester', 780911708, 'Anime_Vanguards_Tester'
        ExtraUnitStorage     = 'Extra Unit Storage',     842367966, 'Extra_Unit_Storage'
        VIP                  = 'VIP',                    843295206, 'VIP'
        ShinyHunter          = 'Shiny Hunter',           846032291, 'Shiny_Hunter'
        DisplayAllUnits      = 'Display All Units',      846695813, 'Display_All_Units'
        # List Of Gamepasses
        listOfGamepasses = [AnimeVanguardsTester, ExtraUnitStorage, VIP, ShinyHunter, DisplayAllUnits]


class BeeSwarmSimulator: # https://www.roblox.com/games/1537690962
    placeNames = 'Bee Swarm Simulator', 'Bee_Swarm_Simulator', 'BSS', 1537690962
    class Gamepasses:
        x2ConvertSpeed    = 'x2 Convert Speed',     4231119, 'x2_Convert_Speed'
        x2BeeGatherPollen = 'x2 Bee Gather Pollen', 4231126, 'x2_BeeGather_Pollen'
        BearBee           = 'Bear Bee',             4257788, 'Bear_Bee'
        x2TicketChance    = 'x2 Ticket Chance',     4492467, 'x2_Ticket_Chance'
        # List Of Gamepasses
        listOfGamepasses = [x2ConvertSpeed, x2BeeGatherPollen, BearBee, x2TicketChance]
    class Badges:
        YouPlayedBeeSwarmSimulator = 'You Played Bee Swarm Simulator!', 2124634293, 'You_Played_Bee_Swarm_Simulator'
        SwarmingEggOfTheHive       = 'Swarming Egg Of The Hive',        2124520746, 'Swarming_Egg_Of_The_Hive'
        BeesmasBeeliever           = 'Beesmas Beeliever',               2124445684, 'Beesmas_Beeliever'
        BeesmasOverachiever        = 'Beesmas Overachiever',            2124445842, 'Beesmas_Overachiever'
        EggHunt2019                = 'Egg Hunt 2019',                   2124458125, 'Egg_Hunt_2019'
        Million1Honey              = '1 Million Honey',                 1749468648, '1_Million_Honey'
        Million10Honey             = '10 Million Honey',                1749519033, '10_Million_Honey'
        Million100Honey            = '100 Million Honey',               1749523673, '100_Million_Honey'
        Billion1Honey              = '1 Billion Honey',                 1749534539, '1_Billion_Honey'
        Billion20Honey             = '20 Billion Honey',                2124426329, '20_Billion_Honey'
        Thousand500Goo             = '500 Thousand Goo',                1874484250, '500_Thousand_Goo'
        Million5Goo                = '5 Million Goo',                   1874485358, '5_Million_Goo'
        Million50Goo               = '50 Million Goo',                  1874486035, '50_Million_Goo'
        Million500Goo              = '500 Million Goo',                 1874487127, '500_Million_Goo'
        Billion10Goo               = '10 Billion Goo',                  2124426332, '10_Billion_Goo'
        Battle100Points            = '100 Battle Points',               1749564142, '100_Battle_Points'
        Thousand1BattlePoints      = '1 Thousand Battle Points',        1749566481, '1_Thousand_Battle_Points'
        Thousand10BattlePoints     = '10 Thousand Battle Points',       1749568562, '10_Thousand_Battle_Points'
        Thousand50BattlePoints     = '50 Thousand Battle Points',       1749570424, '50_Thousand_Battle_Points'
        Million1BattlePoints       = '1 Million Battle Points',         2124426330, '1_Million_Battle_Points'
        Ability2500Tokens          = '2500 Ability Tokens',             1874442964, '2500_Ability_Tokens'
        Thousand25AbilityTokens    = '25 Thousand Ability Tokens',      1874445609, '25_Thousand_AbilityTokens'
        Thousand100AbilityTokens   = '100 Thousand Ability Tokens',     1874446720, '100_Thousand_AbilityTokens'
        Million1AbilityTokens      = '1 Million Ability Tokens',        1874447816, '1_Million_Ability_Tokens'
        Million10AbilityTokens     = '10 Million Ability Tokens',       2124426331, '10_Million_Ability_Tokens'
        # List Of Badges
        listOfBadges = [YouPlayedBeeSwarmSimulator, SwarmingEggOfTheHive, BeesmasBeeliever, BeesmasOverachiever, EggHunt2019, Million1Honey, Million10Honey, Million100Honey, Billion1Honey, Billion20Honey, Thousand500Goo, Million5Goo, Million50Goo, Million500Goo, Billion10Goo, Battle100Points, Thousand1BattlePoints, Thousand10BattlePoints, Thousand50BattlePoints, Million1BattlePoints, Ability2500Tokens, Thousand25AbilityTokens, Thousand100AbilityTokens, Million1AbilityTokens, Million10AbilityTokens]

class BladeBall: # https://www.roblox.com/games/13772394625
    placeNames = 'Blade Ball', 'Blade_Ball', 'BB', 13772394625
    class Gamepasses:
        VIP         = 'VIP',          223367086, 'VIP'
        DoubleCoins = 'Double Coins', 226785981, 'Double_Coins'
        InstantSpin = 'Instant Spin', 229765926, 'Instant_Spin'
        TradingSign = 'Trading Sign', 895596060, 'Trading_Sign'
        # List Of Gamepasses
        listOfGamepasses = [VIP, DoubleCoins, InstantSpin, TradingSign]

class BloxFruits: # https://www.roblox.com/games/2753915549
    placeNames = 'Blox Fruits', 'Blox_Fruits', 'BF', 2753915549
    class Gamepasses:
        x2Money       = '2x Money',       6028662, '2x_Money'
        DarkBlade     = 'Dark Blade',     6028786, 'Dark_Blade'
        x2Mastery     = '2x Mastery',     6240746, '2x_Mastery'
        FastBoats     = 'Fast Boats',     6525589, 'Fast_Boats'
        FruitNotifier = 'Fruit Notifier', 6738811, 'Fruit_Notifier'
        x2BossDrops   = '2x Boss Drops',  7578721, '2x_Boss_Drops'
        # List Of Gamepasses
        listOfGamepasses = [x2Money, DarkBlade, x2Mastery, FastBoats, FruitNotifier, x2BossDrops]
    class Badges:
        SecondSea     = 'Second Sea', 2125253106, 'Second_Sea'
        ThirdSea      = 'Third Sea',  2125253113, 'Third_Sea'
        # List Of Badges
        listOfBadges = [SecondSea, ThirdSea]

class BlueLockRivals: # https://www.roblox.com/games/18668065416
    placeNames = 'Blue Lock: Rivals', 'Blue_Lock_Rivals', 'BLR', 18668065416
    class Gamepasses:
        VIP                = 'VIP',                 952453152,  'VIP'
        AnimeEmotes        = 'Anime Emotes',        957906237,  'Anime_Emotes'
        ToxicEmotes        = 'Toxic Emotes',        958185291,  'Toxic_Emotes'
        SkipSpins          = 'Skip Spins',          965195377,  'Skip_Spins'
        AwakeningOutfits   = 'Awakening Outfits',   1034038790, 'Awakening_Outfits'
        GoalSound          = 'Goal Sound',          1045871823, 'Goal_Sound'
        AnkleBreakerSound  = 'Ankle Breaker Sound', 1046171023, 'Ankle_Breaker_Sound'
        PrivacyServersPlus = 'Privacy Servers+',    1054209537, 'Privacy_Servers_Plus'
        # List Of Gamepasses
        listOfGamepasses = [VIP, AnimeEmotes, ToxicEmotes, SkipSpins, AwakeningOutfits, GoalSound, AnkleBreakerSound, PrivacyServersPlus]

class CreaturesofSonaria: # https://www.roblox.com/games/5233782396
    placeNames = 'Creatures of Sonaria', 'Creatures_of_Sonaria', 'CoS', 5233782396
    class Gamepasses:
        CorvuraxSpecies = 'Corvurax Species', 216724088, 'Corvurax_Species'
        # List Of Gamepasses
        listOfGamepasses = [CorvuraxSpecies]
    class Badges:
        BetaTester                      = 'Beta Tester',                       2124595590,       'Beta_Tester'
        BetaSupporter                   = 'Beta Supporter',                    2124595592,       'Beta_Supporter'
        Halloween2022                   = 'Halloween 2022',                    2129022315,       'Halloween_2022'
        Halloween2023                   = 'Halloween 2023',                    2153215846,       'Halloween_2023'
        Halloween2024                   = 'Halloween 2024',                    4462319084474111, 'Halloween_2024'
        ChristmasBadge                  = 'Christmas Badge',                   2124660417,       'Christmas_Badge'
        Christmas2022                   = 'Christmas 2022',                    2129936623,       'Christmas_2022'
        Valentines                      = 'Valentines',                        2124686302,       'Valentines'
        Valentines2023                  = 'Valentines 2023',                   2140726547,       'Valentines_2023'
        Valentines2024                  = 'Valentines 2024',                   55658403086320,   'Valentines_2024'
        Easter2023                      = 'Easter 2023',                       2143625119,       'Easter_2023'
        Easter2024                      = 'Easter 2024',                       1734098717984624, 'Easter_2024'
        LandSeaSky2023                  = 'Land Sea Sky 2023',                 2145610041,       'Land_Sea_Sky_2023'
        LandSeaSky2024                  = 'Land Sea Sky 2024',                 2960167874826659, 'Land_Sea_Sky_2024'
        SummerParadise2023              = 'Summer Paradise 2023',              2149100257,       'Summer_Paradise_2023'
        SummerParadise2024              = 'Summer Paradise 2024',              1654242147814853, 'Summer_Paradise_2024'
        Winter2023                      = 'Winter 2023',                       2661459542444321, 'Winter_2023'
        Winter2024                      = 'Winter 2024',                       2998142934210494, 'Winter_2024'
        SpringMeadows2024               = 'Spring Meadows 2024',               1040006371199126, 'Spring_Meadows_2024'
        Disaster2024                    = 'Disaster 2024',                     1888520945881505, 'Disaster_2024'
        Lore2024                        = 'Lore 2024',                         4346068251661631, 'Lore_2024'
        Harvest2024                     = 'Harvest 2024',                      1596996370838262, 'Harvest_2024'
        Amazon2024                      = 'Amazon 2024',                       2291949305789809, 'Amazon_2024'
        July4th2023                     = 'July 4th 2023',                     2148143991,       'July_4th_2023'
        Firework2024                    = 'Firework 2024',                     2566270751122609, 'Firework_2024'
        TwentyOnePilotsEvent            = 'Twenty One Pilots Event',           2124810991,       'Twenty_One_Pilots_Event'
        RecodeEarlyAccess               = 'Recode Early Access',               2147582505,       'Recode_Early_Access'
        RecodeSupporterTitleAndCreature = 'Recode Supporter Title & Creature', 2147584013,       'Recode_Supporter_Title_And_Creature'
        TwinAtlasWinterClash            = 'Twin Atlas Winter Clash',           1964648519335747, 'Twin_Atlas_Winter_Clash'
        # List Of Badges
        listOfBadges = [BetaTester, BetaSupporter, Halloween2022, Halloween2023, Halloween2024, ChristmasBadge, Christmas2022, Valentines, Valentines2023, Valentines2024, Easter2023, Easter2024, LandSeaSky2023, LandSeaSky2024, SummerParadise2023, SummerParadise2024, Winter2023, Winter2024, SpringMeadows2024, Disaster2024, Lore2024, Harvest2024, Amazon2024, July4th2023, Firework2024, TwentyOnePilotsEvent, RecodeEarlyAccess, RecodeSupporterTitleAndCreature, TwinAtlasWinterClash]

class DaHood: # https://www.roblox.com/games/2788229376
    placeNames = 'Da Hood', 'Da_Hood', 'DH', 2788229376
    class Gamepasses:
        AnonymousCalls        = 'Anonymous Calls',   6072006,   'Anonymous_Calls'
        CustomRingtone        = 'Custom Ringtone',   6080836,   'Custom_Ringtone'
        Boombox               = 'Boombox',           6207330,   'Boombox'
        Knife                 = 'Knife',             6217663,   'Knife'
        Bat                   = 'Bat',               6407926,   'Bat'
        AnimationPack         = 'Animation Pack',    6412475,   'Animation_Pack'
        Flashlight            = 'Flashlight',        6673363,   'Flashlight'
        Shovel                = 'Shovel',            6813576,   'Shovel'
        PepperSpray           = 'Pepper Spray',      6966816,   'Pepper_Spray'
        HouseLimitBoost       = 'House Limit Boost', 7130657,   'House_Limit_Boost'
        Mask                  = 'Mask',              103232594, 'Mask'
        CustomCursor          = 'Custom Cursor',     106911810, 'Custom_Cursor'
        AnimationPackPlusPlus = 'Animation Pack++',  106912041, 'Animation_PackPlusPlus'
        HairGlue              = 'Hair Glue',         916795141, 'Hair_Glue'
        # List Of Gamepasses
        listOfGamepasses = [AnonymousCalls, CustomRingtone, Boombox, Knife, Bat, AnimationPack, Flashlight, Shovel, PepperSpray, HouseLimitBoost, Mask, CustomCursor, AnimationPackPlusPlus, HairGlue]

class DragonAdventures: # https://www.roblox.com/games/3475397644
    placeNames = 'Dragon Adventures', 'Dragon_Adventures', 'DA', 3475397644
    class Gamepasses:
        VIP              = 'VIP',               7010034,  'VIP'
        AdvancedBuilding = 'Advanced Building', 7578781,  'Advanced_Building'
        LuckyEgg         = 'Lucky Egg',         8510023,  'Lucky_Egg'
        ResourceHog      = 'Resource Hog',      8510024,  'Resource_Hog'
        BigBackpack      = 'Big Backpack',      8510025,  'Big_Backpack'
        LuckyTrainer     = 'Lucky Trainer',     8510026,  'Lucky_Trainer'
        MultiRiding      = 'Multi-Riding',      9802010,  'Multi_Riding'
        LuckyTailor      = 'Lucky Tailor',      10999031, 'Lucky_Tailor'
        MultiAccessory   = 'Multi-Accessory',   12000312, 'Multi_Accessory'
        # List Of Gamepasses
        listOfGamepasses = [VIP, AdvancedBuilding, LuckyEgg, ResourceHog, BigBackpack, LuckyTrainer, MultiRiding, LuckyTailor, MultiAccessory]
    class Badges:
        MetaDeveloper  = 'Met a Developer!', 2124634392,       'Met_a_Developer'
        Christmas2022  = 'Christmas 2022',   2129850167,       'Christmas_2022'
        Winter2019     = 'Winter 2019',      2124564089,       'Winter_2019'
        Winter2021     = 'Winter 2021',      2124879418,       'Winter_2021'
        Winter2023     = 'Winter 2023',      1724546607470910, 'Winter_2023'
        Winter2024     = 'Winter 2024',      1680929594185010, 'Winter_2024'
        Valentines2020 = 'Valentines 2020',  2124564091,       'Valentines_2020'
        Valentines2022 = 'Valentines 2022',  2124928448,       'Valentines_2022'
        Valentines2023 = 'Valentines 2023',  2140856200,       'Valentines_2023'
        Valentines2024 = 'Valentines 2024',  2897784583321876, 'Valentines_2024'
        Halloween2019  = 'Halloween 2019',   2124564088,       'Halloween_2019'
        Halloween2020  = 'Halloween 2020',   2124622292,       'Halloween_2020'
        Halloween2021  = 'Halloween 2021',   2124843641,       'Halloween_2021'
        Halloween2022  = 'Halloween 2022',   2129053839,       'Halloween_2022'
        Halloween2023  = 'Halloween 2023',   2153596435,       'Halloween_2023'
        Halloween2024  = 'Halloween 2024',   778861698160847,  'Halloween_2024'
        Easter2020     = 'Easter 2020',      2124564092,       'Easter_2020'
        Easter2021     = 'Easter 2021',      2124706777,       'Easter_2021'
        Easter2022     = 'Easter 2022',      2125832921,       'Easter_2022'
        Easter2023     = 'Easter 2023',      2143031781,       'Easter_2023'
        Easter2024     = 'Easter 2024',      3467626479412502, 'Easter_2024'
        Solstice2020   = 'Solstice 2020',    2124564093,       'Solstice_2020'
        Solstice2021   = 'Solstice 2021',    2124583228,       'Solstice_2021'
        Solstice2022   = 'Solstice 2022',    2128140324,       'Solstice_2022'
        Solstice2023   = 'Solstice 2023',    2150313169,       'Solstice_2023'
        Solstice2024   = 'Solstice 2024',    1575651999109337, 'Solstice_2024'
        Galaxy2022     = 'Galaxy 2022',      2126825175,       'Galaxy_2022'
        Galaxy2023     = 'Galaxy 2023',      2147481065,       'Galaxy_2023'
        Galaxy2024     = 'Galaxy 2024',      2412831398413312, 'Galaxy_2024'
        # List Of Badges
        listOfBadges = [MetaDeveloper, Christmas2022, Winter2019, Winter2021, Winter2023, Winter2024, Valentines2020, Valentines2022, Valentines2023, Valentines2024, Halloween2019, Halloween2020, Halloween2021, Halloween2022, Halloween2023, Halloween2024, Easter2020, Easter2021, Easter2022, Easter2023, Easter2024, Solstice2020, Solstice2021, Solstice2022, Solstice2023, Solstice2024, Galaxy2022, Galaxy2023, Galaxy2024]

class Fisch: # https://www.roblox.com/games/16732694052
    placeNames = 'Fisch', 'Fisch', 'F', 16732694052
    class Gamepasses:
        AppraisersLuck    = 'Appraisers Luck',     837341519, 'Appraisers_Luck'
        DoubleXP          = 'Double XP',           837360470, 'Double_XP'
        Supporter         = 'Supporter',           837478377, 'Supporter'
        EmotePack         = 'Emote Pack',          847012516, 'Emote_Pack'
        SellAnywhere      = 'Sell Anywhere',       901839344, 'Sell_Anywhere'
        BobberPack        = 'Bobber Pack',         927437431, 'Bobber_Pack'
        Radio             = 'Radio',               948629114, 'Radio'
        SpawnBoatAnywhere = 'Spawn Boat Anywhere', 986687236, 'Spawn_Boat_Anywhere'
        AppraiseAnywhere  = 'Appraise Anywhere',   986882975, 'Appraise_Anywhere'
        # List Of Gamepasses
        listOfGamepasses = [AppraisersLuck, DoubleXP, Supporter, EmotePack, SellAnywhere, BobberPack, Radio, SpawnBoatAnywhere, AppraiseAnywhere]
    class Badges:
        FirstTimeFischer        = 'First Time Fischer',         3713345851024569, 'First_Time_Fischer'
        SpecialSomeone          = 'Special Someone',            2548603185740666, 'Special_Someone'
        EconomyExpert           = 'Economy Expert',             4227551957813448, 'Economy_Expert'
        RareHunter              = 'Rare Hunter',                398396161277206,  'Rare_Hunter'
        KeepersPupil            = 'Keepers Pupil',              292081433761936,  'Keepers_Pupil'
        AttemptedUpgrade        = 'Attempted Upgrade',          2087500307302023, 'Attempted_Upgrade'
        DivineRelic             = 'Divine Relic',               4469874271658702, 'Divine_Relic'
        Catches50               = '50 Catches',                 3051769055311800, '50_Catches'
        Catches100              = '100 Catches',                980568772269520,  '100_Catches'
        Catches500              = '500 Catches',                2392322242811007, '500_Catches'
        Catches1000             = '1000 Catches',               2121501969748139, '1000_Catches'
        Catches2000             = '2000 Catches',               4043528816128290, '2000_Catches'
        Catches3000             = '3000 Catches',               2237691197864883, '3000_Catches'
        Catches4000             = '4000 Catches',               2586667227808420, '4000_Catches'
        Catches5000             = '5000 Catches',               2440764735271938, '5000_Catches'
        Catches10000            = '10,000 Catches',             1009279661183813, '10000_Catches'
        LavaCaster              = 'Lava Caster',                1708816354589502, 'Lava_Caster'
        ReconExpert             = 'Recon Expert',               3526079295826418, 'Recon_Expert'
        TruePower               = 'True Power',                 163992758707317,  'True_Power'
        ExperiencedTrueBeauty   = 'Experienced True Beauty',    553555175646641,  'Experienced_True_Beauty'
        BestiaryOcean           = 'Bestiary: Ocean',            1045860405568363, 'Bestiary_Ocean'
        BestiaryMoosewood       = 'Bestiary: Moosewood',        3871316346306270, 'Bestiary_Moosewood'
        BestiaryRoslit          = 'Bestiary: Roslit',           225841574756551,  'Bestiary_Roslit'
        BestiarySunstone        = 'Bestiary: Sunstone',         2903347774735091, 'Bestiary_Sunstone'
        BestiaryTerrapin        = 'Bestiary: Terrapin',         2994442057572213, 'Bestiary_Terrapin'
        BestiaryVolcano         = 'Bestiary: Volcano',          4479912445209985, 'Bestiary_Volcano'
        BestiaryVertigo         = 'Bestiary: Vertigo',          3200076862852988, 'Bestiary_Vertigo'
        BestiaryMushgrove       = 'Bestiary: Mushgrove',        4343979385420841, 'Bestiary_Mushgrove'
        BestiarySnowcap         = 'Bestiary: Snowcap',          4101868524305507, 'Bestiary_Snowcap'
        BestiaryEverything      = 'Bestiary: Everything',       635398639427099,  'Bestiary_Everything'
        BestiaryKeepersAltar    = 'Bestiary: Keepers Altar',    772547227400435,  'Bestiary_Keepers_Altar'
        BestiaryDesolateDeep    = 'Bestiary: Desolate Deep',    3161443122784523, 'Bestiary_Desolate_Deep'
        BestiaryBrinePool       = 'Bestiary: Brine Pool',       1535329670769985, 'Bestiary_Brine_Pool'
        BestiaryForsaken        = 'Bestiary: Forsaken',         3591399443042848, 'Bestiary_Forsaken'
        BestiaryDepths          = 'Bestiary: Depths',           2042505003241970, 'Bestiary_Depths'
        BestiaryAncientArchives = 'Bestiary: Ancient Archives', 1666493813690822, 'Bestiary_Ancient_Archives'
        BestiaryAncientIsles    = 'Bestiary: Ancient Isles',    2054807830474099, 'Bestiary_Ancient_Isles'
        BestiaryOvergrowthCaves = 'Bestiary: Overgrowth Caves', 272078520028439,  'Bestiary_Overgrowth_Caves'
        BestiaryFrigidCavern    = 'Bestiary: Frigid Cavern',    843774301770016,  'Bestiary_Frigid_Cavern'
        BestiaryCryogenicCanal  = 'Bestiary: Cryogenic Canal',  4189906956026791, 'Bestiary_Cryogenic_Canal'
        BestiaryGlacialGrotto   = 'Bestiary: Glacial Grotto',   1396071619017862, 'Bestiary_Glacial_Grotto'
        BestiaryGrandReef       = 'Bestiary: Grand Reef',       968483808853747,  'Bestiary_Grand_Reef'
        BestiaryAtlanteanStorm  = 'Bestiary: Atlantean Storm',  32642745294476,   'Bestiary_Atlantean_Storm'
        BestiaryAtlantis        = 'Bestiary: Atlantis',         2070428894950149, 'Bestiary_Atlantis'
        FischFright2024         = 'FISCHFRIGHT 2024',           2594646182778359, 'Fisch_Fright_2024'
        # List Of Badges    
        listOfBadges = [FirstTimeFischer, SpecialSomeone, EconomyExpert, RareHunter, KeepersPupil, AttemptedUpgrade, DivineRelic, Catches50, Catches100, Catches500, Catches1000, Catches2000, Catches3000, Catches4000, Catches5000, Catches10000, LavaCaster, ReconExpert, TruePower, ExperiencedTrueBeauty, BestiaryOcean, BestiaryMoosewood, BestiaryRoslit, BestiarySunstone, BestiaryTerrapin, BestiaryVolcano, BestiaryVertigo, BestiaryMushgrove, BestiarySnowcap, BestiaryEverything, BestiaryKeepersAltar, BestiaryDesolateDeep, BestiaryBrinePool, BestiaryForsaken, BestiaryDepths, BestiaryAncientArchives, BestiaryAncientIsles, BestiaryOvergrowthCaves, BestiaryFrigidCavern, BestiaryCryogenicCanal, BestiaryGlacialGrotto, BestiaryGrandReef, BestiaryAtlanteanStorm, BestiaryAtlantis, FischFright2024]

class FiveNightsTD: # https://www.roblox.com/games/15846919378
    placeNames = 'Five Nights TD', 'Five_Nights_TD', 'FNTD', 15846919378
    class Gamepasses:
        VIP = 'VIP', 755213386, 'VIP', True
        # List Of Gamepasses
        listOfGamepasses = [VIP]
    class Badges:
        JoinTheGame                = 'Join The Game',                  450768915498982,  'Join_The_Game'
        WinaGame                   = 'Win a Game',                     3361299059765,    'Win_a_Game'
        TheARG1                    = 'The ARG 1',                      2308722040924793, 'The_ARG_1'
        ARG2Winner                 = 'ARG 2 Winner',                   4348953112147721, 'ARG_2_Winner'
        CompleteGame1              = 'Complete Game 1',                1801557447657311, 'Complete_Game_1'
        CompleteGame2              = 'Complete Game 2',                660308672766666,  'Complete_Game_2'
        CompleteGame4              = 'Complete Game 4',                1352734224772502, 'Complete_Game_4'
        FinishGame3                = 'Finish Game 3',                  1249525436995984, 'Finish_Game_3'
        CompleteGame5              = 'Complete Game 5',                3840686186033460, 'Complete_Game_5'
        CompleteGame6              = 'Complete Game 6',                1289932523675224, 'Complete_Game_6'
        PlaySummerEvent            = 'Play Summer Event',              4093753784951799, 'Play_Summer_Event'
        CompleteSummerEvent        = 'Complete Summer Event',          4192377969805376, 'Complete_Summer_Event'
        PlayMilitaryEvent          = 'Play Military Event',            3717054685843370, 'Play_Military_Event'
        CompleteMilitaryEvent      = 'Complete Military Event',        1710710467179779, 'Complete_Military_Event'
        PlayWildWestEvent          = 'Play Wild West Event',           78638580451212,   'Play_WildWest_Event'
        FinishWildWest             = 'Finish Wild West',               4427897814216895, 'Finish_Wild_West'
        PlayHalloweenEvent         = 'Play Halloween Event',           481777508062526,  'Play_Halloween_Event'
        CompleteHalloweenEvent     = 'Complete Halloween Event',       314612341496152,  'Complete_Halloween_Event'
        PlayedSteampunkEvent       = 'PlayedSteampunk Event',          2794698248016894, 'Played_Steampunk_Event'
        CompletedSteampunkEvent    = 'Completed Steampunk Event',      4321640724737709, 'Completed_Steampunk_Event'
        PlayedChristmasEvent       = 'Played Christmas Event',         2924114884782147, 'Played_Christmas_Event'
        CompletedChristmasEvent    = 'Completed Christmas Event',      2486341879016297, 'Completed_Christmas_Event'
        ClaimCalenderSpecialReward = 'Claim Calender Special Reward',  3554984265461704, 'Claim_Calender_Special_Reward'
        # List Of Badges
        listOfBadges = [JoinTheGame, WinaGame, TheARG1, ARG2Winner, CompleteGame1, CompleteGame2, CompleteGame4, FinishGame3, CompleteGame5, CompleteGame6, PlaySummerEvent, CompleteSummerEvent, PlayMilitaryEvent, CompleteMilitaryEvent, PlayWildWestEvent, FinishWildWest, PlayHalloweenEvent, CompleteHalloweenEvent, PlayedSteampunkEvent, CompletedSteampunkEvent, PlayedChristmasEvent, CompletedChristmasEvent, ClaimCalenderSpecialReward]

class GrandPieceOnline: # https://www.roblox.com/games/1730877806
    placeNames = 'Grand Piece Online', 'Grand_Piece_Online', 'GPO', 1730877806
    class Gamepasses:
        EmotePack1          = 'Emote Pack #1',         5233790,    'Emote_Pack_1'
        EmotePack2          = 'Emote Pack #2',         6360299,    'Emote_Pack_2'
        EmotePack3          = 'Emote Pack #3',         9247442,    'Emote_Pack_3'
        x2_Bank_Storage     = '2x Bank Storage',       9846094,    '2x_Bank_Storage'
        DevilFruitNotifier  = 'Devil Fruit Notifier',  10535601,   'Devil_Fruit_Notifier'
        FruitBag            = 'Fruit Bag',             12776768,   'Fruit_Bag'
        Striker             = 'Striker',               12146732,   'Striker'
        CoffinBoat          = 'Coffin Boat',           10897748,   'Coffin_Boat'
        FacePack1           = 'Face Pack #1',          11023931,   'Face_Pack_1'
        PrivacyServers      = 'Privacy Servers',       12769541,   'Privacy_Servers'
        MemeEmotes          = 'Meme Emotes',           13465428,   'Meme_Emotes'
        MarineEmotes        = 'Marine Emotes',         13465435,   'Marine_Emotes'
        JojoEmotes          = 'Jojo Emotes',           13465461,   'Jojo_Emotes'
        MusicSnail          = 'Music Snail',           13467111,   'Music_Snail'
        DrippyFit           = 'Drippy Fit',            14337840,   'Drippy_Fit'
        DungeonMapChooser   = 'Dungeon Map Chooser',   24351992,   'Dungeon_Map_Chooser'
        FastAutoRaceReroll  = 'Fast Auto Race Reroll', 843435230,  'Fast_Auto_Race_Reroll'
        Season1Battlepass   = 'Season 1 Battlepass',   99823291,   'Season_1_Battlepass'
        Season2Battlepass   = 'Season 2 Battlepass',   114432469,  'Season_2_Battlepass'
        BP                  = 'BP',                    659418065,  'BP'
        ChristmasBattlepass = 'Christmas Battlepass',  676823798,  'Christmas_Battlepass'
        Season5BP           = 'Season 5 BP',           867616837,  'Season_5_BP'
        Season6BP           = 'Season 6 BP',           1010918687, 'Season_6_BP'
        # List Of Gamepasses
        listOfGamepasses = [EmotePack1, EmotePack2, EmotePack3, x2_Bank_Storage, DevilFruitNotifier, FruitBag, Striker, CoffinBoat, FacePack1, PrivacyServers, MemeEmotes, MarineEmotes, JojoEmotes, MusicSnail, DrippyFit, DungeonMapChooser, FastAutoRaceReroll, Season1Battlepass, Season2Battlepass, BP, ChristmasBattlepass, Season5BP, Season6BP]
    class Badges:
        early           = 'early',             2124538094, 'early'
        PaidAccessToken = 'Paid Access Token', 2124636610, 'Paid_Access_Token'
        CertifiedTrader = 'Certified Trader',  2124828978, 'Certified_Trader'
        ANewAdventure   = 'A New Adventure',   2127154256, 'A_New_Adventure'
        phoeyugate      = 'phoeyu gate',       2127585705, 'phoeyu_gate'
        # List Of Badges
        listOfBadges = [early, PaidAccessToken, CertifiedTrader, ANewAdventure, phoeyugate]

class JailBreak: # https://www.roblox.com/games/606849621
    placeNames = 'Jail Break', 'Jail_Break', 'JB', 606849621
    class Gamepasses:
        ExtraStorage = 'Extra Storage',               2068240,  'Extra_Storage'
        SWATTeam     = 'SWAT Team',                   2070427,  'SWAT_Team'
        CarStereo    = 'Car Stereo',                  2218187,  'Car_Stereo'
        DuffelBag    = 'Duffel Bag',                  2219040,  'Duffel_Bag'
        VIP          = 'VIP (Very Important Player)', 2296901,  'VIP_Very_Important_Player'
        ProGarage    = 'Pro Garage',                  2725211,  'Pro_Garage'
        CrimeBoss    = 'Crime Boss',                  4974038,  'Crime_Boss'
        XPBoost      = 'XP Boost',                    6631507,  'XP_Boost'
        VIPTrading   = 'VIP Trading',                 56149618, 'VIP_Trading'
        # List Of Gamepasses
        listOfGamepasses = [ExtraStorage, SWATTeam, CarStereo, DuffelBag, VIP, ProGarage, CrimeBoss, XPBoost, VIPTrading]
    class Badges:
        MVP                                 = 'MVP (Most Valuable Player)',              958186367,  'MVP_Most_Valuable_Player'
        BankBust                            = 'Bank Bust',                               958186941,  'Bank_Bust'
        DrillSergeant                       = 'Drill Sergeant',                          958187053,  'Drill_Sergeant'
        MasterCriminal                      = 'Master Criminal',                         958187226,  'Master_Criminal'
        BonnieAndClyde                      = 'Bonnie & Clyde',                          958187343,  'Bonnie_And_Clyde'
        SmoothCriminal                      = 'Smooth Criminal',                         958187470,  'Smooth_Criminal'
        MeetTheDevs                         = 'Meet The Devs!',                          1399506017, 'Meet_The_Devs'
        Unnamed1                            = '??? 1',                                   2124575784, 'Unnamed_1'
        JailbreakRBBattlesChampionshipBadge = 'Jailbreak RB Battles Championship Badge', 2124624990, 'Jailbreak_RB_Battles_Championship_Badge'
        Unnamed2                            = '??? 2',                                   2129465542, 'Unnamed_2'
        DefeatTheCEO                        = 'Defeat The CEO!',                         2129891386, 'Defeat_The_CEO'
        # List Of Badges
        listOfBadges = [MVP, BankBust, DrillSergeant, MasterCriminal, BonnieAndClyde, SmoothCriminal, MeetTheDevs, Unnamed1, JailbreakRBBattlesChampionshipBadge, Unnamed2, DefeatTheCEO]

class JujutsuInfinite: # https://www.roblox.com/games/10450270085
    placeNames = 'Jujutsu Infinite', 'Jujutsu_Infinite', 'JI', 10450270085
    class Gamepasses:
        InnateSlot3         = 'Innate Slot 3',        77102481,  'Innate_Slot_3'
        InnateSlot4         = 'Innate Slot 4',        77102528,  'Innate_Slot_4'
        HeavenlyRestriction = 'Heavenly Restriction', 77102969,  'Heavenly_Restriction'
        ExtraEmoteSlots     = 'Extra Emote Slots',    77103194,  'Extra_Emote_Slots'
        ItemNotifier        = 'Item Notifier',        77103458,  'Item_Notifier'
        InnateBag           = 'Innate Bag',           77110710,  'Innate_Bag'
        SkipSpins           = 'Skip Spins',           259500454, 'Skip_Spins'
        # List Of Gamepasses
        listOfGamepasses = [InnateSlot3, InnateSlot4, HeavenlyRestriction, ExtraEmoteSlots, ItemNotifier, InnateBag, SkipSpins]
    class Badges:
        PlayedJujutsuInfinite = 'Played Jujutsu Infinite', 2136221767,       'Played_Jujutsu_Infinite'
        DomainExpansion       = 'Domain Expansion',        2136222659,       'Domain_Expansion'
        SpecialGradeSorcerer  = 'Special Grade Sorcerer',  2136224010,       'Special_Grade_Sorcerer'
        PlayedTutorial        = 'Played Tutorial',         1768126716824041, 'Played_Tutorial'
        # List Of Badges
        listOfBadges = [PlayedJujutsuInfinite, DomainExpansion, SpecialGradeSorcerer, PlayedTutorial]

class KingLegacy: # https://www.roblox.com/games/4520749081
    placeNames = 'King Legacy', 'King_Legacy', 'KL', 4520749081
    class Gamepasses:
        Tips              = 'Tips',                7866886,  'Tips'
        QuestExperiencex2 = 'Quest Experience x2', 7888149,  'Quest_Experience_x2'
        NightBlade        = 'Night Blade',         7929804,  'Night_Blade'
        FruitPosition     = 'Fruit Position',      7936106,  'Fruit_Position'
        QuestMoneyx2      = 'Quest Money x2',      8114853,  'Quest_Money_x2'
        ConquerorAbility  = 'Conqueror Ability',   8287391,  'Conqueror_Ability'
        CoffinBoat        = 'Coffin Boat',         9876237,  'Coffin_Boat'
        ItemDropx2        = 'Item Drop x2',        18044132, 'Item_Drop_x2'
        LegacyPose        = 'Legacy Pose',         18399361, 'Legacy_Pose'
        FruitBag          = 'Fruit Bag',           23746192, 'Fruit_Bag'
        # List Of Gamepasses
        listOfGamepasses = [Tips, QuestExperiencex2, NightBlade, FruitPosition, QuestMoneyx2, ConquerorAbility, CoffinBoat, ItemDropx2, LegacyPose, FruitBag]
    class Badges:
        SecondSea = 'Second Sea', 570761085363018,  'Second_Sea'
        ThirdSea  = 'Third Sea',  2677309180656288, 'Third_Sea'
        # List Of Badges
        listOfBadges = [SecondSea, ThirdSea]

class MurderMystery2: # https://www.roblox.com/games/142823291
    placeNames = 'Murder Mystery 2', 'Murder_Mystery_2', 'MM2', 142823291
    class Gamepasses:
        Elite                    = 'Elite',                                   429957 ,    'Elite'
        Radio                    = 'Radio',                                   1308795,    'Radio'
        RandomizedFaces1         = 'Randomized Faces 1',                      79442,      'Randomized_Faces_1'
        RandomizedFaces2         = 'Randomized Faces 2',                      429356,     'Randomized_Faces_2'
        ShadowItemPack           = 'Shadow Item Pack',                        1201672,    'Shadow_Item_Pack'
        ClockworkItemPack        = 'Clockwork Item Pack ',                    1491260,    'Clockwork_Item_Pack'
        BIT8ItemPack             = '8-BIT Item Pack',                         1531578,    '8_BIT_Item_Pack'
        FuturisticItemPack       = 'Futuristic Item Pack',                    1712843,    'Futuristic_Item_Pack'
        AmericanItemPack         = 'American Item Pack',                      2002511,    'American_Item_Pack'
        HalloweenItemPack        = 'Halloween Item Pack',                     3346253,    'Halloween_Item_Pack'
        WinterItemPack           = 'Winter Item Pack',                        3646351,    'Winter_Item_Pack'
        Batwing                  = 'Batwing',                                 5299081,    'Batwing'
        Icewing                  = 'Icewing',                                 5593012,    'Icewing'
        GhostlyItemPack          = 'Ghostly Item Pack',                       7435036,    'Ghostly_Item_Pack'
        FrostbiteItemPack        = 'Frostbite Item Pack',                     7795820,    'Frostbite_Item_Pack'
        Bioblade                 = 'Bioblade',                                8456434,    'Bioblade'
        Prismatic                = 'Prismatic',                               10747452,   'Prismatic'
        VampiresEdge             = 'Vampire\'s Edge',                         12448341,   'Vampires_Edge'
        Peppermint               = 'Peppermint',                              13308756,   'Peppermint'
        Cookieblade              = 'Cookieblade',                             13502690,   'Cookieblade'
        Heartblade               = 'Heartblade',                              15066851,   'Heartblade'
        Eggblade                 = 'Eggblade',                                16462794,   'Eggblade'
        GODLYNebula              = 'GODLY: Nebula',                           21348436,   'GODLY_Nebula'
        EVOReaver                = 'EVO: Reaver',                             24102758,   'EVO_Reaver'
        GODLYIceBeam             = 'GODLY: Ice Beam',                         26304638,   'GODLY_Ice_Beam'
        GODLYIceFlake            = 'GODLY: Ice Flake',                        26304644,   'GODLY_Ice_Flake'
        BUNDLEIceBeamFlakeEffect = 'BUNDLE: Ice Beam, Ice Flake, Ice Effect', 26304640,   'BUNDLE_Ice_Beam_Ice_Flake_Ice_Effect'
        GODLYPlasmabeam          = 'GODLY: Plasmabeam',                       55292828,   'GODLY_Plasmabeam'
        GODLYPlasmablade         = 'GODLY: Plasmablade',                      55292879,   'GODLY_Plasmablade'
        BUNDLEPlasma             = 'BUNDLE: Plasma',                          55292987,   'BUNDLE_Plasma'
        GODLYPhantom             = 'GODLY: Phantom',                          93780280,   'GODLY_Phantom'
        GODLYSpectre             = 'GODLY: Spectre',                          93780323,   'GODLY_Spectre'
        BUNDLEPhantomSpectre     = 'BUNDLE: Phantom & Spectre',               93780371,   'BUNDLE_Phantom_Spectre'
        EVOIcecrusher            = 'EVO: Icecrusher',                         112956652,  'EVO_Icecrusher'
        GODLYBlossom             = 'GODLY: Blossom',                          131048887,  'GODLY_Blossom'
        GODLYSakura              = 'GODLY: Sakura',                           131048950,  'GODLY_Sakura'
        BUNDLESakura             = 'BUNDLE: Sakura',                          131048794,  'BUNDLE_Sakura'
        GODLYRainbowGun          = 'GODLY: Rainbow Gun',                      156618021,  'GODLY_Rainbow_Gun'
        GODLYRainbow             = 'GODLY: Rainbow',                          156618096,  'GODLY_Rainbow'
        BUNDLERainbow            = 'BUNDLE: Rainbow',                         156618061,  'BUNDLE_Rainbow'
        GODLYDarkshot            = 'GODLY: Darkshot',                         273009597,  'GODLY_Darkshot'
        GODLYDarksword           = 'GODLY: Darksword',                        273009675,  'GODLY_Darksword'
        BUNDLEDarknessPack       = 'BUNDLE: Darkness Pack',                   273009641,  'BUNDLE_Darkness_Pack'
        PACKLatte                = 'PACK: Latte',                             658376309,  'PACK_Latte'
        GODLYTurkey              = 'GODLY: Turkey',                           658667213,  'GODLY_Turkey'
        EVOGingerscythe          = 'EVO: Gingerscythe',                       674830453,  'EVO_Gingerscythe'
        GODLYFlowerwoodGun       = 'GODLY: Flowerwood Gun',                   768389355,  'GODLY_Flowerwood_Gun'
        GODLYFlowerwood          = 'GODLY: Flowerwood',                       769140200,  'GODLY_Flowerwood'
        BUNDLEFlowerwood         = 'BUNDLE: Flowerwood',                      767127317,  'BUNDLE_Flowerwood'
        GODLYPearlshine          = 'GODLY: Pearlshine',                       850293409,  'GODLY_Pearlshine'
        GODLYPearl               = 'GODLY: Pearl',                            850003963,  'GODLY_Pearl'
        BUNDLEPearls             = 'BUNDLE: Pearls',                          850387075,  'BUNDLE_Pearls'
        GODLYBorealis            = 'GODLY: Borealis',                         1008841389, 'GODLY_Borealis'
        GODLYAustralis           = 'GODLY: Australis',                        1008813284, 'GODLY_Australis'
        BUNDLEAurora             = 'BUNDLE: Aurora',                          1009231264, 'BUNDLE_Aurora'
        # List Of Gamepasses
        listOfGamepasses = [Elite, Radio, RandomizedFaces1, RandomizedFaces2, ShadowItemPack, ClockworkItemPack, BIT8ItemPack, FuturisticItemPack, AmericanItemPack, HalloweenItemPack, WinterItemPack, Batwing, Icewing, GhostlyItemPack, FrostbiteItemPack, Bioblade, Prismatic, VampiresEdge, Peppermint, Cookieblade, Heartblade, Eggblade, GODLYNebula, EVOReaver, GODLYIceBeam, GODLYIceFlake, BUNDLEIceBeamFlakeEffect, GODLYPlasmabeam, GODLYPlasmablade, BUNDLEPlasma, GODLYPhantom, GODLYSpectre, BUNDLEPhantomSpectre, EVOIcecrusher, GODLYBlossom, GODLYSakura, BUNDLESakura, GODLYRainbowGun, GODLYRainbow, BUNDLERainbow, GODLYDarkshot, GODLYDarksword, BUNDLEDarknessPack, PACKLatte, GODLYTurkey, EVOGingerscythe, GODLYFlowerwoodGun, GODLYFlowerwood, BUNDLEFlowerwood, GODLYPearlshine, GODLYPearl, BUNDLEPearls, GODLYBorealis, GODLYAustralis, BUNDLEAurora]
    class Badges:
        Level10            = 'Level 10',             196198137,  'Level_10'
        Level20            = 'Level 20',             196198654,  'Level_20'
        Level30            = 'Level 30',             196198776,  'Level_30'
        Level40            = 'Level 40',             196199518,  'Level_40'
        Level50            = 'Level 50',             196200089,  'Level_50'
        Level60            = 'Level 60',             196200207,  'Level_60'
        Level70            = 'Level 70',             196200425,  'Level_70'
        Level80            = 'Level 80',             196200625,  'Level_80'
        Level90            = 'Level 90',             196200691,  'Level_90'
        Level100           = 'Level 100',            196200785,  'Level_100'
        JoinedtheSurvivors = 'Joined the Survivors', 2129030855, 'Joined_the_Survivors'
        JoinedtheZombies   = 'Joined the Zombies',   2129030849, 'Joined_the_Zombies'
        RBKnife            = 'RB Knife',             2124636122, 'RB_Knife'
        # List Of Badges
        listOfBadges = [Level10, Level20, Level30, Level40, Level50, Level60, Level70, Level80, Level90, Level100, JoinedtheSurvivors, JoinedtheZombies, RBKnife]

class PetSimulator99: # https://www.roblox.com/games/8737899170
    placeNames = 'Pet Simulator 99', 'Pet_Simulator_99', 'PS99', 8737899170
    class Gamepasses:
        Lucky            = 'Lucky!',              205379487, 'Lucky'
        UltraLucky       = 'Ultra Lucky!',        257803774, 'Ultra_Lucky'
        VIP              = 'VIP!',                257811346, 'VIP'
        MagicEggs        = 'Magic Eggs!',         258567677, 'Magic_Eggs'
        Plus15Pets       = '+15 Pets!',           259437976, 'Plus_15_Pets'
        HugeHunter       = 'Huge Hunter!',        264808140, 'Huge_Hunter'
        AutoFarm         = 'Auto Farm!',          265320491, 'Auto_Farm'
        AutoTap          = 'Auto Tap!',           265324265, 'Auto_Tap'
        DaycareSlots     = 'Daycare Slots!',      651611000, 'Daycare_Slots'
        Plus15Eggs       = '+15 Eggs!',           655859720, 'Plus_15_Eggs'
        SuperDrops       = 'Super Drops!',        690997523, 'Super_Drops'
        DoubleStars      = 'Double Stars!',       720275150, 'Double_Stars'
        SuperShinyHunter = 'Super Shiny Hunter!', 975558264, 'Super_Shiny_Hunter'
        # List Of Gamepasses
        listOfGamepasses = [Lucky, UltraLucky, VIP, MagicEggs, Plus15Pets, HugeHunter, AutoFarm, AutoTap, DaycareSlots, Plus15Eggs, SuperDrops, DoubleStars, SuperShinyHunter]
    class Badges:
        Welcome             = 'Welcome',                 2153913164      , 'Welcome'
        TheHuntFirstEdition = 'The Hunt: First Edition', 3189151177666639, 'The_Hunt_First_Edition'
        # List Of Badges
        listOfBadges = [Welcome, TheHuntFirstEdition]

class PetSimulatorX: # https://www.roblox.com/games/6284583030
    placeNames = 'Pet Simulator X', 'Pet_Simulator_X', 'PSX', 6284583030
    class Gamepasses:
        Pets8Equipped   = '8 Pets Equipped!',   18674288,  '8_Pets_Equipped'
        Teleport        = 'Teleport!',          18674296,  'Teleport'
        Hoverboard      = 'Hoverboard!',        18674298,  'Hoverboard'
        VIP             = 'VIP!',               18674305,  'VIP'
        TripleEggs      = 'Triple Eggs!',       18674307,  'Triple_Eggs'
        PetStorage      = 'Pet Storage!',       18674317,  'Pet_Storage'
        EggSkip         = 'Egg Skip!',          18674321,  'Egg_Skip'
        SuperPetStorage = 'Super Pet Storage!', 18829757,  'Super_Pet_Storage'
        AutoHatch       = 'Auto Hatch!',        21176989,  'Auto_Hatch'
        Lucky           = 'Lucky!',             21583760,  'Lucky'
        MythicalHunter  = 'Mythical Hunter!',   21641016,  'Mythical_Hunter'
        MagicEggs       = 'Magic Eggs!',        22596039,  'Magic_Eggs'
        SuperMagnet     = 'Super Magnet!',      26398305,  'Super_Magnet'
        ShinyHunter     = 'Shiny Hunter!',      109685917, 'Shiny_Hunter'
        SecretHunter    = 'Secret Hunter!',     122535467, 'Secret_Hunter'
        # List Of Gamepasses
        listOfGamepasses = [Pets8Equipped, Teleport, Hoverboard, VIP, TripleEggs, PetStorage, EggSkip, SuperPetStorage, AutoHatch, Lucky, MythicalHunter, MagicEggs, SuperMagnet, ShinyHunter, SecretHunter]
    class Badges:
        Welcome = 'Welcome!', 2124793144, 'Welcome'
        # List Of Badges
        listOfBadges = [Welcome]
        
class PETSGO: # https://www.roblox.com/games/18901165922
    placeNames = 'PETS GO', 'PETS_GO', 'PG', 18901165922
    class Gamepasses:
        Lucky          = 'Lucky!',           923677450,  'Lucky'
        UltraLucky     = 'Ultra Lucky!',     924643143,  'Ultra_Lucky'
        CelestialLuck  = 'Celestial Luck!',  974931021,  'Celestial_Luck'
        VIP            = 'VIP!',             947426555,  'VIP'
        Plus3Pets      = '+3 Pets!',         955414606,  'Plus_3_Pets'
        HyperDice      = 'Hyper Dice!',      923754964,  'Hyper_Dice'
        DoubleDice     = 'Double Dice!',     951531608,  'Double_Dice'
        DoubleCoins    = 'Double Coins!',    955430652,  'Double_Coins'
        HugeHunter     = 'Huge Hunter!',     966471470,  'Huge_Hunter'
        DiamondPrinter = 'Diamond Printer!', 1008933294, 'Diamond_Printer'
        # List Of Gamepasses
        listOfGamepasses = [Lucky, UltraLucky, CelestialLuck, VIP, Plus3Pets, HyperDice, DoubleDice, DoubleCoins, HugeHunter, DiamondPrinter]
    class Badges:
        P                      = 'P',                          3587889778036452, 'P'
        E                      = 'E',                          513094477922687,  'E'
        T                      = 'T',                          2446810370554117, 'T'
        S                      = 'S',                          2632896258542796, 'S'
        G                      = 'G',                          3957160897472233, 'G'
        O                      = 'O',                          1244002859092897, 'O'
        RobloxWinterToken      = 'Roblox Winter Token!',       3275096128139364, 'Roblox_Winter_Token'
        RobloxWinterEliteToken = 'Roblox Winter Elite Token!', 3275096128139364, 'Roblox_Winter_Elite_Token'
        # List Of Badges
        listOfBadges = [P, E, T, S, G, O, RobloxWinterToken, RobloxWinterEliteToken]

class ProjectSlayers: # https://www.roblox.com/games/5956785391
    placeNames = 'Project Slayers', 'Project_Slayers', 'PS', 5956785391
    class Gamepasses:
        SealedBox                                   = 'Sealed Box',                                       15101943,  'Sealed_Box'
        MuzanSpawn                                  = 'Muzan Spawn',                                      17958345,  'Muzan_Spawn'
        TotalConcentrationandDemonprogressionviewer = 'Total Concentration and Demon progression viewer', 18589360,  'Total_Concentration_and_Demon_progression_viewer'
        DisableOrEnableSlayerCorpUniform            = 'Disable Or Enable Slayer Corp Uniform',            18710993,  'Disable_Or_Enable_Slayer_Corp_Uniform'
        GourdDurabilityViewer                       = 'Gourd Durability Viewer',                          19241624,  'Gourd_Durability_Viewer'
        MoreEyesOptions                             = 'More Eyes Options',                                19270529,  'More_Eyes_Options'
        MoreFacialAccessoriesOptions                = 'More Facial Accessories Options',                  19270563,  'More_Facial_Accessories_Options'
        SetSpawnAnywhere                            = 'Set Spawn Anywhere',                               19300397,  'Set_Spawn_Anywhere'
        UrokodakisMask                              = 'Urokodaki\'s Mask',                                19340032,  'Urokodakis_Mask'
        MoreCharacterSlots                          = 'More Character Slots',                             19426240,  'More_Character_Slots'
        PrivacyServers                              = 'Privacy Servers',                                  19516845,  'Privacy_Servers'
        CrowCustomization                           = 'Crow Customization',                               21698004,  'Crow_Customization'
        SkipSpin                                    = 'Skip Spin',                                        46503236,  'Skip_Spin'
        EmotePack                                   = 'Emote Pack',                                       42670615,  'Emote_Pack'
        EmotePack2                                  = 'Emote Pack 2',                                     178295110, 'Emote_Pack_2'
        ExtraEquipmentLoadouts                      = 'Extra Equipment Loadouts',                         181954095, 'Extra_Equipment_Loadouts'
        # List Of Gamepasses
        listOfGamepasses = [SealedBox, MuzanSpawn, TotalConcentrationandDemonprogressionviewer, DisableOrEnableSlayerCorpUniform, GourdDurabilityViewer, MoreEyesOptions, MoreFacialAccessoriesOptions, SetSpawnAnywhere, UrokodakisMask, MoreCharacterSlots, PrivacyServers, CrowCustomization, SkipSpin, EmotePack, EmotePack2, ExtraEquipmentLoadouts]

class RoyalHigh: # https://www.roblox.com/games/735030788
    placeNames = 'Royal High', 'Royal_High', 'RH', 735030788
    class Gamepasses:
        FasterFlightPlusCustomSpeeds                   = 'Faster Flight! (+ Custom Speeds)',                   3436552,   'Faster_Flight_Plus_Custom_Speeds'
        DoubleDiamonds                                 = 'Double Diamonds!',                                   3455446,   'Double_Diamonds'
        PaintbrushPass                                 = 'Paintbrush Pass!',                                   3457412,   'Paintbrush_Pass'
        QuadrupleDiamonds                              = 'Quadruple Diamonds!',                                3457593,   'Quadruple_Diamonds'
        NewHairColorsPlusGLOWINGHairPass4500PlusColors = 'New Hair Colors +GLOWING Hair Pass(4,500+ colors!)', 4097864,   'New_Hair_Colors_Plus_GLOWING_Hair_Pass_4500Plus_Colors'
        FlyonEarth                                     = 'Fly on Earth!',                                      5350675,   'Fly_on_Earth'
        SpecialFabricDesigns7000PlusDesigns            = 'Special Fabric Designs (7,000+ designs!)',           5585682,   'Special_Fabric_Designs_7000Plus_Designs'
        CrystalBallPower                               = 'Crystal Ball Power',                                 6316501,   'Crystal_Ball_Power'
        StickerPacksPass                               = 'Sticker Packs Pass!',                                10111433,  'Sticker_Packs_Pass'
        UploadCustomFabricsPass                        = 'Upload Custom Fabrics Pass!',                        785128363, 'Upload_Custom_Fabrics_Pass'
        MaterialsPass                                  = 'Materials Pass!',                                    982344484, 'Materials_Pass'
        # List Of Gamepasses
        listOfGamepasses = [FasterFlightPlusCustomSpeeds, DoubleDiamonds, PaintbrushPass, QuadrupleDiamonds, NewHairColorsPlusGLOWINGHairPass4500PlusColors, FlyonEarth, SpecialFabricDesigns7000PlusDesigns, CrystalBallPower, StickerPacksPass, UploadCustomFabricsPass, MaterialsPass]
    class Badges:
        PumpkinContest2018                      = 'Pumpkin Contest 2018',                         2124428491, 'Pumpkin_Contest_2018'
        Halloween2018                           = 'Halloween 2018',                               2124428509, 'Halloween_2018'
        SaintPatricksDay2019                    = 'Saint Patricks Day 2019!',                     2124459883, 'Saint_Patricks_Day_2019'
        Halloween2019DesignerEventCompletionist = 'Halloween 2019 Designer Event Completionist!', 2124487935, 'Halloween_2019_Designer_Event_Completionist'
        RoyaleHighHalloween2019                 = 'Royale High Halloween 2019!',                  2124490533, 'Royale_High_Halloween_2019'
        CompletedSuperHardMaze2019              = 'Completed Super Hard Maze 2019',               2124490534, 'Completed_Super_Hard_Maze_2019'
        RoyaleChristmas2019                     = 'Royale Christmas 2019!',                       2124498675, 'Royale_Christmas_2019'
        # List Of Badges
        listOfBadges = [PumpkinContest2018, Halloween2018, SaintPatricksDay2019, Halloween2019DesignerEventCompletionist, RoyaleHighHalloween2019, CompletedSuperHardMaze2019, RoyaleChristmas2019]

class SolsRNG: # https://www.roblox.com/games/15532962292
    placeNames = 'Sol\'s RNG', 'Sols_RNG', 'SRNG', 15532962292
    class Gamepasses:
        VIP                = 'VIP',                  705238616,  'VIP'
        VIP_Plus           = 'VIP+',                 952898058,  'VIP_Plus'
        QuickRoll          = 'Quick Roll',           673353863,  'Quick_Roll'
        InvisibleGear      = 'Invisible Gear',       792728808,  'Invisible_Gear'
        MerchantTeleporter = 'Merchant Teleporter',  879770191,  'Merchant_Teleporter'
        InnovatorPackVol1  = 'Innovator Pack Vol 1', 958699822,  'Innovator_Pack_Vol_1'
        InnovatorPackVol2  = 'Innovator Pack Vol 2', 958340231,  'Innovator_Pack_Vol_2'
        InnovatorPackVol3  = 'Innovator Pack Vol 3', 958598071,  'Innovator_Pack_Vol_3'
        # List Of Gamepasses
        listOfGamepasses = [VIP, VIP_Plus, QuickRoll, InvisibleGear, MerchantTeleporter, InnovatorPackVol1, InnovatorPackVol2, InnovatorPackVol3]
    class Badges:
        IjuststartedSolsRNG     = 'I just started Sol\'s RNG',        1441130719000460, 'I_just_started_Sols_RNG'
        Alittlebitofrolls       = 'A little bit of rolls',            3622512718465802, 'A_little_bit_of_rolls'
        ImaddictedtoSolsRNG     = 'I\'m addicted to Sol\'s RNG',      1107034638377762, 'Im_addicted_to_Sols_RNG'
        WouldYouLeaveNahIdRoll  = 'Would You Leave? / Nah I\'d Roll', 846169662502095,  'Would_You_Leave_Nah_Id_Roll'
        RollEatSleepRepeat      = 'Roll, Eat, Sleep, Repeat',         1872289370492358, 'Roll_Eat_Sleep_Repeat'
        Takeabreak              = 'Take a break',                     1092603390197325, 'Take_a_break'
        Icantstopplayingthis    = 'I can\'t stop playing this',       2731678596419900, 'I_cant_stop_playing_this'
        Wasteoftime             = 'Waste of time',                    4356557421515611, 'Waste_of_time'
        Touchthegrass           = 'Touch the grass',                  3336758570255487, 'Touch_the_grass'
        Breakthrough            = 'Breakthrough',                     2925176588215112, 'Breakthrough'
        Breakthelimit           = 'Break the limit',                  1356271377596280, 'Break_the_limit'
        SpottedtheSol           = 'Spotted the Sol',                  2201290015607347, 'Spotted_the_Sol'
        Indev                   = 'In-dev',                           1253153057071204, 'In_dev'
        Finishedworkfortoday    = 'Finished work for today',          257464335458276,  'Finished_work_for_today'
        Goodjobthisweektoo      = 'Good job this week too',           1918952643310114, 'Good_job_this_week_too'
        Asincereperson          = 'A sincere person',                 3145321935208607, 'A_sincere_person'
        Whenispayday            = 'When is payday???',                1496986902550849, 'When_is_payday'
        StarEgg                 = 'Star Egg',                         2270659814141729, 'Star_Egg'
        LockEgg                 = 'Lock Egg',                         559749433012559,  'Lock_Egg'
        Theresnowaytostopit     = 'There\'s no way to stop it!',      202360729284337,  'Theres_no_way_to_stop_it'
        Igivemylife             = 'I give my life...',                744944723444729,  'I_give_my_life'
        Eternaltime             = 'Eternal time...',                  4072147147623458, 'Eternal_time'
        BreaktheSpace           = 'Break the Space',                  1858966971108205, 'Break_the_Space'
        BreaktheGalaxy          = 'Break the Galaxy',                 1849903315759188, 'Break_the_Galaxy'
        BreaktheReality         = 'Break the Reality',                3593181263483436, 'Break_the_Reality'
        PerfectAttendanceAward  = 'Perfect Attendance Award',         3718807305779124, 'Perfect_Attendance_Award'
        Myfirst10MPlusfinding   = 'My first 10M+ finding',            1121298629065726, 'My_first_10M_Plus_finding'
        Myfirst100MPlusfinding  = 'My first 100M+ finding',           3516455555443766, 'My_first_100M_Plus_finding'
        Myfirst1BPlusfinding    = 'My first 1B+ finding',             1224551724339726, 'My_first_1B_Plus_finding'
        FlawsintheWorld         = '-Flaws in the World-',             2457971054390553, 'Flaws_in_the_World'
        OnewhostandsbeforeGod   = '-One who stands before God-',      3236492292509665, 'One_who_stands_before_God'
        TheUnknown              = '-The Unknown-',                    1503563480176545, 'The_Unknown'
        AchievementSlayer       = 'Achievement Slayer',               476770132708833,  'Achievement_Slayer'
        AchievementMaster       = 'Achievement Master',               1201821091232234, 'Achievement_Master'
        AchievementChampion     = 'Achievement Champion',             348376112222987,  'Achievement_Champion'
        TheStigma               = 'The Stigma',                       1896511924362574, 'The_Stigma'
        DAY100                  = '#DAY100',                          399984649890845,  'DAY100'
        SecretTrade             = 'Secret Trade',                     2620948537626731, 'Secret_Trade'
        Biomeitself             = 'Biome itself',                     4224933102884595, 'Biome_itself'
        Myeternaljourney        = 'My eternal journey',               1605629548712504, 'My_eternal_journey'
        TheLost                 = 'The Lost',                         2460941940564506, 'The_Lost'
        Famous                  = 'Famous!',                          4096899752944070, 'Famous'
        Grandmaster             = 'Grandmaster',                      2091741945674306, 'Grandmaster'
        Amemorytobeforgotten    = 'A memory to be forgotten',         3625566987462442, 'A_memory_to_be_forgotten'
        TheZero                 = 'The Zero',                         4370606648952666, 'The_Zero'
        Millions10              = '10,000,000',                       137829805535621,  '10000000'
        Millions15              = '15,000,000',                       485557368787476,  '15000000'
        Millions20              = '20,000,000',                       1801598389006571, '20000000'
        Millions30              = '30,000,000',                       2295935762202367, '30000000'
        Millions50              = '50,000,000',                       2994269484017383, '50000000'
        Unnamed1                = '??? 1',                            3137343012568311, 'Unnamed_1'
        Unnamed2                = '??? 2',                            734804938884338,  'Unnamed_2'
        Unnamed3                = '??? 3',                            1956542596523913, 'Unnamed_3'
        Unnamed4                = '??? 4',                            1324193838431233, 'Unnamed_4'
        Unnamed5                = '??? 5',                            807013057656632,  'Unnamed_5'
        # List Of Badges
        listOfBadges = [IjuststartedSolsRNG, Alittlebitofrolls, ImaddictedtoSolsRNG, WouldYouLeaveNahIdRoll, RollEatSleepRepeat, Takeabreak, Icantstopplayingthis, Wasteoftime, Touchthegrass, Breakthrough, Breakthelimit, SpottedtheSol, Indev, Finishedworkfortoday, Goodjobthisweektoo, Asincereperson, Whenispayday, StarEgg, LockEgg, Theresnowaytostopit, Igivemylife, Eternaltime, BreaktheSpace, BreaktheGalaxy, BreaktheReality, PerfectAttendanceAward, Myfirst10MPlusfinding, Myfirst100MPlusfinding, Myfirst1BPlusfinding, FlawsintheWorld, OnewhostandsbeforeGod, TheUnknown, AchievementSlayer, AchievementMaster, AchievementChampion, TheStigma, DAY100, SecretTrade, Biomeitself, Myeternaljourney, TheLost, Famous, Grandmaster, Amemorytobeforgotten, TheZero, Millions10, Millions15, Millions20, Millions30, Millions50, Unnamed1, Unnamed2, Unnamed3, Unnamed4, Unnamed5]

class ToiletTowerDefense: # https://www.roblox.com/games/13775256536
    placeNames = 'Toilet Tower Defense', 'Toilet_Tower_Defense', 'TTD', 13775256536
    class Gamepasses:
        Lucky                    = 'Lucky',                   208619622, 'Lucky'
        DoubleCoins              = 'Double Coins',            208620375, 'Double_Coins'
        VIP                      = 'VIP',                     257410325, 'VIP'
        Plus1000InventoryStorage = '+1000 Inventory Storage', 646799606, 'Plus_1000_Inventory_Storage'
        InfiniteUnits            = 'Infinite Units',          767749542, 'Infinite_Units'
        ClanCreator              = 'Clan Creator',            897195671, 'Clan_Creator'
        x2Drills                 = '2x Drills',               930624309, '2x_Drills'
        ShinyHunter              = 'Shiny Hunter',            952446306, 'Shiny_Hunter'
        # List Of Gamepasses
        listOfGamepasses = [Lucky, DoubleCoins, VIP, Plus1000InventoryStorage, InfiniteUnits, ClanCreator, x2Drills, ShinyHunter]
    class Badges:
        BeatEasyDifficulty           = 'Beat Easy Difficulty!',           2148808870,       'Beat_Easy_Difficulty'
        BeatMediumDifficulty         = 'Beat Medium Difficulty!',         2148808877,       'Beat_Medium_Difficulty'
        BeatHardDifficulty           = 'Beat Hard Difficulty!',           2148967266,       'Beat_Hard_Difficulty'
        BeatNightmareDifficulty      = 'Beat Nightmare Difficulty!',      2149510852,       'Beat_Nightmare_Difficulty'
        BeatAbysmalDifficulty        = 'Beat Abysmal Difficulty!',        205916089448424,  'Beat_Abysmal_Difficulty'
        BeatSecretEvilWave           = 'Beat Secret Evil Wave',           3269012098035529, 'Beat_Secret_Evil_Wave'
        TitanSpeakerman              = 'Titan Speakerman',                2148698556,       'Titan_Speakerman'
        TitanTVMan                   = 'Titan TV Man',                    2148967295,       'Titan_TV_Man'
        NinjaCameraman               = 'Ninja Cameraman',                 2149260235,       'Ninja_Cameraman'
        MechCameraman                = 'Mech Cameraman',                  2149529631,       'Mech_Cameraman'
        LaserCameramanCar            = 'Laser Cameraman Car',             2149898179,       'Laser_Cameraman_Car'
        SecretAgent                  = 'Secret Agent',                    2150077001,       'Secret_Agent'
        UpgradedTitanCameraman       = 'Upgraded Titan Cameraman',        2150356615,       'Upgraded_Titan_Cameraman'
        TitanCinemaman               = 'Titan Cinemaman',                 2150356638,       'Titan_Cinemaman'
        DarkSpeakerman               = 'Dark Speakerman',                 2150593479,       'Dark_Speakerman'
        UpgradedTitanSpeakerman      = 'Upgraded Titan Speakerman',       2150879473,       'Upgraded_Titan_Speakerman'
        DancingSpeakerwoman          = 'Dancing Speakerwoman',            2151779704,       'Dancing_Speakerwoman'
        GlitchCameraman              = 'Glitch Cameraman',                2153379585,       'Glitch_Cameraman'
        JetpackSpeakerman            = 'Jetpack Speakerman',              2153379588,       'Jetpack_Speakerman'
        UpgradedTitanCinemaman       = 'Upgraded Titan Cinemaman',        2502574037187648, 'Upgraded_Titan_Cinemaman'
        DualBatSpeakerman            = 'Dual Bat Speakerman',             4443545723157147, 'Dual_Bat_Speakerman'
        LargeLaserCameraman          = 'Large Laser Cameraman',           3045860093689297, 'Large_Laser_Cameraman'
        ShotgunCameraman             = 'Shotgun Cameraman',               2385641468984928, 'Shotgun_Cameraman'
        MinigunCamerawoman           = 'Minigun Camerawoman',             1233182747919466, 'Minigun_Camerawoman'
        KatanaSpeakerwoman           = 'Katana Speakerwoman',             2817031393332978, 'Katana_Speakerwoman'
        SpearSpeakerman              = 'Spear Speakerman',                1150879405352932, 'Spear_Speakerman'
        RedLaserCameraman            = 'Red Laser Cameraman',             931050305844465,  'Red_Laser_Cameraman'
        UpgradedMechCameraman        = 'Upgraded Mech Cameraman',         1115010233662541, 'Upgraded_Mech_Cameraman'
        MaceCamerawoman              = 'Mace Camerawoman',                1127660680344125, 'Mace_Camerawoman'
        ClockEvent                   = 'Clock Event',                     1630314579932289, 'Clock_Event'
        KnifeUpgradedTitanSpeakerman = 'Knife Upgraded Titan Speakerman', 4014008284565926, 'Knife_Upgraded_Titan_Speakerman'
        AstroGunCameraman            = 'Astro Gun Cameraman',             3721219248389823, 'Astro_Gun_Cameraman'
        SummerEvent2024              = 'Summer Event 2024',               2473445528937503, 'Summer_Event_2024'
        FinishedBeachBallHunt2024    = 'Finished Beach Ball Hunt 2024',   2247321279730360, 'Finished_Beach_Ball_Hunt_2024'
        BuffMutantToilet             = 'Buff Mutant Toilet',              1712380323524027, 'Buff_Mutant_Toilet'
        BeatDrillForest              = 'Beat Drill Forest',               1983663233025849, 'Beat_Drill_Forest'
        BeatDrillWorld               = 'Beat Drill World',                3719490798478354, 'Beat_Drill_World'
        BeatHalloweenGraveyard2024   = 'Beat Halloween Graveyard 2024',   2977453670049037, 'Beat_Halloween_Graveyard_2024'
        BeatThanksgivingTable        = 'Beat Thanksgiving Table',         1799362452924436, 'Beat_Thanksgiving_Table'
        BeatDiceWorld                = 'Beat Dice World',                 315021521983622,  'Beat_Dice_World'
        # List Of Badges
        listOfBadges = [BeatEasyDifficulty, BeatMediumDifficulty, BeatHardDifficulty, BeatNightmareDifficulty, BeatAbysmalDifficulty, BeatSecretEvilWave, TitanSpeakerman, TitanTVMan, NinjaCameraman, MechCameraman, LaserCameramanCar, SecretAgent, UpgradedTitanCameraman, TitanCinemaman, DarkSpeakerman, UpgradedTitanSpeakerman, DancingSpeakerwoman, GlitchCameraman, JetpackSpeakerman, UpgradedTitanCinemaman, DualBatSpeakerman, LargeLaserCameraman, ShotgunCameraman, MinigunCamerawoman, KatanaSpeakerwoman, SpearSpeakerman, RedLaserCameraman, UpgradedMechCameraman, MaceCamerawoman, ClockEvent, KnifeUpgradedTitanSpeakerman, AstroGunCameraman, SummerEvent2024, FinishedBeachBallHunt2024, BuffMutantToilet, BeatDrillForest, BeatDrillWorld, BeatHalloweenGraveyard2024, BeatThanksgivingTable, BeatDiceWorld]

class TowerDefenseSimulator: # https://www.roblox.com/games/3260590327
    placeNames = 'Tower Defense Simulator', 'Tower_Defense_Simulator', 'TDS', 3260590327
    class Gamepasses:
        Test                  = 'Test',                    6808274,    'Test'
        SmallDonation         = 'Small Donation',          6680173,    'Small_Donation'
        CrookBoss             = 'Crook Boss',              6757455,    'Crook_Boss'
        Turret                = 'Turret',                  6935538,    'Turret'
        CustomMusic           = 'Custom Music',            7104817,    'Custom_Music'
        Mortar                = 'Mortar',                  7838041,    'Mortar'
        Pursuit               = 'Pursuit',                 9735384,    'Pursuit'
        VIP                   = 'VIP',                     10518590,   'VIP'
        MemeEmotes            = 'Meme Emotes',             11467931,   'Meme_Emotes'
        Sledger               = 'Sledger',                 13534631,   'Sledger'
        Executioner           = 'Executioner',             25711202,   'Executioner'
        Engineer              = 'Engineer',                40385775,   'Engineer'
        ResizeYourPlayer      = 'Resize Your Player!',     65949871,   'Resize_Your_Player'
        Cowboy                = 'Cowboy',                  90119024,   'Cowboy'
        Warden                = 'Warden',                  99570026,   'Warden'
        VigilanteSkinBundle   = 'Vigilante Skin Bundle',   193944933,  'Vigilante_Skin_Bundle'
        UnwaveringTidesBundle = 'Unwavering Tides Bundle', 224102025,  'Unwavering_Tides_Bundle'
        MercenaryBase         = 'Mercenary Base',          786591818,  'Mercenary_Base'
        GatlingGun            = 'Gatling Gun!',            924927232,  'Gatling_Gun'
        AdminMode             = 'Admin Mode',              1002808617, 'Admin_Mode'
        Slasher               = 'Slasher',                 7386135,    'Slasher'
        Gladiator             = 'Gladiator',               7656528,    'Gladiator'
        FrostBlasterTower     = 'Frost Blaster Tower',     7846530,    'Frost_Blaster_Tower'
        GiftOfJoy             = 'Gift Of Joy',             7846620,    'Gift_Of_Joy'
        GiftofMystery         = 'Gift of Mystery',         7846621,    'Gift_of_Mystery'
        GiftofSharp           = 'Gift of Sharp',           7846623,    'Gift_of_Sharp'
        FireworksEmote        = 'Fireworks Emote',         7913109,    'Fireworks_Emote'
        PartySkins            = 'Party Skins',             7913591,    'Party_Skins'
        AllEasterSkins        = 'All Easter Skins',        8868550,    'All_Easter_Skins'
        Swarmer               = 'Swarmer',                 8868555,    'Swarmer'
        ArcherTower           = 'Archer Tower',            8928263,    'Archer_Tower'
        ToxicGunner           = 'Toxic Gunner',            13534630,   'Toxic_Gunner'
        ElfCamp               = 'Elf Camp!',               112619685,  'Elf_Camp'
        Necromancer           = 'Necromancer',             643819691,  'Necromancer'
        JesterTower           = 'Jester Tower!',           652291181,  'Jester_Tower'
        CryomancerTower       = 'Cryomancer Tower',        674876666,  'Cryomancer_Tower'
        Harvester             = 'Harvester',               953808062,  'Harvester'
        HallowPunk            = 'Hallow Punk',             954430263,  'Hallow_Punk'
        Commando              = 'Commando',                977109244,  'Commando'
        Elementalist          = 'Elementalist',            1007556869, 'Elementalist'
        Snowballer            = 'Snowballer',              1007420790, 'Snowballer'
        # List Of Gamepasses
        listOfGamepasses = [Test, SmallDonation, CrookBoss, Turret, CustomMusic, Mortar, Pursuit, VIP, MemeEmotes, Sledger, Executioner, Engineer, ResizeYourPlayer, Cowboy, Warden, VigilanteSkinBundle, UnwaveringTidesBundle, MercenaryBase, GatlingGun, AdminMode, Slasher, Gladiator, FrostBlasterTower, GiftOfJoy, GiftofMystery, GiftofSharp, FireworksEmote, PartySkins, AllEasterSkins, Swarmer, ArcherTower, ToxicGunner, ElfCamp, Necromancer, JesterTower, CryomancerTower, Harvester, HallowPunk, Commando, Elementalist, Snowballer]
    class Badges:
        WelcometoTDS           = 'Welcome to TDS!',           2124615656,       'Welcome_to_TDS'
        Level10                = 'Level 10',                  2124477834,       'Level_10'
        Lvl20                  = 'Lvl 20',                    2124477835,       'Lvl_20'
        Level30                = 'Level 30',                  2124475816,       'Level_30'
        Level50                = 'Level 50',                  2124477836,       'Level_50'
        Level75                = 'Level 75',                  2124477837,       'Level_75'
        Level100               = 'Level 100',                 2124477838,       'Level_100'
        ReachLevel150          = 'Reach Level 150!',          265315644206668,  'Reach_Level_150'
        DefeatGraveDigger      = 'Defeat Grave Digger',       2124572793,       'Defeat_Grave_Digger'
        DefeatMoltenWarlord    = 'Defeat Molten Warlord',     2124572794,       'Defeat_Molten_Warlord'
        DefeattheFallenKing    = 'Defeat the Fallen King',    2124615655,       'Defeat_the_Fallen_King'
        DefeatedNuclearMonster = 'Defeated Nuclear Monster!', 2127670181,       'Defeated_Nuclear_Monster'
        DefeatedGunslinger     = 'Defeated Gunslinger!',      2128794382,       'Defeated_Gunslinger'
        DefeatedWoxTheFox      = 'Defeated Wox The Fox!',     2129234537,       'Defeated_Wox_The_Fox'
        DefeatedPatientZero    = 'Defeated Patient Zero!',    2433001319089453, 'Defeated_Patient_Zero'
        TriumphHardcore        = 'Triumph Hardcore',          2124629158,       'Triumph_Hardcore'
        Quickdraw              = 'Quickdraw!',                2128794398,       'Quickdraw'
        TheLostSouls           = 'The Lost Souls',            2129234540,       'The_Lost_Souls'
        FrostInvasionEasy      = 'Frost Invasion - Easy',     1566890568849948, 'Frost_Invasion_Easy'
        FrostInvasionHard      = 'Frost Invasion - Hard',     842976148689508,  'Frost_Invasion_Hard'
        Unnamed                = '???',                       1270412135564244, 'Unnamed'
        # List Of Badges
        listOfBadges = [WelcometoTDS, Level10, Lvl20, Level30, Level50, Level75, Level100, ReachLevel150, DefeatGraveDigger, DefeatMoltenWarlord, DefeattheFallenKing, DefeatedNuclearMonster, DefeatedGunslinger, DefeatedWoxTheFox, DefeatedPatientZero, TriumphHardcore, Quickdraw, TheLostSouls, FrostInvasionEasy, FrostInvasionHard, Unnamed]

class YourBizarreAdventure: # https://www.roblox.com/games/2809202155
    placeNames = 'Your Bizarre Adventure', 'Your_Bizarre_Adventure', 'YBA', 2809202155
    class Gamepasses:
        ItemNotifier      = 'Item Notifier',          7355317,  'Item_Notifier'
        SelectPose        = 'Select Pose',            7361207,  'Select_Pose'
        CosmeticsBundle1  = 'Cosmetics Bundle #1',    7368580,  'Cosmetics_Bundle_1'
        VoiceLines        = 'Voice Lines',            7376923,  'Voice_Lines'
        Tips              = 'Tips',                   8062778,  'Tips'
        StandStorageSlot2 = 'Stand Storage: Slot #2', 9837261,  'Stand_Storage_Slot_2'
        StandStorageSlot3 = 'Stand Storage: Slot #3', 9838197,  'Stand_Storage_Slot_3'
        StandStorageSlot4 = 'Stand Storage: Slot #4', 16423469, 'Stand_Storage_Slot_4'
        StandStorageSlot5 = 'Stand Storage: Slot #5', 16423475, 'Stand_Storage_Slot_5'
        StyleStorageSlot2 = 'Style Storage: Slot #2', 13258801, 'Style_Storage_Slot_2'
        StyleStorageSlot3 = 'Style Storage: Slot #3', 13258808, 'Style_Storage_Slot_3'
        x2CosmeticSlots   = '2x Cosmetic Slots',      14597766, '2x_Cosmetic_Slots'
        x2Inventory       = '2x Inventory',           14597778, '2x_Inventory'
        # List Of Gamepasses
        listOfGamepasses = [ItemNotifier, SelectPose, CosmeticsBundle1, VoiceLines, Tips, StandStorageSlot2, StandStorageSlot3, StandStorageSlot4, StandStorageSlot5, StyleStorageSlot2, StyleStorageSlot3, x2CosmeticSlots, x2Inventory]
    class Badges:
        Prestige1 = 'Prestige 1', 2124517293, 'Prestige_1'
        Prestige2 = 'Prestige 2', 2124517294, 'Prestige_2'
        Prestige3 = 'Prestige 3', 2124517296, 'Prestige_3'
        # List Of Badges
        listOfBadges = [Prestige1, Prestige2, Prestige3]

listOfPlaces = [AUniversalTime, AdoptMe, AnimeAdventures, AnimeDefenders, AnimeVanguards, BeeSwarmSimulator, BladeBall, BloxFruits, BlueLockRivals, CreaturesofSonaria, DaHood, DragonAdventures, Fisch, FiveNightsTD, GrandPieceOnline, JailBreak, JujutsuInfinite, KingLegacy, MurderMystery2, PetSimulator99, PetSimulatorX, PETSGO, ProjectSlayers, RoyalHigh, SolsRNG, ToiletTowerDefense, TowerDefenseSimulator, YourBizarreAdventure]

class cookieData: #                 Normal Name                             Config Name                   Color           Sort
    isAccountLink                 = 'Link',                                 'Link',                       ANSI.FG.GREEN,  None
    isCountryRegistration         = 'Country Registration',                 'Country_Registration',       ANSI.FG.RED,    bool
    isID                          = 'ID',                                   'ID',                         ANSI.FG.GREEN,  bool
    isName                        = 'Name',                                 'Name',                       ANSI.FG.GREEN,  bool
    isDisplayName                 = 'Display Name',                         'Display_Name',               ANSI.FG.GREEN,  None
    isRegistrationDate            = 'Registration Date (D.M.Y)',            'Registration_Date',          ANSI.FG.RED,    None
    isExtendedRegistrationDateAge = 'Extended Registration Date (In Days)', 'Extended_Registration_Date', ANSI.FG.GREEN,  int
    isRobux                       = 'Robux',                                'Robux',                      ANSI.FG.RED,    int
    isBilling                     = 'Billing',                              'Billing',                    ANSI.FG.RED,    int
    isPending                     = 'Pending',                              'Pending',                    ANSI.FG.YELLOW, int
    isDonate                      = 'Donate',                               'Donate',                     ANSI.FG.YELLOW, int
    isPurchases                   = 'Purchases',                            'Purchases',                  ANSI.FG.BLUE,   int
    isRap                         = 'Rap',                                  'Rap',                        ANSI.FG.RED,    int
    isCard                        = 'Card',                                 'Card',                       ANSI.FG.RED,    int
    isPremium                     = 'Premium',                              'Premium',                    ANSI.FG.GREEN,  bool
    isGamepasses                  = 'Gamepasses',                           'Gamepasses',                 ANSI.FG.RED,    int
    isCustomGamepasses            = 'Custom Gamepasses',                    'Custom_Gamepasses',          ANSI.FG.BLUE,   int
    isBadges                      = 'Badges',                               'Badges',                     ANSI.FG.RED,    int
    isFavoritePlaces              = 'Favorite Places',                      'Favorite_Places',            ANSI.FG.RED,    int
    isBundles                     = 'Bundles',                              'Bundles',                    ANSI.FG.RED,    int
    isInventoryPrivacy            = 'Inventory Privacy',                    'Inventory_Privacy',          ANSI.FG.RED,    bool
    isTradePrivacy                = 'Trade Privacy',                        'Trade_Privacy',              ANSI.FG.RED,    bool
    isCanTrade                    = 'Can Trade',                            'Can_Trade',                  ANSI.FG.GREEN,  bool
    isSessions                    = 'Sessions',                             'Sessions',                   ANSI.FG.RED,    int
    isEmail                       = 'Email',                                'Email',                      ANSI.FG.GREEN,  bool
    isPhone                       = 'Phone',                                'Phone',                      ANSI.FG.RED,    bool
    is2FA                         = '2FA',                                  '2FA',                        ANSI.FG.GREEN,  bool
    isPin                         = 'Pin',                                  'Pin',                        ANSI.FG.GREEN,  bool
    isAbove13                     = '>13',                                  'Above_13',                   ANSI.FG.GREEN,  bool
    isVerifiedAge                 = 'Verified Age',                         'Verified_Age',               ANSI.FG.RED,    bool
    isVoice                       = 'Voice',                                'Voice',                      ANSI.FG.RED,    bool
    isNumberOfFriends             = 'Friends',                              'Friends',                    ANSI.FG.RED,    int
    isNumberOfFollowers           = 'Followers',                            'Followers',                  ANSI.FG.RED,    int
    isNumberOfFollowings          = 'Followings',                           'Followings',                 ANSI.FG.RED,    int
    isRobloxBadges                = 'Roblox Badges',                        'Roblox_Badges',              ANSI.FG.RED,    None
    isXCSRFToken                  = 'X-CSRF-Token',                         'X_CSRF_Token',               ANSI.FG.RED,    None
    isCookieInConsole             = 'Cookie (In Console)',                  'Cookie_In_Console',          ANSI.FG.GREEN,  None
    # List Of Cookie Data
    listOfCookieData = [isAccountLink, isCountryRegistration, isID, isName, isDisplayName, isRegistrationDate, isExtendedRegistrationDateAge, isRobux, isBilling, isPending, isDonate, isPurchases, isRap, isCard, isPremium, isGamepasses, isCustomGamepasses, isBadges, isFavoritePlaces, isBundles, isInventoryPrivacy, isTradePrivacy, isCanTrade, isSessions, isEmail, isPhone, is2FA, isPin, isAbove13, isVerifiedAge, isVoice, isNumberOfFriends, isNumberOfFollowers, isNumberOfFollowings, isRobloxBadges, isXCSRFToken, isCookieInConsole]

async def isValidFunc(cookieRoblox):
    async with ClientSession(cookies=cookieRoblox) as session:
        while True:
            try:
                async with session.get('https://www.roblox.com/my/settings/json', timeout=3, ssl=False) as response:
                    try:
                        data = await response.json()
                        isValid = True if 'UserId' in data else False
                    except ContentTypeError:
                        isValid = False
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Valid:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Yes' if isValid else f'{ANSI.FG.RED}No'}{ANSI.CLEAR} | ', f'Valid: {'Yes' if isValid else 'No'} | ', 'Yes' if isValid else 'No', isValid
            except (TypeError, ContentTypeError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, TimeoutError):
                await asyncio.sleep(2)

async def isLinkFunc(isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Link'] and not isControlPanel:
        return '', ''
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Link:{ANSI.CLEAR} https://www.roblox.com/users/{isID} | ', f'Link: https://www.roblox.com/users/{isID} | '

async def isUselessIDFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['ID'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://www.roblox.com/my/settings/json', timeout=3, ssl=False) as response:
                data = await response.json()
                isUselessID = data['UserId']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}ID:{ANSI.CLEAR} {isUselessID} | ', f'ID: {isUselessID} | ', isUselessID
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isAccountInformationFunc(session: ClientSession):
    while True:
        try:
            async with session.get(f'https://www.roblox.com/my/settings/json', timeout=3, ssl=False) as response:
                isAccountInfomation = await response.json()
            return isAccountInfomation
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isCountryRegistrationFunc(session: ClientSession, sendRequestsThrough: str, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Country_Registration'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://users.{sendRequestsThrough}.com/v1/users/authenticated/country-code', timeout=3, ssl=False) as response:
                data = await response.json()
                isCountryRegistration = data['countryCode']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Country Reg.:{ANSI.CLEAR} {isCountryRegistration} | ', f'Country Reg.: {isCountryRegistration} | ', isCountryRegistration
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isNameFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Name'] and not isControlPanel:
        return '', '', ''
    isName = isAccountInformation['Name']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Name:{ANSI.CLEAR} {isName} | ', f'Name: {isName} | ', isName

async def isDisplayNameFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Display_Name'] and not isControlPanel:
        return '', '', ''
    isDisplayName = isAccountInformation['DisplayName']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Display Name:{ANSI.CLEAR} {isDisplayName} | ', f'Display Name: {isDisplayName} | ', isDisplayName

async def isRegistrationDateFunc(session: ClientSession, isID, isAccountInformation, sendRequestsThrough: str, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Registration_Date'] and not isControlPanel:
        return '', '', '', '', '', ''
    while True:
        try:
            async with session.get(f'https://users.{sendRequestsThrough}.com/v1/users/{isID}', timeout=3, ssl=False) as response:
                data = await response.json()
                isRegistrationDate       = datetime.datetime.strptime(data['created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y')
                isRegistrationDateInDays = await isExtendedRegistrationDateAgeFunc(isAccountInformation)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Reg. Date:{ANSI.CLEAR} {isRegistrationDate}{isRegistrationDateInDays[0]} | ', f'Reg. Date: {isRegistrationDate}{isRegistrationDateInDays[0]} | ', isRegistrationDate, isRegistrationDateInDays[0], isRegistrationDateInDays[1], isRegistrationDateInDays[2]
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isExtendedRegistrationDateAgeFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Extended_Registration_Date'] and not isControlPanel:
        return '', '', ''
    isExtendedRegistrationDateAge = isAccountInformation['AccountAgeInDays']
    return f' ({isExtendedRegistrationDateAge})', f' ({isExtendedRegistrationDateAge})', isExtendedRegistrationDateAge

async def isRobuxFunc(session: ClientSession, isID, sendRequestsThrough: str, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Robux'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://economy.{sendRequestsThrough}.com/v1/users/{isID}/currency', timeout=3, ssl=False) as response:
                data = await response.json()
                isRobux = data['robux']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Robux:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isRobux}' if isRobux else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Robux: {isRobux} | ', isRobux
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isBillingFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Billing'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://apis.roblox.com/credit-balance/v1/get-conversion-metadata', timeout=3, ssl=False) as response:
                data = await response.json()
                isBilling = data['robuxConversionAmount']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Billing:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isBilling}' if isBilling else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Billing: {isBilling} | ', isBilling
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isTransactionsForYearFunc(session: ClientSession, isID, sendRequestsThrough: str, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Pending'] and not config['Roblox']['CookieChecker']['Main']['Donate'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://economy.{sendRequestsThrough}.com/v2/users/{isID}/transaction-totals?timeFrame=Year&transactionType=summary', timeout=3, ssl=False) as response:
                isTransactionsForYear = await response.json()
                isPending = isTransactionsForYear['pendingRobuxTotal']
                isDonate = isTransactionsForYear['outgoingRobuxTotal']
            if config['Roblox']['CookieChecker']['Main']['Pending'] and config['Roblox']['CookieChecker']['Main']['Donate'] or isControlPanel:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Pending:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isPending}' if isPending else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | {ANSI.FG.CYAN + ANSI.DECOR.BOLD}Donate:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isDonate}' if isDonate else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Pending: {f'{isPending}' if isPending else '0'} | Donate: {f'{isDonate}' if isDonate else '0'} | ', isPending, isDonate
            elif config['Roblox']['CookieChecker']['Main']['Pending']:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Pending:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isPending}' if isPending else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Pending: {f'{isPending}' if isPending else '0'} | ', isPending, isPending
            elif config['Roblox']['CookieChecker']['Main']['Donate']:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Donate:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isDonate}' if isDonate else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Donate: {f'{isDonate}' if isDonate else '0'} | ', isDonate, isDonate
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isPurchasesFunc(session: ClientSession, isID, sendRequestsThrough: str, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Purchases'] and not config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] and not isControlPanel:
        return '', '', ''
    maxPages = max(config['Roblox']['CookieChecker']['Main']['Purchases_Max_Check_Pages'], config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'])
    isPurchases = 0
    pageCurrentCount = 1
    isCustomGamepasses = []
    while True:
        try:
            async with session.get(f'https://economy.{sendRequestsThrough}.com/v2/users/{isID}/transactions?transactionType=2&limit=100', timeout=3, ssl=False) as response:
                purchases = await response.json()
                nextPageCursorPurchases = purchases['nextPageCursor']
                for purchase in purchases['data']:
                    if config['Roblox']['CookieChecker']['Main']['Purchases']:
                        isPurchases += int(str(purchase['currency']['amount'])[1:])
                    if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] and purchase['details']['name'] in checkListCustomGamepasses:
                        isCustomGamepasses.append(purchase['details']['name'])
                while nextPageCursorPurchases != None and pageCurrentCount != maxPages or 'errors' in purchases:
                    try:
                        async with session.get(f'https://economy.{sendRequestsThrough}.com/v2/users/{isID}/transactions?transactionType=2&limit=100&cursor={nextPageCursorPurchases}', timeout=3, ssl=False) as response:
                            purchases = await response.json()
                            for purchase in purchases['data']:
                                if config['Roblox']['CookieChecker']['Main']['Purchases'] and (config['Roblox']['CookieChecker']['Main']['Purchases_Max_Check_Pages'] == 0 or pageCurrentCount < config['Roblox']['CookieChecker']['Main']['Purchases_Max_Check_Pages']):
                                    isPurchases += int(str(purchase['currency']['amount'])[1:])
                                if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] and purchase['details']['name'] in checkListCustomGamepasses and (config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'] == 0 or pageCurrentCount < config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages']):
                                    isCustomGamepasses.append(purchase['details']['name'])
                            nextPageCursorPurchases = purchases['nextPageCursor']
                            pageCurrentCount += 1
                    except (KeyError, TypeError, ContentTypeError):
                        await asyncio.sleep(2)
            if config['Roblox']['CookieChecker']['Main']['Purchases'] and config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] or isControlPanel:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Purchases:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isPurchases}' if isPurchases else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Purchases: {isPurchases} | ', isPurchases, f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Custom Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isCustomGamepasses)}' if isCustomGamepasses else f'{ANSI.FG.RED}0{ANSI.CLEAR}'} | ', f'Custom Gamepasses: {len(isCustomGamepasses)} | ', len(isCustomGamepasses)
            elif config['Roblox']['CookieChecker']['Main']['Purchases']:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Purchases:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isPurchases}' if isPurchases else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Purchases: {isPurchases} | ', isPurchases, '', '', ''
            elif config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']:
                return '', '', '', f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Custom Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isCustomGamepasses)}' if isCustomGamepasses else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Custom Gamepasses: {len(isCustomGamepasses)} | ', len(isCustomGamepasses)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isRapFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Rap'] and not isControlPanel:
        return '', '', ''
    isRap = 0
    pageCurrentCount = 1
    while True:
        try:
            async with session.get(f'https://inventory.roblox.com/v1/users/{isID}/assets/collectibles?sortOrder=Asc&limit=100', timeout=3, ssl=False) as response:
                rap = await response.json()
                nextPageCursorRap = rap['nextPageCursor']
                for item in rap['data']:
                    if str(item['recentAveragePrice']).isdigit(): isRap += int(item['recentAveragePrice'])
                while nextPageCursorRap != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Rap_Max_Check_Pages'] or 'errors' in rap:
                    try:
                        async with session.get(f'https://inventory.roblox.com/v1/users/{isID}/assets/collectibles?sortOrder=Asc&limit=100&cursor={nextPageCursorRap}', timeout=3, ssl=False) as response:
                            rap = await response.json()
                            for item in rap['data']:
                                if str(item['recentAveragePrice']).isdigit(): isRap += int(item['recentAveragePrice'])
                            nextPageCursorRap = rap['nextPageCursor']
                            pageCurrentCount += 1
                    except (KeyError, TypeError, ContentTypeError):
                        await asyncio.sleep(2)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Rap:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isRap}' if isRap else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Rap: {isRap} | ', isRap
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isCardFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Card'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://apis.roblox.com/payments-gateway/v1/payment-profiles', timeout=3, ssl=False) as response:
                isCard = await response.json()
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Card:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isCard)}' if isCard else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Card: {len(isCard) if isCard else '0'} | ', len(isCard)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isPremiumFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Premium'] and not isControlPanel:
        return '', '', ''
    isPremium = isAccountInformation['IsPremium']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Premium:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Yes' if isPremium else f'{ANSI.FG.RED}No'}{ANSI.CLEAR} | ', f'Premium: {'Yes' if isPremium else 'No'} | ', 'Yes' if isPremium else 'No', isPremium

async def isGamepassesFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Gamepasses'] and not isControlPanel:
        return '', '', ''
    isGamepasses = []
    pageCurrentCount = 1
    isGamepassesTimedList = checkListGamepasses[:]
    while True:
        try:
            async with session.get(f'https://apis.roblox.com/game-passes/v1/users/{isID}/game-passes?count=100', timeout=3, ssl=False) as response:
                gamepasses = await response.json()
                if not gamepasses['gamePasses']:
                    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Gamepasses: 0 | ', 0
                for gamepass in gamepasses['gamePasses']:
                    if gamepass['gamePassId'] in isGamepassesTimedList:
                        isGamepassesTimedList.remove(gamepass['gamePassId'])
                        isGamepasses.append(gamepass['gamePassId'])
                while isGamepassesTimedList and len(isGamepasses) >= 100 and gamepasses['gamePassId'] and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Gamepasses_Max_Check_Pages'] or 'errors' in gamepasses:
                    try:
                        async with session.get(f'https://apis.roblox.com/game-passes/v1/users/{isID}/game-passes?count=100&exclusiveStartId={nextPage}', timeout=3, ssl=False) as response:
                            nextPage = isGamepasses[-1]
                            gamepasses = await response.json()
                            if not gamepasses['gamePasses']:
                                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isGamepasses)}' if isGamepasses else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Gamepasses: {len(isGamepasses)} | ', len(isGamepasses)
                            for gamepass in gamepasses['gamePasses']:
                                if gamepass['gamePassId'] in isGamepassesTimedList:
                                    isGamepasses.append(gamepass['gamePassId'])
                                    isGamepassesTimedList.remove(gamepass['gamePassId'])
                            pageCurrentCount += 1
                    except (KeyError, TypeError, ContentTypeError):
                        await asyncio.sleep(2)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isGamepasses)}' if isGamepasses else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Gamepasses: {len(isGamepasses)} | ', len(isGamepasses)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isBadgesFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Badges'] and not isControlPanel:
        return '', '', ''
    isBadges = []
    pageCurrentCount = 1
    isBadgesTimedFunc = checkListBadges[:]
    while True:
        try:
            async with session.get(f'https://badges.roblox.com/v1/users/{isID}/badges?limit=100&sortOrder=Desc', timeout=3, ssl=False) as response:
                badges = await response.json()
                nextPageCursorBadges = badges['nextPageCursor']
                for badge in badges['data']:
                    if badge['id'] in isBadgesTimedFunc:
                        isBadges.append(badge['id'])
                        isBadgesTimedFunc.remove(badge['id'])
                while isBadgesTimedFunc and nextPageCursorBadges != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Badges_Max_Check_Pages']:
                    async with session.get(f'https://badges.roblox.com/v1/users/{isID}/badges?limit=100&sortOrder=Desc&cursor={nextPageCursorBadges}', timeout=3, ssl=False) as response:
                        badges = await response.json()
                        for badge in badges['data']:
                            if badge['id'] in isBadgesTimedFunc:
                                isBadges.append(badge['id'])
                                isBadgesTimedFunc.remove(badge['id'])
                        nextPageCursorBadges = badges['nextPageCursor']
                        pageCurrentCount += 1
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Badges:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isBadges)}' if isBadges else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Badges: {len(isBadges)} | ', len(isBadges)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isFavoritePlacesFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Favorite_Places'] and not isControlPanel:
        return '', '', ''
    isFavoritePlaces = []
    pageCurrentCount = 1
    isFavoritePlacesTimedFunc = checkListFavoritePlaces[:]
    while True:
        try:
            async with session.get(f'https://games.roblox.com/v2/users/{isID}/favorite/games?limit=100', timeout=3, ssl=False) as response:
                favoritePlaces = await response.json()
                nextPageCursorFavoritePlaces = favoritePlaces['nextPageCursor']
                for game in favoritePlaces['data']:
                    if game['rootPlace']['id'] in isFavoritePlacesTimedFunc:
                        isFavoritePlaces.append(game['rootPlace']['id'])
                        isFavoritePlacesTimedFunc.remove(game['rootPlace']['id'])
                while nextPageCursorFavoritePlaces != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages'] or 'errors' in favoritePlaces:
                    try:
                        async with session.get(f'https://games.roblox.com/v2/users/{isID}/favorite/games?limit=100&cursor={nextPageCursorFavoritePlaces}', timeout=3, ssl=False) as response:
                            favoritePlaces = await response.json()
                            for game in favoritePlaces['data']:
                                if game['rootPlace']['id'] in isFavoritePlacesTimedFunc:
                                    isFavoritePlaces.append(game['rootPlace']['id'])
                                    isFavoritePlacesTimedFunc.remove(game['rootPlace']['id'])
                            nextPageCursorFavoritePlaces = favoritePlaces['nextPageCursor']
                            pageCurrentCount += 1
                    except (KeyError, TypeError, ContentTypeError):
                        await asyncio.sleep(2)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Favorites:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isFavoritePlaces)}' if isFavoritePlaces else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Fav. Games: {len(isFavoritePlaces)} | ', len(isFavoritePlaces)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isBundlesFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Bundles'] and not isControlPanel:
        return '', '', ''
    isBundles = []
    pageCurrentCount = 1
    isBundlesTimedFunc = checkListBundles[:]
    while True:
        try:
            async with session.get(f'https://catalog.roblox.com/v1/users/{isID}/bundles?limit=100', timeout=3, ssl=False) as response:
                bundles = await response.json()
                nextPageCursorBundles = bundles['nextPageCursor']
                for bundle in bundles['data']:
                    if bundle['id'] in isBundlesTimedFunc:
                        isBundles.append(bundle['id'])
                        isBundlesTimedFunc.remove(bundle['id'])
                while nextPageCursorBundles != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages'] or 'errors' in bundles:
                    try:
                        async with session.get(f'https://catalog.roblox.com/v1/users/{isID}/bundles?limit=100&cursor={nextPageCursorBundles}', timeout=3, ssl=False) as response:
                            bundles = await response.json()
                            for bundle in bundles['data']:
                                if bundle['id'] in isBundlesTimedFunc:
                                    isBundles.append(bundle['id'])
                                    isBundlesTimedFunc.remove(bundle['id'])
                            nextPageCursorBundles = bundles['nextPageCursor']
                            pageCurrentCount += 1
                    except (KeyError, TypeError, ContentTypeError):
                        await asyncio.sleep(2)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Bundles:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isBundles)}' if isBundles else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Bundles: {len(isBundles)} | ', len(isBundles)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isInventoryPrivacyFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Inventory_Privacy'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://apis.roblox.com/user-settings-api/v1/user-settings/settings-and-options', timeout=3, ssl=False) as response:
                data = await response.json()
                isInventoryPrivacy = data['whoCanSeeMyInventory']['currentValue']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Inv. Privacy:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Everyone' if isInventoryPrivacy == 'AllUsers' else f'{ANSI.FG.YELLOW}Friends & Followers & Followings' if isInventoryPrivacy == 'FriendsFollowingAndFollowers' else f'{ANSI.FG.YELLOW}Friends & Followings' if isInventoryPrivacy == 'FriendsAndFollowing' else f'{ANSI.FG.YELLOW}Friends' if isInventoryPrivacy == 'Friends' else f'{ANSI.FG.RED}No One'}{ANSI.CLEAR} | ', f'Inv. Privacy: {'Everyone' if isInventoryPrivacy == 'AllUsers' else 'Friends & Followers & Followings' if isInventoryPrivacy == 'FriendsFollowingAndFollowers' else 'Friends & Followings' if isInventoryPrivacy == 'FriendsAndFollowing' else 'Friends' if isInventoryPrivacy == 'Friends' else 'No One'} | ', 'Everyone' if isInventoryPrivacy == 'AllUsers' else 'Friends & Followers & Followings' if isInventoryPrivacy == 'FriendsFollowingAndFollowers' else 'Friends & Followings' if isInventoryPrivacy == 'FriendsAndFollowing' else 'Friends' if isInventoryPrivacy == 'Friends' else 'No One'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isTradePrivacyFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Trade_Privacy'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://accountsettings.roblox.com/v1/trade-privacy', timeout=3, ssl=False) as response:
                data = await response.json()
                isTradePrivacy = data['tradePrivacy']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Trade Privacy:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}No{ANSI.CLEAR}' if isTradePrivacy == 'AllUsers' else f'{ANSI.FG.RED}Yes{ANSI.CLEAR}'} | ', f'Trade Privacy: {'No' if isTradePrivacy == 'AllUsers' else 'Yes'} | ', 'No' if isTradePrivacy == 'AllUsers' else 'Yes'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isCanTradeFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Can_Trade'] and not isControlPanel:
        return '', '', ''
    isCanTrade = isAccountInformation['CanTrade']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Can Trade:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Yes' if isCanTrade else f'{ANSI.FG.RED}No'}{ANSI.CLEAR} | ', f'Can Trade: {'Yes' if isCanTrade else 'No'} | ', 'Yes' if isCanTrade else 'No'

async def isSessionsFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Sessions'] and not isControlPanel:
        return '', '', ''
    pageCurrentCount = 1
    while True:
        try:
            async with session.get('https://apis.roblox.com/token-metadata-service/v1/sessions', timeout=3, ssl=False) as response:
                data = await response.json()
                isSessions = len(data['sessions'])
                nextPageCursorSessions = data['nextCursor']
                while (nextPageCursorSessions != None and 'statusCode' not in data and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages']) or ('errors' in data and 'statusCode' not in data): # на 3 странице возникает 500 ошибка, непонятка =(
                    try:
                        async with session.get(f'https://apis.roblox.com/token-metadata-service/v1/sessions?nextCursor={nextPageCursorSessions}', timeout=3, ssl=False) as response:
                            data = await response.json()
                            isSessions += len(data['sessions'])
                            nextPageCursorSessions = data['nextCursor']
                            pageCurrentCount += 1
                    except (KeyError, TypeError, ContentTypeError):
                        await asyncio.sleep(2)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Sessions:{ANSI.CLEAR} {f'{ANSI.FG.RED}{isSessions}' if isSessions >= 10 else f'{ANSI.FG.YELLOW}{isSessions}' if isSessions >= 5 else f'{ANSI.FG.GREEN}{isSessions}'}{ANSI.CLEAR} | ', f'Sessions: {isSessions} | ', isSessions
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isEmailFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Email'] and not isControlPanel:
        return '', '', ''
    isEmailSetted = isAccountInformation['MyAccountSecurityModel']['IsEmailSet']
    isEmailVerified = isAccountInformation['MyAccountSecurityModel']['IsEmailVerified']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Email:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}No' if not isEmailSetted else f'{ANSI.FG.RED}Yes' if isEmailSetted and isEmailVerified else f'{ANSI.FG.YELLOW}Setted'}{ANSI.CLEAR} | ', f'Email: {'No' if not isEmailSetted else 'Yes' if isEmailSetted and isEmailVerified else 'Setted'} | ', 'No' if not isEmailSetted else 'Yes' if isEmailSetted and isEmailVerified else 'Setted'

async def isPhoneFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Phone'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://accountinformation.roblox.com/v1/phone', timeout=3, ssl=False) as response:
                data = await response.json()
                isPhone = data['phone']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Phone:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}No' if isPhone == None else f'{ANSI.FG.RED}Yes'}{ANSI.CLEAR} | ', f'Phone: {'No' if isPhone == None else 'Yes'} | ', 'No' if isPhone == None else 'Yes'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def is2FAFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['2FA'] and not isControlPanel:
        return '', '', ''
    is2FA = isAccountInformation['MyAccountSecurityModel']['IsTwoStepEnabled']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}2FA:{ANSI.CLEAR} {f'{ANSI.FG.RED}Yes' if is2FA else f'{ANSI.FG.GREEN}No'}{ANSI.CLEAR} | ', f'2FA: {'Yes' if is2FA else 'No'} | ', 'Yes' if is2FA else 'No'

async def isPinFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Pin'] and not isControlPanel:
        return '', '', ''
    isPin = isAccountInformation['IsAccountPinEnabled']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Pin:{ANSI.CLEAR} {f'{ANSI.FG.RED}Yes' if isPin else f'{ANSI.FG.GREEN}No'}{ANSI.CLEAR} | ', f'Pin: {'Yes' if isPin else 'No'} | ', 'Yes' if isPin else 'No'

async def isAbove13Func(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Above_13'] and not isControlPanel:
        return '', '', ''
    isAbove13 = isAccountInformation['UserAbove13']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}>13:{ANSI.CLEAR} {'Yes' if isAbove13 else 'No'} | ', f'>13: {'Yes' if isAbove13 else 'No'} | ', 'Yes' if isAbove13 else 'No'

async def isVerifiedAgeFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Verified_Age'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://apis.roblox.com/age-verification-service/v1/age-verification/verified-age', timeout=3, ssl=False) as response:
                data = await response.json()
                isVerifiedAge = data['isVerified']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Verified Age:{ANSI.CLEAR} {'Yes' if isVerifiedAge else 'No'} | ', f'Verified Age: {'Yes' if isVerifiedAge else 'No'} | ', 'Yes' if isVerifiedAge else 'No'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isVoiceFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Voice'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://voice.roblox.com/v1/settings', timeout=3, ssl=False) as response:
                data = await response.json()
                isVoice = data['isVerifiedForVoice']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Voice:{ANSI.CLEAR} {'Yes' if isVoice else 'No'} | ', f'Voice: {'Yes' if isVoice else 'No'} | ', 'Yes' if isVoice else 'No'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isNumberOfFriendsFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Friends'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://friends.roblox.com/v1/users/{isID}/friends/count', timeout=3, ssl=False) as response:
                data = await response.json()
                isNumberOfFriends = data['count']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Friends:{ANSI.CLEAR} {isNumberOfFriends} | ', f'Friends: {isNumberOfFriends} | ', isNumberOfFriends
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isNumberOfFollowersFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Followers'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://friends.roblox.com/v1/users/{isID}/followers/count', timeout=3, ssl=False) as response:
                data = await response.json()
                isNumberOfFollowers = data['count']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Followers:{ANSI.CLEAR} {isNumberOfFollowers} | ', f'Followers: {isNumberOfFollowers} | ', isNumberOfFollowers
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isNumberOfFollowingsFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Followings'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://friends.roblox.com/v1/users/{isID}/followings/count', timeout=3, ssl=False) as response:
                data = await response.json()
                isNumberOfFollowings = data['count']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Followings:{ANSI.CLEAR} {isNumberOfFollowings} | ', f'Followings: {isNumberOfFollowings} | ', isNumberOfFollowings
        except (KeyError, TypeError, ContentTypeError, ):
            await asyncio.sleep(2)

async def isRobloxBadgesFunc(session: ClientSession, isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Roblox_Badges'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://accountinformation.roblox.com/v1/users/{isID}/roblox-badges', timeout=3, ssl=False) as response:
                robloxBadges = await response.json()
                isRobloxBadges = [robloxBadge['name'] for robloxBadge in robloxBadges]
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Roblox Badges:{ANSI.CLEAR} {', '.join(isRobloxBadges) if isRobloxBadges else 'No'} | ', f'Roblox Badges: {', '.join(isRobloxBadges) if isRobloxBadges else 'No'} | ', isRobloxBadges
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

async def isXCSRFTokenFunc(session: ClientSession, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['X_CSRF_Token'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.post('https://auth.roblox.com/v2/logout') as response:
                isXCSRFToken = response.headers['X-CSRF-Token']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}X-CSRF-Token:{ANSI.CLEAR} {isXCSRFToken} | ', f'X-CSRF-Token: {isXCSRFToken} | ', isXCSRFToken
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(2)

def getGlobalsCheckListGamepasses():
    global checkListGamepasses; checkListGamepasses = []
    for place in listOfPlaces:
        if config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] and getattr(place, 'Gamepasses', False):
            for gamepass in place.Gamepasses.listOfGamepasses:
                if config['Roblox']['CookieChecker'][place.__name__][gamepass[2]]:
                    checkListGamepasses.append(gamepass[1])
    for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
        if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][0] and f'{customPlace}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']:
            for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlace}_Gamepasses']:
                if gamepass[2]:
                    checkListGamepasses.append(gamepass[0])

def getGlobalsCheckListBadges():
    global checkListBadges; checkListBadges = []
    for place in listOfPlaces:
        if config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] and getattr(place, 'Badges', False):
            for badge in place.Badges.listOfBadges:
                if config['Roblox']['CookieChecker'][place.__name__][badge[2]]:
                    checkListBadges.append(badge[1])
    for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
        if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][0] and f'{customPlace}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlace}_Badges']:
                if badge[2]:
                    checkListBadges.append(badge[0])

def getGlobalCheckListCustomGamepasses(): global checkListCustomGamepasses; checkListCustomGamepasses = [customGamepass[0] for customGamepass in config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'] if customGamepass[1]]
def getGlobalCheckListFavoritePlaces():   global checkListFavoritePlaces;   checkListFavoritePlaces   = [favoritePlace[0]  for favoritePlace  in config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs']     if favoritePlace[2]]
def getGlobalCheckListBundles():          global checkListBundles;          checkListBundles          = [bundle[0]         for bundle         in config['Roblox']['CookieChecker']['Main']['Bundles_IDs']             if bundle[2]]

async def isResponseStatusFromCookie(cookieRoblox: dict | None, headersRoblox: dict | None, proxies: list) -> int:
    while True:
        try:
            session = ClientSession(connector=await getConnector(proxies), cookies=cookieRoblox, headers=headersRoblox)
            response = await session.get(f'https://users.roblox.com/v1/users/authenticated', timeout=3, ssl=False)
            if response.status == 429:
                await asyncio.sleep(int(response.headers.get('x-ratelimit-reset', 10)))
                continue
            await session.close()
            return response.status
        except (ContentTypeError):
            # sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Could_Not_Connect_To_The_API}. {MT_Trying_To_Connect_Again}... :<{ANSI.CLEAR}\n')
            await asyncio.sleep(0.5) # default: 2 seconds
            # await removeLines(1)
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            pass
        finally:
            await session.close()

async def isResponseDataFromCookie(cookieRoblox: dict | None, headersRoblox: dict | None, sendRequestsThrough: str, proxies: list = None, isControlPanel: bool = False):
    responseStatus = await isResponseStatusFromCookie(cookieRoblox, headersRoblox, proxies)
    if responseStatus != 200:
        return responseStatus, None, None

    session = ClientSession(connector=await getConnector(proxies), cookies=cookieRoblox, headers=headersRoblox)
    
    while True:
        try:
            responseAccountInfo = await session.get(f'https://www.roblox.com/my/settings/json', timeout=3, ssl=False)
            isAccountInformation = await responseAccountInfo.json()
            isID = isAccountInformation['UserId']
            break
        except ContentTypeError:
            await asyncio.sleep(2)
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            await session.close()
            session = ClientSession(connector=await getConnector(proxies), cookies=cookieRoblox, headers=headersRoblox)

    while True:
        try:
            responseAllData = await asyncio.gather(*(
                isLinkFunc(                        isID,                                            isControlPanel),
                isCountryRegistrationFunc(session,                             sendRequestsThrough, isControlPanel),
                isNameFunc(                              isAccountInformation,                      isControlPanel),
                isDisplayNameFunc(                       isAccountInformation,                      isControlPanel),
                isRegistrationDateFunc(   session, isID, isAccountInformation, sendRequestsThrough, isControlPanel),
                isRobuxFunc(              session, isID,                       sendRequestsThrough, isControlPanel),
                isBillingFunc(            session,                                                  isControlPanel),
                isTransactionsForYearFunc(session, isID,                       sendRequestsThrough, isControlPanel),
                isPurchasesFunc(          session, isID,                       sendRequestsThrough, isControlPanel),
                isRapFunc(                session, isID,                                            isControlPanel),
                isCardFunc(               session,                                                  isControlPanel),
                isPremiumFunc(                           isAccountInformation,                      isControlPanel),
                isGamepassesFunc(         session, isID,                                            isControlPanel),
                isBadgesFunc(             session, isID,                                            isControlPanel),
                isFavoritePlacesFunc(     session, isID,                                            isControlPanel),
                isBundlesFunc(            session, isID,                                            isControlPanel),
                isInventoryPrivacyFunc(   session,                                                  isControlPanel),
                isTradePrivacyFunc(       session,                                                  isControlPanel),
                isCanTradeFunc(                          isAccountInformation,                      isControlPanel),
                isSessionsFunc(           session,                                                  isControlPanel),
                isEmailFunc(                             isAccountInformation,                      isControlPanel),
                isPhoneFunc(              session,                                                  isControlPanel),
                is2FAFunc(                               isAccountInformation,                      isControlPanel),
                isPinFunc(                               isAccountInformation,                      isControlPanel),
                isAbove13Func(                           isAccountInformation,                      isControlPanel),
                isVerifiedAgeFunc(        session,                                                  isControlPanel),
                isVoiceFunc(              session,                                                  isControlPanel),
                isNumberOfFriendsFunc(    session, isID,                                            isControlPanel),
                isNumberOfFollowersFunc(  session, isID,                                            isControlPanel),
                isNumberOfFollowingsFunc( session, isID,                                            isControlPanel),
                isRobloxBadgesFunc(       session, isID,                                            isControlPanel),
                isXCSRFTokenFunc(         session,                                                  isControlPanel)
            ))
            await session.close()
            return responseStatus, isID, responseAllData
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            await session.close()
            session = ClientSession(connector=await getConnector(proxies), cookies=cookieRoblox, headers=headersRoblox)

async def getConnector(proxies: list = None):
    if config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy'] and proxies:
        choosenProxy = str(random.choice(proxies))
        if '://' not in choosenProxy: choosenProxy = f'{config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] if config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] in ('http', 'socks4', 'socks5') else 'http'}://{choosenProxy}'
        elif 'https' in choosenProxy: choosenProxy = choosenProxy.replace('https', 'http')
        return ProxyConnector.from_url(choosenProxy)
    return TCPConnector(ssl=False)

async def robloxCookieChecker(file):
    if not [data[1] for data in cookieData.listOfCookieData if config['Roblox']['CookieChecker']['Main'][data[1]]]:
        return await errorOrCorrectHandler(True, 8, MT_Enable_Something_To_Start_Checking, f'{MT_Roblox}\\{MT_Cookie_Checker} {ANSI.FG.RED}{MT_Beta}{ANSI.CLEAR + ANSI.DECOR.BOLD}')

    if config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy']:
        proxiesFromFile = list({proxy.strip() for proxy in open('Roblox\\Cookie Checker\\proxies.txt', 'r', encoding='UTF-8').readlines()
                                if '@' in proxy and len(proxy.split(':')) in (3, 4)})
        if not proxiesFromFile:
            return await errorOrCorrectHandler(True, 3, MT_No_Proxy_Was_Found, f'{MT_Roblox}\\{MT_Cookie_Checker} {ANSI.FG.RED}{MT_Beta}{ANSI.CLEAR + ANSI.DECOR.BOLD}')

    await removeLines(7)
    sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}{file}.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')

    dateOfCheck = datetime.datetime.now().strftime('%d.%m.%Y - %H.%M.%S')
    timedCookiesFromFile = {cookie.strip() for cookie in open('Roblox\\Cookie Checker\\cookies.txt', 'r', encoding='UTF-8').readlines()}
    checkReadyRobloxCookies = []
    locker = asyncio.Lock()

    # Валид чекер
    if config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid']:
        totalWord = ''.join(MT_Total).lower().capitalize()
        validCount = invalidCount = 0
        amountOfCookiesFromFile = len(timedCookiesFromFile)
        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_First_We_Check_For_Valid}: {ANSI.FG.GREEN}{MT_Valid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: 0, {ANSI.FG.RED}{MT_Invalid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: 0 | {ANSI.FG.CYAN}{totalWord}{ANSI.CLEAR + ANSI.DECOR.BOLD}: 0 {MT_Of} {amountOfCookiesFromFile}{ANSI.CLEAR}')

        semaphore = asyncio.Semaphore(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']) <= 500) else 5)

        async def threadingCheckValid(cookie: str, proxies: list):
            nonlocal validCount, invalidCount
            async with semaphore:
                cookie = cookie.strip()
                headersRoblox = None # {'User-Agent': ua.random}
                cookieRoblox = {'.ROBLOSECURITY': cookie}

                isResponseStatus = await isResponseStatusFromCookie(cookieRoblox, headersRoblox, proxies)

                async with locker:
                    if isResponseStatus == 200:
                        checkReadyRobloxCookies.append(cookie)
                        validCount += 1
                    else:
                        invalidCount += 1

                    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_First_We_Check_For_Valid}: {ANSI.FG.GREEN}{MT_Valid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: {validCount}, {ANSI.FG.RED}{MT_Invalid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: {invalidCount} | {ANSI.FG.CYAN}{totalWord}{ANSI.CLEAR + ANSI.DECOR.BOLD}: {validCount + invalidCount} {MT_Of} {amountOfCookiesFromFile}{ANSI.CLEAR}')
                    sys.stdout.flush()

        validCheckTasks = [threadingCheckValid(cookie, proxiesFromFile if config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy'] else None) for cookie in timedCookiesFromFile]
        await asyncio.gather(*validCheckTasks)
        await removeLines(1)
    else:
        checkReadyRobloxCookies = {cookie for cookie in timedCookiesFromFile}

    async def totalOutputRCC():
        labelsTotalOutputRCC = [
            rf'   {ANSI.FG.GRAY}______________________________',
            rf'  {ANSI.FG.GRAY}/  | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Cookie:{           ANSI.CLEAR} {cookieCount} {MT_Of} {amountOfCookiesFromFile}',
            rf' {ANSI.FG.GRAY}/   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Valid:{            ANSI.CLEAR} {validCount}',
            rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Robux:{            ANSI.CLEAR} {totalData_CURRENT['Robux']}',
            rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Billing:{          ANSI.CLEAR} {totalData_CURRENT['Billing']}',
            rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Pending:{          ANSI.CLEAR} {totalData_CURRENT['Pending']}',
            rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[0] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Donate:{           ANSI.CLEAR} {totalData_CURRENT['Donate']}',
            rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[1] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Purchases:{        ANSI.CLEAR} {totalData_CURRENT['Purchases']}',
            rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[2] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Rap:{              ANSI.CLEAR} {totalData_CURRENT['Rap']}',
            rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[3] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Premium:{          ANSI.CLEAR} {totalData_CURRENT['Premium']}',
            rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[4] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Card:{             ANSI.CLEAR} {totalData_CURRENT['Card']}',
            rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Gamepasses:{       ANSI.CLEAR} {totalData_CURRENT['Gamepasses']}',
            rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Custom Gamepasses:{ANSI.CLEAR} {totalData_CURRENT['Custom Gamepasses']}',
            rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Badges:{           ANSI.CLEAR} {totalData_CURRENT['Badges']}',
            rf' {ANSI.FG.GRAY}\   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Favorite Places:{  ANSI.CLEAR} {totalData_CURRENT['Favorite Places']}',
            rf'  {ANSI.FG.GRAY}\  | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Bundles:{          ANSI.CLEAR} {totalData_CURRENT['Bundles']}',
            rf'   {ANSI.FG.GRAY}‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾{ANSI.CLEAR}'
        ]
        
        for label in labelsTotalOutputRCC:
            sys.stdout.write(f'{label}\n')
            sys.stdout.flush()

    if config['Roblox']['CookieChecker']['Main']['Gamepasses']:        getGlobalsCheckListGamepasses()
    if config['Roblox']['CookieChecker']['Main']['Badges']:            getGlobalsCheckListBadges()
    if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']: getGlobalCheckListCustomGamepasses()
    if config['Roblox']['CookieChecker']['Main']['Favorite_Places']:   getGlobalCheckListFavoritePlaces()
    if config['Roblox']['CookieChecker']['Main']['Bundles']:           getGlobalCheckListBundles()

    if config['Roblox']['CookieChecker']['Sorting']['Sort']:
        sortListCategories = {}
        categories = getCookieDataForSort()
        await removeDuplicatedSortValues(categories[1])
        for category in categories[0]:
            if categories[0][category] == int and config['Roblox']['CookieChecker']['Sorting'][category][0] or categories[0][category] == bool and config['Roblox']['CookieChecker']['Sorting'][category]:
                sortListCategories[category] = categories[0][category]
    
    sendRequestsThrough = 'roproxy' if config['Roblox']['CookieChecker']['General']['Send_Some_Requests_Through_RoProxy'] else 'roblox'

    cookieCount = validCount = 0
    amountOfCookiesFromFile = len(checkReadyRobloxCookies)
    semaphore = asyncio.Semaphore(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']) <= 500) else 5)

    if config['Roblox']['CookieChecker']['General']['Output_Total']:
        totalData_CURRENT = {
            'Robux'             : 0,
            'Billing'           : 0,
            'Pending'           : 0,
            'Donate'            : 0,
            'Purchases'         : 0,
            'Rap'               : 0,
            'Premium'           : 0,
            'Card'              : 0,
            'Gamepasses'        : 0,
            'Custom Gamepasses' : 0,
            'Badges'            : 0,
            'Favorite Places'   : 0,
            'Bundles'           : 0
        }

        for key in totalData_CURRENT:
            if not config['Roblox']['CookieChecker']['Main']['_'.join(key.split(' '))]:
                totalData_CURRENT[key] = f'{ANSI.FG.GRAY}Off{ANSI.CLEAR}'

    # Основной чекер
    async def threadingCheckData(cookie: str, proxies: list | None = None):
        nonlocal cookieCount, validCount
        async with semaphore:
            headersRoblox = None # {'User-Agent': ua.random}
            cookieRoblox = {'.ROBLOSECURITY': cookie}

            responseStatus, isID, resultsRCC = await isResponseDataFromCookie(cookieRoblox, headersRoblox, sendRequestsThrough, proxies)

            if responseStatus == 200:
                # Вывод данных
                isAccountLink,             isAccountLinkN                                                                                            = resultsRCC[0]
                isCountryRegistration,     isCountryRegistrationN,                             isCountryRegistrationSorting                          = resultsRCC[1]
                isName,                    isNameN,                   isNameClean                                                                    = resultsRCC[2]
                isDisplayName,             isDisplayNameN,            isDisplayNameClean                                                             = resultsRCC[3]
                isRegistrationDate,        isRegistrationDateN,       isRegistrationDateClean                                                        = resultsRCC[4][0], resultsRCC[4][1], resultsRCC[4][2]
                isRegistrationDateInDaysSorting                                                                                                      = resultsRCC[4][5]
                isRobux,                   isRobuxN,                                                                                    isRobuxTimed = resultsRCC[5]
                isBilling,                 isBillingN,                                                                                isBillingTimed = resultsRCC[6]
                isTransactionsForYear, isTransactionsForYearN, isPendingTimed, isDonateTimed                                                         = resultsRCC[7]
                isPurchases, isPurchasesN, isPurchasesTimed, isCustomGamepasses, isCustomGamepassesN, isCustomGamepassesTimed                        = resultsRCC[8]
                isRap,                     isRapN,                                                                                        isRapTimed = resultsRCC[9]
                isCard,                    isCardN,                                                                                      isCardTimed = resultsRCC[10]
                isPremium,                 isPremiumN,                                         isPremiumSorting,                      isPremiumTimed = resultsRCC[11]
                isGamepasses,              isGamepassesN,                                                                          isGamepassesTimed = resultsRCC[12]
                isBadges,                  isBadgesN,                                                                                  isBadgesTimed = resultsRCC[13]
                isFavoritePlaces,          isFavoritePlacesN,                                                                  isFavoritePlacesTimed = resultsRCC[14]
                isBundles,                 isBundlesN,                                                                                isBundlesTimed = resultsRCC[15]
                isInventoryPrivacy,        isInventoryPrivacyN,       isInventoryPrivacyClean                                                        = resultsRCC[16]
                isTradePrivacy,            isTradePrivacyN,           isTradePrivacyClean                                                            = resultsRCC[17]
                isCanTrade,                isCanTradeN,               isCanTradeClean                                                                = resultsRCC[18]
                isSessions,                isSessionsN,                                        isSessionsSorting                                     = resultsRCC[19]
                isEmail,                   isEmailN,                                           isEmailSorting                                        = resultsRCC[20]
                isPhone,                   isPhoneN,                                           isPhoneSorting                                        = resultsRCC[21]
                is2FA,                     is2FAN,                                             is2FASorting                                          = resultsRCC[22]
                isPin,                     isPinN,                                             isPinSorting                                          = resultsRCC[23]
                isAbove13,                 isAbove13N,                                         isAbove13Sorting                                      = resultsRCC[24]
                isVerifiedAge,             isVerifiedAgeN,                                     isVerifiedAgeSorting                                  = resultsRCC[25]
                isVoice,                   isVoiceN,                                           isVoiceSorting                                        = resultsRCC[26]
                isNumberOfFriends,         isNumberOfFriendsN,                                 isNumberOfFriendsSorting                              = resultsRCC[27]
                isNumberOfFollowers,       isNumberOfFollowersN,                               isNumberOfFollowersSorting                            = resultsRCC[28]
                isNumberOfFollowings,      isNumberOfFollowingsN,                              isNumberOfFollowingsSorting                           = resultsRCC[29]
                isRobloxBadges,            isRobloxBadgesN,           isRobloxBadgesClean                                                            = resultsRCC[30]
                isXCSRFToken,              isXCSRFTokenN,             isXCSRFTokenClean                                                              = resultsRCC[31]
                # Всё, что сверху, переменные для вывода, в планах поменять их просто на resultRCC[index][index]

                # Обновление данных общего вывода
                if config['Roblox']['CookieChecker']['General']['Output_Total']:
                    totalData_UPDATE = {
                        'Robux'             : isRobuxTimed,
                        'Billing'           : isBillingTimed,
                        'Pending'           : isPendingTimed,
                        'Donate'            : isDonateTimed,
                        'Purchases'         : isPurchasesTimed,
                        'Custom Gamepasses' : isCustomGamepassesTimed,
                        'Rap'               : isRapTimed,
                        'Card'              : isCardTimed,
                        'Premium'           : isPremiumTimed,
                        'Gamepasses'        : isGamepassesTimed,
                        'Badges'            : isBadgesTimed,
                        'Favorite Places'   : isFavoritePlacesTimed,
                        'Bundles'           : isBundlesTimed
                    }

                    for key, value in totalData_UPDATE.items():
                        if isinstance(totalData_CURRENT[key], int): totalData_CURRENT[key] += int(value)

                async def isSortingCookiesFunc(category: str, value: int | str, dateOfCheck: str):
                    newNameOfCategory = ' '.join(category.split('_'))
                    if type(value) == int and str(value) != '0':
                        sortValues = await getSortValuesFromCategory(category)
                        if not sortValues: return

                        os.makedirs(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{newNameOfCategory}', exist_ok=True)
                        for sortValue in sortValues:
                            if value >= sortValue:
                                async with aiofiles.open(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{newNameOfCategory}\\{sortValue}+.txt', 'a', encoding='UTF-8') as file:
                                    await file.write(f'{isAccountLinkN}{isCountryRegistrationN}{f'ID: {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isNameN}{isDisplayNameN}{isRegistrationDateN}{isRobuxN}{isBillingN}{isTransactionsForYearN}{isPurchasesN}{isRapN}{isCardN}{isPremiumN}{isGamepassesN}{isCustomGamepassesN}{isBadgesN}{isFavoritePlacesN}{isBundlesN}{isInventoryPrivacyN}{isTradePrivacyN}{isCanTradeN}{isSessionsN}{isEmailN}{isPhoneN}{is2FAN}{isPinN}{isAbove13N}{isVerifiedAgeN}{isVoiceN}{isNumberOfFriendsN}{isNumberOfFollowersN}{isNumberOfFollowingsN}{isRobloxBadgesN}{isXCSRFTokenN}Cookie: {cookie}\n')
                    elif type(value) == str:
                        os.makedirs(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{newNameOfCategory}', exist_ok=True)
                        async with aiofiles.open(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{newNameOfCategory}\\{value}.txt', 'a', encoding='UTF-8') as file:
                            await file.write(f'{isAccountLinkN}{isCountryRegistrationN}{f'ID: {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isNameN}{isDisplayNameN}{isRegistrationDateN}{isRobuxN}{isBillingN}{isTransactionsForYearN}{isPurchasesN}{isRapN}{isCardN}{isPremiumN}{isGamepassesN}{isCustomGamepassesN}{isBadgesN}{isFavoritePlacesN}{isBundlesN}{isInventoryPrivacyN}{isTradePrivacyN}{isCanTradeN}{isSessionsN}{isEmailN}{isPhoneN}{is2FAN}{isPinN}{isAbove13N}{isVerifiedAgeN}{isVoiceN}{isNumberOfFriendsN}{isNumberOfFollowersN}{isNumberOfFollowingsN}{isRobloxBadgesN}{isXCSRFTokenN}Cookie: {cookie}\n')

                # Сортировка
                if config['Roblox']['CookieChecker']['Sorting']['Sort']:
                    if config['Roblox']['CookieChecker']['Sorting']['Country_Registration']          and config['Roblox']['CookieChecker']['Main']['Country_Registration']:       await isSortingCookiesFunc('Country_Registration',       isCountryRegistrationSorting,    dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['ID']                            and config['Roblox']['CookieChecker']['Main']['ID']:                         await isSortingCookiesFunc('ID',                         str(isID),                       dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Name']                          and config['Roblox']['CookieChecker']['Main']['Name']:                       await isSortingCookiesFunc('Name',                       isNameClean,                     dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Extended_Registration_Date'][0] and config['Roblox']['CookieChecker']['Main']['Extended_Registration_Date']: await isSortingCookiesFunc('Extended_Registration_Date', isRegistrationDateInDaysSorting, dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Robux'][0]                      and config['Roblox']['CookieChecker']['Main']['Robux']:                      await isSortingCookiesFunc('Robux',                      isRobuxTimed,                    dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Billing'][0]                    and config['Roblox']['CookieChecker']['Main']['Billing']:                    await isSortingCookiesFunc('Billing',                    isBillingTimed,                  dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Pending'][0]                    and config['Roblox']['CookieChecker']['Main']['Pending']:                    await isSortingCookiesFunc('Pending',                    isPendingTimed,                  dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Donate'][0]                     and config['Roblox']['CookieChecker']['Main']['Donate']:                     await isSortingCookiesFunc('Donate',                     isDonateTimed,                   dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Purchases'][0]                  and config['Roblox']['CookieChecker']['Main']['Purchases']:                  await isSortingCookiesFunc('Purchases',                  isPurchasesTimed,                dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Rap'][0]                        and config['Roblox']['CookieChecker']['Main']['Rap']:                        await isSortingCookiesFunc('Rap',                        isRapTimed,                      dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Card']                          and config['Roblox']['CookieChecker']['Main']['Card']:                       await isSortingCookiesFunc('Card',                       isCardTimed,                     dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Premium']                       and config['Roblox']['CookieChecker']['Main']['Premium']:                    await isSortingCookiesFunc('Premium',                    isPremiumSorting,                dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Gamepasses'][0]                 and config['Roblox']['CookieChecker']['Main']['Gamepasses']:                 await isSortingCookiesFunc('Gamepasses',                 isGamepassesTimed,               dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Custom_Gamepasses'][0]          and config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']:          await isSortingCookiesFunc('Custom_Gamepasses',          isCustomGamepassesTimed,         dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Badges'][0]                     and config['Roblox']['CookieChecker']['Main']['Badges']:                     await isSortingCookiesFunc('Badges',                     isBadgesTimed,                   dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Favorite_Places'][0]            and config['Roblox']['CookieChecker']['Main']['Favorite_Places']:            await isSortingCookiesFunc('Favorite_Places',            isFavoritePlacesTimed,           dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Bundles'][0]                    and config['Roblox']['CookieChecker']['Main']['Bundles']:                    await isSortingCookiesFunc('Bundles',                    isBundlesTimed,                  dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Inventory_Privacy']             and config['Roblox']['CookieChecker']['Main']['Inventory_Privacy']:          await isSortingCookiesFunc('Inventory_Privacy',          isInventoryPrivacyClean,         dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Trade_Privacy']                 and config['Roblox']['CookieChecker']['Main']['Trade_Privacy']:              await isSortingCookiesFunc('Trade_Privacy',              isTradePrivacyClean,             dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Can_Trade']                     and config['Roblox']['CookieChecker']['Main']['Can_Trade']:                  await isSortingCookiesFunc('Can_Trade',                  isCanTradeClean,                 dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Sessions'][0]                   and config['Roblox']['CookieChecker']['Main']['Sessions']:                   await isSortingCookiesFunc('Sessions',                   isSessionsSorting,               dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Email']                         and config['Roblox']['CookieChecker']['Main']['Email']:                      await isSortingCookiesFunc('Email',                      isEmailSorting,                  dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Phone']                         and config['Roblox']['CookieChecker']['Main']['Phone']:                      await isSortingCookiesFunc('Phone',                      isPhoneSorting,                  dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['2FA']                           and config['Roblox']['CookieChecker']['Main']['2FA']:                        await isSortingCookiesFunc('2FA',                        is2FASorting,                    dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Pin']                           and config['Roblox']['CookieChecker']['Main']['Pin']:                        await isSortingCookiesFunc('Pin',                        isPinSorting,                    dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Above_13']                      and config['Roblox']['CookieChecker']['Main']['Above_13']:                   await isSortingCookiesFunc('Above_13',                   isAbove13Sorting,                dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Verified_Age']                  and config['Roblox']['CookieChecker']['Main']['Verified_Age']:               await isSortingCookiesFunc('Verified_Age',               isVerifiedAgeSorting,            dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Voice']                         and config['Roblox']['CookieChecker']['Main']['Voice']:                      await isSortingCookiesFunc('Voice',                      isVoiceSorting,                  dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Friends'][0]                    and config['Roblox']['CookieChecker']['Main']['Friends']:                    await isSortingCookiesFunc('Friends',                    isNumberOfFriendsSorting,        dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Followers'][0]                  and config['Roblox']['CookieChecker']['Main']['Followers']:                  await isSortingCookiesFunc('Followers',                  isNumberOfFollowersSorting,      dateOfCheck)
                    if config['Roblox']['CookieChecker']['Sorting']['Followings'][0]                 and config['Roblox']['CookieChecker']['Main']['Followings']:                 await isSortingCookiesFunc('Followings',                 isNumberOfFollowingsSorting,     dateOfCheck)

                if config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker']:
                    config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory'][f'{cookie[115:125]}...{cookie[-10:-1]}'] = [isCountryRegistrationSorting if isCountryRegistrationSorting != '' else None, isID if config['Roblox']['CookieChecker']['Main']['ID'] else None, isNameClean if isNameClean != '' else None, isDisplayNameClean if isDisplayNameClean != '' else None, isRegistrationDateClean if isRegistrationDateClean != '' else None, isRegistrationDateInDaysSorting if isRegistrationDateInDaysSorting != '' else None, isRobuxTimed if isRobuxTimed != '' else None, isBillingTimed if isBillingTimed != '' else None, isPendingTimed if config['Roblox']['CookieChecker']['Main']['Pending'] else None, isDonateTimed if config['Roblox']['CookieChecker']['Main']['Donate'] else None, isPurchasesTimed if isPurchasesTimed != '' else None, isCustomGamepassesTimed if isCustomGamepassesTimed != '' else None, isRapTimed if isRapTimed != '' else None, isCardTimed if isCardTimed != '' else None, isPremiumSorting if isPremiumSorting != '' else None, isGamepassesTimed if isGamepassesTimed != '' else None, isBadgesTimed if isBadgesTimed != '' else None, isFavoritePlacesTimed if isFavoritePlacesTimed != '' else None, isBundlesTimed if isBundlesTimed != '' else None, isInventoryPrivacyClean if isInventoryPrivacyClean != '' else None, isTradePrivacyClean if isTradePrivacyClean != '' else None, isCanTradeClean if isCanTradeClean != '' else None, isSessionsSorting if isSessionsSorting != '' else None, isEmailSorting if isEmailSorting != '' else None, isPhoneSorting if isPhoneSorting != '' else None, is2FASorting if is2FASorting != '' else None, isPinSorting if isPinSorting != '' else None, isAbove13Sorting if isAbove13Sorting != '' else None, isVerifiedAgeSorting if isVerifiedAgeSorting != '' else None, isVoiceSorting if isVoiceSorting != '' else None, isNumberOfFriendsSorting if isNumberOfFriendsSorting != '' else None, isNumberOfFollowersSorting if isNumberOfFollowersSorting != '' else None, isNumberOfFollowingsSorting if isNumberOfFollowingsSorting != '' else None, isRobloxBadgesClean if isRobloxBadgesClean != '' else None, isXCSRFTokenClean if isXCSRFTokenClean != '' else None, cookie]
                    await AutoSaveConfig()

                async with locker: # fix_it_3
                    os.makedirs(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}', exist_ok=True)
                    async with aiofiles.open(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\outputs.txt', 'a', encoding='UTF-8') as file:
                        await file.write(f'{isAccountLinkN}{isCountryRegistrationN}{f'ID: {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isNameN}{isDisplayNameN}{isRegistrationDateN}{isRobuxN}{isBillingN}{isTransactionsForYearN}{isPurchasesN}{isRapN}{isCardN}{isPremiumN}{isGamepassesN}{isCustomGamepassesN}{isBadgesN}{isFavoritePlacesN}{isBundlesN}{isInventoryPrivacyN}{isTradePrivacyN}{isCanTradeN}{isSessionsN}{isEmailN}{isPhoneN}{is2FAN}{isPinN}{isAbove13N}{isVerifiedAgeN}{isVoiceN}{isNumberOfFriendsN}{isNumberOfFollowersN}{isNumberOfFollowingsN}{isRobloxBadgesN}{isXCSRFTokenN}Cookie: {cookie}\n')
                    validCount += 1
                    if config['Roblox']['CookieChecker']['General']['Output_Total'] and cookieCount: await removeLines(17)
                    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}]{ANSI.CLEAR} {isAccountLink}{isCountryRegistration}{f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}ID:{ANSI.CLEAR} {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isName}{isDisplayName}{isRegistrationDate}{isRobux}{isBilling}{isTransactionsForYear}{isPurchases}{isRap}{isCard}{isPremium}{isGamepasses}{isCustomGamepasses}{isBadges}{isFavoritePlaces}{isBundles}{isInventoryPrivacy}{isTradePrivacy}{isCanTrade}{isSessions}{isEmail}{isPhone}{is2FA}{isPin}{isAbove13}{isVerifiedAge}{isVoice}{isNumberOfFriends}{isNumberOfFollowers}{isNumberOfFollowings}{isRobloxBadges}{isXCSRFToken}{f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Cookie: {ANSI.FG.YELLOW}{cookie}{ANSI.CLEAR}' if config['Roblox']['CookieChecker']['Main']['Cookie_In_Console'] else ''}\n')
            else:
                async with locker: # fix_it_3
                    if config['Roblox']['CookieChecker']['General']['Output_Total'] and cookieCount: await removeLines(17)
                    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Invalid_Cookie}{ANSI.CLEAR}\n')

            sys.stdout.flush()
            cookieCount += 1
            if config['Roblox']['CookieChecker']['General']['Output_Total']: await totalOutputRCC()

    dataCheckTasks = [threadingCheckData(cookie, proxiesFromFile if config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy'] else None) for cookie in checkReadyRobloxCookies]
    await asyncio.gather(*dataCheckTasks)

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Finish_Checking_File}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
    await waitingInput()

def printRCCGeneral():
    for index, data in enumerate(cookieData.listOfCookieData):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(cookieData.listOfCookieData))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Main'][data[1]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {data[0]}{f'{ANSI.CLEAR + data[2]}*{ANSI.CLEAR}'}\n')

def RCCGeneralCustomGamepasses(printCustomGamepasses=False) -> list:
    noDuplicatedCustomGamepasses = []
    noDuplicatedCustomGamepasses = [customGamepass for customGamepass in config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names']
                                    if len(str(customGamepass)) <= 100 and customGamepass not in noDuplicatedCustomGamepasses]
    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'] = noDuplicatedCustomGamepasses

    if printCustomGamepasses:
        for index, customGamepass in enumerate(noDuplicatedCustomGamepasses):
            sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(noDuplicatedCustomGamepasses))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if customGamepass[1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {customGamepass[0]}\n')
    return noDuplicatedCustomGamepasses

def RCCGeneralFavPlaces(printFavoritePlaces=False) -> list:
    noDuplicatedFavoritePlaces = []
    noDuplicatedFavoritePlaces = [favplace for favplace in config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs']
                            if str(favplace[0]).isdigit() and len(str(favplace[0])) <= 20 and favplace[0] not in noDuplicatedFavoritePlaces]
    config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'] = noDuplicatedFavoritePlaces

    if printFavoritePlaces:
        for index, favplace in enumerate(noDuplicatedFavoritePlaces):
            sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(noDuplicatedFavoritePlaces))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if favplace[2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {favplace[0]} ({favplace[1]})\n')
    return noDuplicatedFavoritePlaces

def RCCGeneralBundles(printBundles=False) -> list:
    noDuplicatedBundles = []
    noDuplicatedBundles = [bundle for bundle in config['Roblox']['CookieChecker']['Main']['Bundles_IDs']
                           if str(bundle[0]).isdigit() and len(str(bundle[0])) <= 20 and bundle[0] not in noDuplicatedBundles]
    config['Roblox']['CookieChecker']['Main']['Bundles_IDs'] = noDuplicatedBundles

    if printBundles:
        for index, bundle in enumerate(noDuplicatedBundles):
            sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(noDuplicatedBundles))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if bundle[2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {bundle[0]} ({bundle[1]})\n')
    return noDuplicatedBundles

def checkDuplicates(input, listIDs):
    listIDs = [id[0] for id in config['Roblox']['CookieChecker']['Main'][listIDs]]
    if input in listIDs:
        return True

def printRCCPlaces():
    for index, place in enumerate(listOfPlaces):
        sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfPlaces))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {place.placeNames[0]}\n')

async def placeContextMenu(indexPlace: int):
    async def removeLinesGamepassesAndOrBadges():
        if getattr(listOfPlaces[indexPlace], 'Gamepasses', False) and getattr(listOfPlaces[indexPlace], 'Badges', False):
            await removeLines(9)
        else:
            await removeLines(8)

    async def printPlaceGamepasses():
        for index, gamepass in enumerate(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {gamepass[0]}{ANSI.CLEAR}\n')
    
    async def openPlaceGamepasses():
        whileTrueStage5 = True
        await removeLinesGamepassesAndOrBadges()
        while whileTrueStage5:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}\\{listOfPlaces[indexPlace].placeNames[0]}\\{MT_Gamepasses}{ANSI.CLEAR}\n\n')
            await printPlaceGamepasses()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCPlacesPlaceGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCPlacesPlaceGamepassesTab == '0': whileTrueStage5 = False
            elif settingsRCCPlacesPlaceGamepassesTab.isdigit() and int(settingsRCCPlacesPlaceGamepassesTab) <= len(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses):
                config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Gamepasses.listOfGamepasses[int(settingsRCCPlacesPlaceGamepassesTab) - 1][2]] = not config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Gamepasses.listOfGamepasses[int(settingsRCCPlacesPlaceGamepassesTab) - 1][2]]
                await AutoSaveConfig()
            elif settingsRCCPlacesPlaceGamepassesTab in ('+', '='):
                for gamepass in listOfPlaces[indexPlace].Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] = True
                await AutoSaveConfig()
            elif settingsRCCPlacesPlaceGamepassesTab in ('-', '_'):
                for gamepass in listOfPlaces[indexPlace].Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] = False
                await AutoSaveConfig()
            elif settingsRCCPlacesPlaceGamepassesTab.upper() in ('R', 'К'):
                loadConfig(configLoader['Loader']['Current_Config'])

            await cls()
            await lableASCII()

    async def printPlaceBadges():
        for index, badge in enumerate(listOfPlaces[indexPlace].Badges.listOfBadges):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfPlaces[indexPlace].Badges.listOfBadges))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {badge[0]}{ANSI.CLEAR}\n')
    
    async def openPlaceBadges():
        whileTrueStage5 = True
        await removeLinesGamepassesAndOrBadges()
        while whileTrueStage5:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}\\{listOfPlaces[indexPlace].placeNames[0]}\\{MT_Badges}{ANSI.CLEAR}\n\n')
            await printPlaceBadges()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCPlacesPlaceBadgesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCPlacesPlaceBadgesTab == '0': whileTrueStage5 = False
            elif settingsRCCPlacesPlaceBadgesTab.isdigit() and int(settingsRCCPlacesPlaceBadgesTab) <= len(listOfPlaces[indexPlace].Badges.listOfBadges):
                config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Badges.listOfBadges[int(settingsRCCPlacesPlaceBadgesTab) - 1][2]] = not config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Badges.listOfBadges[int(settingsRCCPlacesPlaceBadgesTab) - 1][2]]
                await AutoSaveConfig()
            elif settingsRCCPlacesPlaceBadgesTab in ('+', '='):
                for badge in listOfPlaces[indexPlace].Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] = True
                await AutoSaveConfig()
            elif settingsRCCPlacesPlaceBadgesTab in ('-', '_'):
                for badge in listOfPlaces[indexPlace].Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] = False
                await AutoSaveConfig()
            elif settingsRCCPlacesPlaceBadgesTab.upper() in ('R', 'К'):
                loadConfig(configLoader['Loader']['Current_Config'])

            await cls()
            await lableASCII()
    
    whileTrueStage4 = True
    await cls()
    await lableASCII()
    while whileTrueStage4:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}\\{listOfPlaces[indexPlace].placeNames[0]}{ANSI.CLEAR}\n\n')
        
        if   getattr(listOfPlaces[indexPlace], 'Gamepasses', False) and getattr(listOfPlaces[indexPlace], 'Badges', False):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges}{ANSI.CLEAR}\n')
        elif getattr(listOfPlaces[indexPlace], 'Gamepasses', False):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses}{ANSI.CLEAR}\n')
        elif getattr(listOfPlaces[indexPlace], 'Badges', False):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges}{ANSI.CLEAR}\n')

        sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Places'][listOfPlaces[indexPlace].placeNames[1]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        settingsRCCPlacesPlaceTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match settingsRCCPlacesPlaceTab.upper():
            case '1':
                if getattr(listOfPlaces[indexPlace], 'Gamepasses', False): await openPlaceGamepasses()
                else: await openPlaceBadges()
            case '2':
                if getattr(listOfPlaces[indexPlace], 'Badges', False) and getattr(listOfPlaces[indexPlace], 'Gamepasses', False): await openPlaceBadges()
                else: await removeLinesGamepassesAndOrBadges()
            case 'C' | 'С':
                config['Roblox']['CookieChecker']['Places'][listOfPlaces[indexPlace].placeNames[1]] = not config['Roblox']['CookieChecker']['Places'][listOfPlaces[indexPlace].placeNames[1]]
                await AutoSaveConfig()
                await removeLinesGamepassesAndOrBadges()
            case '0':
                whileTrueStage4 = False
                await removeLinesGamepassesAndOrBadges()
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case _:
                await removeLinesGamepassesAndOrBadges()

async def printRCCCustomPlaces():
    if config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
        listOfCustomPlacesPrint = []
        placeCounter = 0
        while placeCounter < len(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']):
            if str(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'][placeCounter]).isdigit() and str(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'][placeCounter]) in config['Roblox']['CookieChecker']['CustomPlaces'] and config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'][placeCounter] not in listOfCustomPlacesPrint:
                listOfCustomPlacesPrint.append(str(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'][placeCounter]))
                placeCounter += 1
            else:
                config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'][placeCounter])
        await AutoSaveConfig()
        for index, customPlace in enumerate(listOfCustomPlacesPrint):
            sys.stdout.write(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfCustomPlacesPrint))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['CustomPlaces'][customPlace][0] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {config['Roblox']['CookieChecker']['CustomPlaces'][customPlace][2][0] if config['Roblox']['CookieChecker']['CustomPlaces'][customPlace][2][0] != f'Unknown_Normal_{customPlace}' else config['Roblox']['CookieChecker']['CustomPlaces'][customPlace][2][1] if config['Roblox']['CookieChecker']['CustomPlaces'][customPlace][2][1] != f'Unknown_Default_{customPlace}' else f'Unknown_{customPlace}'} {f'({config['Roblox']['CookieChecker']['CustomPlaces'][customPlace][1]})' if config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] else ''}\n')

async def customPlaceContextMenu(indexPlace: int):
    listOfCustomPlacesTimed = [str(customPlace) for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']
                               if str(customPlace).isdigit() and str(customPlace) in config['Roblox']['CookieChecker']['CustomPlaces']]
    
    async def removeLinesCustomPlaces():
        if f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfCustomPlacesTimed[indexPlace]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            await removeLines(10)
        else:
            await removeLines(9)

    async def printCustomPlaceGamepasses():
        for index, gamepass in enumerate(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses']):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses']))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if gamepass[2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {gamepass[1]}{ANSI.CLEAR}\n')
    
    async def openCustomPlaceGamepasses():
        whileTrueStage5 = True
        await removeLinesCustomPlaces()
        while whileTrueStage5:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0] != f'Unknown_Normal_{listOfCustomPlacesTimed[indexPlace]}' else config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][1] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][1] != f'Unknown_Default_{listOfCustomPlacesTimed[indexPlace]}' else f'Unknown_{listOfCustomPlacesTimed[indexPlace]}'}\\{MT_Gamepasses}{ANSI.CLEAR}\n\n')
            await printCustomPlaceGamepasses()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCCustomPlacesPlaceGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCCustomPlacesPlaceGamepassesTab == '0': whileTrueStage5 = False
            elif settingsRCCCustomPlacesPlaceGamepassesTab.isdigit() and int(settingsRCCCustomPlacesPlaceGamepassesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses']):
                config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses'][int(settingsRCCCustomPlacesPlaceGamepassesTab) - 1][2] = not config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses'][int(settingsRCCCustomPlacesPlaceGamepassesTab) - 1][2]
                await AutoSaveConfig()
            elif settingsRCCCustomPlacesPlaceGamepassesTab in ('+', '='):
                for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses']:
                    config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses'][config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses'].index(gamepass)][2] = True
                await AutoSaveConfig()
            elif settingsRCCCustomPlacesPlaceGamepassesTab in ('-', '_'):
                for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses']:
                    config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses'][config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses'].index(gamepass)][2] = False
                await AutoSaveConfig()

            await cls()
            await lableASCII()

    async def printCustomPlaceBadges():
        for index, badge in enumerate(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges']):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges']))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if badge[2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {badge[1]}{ANSI.CLEAR}\n')
    
    async def openCustomPlaceBadges():
        whileTrueStage5 = True
        await removeLinesCustomPlaces()
        while whileTrueStage5:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0]}\\{MT_Badges}{ANSI.CLEAR}\n\n')
            await printCustomPlaceBadges()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCCustomPlacesPlaceBadgesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCCustomPlacesPlaceBadgesTab == '0': whileTrueStage5 = False
            elif settingsRCCCustomPlacesPlaceBadgesTab.isdigit() and int(settingsRCCCustomPlacesPlaceBadgesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges']):
                config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges'][int(settingsRCCCustomPlacesPlaceBadgesTab) - 1][2] = not config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges'][int(settingsRCCCustomPlacesPlaceBadgesTab) - 1][2]
                await AutoSaveConfig()
            elif settingsRCCCustomPlacesPlaceBadgesTab in ('+', '='):
                for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges']:
                    config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges'][config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges'].index(badge)][2] = True
                await AutoSaveConfig()
            elif settingsRCCCustomPlacesPlaceBadgesTab in ('-', '_'):
                for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges']:
                    config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges'][config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfCustomPlacesTimed[indexPlace]}_Badges'].index(badge)][2] = False
                await AutoSaveConfig()

            await cls()
            await lableASCII()
    
    whileTrueStage4 = True
    await cls()
    await lableASCII()
    while whileTrueStage4:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0] != f'Unknown_Normal_{listOfCustomPlacesTimed[indexPlace]}' else config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][1] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][1] != f'Unknown_Default_{listOfCustomPlacesTimed[indexPlace]}' else f'Unknown_{listOfCustomPlacesTimed[indexPlace]}'}{ANSI.CLEAR}\n\n')
        
        if f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfCustomPlacesTimed[indexPlace]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges}{ANSI.CLEAR}\n')
        elif f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses}{ANSI.CLEAR}\n')
        elif f'{listOfCustomPlacesTimed[indexPlace]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges}{ANSI.CLEAR}\n')

        sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][0] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        settingsRCCPlacesPlaceTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match settingsRCCPlacesPlaceTab.upper():
            case '1':
                if f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']: await openCustomPlaceGamepasses()
                else: await openCustomPlaceBadges()
            case '2':
                if f'{listOfCustomPlacesTimed[indexPlace]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']: await openCustomPlaceBadges()
                else: await removeLinesCustomPlaces()
            case 'C' | 'С':
                config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][0] = not config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][0]
                await AutoSaveConfig()
                await removeLinesCustomPlaces()
            case 'D' | 'В':
                if not config['General']['Disable_All_Warnings']:
                    whileTrueStage5 = True
                    await removeLinesCustomPlaces()
                    while whileTrueStage5:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][0] != f'Unknown_Normal_{listOfCustomPlacesTimed[indexPlace]}' else config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][1] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfCustomPlacesTimed[indexPlace]][2][1] != f'Unknown_Default_{listOfCustomPlacesTimed[indexPlace]}' else f'Unknown_{listOfCustomPlacesTimed[indexPlace]}'}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStage4 = False
                                whileTrueStage5 = False

                                try: config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(listOfCustomPlacesTimed[indexPlace])
                                except Exception: pass

                                try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(listOfCustomPlacesTimed[indexPlace])
                                except Exception: pass

                                try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses')
                                except Exception: pass

                                try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfCustomPlacesTimed[indexPlace]}_Badges')
                                except Exception: pass

                                try: listOfCustomPlacesTimed.remove(listOfCustomPlacesTimed[indexPlace])
                                except Exception: pass
                            case 'N' | 'Т':
                                whileTrueStage5 = False

                        await removeLines(8)
                else:
                    whileTrueStage4 = False
                    await removeLinesCustomPlaces()

                    try: config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(listOfCustomPlacesTimed[indexPlace])
                    except Exception: pass

                    try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(listOfCustomPlacesTimed[indexPlace])
                    except Exception: pass

                    try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfCustomPlacesTimed[indexPlace]}_Gamepasses')
                    except Exception: pass

                    try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfCustomPlacesTimed[indexPlace]}_Badges')
                    except Exception: pass

                    try: listOfCustomPlacesTimed.remove(listOfCustomPlacesTimed[indexPlace])
                    except Exception: pass

                await AutoSaveConfig()
            case '0':
                whileTrueStage4 = False
                await removeLinesCustomPlaces()
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case 'R' | 'К':
                loadConfig(configLoader['Loader']['Current_Config'])
                await cls()
                await lableASCII()
            case _:
                await removeLinesCustomPlaces()

def getCookieDataForSort():
    categoriesBoth = {}
    categoriesInt  = {}
    categoriesBool = {}
    for category in cookieData.listOfCookieData:
        if category[3] == int:
            categoriesBoth[category[1]] = int
            categoriesInt[category[1]]  = int
        elif category[3] == bool:
            categoriesBoth[category[1]] = bool
            categoriesBool[category[1]] = bool
    return categoriesBoth, categoriesInt, categoriesBool

def printSortCategories(categories: list):
    for index, category in enumerate(categories):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(categories))) + 15)} ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if categories[category] == int and config['Roblox']['CookieChecker']['Sorting'][category][0] or categories[category] == bool and config['Roblox']['CookieChecker']['Sorting'][category] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {' '.join(str(category).split('_'))}\n')

async def getSortValuesFromCategory(category: str):
    listOfValues = config['Roblox']['CookieChecker']['Sorting'][category][1]
    newSortValues = set()
    i = 0
    while len(listOfValues) > i:
        if int(listOfValues[i][0]) not in newSortValues and str(listOfValues[i][0]).isdigit():
            newSortValues.add(int(listOfValues[i][0]))
            try: config['Roblox']['CookieChecker']['Sorting'][category][1][i][0] = int(listOfValues[i][0])
            except TypeError: pass
            i += 1
        else:
            config['Roblox']['CookieChecker']['Sorting'][category][1].pop(i)
    config['Roblox']['CookieChecker']['Sorting'][category][1] = sorted(config['Roblox']['CookieChecker']['Sorting'][category][1])
    await AutoSaveConfig()
    return sorted(newSortValues)

async def removeDuplicatedSortValues(categories):
    for category in categories:
        listValues = config['Roblox']['CookieChecker']['Sorting'][category][1]
        i = 0
        while len(listValues) > i:
            if not str(listValues[i][0]).isdigit():
                config['Roblox']['CookieChecker']['Sorting'][category][1].pop(i)
            else:
                i += 1
    await AutoSaveConfig()

async def printSortValuesInCategory(sortValues: list, category: str):
    for index, sortValue in enumerate(sortValues):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(sortValues))) + 15)} ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting'][category][1][index][1] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {sortValue}\n')

### Roblox Cookie Refresher

async def getXCSRFToken(cookieRoblox):
    async with ClientSession(cookies=cookieRoblox) as session:
        async with session.post(f'https://auth.roblox.com/v2/logout') as response:
            isXCSRFToken = response.headers['X-CSRF-Token']
            return isXCSRFToken

async def getRBXAuthenticationTicket(cookieRoblox, XCSRFToken):
    async with ClientSession(
        cookies=cookieRoblox,
        headers={
            'rbxauthenticationnegotiation': '1',
            'referer': 'https://www.roblox.com/hewhewhew',
            'Content-Type': 'application/json',
            'x-csrf-token': XCSRFToken
        }) as session:

        async with session.post(f'https://auth.roblox.com/v1/authentication-ticket') as response:
            isRBXAuthenticationTicket = response.headers['rbx-authentication-ticket']
            return isRBXAuthenticationTicket

async def getSetCookie(isRBXAuthenticationTicket):
    async with ClientSession(headers={'rbxauthenticationnegotiation': '1'}) as session:
        async with session.post(f'https://auth.roblox.com/v1/authentication-ticket/redeem', data={'authenticationTicket': isRBXAuthenticationTicket}) as response:
            isSetCookie = response.headers
            return isSetCookie

async def startSingleModeRCR(cookieRoblox):
    isXCSRFToken              = await getXCSRFToken(cookieRoblox)
    isRBXAuthenticationTicket = await getRBXAuthenticationTicket(cookieRoblox, isXCSRFToken)
    isSetCookie               = await getSetCookie(isRBXAuthenticationTicket)
    return isSetCookie

async def startMassModeRCR(cookieRoblox: str, dateRefreshing: str):
    cookie = {'.ROBLOSECURITY': cookieRoblox}

    isValid = await isValidFunc(cookie) # изменить проверку на валидность [fix_it_1]
    isSetCookie = await startSingleModeRCR(cookie) if isValid[3] else ''

    try:
        newCookie = search(COOKIE_PATTERN, str(isSetCookie)).group(0)[:-1]
    except Exception:
        newCookie = MT_Invalid_Cookie

    def saveCookie():
        os.makedirs(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}', exist_ok=True)
        oldCookie = f'{cookieRoblox[115:125]}...{cookieRoblox[-10:-1]}'
        if 1 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
            open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed_cookies_mode_1.txt', 'a', encoding='UTF-8').write(f'{oldCookie} -> {newCookie}\n')
        if 2 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
            open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed_cookies_mode_2.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')
        if 3 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
            os.makedirs(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed cookies mode 3', exist_ok=True)
            open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed cookies mode 3\\{oldCookie}.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')

    if newCookie != MT_Invalid_Cookie:
        saveCookie()
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {cookieRoblox[115:125]}...{cookieRoblox[-10:-1]} {ANSI.FG.CYAN}->{ANSI.CLEAR + ANSI.DECOR.BOLD} {newCookie[115:125]}...{newCookie[-10:-1]}{ANSI.CLEAR}\n')
    elif config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies']:
        saveCookie()
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {cookieRoblox[115:125]}...{cookieRoblox[-10:-1]} {ANSI.FG.CYAN}->{ANSI.CLEAR + ANSI.DECOR.BOLD} {MT_Invalid_Cookie}{ANSI.CLEAR}\n')
    else:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {cookieRoblox[115:125]}...{cookieRoblox[-10:-1]} {ANSI.FG.CYAN}->{ANSI.CLEAR + ANSI.DECOR.BOLD} {MT_Invalid_Cookie}{ANSI.CLEAR}\n')

### Cookie Control Panel

async def printCCPCookiesInHistory(category):
    for index, cookie in enumerate(config['Roblox']['CookieControlPanel'][category]):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['CookieControlPanel'][category]))) + 15)} ┃ {cookie} ({config['Roblox']['CookieControlPanel'][category][cookie][2]})\n')

async def cookieControlPanel(category: str, key: str, path: str):
    whileTrueStageCCP1 = True
    await cls()
    await lableASCII()
    while whileTrueStageCCP1:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{path}\\{key}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Data}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Show_Cookie}\n  ┃\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        cookieControlPanelCookieCurrentCookieMainTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match cookieControlPanelCookieCurrentCookieMainTab.upper():
            case '1':
                whileTrueStageCCP2 = True
                await cls()
                await lableASCII()
                while whileTrueStageCCP2:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{path}\\{key}\\{MT_Data}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n  [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Country Reg.' if config['Roblox']['CookieControlPanel'][category][key][0] == None else f'Country Reg.: {config['Roblox']['CookieControlPanel'][category][key][0]}'}\n  [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} ID' if config['Roblox']['CookieControlPanel'][category][key][1] == None else f'ID: {config['Roblox']['CookieControlPanel'][category][key][1]}'}\n  [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Name' if config['Roblox']['CookieControlPanel'][category][key][2] == None else f'Name: {config['Roblox']['CookieControlPanel'][category][key][2]}'}\n  [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Display Name' if config['Roblox']['CookieControlPanel'][category][key][3] == None else f'Display Name: {config['Roblox']['CookieControlPanel'][category][key][3]}'}\n  [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Reg. Date' if config['Roblox']['CookieControlPanel'][category][key][4] == None else f'Reg. Date: {config['Roblox']['CookieControlPanel'][category][key][4]}'} {f'({config['Roblox']['CookieControlPanel'][category][key][5]})' if config['Roblox']['CookieControlPanel'][category][key][5] != None else ''}\n  [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Robux' if config['Roblox']['CookieControlPanel'][category][key][6] == None else f'Robux: {config['Roblox']['CookieControlPanel'][category][key][6]}'}\n  [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Billing' if config['Roblox']['CookieControlPanel'][category][key][7] == None else f'Billing: {config['Roblox']['CookieControlPanel'][category][key][7]}'}\n  [{ANSI.FG.PINK}8{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Pending' if config['Roblox']['CookieControlPanel'][category][key][8] == None else f'Pending: {config['Roblox']['CookieControlPanel'][category][key][8]}'}\n  [{ANSI.FG.PINK}9{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Donate' if config['Roblox']['CookieControlPanel'][category][key][9] == None else f'Donate: {config['Roblox']['CookieControlPanel'][category][key][9]}'}\n [{ANSI.FG.PINK}10{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Purchases' if config['Roblox']['CookieControlPanel'][category][key][10] == None else f'Purchases: {config['Roblox']['CookieControlPanel'][category][key][10]}'}\n [{ANSI.FG.PINK}11{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Custom Gamepasses' if config['Roblox']['CookieControlPanel'][category][key][11] == None else f'Custom Gamepasses: {config['Roblox']['CookieControlPanel'][category][key][11]}'}\n [{ANSI.FG.PINK}12{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Rap' if config['Roblox']['CookieControlPanel'][category][key][12] == None else f'Rap: {config['Roblox']['CookieControlPanel'][category][key][12]}'}\n [{ANSI.FG.PINK}13{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Card' if config['Roblox']['CookieControlPanel'][category][key][13] == None else f'Card: {config['Roblox']['CookieControlPanel'][category][key][13]}'}\n [{ANSI.FG.PINK}14{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Premium' if config['Roblox']['CookieControlPanel'][category][key][14] == None else f'Premium: {config['Roblox']['CookieControlPanel'][category][key][14]}'}\n [{ANSI.FG.PINK}15{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Gamepasses' if config['Roblox']['CookieControlPanel'][category][key][15] == None else f'Gamepasses: {config['Roblox']['CookieControlPanel'][category][key][15]}'}\n [{ANSI.FG.PINK}16{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Badges' if config['Roblox']['CookieControlPanel'][category][key][16] == None else f'Badges: {config['Roblox']['CookieControlPanel'][category][key][16]}'}\n [{ANSI.FG.PINK}17{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Fav. Games' if config['Roblox']['CookieControlPanel'][category][key][16] == None else f'Fav. Games: {config['Roblox']['CookieControlPanel'][category][key][16]}'}\n [{ANSI.FG.PINK}18{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Bundles' if config['Roblox']['CookieControlPanel'][category][key][18] == None else f'Bundles: {config['Roblox']['CookieControlPanel'][category][key][18]}'}\n [{ANSI.FG.PINK}19{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Inv. Privacy' if config['Roblox']['CookieControlPanel'][category][key][19] == None else f'Inv. Privacy: {config['Roblox']['CookieControlPanel'][category][key][19]}'}\n [{ANSI.FG.PINK}20{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Trade Privacy' if config['Roblox']['CookieControlPanel'][category][key][20] == None else f'Trade Privacy: {config['Roblox']['CookieControlPanel'][category][key][20]}'}\n [{ANSI.FG.PINK}21{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Can Trade' if config['Roblox']['CookieControlPanel'][category][key][21] == None else f'Can Trade: {config['Roblox']['CookieControlPanel'][category][key][21]}'}\n [{ANSI.FG.PINK}22{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Sessions' if config['Roblox']['CookieControlPanel'][category][key][22] == None else f'Sessions: {config['Roblox']['CookieControlPanel'][category][key][22]}'}\n [{ANSI.FG.PINK}23{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Email' if config['Roblox']['CookieControlPanel'][category][key][23] == None else f'Email: {config['Roblox']['CookieControlPanel'][category][key][23]}'}\n [{ANSI.FG.PINK}24{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Phone' if config['Roblox']['CookieControlPanel'][category][key][24] == None else f'Phone: {config['Roblox']['CookieControlPanel'][category][key][24]}'}\n [{ANSI.FG.PINK}25{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} 2FA' if config['Roblox']['CookieControlPanel'][category][key][25] == None else f'2FA: {config['Roblox']['CookieControlPanel'][category][key][25]}'}\n [{ANSI.FG.PINK}26{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Pin' if config['Roblox']['CookieControlPanel'][category][key][26] == None else f'Pin: {config['Roblox']['CookieControlPanel'][category][key][26]}'}\n [{ANSI.FG.PINK}27{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} >13' if config['Roblox']['CookieControlPanel'][category][key][27] == None else f'>13: {config['Roblox']['CookieControlPanel'][category][key][27]}'}\n [{ANSI.FG.PINK}28{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Verified Age' if config['Roblox']['CookieControlPanel'][category][key][28] == None else f'Verified Age: {config['Roblox']['CookieControlPanel'][category][key][28]}'}\n [{ANSI.FG.PINK}29{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Voice' if config['Roblox']['CookieControlPanel'][category][key][29] == None else f'Voice: {config['Roblox']['CookieControlPanel'][category][key][29]}'}\n [{ANSI.FG.PINK}30{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Friends' if config['Roblox']['CookieControlPanel'][category][key][30] == None else f'Friends: {config['Roblox']['CookieControlPanel'][category][key][30]}'}\n [{ANSI.FG.PINK}31{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Followers' if config['Roblox']['CookieControlPanel'][category][key][31] == None else f'Followers: {config['Roblox']['CookieControlPanel'][category][key][31]}'}\n [{ANSI.FG.PINK}32{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Followings' if config['Roblox']['CookieControlPanel'][category][key][32] == None else f'Followings: {config['Roblox']['CookieControlPanel'][category][key][32]}'}\n [{ANSI.FG.PINK}33{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Roblox Badges' if config['Roblox']['CookieControlPanel'][category][key][33] == None else f'Roblox Badges: {', '.join(config['Roblox']['CookieControlPanel'][category][key][33])}'}\n [{ANSI.FG.PINK}34{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} X-CSRF-Token' if config['Roblox']['CookieControlPanel'][category][key][34] == None else f'X-CSRF-Token: {config['Roblox']['CookieControlPanel'][category][key][34]}'}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    cookieControlPanelCookieCurrentCookieDataTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    if cookieControlPanelCookieCurrentCookieDataTab == '0': whileTrueStageCCP2 = False
                    elif cookieControlPanelCookieCurrentCookieDataTab.isdigit() and int(cookieControlPanelCookieCurrentCookieDataTab) <= 35:
                        cookieRoblox = {'.ROBLOSECURITY': config['Roblox']['CookieControlPanel'][category][key][35]}

                        async def startCCP():
                            async with ClientSession(cookies=cookieRoblox) as session:
                                try:
                                    async with session.get('https://users.roblox.com/v1/users/authenticated') as response:
                                        if response.status == 401: return await errorOrCorrectHandler(True, 5, MT_Invalid_Cookie, f'{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}')

                                    async with session.get('https://www.roblox.com/my/settings/json') as response:
                                        isAccountInformation = await response.json()
                                        isID = isAccountInformation['UserId']

                                        # нужно переделать
                                        getGlobalsCheckListGamepasses()
                                        getGlobalsCheckListBadges()
                                        getGlobalCheckListCustomGamepasses()
                                        getGlobalCheckListFavoritePlaces()
                                        getGlobalCheckListBundles()

                                        match cookieControlPanelCookieCurrentCookieDataTab.upper():
                                            case '1':  config['Roblox']['CookieControlPanel'][category][key][0]  = list(await isCountryRegistrationFunc(session, isID, isAccountInformation, True))[2]
                                            case '2':  config['Roblox']['CookieControlPanel'][category][key][1]  = list(await isUselessIDFunc(          session, isID, isAccountInformation, True))[2]
                                            case '3':  config['Roblox']['CookieControlPanel'][category][key][2]  = list(await isNameFunc(               session, isID, isAccountInformation, True))[2]
                                            case '4':  config['Roblox']['CookieControlPanel'][category][key][3]  = list(await isDisplayNameFunc(        session, isID, isAccountInformation, True))[2]
                                            case '5':  config['Roblox']['CookieControlPanel'][category][key][4]  = list(await isRegistrationDateFunc(   session, isID, isAccountInformation, True))[2]; config['Roblox']['CookieControlPanel'][category][key][5] = list(await isRegistrationDateFunc(session, isID, isAccountInformation, True))[5]
                                            case '6':  config['Roblox']['CookieControlPanel'][category][key][6]  = list(await isRobuxFunc(              session, isID, isAccountInformation, True))[2]
                                            case '7':  config['Roblox']['CookieControlPanel'][category][key][7]  = list(await isBillingFunc(            session, isID, isAccountInformation, True))[2]
                                            case '8':  config['Roblox']['CookieControlPanel'][category][key][8]  = list(await isTransactionsForYearFunc(session, isID, isAccountInformation, True))[2]
                                            case '9':  config['Roblox']['CookieControlPanel'][category][key][9]  = list(await isTransactionsForYearFunc(session, isID, isAccountInformation, True))[3]
                                            case '10': config['Roblox']['CookieControlPanel'][category][key][10] = list(await isPurchasesFunc(          session, isID, isAccountInformation, True))[2]
                                            case '11': config['Roblox']['CookieControlPanel'][category][key][11] = list(await isPurchasesFunc(          session, isID, isAccountInformation, True))[5]
                                            case '12': config['Roblox']['CookieControlPanel'][category][key][12] = list(await isRapFunc(                session, isID, isAccountInformation, True))[2]
                                            case '13': config['Roblox']['CookieControlPanel'][category][key][13] = list(await isCardFunc(               session, isID, isAccountInformation, True))[2]
                                            case '14': config['Roblox']['CookieControlPanel'][category][key][14] = list(await isPremiumFunc(            session, isID, isAccountInformation, True))[2]
                                            case '15': config['Roblox']['CookieControlPanel'][category][key][15] = list(await isGamepassesFunc(         session, isID, isAccountInformation, True))[2]
                                            case '16': config['Roblox']['CookieControlPanel'][category][key][16] = list(await isBadgesFunc(             session, isID, isAccountInformation, True))[2]
                                            case '17': config['Roblox']['CookieControlPanel'][category][key][17] = list(await isFavoritePlacesFunc(     session, isID, isAccountInformation, True))[2]
                                            case '18': config['Roblox']['CookieControlPanel'][category][key][18] = list(await isBundlesFunc(            session, isID, isAccountInformation, True))[2]
                                            case '19': config['Roblox']['CookieControlPanel'][category][key][19] = list(await isInventoryPrivacyFunc(   session, isID, isAccountInformation, True))[2]
                                            case '20': config['Roblox']['CookieControlPanel'][category][key][20] = list(await isTradePrivacyFunc(       session, isID, isAccountInformation, True))[2]
                                            case '21': config['Roblox']['CookieControlPanel'][category][key][21] = list(await isCanTradeFunc(           session, isID, isAccountInformation, True))[2]
                                            case '22': config['Roblox']['CookieControlPanel'][category][key][22] = list(await isSessionsFunc(           session, isID, isAccountInformation, True))[2]
                                            case '23': config['Roblox']['CookieControlPanel'][category][key][23] = list(await isEmailFunc(              session, isID, isAccountInformation, True))[2]
                                            case '24': config['Roblox']['CookieControlPanel'][category][key][24] = list(await isPhoneFunc(              session, isID, isAccountInformation, True))[2]
                                            case '25': config['Roblox']['CookieControlPanel'][category][key][25] = list(await is2FAFunc(                session, isID, isAccountInformation, True))[2]
                                            case '26': config['Roblox']['CookieControlPanel'][category][key][26] = list(await isPinFunc(                session, isID, isAccountInformation, True))[2]
                                            case '27': config['Roblox']['CookieControlPanel'][category][key][27] = list(await isAbove13Func(            session, isID, isAccountInformation, True))[2]
                                            case '28': config['Roblox']['CookieControlPanel'][category][key][28] = list(await isVerifiedAgeFunc(        session, isID, isAccountInformation, True))[2]
                                            case '29': config['Roblox']['CookieControlPanel'][category][key][29] = list(await isVoiceFunc(              session, isID, isAccountInformation, True))[2]
                                            case '30': config['Roblox']['CookieControlPanel'][category][key][30] = list(await isNumberOfFriendsFunc(    session, isID, isAccountInformation, True))[2]
                                            case '31': config['Roblox']['CookieControlPanel'][category][key][31] = list(await isNumberOfFollowersFunc(  session, isID, isAccountInformation, True))[2]
                                            case '32': config['Roblox']['CookieControlPanel'][category][key][32] = list(await isNumberOfFollowingsFunc( session, isID, isAccountInformation, True))[2]
                                            case '33': config['Roblox']['CookieControlPanel'][category][key][33] = list(await isRobloxBadgesFunc(       session, isID, isAccountInformation, True))[2]
                                            case '34': config['Roblox']['CookieControlPanel'][category][key][34] = list(await isXCSRFTokenFunc(         session, isID, isAccountInformation, True))[2]
                                        # ---
                                except Exception as e:
                                    print(f'CCP_U_Error: {e}')

                        await startCCP()
                        await AutoSaveConfig()

                    await cls()
                    await lableASCII()
            case '2':
                whileTrueStageCCP2 = True
                await cls()
                await lableASCII()
                while whileTrueStageCCP2:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{path}\\{key}\\{MT_Show_Cookie}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n{config['Roblox']['CookieControlPanel'][category][key][35]}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    cookieControlPanelCookieCurrentCookieShowCookie = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match cookieControlPanelCookieCurrentCookieShowCookie.upper():
                        case '0':
                            whileTrueStageCCP2 = False
                    await cls()
                    await lableASCII()
            case 'D' | 'В':
                if not config['General']['Disable_All_Warnings']:
                    whileTrueStageCCP2 = True
                    await removeLines(9)
                    while whileTrueStageCCP2:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{path}\\{key}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStageCCP1 = False
                                whileTrueStageCCP2 = False
                                try: config['Roblox']['CookieControlPanel'][category].remove(key)
                                except Exception: pass
                                await AutoSaveConfig()
                                await removeLines(8)
                            case 'N' | 'Т':
                                whileTrueStageCCP2 = False
                                await removeLines(8)
                            case _:
                                await removeLines(8)
                else:
                    whileTrueStageCCP1 = False
                    try: config['Roblox']['CookieControlPanel'][category].remove(key)
                    except Exception: pass
                    await AutoSaveConfig()
            case '0':
                whileTrueStageCCP1 = False
                await removeLines(9)
            case _:
                await removeLines(9)

### Основные функции

def neededFoldersAndFiles():
    folders = ['Proxy\\Checker', 'Roblox\\Cookie Parser', 'Roblox\\Cookie Checker', 'Roblox\\Cookie Refresher', 'Roblox\\Cookie Refresher\\Mass Mode']
    files = ['Proxy\\Checker\\proxies.txt', 'Roblox\\Cookie Parser\\cookies.txt', 'Roblox\\Cookie Checker\\cookies.txt', 'Roblox\\Cookie Checker\\proxies.txt', 'Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    for file in files:
        if not os.path.exists(file): open(file, 'w')

def loadConfigLoader():
    os.makedirs('Settings\\Configs', exist_ok=True)
    try:
        global configLoader; configLoader = loads(open('Settings\\Configs\\.Loader.toml', 'r', encoding='UTF-8').read())

        try:
            nameConfig = str(configLoader['Loader']['Load_Config'])
            configLoader['Loader']['Current_Config'] = nameConfig
            open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
        except Exception:
            configLoader['Loader']['Load_Config'] = 'default'
            open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
            return loadConfig('default')

        if nameConfig in configFiles():
            return loadConfig(nameConfig)
        else:
            configLoader['Loader']['Load_Config'] = 'default'
            open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
            return loadConfig('default')
    except Exception:
        configLoader = document()
        configLoader.add(nl())
        configLoader.add(comment('Meow >:3'))
        configLoader.add(nl())
        configLoader.add('Loader', table())
        configLoader['Loader']['Load_Config'] = 'default'
        configLoader['Loader']['Load_Config'].comment('name of config for load on launch')
        configLoader['Loader']['Current_Config'] = 'default'
        configLoader.add('Saver', table())
        configLoader['Saver']['Auto_Save_Changes'] = False
        
        open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
        return loadConfig('default')

def loadConfig(name):
    global config
    os.makedirs('Settings\\Configs', exist_ok=True)
    if not os.path.exists(f'Settings\\Configs\\{name}.toml'):
        config = document()
        config.add(nl())
        config.add(comment('Meow >:3'))
        config.add(nl())

        # General
        config.add('General', table())
        config['General']['Console_Title'] = 'MeowTool... Meow :3'
        config['General']['Language'] = 'RU'
        config['General']['Language'].comment('RU or EN')
        config['General']['Show_Lable_MeowTool'] = True
        config['General']['Show_Lable_by_h1kken'] = False
        config['General']['Press_Any_Key_To_Continue'] = True
        config['General']['Disable_All_Warnings'] = False
        
        # Proxy
        config.add('Proxy', table())
        
        # Proxy - Checker
        config['Proxy'].add('Checker', table())
        config['Proxy']['Checker']['Timeout'] = 1
        config['Proxy']['Checker']['Timeout'].comment('maximum wait for a response from a proxy (in seconds)')
        config['Proxy']['Checker']['Save_In_Custom_Folder'] = False
        config['Proxy']['Checker']['Save_Without_Protocol'] = False

        # Roblox
        config.add('Roblox', table())
    
        # Roblox - Cookie Parser
        config['Roblox'].add('CookieParser', table())
        config['Roblox']['CookieParser']['Create_Backups'] = True
        config['Roblox']['CookieParser']['Save_To_A_File'] = 'outputs'

        # Roblox - Cookie Checker
        config['Roblox'].add('CookieChecker', table())

        # Roblox - Cookie Checker - General
        config['Roblox']['CookieChecker'].add('General', table())
        config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] = False
        config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] = 5
        config['Roblox']['CookieChecker']['General']['Send_Some_Requests_Through_RoProxy'] = False
        config['Roblox']['CookieChecker']['General']['Output_Total'] = True
        config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] = 5

        # Roblox - Cookie Checker - Sorting
        config['Roblox']['CookieChecker'].add('Sorting', table())
        config['Roblox']['CookieChecker']['Sorting']['Sort'] = False
        config['Roblox']['CookieChecker']['Sorting'].add(comment('Categories'))
        for category in cookieData.listOfCookieData:
            if   category[3] == int:  config['Roblox']['CookieChecker']['Sorting'][category[1]] = [False, []]
            elif category[3] == bool: config['Roblox']['CookieChecker']['Sorting'][category[1]] = False

        # Roblox - Cookie Checker - Proxy
        config['Roblox']['CookieChecker']['General'].add('Proxy', table())
        config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy'] = False
        config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
        config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'].comment('if protocol is not specified - it will be this (available: http, https, socks4, socks5)')

        # Roblox - Cookie Checker - Main
        config['Roblox']['CookieChecker'].add('Main', table())
        for data in cookieData.listOfCookieData:
            config['Roblox']['CookieChecker']['Main'][data[1]] = False
            match data[1]:
                case 'Purchases':
                    config['Roblox']['CookieChecker']['Main']['Purchases_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Purchases_Max_Check_Pages'].comment('0 - All')
                case 'Rap':
                    config['Roblox']['CookieChecker']['Main']['Rap_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Rap_Max_Check_Pages'].comment('0 - All')
                case 'Gamepasses':
                    config['Roblox']['CookieChecker']['Main']['Gamepasses_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Gamepasses_Max_Check_Pages'].comment('0 - All')
                case 'Custom_Gamepasses':
                    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'] = [
                        ['Fly-A-Pet Potion',  False],
                        ['Ride-A-Pet Potion', False]
                    ]
                    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'].comment('0 - All')
                case 'Badges':
                    config['Roblox']['CookieChecker']['Main']['Badges_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Badges_Max_Check_Pages'].comment('0 - All')
                case 'Favorite_Places':
                    config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'] = [
                        [920587237,  'Adopt Me',         False],
                        [142823291,  'Murder Mystery 2', False],
                        [8737899170, 'Pet Simulator 99', False]
                    ]
                    config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages'].comment('0 - All')
                case 'Bundles':
                    config['Roblox']['CookieChecker']['Main']['Bundles_IDs'] = [
                        [192, 'Korblox Deathspeaker', False],
                        [201, 'Headless Horseman',    False]
                    ]
                    config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages'] = 0
                    config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages'].comment('0 - All')
                case 'Sessions':
                    config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages'] = 1
                    config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages'].comment('0 - All, 1 - Must be good to avoid long wait for this \'https://imgur.com/a/TrBIdCu\'')

        # Roblox - Cookie Checker - Places
        config['Roblox']['CookieChecker'].add('Places', table())
        for place in listOfPlaces:
            config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = False
        
        # Roblox - Cookie Checker - Places - Gamepasses and Badges
        for place in listOfPlaces:
            config['Roblox']['CookieChecker'].add(place.__name__, table())
            if getattr(place, 'Gamepasses', False):
                config['Roblox']['CookieChecker'][place.__name__].add(comment('Gamepasses'))
                for gamepass in place.Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][place.__name__][gamepass[2]] = False
            if getattr(place, 'Badges', False):
                config['Roblox']['CookieChecker'][place.__name__].add(comment('Badges'))
                for badge in place.Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][place.__name__][badge[2]] = False

        # Roblox - Cookie Checker - Custom Places
        config['Roblox']['CookieChecker'].add('CustomPlaces', table())
        config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] = False
        config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'] = []
        config['Roblox']['CookieChecker']['CustomPlaces'].add(comment('Custom Places'))

        # Roblox - Cookie Refresher
        config['Roblox'].add('CookieRefresher', table())

        # Roblox - Cookie Refresher - Single Mode
        config['Roblox']['CookieRefresher'].add('SingleMode', table())
        config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] = [1]
        config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].comment('Modes: 1, 2, 3 | Examples: [1, 2, 3] / [1, 2] / [1, 3] etc.')
        
        # Roblox - Cookie Refresher - Mass Mode
        config['Roblox']['CookieRefresher'].add('MassMode', table())
        config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] = [1]
        config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].comment('Modes: 1, 2, 3 | Examples: [1, 2, 3] / [1, 2] / [1, 3] etc.')
        config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies'] = False
        config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = ''
        
        # Roblox - Cookie Control Panel
        config['Roblox'].add('CookieControlPanel', table())
        config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually'] = False
        config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker'] = False
        
        # Roblox - Cookie Control Panel - Cookie Control Panel History
        config['Roblox']['CookieControlPanel'].add('CookieControlPanelHistory', table())
        
        # Roblox - Cookie Control Panel - Roblox Cookie Checker History
        config['Roblox']['CookieControlPanel'].add('RobloxCookieCheckerHistory', table())
        
        # Roblox - Misc
        config['Roblox'].add('Misc', table())
        
        # Roblox - Misc - Gamepasses Parser
        config['Roblox']['Misc'].add('GamepassesParser', table())
        config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name'] = False
        config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name'] = False
        config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name'] = False
        
        # Roblox - Misc - Badges Parser
        config['Roblox']['Misc'].add('BadgesParser', table())
        config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name'] = False
        config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name'] = False
        config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name'] = False

        open(f'Settings\\Configs\\{name}.toml', 'w', encoding='UTF-8').write(dumps(config))

    configLoader['Loader']['Current_Config'] = name
    open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
    config = loads(open(f'Settings\\Configs\\{name}.toml', 'r', encoding='UTF-8').read())

def configFiles():
    configs = []
    for file in os.listdir('Settings\\Configs'):
        if len(file) <= 65 and file.strip() not in ('.Loader.toml', '.toml') and file.endswith('.toml'):
            configs.append(file[:-5])
    if not configs:
        loadConfig('default')
        configs.append('default')
    return configs

def printConfigs(configs):
    for index, config in enumerate(configs):
        sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(configs))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Loader']['Current_Config'] == config else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {config}\n')

async def configContextMenu(indexConfig: int):
    whileTrueStage3 = True
    choosedConfig = configFiles()[indexConfig]
    errorDeleteConfig = {str(file).lower() for file in configFiles()}
    await cls()
    await lableASCII()
    while whileTrueStage3:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Configs}\\{choosedConfig}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Loader']['Load_Config'] == choosedConfig else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Load_On_Launch}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Save[0]}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Load}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Rename}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_File_Location}\n  ┃\n [{ANSI.FG.YELLOW}R{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Reset_To_Default_Settings}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        configTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match configTab.upper():
            case '1':
                if configLoader['Loader']['Load_Config'] != choosedConfig:
                    configLoader['Loader']['Load_Config'] = choosedConfig
                else:
                    configLoader['Loader']['Load_Config'] = 'default'
                open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
                await removeLines(13)
            case '2':
                open(f'Settings\\Configs\\{configLoader['Loader']['Current_Config']}.toml', 'w', encoding='UTF-8').write(dumps(config))
                await removeLines(13)
            case '3':
                loadConfig(choosedConfig)
                await removeLines(13)
            case '4':
                await removeLines(11)
                newNameOfConfig = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_New_Name_For_Config}:{ANSI.CLEAR} ')
                if newNameOfConfig == '0': return await removeLines(5)
                if len(newNameOfConfig) > 60:
                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Config_Name_60, f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')
                if any(char in newNameOfConfig for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']) or not newNameOfConfig.strip():
                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,                f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')
                if not os.path.exists(f'Settings\\Configs\\{choosedConfig}.toml'):
                    return await errorOrCorrectHandler(True, 5, MT_File_Is_Missing,                    f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')
                if newNameOfConfig.lower() in errorDeleteConfig and newNameOfConfig != choosedConfig:
                    return await errorOrCorrectHandler(True, 5, MT_File_With_This_Name_Already_Exists, f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')

                os.rename(f'Settings\\Configs\\{choosedConfig}.toml', f'Settings\\Configs\\{newNameOfConfig}.toml')
                if configLoader['Loader']['Load_Config']    == choosedConfig: configLoader['Loader']['Load_Config']    = newNameOfConfig
                if configLoader['Loader']['Current_Config'] == choosedConfig: configLoader['Loader']['Current_Config'] = newNameOfConfig
                open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
                whileTrueStage3 = False
                await removeLines(5)
            case '5':
                os.makedirs('Settings\\Configs', exist_ok=True)
                os.startfile('Settings\\Configs')
                await removeLines(13)
            case 'R' | 'К':
                if not config['General']['Disable_All_Warnings']:
                    whileTrueStage4 = True
                    await removeLines(13)
                    while whileTrueStage4:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Configs}\\{choosedConfig}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStage4 = False
                                try: os.remove(f'Settings\\Configs\\{choosedConfig}.toml')
                                except Exception: pass
                                loadConfig(choosedConfig)
                            case 'N' | 'Т':
                                whileTrueStage4 = False
                        await removeLines(8)
                else:
                    try: os.remove(f'Settings\\Configs\\{choosedConfig}.toml')
                    except Exception: pass
                    loadConfig(choosedConfig)
                    await removeLines(13)
            case 'D' | 'В':
                if not config['General']['Disable_All_Warnings']:
                    whileTrueStage4 = True
                    await removeLines(13)
                    while whileTrueStage4:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Configs}\\{choosedConfig}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStage3 = False
                                whileTrueStage4 = False
                                try: os.remove(f'Settings\\Configs\\{choosedConfig + '.toml'}')
                                except Exception: pass
                                if configLoader['Loader']['Current_Config'] not in configFiles() or len(configFiles()) == 0: loadConfig('default')
                                await removeLines(8)
                            case 'N' | 'Т':
                                whileTrueStage4 = False
                                await removeLines(8)
                            case _:
                                await removeLines(8)
                else:
                    whileTrueStage3 = False
                    try: os.remove(f'Settings\\Configs\\{choosedConfig + '.toml'}')
                    except Exception: pass
                    if configLoader['Loader']['Current_Config'] not in configFiles() or len(configFiles()) == 0: loadConfig('default')
                    await removeLines(13)
            case '0':
                whileTrueStage3 = False
                await removeLines(13)
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case _:
                await removeLines(13)

async def mainMenu():
    global config

    if str(config['General']['Console_Title']).replace(' ', '') == '' or len(str(config['General']['Console_Title'])) > 50 or any(char in str(config['General']['Console_Title']) for char in ['<', '>', '|', '^', '&']):
        os.system('title MeowTool... Meow :3')
    else:
        os.system(f'title {config['General']['Console_Title']}')

    await lableASCII(True)

    while True:
        # Главное меню
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Proxy}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Roblox}\n  ┃\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Settings}\n [{ANSI.FG.RED}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Close_Program}{ANSI.CLEAR}\n\n')
        mainTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match mainTab.upper():
            # Прокси
            case '1':
                whileTrueStage1 = True
                await removeLines(9)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Proxy}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    proxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match proxyTab.upper():
                        # Прокси Чекер
                        case '1':
                            whileTrueStage2 = True
                            await removeLines(7)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Proxy}\\{MT_Checker}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ proxies {amountOfLines('Proxy\\Checker', 'proxies')}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ http_valid {amountOfLines('Proxy\\Checker', 'http_valid')}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ http_invalid {amountOfLines('Proxy\\Checker', 'http_invalid')}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks4_valid {amountOfLines('Proxy\\Checker', 'socks4_valid')}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks4_invalid {amountOfLines('Proxy\\Checker', 'socks4_invalid')}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks5_valid {amountOfLines('Proxy\\Checker', 'socks5_valid')}\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks5_invalid {amountOfLines('Proxy\\Checker', 'socks5_invalid')}\n [{ANSI.FG.PINK}8{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ custom_valid {amountOfLines('Proxy\\Checker', 'custom_valid')}\n [{ANSI.FG.PINK}9{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ unknown_invalid {amountOfLines('Proxy\\Checker', 'unknown_invalid')}\n  ┃\n [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                proxyCheckerTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match proxyCheckerTab.upper():
                                    case '1': await proxyChecker('proxies')
                                    case '2': await proxyChecker('http_valid')
                                    case '3': await proxyChecker('http_invalid')
                                    case '4': await proxyChecker('socks4_valid')
                                    case '5': await proxyChecker('socks4_invalid')
                                    case '6': await proxyChecker('socks5_valid')
                                    case '7': await proxyChecker('socks5_invalid')
                                    case '8': await proxyChecker('custom_valid')
                                    case '9': await proxyChecker('unknown_invalid')
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(16)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:   
                                        await removeLines(16)
                        case '0':
                            whileTrueStage1 = False
                            await removeLines(7)
                        case 'F' | 'А':
                            await cls()
                            await lableASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                            await cls()
                            await lableASCII()
                        case _:   
                            await removeLines(7)
            # Роблокс
            case '2':
                whileTrueStage1 = True
                await removeLines(9)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Parser}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Checker} {ANSI.FG.RED}{MT_Beta}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Refresher}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Control_Panel}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Misc}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    robloxTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match robloxTab.upper():
                        # Роблокс Куки Парсер
                        case '1':
                            whileTrueStage2 = True
                            await removeLines(11)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Parser}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Start_Parsing}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxCookieParserTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxCookieParserTab.upper():
                                    case '1':
                                        await robloxCookieParser()
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(7)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:
                                        await removeLines(7)
                        # Роблокс Куки Чекер
                        case '2':
                            whileTrueStage2 = True
                            await removeLines(11)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Checker} {ANSI.FG.RED}{MT_Beta}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ cookies {amountOfLines('Roblox\\Cookie Checker', 'cookies')}\n  ┃\n [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxCookieCheckerTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxCookieCheckerTab.upper():
                                    case '1':
                                        await robloxCookieChecker('cookies')
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(8)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:
                                        await removeLines(8)
                        # Роблокс Куки Рефрешер
                        case '3':
                            whileTrueStage2 = True
                            await removeLines(11)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Refresher}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Single_Mode}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Mass_Mode}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxCookieRefresherTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxCookieRefresherTab.upper():
                                    case '1':
                                        await removeLines(8)
                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                        robloxCookieRefresherCookieEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Cookie1}:{ANSI.CLEAR} ')

                                        async def refresherSingleModeCookie():
                                            if robloxCookieRefresherCookieEnter == '0': return
                                            if not search(COOKIE_PATTERN, robloxCookieRefresherCookieEnter):
                                                await cls()
                                                await lableASCII()
                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.RED}X{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Incorrect_Cookie}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
                                                await waitingInput()
                                                return

                                            await cls()
                                            await lableASCII()
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Wait}...{ANSI.CLEAR}\n')

                                            cookie = {'.ROBLOSECURITY': robloxCookieRefresherCookieEnter}

                                            try:
                                                isSetCookie = await startSingleModeRCR(cookie)

                                                newCookie = search(COOKIE_PATTERN, str(isSetCookie)).group(0)[:-1]

                                                if not newCookie:
                                                    await cls()
                                                    await lableASCII()
                                                    return await errorOrCorrectHandler(True, 0, MT_Invalid_Cookie, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}')
                                            except (KeyError, TypeError, ContentTypeError):
                                                await cls()
                                                await lableASCII()
                                                return await errorOrCorrectHandler(True, 0, MT_Invalid_Cookie, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}')

                                            dateOfSingleModeRefreshing = datetime.datetime.now().strftime('%d.%m.%Y - %H.%M.%S')

                                            os.makedirs(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}', exist_ok=True)
                                            if 1 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                open(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed_cookies_mode_1.txt', 'a', encoding='UTF-8').write(f'{robloxCookieRefresherCookieEnter[115:125]}...{robloxCookieRefresherCookieEnter[-10:-1]} -> {newCookie}\n')
                                            if 2 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                open(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed_cookies_mode_2.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')
                                            if 3 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                os.makedirs(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed cookies mode 3', exist_ok=True)
                                                open(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed cookies mode 3\\{robloxCookieRefresherCookieEnter[115:125]}...{robloxCookieRefresherCookieEnter[-10:-1]}.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')

                                            await removeLines(3)
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n{newCookie}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
                                            await waitingInput()

                                        await refresherSingleModeCookie()
                                    case '2':
                                        # не самая лучшая идея проверки времени [fix_it_2]
                                        whileTrueStage3 = True
                                        await removeLines(8)
                                        while whileTrueStage3:
                                            try:
                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Start_Refresher} ({MT_50_Cookies_In_Once}) [{f'{ANSI.FG.GREEN + MT_Can_Continue + ANSI.CLEAR + ANSI.DECOR.BOLD}' if config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] == '' else f'{ANSI.FG.RED + f'{MT_Wait} {str(int((datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'), '%H:%M:%S') - (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1))).total_seconds()))[1:]} {MT_Seconds}.' + ANSI.CLEAR + ANSI.DECOR.BOLD}' if (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1)).time() > datetime.datetime.now().time() else f'{ANSI.FG.GREEN + MT_Can_Continue + ANSI.CLEAR + ANSI.DECOR.BOLD}'}]\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Start_Refresher} ({MT_50_Cookies_In_60_Seconds}) [{f'{ANSI.FG.GREEN + MT_Can_Continue + ANSI.CLEAR + ANSI.DECOR.BOLD}' if config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] == '' else f'{ANSI.FG.RED + f'{MT_Wait} {str(int((datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'), '%H:%M:%S') - (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1))).total_seconds()))[1:]} {MT_Seconds}.' + ANSI.CLEAR + ANSI.DECOR.BOLD}' if (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1)).time() > datetime.datetime.now().time() else f'{ANSI.FG.GREEN + MT_Can_Continue + ANSI.CLEAR + ANSI.DECOR.BOLD}'}]\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                robloxCookieRefresherMassModeTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                match robloxCookieRefresherMassModeTab.upper():
                                                    case '1':
                                                        async def refresherMassModeOnly50Cookie():
                                                            if config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] != '' and (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1)).time() > datetime.datetime.now().time():
                                                                return await errorOrCorrectHandler(True, 8, f'{MT_Wait} {str(int((datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'), '%H:%M:%S') - (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1))).total_seconds()))[1:]} {MT_Seconds}.', f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')

                                                            await removeLines(7)
                                                            sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}cookies.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')
                                                            
                                                            dateOfMassMode1Refreshing     = datetime.datetime.now()
                                                            dateOfMassMode1RefreshingStrf = dateOfMassMode1Refreshing.strftime('%d.%m.%Y - %H.%M.%S')
                                                            
                                                            refreshTasks = []
                                                            for cookie in open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\cookies.txt', 'r', encoding='UTF-8').readlines():
                                                                refreshTask = asyncio.create_task(startMassModeRCR(cookie.strip(), dateOfMassMode1RefreshingStrf))
                                                                refreshTasks.append(refreshTask)
                                                                if len(refreshTasks) >= 50: break
                                                            
                                                            await asyncio.gather(*refreshTasks)

                                                            config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = dateOfMassMode1Refreshing.strftime('%H:%M:%S')
                                                            await AutoSaveConfig()
                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Finish_Checking_File}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
                                                            await waitingInput()
                                                            
                                                        await refresherMassModeOnly50Cookie()
                                                    case '2':
                                                        async def refresherMassModeMore50Cookie():
                                                            if config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] != '' and (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1)).time() > datetime.datetime.now().time():
                                                                return await errorOrCorrectHandler(True, 8, f'{MT_Wait} {str(int((datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'), '%H:%M:%S') - (datetime.datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%H:%M:%S') + datetime.timedelta(minutes=1))).total_seconds()))[1:]} {MT_Seconds}.', f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')

                                                            await removeLines(7)
                                                            sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}cookies.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')
                                                            
                                                            dateOfMassMode2Refreshing     = datetime.datetime.now()
                                                            dateOfMassMode2RefreshingStrf = dateOfMassMode2Refreshing.strftime('%d.%m.%Y - %H.%M.%S')
                                                            
                                                            cookieListAll = []
                                                            for cookie in open(f'Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt', 'r', encoding='UTF-8').readlines():
                                                                cookie = cookie.strip()
                                                                if search(COOKIE_PATTERN, cookie):
                                                                    cookieListAll.append(cookie)

                                                            while True:
                                                                refreshTasks = []
                                                                while len(cookieListAll) and len(refreshTasks) < 50:
                                                                    refreshTask = asyncio.create_task(startMassModeRCR(cookieListAll[0], dateOfMassMode2RefreshingStrf))
                                                                    refreshTasks.append(refreshTask)
                                                                    cookieListAll.remove(cookieListAll[0])
                                                                await asyncio.gather(*refreshTasks)

                                                                config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = dateOfMassMode2Refreshing.strftime('%H:%M:%S')
                                                                await AutoSaveConfig()
                                                                
                                                                if not len(cookieListAll):
                                                                    break
                                                            
                                                                sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Rate_Limit_Has_Been_Reached}. {MT_Waiting} 60 {MT_Seconds}... :<{ANSI.CLEAR}\n')
                                                                time.sleep(60)
                                                                await removeLines(1)

                                                            config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = dateOfMassMode2Refreshing.strftime('%H:%M:%S')
                                                            await AutoSaveConfig()
                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Finish_Checking_File}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
                                                            await waitingInput()
                                                            await cls()
                                                            await lableASCII()
                                                            
                                                        await refresherMassModeMore50Cookie()
                                                    case '0':
                                                        whileTrueStage3 = False
                                                        await removeLines(8)
                                                    case 'F' | 'А':
                                                        await cls()
                                                        await lableASCII()
                                                    case 'R' | 'К':
                                                        loadConfig(configLoader['Loader']['Current_Config'])
                                                        await cls()
                                                        await lableASCII()
                                                    case _:
                                                        await removeLines(8)
                                            except ValueError:
                                                config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = ''
                                                await AutoSaveConfig()
                                    case '0':
                                        whileTrueStage2 = False
                                await cls()
                                await lableASCII()
                        # Панель управлением куки
                        case '4':
                            whileTrueStage2 = True
                            await removeLines(11)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enter_A_Cookie2}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_History_Manual}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_History_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                cookieControlPanelCookieTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match cookieControlPanelCookieTab.upper():
                                    case '1':
                                        await removeLines(9)
                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                        cookieControlPanelCookieEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Cookie1}:{ANSI.CLEAR} ')

                                        async def cookieControlPanelManualEnter():
                                            if cookieControlPanelCookieEnter == '0': return
                                            if not search(COOKIE_PATTERN, cookieControlPanelCookieEnter):
                                                await cls()
                                                await lableASCII()
                                                return await errorOrCorrectHandler(True, 0, MT_Incorrect_Cookie, f'{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}')

                                            cookieRoblox  = {'.ROBLOSECURITY': cookieControlPanelCookieEnter}
                                            headersRoblox = None # {'User-Agent': ua.random}

                                            try:
                                                isAccountInformation = requests.get('https://www.roblox.com/my/settings/json', cookies=cookieRoblox).json()
                                            except requests.exceptions.JSONDecodeError:
                                                await cls()
                                                await lableASCII()
                                                return await errorOrCorrectHandler(True, 0, MT_Invalid_Cookie, f'{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}')

                                            isID = isAccountInformation['UserId']

                                            getGlobalsCheckListGamepasses()
                                            getGlobalsCheckListBadges()
                                            getGlobalCheckListCustomGamepasses()
                                            getGlobalCheckListFavoritePlaces()
                                            getGlobalCheckListBundles()
                                            
                                            isID, responseStatus, resultsRCC = await isResponseDataFromCookie(cookieRoblox, headersRoblox, 'roblox', None, True)
                                            
                                            if f'{cookieControlPanelCookieEnter[115:125]}...{cookieControlPanelCookieEnter[-10:-1]}' not in config['Roblox']['CookieControlPanel']['CookieControlPanelHistory']:
                                                config['Roblox']['CookieControlPanel']['CookieControlPanelHistory'][f'{cookieControlPanelCookieEnter[115:125]}...{cookieControlPanelCookieEnter[-10:-1]}'] = [resultsRCC[1][2] if resultsRCC[1][2] != '' else None, isID if config['Roblox']['CookieChecker']['Main']['ID'] else None, resultsRCC[2][2] if resultsRCC[2][2] != '' else None, resultsRCC[3][2] if resultsRCC[3][2] != '' else None, resultsRCC[4][2] if resultsRCC[4][2] != '' else None, resultsRCC[4][5] if resultsRCC[4][5] != '' else None, resultsRCC[5][2] if resultsRCC[5][2] != '' else None, resultsRCC[6][2] if resultsRCC[6][2] != '' else None, resultsRCC[7][2] if config['Roblox']['CookieChecker']['Main']['Pending'] else None, resultsRCC[7][3] if config['Roblox']['CookieChecker']['Main']['Donate'] else None, resultsRCC[8][2] if resultsRCC[8][2] != '' else None, resultsRCC[8][5] if resultsRCC[8][5] != '' else None, resultsRCC[9][2] if resultsRCC[9][2] != '' else None, resultsRCC[10][2] if resultsRCC[10][2] != '' else None, resultsRCC[11][2] if resultsRCC[11][2] != '' else None, resultsRCC[12][2] if resultsRCC[12][2] != '' else None, resultsRCC[13][2] if resultsRCC[13][2] != '' else None, resultsRCC[14][2] if resultsRCC[14][2] != '' else None, resultsRCC[15][2] if resultsRCC[15][2] != '' else None, resultsRCC[16][2] if resultsRCC[16][2] != '' else None, resultsRCC[17][2] if resultsRCC[17][2] != '' else None, resultsRCC[18][2] if resultsRCC[18][2] != '' else None, resultsRCC[19][2] if resultsRCC[19][2] != '' else None, resultsRCC[20][2] if resultsRCC[20][2] != '' else None, resultsRCC[21][2] if resultsRCC[21][2] != '' else None, resultsRCC[22][2] if resultsRCC[22][2] != '' else None, resultsRCC[23][2] if resultsRCC[23][2] != '' else None, resultsRCC[24][2] if resultsRCC[24][2] != '' else None, resultsRCC[25][2] if resultsRCC[25][2] != '' else None, resultsRCC[26][2] if resultsRCC[26][2] != '' else None, resultsRCC[27][2] if resultsRCC[27][2] != '' else None, resultsRCC[28][2] if resultsRCC[28][2] != '' else None, resultsRCC[29][2] if resultsRCC[29][2] != '' else None, resultsRCC[30][2] if resultsRCC[30][2] != '' else None, resultsRCC[31][2] if resultsRCC[31][2] != '' else None, cookieControlPanelCookieEnter]
                                                if config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually']:
                                                    await AutoSaveConfig()

                                            await cookieControlPanel('CookieControlPanelHistory', f'{cookieControlPanelCookieEnter[115:125]}...{cookieControlPanelCookieEnter[-10:-1]}', f'{MT_Cookie_Control_Panel}')

                                        await cookieControlPanelManualEnter()
                                        await cls()
                                        await lableASCII()
                                    case '2':
                                        await removeLines(9)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}\\{MT_History_Manual}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                            await printCCPCookiesInHistory('CookieControlPanelHistory')
                                            cookieControlPanelCookieManualHistoryFinderTab = input(f'{'  ┃\n' if config['Roblox']['CookieControlPanel']['CookieControlPanelHistory'] else ''} [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            if cookieControlPanelCookieManualHistoryFinderTab == '0': whileTrueStage3 = False
                                            elif cookieControlPanelCookieManualHistoryFinderTab.isdigit() and int(cookieControlPanelCookieManualHistoryFinderTab) <= len(config['Roblox']['CookieControlPanel']['CookieControlPanelHistory']):
                                                await cookieControlPanel('CookieControlPanelHistory', list(config['Roblox']['CookieControlPanel']['CookieControlPanelHistory'])[int(cookieControlPanelCookieManualHistoryFinderTab) - 1], f'{MT_Cookie_Control_Panel}\\{MT_History_Manual}')

                                            await cls()
                                            await lableASCII()
                                    case '3':
                                        await removeLines(9)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}\\{MT_History_Checker}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                            await printCCPCookiesInHistory('RobloxCookieCheckerHistory')
                                            cookieControlPanelCookieCheckerHistoryFinderTab = input(f'{'  ┃\n' if config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory'] else ''} [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            if cookieControlPanelCookieCheckerHistoryFinderTab == '0': whileTrueStage3 = False
                                            elif cookieControlPanelCookieCheckerHistoryFinderTab.isdigit() and int(cookieControlPanelCookieCheckerHistoryFinderTab) <= len(config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory']):
                                                await cookieControlPanel('RobloxCookieCheckerHistory', list(config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory'])[int(cookieControlPanelCookieCheckerHistoryFinderTab) - 1], f'{MT_Cookie_Control_Panel}\\{MT_History_Checker}')

                                            await cls()
                                            await lableASCII()
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(9)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:
                                        await removeLines(9)
                        # Разное
                        case '5':
                            whileTrueStage2 = True
                            columnarHeaders = [MT_Id, MT_Name, MT_Link]
                            await removeLines(11)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Misc}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses_Parser_From_The_Place}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges_Parser_From_The_Place}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Upload_All_Info_Gamepasses_And_Badges}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxMiscTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxMiscTab.upper():
                                    # Парсер геймпассов
                                    case '1':
                                        await removeLines(9)
                                        miscRobloxParseGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')

                                        async def parseRobloxGamepasses():
                                            if miscRobloxParseGamepassesTab == '0': return
                                            if not miscRobloxParseGamepassesTab.isdigit():
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,          f'{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}')
                                            if len(miscRobloxParseGamepassesTab) > 20:
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_20,  f'{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}')

                                            requestUniverseId = requests.get(f'https://apis.roblox.com/universes/v1/places/{miscRobloxParseGamepassesTab}/universe').json()['universeId']

                                            if requestUniverseId == None:
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,          f'{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}')

                                            requestGamepassesInfo = requests.get(f'https://games.roblox.com/v1/games/{requestUniverseId}/game-passes?limit=100&sortOrder=Asc').json()

                                            if not requestGamepassesInfo['data']:
                                                return await errorOrCorrectHandler(True, 5, MT_The_Place_Has_No_Gamepasses, f'{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}')

                                            requestGameInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={requestUniverseId}').json()
                                            placeNameWithoutSpecial = removeTwoSpaces(sub(r'[\\/:*?"<>|]', '', removeBracketsAndIn(replace_emoji(requestGameInfo['data'][0]['name'], replace=''), True, True))).strip()
                                            await removeLines(3)
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Found_Data_On} {miscRobloxParseGamepassesTab} ({placeNameWithoutSpecial}):\n\n')

                                            parsedGamepasses = []

                                            for gamepass in requestGamepassesInfo['data']:
                                                gamepassName = str(gamepass['name']).replace('\r', '').replace('\n', '')
                                                if config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name']:                gamepassName = replace_emoji(gamepassName, replace='')
                                                if config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name']:  gamepassName = removeBracketsAndIn(gamepassName, True, False)
                                                if config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name']: gamepassName = removeBracketsAndIn(gamepassName, False, True)
                                                parsedGamepasses.append([gamepass['id'], gamepassName, f'https://www.roblox.com/game-pass/{gamepass['id']}'])

                                            os.makedirs('Roblox\\Misc\\Gamepasses parser', exist_ok=True)
                                            open(f'Roblox\\Misc\\Gamepasses parser\\{miscRobloxParseGamepassesTab} ({placeNameWithoutSpecial}).txt', 'w', encoding='UTF-8').write(f'\n  Meow >:3\n\n  {MT_Place_ID}: {miscRobloxParseGamepassesTab}\n  {MT_Place_Name}: {requestGameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseGamepassesTab}\n\n  [*] {MT_Gamepasses}\n{columnar(parsedGamepasses, columnarHeaders, no_borders=True)}')
                                            sys.stdout.write(f'  {MT_Place_ID}: {miscRobloxParseGamepassesTab}\n  {MT_Place_Name}: {requestGameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseGamepassesTab}\n\n  [{ANSI.FG.GREEN}*{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.UNDERLINE1}{MT_Gamepasses}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n{columnar(parsedGamepasses, columnarHeaders, no_borders=True)}\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_The_Data_Is_Saved_In}: Misc\\Roblox\\Gamepasses parser\\{miscRobloxParseGamepassesTab} ({placeNameWithoutSpecial}).txt\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
                                            await waitingInput()

                                        await parseRobloxGamepasses()
                                        await cls()
                                        await lableASCII()
                                    # Парсер бейджей
                                    case '2':
                                        await removeLines(9)
                                        miscRobloxParseBadgesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')
                                        
                                        async def parseRobloxBadges():
                                            if miscRobloxParseBadgesTab == '0': return
                                            if not miscRobloxParseBadgesTab.isdigit():
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,         f'{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}')
                                            if len(miscRobloxParseBadgesTab) > 20:
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_20, f'{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}')

                                            requestUniverseId = requests.get(f'https://apis.roblox.com/universes/v1/places/{miscRobloxParseBadgesTab}/universe').json()['universeId']

                                            if requestUniverseId == None:
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,         f'{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}')

                                            requestBadgesInfo = requests.get(f'https://badges.roblox.com/v1/universes/{requestUniverseId}/badges?limit=100&sortOrder=Asc').json()

                                            if not requestBadgesInfo['data']:
                                                return await errorOrCorrectHandler(True, 5, MT_The_Place_Has_No_Badges,    f'{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}')

                                            requestGameInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={requestUniverseId}').json()
                                            placeNameWithoutSpecial = removeTwoSpaces(sub(r'[\/:*?"<>|]', '', removeBracketsAndIn(replace_emoji(requestGameInfo['data'][0]['name'], replace=''), True, True))).strip()

                                            await removeLines(3)
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Found_Data_On} {miscRobloxParseBadgesTab} ({placeNameWithoutSpecial}):\n\n')

                                            parsedBadges = []

                                            for badge in requestBadgesInfo['data']:
                                                badgeName = str(badge['name']).replace('\r', '').replace('\n', '')
                                                if config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name']:                badgeName = replace_emoji(badgeName, replace='')
                                                if config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name']:  badgeName = removeBracketsAndIn(badgeName, True, False)
                                                if config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name']: badgeName = removeBracketsAndIn(badgeName, False, True)
                                                parsedBadges.append([badge['id'], badgeName, f'https://www.roblox.com/badges/{badge['id']}'])

                                            os.makedirs('Roblox\\Misc\\Badges parser', exist_ok=True)
                                            open(f'Roblox\\Misc\\Badges parser\\{miscRobloxParseBadgesTab} ({placeNameWithoutSpecial}).txt', 'w', encoding='UTF-8').write(f'\n  Meow >:3\n\n  {MT_Place_ID}: {miscRobloxParseBadgesTab}\n  {MT_Place_Name}: {requestGameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseBadgesTab}\n\n  [*] {MT_Badges}\n{columnar(parsedBadges, columnarHeaders, no_borders=True)}')
                                            sys.stdout.write(f'  {MT_Place_ID}: {miscRobloxParseBadgesTab}\n  {MT_Place_Name}: {requestGameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseBadgesTab}\n\n  [{ANSI.FG.GREEN}*{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.UNDERLINE1}{MT_Badges}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n{columnar(parsedBadges, columnarHeaders, no_borders=True)}\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_The_Data_Is_Saved_In}: Misc\\Roblox\\Badges parser\\{miscRobloxParseBadgesTab} ({placeNameWithoutSpecial}).txt\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue if config['General']['Press_Any_Key_To_Continue'] else MT_Press_Enter_To_Continue}...{ANSI.CLEAR}')
                                            await waitingInput()

                                        await parseRobloxBadges()
                                        await cls()
                                        await lableASCII()
                                    # Выгрузка геймпассов и бейджей используемые скриптом
                                    case '3':
                                        for place in listOfPlaces:
                                            uploadAllGamepassesAndBadges = []
                                            if getattr(place, 'Gamepasses', False):
                                                for gamepass in place.Gamepasses.listOfGamepasses:
                                                    uploadAllGamepassesAndBadges.append([gamepass[1], gamepass[0], f'https://www.roblox.com/game-pass/{gamepass[1]}'])
                                                os.makedirs('Roblox\\Misc\\All gamepasses and badges from script\\Gamepasses', exist_ok=True)
                                                open(f'Roblox\\Misc\\All gamepasses and badges from script\\Gamepasses\\{place.placeNames[3]} ({sub(r'[\/:*?"<>|]', '', place.placeNames[0])}).txt', 'w', encoding='UTF-8').write(f'\n  Meow >:3\n\n  {MT_Place_ID}: {place.placeNames[3]}\n  {MT_Place_Name}: {place.placeNames[0]}\n  {MT_Place_Link}: https://www.roblox.com/games/{place.placeNames[3]}\n\n  [*] {MT_Gamepasses}\n{columnar(uploadAllGamepassesAndBadges, columnarHeaders, no_borders=True)}')
                                            uploadAllGamepassesAndBadges = []
                                            if getattr(place, 'Badges', False):
                                                for badge in place.Badges.listOfBadges:
                                                    uploadAllGamepassesAndBadges.append([badge[1], badge[0], f'https://www.roblox.com/badges/{badge[1]}'])
                                                os.makedirs('Roblox\\Misc\\All gamepasses and badges from script\\Badges', exist_ok=True)
                                                open(f'Roblox\\Misc\\All gamepasses and badges from script\\Badges\\{place.placeNames[3]} ({sub(r'[\/:*?"<>|]', '', place.placeNames[0])}).txt', 'w', encoding='UTF-8').write(f'\n  Meow >:3\n\n  {MT_Place_ID}: {place.placeNames[3]}\n  {MT_Place_Name}: {place.placeNames[0]}\n  {MT_Place_Link}: https://www.roblox.com/games/{place.placeNames[3]}\n\n  [*] {MT_Badges}\n{columnar(uploadAllGamepassesAndBadges, columnarHeaders, no_borders=True)}')    
                                        await errorOrCorrectHandler(False, 9, f'{MT_Successfully_Uploaded_In} \'Roblox\\Misc\\All gamepasses and badges from script\'', f'{MT_Roblox}\\{MT_Misc}')
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(9)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:
                                        await removeLines(9)
                        case '0':
                            whileTrueStage1 = False
                            await removeLines(11)
                        case 'F' | 'А':
                            await cls()
                            await lableASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                            await cls()
                            await lableASCII()
                        case _:
                            await removeLines(11)
            # Настройки
            case 'S' | 'Ы':
                whileTrueStage1 = True
                await removeLines(9)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Proxy}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Roblox}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Configs}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    settingsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match settingsTab.upper():
                        # Настройки - Общие
                        case '1':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_General}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Language}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Console_Title}: {config['General']['Console_Title'][:50]}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Show_Lable_MeowTool'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Lable_MeowTool}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Show_Lable_by_h1kken'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Lable_by_h1kken}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Key_To_Continue}: {MT_Any if config['General']['Press_Any_Key_To_Continue'] else 'Enter'}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Disable_All_Warnings'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Disable_All_Warnings}\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Fix_Console} ({MT_Bind}: F)\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                settingsGeneralTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match settingsGeneralTab.upper():
                                    # Общие - Язык
                                    case '1':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_General}\\{MT_Language}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if str(config['General']['Language']).upper() == 'RU' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} Русский\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if str(config['General']['Language']).upper() == 'EN' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} English\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsLanguageTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsLanguageTab.upper():
                                                case '1':
                                                    config['General']['Language'] = 'RU'
                                                    await AutoSaveConfig()
                                                    translateMT(config['General']['Language'])
                                                    await removeLines(8)
                                                case '2':
                                                    config['General']['Language'] = 'EN'
                                                    await AutoSaveConfig()
                                                    translateMT(config['General']['Language'])
                                                    await removeLines(8)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(8)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case _:
                                                    await removeLines(8)
                                    case '2':
                                        await removeLines(11)
                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_Not_Use_Characters_Such_As}: >, <, |, ^, &\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}\n\n')
                                        settingsTitleEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_New_Title}:{ANSI.CLEAR} ')
                                        
                                        async def changeConsoleTitle():
                                            if settingsTitleEnter == '0': return await removeLines(7)
                                            if settingsTitleEnter.replace(' ', '') == '':
                                                return await errorOrCorrectHandler(True, 7, MT_The_Name_Cannot_Be_Empty,                          f'{MT_Settings}\\{MT_General}')
                                            if len(settingsTitleEnter) > 50:
                                                return await errorOrCorrectHandler(True, 7, MT_Incorrect_Length_Of_Name_50,                       f'{MT_Settings}\\{MT_General}')
                                            if any(char in settingsTitleEnter for char in ['<', '>', '|', '^', '&']):
                                                return await errorOrCorrectHandler(True, 7, f'{MT_Do_Not_Use_Characters_Such_As}: <, >, |, ^, &', f'{MT_Settings}\\{MT_General}')

                                            os.system(f'title {settingsTitleEnter}')
                                            config['General']['Console_Title'] = settingsTitleEnter
                                            await AutoSaveConfig()
                                            await removeLines(7)
                                        
                                        await changeConsoleTitle()
                                    case '3':
                                        config['General']['Show_Lable_MeowTool'] = not config['General']['Show_Lable_MeowTool']
                                        await AutoSaveConfig()
                                        await cls()
                                        await lableASCII()
                                    case '4':
                                        config['General']['Show_Lable_by_h1kken'] = not config['General']['Show_Lable_by_h1kken']
                                        await AutoSaveConfig()
                                        await cls()
                                        await lableASCII()
                                    case '5':
                                        config['General']['Press_Any_Key_To_Continue'] = not config['General']['Press_Any_Key_To_Continue']
                                        await AutoSaveConfig()
                                        await removeLines(13)
                                    case '6':
                                        config['General']['Disable_All_Warnings'] = not config['General']['Disable_All_Warnings']
                                        await AutoSaveConfig()
                                        await removeLines(13)
                                    case '7' | 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(13)
                                    case _:
                                        await removeLines(13)
                        # Прокси
                        case '2':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Proxy}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                settingsProxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match settingsProxyTab.upper():
                                    # Прокси Чекер (PC)
                                    case '1':
                                        whileTrueStage3 = True
                                        await removeLines(7)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Proxy}\\{MT_Checker}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Waiting_Time}: {int(config['Proxy']['Checker']['Timeout'])} {MT_Seconds}.\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Proxy']['Checker']['Save_In_Custom_Folder'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_In} custom_valid.txt\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Proxy']['Checker']['Save_Without_Protocol'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Without_Protocol}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsPCTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsPCTab.upper():
                                                case '1':
                                                    await removeLines(9)
                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Proxy}\\{MT_Checker}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                    settingsPCTimeoutChange = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Waiting_Time}:{ANSI.CLEAR} ')

                                                    async def changeProxyTimeout():
                                                        if settingsPCTimeoutChange == '0': return
                                                        if not settingsPCTimeoutChange.isdigit():
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,        f'{MT_Settings}\\{MT_Proxy}\\{MT_Checker}')
                                                        if int(settingsPCTimeoutChange) > 3600:
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Waiting_Time, f'{MT_Settings}\\{MT_Proxy}\\{MT_Checker}')

                                                        config['Proxy']['Checker']['Timeout'] = int(settingsPCTimeoutChange)
                                                        await AutoSaveConfig()

                                                    await changeProxyTimeout()
                                                    await removeLines(5)
                                                case '2':
                                                    config['Proxy']['Checker']['Save_In_Custom_Folder'] = not config['Proxy']['Checker']['Save_In_Custom_Folder']
                                                    await AutoSaveConfig()
                                                    await removeLines(9)
                                                case '3':
                                                    config['Proxy']['Checker']['Save_Without_Protocol'] = not config['Proxy']['Checker']['Save_Without_Protocol']
                                                    await AutoSaveConfig()
                                                    await removeLines(9)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(9)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case _:
                                                    await removeLines(9)
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(7)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:
                                        await removeLines(7)
                        # Роблокс
                        case '3':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Parser}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Checker}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Refresher}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Control_Panel}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Misc}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                settingsRobloxTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match settingsRobloxTab.upper():
                                    # Роблокс Куки Парсер (RCP)
                                    case '1':
                                        whileTrueStage3 = True
                                        await removeLines(11)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Parser}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Save_To_A_File}: {config['Roblox']['CookieParser']['Save_To_A_File']}.txt\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRCPTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRCPTab.upper():
                                                case '1':
                                                    await removeLines(5)
                                                    newParserFilename = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Name_For_New_Config}:{ANSI.CLEAR} ')

                                                    async def changeParserFilename():
                                                        if newParserFilename == '0': return
                                                        if newParserFilename.strip() == '':
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,        f'{MT_Settings}\\{MT_Cookie_Parser}')
                                                        if any(char in newParserFilename for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name, f'{MT_Settings}\\{MT_Cookie_Parser}')

                                                        config['Roblox']['CookieParser']['Save_To_A_File'] = newParserFilename.replace('.txt', '')
                                                        await AutoSaveConfig()

                                                    await changeParserFilename()
                                                    await removeLines(5)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(7)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case _:
                                                    await removeLines(7)
                                    # Роблокс Куки Чекер (RCC)
                                    case '2':
                                        whileTrueStage3 = True
                                        await removeLines(11)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_General}\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Proxy}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting']['Sort'] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sorting}\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Main}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Places}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Custom_Places}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRCCTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRCCTab.upper():
                                                # Общие
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_First_Check_All_Cookies_For_Valid}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Number_Of_Threads_For_Valid_Checker}: {config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']) <= 500) else 5}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Send_Some_Requests_Through_RoProxy'] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send_Some_Requests_Through_RoProxy}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Output_Total'] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Output_Total}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Number_Of_Threads_For_Main_Checker}: {config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']) <= 500) else 5}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCGeneralTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCCGeneralTab.upper():
                                                            case '1':
                                                                config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] = not config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid']
                                                                await AutoSaveConfig()
                                                                await removeLines(11)
                                                            case '2':
                                                                whileTrueStage5 = True
                                                                await removeLines(11)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralValidThreadsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Number_Of_Threads}:{ANSI.CLEAR} ')
                                                                    
                                                                    async def changeNumberOfThreadsForValid():
                                                                        if settingsRCCGeneralValidThreadsTab == '0': return await removeLines(5)
                                                                        if not settingsRCCGeneralValidThreadsTab.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,             f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')
                                                                        if int(settingsRCCGeneralValidThreadsTab) > 500:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Number_Of_Threads, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')

                                                                        config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] = int(settingsRCCGeneralValidThreadsTab)
                                                                        await AutoSaveConfig()
                                                                        await removeLines(5)

                                                                    await changeNumberOfThreadsForValid()
                                                                    whileTrueStage5 = False
                                                            case '3':
                                                                config['Roblox']['CookieChecker']['General']['Send_Some_Requests_Through_RoProxy'] = not config['Roblox']['CookieChecker']['General']['Send_Some_Requests_Through_RoProxy']
                                                                await AutoSaveConfig()
                                                                await removeLines(11)
                                                            case '4':
                                                                config['Roblox']['CookieChecker']['General']['Output_Total'] = not config['Roblox']['CookieChecker']['General']['Output_Total']
                                                                await AutoSaveConfig()
                                                                await removeLines(11)
                                                            case '5':
                                                                whileTrueStage5 = True
                                                                await removeLines(11)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralCheckerThreadsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Number_Of_Threads}:{ANSI.CLEAR} ')
                                                                    
                                                                    async def changeNumberOfThreadsForChecker():
                                                                        if settingsRCCGeneralCheckerThreadsTab == '0': return await removeLines(5)
                                                                        if not settingsRCCGeneralCheckerThreadsTab.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,             f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')
                                                                        if int(settingsRCCGeneralCheckerThreadsTab) > 500:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Number_Of_Threads, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')

                                                                        config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] = int(settingsRCCGeneralCheckerThreadsTab)
                                                                        await AutoSaveConfig()
                                                                        await removeLines(5)

                                                                    await changeNumberOfThreadsForChecker()
                                                                    whileTrueStage5 = False
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(11)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                await cls()
                                                                await lableASCII()
                                                            case _:
                                                                await removeLines(11)
                                                # Прокси
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Proxy}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Use_Proxy}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Auto_Protocol_If_Not_Specified}: {config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] if config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] in ('http', 'socks4', 'socks5') else 'http'}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCProxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCCProxyTab.lower():
                                                            case '1':
                                                                config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy'] = not config['Roblox']['CookieChecker']['General']['Proxy']['Use_Proxy']
                                                                await AutoSaveConfig()
                                                                await removeLines(8)
                                                            case '2':
                                                                whileTrueStage4 = True
                                                                await removeLines(8)
                                                                while whileTrueStage4:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Proxy}\\{MT_Auto_Protocol}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'http' or config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] not in ('http', 'socks4', 'socks5') else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} http\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'socks4' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} socks4\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'socks5' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} socks5\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCProxyAutoProtocolTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    match settingsRCCProxyAutoProtocolTab.lower():
                                                                        case '1':
                                                                            config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
                                                                            await AutoSaveConfig()
                                                                            await removeLines(9)
                                                                        case '2':
                                                                            config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'socks4'
                                                                            await AutoSaveConfig()
                                                                            await removeLines(9)
                                                                        case '3':
                                                                            config['Roblox']['CookieChecker']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'socks5'
                                                                            await AutoSaveConfig()
                                                                            await removeLines(9)
                                                                        case '0':
                                                                            whileTrueStage4 = False
                                                                            await removeLines(9)
                                                                        case 'F' | 'А':
                                                                            await cls()
                                                                            await lableASCII()
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                            await removeLines(9)
                                                                        case _:
                                                                            await removeLines(9)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(8)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(8)
                                                # Сортировка
                                                case '3':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        global cookieDataCategories; cookieDataCategories = getCookieDataForSort()[0]
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}{ANSI.CLEAR}\n\n')
                                                        printSortCategories(cookieDataCategories)
                                                        sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting']['Sort'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sort}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCGeneralSortTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsRCCGeneralSortTab == '0': whileTrueStage4 = False
                                                        elif settingsRCCGeneralSortTab.isdigit() and int(settingsRCCGeneralSortTab) <= len(getCookieDataForSort()[0]):
                                                            if cookieDataCategories[list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]] == int:
                                                                whileTrueStage5 = True
                                                                await cls()
                                                                await lableASCII()
                                                                while whileTrueStage5:
                                                                    sortValues = await getSortValuesFromCategory(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1])
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}{ANSI.CLEAR}\n\n')
                                                                    await printSortValuesInCategory(sortValues, list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1])
                                                                    sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if sortValues else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_A_Parameter}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][0] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sort}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralSortCategoryTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    if settingsRCCGeneralSortCategoryTab == '0': whileTrueStage5 = False
                                                                    elif settingsRCCGeneralSortCategoryTab.isdigit() and int(settingsRCCGeneralSortCategoryTab) <= len(sortValues):
                                                                        whileTrueStage6 = True
                                                                        await cls()
                                                                        await lableASCII()
                                                                        while whileTrueStage6:
                                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}\\{sortValues[int(settingsRCCGeneralSortCategoryTab) - 1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValues[int(settingsRCCGeneralSortCategoryTab) - 1])][1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sort}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                            settingsRCCGeneralSortValueContextMenuTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                            match settingsRCCGeneralSortValueContextMenuTab.upper():
                                                                                case 'C' | 'С':
                                                                                    config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValues[int(settingsRCCGeneralSortCategoryTab) - 1])][1] = not config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValues[int(settingsRCCGeneralSortCategoryTab) - 1])][1]
                                                                                    await AutoSaveConfig()
                                                                                    await removeLines(7)
                                                                                case 'D' | 'В':
                                                                                    if not config['General']['Disable_All_Warnings']:
                                                                                        whileTrueStage7 = True
                                                                                        await removeLines(7)
                                                                                        while whileTrueStage7:
                                                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}\\{sortValues[int(settingsRCCGeneralSortCategoryTab) - 1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                                                                            confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                            match confirmTheAction.upper():
                                                                                                case 'Y' | 'Н':
                                                                                                    whileTrueStage6 = False
                                                                                                    whileTrueStage7 = False
                                                                                                    config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1].pop(int(settingsRCCGeneralSortCategoryTab) - 1)
                                                                                                    await AutoSaveConfig()
                                                                                                    await removeLines(8)
                                                                                                case 'N' | 'Т':
                                                                                                    whileTrueStage7 = False
                                                                                                    await removeLines(8)
                                                                                                case _:
                                                                                                    await removeLines(8)
                                                                                    else:
                                                                                        whileTrueStage6 = False
                                                                                        config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1].pop(int(settingsRCCGeneralSortCategoryTab) - 1)
                                                                                        await AutoSaveConfig()
                                                                                        await removeLines(7)
                                                                                case '0':
                                                                                    whileTrueStage6 = False
                                                                                    await removeLines(7)
                                                                                case 'F' | 'А':
                                                                                    await cls()
                                                                                    await lableASCII()
                                                                                case 'R' | 'К':
                                                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                                                    await cls()
                                                                                    await lableASCII()
                                                                                case _:
                                                                                    await removeLines(7)
                                                                    elif settingsRCCGeneralSortCategoryTab in ('+', '='):
                                                                        for sortValue in sortValues:
                                                                            config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValue)][1] = True
                                                                        await AutoSaveConfig()
                                                                    elif settingsRCCGeneralSortCategoryTab in ('-', '_'):
                                                                        for sortValue in sortValues:
                                                                            config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValue)][1] = False
                                                                        await AutoSaveConfig()
                                                                    elif settingsRCCGeneralSortCategoryTab.upper() in ('A', 'Ф'):
                                                                        await cls()
                                                                        await lableASCII()
                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                                        settingsRCCGeneralSortParameterAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Parameter_Value}:{ANSI.CLEAR} ')

                                                                        async def sortParameterAdd():
                                                                            if settingsRCCGeneralSortParameterAdd == '0': return
                                                                            if not settingsRCCGeneralSortParameterAdd.isdigit():
                                                                                return await errorOrCorrectHandler(True, 5, MT_The_Parameter_Can_Only_Be_A_Number,       f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}')
                                                                            if int(settingsRCCGeneralSortParameterAdd) in [parameter[0] for parameter in config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1]]:
                                                                                return await errorOrCorrectHandler(True, 5, MT_Parameter_With_This_Value_Already_Exists, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}')
                                                                            if len(str(settingsRCCGeneralSortParameterAdd)) > 20:
                                                                                return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Parameter_20,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}')

                                                                            config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1].append([int(settingsRCCGeneralSortParameterAdd), False])
                                                                            await AutoSaveConfig()

                                                                        await sortParameterAdd()
                                                                    elif settingsRCCGeneralSortCategoryTab.upper() in ('C', 'С'):
                                                                        config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][0] = not config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][0]
                                                                        await AutoSaveConfig()
                                                                    elif settingsRCCGeneralSortCategoryTab.upper() in ('R', 'К'):
                                                                        loadConfig(configLoader['Loader']['Current_Config'])

                                                                    await cls()
                                                                    await lableASCII()
                                                            elif cookieDataCategories[list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]] == bool:
                                                                config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]] = not config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]]
                                                            await AutoSaveConfig()
                                                        elif settingsRCCGeneralSortTab in ('+', '='):
                                                            for category in cookieDataCategories:
                                                                if   cookieDataCategories[category] == int and config['Roblox']['CookieChecker']['Sorting'][category][1]: config['Roblox']['CookieChecker']['Sorting'][category][0] = True
                                                                elif cookieDataCategories[category] == bool:                                                              config['Roblox']['CookieChecker']['Sorting'][category]    = True 
                                                            await AutoSaveConfig()
                                                        elif settingsRCCGeneralSortTab in ('-', '_'):
                                                            for category in cookieDataCategories:
                                                                if   cookieDataCategories[category] == int:  config['Roblox']['CookieChecker']['Sorting'][category][0] = False
                                                                elif cookieDataCategories[category] == bool: config['Roblox']['CookieChecker']['Sorting'][category]    = False 
                                                            await AutoSaveConfig()
                                                        elif settingsRCCGeneralSortTab.upper() in ('S', 'Ы'):
                                                            config['Roblox']['CookieChecker']['Sorting']['Sort'] = not config['Roblox']['CookieChecker']['Sorting']['Sort']
                                                            await AutoSaveConfig()
                                                        elif settingsRCCGeneralSortTab.upper() in ('R', 'К'):
                                                            loadConfig(configLoader['Loader']['Current_Config'])

                                                        await cls()
                                                        await lableASCII()
                                                # Основные
                                                case '4':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}{ANSI.CLEAR}\n\n  {ANSI.FG.RED}*{ANSI.CLEAR + ANSI.DECOR.BOLD}   - +1 {MT_Request.lower()}{ANSI.CLEAR}\n  {ANSI.FG.YELLOW}* {ANSI.FG.BLUE}*{ANSI.CLEAR + ANSI.DECOR.BOLD} - {MT_Everything_Or_Something_Is_On} +1 {MT_Request.lower()}{ANSI.CLEAR}\n  {ANSI.FG.GREEN}*{ANSI.CLEAR + ANSI.DECOR.BOLD}   - {MT_Everything_Is_On_Or_Off} +1 {MT_Request.lower()}{ANSI.CLEAR}\n\n')
                                                        printRCCGeneral()
                                                        sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCMainTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        # Custom Gamepasses
                                                        if settingsRCCMainTab == '0': whileTrueStage4 = False
                                                        elif settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData) and cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0] == 'Custom Gamepasses':
                                                            whileTrueStage4 = True
                                                            await cls()
                                                            await lableASCII()
                                                            while whileTrueStage4:
                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses\n\n{ANSI.CLEAR}')
                                                                RCCGeneralCustomGamepasses(True)
                                                                sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_A_Gamepass_Name}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                settingsRCCGeneralCustomGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                if settingsRCCGeneralCustomGamepassesTab == '0': whileTrueStage4 = False
                                                                elif settingsRCCGeneralCustomGamepassesTab.isdigit() and int(settingsRCCGeneralCustomGamepassesTab) <= len(config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names']):
                                                                    whileTrueStage5 = True
                                                                    await cls()
                                                                    await lableASCII()
                                                                    while whileTrueStage5:
                                                                        noDuplicatedCustomGamepasses = RCCGeneralCustomGamepasses()
                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses\\{noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][0]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                        settingsRCCGeneralCustomGamepassContextMenuTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                        match settingsRCCGeneralCustomGamepassContextMenuTab.upper():
                                                                            case 'C' | 'С':
                                                                                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'][int(settingsRCCGeneralCustomGamepassesTab) - 1][1] = not config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'][int(settingsRCCGeneralCustomGamepassesTab) - 1][1]
                                                                                await AutoSaveConfig()
                                                                                await removeLines(7)
                                                                            case 'D' | 'В':
                                                                                if not config['General']['Disable_All_Warnings']:
                                                                                    whileTrueStage6 = True
                                                                                    await removeLines(7)
                                                                                    while whileTrueStage6:
                                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses\\{noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][0]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                                                                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                        match confirmTheAction.upper():
                                                                                            case 'Y' | 'Н':
                                                                                                whileTrueStage5 = False
                                                                                                whileTrueStage6 = False
                                                                                                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'].remove([noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][0], noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][1]])
                                                                                                await AutoSaveConfig()
                                                                                                await removeLines(8)
                                                                                            case 'N' | 'Т':
                                                                                                whileTrueStage6 = False
                                                                                                await removeLines(8)
                                                                                            case _:
                                                                                                await removeLines(8)
                                                                                else:
                                                                                    whileTrueStage5 = False
                                                                                    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'].remove([noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][0], noDuplicatedCustomGamepasses[int(settingsRCCGeneralCustomGamepassesTab) - 1][1]])
                                                                                    await AutoSaveConfig()
                                                                                    await removeLines(7)
                                                                            case '0':
                                                                                whileTrueStage5 = False
                                                                                await removeLines(7)
                                                                            case 'F' | 'А':
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case 'R' | 'К':
                                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case _:
                                                                                await removeLines(7)
                                                                elif settingsRCCGeneralCustomGamepassesTab.upper() in ('A', 'Ф'):
                                                                    await cls()
                                                                    await lableASCII()
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralCustomGamepassesAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Gamepass_Name}:{ANSI.CLEAR} ')

                                                                    async def addCustomGamepass():
                                                                        if settingsRCCGeneralCustomGamepassesAdd == '0': return
                                                                        if settingsRCCGeneralCustomGamepassesAdd.replace(' ', '') == '':
                                                                            return await errorOrCorrectHandler(True, 5, MT_The_Name_Cannot_Be_Empty,               f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses')
                                                                        if len(settingsRCCGeneralCustomGamepassesAdd) > 50:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Name_50,            f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses')
                                                                        if checkDuplicates(settingsRCCGeneralCustomGamepassesAdd, 'Custom_Gamepasses_Names'):
                                                                            return await errorOrCorrectHandler(True, 5, MT_Gamepass_With_This_Name_Already_Exists, f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\Custom Gamepasses')

                                                                        config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'].append([settingsRCCGeneralCustomGamepassesAdd, True])
                                                                        await AutoSaveConfig()

                                                                    await addCustomGamepass()
                                                                elif settingsRCCGeneralCustomGamepassesTab in ('+', '='):
                                                                    for i in range(len(config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'])):
                                                                        config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'][i][1] = True
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralCustomGamepassesTab in ('-', '_'):
                                                                    for i in range(len(config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'])):
                                                                        config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Names'][i][1] = False
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralCustomGamepassesTab.upper() in ('C', 'С'):
                                                                    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] = not config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralCustomGamepassesTab.upper() in ('R', 'К'):
                                                                    loadConfig(configLoader['Loader']['Current_Config'])

                                                                await cls()
                                                                await lableASCII()
                                                        # Favorite Places
                                                        elif settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData) and cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0] == 'Favorite Places':
                                                            whileTrueStage4 = True
                                                            await cls()
                                                            await lableASCII()
                                                            while whileTrueStage4:
                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places\n\n{ANSI.CLEAR}')
                                                                RCCGeneralFavPlaces(True)
                                                                sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_ID_Place}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Main']['Favorite_Places'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                settingsRCCGeneralFavPlacesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                if settingsRCCGeneralFavPlacesTab == '0': whileTrueStage4 = False
                                                                elif settingsRCCGeneralFavPlacesTab.isdigit() and int(settingsRCCGeneralFavPlacesTab) <= len(config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs']):
                                                                    whileTrueStage5 = True
                                                                    await cls()
                                                                    await lableASCII()
                                                                    while whileTrueStage5:
                                                                        noDuplicatedFavoritePlaces = RCCGeneralFavPlaces()
                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places\\{noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][0]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                        settingsRCCGeneralFavPlaceContextMenuTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                        match settingsRCCGeneralFavPlaceContextMenuTab.upper():
                                                                            case 'C' | 'С':
                                                                                config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'][int(settingsRCCGeneralFavPlacesTab) - 1][2] = not config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'][int(settingsRCCGeneralFavPlacesTab) - 1][2]
                                                                                await AutoSaveConfig()
                                                                                await removeLines(7)
                                                                            case 'D' | 'В':
                                                                                if not config['General']['Disable_All_Warnings']:
                                                                                    whileTrueStage6 = True
                                                                                    await removeLines(7)
                                                                                    while whileTrueStage6:
                                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places\\{noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][0]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                                                                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                        match confirmTheAction.upper():
                                                                                            case 'Y' | 'Н':
                                                                                                whileTrueStage5 = False
                                                                                                whileTrueStage6 = False
                                                                                                config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'].remove([noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][0], noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][1], noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][2]])
                                                                                                await AutoSaveConfig()
                                                                                                await removeLines(8)
                                                                                            case 'N' | 'Т':
                                                                                                whileTrueStage6 = False
                                                                                                await removeLines(8)
                                                                                            case _:
                                                                                                await removeLines(8)
                                                                                else:
                                                                                    whileTrueStage5 = False
                                                                                    config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'].remove([noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][0], noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][1], noDuplicatedFavoritePlaces[int(settingsRCCGeneralFavPlacesTab) - 1][2]])
                                                                                    await AutoSaveConfig()
                                                                                    await removeLines(7)
                                                                            case '0':
                                                                                whileTrueStage5 = False
                                                                                await removeLines(7)
                                                                            case 'F' | 'А':
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case 'R' | 'К':
                                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case _:
                                                                                await removeLines(7)
                                                                elif settingsRCCGeneralFavPlacesTab.upper() in ('A', 'Ф'):
                                                                    await cls()
                                                                    await lableASCII()
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralFavPlacesAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')

                                                                    async def addFavPlace():
                                                                        if settingsRCCGeneralFavPlacesAdd == '0': return
                                                                        if not settingsRCCGeneralFavPlacesAdd.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                          f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')
                                                                        if len(settingsRCCGeneralFavPlacesAdd) > 20:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_20,                  f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')
                                                                        if checkDuplicates(settingsRCCGeneralFavPlacesAdd, 'Favorite_Places_IDs'):
                                                                            return await errorOrCorrectHandler(True, 5, MT_Place_With_This_ID_Already_Exists,           f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')

                                                                        requestUniverseId = requests.get(f'https://apis.roblox.com/universes/v1/places/{settingsRCCGeneralFavPlacesAdd}/universe').json()['universeId']

                                                                        if requestUniverseId == None:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                          f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')

                                                                        requestFavPlaceInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={requestUniverseId}').json()

                                                                        config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'].append([int(settingsRCCGeneralFavPlacesAdd), requestFavPlaceInfo['data'][0]['name'], True])
                                                                        await AutoSaveConfig()

                                                                    await addFavPlace()
                                                                elif settingsRCCGeneralFavPlacesTab in ('+', '='):
                                                                    for i in range(len(config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'])):
                                                                        config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'][i][2] = True
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralFavPlacesTab in ('-', '_'):
                                                                    for i in range(len(config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'])):
                                                                        config['Roblox']['CookieChecker']['Main']['Favorite_Places_IDs'][i][2] = False
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralFavPlacesTab.upper() in ('C', 'С'):
                                                                    config['Roblox']['CookieChecker']['Main']['Favorite_Places'] = not config['Roblox']['CookieChecker']['Main']['Favorite_Places']
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralFavPlacesTab.upper() in ('R', 'К'):
                                                                    loadConfig(configLoader['Loader']['Current_Config'])

                                                                await cls()
                                                                await lableASCII()

                                                        # Bundles
                                                        elif settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData) and cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0] == 'Bundles':
                                                            whileTrueStage4 = True
                                                            await cls()
                                                            await lableASCII()
                                                            while whileTrueStage4:
                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles\n\n{ANSI.CLEAR}')
                                                                RCCGeneralBundles(True)
                                                                sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['Main']['Bundles_IDs'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_Bundle}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Main']['Bundles'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                settingsRCCGeneralBundlesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                if settingsRCCGeneralBundlesTab == '0': whileTrueStage4 = False
                                                                elif settingsRCCGeneralBundlesTab.isdigit() and int(settingsRCCGeneralBundlesTab) <= len(config['Roblox']['CookieChecker']['Main']['Bundles_IDs']):
                                                                    whileTrueStage5 = True
                                                                    await cls()
                                                                    await lableASCII()
                                                                    while whileTrueStage5:
                                                                        noDuplicatedBundles = RCCGeneralBundles()
                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles\\{noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][0]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                        settingsRCCGeneralBundleContextMenuTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                        match settingsRCCGeneralBundleContextMenuTab.upper():
                                                                            case 'C' | 'С':
                                                                                config['Roblox']['CookieChecker']['Main']['Bundles_IDs'][int(settingsRCCGeneralBundlesTab) - 1][2] = not config['Roblox']['CookieChecker']['Main']['Bundles_IDs'][int(settingsRCCGeneralBundlesTab) - 1][2]
                                                                                await AutoSaveConfig()
                                                                                await removeLines(7)
                                                                            case 'D' | 'В':
                                                                                if not config['General']['Disable_All_Warnings']:
                                                                                    whileTrueStage6 = True
                                                                                    await removeLines(7)
                                                                                    while whileTrueStage6:
                                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles\\{noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][0]}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                                                                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                        match confirmTheAction.upper():
                                                                                            case 'Y' | 'Н':
                                                                                                whileTrueStage5 = False
                                                                                                whileTrueStage6 = False
                                                                                                config['Roblox']['CookieChecker']['Main']['Bundles_IDs'].remove([noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][0], noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][1], noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][2]])
                                                                                                await AutoSaveConfig()
                                                                                                await removeLines(8)
                                                                                            case 'N' | 'Т':
                                                                                                whileTrueStage6 = False
                                                                                                await removeLines(8)
                                                                                            case _:
                                                                                                await removeLines(8)
                                                                                else:
                                                                                    whileTrueStage5 = False
                                                                                    config['Roblox']['CookieChecker']['Main']['Bundles_IDs'].remove([noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][0], noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][1], noDuplicatedBundles[int(settingsRCCGeneralBundlesTab) - 1][2]])
                                                                                    await AutoSaveConfig()
                                                                                    await removeLines(7)
                                                                            case '0':
                                                                                whileTrueStage5 = False
                                                                                await removeLines(7)
                                                                            case 'F' | 'А':
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case 'R' | 'К':
                                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case _:
                                                                                await removeLines(7)
                                                                elif settingsRCCGeneralBundlesTab.upper() in ('A', 'Ф'):
                                                                    await cls()
                                                                    await lableASCII()
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralBundlesAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Bundle_ID}:{ANSI.CLEAR} ')

                                                                    async def addBundle():
                                                                        if settingsRCCGeneralBundlesAdd == '0': return
                                                                        if not settingsRCCGeneralBundlesAdd.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrent_Bundle_ID,                 f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')
                                                                        if len(settingsRCCGeneralBundlesAdd) > 20:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_20,           f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')
                                                                        if checkDuplicates(settingsRCCGeneralBundlesAdd, 'Bundles_IDs'):
                                                                            return await errorOrCorrectHandler(True, 5, MT_Bundle_With_This_ID_Already_Exists,  f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')

                                                                        requestBundleInfo = requests.get(f'https://catalog.roblox.com/v1/bundles/{settingsRCCGeneralBundlesAdd}/details').json()

                                                                        if 'errors' in requestBundleInfo:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrent_Bundle_ID,                 f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')

                                                                        config['Roblox']['CookieChecker']['Main']['Bundles_IDs'].append([int(settingsRCCGeneralBundlesAdd), requestBundleInfo['name'], True])
                                                                        await AutoSaveConfig()

                                                                    await addBundle()
                                                                elif settingsRCCGeneralBundlesTab in ('+', '='):
                                                                    for i in range(len(config['Roblox']['CookieChecker']['Main']['Bundles_IDs'])):
                                                                        config['Roblox']['CookieChecker']['Main']['Bundles_IDs'][i][2] = True
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralBundlesTab in ('-', '_'):
                                                                    for i in range(len(config['Roblox']['CookieChecker']['Main']['Bundles_IDs'])):
                                                                        config['Roblox']['CookieChecker']['Main']['Bundles_IDs'][i][2] = False
                                                                    await AutoSaveConfig()
                                                                elif settingsRCCGeneralBundlesTab.upper() in ('C', 'С'):
                                                                    config['Roblox']['CookieChecker']['Main']['Bundles'] = not config['Roblox']['CookieChecker']['Main']['Bundles']
                                                                    await AutoSaveConfig()

                                                                await cls()
                                                                await lableASCII()
                                                        elif settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData):
                                                            config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][1]] = not config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][1]]
                                                            await AutoSaveConfig()
                                                        elif settingsRCCMainTab in ('+', '='):
                                                            for i in range(len(cookieData.listOfCookieData)):
                                                                config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[i][1]] = True
                                                            await AutoSaveConfig()
                                                        elif settingsRCCMainTab in ('-', '_'):
                                                            for i in range(len(cookieData.listOfCookieData)):
                                                                config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[i][1]] = False
                                                            await AutoSaveConfig()

                                                        await cls()
                                                        await lableASCII()
                                                # Плейсы
                                                case '5':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                                        printRCCPlaces()
                                                        sys.stdout.write(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCPlacesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsRCCPlacesTab == '0': whileTrueStage4 = False
                                                        elif settingsRCCPlacesTab.isdigit() and int(settingsRCCPlacesTab) <= len(listOfPlaces):
                                                            await placeContextMenu(int(settingsRCCPlacesTab) - 1)
                                                        elif settingsRCCPlacesTab in ('+', '='):
                                                            for place in listOfPlaces:
                                                                config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = True
                                                            await AutoSaveConfig()
                                                        elif settingsRCCPlacesTab in ('-', '_'):
                                                            for place in listOfPlaces:
                                                                config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = False
                                                            await AutoSaveConfig()

                                                        await cls()
                                                        await lableASCII()
                                                # Кастомные плейсы
                                                case '6':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                                        await printRCCCustomPlaces()
                                                        sys.stdout.write(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_ID_Place}\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Place_ID_Next_To_The_Name}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCCustomPlacesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsRCCCustomPlacesTab == '0': whileTrueStage4 = False
                                                        elif settingsRCCCustomPlacesTab.isdigit() and int(settingsRCCCustomPlacesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']):
                                                            await customPlaceContextMenu(int(settingsRCCCustomPlacesTab) - 1)
                                                        elif settingsRCCCustomPlacesTab in ('+', '='):
                                                            for place in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                try: config['Roblox']['CookieChecker']['CustomPlaces'][str(place)][0] = True
                                                                except Exception: pass
                                                            await AutoSaveConfig()
                                                        elif settingsRCCCustomPlacesTab in ('-', '_'):
                                                            for place in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                try: config['Roblox']['CookieChecker']['CustomPlaces'][str(place)][0] = False
                                                                except Exception: pass
                                                            await AutoSaveConfig()
                                                        elif settingsRCCCustomPlacesTab.upper() in ('A', 'Ф'):
                                                            await cls()
                                                            await lableASCII()
                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                            settingsRCCCustomPlaceAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')

                                                            async def addCustomPlace():
                                                                if settingsRCCCustomPlaceAdd == '0': return
                                                                if not settingsRCCCustomPlaceAdd.isdigit():
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                         f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')
                                                                if len(settingsRCCCustomPlaceAdd) > 20:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_20,                 f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')
                                                                if int(settingsRCCCustomPlaceAdd) in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Place_With_This_ID_Already_Exists,          f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')

                                                                requestUniverseId = requests.get(f'https://apis.roblox.com/universes/v1/places/{settingsRCCCustomPlaceAdd}/universe').json()['universeId']

                                                                if requestUniverseId == None:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                         f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')

                                                                requestCustomPlaceGamepasses = requests.get(f'https://games.roblox.com/v1/games/{requestUniverseId}/game-passes?limit=100&sortOrder=Asc').json()
                                                                requestCustomPlaceBadges     = requests.get(f'https://badges.roblox.com/v1/universes/{requestUniverseId}/badges?limit=100&sortOrder=Asc').json()

                                                                if not requestCustomPlaceGamepasses['data'] and not requestCustomPlaceBadges['data']:
                                                                    return await errorOrCorrectHandler(True, 5, MT_The_Place_Has_No_Gamepasses_And_Badges,     f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')

                                                                requestCustomPlaceInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={requestUniverseId}').json()

                                                                normalPlaceName = str(removeSpecialCharsAndOrEmojies(removeBracketsAndIn(requestCustomPlaceInfo['data'][0]['name'], True, True), False, True)).strip()
                                                                if normalPlaceName != '':
                                                                    abbreviatedPlaceName = ''
                                                                    for word in normalPlaceName.split():
                                                                        abbreviatedPlaceName += word[0]
                                                                else:
                                                                    normalPlaceName      = f'Unknown_Normal_{settingsRCCCustomPlaceAdd}'
                                                                    abbreviatedPlaceName = f'UNK_{settingsRCCCustomPlaceAdd[:5]}'

                                                                config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].append(int(settingsRCCCustomPlaceAdd))

                                                                config['Roblox']['CookieChecker']['CustomPlaces'][settingsRCCCustomPlaceAdd] = [False, int(settingsRCCCustomPlaceAdd), [normalPlaceName, str(requestCustomPlaceInfo['data'][0]['name']).strip(), abbreviatedPlaceName.upper()]]
                                                                if requestCustomPlaceGamepasses['data']: config['Roblox']['CookieChecker']['CustomPlaces'][f'{settingsRCCCustomPlaceAdd}_Gamepasses'] = [[gamepass['id'], str(gamepass['name']).strip(), False] for gamepass in requestCustomPlaceGamepasses['data']]
                                                                if requestCustomPlaceBadges['data']:     config['Roblox']['CookieChecker']['CustomPlaces'][f'{settingsRCCCustomPlaceAdd}_Badges']     = [[badge['id'],    str(badge['name']).strip(),    False] for badge in requestCustomPlaceBadges['data']]

                                                                await AutoSaveConfig()

                                                            await addCustomPlace()
                                                        elif settingsRCCCustomPlacesTab.upper() in ('S', 'Ы'):
                                                            config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] = not config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name']
                                                            await AutoSaveConfig()

                                                        await cls()
                                                        await lableASCII()
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(12)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case _:
                                                    await removeLines(12)
                                    # Роблокс Куки Рефрешер (RCR)
                                    case '3':
                                        whileTrueStage3 = True
                                        await removeLines(11)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Refresher}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Single_Mode}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Mass_Mode}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRCPTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRCPTab.upper():
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 1 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'_XXXXXXXXX...XXXXXXXXX -> {MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_1.txt\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 2 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_2.txt\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 3 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed cookies\\_XXXXXXXXX...XXXXXXXXX.txt\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCPSingleModeTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCPSingleModeTab.upper():
                                                            case '1':
                                                                if 1 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                                    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].remove(1)
                                                                else:
                                                                    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].append(1)
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '2':
                                                                if 2 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                                    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].remove(2)
                                                                else:
                                                                    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].append(2)
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '3':
                                                                if 3 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                                    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].remove(3)
                                                                else:
                                                                    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].append(3)
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(9)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                await cls()
                                                                await lableASCII()
                                                            case _:
                                                                await removeLines(9)
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 1 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'_XXXXXXXXX...XXXXXXXXX -> {MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_1.txt\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 2 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_2.txt\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 3 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed cookies\\_XXXXXXXXX...XXXXXXXXX.txt\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Invalid_Cookies}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCPMassModeTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCPMassModeTab.upper():
                                                            case '1':
                                                                if 1 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
                                                                    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].remove(1)
                                                                else:
                                                                    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].append(1)
                                                                await AutoSaveConfig()
                                                                await removeLines(10)
                                                            case '2':
                                                                if 2 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
                                                                    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].remove(2)
                                                                else:
                                                                    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].append(2)
                                                                await AutoSaveConfig()
                                                                await removeLines(10)
                                                            case '3':
                                                                if 3 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
                                                                    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].remove(3)
                                                                else:
                                                                    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].append(3)
                                                                await AutoSaveConfig()
                                                                await removeLines(10)
                                                            case '4':
                                                                config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies'] = not config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies']
                                                                await AutoSaveConfig()
                                                                await removeLines(10)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(10)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                await cls()
                                                                await lableASCII()
                                                            case _:
                                                                await removeLines(10)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(8)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case _:
                                                    await removeLines(8)
                                    # Панель управления куком
                                    case '4':
                                        whileTrueStage3 = True
                                        await removeLines(11)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Cookies_Added_Manually}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Cookies_Checked_By_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsCookieControlPanelTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsCookieControlPanelTab.upper():
                                                case '1':
                                                    config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually'] = not config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually']
                                                    await AutoSaveConfig()
                                                    await removeLines(8)
                                                case '2':
                                                    config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker'] = not config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker']
                                                    await AutoSaveConfig()
                                                    await removeLines(8)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(8)
                                                case _:
                                                    await removeLines(8)
                                    # Разное
                                    case '5':
                                        whileTrueStage3 = True
                                        await removeLines(11)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Misc}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses_Parser_From_The_Place}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges_Parser_From_The_Place}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRobloxMiscTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRobloxMiscTab.upper():
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Emojies}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Round_Brackets}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Square_Brackets}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        miscRobloxGamepassesParserTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match miscRobloxGamepassesParserTab.upper():
                                                            case '1':
                                                                config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name'] = not config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name']
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '2':
                                                                config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name'] = not config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name']
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '3':
                                                                config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name'] = not config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name']
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                await cls()
                                                                await lableASCII()
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(9)
                                                            case _:
                                                                await removeLines(9)
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Emojies}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Round_Brackets}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Square_Brackets}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        miscRobloxBadgesParserTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match miscRobloxBadgesParserTab.upper():
                                                            case '1':
                                                                config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name'] = not config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name']
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '2':
                                                                config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name'] = not config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name']
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case '3':
                                                                config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name'] = not config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name']
                                                                await AutoSaveConfig()
                                                                await removeLines(9)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                await cls()
                                                                await lableASCII()
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(9)
                                                            case _:
                                                                await removeLines(9)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(8)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await cls()
                                                    await lableASCII()
                                                case _:
                                                    await removeLines(8)
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(11)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await cls()
                                        await lableASCII()
                                    case _:
                                        await removeLines(11)
                        # Настройки - Конфиги
                        case '4':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Configs}\n\n')
                                printConfigs(configFiles())
                                sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}R{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Reload_Config} ({MT_Bind}: R)\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Saver']['Auto_Save_Changes'] else f'{ANSI.DECOR.BOLD}[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Auto_Save_Changes}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Create_Config}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                configsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                if configsTab == '0': whileTrueStage2 = False
                                elif configsTab.isdigit() and int(configsTab) <= len(configFiles()):
                                    await configContextMenu(int(configsTab) - 1)
                                elif configsTab.upper() in ('C', 'С'):
                                    await cls()
                                    await lableASCII()

                                    nameOfNewConfig = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{MT_Settings}\\{MT_Configs}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Name_For_New_Config}:{ANSI.CLEAR} ')
                                    
                                    async def createConfig():
                                        if nameOfNewConfig == '0': return
                                        if len(nameOfNewConfig) > 60:
                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Config_Name_60, f'{MT_Settings}\\{MT_Configs}')
                                        if f'{nameOfNewConfig.lower()}' in {str(file).lower() for file in configFiles()}:
                                            return await errorOrCorrectHandler(True, 5, MT_File_With_This_Name_Already_Exists, f'{MT_Settings}\\{MT_Configs}')
                                        if any(char in nameOfNewConfig for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,                f'{MT_Settings}\\{MT_Configs}')

                                        copyfile(f'Settings\\Configs\\{configLoader['Loader']['Current_Config']}.toml', f'Settings\\Configs\\{nameOfNewConfig}.toml')
                                        loadConfig(nameOfNewConfig)
                                        await AutoSaveConfig()
                                    
                                    await createConfig()
                                elif configsTab.upper() in ('S', 'Ы'):
                                    configLoader['Saver']['Auto_Save_Changes'] = not configLoader['Saver']['Auto_Save_Changes']
                                    open(f'Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
                                    await AutoSaveConfig()
                                elif configsTab.upper() in ('R', 'К'):
                                    loadConfig(configLoader['Loader']['Current_Config'])

                                await cls()
                                await lableASCII()
                        case '0':
                            whileTrueStage1 = False
                            await removeLines(10)
                        case 'F' | 'А':
                            await cls()
                            await lableASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                            await cls()
                            await lableASCII()
                        case _:
                            await removeLines(10)
            # Закрыть программу
            case '0':
                if not config['General']['Disable_All_Warnings']:
                    whileTrueStage1 = True
                    await removeLines(9)
                    while whileTrueStage1:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}MeowTool:\\{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                sys.exit()
                            case 'N' | 'Т':
                                whileTrueStage1 = False
                                await removeLines(8)
                            case _:
                                await removeLines(8)
                else:
                    sys.exit()
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case 'R' | 'К':
                loadConfig(configLoader['Loader']['Current_Config'])
                await cls()
                await lableASCII()
            case _:
                await removeLines(9)

if __name__ == '__main__':
    sys.stdout.write('\r Настраиваемся к комфорту и уюту... >:3')
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    sys.stdout.write('\r Сортируем папки по полочкам... >:3    ')
    neededFoldersAndFiles()
    sys.stdout.write('\r Мило просим у конфига настройки... >:3')
    loadConfigLoader()
    sys.stdout.write('\r Надеемся на честность переводов... >:3')
    translateMT(config['General']['Language'])
    sys.stdout.write('\r Почти готово, ещё парочку часов... >:3')
    asyncio.run(mainMenu())