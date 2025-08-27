import os
import sys
import unittest
from qtpy import QtWidgets, QtCore
from qtdialogs.DlgSetupManager import DlgSetupManager
from armoryengine.Settings import TheSettings

class TestSetupManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance if it doesn't exist
        app = QtWidgets.QApplication.instance()
        if app is None:
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = app
        
    def setUp(self):
        # Create dialog instance for each test with testing flag
        self.dialog = DlgSetupManager(testing=True)
        # Initialize with testing mode
        self.dialog.loadSettings(testing=True)
        
    def test_initial_state(self):
        """Test initial state of the dialog"""
        # Check window title
        self.assertEqual(self.dialog.windowTitle(), "Armory Setup Manager")
        
        # Check tab count and titles
        self.assertEqual(self.dialog.tabWidget.count(), 3)
        self.assertEqual(self.dialog.tabWidget.tabText(0), "Wallet Settings")
        self.assertEqual(self.dialog.tabWidget.tabText(1), "Pathing")
        self.assertEqual(self.dialog.tabWidget.tabText(2), "DB Settings")
        
    def test_pathing_tab(self):
        """Test pathing tab functionality"""
        # Check initial paths
        self.assertEqual(
            self.dialog.edtCoreDatadir.text(),
            TheSettings.getSettingOrSetDefault('CoreDataDir', '')
        )
        self.assertEqual(
            self.dialog.edtArmoryDatadir.text(),
            TheSettings.getSettingOrSetDefault('ArmoryDataDir', '')
        )
        self.assertEqual(
            self.dialog.edtDbDir.text(),
            TheSettings.getSettingOrSetDefault('DBDir', '')
        )
        
        # Test setting new paths
        test_path = os.path.expanduser("~/test_path")
        self.dialog.edtCoreDatadir.setText(test_path)
        self.assertEqual(self.dialog.edtCoreDatadir.text(), test_path)
        
    def test_db_settings_tab(self):
        """Test database settings tab functionality"""
        # Check initial values
        self.assertEqual(
            self.dialog.cmbDbType.currentText(),
            TheSettings.getSettingOrSetDefault('DBType', 'DB_FULL')
        )
        self.assertEqual(
            self.dialog.spnRamUsage.value(),
            TheSettings.getSettingOrSetDefault('RAMUsage', 50)
        )
        self.assertEqual(
            self.dialog.spnThreadCount.value(),
            TheSettings.getSettingOrSetDefault('ThreadCount', 4)
        )
        
        # Test setting new values
        self.dialog.cmbDbType.setCurrentText('DB_SUPER')
        self.dialog.spnRamUsage.setValue(75)
        self.dialog.spnThreadCount.setValue(8)
        
        self.assertEqual(self.dialog.cmbDbType.currentText(), 'DB_SUPER')
        self.assertEqual(self.dialog.spnRamUsage.value(), 75)
        self.assertEqual(self.dialog.spnThreadCount.value(), 8)
        
    def test_wallet_settings_tab(self):
        """Test wallet settings tab functionality"""
        # Initially, convert button should be disabled
        self.assertFalse(self.dialog.btnConvert.isEnabled())
        
        # Test wallet list is empty initially (no main window provided)
        self.assertEqual(self.dialog.walletList.count(), 0)
        
    def test_settings_validation(self):
        """Test settings validation"""
        # Test with invalid paths - use a path that definitely won't exist
        nonexistent_path = os.path.join(os.path.expanduser("~"), "definitely_nonexistent_armory_test_path_123456789")
        self.dialog.edtCoreDatadir.setText(nonexistent_path)
        self.dialog.edtArmoryDatadir.setText(nonexistent_path)
        self.dialog.edtDbDir.setText(nonexistent_path)
        self.assertFalse(self.dialog.validateSettings(interactive=False))
        
        # Test with valid paths
        test_path = os.path.expanduser("~")
        self.dialog.edtCoreDatadir.setText(test_path)
        self.dialog.edtArmoryDatadir.setText(test_path)
        self.dialog.edtDbDir.setText(test_path)
        self.assertTrue(self.dialog.validateSettings(interactive=False))
        
    def test_settings_persistence(self):
        """Test settings are saved and loaded correctly"""
        # Set test values
        test_path = os.path.expanduser("~/test_armory")
        self.dialog.edtCoreDatadir.setText(test_path)
        self.dialog.edtArmoryDatadir.setText(test_path)
        self.dialog.edtDbDir.setText(test_path)
        self.dialog.cmbDbType.setCurrentText('DB_SUPER')
        self.dialog.spnRamUsage.setValue(75)
        self.dialog.spnThreadCount.setValue(8)
        
        # Save settings
        self.dialog.saveSettings()
        
        # Create new dialog instance
        new_dialog = DlgSetupManager()
        
        # Check if settings were loaded correctly
        self.assertEqual(new_dialog.edtCoreDatadir.text(), test_path)
        self.assertEqual(new_dialog.edtArmoryDatadir.text(), test_path)
        self.assertEqual(new_dialog.edtDbDir.text(), test_path)
        self.assertEqual(new_dialog.cmbDbType.currentText(), 'DB_SUPER')
        self.assertEqual(new_dialog.spnRamUsage.value(), 75)
        self.assertEqual(new_dialog.spnThreadCount.value(), 8)
        
    def tearDown(self):
        # Clean up dialog
        self.dialog.close()
        
    @classmethod
    def tearDownClass(cls):
        # Don't quit the application if we didn't create it
        if QtWidgets.QApplication.instance() == cls.app:
            cls.app.quit()

if __name__ == '__main__':
    unittest.main() 