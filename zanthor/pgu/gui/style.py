"""
"""
class Style:
    """The class used by widget for the widget.style
    
    <p>This object is used mainly as a dictionary, accessed via <tt>widget.style.attr</tt>, as opposed to
    <tt>widget.style['attr']</tt>.  It automatically grabs information from the theme via <tt>value = theme.get(widget.cls,widget.pcls,attr)</tt>.</p>
    
    """
    def __init__(self,o,dict):
        self.obj = o
        self._cache = 0
        for k,v in dict.items(): self.__dict__[k]=v
    
    def __getattr__(self,k):
        import app
        v = app.App.app.theme.get(self.obj.cls, self.obj.pcls, k)
        if self._cache: self.__dict__[k] = v
        return v
    
    def cache(self,v):
        """Enable the cache.
        
        <p>This should be used when changes of the pcls are unlikely to impact the data, or when there is a lot of repetitive access to the same attributes expected.</p>
        
        <pre>Style.cache(v)</pre>
        
        <dl>
        <dt>v<dd>True if the cache should be enabled.
        </dl>
        """
        if v: self._cache += 1
        else: self._cache -= 1
    
    def __setattr__(self,k,v):
        self.__dict__[k] = v
