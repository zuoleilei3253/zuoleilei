#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.mixin
    ~~~~~~~~~~~

    :copyright:
    :license:

"""

__author__ = "aiqi@xmind.net <Woody Ai>"

from . import const
from . import Element

from .. import utils


class WorkbookMixinElement(Element):
    """
    """
    def __init__(self, node=None, ownerWorkbook=None):
        super(WorkbookMixinElement, self).__init__(node)
        self._owner_workbook = ownerWorkbook
        self.registOwnerWorkbook()

    def registOwnerWorkbook(self):
        if self._owner_workbook:
            self.setOwnerDocument(self._owner_workbook.getOwnerDocument())

    def getOwnerWorkbook(self):
        return self._owner_workbook

    def setOwnerWorkbook(self, workbook):
        if not self._owner_workbook:
            self._owner_workbook = workbook

    def getModifiedTime(self):
        timestamp = self.getAttribute(const.ATTR_TIMESTAMP)
        if timestamp:
            return utils.readable_time(timestamp)

    def setModifiedTime(self, time):
        self.setAttribute(const.ATTR_TIMESTAMP, long(time))

    def updateModifiedTime(self):
        self.setModifiedTime(utils.get_current_time())

    def getID(self):
        return self.getAttribute(const.ATTR_ID)


class TopicMixinElement(Element):
    def __init__(self, node, ownerTopic):
        super(TopicMixinElement, self).__init__(node)
        self._owner_topic = ownerTopic

    def getOwnerTopic(self):
        return self._owner_topic

    def getOwnerSheet(self):
        if not self._owner_topic:
            return

        return self._owner_topic.getOwnerSheet()

    def getOwnerWorkbook(self):
        if not self._owner_topic:
            return

        return self._owner_topic.getOwnerWorkbook()


def main():
    pass

if __name__ == "__main__":
    main()
