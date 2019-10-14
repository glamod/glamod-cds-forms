def render_page(out_file, title, body, template="template.html"):

    with open(template) as reader:
        tmpl = reader.read()

    with open(out_file, "w") as writer:
        writer.write(tmpl.format(title=title, body=body))

    print(f"Wrote: {out_file}")


class Section(object):
    def __init__(self, title, note, tooltip, labels=None, n=1, select_all=False, default=None, widget=None,
                 subsections=None):
        self.title = title
        self.note = note
        self.tooltip = tooltip
        self.n = n

        self.labels = labels
        self.select_all = select_all
        self.default = default
        self.widget = widget
        
        self.subsections = subsections

    def _common(self):

        content = ""
        ss = self.subsections
        
        if self.n == 1:
            n_string = self.n
        else:
            n_string = "at least 1 option"
            self.select_all = True

        content += f' <div class="howmany">Please select: {n_string}</div>\n'
        content += ' <div class="aselector">\n'

        for count, label in enumerate(self.labels):
        
            if ss and count in ss:
                value = ss[count]
                content += f'  <div><img class="smallicon" src="arrow.png" /> <b>{value}</b></div>'
                
            if self.default == label:
                checked = "checked=checked"
            else:
                checked = ""

            if len(label) > 40:
                # Put one on each line
                newline = "<br />"
                label = label.replace("&nbsp;", "")
            else:
                newline = ""

            if len(self.labels) < 5:
                # Put on single lines if up to 4
                newline = "<br />"

            content += f'  <input type="checkbox" class="acheckbox" {checked}>{label}</input>{newline}\n'

        content += " </div>\n"

        if self.select_all:
            content += ' <div class="aselectall"><a href="#">Select all</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="#">Clear all</a></div>\n'
        else:
            content += ' <div class="aselectall"><a href="#">Clear</a></div>\n'

        return content

    def _render_bbox(self):
        content = ' <div class="howmany">Please select: a valid domain</div>\n'

        content += (
            ' <div class="padmid"><input type="text" size="7" value="90.0" /> N</div>'
        )
        content += " <div>\n"
        content += '   <span class="padleft"><input type="text" size="7" value="-180.0" /> W</span>\n'
        content += '   <span class="padright"><input type="text" size="7" value="180.0" /> E</span>\n'
        content += " </div>\n"
        content += (
            ' <div class="padmid"><input type="text" size="7" value="-90.0" /> S</div>'
        )

        content += ' <div class="aselectall"><a href="#">Reset bounding box</a></div>\n'

        return content

    def _render_location(self):
        content = ' <div class="howmany">Please select: a valid location</div>\n'

        content += " <div>\n"
        content += '   <span class="padleft"><input type="text" size="7" value="0.0" /> N</span>\n'
        content += '   <span class="padmid"><input type="text" size="7" value="0.0" /> E</span>\n'
        content += " </div>"

        content += ' <div class="aselectall"><a href="#">Reset location</a></div>\n'

        return content

    def _render_widget(self):
        if self.widget == "bbox":
            return self._render_bbox()
        elif self.widget == "location":
            return self._render_location()

    def render(self):
        body = '<div class="abox">\n'
        body += f' <div class="atitle">{self.title} <span title="{self.tooltip}">'
        body += f'<img class="smallicon" src="tooltip_icon.png" /></span>'
        body += f'<span class="smalltext">{self.tooltip}</span></div>\n'

        body += f' <div class="note">{self.note}</div>\n'

        if self.widget:
            body += self._render_widget()
        else:
            body += self._common()

        body += "</div>\n"

        return body


def format_strings(l):
    longest = max([len(i) for i in l])
    pad = "&nbsp;"

    n = []
    for i in l:
        x = i
        diff = longest - len(x)

        x += pad * diff
        n.append(x)

    return n


def main():

    mockup_land()
    mockup_marine()


