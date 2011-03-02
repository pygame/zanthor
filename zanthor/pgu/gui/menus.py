"""
"""
from const import *
import table
import basic, button

class _Menu_Options(table.Table):
    def __init__(self,menu,**params):
        table.Table.__init__(self,**params)
        
        self.menu = menu
    
    def event(self,e):
        handled = False
        if e.type == MOUSEMOTION:
            abspos = e.pos[0]+self.rect.x,e.pos[1]+self.rect.y
            for w in self.menu.container.widgets:
                if not w is self.menu:
                    if w.rect.collidepoint(abspos):
                        self.menu._close(None)
                        w._open(None)
                        handled = True
        elif e.type == MOUSEBUTTONUP:
            abspos = e.pos[0]+self.rect.x,e.pos[1]+self.rect.y
            if not self.rect.collidepoint(abspos) and not self.menu.container.rect.collidepoint(abspos):
                self.close()
                handled = True
        
        if not handled: table.Table.event(self,e)

class _Menu(button.Button):
    def __init__(self,widget=None,**params): #TODO widget= could conflict with module widget
        params.setdefault('cls','menu')
        button.Button.__init__(self,widget,**params)
        
        self._cls = self.cls
        self.options = _Menu_Options(self, cls=self.cls+".options")
        
        #self.options.connect(BLUR,self._close,None)
        self.connect(CLICK,self._open,None)
        
        self.pos = 0
    
    def _open(self,value):
        self.cls = self._cls + "-open"
        self.repaint()
        self.container.open(self.options,self.rect.x,self.rect.bottom)
        #action_open({'container':self.container,'window':self.options,'x':self.rect.x,'y':self.rect.bottom})
        self.options.blur(self.options.myfocus)
        self.options.focus()
        self.repaint()
        
    def _close(self,value):
        self.cls = self._cls
        self.repaint()
        self.options.close()
    
    def _value(self,value):
        #self.options.close()
        self._close(None)
        if value['fnc'] != None:
            value['fnc'](value['value'])
    
#    def resize(self,width=None,height=None):
#        w,h = button.Button.resize(self,width,height)
#        
#        return w,h
#        #self.options._resize()
    
    def add(self,w,fnc=None,value=None):
        #w.resize()
        
        w.style.align = -1
        b = button.Button(w,cls=self.cls+".option")
        #b.style.hexpand = 1
        b.connect(CLICK,self._value,{'fnc':fnc,'value':value})
        
        #self.options.add(b,0,self.pos,1,1,-1,0)
        self.options.tr()
        self.options.add(b)
        #self.pos += 1
        
        return b

class Menus(table.Table):
    """A drop down menu bar.
    
    <pre>Menus(data)</pre>
    
    <dl>
    <dt>data<dd>Menu data, a list of (path,fnc,value), see example below
    </dl>
    
    <strong>Example</strong>
    <code>
    data = [
        ('File/Save',fnc_save,None),
        ('File/New',fnc_new,None),
        ('Edit/Copy',fnc_copy,None),
        ('Edit/Cut',fnc_cut,None),
        ('Help/About',fnc_help,help_about_content),
        ('Help/Reference',fnc_help,help_reference_content),
        ]
    w = Menus(data)
    """
    
    def __init__(self,data,menu_cls='menu',**params):
        params.setdefault('cls','menus')
        table.Table.__init__(self,**params)
        
        n,m,mt = 0,None,None
        for path,cmd,value in data:
            parts = path.split("/")
            if parts[0] != mt:
                mt = parts[0]
                m = _Menu(basic.Label(mt,cls=menu_cls+".label"),cls=menu_cls)
                self.add(m,n,0)
                n += 1
            m.add(basic.Label(parts[1],cls=m.cls+".option.label"),cmd,value)
            #m.resize()