class Env:
    API_TOKEN = "" #PUT YOUR API TOKEN HERE
    DBHST = "" #PUT YOUR DATABASE HOST HERE
    DBUSR = "" #PUT YOUR DATABASE USER HERE
    DBPWD = "" #PUT YOUR DATABASE PWD HERE

class LoadOrder:
    COGS = [
        "Debug.logging",
        "Utilities.events",
        "Utilities.data",
        "Utilities.embeds",
        "Debug.debugmethods",
        "Debug.debugcommands",
        "Utilities.utilities",
        "Utilities.verification",
        "Admin.adminmethods",
        "Admin.admincommands",
        "Bundle.bundlemethods",
        "Bundle.bundlecommands",
        "Help.helpmethods",
        "Help.helpcommands",
        "User.usermethods",
        "User.usercommands",
    ]

class LoggingDefaults:
    NAME = "Exophose"
    CHANNEL = 0 #PUT YOUR LOG CHANNEL ID HERE
    PING = 0 #PUT YOUR USER ID HERE
    COG_COUNT = len(LoadOrder.COGS)

class EmbedDefaults:
    WHITE = 0xFFFFFF
    GREEN = 0x00CC00
    RED = 0xCC0000
    TEMP_IMG_CHANNEL = 0 #PUT YOUR TEMPORARY IMAGE CHANNEL ID HERE

class HelpDefaults:
    HELP_OPTIONS = [
        "About Exophose",
        "Custom Roles",
        "Bundle Roles",
        "Custom Configuration",
        "Bundle Configuration",
    ]

    COLOR = EmbedDefaults.WHITE
    AUTHOR = LoggingDefaults.PING
    APP_DIRECTORY = "[See it for yourself](https://discord.com/application-directory/854906458344259615)"
    SUPPORT_SERVER = "[For updates, feedback & issues](https://discord.gg/dAabxGzned)"
    SUPPORT_ME = "[It's entirely optional](https://ko-fi.com/hookens)"

class DebugLists:
    GUILDS = [
        0, #PUT YOUR DEBUG GUILD ID HERE
    ]

    COGS = [
        "AdminCommands",
        "AdminMethods",
        "BundleCommands",
        "BundleMethods",
        "DebugCommands",
        "DebugMethods",
        "Logging",
        "HelpCommands",
        "HelpMethods",
        "UserCommands",
        "UserMethods",
        "Data",
        "Embeds",
        "Events",
        "Utilities",
        "Verification",
    ]

class AdminTexts:
    C_ALLOW = "Allow a role to use role management commands."
    C_DISALLOW = "Disallow a role from using role management commands."
    C_ALLOWED = "List allowed roles."

    F_ALLOWROLE = "Role to allow."
    F_DISALLOWROLE = "Role to disallow."
    F_MAX = "Maximum number of roles that a user with that role can create."
    F_GRADIENTS = "Can use enhanced role styles."
    F_BADGES = "Can add custom badges."
    F_PUBLIC = "Make this message public."

class BundleTexts:
    CHOICES = [
        "Add", 
        "Remove",
    ]


    C_CREATE = "Create an empty bundle."
    C_LIST = "List created bundles, their roles, and which roles are allowed."
    C_EDIT = "Add or remove a role in a bundle."
    C_DELETE = "Deletes a bundle and its associations. This operation is irreversible."
    C_ALLOW = "Allow a role to use a bundle."
    C_DISALLOW = "Disallow a role from using a bundle."

    F_NAME = "Name of the bundle."
    F_ACTION = "Edition action for the bundle."
    F_ROLE = "Role to add or remove."
    F_INDEX = "Index of the bundle. Refer to the bundle list."
    F_CONFIRM = "Confirm the name of the bundle."
    F_ALLOWROLE = AdminTexts.F_ALLOWROLE
    F_DISALLOWROLE = AdminTexts.F_DISALLOWROLE


    C_CHOICES = "List roles available to you."
    C_CHOOSE = "Pick a role."

    F_CHOICE = "Index of the role. Refer to the choices list."

class DebugTexts:
    C_ANNOUNCE = "Make an announcement embed."
    C_SHUTDOWN = "Ends the bot thread."
    C_RELOAD = "Reload a cog."
    C_STATUS = "Get bot cogs' status."

    F_TITLE = "Title for the announcement."
    F_DESCRIPTION = "Description for the announcement."
    F_COG = "Cog that needs to be reloaded."

class HelpTexts:
    C_HELP = "Show the help menu."
    F_PUBLIC = "If you wish to make this message public."

class UserTexts:
    C_CREATE = "Assign yourself a custom role."
    C_REMOVE = "Remove a custom role."
    C_RECOLOR = "Recolor a custom role."
    C_RENAME = "Rename a custom role."
    C_REBADGE = "Rebadge a custom role. Leave empty to remove it."
    C_CREATED = "List created roles."
    C_PREVIEW = "Preview a color."

    F_NAME = "Name for the role."
    F_COLOR = "Color for your role. Hexadecimal format only."
    F_SECONDARY_COLOR = "Secondary color for your role. Hexadecimal format only."
    F_HOLOGRAPHIC = "Make the role style holographic. Ignores color inputs."
    F_PREVIEW = "Color to preview. Hexadecimal format only."
    F_BADGE = "Badge for your role."
    F_INDEX = "Index of the role."
    F_MEMBER = "Member to list the created roles for."

    DELETE_REASON = "Impossible to connect to the SQL database at the moment."
    DF_NO_BADGE_PERMS = "Your guild does not support custom role badges."
    DF_NOT_BADGE_ALLOWED = "You do not have badge permissions with your currently allowed role(s)."
    DF_NO_GRADIENT_PERMS = "Your guild does not support enhanced role styles."
    DF_NOT_GRADIENT_ALLOWED = "You do not have enhanced role styles permissions with your currently allowed role(s)."
    DF_NOT_VALID_COLOR = "Your given secondary color is not a hexadecimal number."
    DF_INVALID_FILE = "The file you have provided is invalid. Make sure it's an image file type supported by discord (.png, .jpg, .webp)."