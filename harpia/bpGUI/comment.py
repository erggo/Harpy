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

from harpia.GladeWindow import GladeWindow
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

#----------------------------------------------------------------------
   
class Properties( GladeWindow, S2iCommonProperties ):

    #----------------------------------------------------------------------

    def __init__( self, PropertiesXML, S2iBlockProperties):
        
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        
        filename = self.m_sDataDir+'glade/comment.glade'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
            'COMMENTBackgroundColor',
            'COMMENTBorderColor',
            'COMMENTHelpView',
            'COMMENTView'
            ]

        handlers = [
            'on_COMMENTBackColorButton_clicked',
            'on_COMMENTBorderColorButton_clicked',
            'on_comment_cancel_clicked',
            'on_comment_confirm_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        self.widgets['Properties'].set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")

        #load block color
        self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()
        
        #load properties values
        for Property in self.m_oPropertiesXML.properties.block.property:

            #self.widgets['FILLBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)
            
            if Property.name == "comment":
                self.m_sComment = str(Property.value)
                #print self.m_sComment

        #load border color
        self.m_oBorderColor = self.m_oS2iBlockProperties.GetBorderColor()

        t_nBorderRed   = self.m_oBorderColor[0] * 257
        t_nBorderGreen = self.m_oBorderColor[1] * 257
        t_nBorderBlue  = self.m_oBorderColor[2] * 257

        t_oBorderColor = gtk.gdk.Color(red=t_nBorderRed,green=t_nBorderGreen,blue=t_nBorderBlue)

        self.widgets['COMMENTBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oBorderColor)        

        #load block color
        #self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()

        t_nBackRed   = self.m_oBackColor[0] * 257
        t_nBackGreen = self.m_oBackColor[1] * 257
        t_nBackBlue  = self.m_oBackColor[2] * 257

        t_oBackColor = gtk.gdk.Color(red=t_nBackRed,green=t_nBackGreen,blue=t_nBackBlue)

        self.widgets['COMMENTBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)
        
        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+"help/comment"+ _("_en.help"))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['COMMENTHelpView'].set_buffer( t_oTextBuffer )
		
        # Comment View
        
        t_sComment = gtk.TextBuffer()
        t_sComment.set_text(self.m_sComment)
        
        self.widgets['COMMENTView'].set_buffer(t_sComment)
        self.widgets['COMMENTView'].set_property('editable', True)
        
        self.widgets['COMMENTView'].set_cursor_visible(True)

    #----------------------------------------------------------------------

    def __del__(self):
        
	pass

    #---------------------------------------------------------------------- 

    def on_comment_cancel_clicked( self, *args ):

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------
   
    def on_comment_confirm_clicked( self, *args ):

        for Property in self.m_oPropertiesXML.properties.block.property:

            if Property.name == "comment":
               t_oText = self.widgets['COMMENTView'].get_buffer()
               t_oStart = t_oText.get_start_iter()
               t_oEnd = t_oText.get_end_iter()
               t_sComment = t_oText.get_text(t_oStart, t_oEnd)
               Property.value = unicode(t_sComment )


        self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )
        
        self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )

        self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )

        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

    def on_COMMENTBackColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['COMMENTBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBackColor[0] = t_oColor.red / 257

            self.m_oBackColor[1] = t_oColor.green / 257

            self.m_oBackColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

    def on_COMMENTBorderColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['COMMENTBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBorderColor[0] = t_oColor.red / 257
            
            self.m_oBorderColor[1] = t_oColor.green / 257

            self.m_oBorderColor[2] = t_oColor.blue / 257
            
    #----------------------------------------------------------------------

    def on_COMMENTFillColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:

            self.widgets['COMMENTBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            # Sets the back color the same as the color selected for filling
            self.m_oBackColor[0] = t_oColor.red / 257
            self.m_oBackColor[1] = t_oColor.green / 257
            self.m_oBackColor[2] = t_oColor.blue / 257
  
#CommentProperties = Properties()
#CommentProperties.show( center=0 )


