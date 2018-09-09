# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function, division, absolute_import, unicode_literals

from .constants import GLYPHS_PREFIX
from glyphsLib.types import Point

LIB_KEY = GLYPHS_PREFIX + "hints"


def to_ufo_hints(self, ufo_glyph, layer):
    try:
        value = layer.hints
    except KeyError:
        return
    hints = []
    for hi in value:
        hint = {}
        for attr in ["horizontal", "options", "stem", "type"]:
            val = getattr(hi, attr, None)
            hint[attr] = val
        for attr in ["origin", "other1", "other2", "place", "scale", "target"]:
            val = getattr(hi, attr, None)
            # FIXME: (jany) what about target = up/down?
            if val is not None and not any(v is None for v in val):
                hint[attr] = list(val)
        hints.append(hint)

    if hints:
        ufo_glyph.lib[LIB_KEY] = hints


def to_glyphs_hints(self, ufo_glyph, layer):
    if LIB_KEY not in ufo_glyph.lib:
        return
    for hint in ufo_glyph.lib[LIB_KEY]:
        hi = self.glyphs_module.GSHint()
        for attr in ["horizontal", "options", "stem", "type"]:
            setattr(hi, attr, hint[attr])
        for attr in ["origin", "other1", "other2", "place", "scale", "target"]:
            # FIXME: (jany) what about target = up/down?
            if attr in hint:
                value = Point(*hint[attr])
                setattr(hi, attr, value)
        layer.hints.append(hi)
