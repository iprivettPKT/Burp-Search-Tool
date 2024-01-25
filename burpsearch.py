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

        # Adjust the initial size of the window
        self.SetSize((1200, 1000))

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
        self.start_search_btn.Bind(wx.EVT_BUTTON, self.SearchClick)
        vbox.Add(self.start_search_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Add the 'Generated Files' section and its related widgets
        st2 = wx.StaticText(pnl, label='Generated Files:')
        vbox.Add(st2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.file_listbox = wx.ListBox(pnl, style=wx.LB_SINGLE)
        self.file_listbox.Bind(wx.EVT_LISTBOX, self.OnOpen)
        vbox.Add(self.file_listbox, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.refresh_btn = wx.Button(pnl, label='Refresh List')
        self.refresh_btn.Bind(wx.EVT_BUTTON, self.OnRefresh)
        vbox.Add(self.refresh_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.open_btn = wx.Button(pnl, label='Open Selected File')
        self.open_btn.Bind(wx.EVT_BUTTON, self.OnOpen)
        vbox.Add(self.open_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Define the horizontal box sizer for the request and response areas
        hbox_listboxes = wx.BoxSizer(wx.HORIZONTAL)

        # Request display area
        self.request_display = wx.TextCtrl(pnl, style=wx.TE_MULTILINE|wx.TE_READONLY)
        hbox_listboxes.Add(self.request_display, proportion=2, flag=wx.EXPAND|wx.RIGHT, border=5)

        # Response display area
        self.response_display = wx.TextCtrl(pnl, style=wx.TE_MULTILINE|wx.TE_READONLY)
        hbox_listboxes.Add(self.response_display, proportion=2, flag=wx.EXPAND|wx.LEFT, border=5)

        # Add the horizontal box containing the request and response areas to the vertical box sizer
        vbox.Add(hbox_listboxes, proportion=2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        pnl.SetSizer(vbox)

        self.SetTitle('Burp Bulk Search Tool')
        self.Centre()

    def SearchClick(self, event):
        # Execute first function
        self.OnSearch(event)
        
        # Execute second function
        self.OnRefresh(event)

    def OnBrowse(self, event):
        openFileDialog = wx.FileDialog(self, "Open XML file", "", "", "XML files (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        self.file_path = openFileDialog.GetPath()
        self.browse_btn.SetLabel(self.file_path.split(os.path.sep)[-1])

    def OnRefresh(self, event):
        # Clear the current list
        self.file_listbox.Clear()
            
        # Get the search term to identify the results directory
        term = self.search_term.GetValue()
        main_dir = "Burp_Search_Results"
        results_dir = "results_" + term
        dir_path = str(main_dir + "/" + results_dir)

        if os.path.exists(dir_path):

            # Extract the number from the filename for sorting
            def sort_key(filename):
                return int(filename.split("_")[1].split(".")[0])
            
            files = sorted(os.listdir(dir_path), key=sort_key)
            # List files in results directory
            for filename in files:
                if filename.endswith(".txt"):
                    self.file_listbox.Append(filename)

    def OnOpen(self, event):
        self.request_display.Clear()
        self.response_display.Clear()
        # Get selected file from listbox
        selected_file = self.file_listbox.GetString(self.file_listbox.GetSelection())
    
        term = self.search_term.GetValue()
        main_dir = "Burp_Search_Results"
        results_dir = "results_" + term
        dir_path = str(main_dir + "/" + results_dir + "/" + selected_file)
        
        # Read and display the contents
        with open(dir_path, 'r', encoding='utf-8') as f:
            content = f.read()
            request_part = content.split("----- REQUEST -----")[1].split("----- RESPONSE -----")[0].strip()
            response_part = content.split("----- RESPONSE -----")[1].strip()                                  
        self.request_display.AppendText(request_part + "\n\n")
        self.response_display.AppendText(response_part + "\n\n")

        # Scroll back to the top
        self.request_display.SetInsertionPoint(0)
        self.response_display.SetInsertionPoint(0)

        self.highlight_search_term(self.request_display, term)
        self.highlight_search_term(self.response_display, term)

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

    def highlight_search_term(self, textctrl, term):
        start_pos = 0
        term_length = len(term)

        # Define the highlight style (yellow background)
        highlight_style = wx.TextAttr(wx.BLACK, wx.YELLOW)

        # Find and highlight all occurrences of the search term
        content = textctrl.GetValue()
        while start_pos < len(content):
            start_pos = content.find(term, start_pos)
            if start_pos == -1:
                break
            textctrl.SetStyle(start_pos, start_pos + term_length, highlight_style)
            start_pos += term_length

if __name__ == '__main__':
    app = wx.App()
    frm = XMLSearchApp(None, title='XML Search Tool', size=(400, 200))
    frm.Show()
    app.MainLoop()
    app.MainLoop()


