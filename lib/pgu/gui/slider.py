"""All sliders and scroll bar widgets have the same parameters.
   
<pre>Slider(value,min,max,size)</pre> 
<dl>
<dt>value<dd>initial value
<dt>min<dd>minimum value
<dt>max<dd>maximum value
<dt>size<dd>size of bar in pixels
</dl>
"""
import pygame
from pygame.locals import *

from const import *
import widget
import app
import table
import basic

_SLIDER_HORIZONTAL = 0
_SLIDER_VERTICAL = 1

class _slider(widget.Widget):
    def __init__(self,value,orient,min,max,size,step=1,**params):
        params.setdefault('cls','slider')
        widget.Widget.__init__(self,**params)
        self.min,self.max,self.value,self.orient,self.size,self.step = min,max,value,orient,size,step
        
    
    def paint(self,s):
        self.pcls = ""
        
        self.value = self.value
        
        if self.container.myhover is self: self.pcls = "hover"
        if (self.container.myfocus is self and 1 in pygame.mouse.get_pressed()): self.pcls = "down"
        
        r = pygame.rect.Rect(0,0,self.rect.w,self.rect.h)
        if self.orient == _SLIDER_HORIZONTAL:
            r.x = (self.value-self.min) * (self.rect.w-self.size) / (self.max-self.min);
            r.w = self.size;
        else:
            r.y = (self.value-self.min) * (self.rect.h-self.size) / (self.max-self.min);
            r.h = self.size;
            
        self.bar = r
        
        app.App.app.theme.render(s,self.style.bar,r)
    
    def event(self,e):
        adj = 0
        if e.type == ENTER: self.repaint()
        elif e.type == EXIT: self.repaint()
        elif e.type == KEYDOWN:
            if e.key == K_TAB:
                self.next()
        elif e.type == MOUSEBUTTONDOWN:
            if self.bar.collidepoint(e.pos):
                self.grab = e.pos[0],e.pos[1]
                self.grab_value = self.value
            else:
                x,y,adj = e.pos[0],e.pos[1],1
                self.grab = None
            self.repaint()
        elif e.type == MOUSEBUTTONUP:
            #x,y,adj = e.pos[0],e.pos[1],1
            self.repaint()
        elif e.type == MOUSEMOTION:
            if 1 in e.buttons and self.container.myfocus is self:
                if self.grab != None:
                    rel = e.pos[0]-self.grab[0],e.pos[1]-self.grab[1]
                    if self.orient == _SLIDER_HORIZONTAL:
                        d = (self.rect.w - self.size)
                        if d != 0: self.value = self.grab_value + ((self.max-self.min) * rel[0] / d)
                    else:
                        d = (self.rect.h - self.size)
                        if d != 0: self.value = self.grab_value + ((self.max-self.min) * rel[1] / d)
                else:
                    x,y,adj = e.pos[0],e.pos[1],1

        if adj:
            if self.orient == _SLIDER_HORIZONTAL:
                d = self.size/2 - (self.rect.w/(self.max-self.min+1))/2
                self.value = (x-d) * (self.max-self.min) / (self.rect.w-self.size+1) + self.min
            else:
                d = self.size/2 - (self.rect.h/(self.max-self.min+1))/2
                self.value = (y-d) * (self.max-self.min) / (self.rect.h-self.size+1) + self.min
    
    def __setattr__(self,k,v):
        if k == 'value':
            v = int(v)
            v = max(v,self.min)
            v = min(v,self.max)
        _v = self.__dict__.get(k,NOATTR)
        self.__dict__[k]=v
        if k == 'value' and _v != NOATTR and _v != v: 
            self.send(CHANGE)
            self.repaint()
            
        if hasattr(self,'size'):
            self.__dict__['size'] = max(self.size,min(self.style.width,self.style.height))

class VSlider(_slider):
    """A verticle slider.
    
    <pre>VSlider(value,min,max,size)</pre>
    """
    def __init__(self,value,min,max,size,**params):
        params.setdefault('cls','vslider')
        _slider.__init__(self,value,_SLIDER_VERTICAL,min,max,size,**params)

