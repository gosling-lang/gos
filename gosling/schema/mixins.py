# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly.
from . import core
from gosling.schemapi import Undefined
from typing import TypeVar


T = TypeVar('T')
class MarkMethodMixin(object):
    """A mixin class that defines mark methods"""

    def mark_point(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                   bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                   enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                   legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                   outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                   textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                   textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'point'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "point"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_line(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                  bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                  enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                  legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                  outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                  textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                  textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'line'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "line"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_area(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                  bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                  enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                  legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                  outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                  textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                  textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'area'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "area"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_bar(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                 bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                 enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                 legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                 outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                 textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                 textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'bar'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "bar"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_rect(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                  bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                  enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                  legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                  outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                  textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                  textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'rect'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "rect"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_text(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                  bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                  enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                  legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                  outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                  textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                  textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'text'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "text"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_withinLink(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                        bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined,
                        dy=Undefined, enableSmoothPath=Undefined, flatWithinLink=Undefined,
                        inlineLegend=Undefined, legendTitle=Undefined, linePattern=Undefined,
                        linkConnectionType=Undefined, outline=Undefined, outlineWidth=Undefined,
                        textAnchor=Undefined, textFontSize=Undefined, textFontWeight=Undefined,
                        textStroke=Undefined, textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'withinLink'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "withinLink"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_betweenLink(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                         bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined,
                         dy=Undefined, enableSmoothPath=Undefined, flatWithinLink=Undefined,
                         inlineLegend=Undefined, legendTitle=Undefined, linePattern=Undefined,
                         linkConnectionType=Undefined, outline=Undefined, outlineWidth=Undefined,
                         textAnchor=Undefined, textFontSize=Undefined, textFontWeight=Undefined,
                         textStroke=Undefined, textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'betweenLink'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "betweenLink"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_rule(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                  bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                  enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                  legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                  outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                  textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                  textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'rule'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "rule"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_triangleLeft(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                          bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined,
                          dy=Undefined, enableSmoothPath=Undefined, flatWithinLink=Undefined,
                          inlineLegend=Undefined, legendTitle=Undefined, linePattern=Undefined,
                          linkConnectionType=Undefined, outline=Undefined, outlineWidth=Undefined,
                          textAnchor=Undefined, textFontSize=Undefined, textFontWeight=Undefined,
                          textStroke=Undefined, textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'triangleLeft'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "triangleLeft"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_triangleRight(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                           bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined,
                           dy=Undefined, enableSmoothPath=Undefined, flatWithinLink=Undefined,
                           inlineLegend=Undefined, legendTitle=Undefined, linePattern=Undefined,
                           linkConnectionType=Undefined, outline=Undefined, outlineWidth=Undefined,
                           textAnchor=Undefined, textFontSize=Undefined, textFontWeight=Undefined,
                           textStroke=Undefined, textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'triangleRight'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "triangleRight"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_triangleBottom(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                            bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined,
                            dy=Undefined, enableSmoothPath=Undefined, flatWithinLink=Undefined,
                            inlineLegend=Undefined, legendTitle=Undefined, linePattern=Undefined,
                            linkConnectionType=Undefined, outline=Undefined, outlineWidth=Undefined,
                            textAnchor=Undefined, textFontSize=Undefined, textFontWeight=Undefined,
                            textStroke=Undefined, textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'triangleBottom'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "triangleBottom"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_brush(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                   bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                   enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                   legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                   outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                   textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                   textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'brush'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "brush"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy

    def mark_header(self: T, align=Undefined, background=Undefined, backgroundOpacity=Undefined,
                    bezierLink=Undefined, curve=Undefined, dashed=Undefined, dx=Undefined, dy=Undefined,
                    enableSmoothPath=Undefined, flatWithinLink=Undefined, inlineLegend=Undefined,
                    legendTitle=Undefined, linePattern=Undefined, linkConnectionType=Undefined,
                    outline=Undefined, outlineWidth=Undefined, textAnchor=Undefined,
                    textFontSize=Undefined, textFontWeight=Undefined, textStroke=Undefined,
                    textStrokeWidth=Undefined, **kwds) -> T:
        """Set the track's mark to 'header'
    
        For information on additional arguments, see :class:`Style`
        """
        kwds = dict(align=align, background=background, backgroundOpacity=backgroundOpacity,
                    bezierLink=bezierLink, curve=curve, dashed=dashed, dx=dx, dy=dy,
                    enableSmoothPath=enableSmoothPath, flatWithinLink=flatWithinLink,
                    inlineLegend=inlineLegend, legendTitle=legendTitle, linePattern=linePattern,
                    linkConnectionType=linkConnectionType, outline=outline, outlineWidth=outlineWidth,
                    textAnchor=textAnchor, textFontSize=textFontSize, textFontWeight=textFontWeight,
                    textStroke=textStroke, textStrokeWidth=textStrokeWidth, **kwds)
        copy = self.copy()
        copy.mark = "header"
        if any(val is not Undefined for val in kwds.values()):
            copy.style = core.Style(**kwds)
        return copy