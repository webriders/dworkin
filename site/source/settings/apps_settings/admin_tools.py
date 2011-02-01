from .. import main_settings

ADMIN_TOOLS_MEDIA_URL = main_settings.STATIC_URL + 'ext/'
ADMIN_TOOLS_THEMING_CSS = '../admin_skin/css/theming.css'
ADMIN_TOOLS_MENU = 'conf.admin_tools.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'conf.admin_tools.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'conf.admin_tools.dashboard.CustomAppIndexDashboard'

del main_settings