class HSlider(_slider):
    """A horizontal slider.
    
    <pre>HSlider(value,min,max,size)</pre>
    """
    def __init__(self,value,min,max,size,**params):
        params.setdefault('cls','hslider')
        _slider.__init__(self,value,_SLIDER_HORIZONTAL,min,max,size,**params)
	
class xVScrollBar(_slider):
    def __init__(self,value,min,max,size,**params):
        params.setdefault('cls','vscrollbar')
        _slider.__init__(self,value,_SLIDER_VERTICAL,min,max,size,**params)

class xHScrollBar(_slider):
    def __init__(self,value,min,max,size,**params):
        params.setdefault('cls','hscrollbar')
        _slider.__init__(self,value,_SLIDER_HORIZONTAL,min,max,size,**params)
        
class HScrollBar(table.Table):
    """A horizontal scroll bar.
    
    <pre>HScrollBar(value,min,max,size,step=1)</pre>
    """
    def __init__(self,value,min,max,size,step=1,**params):
        params.setdefault('cls','hscrollbar')
        
        table.Table.__init__(self,**params)
        
        
        self.slider = _slider(value,_SLIDER_HORIZONTAL,min,max,size,step=step,cls=self.cls+'.slider')
        
        self.tr()
        
        self.minus = basic.Image(self.style.minus)
        self.minus.connect(MOUSEBUTTONDOWN,self._click,-1)
        self.td(self.minus)
        
        self.td(self.slider)
        self.slider.connect(CHANGE,self.send,CHANGE)
        
        self.minus = basic.Image(self.style.minus)
        self.minus.connect(MOUSEBUTTONDOWN,self._click,-1)
        self.td(self.minus)
        
        self.plus = basic.Image(self.style.plus)
        self.plus.connect(MOUSEBUTTONDOWN,self._click,1)
        self.td(self.plus)
        
    def _click(self,value):
        self.slider.value += self.slider.step*value
        
    def resize(self,width=None,height=None):
        self.slider.style.width = self.style.width - (self.minus.style.width*2+self.plus.style.width)
        return table.Table.resize(self,width,height)
        
    def __setattr__(self,k,v):
        if k in ('min','max','value','size','step'):
            if k == 'size':
                v = v * (self.style.width-(self.minus.style.width*2+self.plus.style.width))/ self.style.width 
            return setattr(self.slider,k,v)
        self.__dict__[k]=v
            
    def __getattr__(self,k):
        if k in ('min','max','value','step'):
            return getattr(self.slider,k)
        return table.Table.__getattr__(self,k) #self.__dict__[k]

class VScrollBar(table.Table):
    """A vertical scroll bar.
    
    <pre>VScrollBar(value,min,max,size,step=1)</pre>
    """
    def __init__(self,value,min,max,size,step=1,**params):
        params.setdefault('cls','vscrollbar')
        
        table.Table.__init__(self,**params)
        
        
        self.slider = _slider(value,_SLIDER_VERTICAL,min,max,size,step=step,cls=self.cls+'.slider')
        
        self.tr()
        self.minus = basic.Image(self.style.minus)
        self.minus.connect(MOUSEBUTTONDOWN,self._click,-1)
        self.td(self.minus)
        
        self.tr()
        self.td(self.slider)
        self.slider.connect(CHANGE,self.send,CHANGE)
        
        self.tr()
        self.minus = basic.Image(self.style.minus)
        self.minus.connect(MOUSEBUTTONDOWN,self._click,-1)
        self.td(self.minus)
        
        self.tr()
        self.plus = basic.Image(self.style.plus)
        self.plus.connect(MOUSEBUTTONDOWN,self._click,1)
        self.td(self.plus)
        
    def _click(self,value):
        self.slider.value += self.slider.step*value
        
    def resize(self,width=None,height=None):
        self.slider.style.height = self.style.height -  (self.minus.style.height*2+self.plus.style.height)
        return table.Table.resize(self,width,height)
        
    def __setattr__(self,k,v):
        if k in ('min','max','value','size','step'):
            if k == 'size':
                v = v * (self.style.height -  (self.minus.style.height*2+self.plus.style.height))/self.style.height
            return setattr(self.slider,k,v)
        self.__dict__[k]=v
            
    def __getattr__(self,k):
        if k in ('min','max','value','step'):
            return getattr(self.slider,k)
        return table.Table.__getattr__(self,k)
