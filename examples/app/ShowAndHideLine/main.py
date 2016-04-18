import numpy as np
import h5py

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox, VBoxForm
from bokeh.models.widgets import Select, CheckboxButtonGroup
from bokeh.io import curdoc

a = 1
b = 0

data_select = Select(title="Output:", value="hip_strength", options=["hip_strength", "knee_strength"])
checkbox_button_group = CheckboxButtonGroup(labels=["first", "second"], active=[0, 1])

source = ColumnDataSource(data=dict(x=[], y=[]))
checkbox_source = ColumnDataSource(data=dict(first=[], second=[]))


p = Figure(plot_height=600, plot_width=800, title="", toolbar_location=None)
p.line(x="x", y="y", alpha="?", source=source)


# Fast direct read from hdf5
def get_data(f, name):
    shape = f[name].shape
    # Empty array
    data = np.empty(shape, dtype=np.float64)
    # read_direct to empty arrays
    f[name].read_direct(data)
    return data


def select_data():
    data_val = data_select.value
    with h5py.File('demo_data.hdf5', 'r') as f:
        return get_data(f, data_val)

def show_hide():
    if checkbox_button_group.active == 0:
        return 0
    if checkbox_button_group.active == 1:
        return 1


def update_data(attrname, old, new):
    # hardcoded length of 100
    x = list(range(1, 101))
    y = select_data()
    source.data = dict(x=x, y=y)

    first = show_hide()
    checkbox_source.data = dict(first=first)


data_select.on_change('value', update_data)
checkbox_button_group.on_click(update_data)

inputs = VBoxForm(data_select, checkbox_button_group, width=300)

update_data(None, None, None)

curdoc().add_root(HBox(inputs, p, width=1100))