def mockup_land():
    body = ""
    title = (
        "Download data: Surface land meteorological station holdings"
    )

    # Time frequency
    options = ["Monthly", "Daily", "Sub-daily"]
    labels = format_strings(options)
    section = Section(
        "Time frequency",
        "The time-step or frequency of observations",
        "Selecting this will constrain the time selections shown below",
        labels,
    )
    body += section.render()

    """
    # Query type
    options = [
        "Single location query (over time series)",
        "Bounding box query (limited times)",
    ]
    labels = format_strings(options)
    section = Section(
        "Query type",
        "Defines which constraints spatial and temporal constraints will be applied to the query",
        "Selecting this will constrain the spatial and temporal selections below",
        labels,
    )
    body += section.render()
"""

    # Bounding Box
    section = Section(
        "Bounding box",
        "Defines a spatial domain in which to select data. "
        "Selecting a large area will reduce the available time range that you can select. ",
        "Selecting some areas of the globe will generate an empty result set",
        widget="bbox",
    )
    body += section.render()

    """# Location
    section = Section(
        "Location",
        "Defines a single location for which to select data. "
        "ONLY AVAILABLE IF Query Type is a Location.",
        "Select a location and the tool will find the nearest 5 stations/observation sets for time series selected",
        widget="location",
    )
    body += section.render()
"""

    # Variable
    options = """
Monthly maximum air temperature [K]
Monthly minimum air temperature [K]
Monthly mean air temperature [K]
Daily maximum air temperature [K]
Daily minimum air temperature [K]
Daily mean air temperature [K]
Daily Dew point temperature [K]
Daily Accumulated precipitation [mm]
Daily Fresh snow [mm]
Daily Snow depth [cm]
Daily Snow water equivalent [mm]
Daily Surface air pressure at sea level [Pa]
Daily Surface air pressure at specified height [Pa]
Daily Wind speed [m s-1]
Sub-daily Air temperature [K]
Sub-daily Dew point temperature [K]
Sub-daily Dew point temperature [K]
Sub-daily Fresh snow [mm]
Sub-daily Snow depth [cm]
Sub-daily Snow water equivalent [mm]
Sub-daily Surface air pressure at sea level [Pa]
Sub-daily Surface air pressure at specified height [Pa]
Sub-daily Wind speed [m s-1]
Sub-daily wind from direction [degree]
""".strip().split('\n')

    labels = format_strings(options)
    subsections = {0: 'Monthly variables - available if time frequency is: <b>Monthly</b>', 
                   3: 'Daily variables - available if time frequency is: <b>Daily</b>', 
                   14: 'Sub-daily variables - available if time frequency is: <b>Sub-daily</b>'}
    
    note = "NOTE: The outputs will only include variables found within the domain specified in the request."    
    section = Section(
        "Variable",
        "Select one or more of the available variables of interest",
        "You can select as many variables as you like",
        labels,
        n="+", subsections=subsections
    )
    body += section.render()

    # Year
    options = ['1761-1790', '1791-1820', '1821-1850', '1851-1880', '1881-1910']
    options += [str(year) for year in range(1911, 2019)]
    labels = format_strings(options)
    section = Section(
        "Year",
        "Historical data can be selected in larger chunks because "
        "more data will be available in recent years.",
        "Select one or more options",
        labels,
        n="+",
    )
    body += section.render()

    # Month
    options = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    labels = format_strings(options)
    section = Section(
        "Month", "Months that you require", "Months required", labels, n="+"
    )
    body += section.render()

    # Day
    options = [f"{day:02d}" for day in range(1, 32)]
    labels = format_strings(options)
    section = Section(
        "Day",
        "Days that you require",
        "This selection is ONLY AVAILABLE for &quot;Daily&quot; and &quot;Sub-daily&quot; time-steps.",
        labels,
        n="+",
    )
    body += section.render()

    # Intended use
    labels = format_strings(["Non-commercial", "Commercial"])
    section = Section(
        "Intended use",
        "How you intend to use the data",
        "Selecting this will reduce the number of observations available, due to usage restrictions",
        labels,
        default="Non-commercial",
    )
    body += section.render()

    # Data Quality
    options = ["Quality controlled", "All data"]
    labels = format_strings(options)
    section = Section(
        "Data Quality",
        "Quality control level required",
        "Selecting &quot;Quality controlled&quot; will only return observations that have passed a certain level of QC (e.g. World Weather Record checks).",
        labels,
        default="Quality controlled",
    )
    body += section.render()

    # Partial record options
    default = "Only download records where all chosen variables are available"
    options = [
        default,
        "Download all records where one or more of the chosen varaibles is available",
    ]
    labels = format_strings(options)
    text = "Decide whether to receive records at time steps when all your chosen variables are not available"
    section = Section(
        "Select full or partial records",
        text,
        text,
        labels,
        default=labels[0]
    )
    body += section.render()

    # Format
    options = ["CSV (zipped)", "JSON (zipped)"]
    labels = format_strings(options)
    section = Section(
        "Format",
        "Data format",
        "Zipped outputs will be smaller in volume, they may contain multiple data files.",
        labels,
        default=labels[0],
    )
    body += section.render()

    render_page("land-mockup.html", title, body)


