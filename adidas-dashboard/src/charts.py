"""
Chart creation module for the Adidas Sales Analytics Dashboard.

All charts use Plotly with a consistent dark professional theme
inspired by Adidas branding (black, white, subtle accents).
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------
COLORS = {
    "primary":    "#FFFFFF",
    "accent":     "#00D4AA",   # Teal-mint accent
    "accent2":    "#FF6B6B",   # Coral accent
    "accent3":    "#4ECDC4",   # Secondary teal
    "accent4":    "#FFE66D",   # Yellow accent
    "accent5":    "#A8E6CF",   # Light green
    "bg":         "#0E1117",
    "card_bg":    "#1A1D23",
    "grid":       "#2A2D35",
    "text":       "#E0E0E0",
    "text_muted": "#8B8D94",
}

# Sequential palette for bar charts
BAR_PALETTE = [
    "#00D4AA", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#FF6B6B", "#C44D58",
    "#F7DC6F", "#BB8FCE",
]

# Gradient palette for multi-series
GRADIENT_PALETTE = ["#00D4AA", "#45B7D1", "#FF6B6B", "#FFE66D", "#A8E6CF", "#DDA0DD"]


def _base_layout(title: str = "", height: int = 420) -> dict:
    """Return shared layout config for all charts."""
    return dict(
        title=dict(
            text=title,
            font=dict(size=16, color=COLORS["text"], family="Inter, sans-serif"),
            x=0.0,
            xanchor="left",
            pad=dict(l=10, t=10),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text_muted"], family="Inter, sans-serif", size=12),
        height=height,
        margin=dict(l=60, r=30, t=60, b=50),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text_muted"], size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis=dict(
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["grid"],
            showgrid=True,
            gridwidth=0.5,
        ),
        yaxis=dict(
            gridcolor=COLORS["grid"],
            zerolinecolor=COLORS["grid"],
            showgrid=True,
            gridwidth=0.5,
        ),
    )


def _format_axis_value(val):
    """Format axis tick values for readability."""
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif abs(val) >= 1_000:
        return f"${val/1_000:.0f}K"
    return f"${val:,.0f}"


# ---------------------------------------------------------------------------
# LINE CHARTS
# ---------------------------------------------------------------------------

def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = None,
    y_prefix: str = "$",
    height: int = 420,
    area: bool = True,
) -> go.Figure:
    """Create a professional line/area chart."""
    line_color = color or COLORS["accent"]

    fig = go.Figure()

    if area:
        fig.add_trace(go.Scatter(
            x=df[x], y=df[y],
            mode="lines",
            line=dict(color=line_color, width=2.5),
            fill="tozeroy",
            fillcolor=f"rgba({_hex_to_rgb(line_color)}, 0.08)",
            hovertemplate=f"%{{x|%b %Y}}<br>{y_prefix}%{{y:,.0f}}<extra></extra>",
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df[x], y=df[y],
            mode="lines+markers",
            line=dict(color=line_color, width=2.5),
            marker=dict(size=5, color=line_color),
            hovertemplate=f"%{{x|%b %Y}}<br>{y_prefix}%{{y:,.0f}}<extra></extra>",
        ))

    layout = _base_layout(title, height)
    layout["yaxis"]["tickprefix"] = y_prefix if y_prefix == "$" else ""
    fig.update_layout(**layout)
    return fig


def create_multi_line_chart(
    df: pd.DataFrame,
    x: str,
    y_columns: list,
    labels: list = None,
    title: str = "",
    height: int = 420,
) -> go.Figure:
    """Create a multi-line chart for comparing metrics."""
    fig = go.Figure()
    labels = labels or y_columns
    colors = GRADIENT_PALETTE

    for i, (col, label) in enumerate(zip(y_columns, labels)):
        c = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col],
            mode="lines",
            name=label,
            line=dict(color=c, width=2),
            hovertemplate=f"{label}: %{{y:,.0f}}<extra></extra>",
        ))

    fig.update_layout(**_base_layout(title, height))
    return fig


# ---------------------------------------------------------------------------
# BAR CHARTS
# ---------------------------------------------------------------------------

def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = None,
    horizontal: bool = False,
    y_prefix: str = "$",
    height: int = 420,
    show_values: bool = True,
    color_sequence: list = None,
) -> go.Figure:
    """Create a professional bar chart."""
    colors = color_sequence or BAR_PALETTE
    bar_colors = [colors[i % len(colors)] for i in range(len(df))]

    if horizontal:
        fig = go.Figure(go.Bar(
            x=df[y], y=df[x],
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(width=0),
                cornerradius=4,
            ),
            hovertemplate=f"%{{y}}<br>{y_prefix}%{{x:,.0f}}<extra></extra>",
            text=[f"{y_prefix}{v:,.0f}" for v in df[y]] if show_values else None,
            textposition="outside",
            textfont=dict(size=11, color=COLORS["text_muted"]),
        ))
    else:
        fig = go.Figure(go.Bar(
            x=df[x], y=df[y],
            marker=dict(
                color=bar_colors,
                line=dict(width=0),
                cornerradius=4,
            ),
            hovertemplate=f"%{{x}}<br>{y_prefix}%{{y:,.0f}}<extra></extra>",
            text=[f"{y_prefix}{v:,.0f}" for v in df[y]] if show_values else None,
            textposition="outside",
            textfont=dict(size=11, color=COLORS["text_muted"]),
        ))

    layout = _base_layout(title, height)
    if not horizontal:
        layout["yaxis"]["tickprefix"] = y_prefix if y_prefix == "$" else ""
    else:
        layout["xaxis"]["tickprefix"] = y_prefix if y_prefix == "$" else ""
    fig.update_layout(**layout)
    return fig


def create_grouped_bar_chart(
    df: pd.DataFrame,
    x: str,
    y_columns: list,
    labels: list = None,
    title: str = "",
    height: int = 420,
) -> go.Figure:
    """Create a grouped bar chart for comparing multiple metrics."""
    fig = go.Figure()
    labels = labels or y_columns
    colors = GRADIENT_PALETTE

    for i, (col, label) in enumerate(zip(y_columns, labels)):
        c = colors[i % len(colors)]
        fig.add_trace(go.Bar(
            x=df[x], y=df[col],
            name=label,
            marker=dict(color=c, cornerradius=3),
            hovertemplate=f"{label}: %{{y:,.0f}}<extra></extra>",
        ))

    layout = _base_layout(title, height)
    layout["barmode"] = "group"
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# DONUT / PIE CHARTS
# ---------------------------------------------------------------------------

def create_donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str = "",
    height: int = 400,
) -> go.Figure:
    """Create a professional donut chart."""
    fig = go.Figure(go.Pie(
        labels=df[names],
        values=df[values],
        hole=0.55,
        marker=dict(
            colors=BAR_PALETTE[:len(df)],
            line=dict(color=COLORS["bg"], width=2),
        ),
        textinfo="label+percent",
        textfont=dict(size=11, color=COLORS["text"]),
        hovertemplate="%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>",
    ))

    layout = _base_layout(title, height)
    layout["showlegend"] = False
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# SCATTER PLOTS
# ---------------------------------------------------------------------------

def create_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str = None,
    size: str = None,
    title: str = "",
    x_label: str = "",
    y_label: str = "",
    height: int = 450,
) -> go.Figure:
    """Create a professional scatter plot."""
    if color and color in df.columns:
        fig = px.scatter(
            df, x=x, y=y, color=color, size=size,
            color_discrete_sequence=GRADIENT_PALETTE,
            hover_data=df.columns.tolist()[:6],
        )
    else:
        fig = go.Figure(go.Scatter(
            x=df[x], y=df[y],
            mode="markers",
            marker=dict(
                color=COLORS["accent"],
                size=8,
                opacity=0.7,
                line=dict(width=0.5, color=COLORS["text_muted"]),
            ),
            hovertemplate=f"{x_label or x}: %{{x:,.0f}}<br>{y_label or y}: %{{y:,.0f}}<extra></extra>",
        ))

    layout = _base_layout(title, height)
    layout["xaxis"]["title"] = x_label or x
    layout["yaxis"]["title"] = y_label or y
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# HELPER
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to RGB string for rgba() usage."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r}, {g}, {b}"
