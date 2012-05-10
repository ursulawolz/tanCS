from gi.repository import GtkClutter
GtkClutter.init([])
from gi.repository import GObject, GtkClutter, Clutter, Gtk

def pressed(widget, event):
    print widget, event

w = Gtk.Window()
e = GtkClutter.Embed.new()
e.set_size_request(500, 500)
w.add(e)

s = e.get_stage()
s.set_color(Clutter.Color.new(0,0,0,0))
s.set_size(500, 500)

r = Clutter.Rectangle()
r.set_color(Clutter.Color.new(255,255,255,255))
r.set_size(200,200)
r.set_position(0,0)
r.set_reactive(True)
s.add_actor(r)

s.connect('button-press-event', pressed)
# r.connect('button-press-event', pressed)
w.show_all()
Gtk.main()