def mockup_marine():
    body = ""
    title = "Download data: In situ sub-daily surface marine observations from 1946"

    """# Query type
    options = [
        "Small location query (over time series)",
        "Bounding box query (limited times)",
    ]
    labels = format_strings(options)
    section = Section(
        "Query type",
        "Defines which constraints spatial and temporal constraints will be applied to the query",
        "Selecting this will constrain the spatial and temporal selections below",
        labels,
    )
    body += section.render()
"""
    # Bounding Box
    section = Section(
        "Bounding box",
        "Defines a spatial domain in which to select data. "
        "Selecting a large area will reduce the available time range that you can select. ",
        "Selecting some areas of the globe will generate an empty result set",
        widget="bbox",
    )
    body += section.render()

    """# Location
    section = Section(
        "Location",
        "Defines the centre of a 1&deg; x 1&deg; polygon in which to search for marinedata. "
        "ONLY AVAILABLE IF Query Type is a Location.",
        "Select a location and the tool will find all observations within the 1&deg; x 1&deg; polygon around that point for time series selected",
        widget="location",
    )
    body += section.render()
"""
    # Variable
    options = [
        "Air temperature [K]",
        "Wet bulb temperature [K]",
        "Water temperature (sea surface temperature) [K]",
        "Air pressure [Pa]",
        "Air pressure at sea level [Pa]",
        "Wind from direction [degrees true]",
        "Wind speed [m s^-1]",
    ]
    labels = format_strings(options)
    note = "NOTE: The outputs will only include variables found within the domain specified in the request."
    section = Section(
        "Variable",
        "Select one or more of the available variables of interest",
        "You can select as many variables as you like",
        labels,
        n="+",
    )
    body += section.render()

    """# Station type
    options = ["Sea stations"]
    labels = format_strings(options)
    section = Section(
        "Station type",
        "The type of station recording the observation",
        "Select the option",
        labels,
        default=labels[0],
    )
    body += section.render()
"""
    # Platform type
    options = ["Ship", "Drifting buoy"]
    labels = format_strings(options)
    section = Section(
        "Platform type",
        "The type of platform from which the measurements were made",
        "Select one or more options",
        labels,
        n="+",
    )
    body += section.render()

    # Year
    options = [str(year) for year in range(1946, 2019)]
    labels = format_strings(options)
    section = Section(
        "Year",
        "More data will be available in recent years.",
        "Select one or more options",
        labels,
        n="+",
    )
    body += section.render()

    # Month
    options = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    labels = format_strings(options)
    section = Section(
        "Month", "Months that you require", "Months required", labels, n="+"
    )
    body += section.render()

    # Day
    options = [f"{day:02d}" for day in range(1, 32)]
    labels = format_strings(options)
    section = Section("Day", "Days that you require", "Days required", labels, n="+")
    body += section.render()

    # Hour
    options = [f"{day:02d}" for day in range(24)]
    labels = format_strings(options)
    section = Section("Hour", "Hours that you require", "Hours required", labels, n="+")
    body += section.render()

    """# Intended use
    labels = format_strings(["Non-commercial", "Commercial"])
    section = Section(
        "Intended use",
        "How you intend to use the data",
        "Selecting this will reduce the number of observations available, due to usage restrictions",
        labels,
        default=labels[0],
    )
    body += section.render()
"""
    # Data Quality
    options = ["Quality controlled", "All data"]
    labels = format_strings(options)
    section = Section(
        "Data Quality",
        "Quality control level required",
        "Selecting &quot;Quality controlled&quot; will only return observations that have passed a certain level of QC (e.g. World Weather Record checks).",
        labels,
        default=labels[0],
    )
    body += section.render()

    # Partial record options
    default = "Only download records where all chosen variables are available"
    options = [
        default,
        "Download all records where one or more of the chosen varaibles is available",
    ]
    labels = format_strings(options)
    text = "Decide whether to receive records at time steps when all your chosen variables are not available"
    section = Section(
        "Select full or partial records",
        text,
        text,
        labels,
        default=labels[0]
    )
    body += section.render()

    # Format
    options = ["CSV (zipped)", "JSON (zipped)"]
    labels = format_strings(options)
    section = Section(
        "Format",
        "Data format",
        "Zipped outputs will be smaller in volume, they may contain multiple data files.",
        labels,
        default=labels[0],
    )
    body += section.render()

    render_page("marine-mockup.html", title, body)


if __name__ == "__main__":

    main()
