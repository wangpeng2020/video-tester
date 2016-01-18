# coding=UTF8
## This file is part of VideoTester
## See https://github.com/Enchufa2/video-tester for more information
## Copyright 2011-2016 Iñaki Úcar <i.ucar86@gmail.com>
## This program is published under a GPLv3 license
# generated by wxGlade HG

import wx, wx.aui, pickle, logging
import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from gi.repository import Gst, GObject
from . import VTLOG, VTClient, netifaces, supported_codecs, supported_protocols
from .resources import getVTIcon, getVTBitmap

class FuncLog(logging.Handler):
    """
    A logging handler that sends logs to an update function.
    """
    def __init__(self, textctrl):
        logging.Handler.__init__(self)
        self.textctrl = textctrl

    def emit(self, record):
        self.textctrl.SetInsertionPointEnd()
        self.textctrl.WriteText(self.format(record) + '\n')

class VTframe(wx.Frame):
    """
    Main window.
    """
    def __init__(self, conf):
        self.main = VTClient(conf)
        # begin wxGlade: VTframe.__init__
        wx.Frame.__init__(self, None)
        self.SetIcon(getVTIcon())

        # Menu Bar
        self.vtmenubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.m_files = wxglade_tmp_menu.Append(wx.ID_OPEN, "&Open files...", "Select Pickle files to plot")
        wxglade_tmp_menu.AppendSeparator()
        self.m_exit = wxglade_tmp_menu.Append(wx.ID_EXIT, "E&xit", "Exit program")
        self.vtmenubar.Append(wxglade_tmp_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        self.m_run = wxglade_tmp_menu.Append(wx.NewId(), "&Run...", "Run test")
        self.vtmenubar.Append(wxglade_tmp_menu, "R&un")
        wxglade_tmp_menu = wx.Menu()
        self.m_about = wxglade_tmp_menu.Append(wx.ID_ABOUT, "&About", "About this program")
        self.vtmenubar.Append(wxglade_tmp_menu, "&Help")
        self.SetMenuBar(self.vtmenubar)
        # Menu Bar end
        self.vtstatusbar = self.CreateStatusBar(1, 0)
        self.tabs = wx.Notebook(self, -1, style=0)
        self.options_tab = wx.Panel(self.tabs, -1)

        self.video_label = wx.StaticText(self.options_tab, -1, "Choose a video:")
        self.video = wx.Choice(self.options_tab, -1, choices=[x[0] for x in self.main.videos])
        self.codec_label = wx.StaticText(self.options_tab, -1, "Choose a codec:")
        self.codec = wx.Choice(self.options_tab, -1, choices=supported_codecs.keys())
        self.bitrate_label = wx.StaticText(self.options_tab, -1, "Select the bitrate:")
        self.bitrate = wx.Slider(self.options_tab, -1, self.main.conf['bitrate'], 64, 1024, style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.framerate_label = wx.StaticText(self.options_tab, -1, "Select the framerate:")
        self.framerate = wx.Slider(self.options_tab, -1, self.main.conf['framerate'], 1, 100, style=wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.sizer_2_staticbox = wx.StaticBox(self.options_tab, -1, "Video options:")

        self.iface_label = wx.StaticText(self.options_tab, -1, "Interface:")
        self.iface = wx.Choice(self.options_tab, -1, choices=netifaces)
        self.ip_label = wx.StaticText(self.options_tab, -1, "Server IP:")
        self.ip = wx.TextCtrl(self.options_tab, -1, self.main.conf['ip'])
        self.port_label = wx.StaticText(self.options_tab, -1, "Server port:")
        self.port = wx.TextCtrl(self.options_tab, -1, str(self.main.port))
        self.protocol = wx.RadioBox(self.options_tab, -1, "Protocol:", choices=supported_protocols, majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.sizer_3_staticbox = wx.StaticBox(self.options_tab, -1, "Net options:")

        self.qos = []
        self.qos.append(('latency', wx.CheckBox(self.options_tab, -1, "Latency")))
        self.qos.append(('delta', wx.CheckBox(self.options_tab, -1, "Delta")))
        self.qos.append(('jitter', wx.CheckBox(self.options_tab, -1, "Jitter")))
        self.qos.append(('skew', wx.CheckBox(self.options_tab, -1, "Skew")))
        self.qos.append(('bandwidth', wx.CheckBox(self.options_tab, -1, "Bandwidth")))
        self.qos.append(('plr', wx.CheckBox(self.options_tab, -1, "Packet Loss Rate")))
        self.qos.append(('pld', wx.CheckBox(self.options_tab, -1, "Packet Loss Distribution")))
        self.sizer_15_staticbox = wx.StaticBox(self.options_tab, -1, "QoS measures:")

        self.bs = []
        self.bs.append(('streameye', wx.CheckBox(self.options_tab, -1, "Stream Eye")))
        self.bs.append(('refstreameye', wx.CheckBox(self.options_tab, -1, "refStream Eye")))
        self.bs.append(('gop', wx.CheckBox(self.options_tab, -1, "GOP size")))
        self.bs.append(('iflr', wx.CheckBox(self.options_tab, -1, "I Frame Loss Rate")))
        self.sizer_16_staticbox = wx.StaticBox(self.options_tab, -1, "BitStream measures:")

        self.vq = []
        self.vq.append(('psnr', wx.CheckBox(self.options_tab, -1, "PSNR")))
        self.vq.append(('ssim', wx.CheckBox(self.options_tab, -1, "SSIM")))
        self.vq.append(('g1070', wx.CheckBox(self.options_tab, -1, "G.1070")))
        self.vq.append(('psnrtomos', wx.CheckBox(self.options_tab, -1, "PSNRtoMOS")))
        self.vq.append(('miv', wx.CheckBox(self.options_tab, -1, "MIV")))
        self.sizer_5_staticbox = wx.StaticBox(self.options_tab, -1, "Video quality measures:")

        self.log_tab = wx.Panel(self.tabs, -1)
        self.log = wx.TextCtrl(self.log_tab, -1, '', style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.results_tab = PlotNotebook(self.tabs)
        self.video_tab = wx.Panel(self.tabs, -1)
        self.label_2 = wx.StaticText(self.video_tab, -1, "Play videos:")
        self.play_video = wx.Button(self.video_tab, -1, "Play", name="playvideo")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.onOpen, self.m_files)
        self.Bind(wx.EVT_MENU, self.onExit, self.m_exit)
        self.Bind(wx.EVT_MENU, self.onRun, self.m_run)
        self.Bind(wx.EVT_MENU, self.onAbout, self.m_about)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.play_video.Bind(wx.EVT_BUTTON, self.onPlay)

        # Logging
        self.old_hdlr = VTLOG.handlers[0]
        self.hdlr = FuncLog(self.log)
        self.hdlr.setLevel(self.old_hdlr.level)
        self.hdlr.setFormatter(self.old_hdlr.formatter)
        VTLOG.handlers[0] = self.hdlr
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: VTframe.__set_properties
        self.SetTitle("Video Tester")
        self.SetSize((800, 600))
        self.Hide()
        self.vtstatusbar.SetStatusWidths([-1])
        # statusbar fields
        vtstatusbar_fields = ["VT Client"]
        for i in range(len(vtstatusbar_fields)):
            self.vtstatusbar.SetStatusText(vtstatusbar_fields[i], i)

        self.video_label.SetMinSize((160, 17))
        self.video.SetMinSize((120, 25))
        self.video.SetSelection(zip(*self.main.videos)[0].index(self.main.conf['video']))

        self.codec_label.SetMinSize((160, 17))
        self.codec.SetMinSize((120, 25))
        self.codec.SetSelection(supported_codecs.keys().index(self.main.conf['codec']))

        self.bitrate_label.SetMinSize((160, 17))
        self.bitrate.SetMinSize((210, 50))

        self.framerate_label.SetMinSize((160, 17))
        self.framerate.SetMinSize((210, 50))

        self.iface_label.SetMinSize((140, 17))
        self.iface.SetMinSize((80, 25))
        self.iface.SetSelection(netifaces.index(self.main.conf['iface']))

        self.ip_label.SetMinSize((140, 17))
        self.ip.SetMinSize((150, 25))

        self.port_label.SetMinSize((140, 17))

        self.protocol.SetSelection(supported_protocols.index(self.main.conf['protocol']))

        for name, el in self.qos + self.bs + self.vq:
            if name in self.main.conf['qos'] + self.main.conf['bs'] + self.main.conf['vq']:
                el.SetValue(True)

        self.results_tab.Hide()
        self.video_tab.Hide()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: VTframe.__do_layout
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(1, 2, 0, 0)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.GridSizer(2, 2, 3, 3)
        self.sizer_5_staticbox.Lower()
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.HORIZONTAL)
        grid_sizer_4 = wx.GridSizer(4, 3, 0, 0)

        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_16_staticbox.Lower()
        sizer_16 = wx.StaticBoxSizer(self.sizer_16_staticbox, wx.HORIZONTAL)
        grid_sizer_6 = wx.GridSizer(2, 2, 0, 0)
        self.sizer_15_staticbox.Lower()
        sizer_15 = wx.StaticBoxSizer(self.sizer_15_staticbox, wx.HORIZONTAL)
        grid_sizer_3 = wx.GridSizer(4, 2, 0, 0)

        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        grid_sizer_2 = wx.GridSizer(4, 1, 0, 0)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_2_staticbox.Lower()
        sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.HORIZONTAL)
        grid_sizer_5 = wx.GridSizer(4, 1, 0, 0)
        sizer_8a = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(self.video_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_6.Add(self.video, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_5.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_7.Add(self.codec_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_7.Add(self.codec, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_5.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_8.Add(self.bitrate_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_8.Add(self.bitrate, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_5.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_8a.Add(self.framerate_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_8a.Add(self.framerate, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_5.Add(sizer_8a, 1, wx.EXPAND, 0)
        sizer_2.Add(grid_sizer_5, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_9.Add(self.iface_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_9.Add(self.iface, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_2.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_10.Add(self.ip_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_10.Add(self.ip, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_2.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_11.Add(self.port_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_11.Add(self.port, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_2.Add(sizer_11, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.protocol, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_3.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        for name, el in self.qos:
            grid_sizer_3.Add(el, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_15.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        sizer_14.Add(sizer_15, 1, wx.EXPAND, 0)
        for name, el in self.bs:
            grid_sizer_6.Add(el, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_16.Add(grid_sizer_6, 1, wx.EXPAND, 0)
        sizer_14.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_14, 1, wx.EXPAND, 0)
        for name, el in self.vq:
            grid_sizer_4.Add(el, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        sizer_5.Add(grid_sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        self.options_tab.SetSizer(sizer_1)
        sizer_13.Add(self.log, 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        self.log_tab.SetSizer(sizer_13)
        grid_sizer_1.Add(self.label_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.play_video, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.video_tab.SetSizer(grid_sizer_1)
        self.tabs.AddPage(self.options_tab, "Configuration")
        self.tabs.AddPage(self.log_tab, "Log")
        self.tabs.AddPage(self.results_tab, "Results")
        self.tabs.AddPage(self.video_tab, "Video")
        sizer_12.Add(self.tabs, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_12)
        self.Layout()
        self.Centre()
        # end wxGlade

    def onExit(self, event): # wxGlade: VTframe.<event_handler>
        self.Close(True)

    def onCloseWindow(self, event):
        """
        Show a dialog to verify exit.
        """
        # dialog to verify exit (including menuExit)
        dlg = wx.MessageDialog(self, "Do you want to exit?", "Exit", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            try:
                self.pipeline.set_state(Gst.State.NULL)
            except:
                pass
            VTLOG.handlers[0] = self.old_hdlr
            self.Destroy() # frame

    def onAbout(self, event):
        """
        Show *About* dialog.
        """
        import textwrap
        license = textwrap.dedent('''\
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.''')
        info = wx.AboutDialogInfo()
        #info.SetIcon(getVTIcon())
        info.SetName('Video Tester')
        info.SetVersion('0.2')
        info.SetDescription('Video Quality Assessment Tool')
        info.SetCopyright('(C) 2011-2016 Iñaki Úcar')
        info.SetWebSite('https://github.com/Enchufa2/video-tester')
        info.SetLicense(license)
        info.AddDeveloper('Iñaki Úcar <i.ucar86@gmail.com>')
        info.AddDocWriter('Iñaki Úcar <i.ucar86@gmail.com>')
        info.AddArtist('Almudena M. Castro <puraturadesign@gmail.com>')
        wx.AboutBox(info)

    def onOpen(self, event): # wxGlade: VTframe.<event_handler>
        """
        Show *Open files* dialog.
        """
        self.video_tab.Hide()
        wildcard = u'Pickle files (*.pkl)|*.pkl'
        dlg = wx.FileDialog(self, u'Open files', '', '', wildcard, wx.FD_MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.__open(dlg.GetDirectory(), dlg.GetFilenames())
            dlg.Destroy()
            self.results()

    def __open(self, path, files):
        self.main.results = []
        for filename in files:
            f = open(path + '/' + filename, 'rb')
            self.main.results.append(pickle.load(f))
            f.close()

    def onRun(self, event): # wxGlade: VTframe.<event_handler>
        """
        Run VT Client.
        """
        self.options_tab.Disable()
        self.vtmenubar.Disable()
        self.results_tab.Hide()
        self.video_tab.Hide()
        self.tabs.SetSelection(1)
        self.vtstatusbar.SetStatusText('Running...')
        self.setValues()
        self.main.run()
        self.path = self.main.conf['tempdir'] + self.main.conf['num']
        self.results()
        self.configureVideos()
        self.options_tab.Enable()
        wx.Window.Enable(self.vtmenubar)
        self.vtstatusbar.SetStatusText('Stopped')

    def onPlay(self, event):
        """
        Play video files.
        """
        if self.play_video.GetLabel() == 'Play':
            self.pipeline = Gst.parse_launch('filesrc name=video1 filesrc name=video2 filesrc name=video3 \
                videomixer name=mix sink_0::alpha=0 sink_2::xpos=' + str(self.width*2) + ' sink_3::xpos=' + str(self.width) + ' ! xvimagesink \
                videotestsrc pattern="black" num-buffers=1 \
                    ! video/x-raw-yuv,width=' + str(self.width*3) + ',height=' + str(self.height) + ' \
                    ! mix.sink_0 \
                video1. \
                    ! queue ! videoparse framerate=' + self.fps + '/1 name=parser1 \
                    ! textoverlay font-desc="Sans 24" text="Original" valignment=top halignment=left shaded-background=true \
                    ! ffmpegcolorspace ! videoscale \
                    ! mix.sink_1 \
                video2. \
                    ! queue ! videoparse framerate=' + self.fps + '/1 name=parser2 \
                    ! textoverlay font-desc="Sans 24" text="Coded" valignment=top halignment=left shaded-background=true \
                    ! ffmpegcolorspace ! videoscale \
                    ! mix.sink_2 \
                video3. \
                    ! queue ! videoparse framerate=' + self.fps + '/1 name=parser3 \
                    ! textoverlay font-desc="Sans 24" text="Received" valignment=top halignment=left shaded-background=true \
                    ! ffmpegcolorspace ! videoscale \
                    ! mix.sink_3')
            self.play_video.SetLabel('Stop')
            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self.onMessage)
            video1 = self.pipeline.get_by_name('video1')
            video2 = self.pipeline.get_by_name('video2')
            video3 = self.pipeline.get_by_name('video3')
            video1.props.location = self.paths['original']
            video2.props.location = self.paths['coded']
            video3.props.location = self.paths['received']
            parser1 = self.pipeline.get_by_name('parser1')
            parser2 = self.pipeline.get_by_name('parser2')
            parser3 = self.pipeline.get_by_name('parser3')
            parser1.props.width = self.width
            parser1.props.height = self.height
            parser2.props.width = self.width
            parser2.props.height = self.height
            parser3.props.width = self.width
            parser3.props.height = self.height
            self.pipeline.set_state(Gst.State.PLAYING)
        else:
            self.pipeline.set_state(Gst.State.NULL)
            self.play_video.SetLabel('Play')

    def onMessage(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS or t == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            self.play_video.SetLabel('Play')

    def results(self):
        """
        Plot measures and show *Results* tab.
        """
        self.results_tab.removePages()
        for measure in self.main.results:
            axes = self.results_tab.add(measure['name']).gca()
            if measure['type'] == 'plot':
                axes.plot(measure['axes'][0], measure['axes'][1], 'b')
                axes.plot(measure['axes'][0], [measure['mean'] for i in measure['axes'][0]], 'g')
                axes.plot(measure['axes'][0], [measure['max'][1] for i in measure['axes'][0]], 'r')
                axes.plot(measure['axes'][0], [measure['min'][1] for i in measure['axes'][0]], 'r')
                axes.set_xlabel(measure['units'][0])
                axes.set_ylabel(measure['units'][1])
            elif measure['type'] == 'value':
                width = 1
                axes.bar([0.5], measure['value'], width=width)
                axes.set_ylabel(measure['units'])
                axes.set_xticks([1])
                axes.set_xlim(0, 2)
                axes.set_xticklabels([measure['name']])
            elif measure['type'] == 'bar':
                axes.bar(measure['axes'][0], measure['axes'][1], width=measure['width'])
                axes.plot(measure['axes'][0], [measure['mean'] for i in measure['axes'][0]], 'g')
                axes.plot(measure['axes'][0], [measure['max'][1] for i in measure['axes'][0]], 'r')
                axes.plot(measure['axes'][0], [measure['min'][1] for i in measure['axes'][0]], 'r')
                axes.set_xlabel(measure['units'][0])
                axes.set_ylabel(measure['units'][1])
            elif measure['type'] == 'videoframes':
                axes.bar(measure['axes'][0], measure['axes'][1]['B'], width=1, color='g')
                axes.bar(measure['axes'][0], measure['axes'][1]['P'], width=1, color='b')
                axes.bar(measure['axes'][0], measure['axes'][1]['I'], width=1, color='r')
                axes.set_xlabel(measure['units'][0])
                axes.set_ylabel(measure['units'][1])
        self.results_tab.Show()

    def configureVideos(self):
        """
        Configure and show *Video* tab.
        """
        f = open(self.path + '_caps.txt', 'rb')
        caps = f.read()
        f.close()
        caps = caps.split(', ')
        for x in caps:
            if x.find('width') != -1:
                self.width = int(x[11:len(x)])
            elif x.find('height') != -1:
                self.height = int(x[12:len(x)])
        self.paths = dict()
        self.paths['original'] = self.path + '_ref_original.yuv'
        self.paths['coded'] = self.path + '_ref.yuv'
        self.paths['received'] = self.path + '.yuv'
        self.video_tab.Show()

    def setValues(self):
        """
        Set configuration options.
        """
        self.main.conf['bitrate'] = int(self.bitrate.GetValue())
        self.main.conf['framerate'] = int(self.framerate.GetValue())
        self.main.conf['video'] = str(self.video.GetStringSelection())
        self.main.conf['codec'] = str(self.codec.GetStringSelection())
        self.main.conf['iface'] = str(self.iface.GetStringSelection())
        self.main.conf['ip'] = str(self.ip.GetValue())
        self.main.port = int(self.port.GetValue())
        self.main.conf['protocol'] = str(self.protocol.GetStringSelection())
        qos = []
        for name, el in self.qos:
            if el.GetValue():
                qos.append(name)
        self.main.conf['qos'] = qos
        bs = []
        for name, el in self.bs:
            if el.GetValue():
                bs.append(name)
        self.main.conf['bs'] = bs
        vq = []
        for name, el in self.vq:
            if el.GetValue():
                vq.append(name)
        self.main.conf['vq'] = vq

# end of class VTframe

class Plot(wx.Panel):
    """
    Plot panel.
    """
    def __init__(self, parent, id = -1, dpi = None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2,2))
        self.canvas = Canvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas,1,wx.EXPAND)
        sizer.Add(self.toolbar, 0 , wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)

class PlotNotebook(wx.Panel):
    """
    Tab-style plotting panel.
    """
    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id=id)
        self.nb = wx.aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.pages = []

    def add(self, name="plot"):
        """
        Add a tab.
        """
        page = Plot(self.nb)
        self.pages.append(page)
        self.nb.AddPage(page, name)
        return page.figure

    def removePages(self):
        """
        Remove all tabs.
        """
        for page in self.pages:
            self.nb.DeletePage(0)

class VTApp(wx.App):
    """
    WxPython application class.
    """
    def __init__(self, conf):
        self.conf = conf
        wx.App.__init__(self)

    def OnInit(self):
        vtframe = VTframe(self.conf)
        self.SetTopWindow(vtframe)
        vtframe.Show()
        return True

# end of class Clientgui
