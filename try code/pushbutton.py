import sys
from PyQt5.QtWidgets import *


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__()
        icons = [
            'SP_TitleBarMinButton',
            'SP_TitleBarMenuButton',
            'SP_TitleBarMaxButton',
            'SP_TitleBarCloseButton',
            'SP_TitleBarNormalButton',
            'SP_TitleBarShadeButton',
            'SP_TitleBarUnshadeButton',
            'SP_TitleBarContextHelpButton',
            'SP_MessageBoxInformation',
            'SP_MessageBoxWarning',
            'SP_MessageBoxCritical',
            'SP_MessageBoxQuestion',
            'SP_DesktopIcon',
            'SP_TrashIcon',
            'SP_ComputerIcon',
            'SP_DriveFDIcon',
            'SP_DriveHDIcon',
            'SP_DriveCDIcon',
            'SP_DriveDVDIcon',
            'SP_DriveNetIcon',
            'SP_DirHomeIcon',
            'SP_DirOpenIcon',
            'SP_DirClosedIcon',
            'SP_DirIcon',
            'SP_DirLinkIcon',
            'SP_FileIcon',
            'SP_FileLinkIcon',
            'SP_FileDialogStart',
            'SP_FileDialogEnd',
            'SP_FileDialogToParent',
            'SP_FileDialogNewFolder',
            'SP_FileDialogDetailedView',
            'SP_FileDialogInfoView',
            'SP_FileDialogContentsView',
            'SP_FileDialogListView',
            'SP_FileDialogBack',
            'SP_DockWidgetCloseButton',
            'SP_ToolBarHorizontalExtensionButton',
            'SP_ToolBarVerticalExtensionButton',
            'SP_DialogOkButton',
            'SP_DialogCancelButton',
            'SP_DialogHelpButton',
            'SP_DialogOpenButton',
            'SP_DialogSaveButton',
            'SP_DialogCloseButton',
            'SP_DialogApplyButton',
            'SP_DialogResetButton',
            'SP_DialogDiscardButton',
            'SP_DialogYesButton',
            'SP_DialogNoButton',
            'SP_ArrowUp',
            'SP_ArrowDown',
            'SP_ArrowLeft',
            'SP_ArrowRight',
            'SP_ArrowBack',
            'SP_ArrowForward',
            'SP_CommandLink',
            'SP_VistaShield',
            'SP_BrowserReload',
            'SP_BrowserStop',
            'SP_MediaPlay',
            'SP_MediaStop',
            'SP_MediaPause',
            'SP_MediaSkipForward',
            'SP_MediaSkipBackward',
            'SP_MediaSeekForward',
            'SP_MediaSeekBackward',
            'SP_MediaVolume',
            'SP_MediaVolumeMuted',
            'SP_CustomBase'
        ]
        Col_size = 6

        layout = QGridLayout()

        count = 0
        for i in icons:
            select_button = QPushButton(i)
            select_button.setIcon(self.style().standardIcon(getattr(QStyle, i)))

            layout.addWidget(select_button, count / Col_size, count % Col_size)
            count += 1

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Widget()
    dialog.show()
    app.exec_()