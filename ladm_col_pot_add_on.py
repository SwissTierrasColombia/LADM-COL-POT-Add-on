"""
/***************************************************************************
                               LADM-COL Add-on
                             --------------------
        begin         : 2021-07-27
        git sha       : :%H$
        copyright     : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email         : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import Qgis
from qgis.utils import plugins

from .model_config import ModelConfig
from .role_config import RoleConfig
from .config import *


class LADMCOLPOTAddOn:

    def __init__(self, iface):
        self.iface = iface
        self.ladmcol = None  # To hold instance of Asistente LADM-COL

    def initGui(self):
        self.__initialize_ladm_col_plugin()

    def __initialize_ladm_col_plugin(self):
        if LADM_COL_PLUGIN_ID not in plugins:
            # Let the user know that Asistente LADM-COL is required
            self.iface.messageBar().pushMessage("LADMColAddOn",
                                                QCoreApplication.translate("LADMColAddOn", WARNING_DEPENDENCY_MISSING),
                                                Qgis.Warning)
            return
    
        self.ladmcol = plugins[LADM_COL_PLUGIN_ID]
        self.ladmcol.plugin_unloaded.connect(self.__unload_ladm_col_plugin)

        # Register POT model
        model = ModelConfig.get_model_instance()
        self.ladmcol.model_registry.register_model(model)

        # Register new role for POT
        role_key, role_config = RoleConfig.get_role_configuration()
        self.ladmcol.role_registry.register_role(role_key, role_config, activate_role=True)

    def __unload_ladm_col_plugin(self):
        # Called when the LADM-COL plugin is uninstalled, informing us
        # we have to reset all member vars that deal with the plugin
        self.ladmcol = None

    def unload(self):
        if self.ladmcol:  # In case LADM-COL has not been uninstalled yet...
            self.ladmcol.role_registry.unregister_role(POT_ROLE_KEY)
            self.ladmcol.model_registry.unregister_model(POT_MODEL_KEY, True)
