import os
import tkinter as tk
import pygetwindow as pw

class App(tk.Tk):
    
    def __init__(self, tlauncher: str) -> None:
        '''
        Represents a window that attaches to TL
        and toggle its size.
        '''
        
        self.TLAUNCHER = tlauncher
        
        self.default_size = None
        
        super().__init__()
        
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.config(bg = '#fff')
        
        self.enlarge = True
        
        # Switch
        self.toggler = tk.Button(self, command = self.switch, bg = '#71a94c', relief = 'flat')
        self.toggler.pack(expand = True, fill = 'both')
        self.switch()
        
    def switch(self, *_) -> None:
        '''
        Toggle the window size.
        '''
        
        self.enlarge = not self.enlarge
        
        TL = pw.getWindowsWithTitle(self.TLAUNCHER)
        
        if not len(TL): return
        TL = TL[0]
        
        if self.default_size is None:
            self.default_size = TL.size
            self.toggler.config(text = '\\/')
        
        if self.enlarge:
            TL.size = self.default_size
            self.toggler.config(text = '/\\')
        
        else:
            TL.size = (self.default_size[0], 105)
    
    def mainloop(self) -> None:
        '''
        Constantly draw the window over TL.
        '''
        
        while 1:
            
            
            if pw.getActiveWindowTitle() == self.TLAUNCHER:
                self.deiconify()
            else:
                self.withdraw()
            
            # Get TL position
            TL = pw.getWindowsWithTitle(self.TLAUNCHER)
            
            if not len(TL): return # Exit
            TL = TL[0]
            
            x, y = TL.bottomright
            w, h = TL.size
            
            self.geometry(f'55x55+{x - 245}+{y - 30 - 40}')
            self.update()

if __name__ == '__main__':
    
    # Get TL version and TL executable
    path = os.getenv('APPDATA')
    
    try:
        with open(path + '/.tlauncher/tlauncher-2.0.properties', 'r') as file:
            version = file.readlines()[1].split()[-1]
    
    except FileNotFoundError:
        print('[*] ERR: TLauncher not found, exiting.')
        exit()
    
    print('[*] Found TLauncher version', version)
    
    # Start TL
    if not (title := f'TLauncher {version}') in pw.getAllTitles():
        print('[*] Starting TL...')
        os.system(path + '/.minecraft/TLauncher.exe')
    
    # Wait for TL to open
    while 1:
        if title in pw.getAllTitles(): break
    
    # Start tk app
    print('[*] TL launched, injecting app')
    App(title).mainloop()
    
    print('[*] TL window closed.')

# EOF