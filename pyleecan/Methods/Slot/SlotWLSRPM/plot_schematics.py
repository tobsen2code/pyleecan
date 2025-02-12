import matplotlib.pyplot as plt
from numpy import pi, exp

from ....Classes.Arc1 import Arc1
from ....Classes.LamSlot import LamSlot
from ....Classes.Segment import Segment
from ....definitions import config_dict
from ....Functions.Plot import (
    ARROW_COLOR,
    ARROW_WIDTH,
    MAIN_LINE_COLOR,
    MAIN_LINE_STYLE,
    MAIN_LINE_WIDTH,
    P_FONT_SIZE,
    SC_FONT_SIZE,
    SC_LINE_COLOR,
    SC_LINE_STYLE,
    SC_LINE_WIDTH,
    TEXT_BOX,
    plot_quote,
)
from ....Methods import ParentMissingError

MAGNET_COLOR = config_dict["PLOT"]["COLOR_DICT"]["MAGNET_COLOR"]


def plot_schematics(
    self,
    is_default=False,
    is_add_point_label=False,
    is_add_schematics=True,
    is_add_main_line=True,
    type_add_active=True,
    save_path=None,
    is_show_fig=True,
    fig=None,
    ax=None,
):
    """Plot the schematics of the slot

    Parameters
    ----------
    self : SlotWLSRPM
        A SlotWLSRPM object
    is_default : bool
        True: plot default schematics, else use current slot values
    is_add_point_label : bool
        True to display the name of the points (Z1, Z2....)
    is_add_schematics : bool
        True to display the schematics information (W0, H0...)
    is_add_main_line : bool
        True to display "main lines" (slot opening and 0x axis)
    type_add_active : int
        0: No active surface, 1: active surface as winding, 2: active surface as magnet
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    is_show_fig : bool
        To call show at the end of the method
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        Axis on which to plot the data

    Returns
    -------
    fig : Matplotlib.figure.Figure
        Figure containing the plot
    ax : Matplotlib.axes.Axes object
        Axis containing the plot
    """

    # Use some default parameter
    if is_default:
        slot = type(self)(Zs=12, W1=8e-3, W3=11.6e-3, H2=14.8e-3, R1=0.75e-3, H3=2e-3)
        lam = LamSlot(
            Rint=50.7e-3,
            Rext=72.5e-3,
            is_internal=False,
            is_stator=True,
            L1=0.95,
            Nrvd=0,
            Wrvd=0,
            slot=slot,
        )
        return slot.plot_schematics(
            is_default=False,
            is_add_point_label=is_add_point_label,
            is_add_schematics=is_add_schematics,
            is_add_main_line=is_add_main_line,
            type_add_active=type_add_active,
            save_path=save_path,
            is_show_fig=is_show_fig,
            fig=fig,
            ax=ax,
        )
    else:
        # Getting the main plot
        if self.parent is None:
            raise ParentMissingError("Error: The slot is not inside a Lamination")
        lam = self.parent
        fig, ax = lam.plot(
            alpha=pi / self.Zs, is_show_fig=False, fig=fig, ax=ax
        )  # center slot on Ox axis
        point_dict = self._comp_point_coordinate()
        if self.is_outwards():
            sign = 1
        else:
            sign = -1
        sp = 2 * pi / self.Zs  # Slot pitch
        # Adding point label
        if is_add_point_label:
            for name, Z in point_dict.items():
                ax.text(
                    Z.real,
                    Z.imag,
                    name,
                    fontsize=P_FONT_SIZE,
                    bbox=TEXT_BOX,
                )

        # Adding schematics
        if is_add_schematics:

            # W1
            line = Segment(
                point_dict["Z4"] + 0.005 - 1j * 0.002,
                point_dict["Z2"] + 0.005 - 1j * 0.002,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W1",
                offset_label=self.H3 * 5,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # W3
            line = Segment(
                point_dict["Z2"],
                point_dict["Z2"] + self.W3 * exp(1j * -(pi / 2 + 15 / 180 * pi)),
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="W3",
                offset_label=-1j * 0.01,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

            # H2
            line = Segment(point_dict["Zch"], point_dict["Zcl"])
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H2",
                offset_label=-1j * self.H3 * 3,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )
            # H3
            line = Segment(
                point_dict["Zcm"] + 1j * 0.003 - 0.0001,
                point_dict["Zcl"] + 1j * 0.003 - 0.0001,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                label="H3",
                offset_label=-self.H3 * 2 + 1j * self.H3 * 2,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

            # R1
            line = Segment(point_dict["Zc1"], point_dict["Z7"])
            line.plot(
                fig=fig,
                ax=ax,
                label="R1",
                color=ARROW_COLOR,
                linewidth=ARROW_WIDTH,
                offset_label=self.H3 * 0.8,
                is_arrow=True,
                fontsize=SC_FONT_SIZE,
            )

        if is_add_main_line:
            # Ox axis
            line = Segment(0, lam.Rext * 1.5)
            line.plot(
                fig=fig,
                ax=ax,
                color=MAIN_LINE_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )
            # damper arc
            line = Arc1(
                begin=point_dict["Z9"],
                end=point_dict["Z10"],
                radius=self.get_Rbo(),
                is_trigo_direction=True,
            )
            line.plot(
                fig=fig,
                ax=ax,
                color=ARROW_COLOR,
                linestyle=MAIN_LINE_STYLE,
                linewidth=MAIN_LINE_WIDTH,
            )

        if type_add_active == 1:
            self.plot_active(fig=fig, is_show_fig=False)
        elif type_add_active == 2:
            self.plot_active(
                fig=fig, is_show_fig=False, enforced_default_color=MAGNET_COLOR
            )

        # Zooming and cleaning
        W = (point_dict["Zch"] * exp(1j * sp)).imag
        Rint = min(point_dict["Z2"].real, point_dict["Z1"].real)
        Rext = max(point_dict["Z2"].real, point_dict["Z1"].real)

        ax.axis("equal")
        ax.set_xlim(Rint, Rext)
        ax.set_ylim(-W * 0.9, W * 0.7)
        manager = plt.get_current_fig_manager()
        if manager is not None:
            manager.set_window_title(type(self).__name__ + " Schematics")
        ax.set_title("")
        ax.get_legend().remove()
        ax.set_axis_off()

        # Save / Show
        if save_path is not None:
            fig.savefig(save_path)
            plt.close(fig=fig)

        if is_show_fig:
            fig.show()
        return fig, ax
