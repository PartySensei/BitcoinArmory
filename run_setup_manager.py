#!/usr/bin/env python

import sys
from qtpy import QtWidgets
from qtdialogs.DlgSetupManager import DlgSetupManager

def main():
    # Create QApplication instance if it doesn't exist
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    
    # Run the dialog
    result = DlgSetupManager.run()
    
    # Exit with the dialog result
    sys.exit(result)

if __name__ == '__main__':
    main() 