import os
import datetime
from tools import indices, ficc, us_plots, top_movers, calendar, mainnews, tablestyle, misc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table, Paragraph, Spacer, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus.flowables import Image, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

#------------------------------------------------------------
# Initialize
COMPANY_NAME = "LOREM IPSUM<br />COMPANY" # Use <br /> to break lines
AUTHOR = "HGNX"
AUTHOR_EMAIL = "contact@hgk.im"

DATE = datetime.datetime.now().strftime("%Y-%m-%d")
DATE_FILENAME = datetime.datetime.now().strftime("%Y%m%d")
FILE_NAME = "output.pdf"

ASSETS_FOLDER = os.path.join(os.getcwd(), "assets")
FONT = os.path.join(ASSETS_FOLDER, "NotoSansKR[wght].ttf")
pdfmetrics.registerFont(TTFont('NotoSansKR', FONT))
#------------------------------------------------------------

#------------------------------------------------------------
# Add fonts and initialize PDF template
class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        frame_x = (A4[0] - 6*inch) / 2
        template = PageTemplate('normal', [Frame(frame_x, 1*inch, 6*inch, 10*inch)])
        self.addPageTemplates(template)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__ == Paragraph:
            text = flowable.getPlainText()
            self.notify('TOCEntry', (text, self.page))

doc = MyDocTemplate(FILE_NAME,
                    pagesize=A4,
                    title=f"Report_{DATE_FILENAME}",
                    author=f"{AUTHOR} ({AUTHOR_EMAIL})",
                    subject=misc.src)
#------------------------------------------------------------

#------------------------------------------------------------
# Set header
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=1, fontSize=14, spaceAfter=20, textColor=colors.black, fontWeight='bold'))

left_style = ParagraphStyle(name='Left', parent=styles['Normal'], alignment=0)
center_style = ParagraphStyle(name='Center', parent=styles['Normal'], alignment=1, fontSize=14, spaceAfter=20, textColor=colors.black, fontWeight='bold', leading=18)
right_style = ParagraphStyle(name='Right', parent=styles['Normal'], alignment=2, fontSize=8, leading=10)

header = [
    [
        Paragraph(COMPANY_NAME, left_style),
        "", 
        Paragraph("<b>STOCK MARKET<br />DAILY REPORT</b>", center_style),
        "", 
        Paragraph(f"{AUTHOR}<br />{AUTHOR_EMAIL}<br />{DATE}", right_style)
    ]
]

header_table = Table(header, colWidths=[1.5*inch, 0.5*inch, 3*inch, 0.5*inch, 1.5*inch])
header_table.setStyle(tablestyle.header_style)

story = [header_table, Spacer(1, 0.3*inch)]
#------------------------------------------------------------

#------------------------------------------------------------
# Add captions
caption_style = ParagraphStyle(name='Caption', parent=styles['Normal'], fontSize=7, alignment=0)
caption_style2 = ParagraphStyle(name='Caption', parent=styles['Normal'], fontSize=7, alignment=0, leading=5)
caption_indices = Paragraph("● Global Market Indices", caption_style)
caption_ficc = Paragraph("● FICC", caption_style)
caption_gainers = Paragraph("● Top Gainers", caption_style)
caption_losers = Paragraph("● Top Losers", caption_style)
caption_events = Paragraph("● Key Events Today", caption_style2)
#------------------------------------------------------------

#------------------------------------------------------------
# Get indices, and ficc data
print("********** Getting indices data **********")
table_indices_data = indices.get_all_indices_data()
print("********** Getting ficc data **********")
table_ficc_data = ficc.get_all_ficc_data()
#------------------------------------------------------------

#------------------------------------------------------------
# Generate indices intraday change and main sectors change charts
print("********** Generating charts **********")
us_plots.create_plots()

nasdaq_graph = Image(os.path.join(ASSETS_FOLDER, "nasdaq.png"), 2.4*inch, 1.6*inch)
sp500_graph = Image(os.path.join(ASSETS_FOLDER, "sp500.png"), 2.4*inch, 1.6*inch)
sectors_graph = Image(os.path.join(ASSETS_FOLDER, "sectors.png"), 2.4*inch, 1.6*inch)  # Increased the height

table_graph_data = [
    nasdaq_graph, 
    Spacer(0.1*inch, 0), 
    sp500_graph, 
    Spacer(0.1*inch, 0), 
    sectors_graph
]
table_graph = Table([table_graph_data], colWidths=[2.4*inch, 0.001*inch, 2.4*inch, 0.001*inch, 2.4*inch])
#------------------------------------------------------------

#------------------------------------------------------------
# Get top movers data
print("********** Getting top movers data **********")
table_gainers_data, table_losers_data = top_movers.get_top_movers_data()
#------------------------------------------------------------

