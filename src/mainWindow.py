"""
This file contains all the functionality and features for the sloth browser

Copyright (c) 2023 Ezpie <ezpie.co@gmail.com>

This file must at all conditions not be edited without permission.
Unless you're part of the maintainer team

All necessary libraries
"""

from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QIcon, QKeySequence, QStandardItem, QStandardItemModel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QDialog,
                             QDialogButtonBox, QDockWidget, QFrame, QLineEdit,
                             QListView, QListWidget, QMainWindow, QMessageBox,
                             QShortcut, QTabWidget, QToolBar, QToolButton,
                             QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
  """ This is the main window for the browser."""

  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    # Set up the main tab widget
    self.tabs = QTabWidget()
    self.tabs.setDocumentMode(True)
    self.tabs.tabBarDoubleClicked.connect(self.HandleAddTab)
    self.tabs.currentChanged.connect(self.CurrentTabChanged)
    self.tabs.setTabsClosable(True)
    self.tabs.tabCloseRequested.connect(self.CloseCurrentTab)
    self.setCentralWidget(self.tabs)

    self.SetupToolBar()

    # Show the main window
    self.show()
    self.setWindowTitle("Sloth")
    self.showMaximized()

    # Initialize the bookmarks and history lists
    self.bookmarks = []
    self.history = []
    self.SetupHistoryFeature()

    # Add the initial tab with Google as the homepage
    self.AddNewTab(QUrl('http://www.google.com'), 'Homepage')

    # Setup sidebar
    self.SideBar()

  def SetupToolBar(self):
    """This method is used to setup the toolbar"""

    # Set up the toolbar
    self.toolBar = QToolBar("Navigation")
    self.addToolBar(self.toolBar)

    # Back button
    back_btn = QAction(QIcon("assets/back.svg"), "Back", self)
    back_btn.setStatusTip("Back to previous page")
    back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
    self.toolBar.addAction(back_btn)

    # Forward button
    next_btn = QAction(QIcon("assets/forward.svg"), "Forward", self)
    next_btn.setStatusTip("Forward to next page")
    next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
    self.toolBar.addAction(next_btn)

    # Reload button
    reload_btn = QAction(QIcon("assets/reload.svg"), "Reload", self)
    reload_btn.setStatusTip("Reload page")
    reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
    self.toolBar.addAction(reload_btn)

    # URL input field
    self.urlbar = QLineEdit()
    self.urlbar.returnPressed.connect(self.NavigateToUrl)
    self.toolBar.addWidget(self.urlbar)

    # Bookmark button
    bookmark_btn = QToolButton()
    bookmark_btn.setIcon(QIcon("assets/bookmark.svg"))
    bookmark_btn.clicked.connect(self.AddCurrentPageToBookmarks)
    self.toolBar.addWidget(bookmark_btn)

  def SetupHistoryFeature(self):
    """This method create's the history widget"""

    # Set up the history functionality
    history_shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
    history_shortcut.activated.connect(self.ShowHistory)

    self.history_widget = QListView()
    self.history_model = QStandardItemModel()
    self.history_widget.setModel(self.history_model)
    self.history_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    self.history_widget.doubleClicked.connect(self.LoadHistoryItem)
    self.history_widget.hide()

    self.history_dock = QDockWidget("History", self)
    self.history_dock.setObjectName("history_dock")
    self.history_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
    self.history_dock.setWidget(self.history_widget)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.history_dock)
    self.history_dock.hide()

  def SideBar(self):
    """This method create's the sidebar widget"""

    self.sideBar = QWidget()
    self.sideBar.setFixedWidth(80)
    self.sideBarLayout = QVBoxLayout()
    self.sideBarLayout.setAlignment(Qt.AlignTop)
    self.sideBar.setLayout(self.sideBarLayout)
    self.sideBar.setObjectName("SideBar")

    # Setup all buttons
    self.SideBarButtons()

    # Setup sidebar widget
    self.sideBarDock = QDockWidget("SideBar", self)
    self.sideBarDock.setObjectName("sideBarDock")
    self.sideBarDock.setAllowedAreas(Qt.RightDockWidgetArea)
    self.sideBarDock.setWidget(self.sideBar)

    self.sideBarDock.setFeatures(self.sideBarDock.features() & ~QDockWidget.
                                 DockWidgetClosable)

    self.addDockWidget(Qt.RightDockWidgetArea, self.sideBarDock)
    self.sideBarDock.show()

  def SideBarButtons(self):
    """ This is a helper method for the SideBar method This method adds all the
    buttons for the SideBar method"""

    # Open bookmarks button
    openBookmarks = QToolButton()
    openBookmarks.setIcon(QIcon("assets/sidebarIcons/bookmarks.svg"))
    openBookmarks.clicked.connect(self.OpenBookmarks)
    openBookmarks.setIconSize(QSize(50, 50))
    self.sideBarLayout.addWidget(openBookmarks)

    # Open History button
    openHistory = QToolButton()
    openHistory.setIcon(QIcon("assets/sidebarIcons/history.svg"))
    openHistory.clicked.connect(self.ShowHistory)
    openHistory.setIconSize(QSize(50, 50))
    self.sideBarLayout.addWidget(openHistory)

    # Separator
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    separator.setFrameShadow(QFrame.Sunken)
    self.sideBarLayout.addWidget(separator)

    # Shortcut button for Twitter
    twitterBtn = QToolButton()
    twitterBtn.setIcon(QIcon("assets/sidebarIcons/twitter.svg"))
    twitterBtn.clicked.connect(lambda: self.OpenShortCut("twitter.com"))
    twitterBtn.setIconSize(QSize(50, 50))
    self.sideBarLayout.addWidget(twitterBtn)

    # Shortcut button for Gmail
    gmailBtn = QToolButton()
    gmailBtn.setIcon(QIcon("assets/sidebarIcons/gmail.svg"))
    gmailBtn.clicked.connect(lambda: self.OpenShortCut("gmail.com"))
    gmailBtn.setIconSize(QSize(50, 50))
    self.sideBarLayout.addWidget(gmailBtn)

    # Shortcut button for YouTube
    youtubeBtn = QToolButton()
    youtubeBtn.setIcon(QIcon("assets/sidebarIcons/youtube.svg"))
    youtubeBtn.clicked.connect(lambda: self.OpenShortCut("youtube.com"))
    youtubeBtn.setIconSize(QSize(50, 50))
    self.sideBarLayout.addWidget(youtubeBtn)


  def OpenShortCut(self, site):
    """ This is a helper method to open a shortcut option"""

    self.AddNewTab(QUrl("https://" + site))

  def AddNewTab(self, qurl=None, label="Blank"):
    """ This method is used for adding new tabs and updating the widgets"""

    if qurl is None:
      qurl = QUrl('https://google.com')

    # Create a new web view widget for the tab
    browser = QWebEngineView()
    browser.setUrl(qurl)

    # Add the tab to the tab widget
    i = self.tabs.addTab(browser, label)
    self.tabs.setCurrentIndex(i)

    # Connect signals to update the URL bar and handle page load
    browser.urlChanged.connect(lambda qurl, browser=browser:self.UpdateUrlbar
                               (qurl, browser))
    browser.loadFinished.connect(lambda _, i=i,
                                 browser=browser: self.OnPageLoadFinished
                                 (i, browser, label))

  def OnPageLoadFinished(self, index, browser):
    """ This method is used to update the history attribute"""
    # Update the tab title and add the page to the history
    self.tabs.setTabText(index, browser.page().title())
    self.history.append({'title': browser.page().title(),
                         'url': browser.url().toString()})

  def HandleAddTab(self, i):
    if i == -1:  # open clicked
      self.AddNewTab()

  def CurrentTabChanged(self):
    """ This method updates the widgets as per the tab change"""

    # Update the URL bar and window title when the current tab changes
    qurl = self.tabs.currentWidget().url()
    self.UpdateUrlbar(qurl, self.tabs.currentWidget())
    self.UpdateTitle(self.tabs.currentWidget())

  def CloseCurrentTab(self, i):
    # Close the current tab, but ensure at least one tab remains open
    if self.tabs.count() < 2:
      return

    self.tabs.removeTab(i)

  def UpdateUrlbar(self, q, browser=None):
    # Update the URL bar text
    if browser != self.tabs.currentWidget():
      return

    self.urlbar.setText(q.toString())
    self.urlbar.setCursorPosition(0)

  def NavigateToUrl(self):
    # Navigate to the URL entered in the URL bar
    q = QUrl(self.urlbar.text())
    if q.scheme() == "":
      q.setScheme("https")

    self.tabs.currentWidget().setUrl(q)

  def UpdateTitle(self, browser):
    # Update the window title with the current tab's title
    if browser != self.tabs.currentWidget():
      return

    title = self.tabs.currentWidget().page().title()
    self.setWindowTitle(title)

  def AddCurrentPageToBookmarks(self):
    """ This method is used to add the current page to the bookmark attribute
    and inform the user about it"""

    # Add the current page to bookmarks
    title = self.tabs.currentWidget().page().title()
    url = self.tabs.currentWidget().url().toString()

    # information Object for displaying message to user
    msg = QMessageBox()

      # Check weather the current page is already bookmarked
    for bookmark in self.bookmarks:
      if bookmark['url'] == url:
        # Inform user about it
        msg.setWindowTitle("Bookmark Exists!")
        msg.setText(
          "Bookmark already exists try adding another page instead."
        )

        # Break the function
        return

    bookmark = {'title': title, 'url': url}
    self.bookmarks.append(bookmark)

    # Show a message to indicate the bookmark has been added
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Bookmark Added")
    msg.setText("Bookmark has been added.")
    msg.exec_()

  def OpenBookmarks(self):
    """ This method helps to open the bookmark dialog widget"""

    # Open the bookmarks dialog to select a bookmark to open
    dialog = QDialog(self)
    dialog.setWindowTitle('Bookmarks')
    dialog.setMinimumWidth(400)

    layout = QVBoxLayout(dialog)
    bookmark_list = QListWidget()

    for bookmark in self.bookmarks:
      bookmark_list.addItem(bookmark['title'])

    layout.addWidget(bookmark_list)

    button_box = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel
    )
    layout.addWidget(button_box)

    button_box.accepted.connect(
      lambda: self.OpenSelectedBookmark(bookmark_list)
    )

    dialog.exec_()

  def OpenSelectedBookmark(self, bookmark_list):
    """ This method helps to open the selected bookmark"""

    # Open the selected bookmark in a new tab
    selected_item = bookmark_list.currentItem()
    if selected_item is None:
      return

    bookmark_title = selected_item.text()
    bookmark_url = None
    for bookmark in self.bookmarks:
      if bookmark['title'] == bookmark_title:
        bookmark_url = bookmark['url']
        break

    if bookmark_url is not None:
      self.AddNewTab(QUrl(bookmark_url), bookmark_title)

  def ShowHistory(self):
    """ This method helps to show and hide the history widget"""

    # Show or hide the history dock widget
    if self.history_dock.isHidden():
      self.history_dock.show()
      self.history_widget.show()
      self.PopulateHistoryModel()
    else:
      self.history_dock.hide()
      self.history_widget.hide()

  def PopulateHistoryModel(self):
    """ This method helps in adding all the user's search history into the
    history widget"""

    # Populate the history model with items from the history list
    self.history_model.clear()
    for item in self.history:
      history_item = QStandardItem(item['title'])
      history_item.setData(item['url'], Qt.UserRole)
      self.history_model.appendRow(history_item)

  def LoadHistoryItem(self, index):
    """ This method is used to add a new tab with the history item selected."""

    # Load the selected history item in a new tab
    item = self.history_model.itemData(index, Qt.UserRole)
    if item:
      url = item[0]
      self.AddNewTab(QUrl(url), self.history_model.item(index).text())
      self.ShowHistory()
