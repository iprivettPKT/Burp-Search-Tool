#!/usr/bin/python3

#Created by: Isaac Privett

import wx
import os
import xml.etree.ElementTree as ET
import base64

class XMLSearchApp(wx.Frame):

    def __init__(self, *args, **kw):
        super(XMLSearchApp, self).__init__(*args, **kw)
        
        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        st1 = wx.StaticText(pnl, label='Enter Search Term:')
        vbox.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        self.search_term = wx.TextCtrl(pnl)
        vbox.Add(self.search_term, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        self.browse_btn = wx.Button(pnl, label='Browse')
        self.browse_btn.Bind(wx.EVT_BUTTON, self.OnBrowse)
        vbox.Add(self.browse_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        self.start_search_btn = wx.Button(pnl, label='Start Search')
        self.start_search_btn.Bind(wx.EVT_BUTTON, self.OnSearch)
        vbox.Add(self.start_search_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        pnl.SetSizer(vbox)
        
        self.SetTitle('XML Search Tool')
        self.Centre()

    def OnBrowse(self, event):
        openFileDialog = wx.FileDialog(self, "Open XML file", "", "", "XML files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        self.file_path = openFileDialog.GetPath()
        self.browse_btn.SetLabel(self.file_path.split(os.path.sep)[-1])

    def OnSearch(self, event):
        term = self.search_term.GetValue()

        # Use self.file_path instead of self.path.GetValue()
        path = self.file_path

        if not term or not path:
            wx.MessageBox('Please enter both a search term and a file path', 'Error', wx.OK | wx.ICON_ERROR)
            return

        tree = ET.parse(path)
        root = tree.getroot()
        main_dir = "Burp_Search_Results"
        results_dir = "results_" + term
        dir_path = str(main_dir + "/" + results_dir)
        os.makedirs(main_dir, exist_ok=True)
        os.makedirs(dir_path, exist_ok=True)

        file_counter = 0
        matched_count = 0

        for item in root.findall(".//item"):
            response = item.find('response')
            request = item.find('request')

            if response is not None and response.text is not None:
                decoded_response = base64.b64decode(response.text)

                # Check if the search term is in the decoded response (searching within bytes)
                if term.encode('utf-8') in decoded_response:
                    file_counter += 1
                    file_name = f"{main_dir}/{results_dir}/result_{file_counter}.txt"

                    with open(file_name, 'w', encoding='utf-8', errors='ignore') as f:
                        if request is not None and request.text is not None:
                            decoded_request = base64.b64decode(request.text).decode('utf-8', 'ignore')
                            f.write("----- REQUEST -----\n")
                            f.write(decoded_request + "\n")
                            f.write("\n")

                        f.write("----- RESPONSE -----\n")
                        f.write(decoded_response.decode('utf-8', 'ignore') + "\n")

                    print(f"Saved {main_dir}/{results_dir}/result_{file_counter}.txt")
                    print('-' * 50)  # Delimiter for readability
    
        # After loop, print total matches
        print(f"Total matches: {file_counter}")



if __name__ == '__main__':
    app = wx.App()
    frm = XMLSearchApp(None, title='XML Search Tool', size=(400, 200))
    frm.Show()
    app.MainLoop()


