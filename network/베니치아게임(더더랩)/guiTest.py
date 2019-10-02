"""
Urwid example fibonacci sequence viewer / unbounded data demo
Features:
- custom list walker class for browsing infinite set
- custom wrap mode "numeric" for wrapping numbers to right and bottom
"""

import urwid

class FibonacciWalker(urwid.ListWalker):
    """ListWalker-compatible class for browsing fibonacci set.
    positions returned are (value at position-1, value at position) tuples.
    """
    def __init__(self):
        self.focus = (0,1)
        self.numeric_layout = NumericLayout()

    def _get_at_pos(self, pos):
        """Return a widget and the position passed."""
        return urwid.Text("%d"%pos[1], layout=self.numeric_layout), pos

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        a, b = start_from
        focus = b, a+b
        return self._get_at_pos(focus)

    def get_prev(self, start_from):
        a, b = start_from
        focus = b-a, a
        return self._get_at_pos(focus)

def main():
    palette = [
        ('body','black','dark cyan', 'standout'),
        ('foot','light gray', 'black'),
        ('key','light cyan', 'black', 'underline'),
        ('title', 'white', 'black',),
		('head','black','white','underline'),
        ]

    footer_text = [
        ('title', "Fibonacci Set Viewer"), "    ",
        ('key', "UP"), ", ", ('key', "DOWN"), ", ",
        ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
        " move view  ",
        ('key', "Q"), " exits",
        ]
    header_text = [
        ('title', "SCORE"), "    ",
        ('key', "UP"), ", ", ('key', "DOWN"), ", ",
        ('key', "PAGE UP"), " and ", ('key', "PAGE DOWN"),
        " move view  ",
        ('key', "Q"), " exits",
        ]
	

    def exit_on_q(input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    listbox = urwid.ListBox(FibonacciWalker())
    footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    header = urwid.AttrMap(urwid.Text(footer_text), 'head')
    body = urwid.AttrWrap(listbox, 'body')
    view = urwid.Frame(body=body,header=header, footer=footer)
    loop = urwid.MainLoop(view, palette, unhandled_input=exit_on_q)
    loop.run()
    # listbox = urwid.ListBox(FibonacciWalker())
    # footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    # view = urwid.Frame(urwid.AttrWrap(listbox, 'body'), footer=footer)
    # loop = urwid.MainLoop(view, palette, unhandled_input=exit_on_q)
    # loop.run()


class NumericLayout(urwid.TextLayout):
    """
    TextLayout class for bottom-right aligned numbers
    """
    def layout( self, text, width, align, wrap ):
        """
        Return layout structure for right justified numbers.
        """
        lt = len(text)
        r = lt % width # remaining segment not full width wide
        if r:
            linestarts = range( r, lt, width )
            return [
                # right-align the remaining segment on 1st line
                [(width-r,None),(r, 0, r)]
                # fill the rest of the lines
                ] + [[(width, x, x+width)] for x in linestarts]
        else:
            linestarts = range( 0, lt, width )
            return [[(width, x, x+width)] for x in linestarts]


if __name__=="__main__":
    main()