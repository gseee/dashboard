from PySide2 import QtWidgets, QtCore, QtGui


class LoadingIcon(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(LoadingIcon, self).__init__(*args, **kwargs)
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._current_index = 0
        self._stopped = True
        self._speed_factor = 1.5
        self._speed = 1.0
        self._pixmaps = []
        self._lbl = QtWidgets.QLabel(self)
        self._lbl_text = QtWidgets.QLabel(self)
        self._all_widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(self._all_widget)
        layout.addWidget(self._lbl)
        layout.addWidget(self._lbl_text)
        self._lbl.setVisible(False)
        self._lbl_text.setVisible(False)

        org_pixmap = QtGui.QPixmap(r'Z:\Python\Dashboard\img\received_334195057820151.webp')
        width = org_pixmap.rect().width() // 8
        height = org_pixmap.rect().height() // 4
        rb_corner = org_pixmap.rect().bottomRight()

        start_rect = QtCore.QRect(rb_corner.x() - width + 1,
                           rb_corner.y() - height + 1,
                           width, height)

        for k in range(31):
            row = k // 8
            column = k % 8

            new_rect = start_rect.translated(-column * width, -row * height)
            pix = org_pixmap.copy(new_rect)

            self._pixmaps.append(pix)

        self._pixmaps.reverse()

        # Sets th layout
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self._lbl)
        main_layout.addWidget(self._lbl_text)
        main_layout.addStretch()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setMinimumWidth(width)
        self.setMinimumHeight(height)

        self.__set_interval()
        self._timer.timeout.connect(self.__next_image)

        self.start()


    def start(self):
        """Show the loading element and start the animation."""
        self._stopped = False
        self._timer.start()
        self._lbl.setVisible(True)
        self._lbl_text.setVisible(True)

    def stop(self):
        """Hide the loading icons and stops the animation in the background."""
        self._stopped = True
        self._lbl.setVisible(False)
        self._lbl_text.setVisible(False)

    def set_speed(self, value):
        """Modify the speed at which the animation runs.
        Default is 1.0.

        Args:
            value (float)
        """
        self._speed = value
        self.__set_interval()

    def set_text(self, text):
        """Sets the text attached with the animated icon.

        Args:
            text (str)
        """
        self._lbl_text.setText(text)

    def __set_interval(self):
        """Internal function that sets the animation timer interval"""
        speed = self._speed * self._speed_factor
        self._timer.setInterval(float(1000) / (speed * 31))

    def __next_image(self):
        """Increment the current image"""
        self._timer.stop()
        self._current_index += 1
        self._current_index = self._current_index % len(self._pixmaps)
        self._lbl.setPixmap(self._pixmaps[self._current_index])

        if not self._stopped:
            self._timer.start()
        else:
            self._lbl.setPixmap(None)