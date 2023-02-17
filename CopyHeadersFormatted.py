from burp import IBurpExtender
from burp import IContextMenuFactory, IContextMenuInvocation
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
from javax.swing import JMenuItem


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        callbacks.setExtensionName("Copy headers as -H arguments")
        # stdout = PrintWriter(callbacks.getStdout(), True)
        # stderr = PrintWriter(callbacks.getStderr(), True)
        self.helpers = callbacks.getHelpers()
        self.callbacks = callbacks
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self, invocation):
        context = invocation.getInvocationContext()
        convertedHeaders = self.getConvertedHeaders(invocation)
        if (
            context == IContextMenuInvocation.CONTEXT_MESSAGE_EDITOR_REQUEST
            or context == IContextMenuInvocation.CONTEXT_MESSAGE_VIEWER_REQUEST
            and convertedHeaders != None
        ):
            label = "Copy headers as -H arguments"
            menuItem = JMenuItem(label, actionPerformed=self.copyConvertedHeaders)
            menuItem.putClientProperty("convertedHeaders", convertedHeaders)
            return [menuItem]

    def getConvertedHeaders(self, invocation):

        def convertHeaders(headers):
            modified = []
            for i, header in enumerate(headers):
                if i == 0:
                    continue
                if header.lower().startswith("content-length"):
                    continue
                # Feroxbuster won't accept "Accept" headers for some reason
                if header.lower().startswith("accept"):
                    continue                
                header_split = header.split(": ")
                header_name = header_split[0]
                header = "{0}:{1}".format(header_name, ": ".join(header_split[1:]))
                modified.append(header)
            return '-H \"{0}\"'.format('\" -H \"'.join(modified))

        request = invocation.getSelectedMessages()[0].getRequest()
        headers = self.helpers.analyzeRequest(request).getHeaders()
        convertedHeaders = convertHeaders(headers)
        return convertedHeaders

    def copyConvertedHeaders(self, event):
        menuItem = event.getSource()
        convertedHeaders = menuItem.getClientProperty("convertedHeaders")
        systemClipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
        transferText = StringSelection(convertedHeaders)
        systemClipboard.setContents(transferText, None)