#------------------------------------------------------------
# Get economic calendar data
print("********** Getting economic calendar data **********")
table_events_data = calendar.get_all_economic_data()
#------------------------------------------------------------

#------------------------------------------------------------
# Get headlines data from Reuters, Financial Times
def add_news_items(news_items):
    items = []
    for title, url in news_items:
        p = Paragraph(f"{mainnews.format_news_title(title)}<br />{mainnews.format_news_url(url)}",
                        ParagraphStyle('Left', parent=styles['Normal'], alignment=0, fontName='NotoSansKR'))
        items.extend(([p], [Spacer(1, 0.2 * inch)]))
    return items

def add_news_source(source, news_items):
    source_paragraph = [Paragraph(f"<b>● {source}</b>", styles['BodyText'])]
    return [source_paragraph] + add_news_items(news_items)

print("********** Getting news data **********")
reuters_news, ft_news = mainnews.get_shortened_news()

news_sources = [
    ("Reuters - Macro Matters", reuters_news),
    ("Financial Times - Most Read: Markets", ft_news)
]

news_result = [row for source, news_items in news_sources for row in add_news_source(source, news_items)]
#------------------------------------------------------------

#------------------------------------------------------------
# Make tables and set styles
ADDITIONAL_SPACE = 0.3 * inch
TOTAL_TABLE_WIDTH = 6 * inch - 0.1 * inch - ADDITIONAL_SPACE
SINGLE_TABLE_WIDTH = TOTAL_TABLE_WIDTH / 2
COLUMN_WIDTH = SINGLE_TABLE_WIDTH / 6
TABLE_ROW_HEIGHT = 0.15 * inch
SPACER_WIDTH = 0.1 * inch

def create_table(data, column_widths, row_heights, styles):
    table = Table(data, column_widths, row_heights)
    table.setStyle(styles)
    return table

# Indices and FICC tables
column_widths_overview = [COLUMN_WIDTH] * 7
table_indices = create_table(table_indices_data, column_widths_overview, [TABLE_ROW_HEIGHT] * len(table_indices_data), tablestyle.common_style + tablestyle.overview_style)
table_ficc = create_table(table_ficc_data, column_widths_overview, [TABLE_ROW_HEIGHT] * len(table_ficc_data), tablestyle.common_style + tablestyle.overview_style)

table_overview_data = [[caption_indices, Spacer(SPACER_WIDTH, 0), caption_ficc], [table_indices, Spacer(SPACER_WIDTH, 0), table_ficc]]
table_overview = Table(table_overview_data)

# Top movers table
mover_column_widths = [COLUMN_WIDTH * 0.9, COLUMN_WIDTH * 2.5] + [COLUMN_WIDTH * 1.2] * 3
table_gainers = create_table(table_gainers_data, mover_column_widths, [TABLE_ROW_HEIGHT] * len(table_gainers_data), tablestyle.common_style + tablestyle.movers_style)
table_losers = create_table(table_losers_data, mover_column_widths, [TABLE_ROW_HEIGHT] * len(table_losers_data), tablestyle.common_style + tablestyle.movers_style)

table_mover_data = [[caption_gainers, Spacer(SPACER_WIDTH, 0), caption_losers], [table_gainers, Spacer(SPACER_WIDTH, 0), table_losers]]
table_mover = Table(table_mover_data)

# Economic calendar table
table_events_width = sum(mover_column_widths) * 2.133
event_column_widths = [table_events_width / 6] * 2 + [table_events_width - 4*(table_events_width / 6)] + [table_events_width / 6] * 2
table_events_data_modified = [[caption_events], [Spacer(SPACER_WIDTH, 0)], *table_events_data]
table_events = create_table(table_events_data_modified, event_column_widths, [TABLE_ROW_HEIGHT] * len(table_events_data_modified), tablestyle.common_style + tablestyle.events_style)

# News table
table_news = create_table(news_result, [7.1*inch], None, tablestyle.news_style)
#------------------------------------------------------------

#------------------------------------------------------------
# Add tables and divider lines then build PDF
story.append(table_overview)
story.append(Spacer(1, 0.3*inch))
story.append(table_graph)
story.append(Spacer(1, 0.3*inch))
story.append(table_mover)
story.append(Spacer(1, 0.3*inch))
story.append(table_events)
story.append(PageBreak())
story.append(header_table)
story.append(Spacer(1, 0.3*inch))
story.append(table_news)
doc.build(story)
#------------------------------------------------------------

#------------------------------------------------------------
# Remove used images
image_files = ["nasdaq.png", "sp500.png", "sectors.png"]
for image_file in image_files:
    image_path = os.path.join(ASSETS_FOLDER, image_file)
    if os.path.exists(image_path):
        os.remove(image_path)
#------------------------------------------------------------

print('Done!')