# window.py
#
# Copyright 2024 Mike Sheldon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi

gi.require_version('WebKit', '6.0')
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Gio, Adw, GLib, GObject
from gi.repository.WebKit import WebView, WebsiteDataManager
from jouvence.parser import JouvenceParser
from jouvence.html import HtmlDocumentRenderer
from io import StringIO
from .style import Style


@Gtk.Template(resource_path='/com/mikeasoft/wellspring/window.ui')
class WellspringWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'WellspringWindow'

    web_view = Gtk.Template.Child()
    content_manager = Gtk.Template.Child()
    zoom = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style = Style()
        self.parser = JouvenceParser()
        self.markup = "Title: Hello World\nAuthor: Mike Sheldon\n\n>**Act One**<\n\nINT. COMPUTER ROOM - DAY\n\nA young woman is sat at a computer reading the text from a monitor\n\nNELLIE\nHello world!"
        self.renderer = HtmlDocumentRenderer(standalone=False)
        self.a = True
        self.scroll_position = 0
        self.content_manager.register_script_message_handler("scrollPosition")
        self.content_manager.connect("script-message-received::scrollPosition", self.update_scroll_position)
        self.zoom.set_icons(['zoom-in-symbolic']) # Blueprint doesn't like icons property
        self.update()
        self.key_controller = Gtk.EventControllerKey()
        self.key_controller.connect('key-pressed', self.key_pressed)
        self.web_view.add_controller(self.key_controller)
        settings = self.web_view.get_settings()
        settings.set_enable_write_console_messages_to_stdout(True)

    def console_message(self, message):
        print(message)

    def update_scroll_position(self, _, position):
        self.scroll_position = position.to_int32()

    def key_pressed(self, controller, key, value, state):
        if key == Gdk.KEY_Return:
            self.markup += "\n"
        elif key == Gdk.KEY_BackSpace:
            self.markup = self.markup[:-1]
        elif key == Gdk.KEY_Shift_L or key == Gdk.KEY_Shift_R:
            pass
        else:
            self.markup += chr(Gdk.keyval_to_unicode(key))
        self.update()

    def update(self):
        io = StringIO()
        self.document = self.parser.parseString(self.markup)

        self.renderer.render_doc(self.document, io)
        html = """<html>
            <head>
                <style>
                """ + self.style.generate_css() + """
                </style>
                <script>
                    window.addEventListener("load", function(event) {
                        window.scrollTo(0, """ + str(self.scroll_position) + """);
                    });

                    window.onscroll = function(e) {
                        window.webkit.messageHandlers.scrollPosition.postMessage(window.scrollY);
                    };
                </script>
            </head>
            <body contenteditable="true">
            """ + io.getvalue() + """
            </body>
        </html>"""
        self.web_view.load_html(html)


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Wellspring'
        self.props.version = "0.1.0"
        self.props.authors = ['Mike Sheldon']
        self.props.copyright = '2024 Mike Sheldon <mike@mikeasoft.com>'
        self.props.logo_icon_name = 'com.mikeasoft.wellspring'
        self.props.modal = True
        self.set_transient_for(parent)
