'''
Created on Dec 27, 2011

@author: ajju
'''
from TurtleContainer import Container
import xbmc #@UnresolvedImport
import time
from common import ExceptionHandler, AddonUtils, XBMCInterfaceUtils
from common.Singleton import SingletonClass
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCRequestHandler
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from threading import Thread


__registered_services__ = {}
__context_root__ = ''
__port__ = 8181
__port_range__ = [8100, 8199]
__service_name__ = ''
__addon_id__ = None

def serviceMethod(name, **params):
    actionId = __registered_services__[name]
    data = {'data':AddonUtils.encodeData(params)}
    service_response_obj = None
    try:
        containerObj = Container(addon_id=__addon_id__)
        
        iconimage = AddonUtils.getCompleteFilePath(baseDirPath=containerObj.getAddonContext().addonPath, filename='icon.png')
        XBMCInterfaceUtils.displayNotification(__service_name__ + ' Service', 'Processing received request...', iconimage=iconimage)
    
        containerObj.reloadTurtleRequest(data)
        containerObj.performAction(actionId)
        service_response_obj = containerObj.getTurtleResponse().get_service_response_obj()
    except Exception, e:
        print __service_name__ + ' Service :: ERROR OCCURRED: ' + str(e)
        ExceptionHandler.handle(e)
        service_response_obj = {"status":"exception", "message":"an unexpected error occurred, please check your input"}
        XBMCInterfaceUtils.displayNotification(__service_name__ + ' Service', 'Error while processing your request', time='5000')
    return service_response_obj


def start(addon_id, service_name, context_root, default_port, allowed_port_range):
    try:
        global __addon_id__
        global __registered_services__
        global __context_root__
        global __port__
        global __port_range__
        global __service_name__
        __addon_id__ = addon_id
        __context_root__ = context_root
        __port__ = default_port
        __port_range__ = allowed_port_range
        __service_name__ = service_name
        containerObj = Container(addon_id=addon_id)
        iconimage = AddonUtils.getCompleteFilePath(baseDirPath=containerObj.getAddonContext().addonPath, filename='icon.png')
        serviceport = int(containerObj.getAddonContext().addon.getSetting('serviceport'))
        
        XBMCInterfaceUtils.setSuppressDialogMsg(True)
        
        if serviceport < __port_range__[0] or serviceport > __port_range__[1] :
            containerObj.getAddonContext().addon.setSetting('serviceport', str(__port__))
            serviceport = __port__
            XBMCInterfaceUtils.displayNotification(__service_name__ + ' Service: Port updated', 'Service port set to default value 8181', iconimage=iconimage)

        server = JSONRPCServer(context_root=__context_root__, server_port=serviceport)
        server.registerService('serviceName', serviceMethod)
        defined_services = containerObj.getAddonContext().getTurtleServices()
        if len(defined_services) == 0:
            print __service_name__ + ' Service :: There are no services defined for registration, end this service program now.'
            return
        for service in defined_services:
            server.registerService(service.get_service_name(), serviceMethod)
            __registered_services__[service.get_service_name()] = service.get_action_id()
            print __service_name__ + ' Service :: service registered = %s @ %s' % (service.get_service_name(), __context_root__)
        server.start()
        XBMCInterfaceUtils.displayNotification(__service_name__ + ' Service has started', 'Use safari extension to play video remotely', iconimage=iconimage)
        
        while not xbmc.abortRequested:
            time.sleep(5)
        print __service_name__ + ' Service :: ABORT request received from XBMC. PlayIt service will stop now.'
    except Exception, e:
        print __service_name__ + ' Service :: ERROR OCCURRED: ' + str(e)
        ExceptionHandler.handle(e)
    
    
def log_request(self, *args, **kwargs):
    """ Making the server output 'quiet' """
    pass
    
class JSONRPCServer(SingletonClass):
    
    def __initialize__(self, context_root='/', server_port=8181):
        
        SimpleJSONRPCRequestHandler.log_request = log_request
        SimpleJSONRPCRequestHandler.rpc_paths = (context_root)
        self.server = SimpleJSONRPCServer(('', server_port))
        
    def registerService(self, serviceName, function):
        self.server.register_function(function, name=serviceName)
        
    def start(self):
        self.server_proc = Thread(target=self.server.serve_forever)
        self.server_proc.daemon = True
        self.server_proc.start()
    
    def stop(self):
        pass
