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
        
        filename = self.m_sDataDir+'glade/findColor.glade'
        self.m_oPropertiesXML = PropertiesXML
        self.m_oS2iBlockProperties = S2iBlockProperties

        widget_list = [
            'Properties',
						'_R',
						'_G',
						'_B',
						'_R_T',
						'_G_T',
						'_B_T',
            'propBackgroundColor',
            'propBorderColor',
            'propHelpView',
						'prop_confirm'
            ]

        handlers = [
            'on_prop_cancel_clicked',
            'on_prop_confirm_clicked',
            'on_propBackColorButton_clicked',
            'on_propBorderColorButton_clicked'
            ]

        top_window = 'Properties'

        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        
        self.widgets['Properties'].set_icon_from_file(self.m_sDataDir+"images/harpia_ave.png")

        #load properties values
        for Property in self.m_oPropertiesXML.properties.block.property:
					if Property.name == "_R":
						self.widgets['_R'].set_value( float(Property.value) );
					if Property.name == "_G":
						self.widgets['_G'].set_value( float(Property.value) );
					if Property.name == "_B":
						self.widgets['_B'].set_value( float(Property.value) );
					if Property.name == "_R_T":
						self.widgets['_R_T'].set_value( float(Property.value) );
					if Property.name == "_G_T":
						self.widgets['_G_T'].set_value( float(Property.value) );
					if Property.name == "_B_T":
						self.widgets['_B_T'].set_value( float(Property.value) );

					#if Property.name == "isFilling":
						#if Property.value == "true":
							#self.widgets['isFilling'].set_active( True );
						#else:
							#self.widgets['isFilling'].set_active( False );

					#if Property.name == "isScalling":
						#if Property.value == "true":
							#self.widgets['isScalling'].set_active( True );
						#else:
							#self.widgets['isScalling'].set_active( False );

					#if Property.name == "isCenter":
						#if Property.value == "true":
							#self.widgets['isAtCenter'].set_active( True );
						#else:
							#self.widgets['isAtPoint'].set_active( True );


        #load border color
        self.m_oBorderColor = self.m_oS2iBlockProperties.GetBorderColor()

        t_nBorderRed   = self.m_oBorderColor[0] * 257
        t_nBorderGreen = self.m_oBorderColor[1] * 257
        t_nBorderBlue  = self.m_oBorderColor[2] * 257

        t_oBorderColor = gtk.gdk.Color(red=t_nBorderRed,green=t_nBorderGreen,blue=t_nBorderBlue)

        self.widgets['propBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oBorderColor)        

        #load block color
        self.m_oBackColor = self.m_oS2iBlockProperties.GetBackColor()

        t_nBackRed   = self.m_oBackColor[0] * 257
        t_nBackGreen = self.m_oBackColor[1] * 257
        t_nBackBlue  = self.m_oBackColor[2] * 257

        t_oBackColor = gtk.gdk.Color(red=t_nBackRed,green=t_nBackGreen,blue=t_nBackBlue)

        self.widgets['propBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oBackColor)

        #load help text
        t_oS2iHelp = bt.bind_file(self.m_sDataDir+'help/findColor'+ _('_en.help'))
        
        t_oTextBuffer = gtk.TextBuffer()

        t_oTextBuffer.set_text( unicode( str( t_oS2iHelp.help.content) ) )
    
        self.widgets['propHelpView'].set_buffer( t_oTextBuffer )
        
    #----------------------------------------------------------------------

    def __del__(self):
				pass

    #---------------------------------------------------------------------- 

    def on_prop_cancel_clicked( self, *args ):
        self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------
   
    def on_prop_confirm_clicked( self, *args ):
			self.widgets['prop_confirm'].grab_focus()
			for Property in self.m_oPropertiesXML.properties.block.property:
				if Property.name == "_R":
					Property.value = unicode(self.widgets['_R'].get_value())
				if Property.name == "_G":
					Property.value = unicode(self.widgets['_G'].get_value())
				if Property.name == "_B":
					Property.value = unicode(self.widgets['_B'].get_value())
				if Property.name == "_R_T":
					Property.value = unicode(self.widgets['_R_T'].get_value())
				if Property.name == "_G_T":
					Property.value = unicode(self.widgets['_G_T'].get_value())
				if Property.name == "_B_T":
					Property.value = unicode(self.widgets['_B_T'].get_value())
				
				#if Property.name == "isCenter":
					#if self.widgets['isAtCenter'].get_active():
						#Property.value = u"true"
					#else:
						#Property.value = u"false"

				#if Property.name == "isFilling":
					#if self.widgets['isFilling'].get_active():
						#Property.value = u"true"
					#else:
						#Property.value = u"false"

				#if Property.name == "isScalling":
					#if self.widgets['isScalling'].get_active():
						#Property.value = u"true"
					#else:
						#Property.value = u"false"

				
			self.m_oS2iBlockProperties.SetPropertiesXML( self.m_oPropertiesXML )

			self.m_oS2iBlockProperties.SetBorderColor( self.m_oBorderColor )
			self.m_oS2iBlockProperties.SetBackColor( self.m_oBackColor )
			self.widgets['Properties'].destroy()

    #----------------------------------------------------------------------

    def on_propBackColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['propBackgroundColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBackColor[0] = t_oColor.red / 257

            self.m_oBackColor[1] = t_oColor.green / 257

            self.m_oBackColor[2] = t_oColor.blue / 257

    #----------------------------------------------------------------------

    def on_propBorderColorButton_clicked(self,*args):

        t_oColor = self.RunColorSelection()

        if t_oColor <> None:
            
            self.widgets['propBorderColor'].modify_bg(gtk.STATE_NORMAL,t_oColor)

            self.m_oBorderColor[0] = t_oColor.red / 257
            
            self.m_oBorderColor[1] = t_oColor.green / 257

            self.m_oBorderColor[2] = t_oColor.blue / 257
            
    #----------------------------------------------------------------------
    
#propProperties = Properties()()
#propProperties.show( center=0 )


