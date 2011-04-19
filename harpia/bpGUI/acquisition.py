# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br), Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br), Mathias Erdtmann (erdtmann@gmail.com) and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
#----------------------------------------------------------------------

from harpia.GladeWindow import  GladeWindow
from harpia.amara import binderytools as bt
import gtk
from harpia.s2icommonproperties import S2iCommonProperties
#i18n
import os
import gettext
APP='harpia'
DIR=os.environ['HARPIA_DATA_DIR']+'po'
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)


from glob import glob

#----------------------------------------------------------------------

class Properties( GladeWindow, S2iCommonProperties):

    #----------------------------------------------------------------------

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/acquisition.glade'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties
        
        widget_list = [
            'Properties',
            'ACQURadioFile',
            'ACQURadioNewImage',
            'ACQURadioCapture',
            'ACQURadioLive',
            'ACQURadioVideo',
            'ACQULabelFileProperty',
            'ACQULabelFilename',
            'ACQUFilename',
            'video_name',
            'video_name_BT',
            'video_name_LABEL',
            'video_name_LABEL2',
            'ACQUButtonSearch',
            'ACQULabelNewImage',
            'ACQULabelImageSize',
            'ACQULabelWidth',
            'ACQULabelHeight',
            'ACQUWidth',
            'ACQUHeight',
            'ACQULabelCameraProperty',
            'ACQULabelCamera',
            'ACQUCamera',
            'ACQULabelSize',
            'ACQUSize',
            'ACQUBackgroundColor',
            'ACQUBorderColor',
            'ACQUHelpView',
            'frameRate_Label',
            'frameRate',
            'streamProperties_label',
            'frameRate_label2',
						'acquisition_confirm'
            ]

        handlers = [
            'on_ACQURadioFile_pressed',
            'on_ACQURadioNewImage_pressed',
            'on_ACQURadioCapture_pressed',
            'on_ACQURadioLive_pressed',
            'on_ACQUButtonSearch_clicked',
            'on_ACQUVideoSearch_clicked',
            'on_ACQUBackColorButton_clicked',
            'on_ACQUBorderColorButton_clicked',
            'on_ACQURadioVideo_pressed',
            'on_acquisition_confirm_clicked',
            'on_acquisition_cancel_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)

        self.widgets['Properties'].set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")
        
        self.m_nNumAvailableCams = 4
        
        if os.name == 'posix':
          self.m_nNumAvailableCams = 0
          t_lListVidDevs = glob("/dev/video*")
          self.m_nNumAvailableCams = len(t_lListVidDevs)
        
        self.widgets['ACQUCamera'].remove_text(0)
        for cam in range(self.m_nNumAvailableCams):
          self.widgets['ACQUCamera'].append_text(str("/dev/video"+ str(cam)))
        self.widgets['ACQUCamera'].append_text(str("Default"))

        

        self.m_sCurrentActive = 'file'
        #load properties values        
        for Property in self.m_oPropertiesXML.properties.block.property:

            if Property.name == "type":
                if Property.value == "file":
                    self.widgets['ACQURadioFile'].set_active( True );
                    self.on_ACQURadioFile_pressed()
                elif Property.value == "camera":
                    self.widgets['ACQURadioCapture'].set_active( True );
                    self.on_ACQURadioCapture_pressed()
                    self.m_sCurrentActive = 'camera'
                elif Property.value == "live":
                    self.widgets['ACQURadioLive'].set_active( True );
                    self.on_ACQURadioLive_pressed()
                    self.m_sCurrentActive = 'live'
                elif Property.value == "video":
                    self.widgets['ACQURadioVideo'].set_active( True );
                    self.on_ACQURadioVideo_pressed()
                    self.m_sCurrentActive = 'video'
                else:
                    self.widgets['ACQURadioNewImage'].set_active( True );
                    self.on_ACQURadioNewImage_pressed()
                    self.m_sCurrentActive = 'newimage'
            if Property.name == "filename":
                self.widgets['ACQUFilename'].set_text( Property.value );
            if Property.name == "video_name":
                self.widgets['video_name'].set_text( Property.value );

            if Property.name == "camera" or Property.name == 'live':
              if os.name == 'posix':
                if int(Property.value) < self.m_nNumAvailableCams:
                  self.widgets['ACQUCamera'].set_active( int(Property.value) );
                else:
                  self.widgets['ACQUCamera'].set_active(self.m_nNumAvailableCams); #will set None

            if Property.name == "frameRate":
                self.widgets['frameRate'].set_value(float(Property.value));

            # Use the property size to set the New Image size too.
            if Property.name == "size":
                if Property.value == "1024x768":
                    self.widgets['ACQUSize'].set_active( 0 );
                if Property.value == "800x600":
                    self.widgets['ACQUSize'].set_active( 1 );
                if Property.value == "832x624":
                    self.widgets['ACQUSize'].set_active( 2 );
                if Property.value == "640x480":
                    self.widgets['ACQUSize'].set_active( 3 );
                else:
                    self.widgets['ACQUSize'].set_active( 0 );
                # New Image size
                
                self.widgets['ACQUWidth'].set_value( float(Property.value[ :Property.value.find('x')]) )
                self.widgets['ACQUHeight'].set_value( float( Property.value[Property.value.find('x')+1: ]) )



        #load block state 
        #load border color
        self.m_oBorderColor = self.m_oS2iBlockProperties.GetBorderColor()

        t_nBorderRed   = self.m_oBorderColor[0] * 257
        t_nBorderGreen = self.m_oBorderColor[1] * 257
        t_nBorderBlue  = self.m_oBorderColor[2] * 257

        t_oBorderColor = gtk.gdk.Color(red=t_nBorderRed,green=t_nBorderGreen,blue=t_nBorderBlue)

        self.widgets['ACQUBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oBorderColor)        

        #load block color
        self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()

        t_nBackRed   = self.m_oBackColor[0] * 257
        t_nBackGreen = self.m_oBackColor[1] * 257
        t_nBackBlue  = self.m_oBackColor[2] * 257

        t_oBackColor = gtk.gdk.Color(red=t_nBackRed,green=t_nBackGreen,blue=t_nBackBlue)

        self.widgets['ACQUBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)

        #load help text
        #t_oS2iHelp = bt.bind_file("../etc/acquisition/acquisition.help")
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/acquisition"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['ACQUHelpView'].set_buffer( t_oTextBuffer )

    #----------------------------------------------------------------------

    def __del__(self):
        pass

    #---------------------------------------------------------------------- 

    def on_acquisition_cancel_clicked( self, *args ):

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------
   
    def on_acquisition_confirm_clicked( self, *args ):
        self.widgets['acquisition_confirm'].grab_focus()
        t_sFilename = unicode(self.widgets['ACQUFilename'].get_text())

        for Property in self.m_oPropertiesXML.properties.block.property:

            if Property.name == "state":
                if self.m_oS2iBlockProperties.GetState():
                    Property.value = u"true"
                else:
                    Property.value = u"false"

            #file selected
            if Property.name == "type":
                if self.widgets['ACQURadioFile'].get_active():
                    Property.value = u"file"
                    self.m_sCurrentActive = 'file'
                elif self.widgets['ACQURadioCapture'].get_active():
                    Property.value = u"camera"
                    self.m_sCurrentActive = 'camera'
                elif self.widgets['ACQURadioLive'].get_active():
                    Property.value = u"live"
                    self.m_sCurrentActive = 'live'
                elif self.widgets['ACQURadioVideo'].get_active():
                    Property.value = u"video"
                    self.m_sCurrentActive = 'video'
                else:
                    Property.value = u"newimage"
                    self.m_sCurrentActive = 'newimage'

            if Property.name == "filename":
                Property.value = unicode(t_sFilename)
            if Property.name == "video_name":
                Property.value = unicode(unicode(self.widgets['video_name'].get_text()))
            #capture selected
            if Property.name == "frameRate":
                Property.value = unicode(str(self.widgets['frameRate'].get_value()))

            if Property.name == "camera" or Property.name == 'live':
              Camera = self.widgets['ACQUCamera'].get_active_text()
              if Camera <> u'Default':
                try:
                  if os.name == 'posix':
                    Property.value = unicode(Camera.split('video')[1]) ## getting rid of the /dev/video
                  else:
                    Property.value = unicode(Camera) ## just the num
                except:
                  Property.value = unicode("-1")
              else:
                Property.value = unicode('-1')
            
            if Property.name == "size":
                if self.m_sCurrentActive == 'camera' or self.m_sCurrentActive == 'live':
                    Size = int(self.widgets['ACQUSize'].get_active())
                    if Size == 0:
                        Property.value = unicode("1024x768")
                    if Size == 1:
                        Property.value = unicode("800x600")
                    if Size == 2:
                        Property.value = unicode("832x624")
                    if Size == 3:
                        Property.value = unicode("640x480")

                if self.m_sCurrentActive == 'newimage':
                    Width = int(self.widgets['ACQUWidth'].get_value())
                    Height = int(self.widgets['ACQUHeight'].get_value())
                    Property.value = unicode( str(Width) + 'x' + str(Height) )
                    
        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()
        
    #----------------------------------------------------------------------
    
    def on_ACQUBackColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['ACQUBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBackColor[0] = t_oColor.red / 257

            self.m_oBackColor[1] = t_oColor.green / 257

            self.m_oBackColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

    def on_ACQUBorderColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['ACQUBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBorderColor[0] = t_oColor.red / 257
            
            self.m_oBorderColor[1] = t_oColor.green / 257

            self.m_oBorderColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

    def on_ACQUButtonSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Abrir...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

#-------------
#Scotti
        if os.name == 'posix':
          dialog.set_current_folder("/home/" + str(os.getenv('USER')) + "/Desktop")
#Scotti

        filter = gtk.FileFilter()
        filter.set_name("All Archives")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("images")
        filter.add_mime_type("*.jpg")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['ACQUFilename'].set_text(response);

    #----------------------------------------------------------------------

    def on_ACQUVideoSearch_clicked( self, *args ):

        dialog = gtk.FileChooserDialog("Abrir...",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

#-------------
#Scotti
        if os.name == 'posix':
          dialog.set_current_folder("/home/" + str(os.getenv('USER')) + "/Desktop")
#Scotti

        filter = gtk.FileFilter()
        filter.set_name("All Archives")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("AVI Videos")
        filter.add_mime_type("*.avi")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            response =  dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            response = None
        dialog.destroy()

        self.widgets['video_name'].set_text(response);

    #----------------------------------------------------------------------


    def on_ACQURadioFile_pressed( self, *args ):

        self.widgets['ACQULabelCameraProperty'].set_sensitive( False )
        self.widgets['ACQULabelCamera'].set_sensitive( False )
        self.widgets['ACQUCamera'].set_sensitive( False )
        self.widgets['ACQULabelSize'].set_sensitive( False )
        self.widgets['ACQUSize'].set_sensitive( False )
        
        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )
        
        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )
        
        self.widgets['ACQULabelFileProperty'].set_sensitive( True )
        self.widgets['ACQULabelFilename'].set_sensitive( True )
        self.widgets['ACQUFilename'].set_sensitive( True )
        self.widgets['ACQUButtonSearch'].set_sensitive( True )
        
        self.widgets['frameRate_Label'].set_sensitive( False )
        self.widgets['frameRate'].set_sensitive( False )
        self.widgets['streamProperties_label'].set_sensitive( False )
        self.widgets['frameRate_label2'].set_sensitive( False )

    #----------------------------------------------------------------------
  
    def on_ACQURadioCapture_pressed( self, *args ):

        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )
        
        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )
        
        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )
        
        self.widgets['ACQULabelCameraProperty'].set_sensitive( True )
        self.widgets['ACQULabelCamera'].set_sensitive( True )
        self.widgets['ACQUCamera'].set_sensitive( True )
        self.widgets['ACQULabelSize'].set_sensitive( True )
        self.widgets['ACQUSize'].set_sensitive( True )
        
        self.widgets['frameRate_Label'].set_sensitive( False )
        self.widgets['frameRate'].set_sensitive( False )
        self.widgets['streamProperties_label'].set_sensitive( False )
        self.widgets['frameRate_label2'].set_sensitive( False )

    #----------------------------------------------------------------------
    def on_ACQURadioNewImage_pressed( self, *args ):

        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )
        
        self.widgets['ACQULabelCameraProperty'].set_sensitive( False )
        self.widgets['ACQULabelCamera'].set_sensitive( False )
        self.widgets['ACQUCamera'].set_sensitive( False )
        self.widgets['ACQULabelSize'].set_sensitive( False )
        self.widgets['ACQUSize'].set_sensitive( False )
        
        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )
        
        self.widgets['ACQULabelNewImage'].set_sensitive( True )
        self.widgets['ACQULabelImageSize'].set_sensitive( True )
        self.widgets['ACQULabelWidth'].set_sensitive( True )
        self.widgets['ACQULabelHeight'].set_sensitive( True )
        self.widgets['ACQUWidth'].set_sensitive( True )
        self.widgets['ACQUHeight'].set_sensitive( True )
				
        self.widgets['frameRate_Label'].set_sensitive( False )
        self.widgets['frameRate'].set_sensitive( False )
        self.widgets['streamProperties_label'].set_sensitive( False )
        self.widgets['frameRate_label2'].set_sensitive( False )
             
    def on_ACQURadioLive_pressed( self, *args ):
        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )
        
        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )
        
        self.widgets['video_name'].set_sensitive( False )
        self.widgets['video_name_BT'].set_sensitive( False )
        self.widgets['video_name_LABEL'].set_sensitive( False )
        self.widgets['video_name_LABEL2'].set_sensitive( False )
        
        self.widgets['ACQULabelCameraProperty'].set_sensitive( True )
        self.widgets['ACQULabelCamera'].set_sensitive( True )
        self.widgets['ACQUCamera'].set_sensitive( True )
        self.widgets['ACQULabelSize'].set_sensitive( True )
        self.widgets['ACQUSize'].set_sensitive( True )
        
        self.widgets['frameRate_Label'].set_sensitive( True )
        self.widgets['frameRate'].set_sensitive( True )
        self.widgets['streamProperties_label'].set_sensitive( True )
        self.widgets['frameRate_label2'].set_sensitive( True )
        
    def on_ACQURadioVideo_pressed( self, *args ):
        self.widgets['ACQULabelFileProperty'].set_sensitive( False )
        self.widgets['ACQULabelFilename'].set_sensitive( False )
        self.widgets['ACQUFilename'].set_sensitive( False )
        self.widgets['ACQUButtonSearch'].set_sensitive( False )
        
        self.widgets['ACQULabelNewImage'].set_sensitive( False )
        self.widgets['ACQULabelImageSize'].set_sensitive( False )
        self.widgets['ACQULabelWidth'].set_sensitive( False )
        self.widgets['ACQULabelHeight'].set_sensitive( False )
        self.widgets['ACQUWidth'].set_sensitive( False )
        self.widgets['ACQUHeight'].set_sensitive( False )
        
        self.widgets['video_name'].set_sensitive( True )
        self.widgets['video_name_BT'].set_sensitive( True )
        self.widgets['video_name_LABEL'].set_sensitive( True )
        self.widgets['video_name_LABEL2'].set_sensitive( True )
        
        self.widgets['ACQULabelCameraProperty'].set_sensitive( False )
        self.widgets['ACQULabelCamera'].set_sensitive( False )
        self.widgets['ACQUCamera'].set_sensitive( False )
        self.widgets['ACQULabelSize'].set_sensitive( False )
        self.widgets['ACQUSize'].set_sensitive( False )
        
        self.widgets['frameRate_Label'].set_sensitive( True )
        self.widgets['frameRate'].set_sensitive( True )
        self.widgets['streamProperties_label'].set_sensitive( True )
        self.widgets['frameRate_label2'].set_sensitive( True )
        
    #----------------------------------------------------------------------
       
#AcquisitionProperties = Properties( )
#AcquisitionProperties.show( center=0 )



