from gi import Keybinder
from gi import Gtk


def test_func(data):
    print(data)


if __name__ == '__main__':
    wnd = Gtk.Window()
    wnd.connect('delete-event', Gtk.main_quit)
    wnd.show_all()
    
    Keybinder.init()
    if not Keybinder.bind('<Super>q', test_func, 'Hi there!'):
        print("Keybinder.bind() failed.")

    Gtk.main()
