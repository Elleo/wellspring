# style.py
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

class Style:

    def __init__(self):
        pass

    def generate_css(self):
        return """
                body {
                    font-family: monospace;
                    text-align: center;
                    font-size: 12pt;
                    margin: 20px;
                    margin-bottom: 800px;
                    line-height: 1.5em;
                }

                .jouvence-main {
                    width: 700px;
                    margin-left: auto;
                    margin-right: auto;
                }

                .jouvence-scene-heading, .jouvence-action {
                    text-align: left;
                }

                .jouvence-character {
                    margin-bottom: 0;
                    padding-bottom: 0;
                }

                .jouvence-dialog {
                    margin-top: 0;
                    margin-left: auto;
                    margin-right: auto;
                    max-width: 400px;
                }

                .jouvence-title-page {
                    padding-top: 300px;
                    padding-bottom: 300px;
                }

                hr {
                    margin-bottom: 50px;
                }

        """
